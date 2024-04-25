# Research on Links between Marine Heatwaves (MHWs) and Rapid Intensification (RI) of Tropical Cyclones

This repository contains code and analysis related to research on the impact of marine heatwaves on the rapid intensification of tropical cyclones. The project aims to investigate the relationship between ocean temperature anomalies and the rapid intensification of tropical cyclones.

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
- Python 3.7 or higher
- NumPy
- Pandas
- Matplotlib
- Xarray
- Scipy

You can install the required Python packages using pip:
```bash
pip install numpy pandas matplotlib xarray scipy
```

## Usage
The main script to run the analysis is main.py. Execute it with the following command:
```bash
python main.py
```
This script will load the necessary data, perform the analysis, and generate output files and visualizations.

## File Structure
```bash
├── data/
│   ├── sst_data/
│   └── cyclone_data/
├── output/
├── scripts/
│   ├── data_processing.py
│   ├── analysis.py
│   └── visualization.py
├── main.py
└── README.md
```

Below is an overview of the main directories and files included in this repository:

- `data`: Directory containing input data files
  - `sst_data`: Sea surface temperature data
  - `cyclone_data`: Tropical cyclone track and intensity data
- `output`: Directory where output files and visualizations will be saved
- `scripts`: Directory containing Python scripts for data processing, analysis, and visualization
- `main.py`: Main script to run the analysis
- `README.md`: This file

## Data
This project requires two types of input data:

1. **Sea Surface Temperature (SST) Data**: Obtainable from NOAA's Optimum Interpolation SST dataset or the Hadley Centre SST dataset.
2. **Tropical Cyclone Track and Intensity Data**: Obtainable from the International Best Track Archive for Climate Stewardship (IBTrACS) or the Joint Typhoon Warning Center (JTWC).
Please ensure that the data files are placed in the appropriate directories (`data/sst_data/` and `data/cyclone_data/`) before running the analysis.

## Results
The main output of this analysis will be a set of visualizations and statistical analyses exploring the relationship between marine heatwaves and the rapid intensification of tropical cyclones. The output files will be saved in the `output/` directory.

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the Apache License.

## Acknowledgments
This research is supported by the Center for Complex Hydrosystems Research at the University of Alabama. We would like to thank **Dr. Alex Sen Gupta** (UNSW) and **Dr. Gregory Foltz** (NOAA) for their valuable contributions to this project. Funding was awarded to Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (NA22NWS4320003). Partial support is also provided by NSF award # 2223893.

## Contact
For any questions or inquiries, please contact the project maintainer at [sradfar@ua.edu].
