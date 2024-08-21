"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
% Center for Complex Hydrosystems Research
% Department of Civil, Construction, and Environmental Engineering
% The University of Alabama
%
% Last modified on June 28, 2024
%
% This script is designed to quantitatively analyze and visually represent the spatial distribution 
% and probabilities of rapid intensification (RI) events of tropical cyclones in the Gulf of Mexico. 
% It computes the frequency of occurrence and conditional probabilities of RI events within a defined 
% spatial grid covering the Gulf of Mexico. The primary outputs are heatmaps that visualize:
% 1. The spatial density of RI events.
% 2. The conditional probability of RI occurrences across the region.
%
% For details on the research framework and methodologies, refer to:
% Radfar, S., Moftakhari, H. & Moradkhani, H. Rapid intensification of tropical cyclones in the Gulf of Mexico is more likely during marine heatwaves. Commun Earth Environ 5, 421 (2024).
% Link: https://doi.org/10.1038/s43247-024-01578-2
%
% Disclaimer:
% This script is designed for instructional, educational, and research use only.
% Commercial use is prohibited. This script is provided 'as is' without warranty of any kind,
% either express or implied. The user assumes all risks and responsibilities for any damage.
% The author and their affiliate institution accept no responsibility for errors or omissions.
% In no event shall the author or their affiliate institution be liable for any special, indirect,
% or consequential damages or any damages whatsoever arising out of or in connection with the
% use of this script.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

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
grid_probs = np.zeros((len(lat_centers), len(lon_centers)))

# Load the MHW data
hi_data = pd.read_csv('../intensifications30_IID_24.csv')
hi_groups = hi_data.groupby(['HI_lat', 'HI_lon', 'HI_name'])

# Iterate over each row of the data
for group_key, group_data in tqdm(hi_groups, total=len(hi_groups), desc='Calculating number of co-occurrence'):
    
    hi_lat, hi_lon, hi_name = group_key
    
    # Find the index of the grid the HI event belongs to
    i_lat = len(lat_edges) - np.searchsorted(lat_edges, hi_lat, 'right') - 1
    i_lon = np.searchsorted(lon_edges, hi_lon, 'left') - 1
    
    # Increment the counts of the central and surrounding grids
    for i in range(max(0, i_lat - 1), min(i_lat + 2, len(lat_centers))):
        for j in range(max(0, i_lon - 1), min(i_lon + 2, len(lon_centers))):
            grid_counts[i, j] += 1
    
# Calculate the probabilities
total_mhw_events = len(hi_data)
grid_probs = 100 * (grid_counts / total_mhw_events)

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

plt.savefig('Figure 4.pdf') # save the figure as a PDF
plt.show()
