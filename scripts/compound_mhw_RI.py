"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
% Center for Complex Hydrosystems Research
% Department of Civil, Construction, and Environmental Engineering
% The University of Alabama
%
% Last modified on April 24, 2024
%
% This script was developed to identify and analyze the compounding effects of
% marine heatwaves (MHWs) and rapid intensification (RI) of tropical cyclones.
% It evaluates spatial and temporal proximity between MHW events
% and RI events to establish a connection that may suggest compounded impact.
%
% The script processes datasets of MHW and RI events, examining each MHW event against
% RI events to determine if they occur within 200 kilometers and 10 days of each other,
% signifying potential compounded effects. The output of this analysis includes:
% 1. A detailed record of MHW events that align closely with RI events.
% 2. A record of MHW events that do not meet these criteria.
%
% Key Outputs:
% 1. 'MHW_info_80_52_24.csv' - CSV file containing MHW events with corresponding RI events 
%     that fall within the specified spatiotemporal thresholds.
% 2. 'no_RI.csv' - CSV file listing MHW events that do not have any corresponding RI events
%     within the defined proximity limits.
%
% For details on the research framework and methodologies, refer to:
% Radfar, S., Moftakhari, H., and Moradkhani, H. (2024), Unraveling the Regional Compounding Effects of Marine Heatwaves on Rapid Intensification of Tropical Cyclones,
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
from tqdm import tqdm

# read the hurricane intensification events CSV file
hi_df = pd.read_csv('intensifications30_IID_24.csv')

# read the marine heatwave events CSV file and drop any rows with NA values
mhw_df = pd.read_csv('MHW_1940_2022_80_52.csv').dropna() # 5-2 MHWs

# define a function to calculate the distance between two coordinates in km
def calc_dist(lat1, lon1, lat2_arr, lon2_arr):
    R = 6371  # radius of the earth in km
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2_arr)
    lon2_rad = np.radians(lon2_arr)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    return distance

# create an empty DataFrame to store the results for compounding events
result_df = pd.DataFrame(columns=['HI_lat', 'HI_lon', 'HI_date', 'HI_name', 'MHW_lat', 'MHW_lon',
                                  'distance_in_km', 'start_wind_speed',
                                  'end_time','end_wind_speed',
                                  'duration', 'date_start', 'date_peak',
                                  'date_end', 'intensity_mean', 'intensity_max', 'intensity_var', 'intensity_cumulative',
                                  'intensity_mean_relThresh', 'intensity_max_relThresh', 'intensity_var_relThresh',
                                  'intensity_cumulative_relThresh', 'intensity_mean_abs', 'intensity_max_abs', 'intensity_var_abs',
                                  'intensity_cumulative_abs', 'rate_onset',	'rate_decline',
                                  'window_start', 'window_peak', 'window_end'])

# create an empty DataFrame to store MHW events that don't satisfy the condition
no_ri_df = pd.DataFrame(columns=mhw_df.columns)

# iterate over each row in the MHW events DataFrame
for mhw_idx, mhw_row in tqdm(mhw_df.iterrows(), total=len(mhw_df)):
    # get the latitude and longitude of the current MHW event
    mhw_lat = mhw_row['MHW_lat']
    mhw_lon = mhw_row['MHW_lon']
    mhw_start = pd.to_datetime(mhw_row['date_start'], format='%m/%d/%Y')
    mhw_end = pd.to_datetime(mhw_row['date_end'], format='%m/%d/%Y')

    # filter the HI events based on distance and time threshold
    hi_df_filtered = hi_df[hi_df.apply(
        lambda row: (calc_dist(mhw_lat, mhw_lon, row['HI_lat'], row['HI_lon']) <= 200) and
                    (((pd.to_datetime(mhw_row['date_start'], format='%m/%d/%Y') >= pd.to_datetime(row['start_time'], format='%m/%d/%Y %H:%M') - pd.DateOffset(days=10)) &
                    (pd.to_datetime(mhw_row['date_start'], format='%m/%d/%Y') <= pd.to_datetime(row['start_time'], format='%m/%d/%Y %H:%M'))) or
                    ((pd.to_datetime(mhw_row['date_end'], format='%m/%d/%Y') >= pd.to_datetime(row['start_time'], format='%m/%d/%Y %H:%M') - pd.DateOffset(days=10)) &
                    (pd.to_datetime(mhw_row['date_end'], format='%m/%d/%Y') <= pd.to_datetime(row['start_time'], format='%m/%d/%Y %H:%M')))),
        axis=1)]

    # iterate over each filtered HI event
    for hi_idx, hi_row in hi_df_filtered.iterrows():
        # calculate the distance between the MHW event and the current HI event
        distance = calc_dist(mhw_lat, mhw_lon, hi_row['HI_lat'], hi_row['HI_lon'])

        # calculate the time gap between the start of the MHW event and the HI event
        hi_date = pd.to_datetime(hi_row['start_time'], format='%m/%d/%Y %H:%M')
    
        if not hi_df_filtered.empty:
            window_start = (mhw_start - hi_date).days
        else:
            window_start = np.nan
    
        if not hi_df_filtered.empty:
            window_end = (mhw_end - hi_date).days
        else:
            window_end = np.nan
    
        # create a dictionary to store the result of the current MHW event and HI event
        result_dict = {'HI_lat': hi_row['HI_lat'], 'HI_lon': hi_row['HI_lon'], 'HI_date': hi_date, 'HI_name': hi_row['HI_name'],
                       'MHW_lon': mhw_lon, 'MHW_lat': mhw_lat, 'distance_in_km': distance,
                       'start_wind_speed': hi_row['start_wind_speed'],
                       'end_time': hi_row['end_time'], 'end_wind_speed': hi_row['end_wind_speed'],
                       'duration': mhw_row['duration'], 'date_start': mhw_start, 'date_peak': mhw_row['date_peak'], 'date_end': mhw_end,
                       'intensity_mean': mhw_row['intensity_mean'], 'intensity_max': mhw_row['intensity_max'],
                       'intensity_var': mhw_row['intensity_var'], 'intensity_cumulative': mhw_row['intensity_cumulative'],
                       'intensity_mean_relThresh': mhw_row['intensity_mean_relThresh'], 'intensity_max_relThresh': mhw_row['intensity_max_relThresh'],
                       'intensity_var_relThresh': mhw_row['intensity_var_relThresh'], 'intensity_cumulative_relThresh': mhw_row['intensity_cumulative_relThresh'],
                       'intensity_mean_abs': mhw_row['intensity_mean_abs'], 'intensity_max_abs': mhw_row['intensity_max_abs'],
                       'intensity_var_abs': mhw_row['intensity_var_abs'], 'intensity_cumulative_abs': mhw_row['intensity_cumulative_abs'],
                       'rate_onset': mhw_row['rate_onset'], 'rate_decline': mhw_row['rate_decline'],
                       'window_start': window_start, 'window_end': window_end}

        # append the result dictionary to the result DataFrame
        result_df = result_df.append(result_dict, ignore_index=True)

    # if no HI events were found, add the MHW event to the "no_ri" DataFrame
    if hi_df_filtered.empty:
        no_ri_df = no_ri_df.append(mhw_row, ignore_index=True)

# save the result DataFrame to a CSV file
result_df.to_csv('MHW_info_80_52_24.csv', index=False)

# save the "no_ri" DataFrame to a separate CSV file
no_ri_df.to_csv('no_RI.csv', index=False)
