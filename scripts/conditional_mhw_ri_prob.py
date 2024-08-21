# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script quantitatively analyzes and visually represents the spatial distribution 
# and probabilities of rapid intensification (RI) events of tropical cyclones in the Gulf of Mexico 
# during marine heatwaves (MHWs). It computes the counts of unique hurricanes and RI events within a defined 
# spatial grid covering the Gulf of Mexico and the northwestern Carribean Sea and calculates the multiplication rate of RI events during MHWs.
# The primary outputs are heatmaps that visualize:
# - The multiplication rate of RI events during MHWs.
#
# Outputs:
# - A visual map of the Gulf of Mexico showing the probability of RI events in each grid cell 
#   during marine heatwaves, providing a clear visual indicator of the areas most likely to experience 
#   rapid intensification of hurricanes.
# - The final map is saved as a PDF titled 'Cond_grdd_41_24.pdf', suitable for inclusion 
#   in reports or presentations.
#
# For a detailed description of the methodologies and further insights, please refer to:
# Radfar, S., Moftakhari, H. & Moradkhani, H. Rapid intensification of tropical cyclones in the Gulf of Mexico is more likely during marine heatwaves. Commun Earth Environ 5, 421 (2024).
# Link: https://doi.org/10.1038/s43247-024-01578-2
#
# Disclaimer:
# This script is intended for research and educational purposes only. It is provided 'as is' 
# without warranty of any kind, express or implied. The developers assume no responsibility for 
# errors or omissions in this script. No liability is assumed for damages resulting from the use 
# of the information contained herein.
#
# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.stats import norm
from scipy import stats
from tqdm import tqdm

# Define the grid size and boundaries
lat_min = 15
lat_max = 31
lon_min = -100
lon_max = -78
grid_size = 1

# Define the grid edges
lon_edges = np.arange(lon_min, lon_max + grid_size, grid_size)
lat_edges = np.arange(lat_min, lat_max + grid_size, grid_size)

# Define the grid centers
lon_centers = lon_edges[:-1] + grid_size / 2
lat_centers = lat_edges[:-1] + grid_size / 2

# Initialize the grid counts and probabilities
grid_counts = np.zeros((len(lat_centers), len(lon_centers)))
hurr_counts = np.zeros((len(lat_centers), len(lon_centers)))
grid_probs = np.zeros((len(lat_centers), len(lon_centers)))

# Load the MHW data
hi_data = pd.read_csv('../MHW_info_41_24.csv')
hurr_data = pd.read_csv('../intensifications30_IID_24.csv')

# Index finder
i_HI_lat = len(lat_edges) - np.searchsorted(lat_edges, hi_data['HI_lat'], 'right') - 1
i_HI_lon = np.searchsorted(lon_edges, hi_data['HI_lon'], 'left') - 1

# Append i_HI_lat and i_HI_lon columns to hi_data
hi_data = hi_data.assign(i_HI_lat=i_HI_lat, i_HI_lon=i_HI_lon)

# Sort the data by i_lat and i_lon
dataa = hi_data.sort_values(by=['i_HI_lat', 'i_HI_lon'])

# Initialize a set to keep track of unique hurricanes
unique_hurr = set()

# Iterate over each row of the data
for row in dataa.itertuples():
    i_lat, i_lon, date, name = row.i_HI_lat, row.i_HI_lon, row.HI_date, row.HI_name
    
    # Ignore rows with hurricane name 'NOT_NAMED'
    if name == 'NOT_NAMED':
        continue
    
    # Check if the current hurricane is unique within the current grid
    if (i_lat, i_lon, name) not in unique_hurr:
        
        # Increment the counts of the central and surrounding grids
        for i in range(max(0, i_lat - 1), min(i_lat + 2, len(lat_centers))):
            for j in range(max(0, i_lon - 1), min(i_lon + 2, len(lon_centers))):
                grid_counts[i, j] += 1
                
        # Add the current hurricane to the set of unique hurricanes
        unique_hurr.add((i_lat, i_lon, name))

# Sort the data by i_lat and i_lon
data = hurr_data.sort_values(by=['i_HI_lat', 'i_HI_lon'])

# Initialize a set to keep track of unique hurricanes
unique_hurricanes = set()

# Iterate over each row of the data
for row in data.itertuples():
    i_lat, i_lon, date, name = row.i_HI_lat, row.i_HI_lon, row.HI_date, row.HI_name
    
    # Ignore rows with hurricane name 'NOT_NAMED'
    if name == 'NOT_NAMED':
        continue
    
    # Check if the current hurricane is unique within the current grid
    if (i_lat, i_lon, name) not in unique_hurricanes:
        
        # Increment the counts of the central and surrounding grids
        for i in range(max(0, i_lat - 1), min(i_lat + 2, len(lat_centers))):
            for j in range(max(0, i_lon - 1), min(i_lon + 2, len(lon_centers))):
                hurr_counts[i, j] += 1
                
        # Add the current hurricane to the set of unique hurricanes
        unique_hurricanes.add((i_lat, i_lon, name))
            
# Calculate the probabilities
total_mhw_events = len(hurr_data)
grid_probs = 100 * (grid_counts / total_mhw_events)
non_mhw = 100 - grid_probs
rate = grid_probs / non_mhw

# Replace nan values in rate array where mhw_probs > 0 and non_mhw = 0
mask = np.logical_and(np.isinf(grid_probs), grid_probs == 0, non_mhw > 0)
grid_probs[mask] = 0

# Ignore cells with 0, inf, and nan values
ignored_matrix = np.ma.masked_invalid(rate)
ignored_matrix = np.ma.masked_equal(ignored_matrix, 0)

# Mask the grids with cond_probs = 0 and set their color to blue
masked_grid_probs = np.ma.masked_where(grid_probs == 0, grid_probs)
cmap = plt.get_cmap('Reds')
cmap.set_bad('#CCECFF')
masked_grid = masked_grid_probs / 100

# Create the Basemap object and draw the heatmap
m = Basemap(projection='merc', llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='l')
lon_centers_2d, lat_centers_2d = np.meshgrid(lon_centers, lat_centers)
x, y = m(lon_centers_2d, lat_centers_2d)
plt.figure(figsize=(8, 6))
quadmesh = m.pcolormesh(x, y, masked_grid[::-1], cmap=cmap)
m.drawcoastlines()

colorbar = plt.colorbar(quadmesh, orientation='horizontal', pad = 0.07, shrink=0.72) # Add color bar label
colorbar.ax.tick_params(labelsize=10)
colorbar.set_label('Probability', fontsize=10)
m.fillcontinents(color='lightgrey')
plt.rcParams['hatch.linewidth'] = 0.6

# Add latitude and longitude labels
lat_labels = np.arange(15, 32, 5)
lon_labels = np.arange(-100, -77, 5)
m.drawparallels(lat_labels, labels=[True, False, False, False], fontsize=12)
m.drawmeridians(lon_labels, labels=[False, False, False, True], fontsize=12)

plt.savefig('Cond_grdd_41_24.pdf') # save the figure as a PDF
plt.show()
