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
% This script is designed for quantitative analysis and visualization of Tropical Cyclone
% Heat Potential (TCHP) in the Gulf of Mexico prior to rapid intensification (RI) events
% of tropical cyclones. It focuses on calculating the mean TCHP over 10 days before each RI
% start date from 2013 to 2022, using Ocean Heat Content (OHC) data.
%
% The script performs the following operations:
% 1. Loads RI event start dates from a CSV file and filters dates within the specified period.
% 2. Defines geographical boundaries for the Gulf of Mexico, crucial for focusing the analysis
%    on this specific region.
% 3. Implements a function to load, clip, and average OHC data from NetCDF files, tailored
%    to the defined spatial bounds of the Gulf of Mexico.
% 4. Aggregates and visualizes the computed mean TCHP values over the study period, displaying
%    them in a heatmap using Basemap for spatial context.
%
% Outputs:
% - Heatmap visualizing the mean TCHP in the days leading up to RI events, saved as a PDF.
% - This visualization assists in understanding the oceanic conditions that might contribute
%   to the rapid intensification of tropical cyclones.
%
% For details on the research framework and methodologies, refer to:
% Radfar, S., Moftakhari, H., and Moradkhani, H. (2024), Rapid intensification of tropical cyclones in the Gulf of Mexico is more likely during marine heatwaves,
% Communications Earth & Environment.
% Link: 
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
import netCDF4 as nc
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib
from matplotlib.colors import ListedColormap, Normalize


# Load RI start dates
ri_dates_df = pd.read_csv('../intensifications30_IID_24.csv')
ri_dates_df['HI_date'] = pd.to_datetime(ri_dates_df['HI_date'])
ri_dates = ri_dates_df[(ri_dates_df['HI_date'] >= '2013-01-01') & (ri_dates_df['HI_date'] <= '2022-12-31')]['HI_date']

# Define the GoM bounds
lat_bounds = (15, 31)  # Latitude bounds for the GoM
lon_bounds = (-100, -78)  # Longitude bounds for the GoM

# Define a function to load and clip OHC data
def load_and_clip_ohc_data(date, base_path):
    ohc_values = []
    for delta in range(10):
        day_to_load = date - timedelta(days=delta)
        year = day_to_load.year
        day_of_year = day_to_load.timetuple().tm_yday
        file_path = f'{base_path}/{year}/ohc_naQG3_{year}_{day_of_year:03d}.nc'
        try:
            dataset = nc.Dataset(file_path)
            variable_name = 'ohc' if 'ohc' in dataset.variables else 'heatcontent'
            ohc_data = dataset.variables[variable_name][:].squeeze()
            ohc_data[ohc_data == -999] = np.nan  # Ignore invalid data

            # Extract relevant lat and lon indices within GoM bounds
            latitudes = dataset.variables['latitude'][:]
            longitudes = dataset.variables['longitude'][:]
            lat_mask = (latitudes >= lat_bounds[0]) & (latitudes <= lat_bounds[1])
            lon_mask = (longitudes >= lon_bounds[0]) & (longitudes <= lon_bounds[1])

            ohc_data_clipped = ohc_data[lat_mask, :][:, lon_mask]
            ohc_values.append(ohc_data_clipped)
            dataset.close()
        except FileNotFoundError:
            continue
    return np.nanmean(ohc_values, axis=0) if ohc_values else None

# Aggregate OHC data by date
ohc_base_path = 'D:/ERA5 ohc'
aggregate_ohc = None

for date in ri_dates:
    ohc_data = load_and_clip_ohc_data(date, ohc_base_path)
    if ohc_data is not None:
        if aggregate_ohc is None:
            aggregate_ohc = ohc_data.copy()
        else:
            aggregate_ohc += ohc_data

if aggregate_ohc is not None:
    aggregate_ohc /= len(ri_dates)

# Visualization with Basemap
plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')
# Draw parallels and meridians
m.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0], fontsize=16)
m.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1], fontsize=16)

# Generate meshgrid for plotting, adding one extra step to include grid boundaries
lats = np.linspace(15, 31, aggregate_ohc.shape[0] + 1)
lons = np.linspace(-100, -78, aggregate_ohc.shape[1] + 1)
lon_mesh, lat_mesh = np.meshgrid(lons, lats)
x, y = m(lon_mesh, lat_mesh)

# Mask the -999.13 values and use NaN for visualization
ohc_masked = np.ma.masked_equal(aggregate_ohc, -999.13)

# Create a custom colormap
# Start with a jet colormap
jet = plt.cm.jet
# Get the colormap colors and create a new colormap from it
colors = jet(np.linspace(0, 1, 256))
new_colormap = ListedColormap(colors)

# Create a Normalize object which scales data values to the [0, 1] range
norm = Normalize(vmin=0, vmax=180)

# Plot using the custom colormap and masked array
cs = m.pcolormesh(x, y, ohc_masked, shading='flat', cmap=new_colormap, norm=norm)
m.drawcoastlines()
m.fillcontinents(color='lightgray')

# Add and configure the color bar
cbar = m.colorbar(cs, extend='both', location='bottom', pad="7%", ticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180])
cbar.set_label('Mean TCHP (kJ/cm^2)', fontsize=14)
cbar.ax.set_xticklabels(['0', '20', '40', '60', '80', '100', '120', '140', '160', '>180'], fontsize=14)

# plt.title('Mean Ocean Heat Content 10 Days Before RI Start Dates in the Gulf of Mexico')
plt.savefig('Figure 9a.pdf', format='pdf')  # Save the figure as a PDF
plt.show()