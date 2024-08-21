# -----------------------------------------------------------------------------
# R script developed by Soheil Radfar (sradfar@ua.edu), Postdoctoral Fellow
# Center for Complex Hydrosystems Research
# Department of Civil, Construction, and Environmental Engineering
# The University of Alabama
#
# Last modified on June 28, 2024
#
# This script is focused on detecting and analyzing Marine Heatwave (MHW) events 
# in the Gulf of Mexico based on ERA5 sea surface temperature data covering the 
# period from 1981 to 2022.
#
# The script executes the following:
# - Calculates climatologies from the temperature data, based on a predefined 
#   percentile for the period of interest.
# - Detects MHW events using the calculated climatologies.
# - Outputs detailed event data, organized by geographical coordinates.
#
# Outputs are efficiently generated through parallel processing across different 
# longitude groups, and include:
# 1. Detailed metrics for each detected MHW event.
# 2. A CSV file compiling these metrics for further analysis or reporting.
#
# For detailed methodology and implications, refer to:
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
# Finding the marine heatwave events based on ERA5 inputs
# -----------------------------------------------------------------------------

library(dplyr)
library(tidyr)
library(heatwaveR)
library(lubridate)
library(furrr)

ERA5SST <- readRDS("gom_1981_2022.rds")

# Define the function to detect MHW events
event_only <- function(df){
  # First calculate the climatologies
  clim <- ts2clm(data = df, pctile = 80, climatologyPeriod = c("1981-01-01", "2022-12-31"))
  
  # Then the events
  event <- detect_event(data = clim, minDuration = 5, maxGap = 2)
  
  # Return only the event metric dataframe of results
  return(event$event)
}

# Split the data into groups based on lon
ERA5SST_splits <- split(ERA5SST, f = ERA5SST$lon)

# Define the function to run MHW detection on a single group
detect_mhw <- function(df){
  df %>%
    group_by(lon, lat) %>%
    group_modify(~event_only(.x))
}

# Set up a parallel backend using furrr
plan(multisession, workers = 12)

# Use furrr to run the MHW detection on all groups in parallel
system.time(
  MHW_dplyr <- future_map_dfr(ERA5SST_splits, detect_mhw)
)

# Save for later use as desired
# saveRDS(MHW_dplyr, "MHW_1940_1980.Rds")
write.csv(MHW_dplyr, "MHW_1981_2022_80_52.csv", row.names = FALSE)
