# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script visualizes the tracks of specific hurricanes along with their 
# intensification points using the Basemap library for geographic plotting.
# It processes hurricane track data, filters for selected hurricanes, and 
# generates a map displaying the hurricane paths with color-coded wind speeds 
# and markers for rapid intensification (RI) events.
#
# Outputs:
# - A visual map of hurricane tracks with segments marked by wind speed categories and 
#   rapid intensification points highlighted, providing a clear visual indicator of the 
#   hurricane paths and intensification events.
# - The final map is saved as a PDF titled 'hurricane_tracks.pdf', suitable for inclusion 
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
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# Read the data
data = pd.read_csv('../ibtracs_5tc.csv')
data['ISO_TIME'] = pd.to_datetime(data['ISO_TIME'])

# Filter data for specific hurricanes
hurricane_names = ['KATRINA', 'HARVEY', 'MICHAEL', 'IDA', 'IAN']
filtered_data = data[data['NAME'].isin(hurricane_names)]

# Define the Basemap
fig, ax = plt.subplots(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')
#m.drawcoastlines()
m.drawcountries(color='#CAD2D3', linewidth=2)
m.drawstates(color='#CAD2D3')
m.fillcontinents(color='#F2F2F0', lake_color='#CAD2D3')
m.drawmapboundary(fill_color='#CAD2D3')

# Define the color scale for hurricane categories
def get_color(wind_speed):
    if wind_speed < 34:
        return '#1C53FF'  # Tropical Depression
    elif 34 <= wind_speed < 64:
        return '#6CC343'  # Tropical Storm
    elif 64 <= wind_speed < 83:
        return '#FFC309'  # Category 1
    elif 83 <= wind_speed < 96:
        return '#FF7109'  # Category 2
    elif 96 <= wind_speed < 113:
        return '#E83A0C'  # Category 3
    elif 113 <= wind_speed < 137:
        return '#E80CAD'  # Category 4
    else:
        return '#BC00FF'  # Category 5

# Plot the tracks
for name, group in filtered_data.groupby('NAME'):
    group = group.sort_values(by='ISO_TIME')
    lats = group['LAT'].values
    lons = group['LON'].values
    winds = group['USA_WIND'].values
    x, y = m(lons, lats)
    
    # Plot lines without markers and with colors based on wind speed
    for i in range(1, len(x)):
        m.plot(x[i-1:i+1], y[i-1:i+1], color=get_color(winds[i-1]), linewidth=2)

    # Plot intensification points
    intensifications = group[group['RI'] == 1]
    if not intensifications.empty:
        xi, yi = m(intensifications['LON'].values, intensifications['LAT'].values)
        m.scatter(xi, yi, color='black', s=150, marker='*', zorder=5)  # Increased size for visibility

# Create legend handles
handles = [
    mpatches.Patch(color='#1C53FF', label='Tropical Depression'),
    mpatches.Patch(color='#6CC343', label='Tropical Storm'),
    mpatches.Patch(color='#FFC309', label='Category 1'),
    mpatches.Patch(color='#FF7109', label='Category 2'),
    mpatches.Patch(color='#E83A0C', label='Category 3'),
    mpatches.Patch(color='#E80CAD', label='Category 4'),
    mpatches.Patch(color='#BC00FF', label='Category 5'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='black', markersize=10, label='Intensification')
]
ax.legend(handles=handles, loc='lower left')

plt.savefig('../hurricane_tracks.pdf', bbox_inches='tight')
plt.show()
