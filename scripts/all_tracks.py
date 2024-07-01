# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script is designed to visualize tropical cyclone (TC) tracks in the Gulf of Mexico,
# colored by maximum sustained wind speeds. The visualization covers a defined grid with
# specified geographic boundaries and grid size.
#
# Key operations include:
# - Defining grid boundaries and creating a 2D grid to store counts.
# - Using the Basemap toolkit to plot the geographic map and TC tracks.
# - Reading TC data and plotting each TC track with colors representing wind speed.
#
# The final outputs are:
# 1. A visualization of TC tracks across the Gulf of Mexico with color indicating wind speed.
# 2. A PDF file titled 'tc_tracks_colored_by_wind.pdf' which provides a detailed visual 
#    representation suitable for reports or further analysis.
#
# For a comprehensive methodology and further details, refer to:
# Radfar, S., Moftakhari, H., and Moradkhani, H. (2024), Visualization of tropical cyclone activity 
# in the Gulf of Mexico using wind speed data, Communications Earth & Environment.
# Link: [Insert link here]
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
from matplotlib.colors import Normalize

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

# Create a 2D grid of zeros to store the counts
count_grid = np.zeros((len(lat_centers), len(lon_centers)))

# Create the Basemap object for plotting the grid
m = Basemap(projection='merc', llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='l')

# Plot the grid
plt.figure(figsize=(8, 6))
m.drawcoastlines()
m.drawparallels(np.arange(15, 32, 5), labels=[True, False, False, False], fontsize=12)
m.drawmeridians(np.arange(-100, -77, 5), labels=[False, False, False, True], fontsize=12)
m.fillcontinents(color='lightgrey')

# Add labels to important locations
important_locations = {
    'Gulf of Mexico': (25, -90),
    'Florida': (27, -81),
    'Texas': (29, -98),
    'Mexico': (18, -97),
    'Cuba': (22.1, -80.5),
    'Carribean Sea': (18, -83),
}

for location, (lat, lon) in important_locations.items():
    x, y = m(lon, lat)
    plt.text(x, y, location, fontsize=12, color='black', ha='center', va='bottom')

# Read TC data from ibtracts_data.csv
tc_data = pd.read_csv('ibtracs_data.csv')

# Create a colormap based on Spectral_r ranging from 10 to 165
cmap = plt.cm.get_cmap('Spectral_r')
norm = Normalize(vmin=10, vmax=165)

# Iterate over TC data to plot the tracks and color segments
for season, group_data in tc_data.groupby(['SEASON', 'NAME']):
    lat = group_data['LAT'].values
    lon = group_data['LON'].values
    wind_speed = group_data['USA_WIND'].values

    x, y = m(lon, lat)
    for i in range(1, len(lat)):
        mean_wind_speed = (wind_speed[i - 1] + wind_speed[i]) / 2
        color = cmap(norm(mean_wind_speed))
        m.plot(x[i - 1:i + 1], y[i - 1:i + 1], color=color, linewidth=0.5)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, label='Maximum sustained wind speed (Knots)', orientation='vertical')

# Save the figure as a PDF
plt.savefig('tc_tracks_colored_by_wind.pdf', format='pdf', bbox_inches='tight')

plt.show()
