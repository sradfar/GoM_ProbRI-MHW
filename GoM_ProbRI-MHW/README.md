# Project 1: Links between Marine Heatwaves (MHWs) and Rapid Intensification (RI) of Tropical Cyclones in the Gulf of Mexico and the northwestern Carrribean Sea

This repository contains code and analysis related to the study of the impact of marine heatwaves (MHWs) on the rapid intensification (RI) of tropical cyclones (TCs). This study presents a probabilistic framework that evaluates the likelihood of complex interactions between MHWs and RI events in the Gulf of Mexico and northwestern Caribbean Sea regions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Data](#data)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Installation

To run the code in this repository, you'll need to have the following dependencies installed:

### Python Dependencies
- Python 3.7 or higher
- NumPy
- Pandas
- Matplotlib
- Xarray
- Scipy
- Seaborn
- Tqdm
- NetCDF4
- Basemap

You can install the required Python packages using pip:
```bash
pip install numpy pandas matplotlib xarray scipy seaborn tqdm netCDF4 basemap
```

### R Dependencies
- ncdf4
- dplyr
- lubridate

You can install the required R packages using the following commands in R:
```bash
install.packages("ncdf4")
install.packages("dplyr")
install.packages("lubridate")
```

## Usage

Each script file has a description on top that clearly describes the objectives of that code and expected outputs. Brief explanations of the scripts are as follows:

- `tc_landfall.py`: Used to plot landfalling TC tracks [Figure 2a].
- `five_tc_tracks.py`: Used to plot tracks and categories of five costly historical TCs of the study area [Figure 2b].
- `SST trend gm.R`: Used to plot the monthly SST trend in the study area [Figure 3].
- `HI_finder.py`: One of the main analysis codes used to detect RI events according to NHC definition.
- `RI_reg_prob_plot.py`: Used for calculating and plotting the probability of RI occurrence in the GoM and NWCS regions [Figure 4].
- `mhw_detect_era5.R`: Another main analysis code used for detecting historical MHW events.
- `GoM_mhw_pattern_plots.py`: Used for calculating and plotting the mean number, duration, and intensity of MHWs across the GoM and NWCS [Figure 5].
- `intensity_duration_plot.py`: Used for plotting maximum intensity relative to the SST threshold [˚C] and duration [days] across the GoM and NWCS [Figure 6].
- `compound_mhw_RI.py`: The final main analysis code used for detecting compound MHW-RI events; events with close spatiotemporal gaps.
- `conditional_mhw_ri_prob.py`: Used for calculating and plotting the conditional probabilities of RI occurrence given MHW occurrence [Figure 7].
- `multiply_rate.py`: Used for calculating and plotting multiplication rates in the study area [Figure 8].
- `TCHP_plot.py`, `VWS_plot.py`, `LHF_plot.py`: Used for calculating and plotting mean heat content, wind shear, and latent flux [Figure 9].
- `all_tracks.py`, `tc_track.py`: Used to plot Supplementary Figures 1 and 2.

## File Structure
```bash
├── data/
│   ├── MHW_1940_2022_80_52.csv
│   ├── MHW_1950_2022_80_52.csv
│   ├── Monthly_RI_data.xlsx
│   ├── gom_1940_1980.rds
│   ├── gom_1981_2022.rds
│   ├── ibtracs_5tc.csv
│   ├── ibtracs_data.csv
│   ├── intensifications30_IID_24.csv
│   ├── intensifications_24 - Copy.csv
│   ├── sst gom.xlsx
│   └── .gitattributes
├── scripts/
│   ├── GoM_mhw_pattern_plots.py
│   ├── HI_finder.py
│   ├── LHF_plot.py
│   ├── RI_reg_prob_plot.py
│   ├── SST trend gm.R
│   ├── TCHP_plot.py
│   ├── VWS_plot.py
│   ├── all_tracks.py
│   ├── compound_mhw_RI.py
│   ├── conditional_mhw_ri_prob.py
│   ├── five_tc_tracks.py
│   ├── intensity_duration_plot.py
│   ├── mhw_detect_era5.R
│   ├── multiply_rate.py
│   ├── tc_landfall.py
│   └── tc_track.py
├── LICENSE
└── README.md
```

## Data

This project requires multiple types of input data:

1. **Sea Surface Temperature (SST) Data**: 
   - The sea surface temperature (SST) data used in this study were obtained from the ERA5 dataset, provided by the Copernicus Climate Change Service (C3S), and is publicly available at [ERA5 SST dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form).

2. **Tropical Cyclone Track and Intensity Data**: 
   - The International Best Track Archive for Climate Stewardship (IBTrACS) dataset, provided by the National Centers for Environmental Information (NCEI), is available from [IBTrACS dataset](https://www.ncei.noaa.gov/products/international-best-track-archive).

3. **Thermal Ocean Parameters**: 
   - TCHP, D26, and MLD data were obtained from the NOAA’s Operational Satellite Ocean Heat Content Suite, available at the National Centers for Environmental Information (NCEI) website [NOAA Ocean Heat Content Suite](https://www.ncei.noaa.gov/products/satellite-ocean-heat-content-suite).

4. **Latent Heat Flux (LHF) Data**: 
   - LHF data was sourced from the ERA5 hourly data on single levels, accessible via the Copernicus Climate Data Store [ERA5 LHF dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form).

5. **Vertical Wind Shear (VWS) Data**: 
   - Data for VWS were calculated based on u and v component wind speeds at 200- and 850 hPa pressure levels, obtained from ERA5 hourly data on pressure levels. This dataset is also available on the Copernicus Climate Data Store [ERA5 Pressure Levels dataset](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form).

6. **Additional Data**: 
   - Other data used for creating the plots are freely available in the `data/` folder of this repository.

## Results
The main output of this analysis will be a set of visualizations and statistical analyses exploring the relationship between marine heatwaves and the rapid intensification of tropical cyclones. The results are available in the cited papers.

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the Apache License.

## Acknowledgments
This research is supported by the Coastal Hydrology Lab and the Center for Complex Hydrosystems Research at the University of Alabama. Funding was awarded to Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (NA22NWS4320003). Partial support was also provided by NSF award # 2223893.

## Contact
For any questions or inquiries, please contact the project maintainer at [sradfar@ua.edu].
