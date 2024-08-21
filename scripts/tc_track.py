# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script visualizes tropical cyclone (TC) tracks, highlighting periods of rapid
# intensification (RI) based on data from intensifications30_IID_24.csv. It uses
# geographical plotting to depict the paths of TCs over a defined grid area covering
# the Gulf of Mexico.
#
# Features of the script:
# - Parses intensification data to identify periods of RI within specific cyclone tracks.
# - Plots all TC tracks on a geographic grid with specific segments marked to denote RI.
# - Enhances visual representation through the use of Basemap for plotting and matplotlib
#   for customization.
#
# Outputs:
# - A visual map of TC tracks where segments of rapid intensification are highlighted in red,
#   providing a clear visual indicator of when and where these events occurred within the
#   lifecycle of the cyclones.
# - The final map is saved as a PDF titled 'tc_tracks_with_red_segments.pdf', suitable for
#   inclusion in reports or presentations.
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
import matplotlib.patches as mpatches

# Read the intensifications data from intensifications30_IID_24.csv
intensifications_data = pd.read_csv('intensifications30_IID_24.csv')

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

# Read TC data from ibtracts_data.csv
tc_data = pd.read_csv('ibtracs_data.csv')

# Convert 'ISO_TIME' column in TC data to datetime objects
tc_data['ISO_TIME'] = pd.to_datetime(tc_data['ISO_TIME'])

# Create legend handles for black and red lines
black_patch = mpatches.Patch(color='gray', label='IBTrACS best track')
red_patch = mpatches.Patch(color='red', label='Track part with RI')

# Add legend with the created handles
plt.legend(handles=[black_patch, red_patch], loc='lower left')

# Iterate over intensifications data to plot the tracks with red segments
for index, row in intensifications_data.iterrows():
    season = row['SEASON']
    name = row['NAME']
    start_time = pd.to_datetime(row['start_time'])
    end_time = pd.to_datetime(row['end_time'])
    
    # Filter TC data for the specific TC by season and name
    tc_group = tc_data[(tc_data['SEASON'] == season) & (tc_data['NAME'] == name)]
    
    # Plot the entire track in black
    lat = tc_group['LAT'].values
    lon = tc_group['LON'].values
    x, y = m(lon, lat)
    m.plot(x, y, color='gray', alpha=0.4, linewidth=0.1)
    
    # Identify the segment of the track within the start_time and end_time and plot it in red
    mask = (tc_group['ISO_TIME'] >= start_time) & (tc_group['ISO_TIME'] <= end_time)
    lat_red = tc_group.loc[mask, 'LAT'].values
    lon_red = tc_group.loc[mask, 'LON'].values
    x_red, y_red = m(lon_red, lat_red)
    m.plot(x_red, y_red, color='red', linewidth=0.5)

# Save the figure as a PDF
plt.savefig('tc_tracks_with_red_segments.pdf', format='pdf', bbox_inches='tight')

plt.show()
