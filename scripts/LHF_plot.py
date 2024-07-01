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
% This script is intended for the analysis of Latent Heat Flux (LHF) in the Gulf of Mexico 
% prior to rapid intensification (RI) events of tropical cyclones over the period from 2013 to 2022.
% It calculates the average LHF from the 10 days preceding each RI event using ERA5 reanalysis data.
%
% The script executes the following operations:
% 1. Loads RI event start dates from a CSV file and filters for the specified period.
% 2. Defines a function to load and clip LHF data from NetCDF files for the specified dates and 
%    geographic boundaries.
% 3. Aggregates LHF data across all relevant RI dates and calculates the mean LHF for the region, 
%    aiming to highlight the atmospheric conditions preceding RI events.
% 4. Visualizes the aggregated LHF data on a geographical map using the Basemap toolkit, enhancing 
%    interpretation with a custom color scale to indicate varying levels of LHF.
%
% Outputs:
% - A heatmap visualizing the mean LHF in the days leading up to RI events, formatted as a PDF.
%   This visualization supports understanding of the oceanic and atmospheric preconditions influencing 
%   tropical cyclone intensification.
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
import matplotlib

# Load RI start dates
ri_dates_df = pd.read_csv('../intensifications30_IID_24.csv')
ri_dates_df['HI_date'] = pd.to_datetime(ri_dates_df['HI_date'])
ri_dates = ri_dates_df[(ri_dates_df['HI_date'] >= '2013-01-01') & (ri_dates_df['HI_date'] <= '2022-12-31')]['HI_date']

# Define the GoM bounds
lat_bounds = (15, 31)  # Latitude bounds for the GoM
lon_bounds = (-100, -78)  # Longitude bounds for the GoM

# Define a function to load and clip LHF data
def load_and_clip_lhf_data(date, base_path):
    lhf_values = []
    year = date.year
    file_path = f'{base_path}/era5_lhc_{year}.nc'
    try:
        with nc.Dataset(file_path) as dataset:
            lhf_data = dataset.variables['mslhf'][:]
            time_var = dataset.variables['time']
            times = nc.num2date(time_var[:], units=time_var.units)  # Convert time variable to datetime objects

            # Find indices for the 10 days before the given date
            target_dates = [date - timedelta(days=delta) for delta in range(10)]
            time_indices = [np.where(times == target_date)[0] for target_date in target_dates]
            time_indices = [idx for sublist in time_indices for idx in sublist]  # Flatten the list

            for time_idx in time_indices:
                if time_idx.size > 0:
                    lhf_day_data = lhf_data[time_idx].squeeze()
                    lhf_day_data[lhf_day_data == -999] = np.nan  # Ignore invalid data

                    # Extract relevant lat and lon indices within GoM bounds
                    latitudes = dataset.variables['latitude'][:]
                    longitudes = dataset.variables['longitude'][:]
                    lat_mask = (latitudes >= lat_bounds[0]) & (latitudes <= lat_bounds[1])
                    lon_mask = (longitudes >= lon_bounds[0]) & (longitudes <= lon_bounds[1])

                    lhf_data_clipped = lhf_day_data[lat_mask, :][:, lon_mask]
                    lhf_values.append(lhf_data_clipped)
    except FileNotFoundError:
        pass  # If the file is not found, continue without adding any data

    return np.nanmean(lhf_values, axis=0) if lhf_values else None

# Aggregate LHF data by date
lhf_base_path = 'D:/ERA5 LHF'
aggregate_lhf = None

for date in ri_dates:
    lhf_data = load_and_clip_lhf_data(date, lhf_base_path)
    if lhf_data is not None:
        if aggregate_lhf is None:
            aggregate_lhf = lhf_data.copy()
        else:
            aggregate_lhf += lhf_data

if aggregate_lhf is not None:
    aggregate_lhf /= len(ri_dates)

# Visualization with Basemap
aggregate_lhf = abs(aggregate_lhf)
plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlat=15, urcrnrlat=31, llcrnrlon=-100, urcrnrlon=-78, resolution='i')
m.drawparallels(np.arange(15, 32, 5), labels=[1, 0, 0, 0], fontsize=16)
m.drawmeridians(np.arange(-100, -77, 5), labels=[0, 0, 0, 1], fontsize=16)

lats = np.linspace(15, 31, aggregate_lhf.shape[0] + 1)
lons = np.linspace(-100, -78, aggregate_lhf.shape[1] + 1)
lon_mesh, lat_mesh = np.meshgrid(lons, lats)
x, y = m(lon_mesh, lat_mesh)

lhf_masked = np.ma.masked_where(aggregate_lhf == 0, aggregate_lhf)
cs = m.pcolormesh(x, y, lhf_masked, shading='flat', cmap='turbo', vmin=0, vmax=180)
m.drawcoastlines()
m.fillcontinents(color='lightgray')

# Create the colorbar with extended ends
cbar = m.colorbar(cs, extend='both', location='bottom', pad="7%", ticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180])
cbar.set_label('Mean LHF (W/m^2)', fontsize=14)
# Here you're manually setting the tick labels to include '<' and '>'.
cbar.ax.set_xticklabels(['<1', '20', '40', '60', '80', '100', '120', '140', '160', '>180'], fontsize=14)

# plt.title('Mean Latent Heat Flux 10 Days Before RI Start Dates in the Gulf of Mexico')
plt.savefig('Figure 9c.pdf', format='pdf')  # Save the figure as a PDF
plt.show()

