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
% This script is developed to analyze the mean vertical wind shear (VWS) associated 
% with rapid intensification (RI) events of tropical cyclones in the Gulf of Mexico
% over a specified period. It calculates the average VWS from the 10 days preceding 
% each RI event during the years 2013-2022, using ERA5 reanalysis wind data at two 
% different pressure levels (200mb and 850mb).
%
% The script includes:
% 1. Loading RI event start dates from a CSV file and filtering dates within the specified 
%    period (2013-2022).
% 2. Defining a function to load wind components from NetCDF files for a given date, 
%    calculate the VWS by computing the vector difference between wind speeds at 200mb 
%    and 850mb, and return the wind shear along with latitude and longitude grids.
% 3. Aggregating VWS data across all RI events and calculating the mean VWS to assess 
%    conditions prior to RI.
% 4. Plotting the average VWS on a map using Basemap, with visualization enhancements 
%    such as custom color scales and coastlines to aid in the interpretation of spatial 
%    patterns in wind shear.
%
% Outputs:
% - A heatmap visualizing the mean VWS in the days leading up to RI events, saved as a PDF.
% - This visualization helps to understand the atmospheric conditions that might contribute 
%   to the rapid intensification of tropical cyclones.
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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Load RI start dates and filter for the years 2013-2022
ri_dates_df = pd.read_csv('../intensifications30_IID_24.csv')
ri_dates_df['HI_date'] = pd.to_datetime(ri_dates_df['HI_date'])
ri_dates = ri_dates_df[(ri_dates_df['HI_date'] >= '2013-01-01') & (ri_dates_df['HI_date'] <= '2022-12-31')]['HI_date']

# Base path for wind data
ws_base_path = 'D:/ERA WS'

# Define the function to load and calculate wind shear for one date
def load_wind_components(date, base_path):
    components = {'u200': [], 'u850': [], 'v200': [], 'v850': []}
    latitudes = longitudes = None
    for delta in range(10):  # Process the 10 days before the RI date
        target_date = date - timedelta(days=delta)
        year = target_date.year
        file_path = f'{base_path}/era5_windspeed_{year}.nc'
        try:
            with nc.Dataset(file_path) as dataset:
                time_var = dataset.variables['time']
                times = nc.num2date(time_var[:], units=time_var.units)
                time_idx = np.where(times == target_date)[0]
                if time_idx.size > 0:
                    time_idx = time_idx[0]
                    levels = dataset.variables['level'][:]
                    level_idx_200 = np.where(levels == 200)[0][0]
                    level_idx_850 = np.where(levels == 850)[0][0]

                    u200 = dataset.variables['u'][time_idx, level_idx_200, :, :]
                    u850 = dataset.variables['u'][time_idx, level_idx_850, :, :]
                    v200 = dataset.variables['v'][time_idx, level_idx_200, :, :]
                    v850 = dataset.variables['v'][time_idx, level_idx_850, :, :]

                    components['u200'].append(u200)
                    components['u850'].append(u850)
                    components['v200'].append(v200)
                    components['v850'].append(v850)

                    if latitudes is None:
                        latitudes = dataset.variables['latitude'][:]
                        longitudes = dataset.variables['longitude'][:]
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    for key in components:
        components[key] = np.mean(components[key], axis=0) if components[key] else None

    wind_shear = np.sqrt((components['u200'] - components['u850'])**2 + (components['v200'] - components['v850'])**2)
    return wind_shear, latitudes, longitudes

# Process all RI dates
all_wind_shear = []
for date in ri_dates:
    ws, lats, lons = load_wind_components(date, ws_base_path)
    all_wind_shear.append(ws)

# Calculate the average wind shear while ignoring NaNs
aggregate_ws = np.nanmean(all_wind_shear, axis=0)

# Plotting the average wind shear
plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')
m.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0], fontsize=16)
m.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1], fontsize=16)
lats = np.linspace(15, 31, aggregate_ws.shape[0] + 1)
lons = np.linspace(-100, -78, aggregate_ws.shape[1] + 1)
lon_mesh, lat_mesh = np.meshgrid(lons, lats)
x, y = m(lon_mesh, lat_mesh)
ws_masked = np.ma.masked_where(aggregate_ws == 0, aggregate_ws)
cs = m.pcolormesh(x, y, ws_masked, shading='flat', cmap='Spectral_r', vmin=4, vmax=14)
m.drawcoastlines()
m.fillcontinents(color='lightgray')
cbar = m.colorbar(cs, extend='both', location='bottom', pad="7%", ticks=[4, 6, 8, 10, 12, 14])
cbar.set_label('Mean VWS (m/s)', fontsize=14)
cbar.ax.set_xticklabels(['<4', '6', '8', '10', '12', '>14'], fontsize=14)
# plt.title('Mean Wind Shear 10 Days Before RI Start Dates in the Gulf of Mexico')
plt.savefig('Figure 9b.pdf', format='pdf')  # Save the figure as a PDF
plt.show()