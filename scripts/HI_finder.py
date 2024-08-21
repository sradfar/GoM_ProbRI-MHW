# -----------------------------------------------------------------------------
# Python script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script analyzes hurricane track data to identify periods of rapid intensification (RI). 
# It processes the data to detect significant increases in wind speed over a short period, 
# and records details of these intensification events.
#
# Outputs:
# - A CSV file named 'intensifications.csv' that contains the details of each detected 
#   rapid intensification event, including hurricane name, start and end times, start and 
#   end wind speeds, latitudes and longitudes, wind speed change, and duration of intensification.
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
from datetime import datetime, timedelta

# Load the dataset
df = pd.read_csv('ibtracs_data.csv')

# Define the criteria for hurricane intensification
def is_intensifying(df, index):
    current_time = datetime.strptime(df.loc[index, 'ISO_TIME'], '%m/%d/%Y %H:%M')
    current_wind_speed = df.loc[index, 'USA_WIND']
    
    for i in range(index+1, len(df)):
        time_diff = datetime.strptime(df.loc[i, 'ISO_TIME'], '%m/%d/%Y %H:%M') - current_time
        if time_diff > timedelta(days=1):
            break
        wind_speed_diff = df.loc[i, 'USA_WIND'] - current_wind_speed
        if wind_speed_diff >= 30:
            return True
    return False

# Iterate over the dataset and find intensifications
results = []
for i in range(len(df)):
    if is_intensifying(df, i):
        start_time = datetime.strptime(df.loc[i, 'ISO_TIME'], '%m/%d/%Y %H:%M')
        start_wind_speed = df.loc[i, 'USA_WIND']
        hurricane_name = df.loc[i, 'NAME']
        lat_start = df.loc[i, 'LAT']
        lon_start = df.loc[i, 'LON']
        
        for j in range(i+1, len(df)):
            time_diff = datetime.strptime(df.loc[j, 'ISO_TIME'], '%m/%d/%Y %H:%M') - start_time
            if time_diff > timedelta(days=1):
                break
            wind_speed_diff = df.loc[j, 'USA_WIND'] - start_wind_speed
            if wind_speed_diff >= 30:
                end_time = datetime.strptime(df.loc[j, 'ISO_TIME'], '%m/%d/%Y %H:%M')
                end_wind_speed = df.loc[j, 'USA_WIND']
                duration = (end_time - start_time).total_seconds() / 3600 # convert to hours
                lat_end = df.loc[j, 'LAT']
                lon_end = df.loc[j, 'LON']
                results.append([hurricane_name, start_time, start_wind_speed, lat_start, lon_start, end_time, end_wind_speed, lat_end, lon_end, wind_speed_diff, duration])
                break

# Create a dataframe from the results and save to a CSV file
columns = ['hurricane_name', 'start_time', 'start_wind_speed', 'lat_start', 'lon_start', 'end_time', 'end_wind_speed', 'lat_end', 'lon_end', 'wind_speed_change', 'duration']
df_results = pd.DataFrame(results, columns=columns)
df_results.to_csv('intensifications.csv', index=False)
