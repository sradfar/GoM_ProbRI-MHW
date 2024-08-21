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
% This script is part of the research on the impact of marine heatwaves on the 
% rapid intensification (RI) of tropical cyclones. The primary aim of this script is to
% analyze and visualize the duration and frequency of marine heatwave (MHW) events and their 
% relative intensity over specific the Gulf on Mexico.
% The output includes three types of geographical visualizations:
% 1. Mean Duration of MHW Events
% 2. Mean Frequency of MHW Events Per Year
% 3. Mean Intensity of MHW Events
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

# Load your data into a DataFrame
mhw_data = pd.read_csv('MHW_1950_2022_80_52.csv')

# Total number of years in the dataset
total_years = 2022 - 1981 + 1

# # Select the number of rows and the columns for visualization
start_row_1981 = 312596
mhw_data = mhw_data.iloc[start_row_1981:]

### Preparing data
# Group the data by latitude and longitude
grouped_data = mhw_data.groupby(['MHW_lat', 'MHW_lon']).agg(
    mean_duration=('duration', 'mean'),
    total_duration=('duration', 'sum'),
    event_count=('duration', 'size')
).reset_index()

# Calculate mean events per year
grouped_data['mean_events_per_year'] = grouped_data['event_count'] / total_years
grouped_data['mean_duration_per_year'] = grouped_data['total_duration'] / total_years

### First plot: MHW_Mean_Duration
# Create a Basemap instance for mean duration
plt.figure(figsize=(10, 8))
m1 = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')

# Draw parallels and meridians
m1.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0])
m1.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1])

# Pivot the grouped data for mean duration
duration_pivot = grouped_data.pivot(index='MHW_lat', columns='MHW_lon', values='mean_duration_per_year')

# Interpolate the data for contourf to make it smooth for mean duration
xi_duration = np.linspace(duration_pivot.columns.min(), duration_pivot.columns.max(), 500)
yi_duration = np.linspace(duration_pivot.index.min(), duration_pivot.index.max(), 500)
xi_duration, yi_duration = np.meshgrid(xi_duration, yi_duration)
zi_duration = m1.transform_scalar(duration_pivot.values, duration_pivot.columns.values, duration_pivot.index.values, xi_duration.shape[1], xi_duration.shape[0])

# Specify contour levels
levels = np.linspace(20, 65, 16)

# Plot the interpolated data using contourf for mean duration with specified levels
contourf_duration = m1.contourf(xi_duration, yi_duration, zi_duration, levels=levels, cmap='plasma', latlon=True)

# Draw coastlines and fill continents
m1.drawcoastlines()
m1.fillcontinents(color='lightgray')

# Add a colorbar for mean duration
cbar_duration = m1.colorbar(contourf_duration, location='right', label='days per year')

plt.title('Mean Duration of MHW Events')
plt.savefig('MHW_Mean_Duration.pdf', format='pdf')  # Save the figure as a PDF
plt.show()


### Second plot: MHW_Mean_Events_Per_Year
# Create a Basemap instance for mean events per year
plt.figure(figsize=(10, 8))
m2 = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')

# Draw parallels and meridians
m2.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0])
m2.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1])

# Pivot the grouped data for mean events per year
events_per_year_pivot = grouped_data.pivot(index='MHW_lat', columns='MHW_lon', values='mean_events_per_year')

# Interpolate the data for contourf to make it smooth for mean events per year
xi_events_per_year = np.linspace(events_per_year_pivot.columns.min(), events_per_year_pivot.columns.max(), 500)
yi_events_per_year = np.linspace(events_per_year_pivot.index.min(), events_per_year_pivot.index.max(), 500)
xi_events_per_year, yi_events_per_year = np.meshgrid(xi_events_per_year, yi_events_per_year)
zi_events_per_year = m2.transform_scalar(events_per_year_pivot.values, events_per_year_pivot.columns.values, events_per_year_pivot.index.values, xi_events_per_year.shape[1], xi_events_per_year.shape[0])

# Specify contour levels
levels = np.linspace(0.5, 6, 12)

# Plot the interpolated data using contourf for mean events per year
contourf_events_per_year = m2.contourf(xi_events_per_year, yi_events_per_year, zi_events_per_year, levels=levels, cmap='plasma', latlon=True)
# Draw coastlines and fill continents
m2.drawcoastlines()
m2.fillcontinents(color='lightgray')

# Add a colorbar for mean events per year
cbar_events_per_year = m2.colorbar(contourf_events_per_year, location='right', label='times per year')

plt.title('Mean Events per Year')
plt.savefig('MHW_Mean_Events_Per_Year.pdf', format='pdf')  # Save the figure as a PDF
plt.show()


### Third plot: MHW_Mean_Intensity
# Group the data by latitude and longitude for intensity_max_relThresh
grouped_intensity = mhw_data.groupby(['MHW_lat', 'MHW_lon']).agg(
    mean_intensity=('intensity_max_relThresh', 'mean')
).reset_index()

# Create a Basemap instance for mean intensity
plt.figure(figsize=(10, 8))
m3 = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')

# Draw parallels and meridians
m3.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0])
m3.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1])

# Pivot the grouped data for mean intensity
intensity_pivot = grouped_intensity.pivot(index='MHW_lat', columns='MHW_lon', values='mean_intensity')

# Interpolate the data for contourf to make it smooth for mean intensity
xi_intensity = np.linspace(intensity_pivot.columns.min(), intensity_pivot.columns.max(), 500)
yi_intensity = np.linspace(intensity_pivot.index.min(), intensity_pivot.index.max(), 500)
xi_intensity, yi_intensity = np.meshgrid(xi_intensity, yi_intensity)
zi_intensity = m3.transform_scalar(intensity_pivot.values, intensity_pivot.columns.values, intensity_pivot.index.values, xi_intensity.shape[1], xi_intensity.shape[0])

# Specify contour levels
levels = np.linspace(0.1, 1, 10)

# Plot the interpolated data using contourf for mean intensity
contourf_intensity = m3.contourf(xi_intensity, yi_intensity, zi_intensity, levels=levels, cmap='plasma', latlon=True)
# Draw coastlines and fill continents
m3.drawcoastlines()
m3.fillcontinents(color='lightgray')

# Add a colorbar for mean intensity
cbar_intensity = m3.colorbar(contourf_intensity, location='right', label='°C per year')

plt.title('Mean i_max_rel')
plt.savefig('MHW_Mean_Intensity.pdf', format='pdf')  # Save the figure as a PDF
plt.show()
