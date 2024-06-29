# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script is designed to visualize tropical cyclone (TC) tracks in the Gulf of Mexico,
# specifically highlighting those that made landfall and those that underwent rapid intensification (RI)
# prior to landfall. It uses data from multiple CSV files to plot these tracks on a geographic grid.
#
# Key Features:
# - Sets up a geographic grid covering the Gulf of Mexico.
# - Plots TC tracks with distinct colors to differentiate between TCs that made landfall and those
#   that also experienced RI.
# - Labels significant locations within the Gulf of Mexico for reference.
# - Adds a legend to help identify the different track types.
#
# Outputs:
# - A visual map of TC tracks differentiated by landfall and RI status, saved as a PDF file 
#   titled 'tc_tracks_with_landfall_and_ri.pdf'. This map provides a clear visual distinction
#   between the paths of TCs based on their characteristics.
#
# Methodology:
# The script reads tropical cyclone data and RI event data from CSV files, then filters and
# categorizes them to plot with specific attributes. Tracks are plotted on a Basemap instance
# using matplotlib, where each track's characteristics (landfall, RI) determine its color on the map.
#
# For comprehensive details on the methodology and further implications, please refer to:
# Radfar, S., Moftakhari, H., and Moradkhani, H. (2024), Visualization of tropical cyclone activity
# in the Gulf of Mexico: Differentiating landfall and rapid intensification, Communications Earth & Environment.
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
import matplotlib.patches as mpatches

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

# Read intensifications data from intensifications_24.csv
intensifications_data = pd.read_csv('intensifications_24.csv')

# Get unique SEASON and NAME combinations from intensifications data
landfall_events = intensifications_data[['SEASON', 'NAME']].drop_duplicates()

# Read intensifications data from intensifications_24 - Copy.csv
intensifications_copy_data = pd.read_csv('intensifications_24 - Copy.csv')

# Get unique SEASON and NAME combinations from intensifications copy data
ri_events = intensifications_copy_data[['SEASON', 'NAME']].drop_duplicates()

# Create legend handles for black and red lines
black_patch = mpatches.Patch(color='cyan', label='Landfalling no RI TCs')
red_patch = mpatches.Patch(color='violet', label='Landfalling RI TCs')

# Add legend with the created handles
plt.legend(handles=[black_patch, red_patch], loc='lower left')

# Iterate over TC data to plot the tracks for TCs with landfall in red and both landfall and RI in blue
for season, name in landfall_events.itertuples(index=False):
    group_data = tc_data[(tc_data['SEASON'] == season) & (tc_data['NAME'] == name)]
    lat = group_data['LAT'].values
    lon = group_data['LON'].values
    x, y = m(lon, lat)
    m.plot(x, y, color='cyan', linewidth=0.5)

for season, name in ri_events.itertuples(index=False):
    group_data = tc_data[(tc_data['SEASON'] == season) & (tc_data['NAME'] == name)]
    lat = group_data['LAT'].values
    lon = group_data['LON'].values
    x, y = m(lon, lat)
    m.plot(x, y, color='violet', linewidth=0.5)

# Save the figure as a PDF
plt.savefig('tc_tracks_with_landfall_and_ri.pdf', format='pdf', bbox_inches='tight')

plt.show()
