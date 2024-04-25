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
% This script is part of the research on the impact of marine heatwaves on the 
% rapid intensification of tropical cyclones. For details on the research framework and
% methodologies, refer to:
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

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
data = pd.read_csv('MHW_1950_2022_80_52.csv')

# Select the number of rows and the columns for visualization
rows_to_plot = 312596
columns_to_visualize = ["duration", "intensity_max_relThresh", "intensity"]

# Create a square figure with a specified size (e.g., 8x8 inches)
plt.figure(figsize=(8, 8))

# Create a PairGrid for the selected data
# Sort the data based on 'intensity' before plotting
data_to_plot = data[columns_to_visualize].iloc[rows_to_plot:].sort_values(by='intensity')
g = sns.PairGrid(data_to_plot, corner=True, hue="intensity", diag_sharey=False, palette="plasma")
g.map_diag(sns.kdeplot, color = '#EB4C42', shade=True, hue=None)
g.map_offdiag(sns.scatterplot, s=5, edgecolor='none')

# Set the xlabels for each axis with units
g.axes[0, 0].set_ylabel('Duration [days]')

# Set the xlabel for the last axis in the second row
g.axes[1, 0].set_xlabel('Duration [days]')
g.axes[1, 0].set_ylabel('i_max_rel [°C]')

# Limit the x-axis and y-axis for specific axes
g.axes[0, 0].set_xlim(0, 400)
g.axes[1, 0].set_xlim(0, 400)
g.axes[1, 0].set_ylim(0, 5)
g.axes[1, 1].set_ylim(0, 5)

# Set the xlabel for the last axis in the last row
g.axes[1, 1].set_xlabel('i_max_rel [°C]')

# Add a continuous color bar legend below the plot
cax = g.fig.add_axes([0.18, -0.03, 0.7, 0.02])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=plt.Normalize(vmin=data["intensity"].min(), vmax=data["intensity"].max()))
sm.set_array([]) # Create an empty array for the color bar
cbar = plt.colorbar(sm, cax=cax, orientation="horizontal")
cbar.set_label("Intensity [°C]")

# Save the figure as a PDF
plt.savefig('1981_2022_pairplot.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()
