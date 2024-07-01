# Research on Links between Marine Heatwaves (MHWs) and Rapid Intensification (RI) of Tropical Cyclones

This repository contains code and analysis related to the study of the impact of marine heatwaves (MHWs) on the rapid intensification (RI) of tropical cyclones (TCs). The rapid intensification of TCs is a multifaceted phenomenon influenced by various oceanic and atmospheric factors, posing significant challenges to accurate TC forecasting and simulation. A key contributing factor to this intensification process is the presence of prolonged high sea surface temperatures, also known as marine heatwaves. However, the extent to which MHWs contribute to the compounding effect of RI events has not been fully explored. 

This study presents a probabilistic framework that evaluates the likelihood of complex interactions between MHWs and RI events in the Gulf of Mexico and northwestern Caribbean Sea regions. Historical analysis shows that the presence of MHWs has been influential in the RI of 70% of past hurricanes. According to our analysis, MHWs can increase the likelihood of RI events by up to five times (on average 1.5 times) compared to non-MHW situations. These results emphasize the need for improved understanding and monitoring of these compounding phenomena for reliable TC risk assessment.

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
