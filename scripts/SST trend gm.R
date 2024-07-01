library(extrafont)
font_import()
loadfonts(device = "win")  # Register fonts for Windows bitmap output
fonts()

library(ggplot2)
library(openxlsx)

# Read in data from the Excel file
sst_data <- readxl::read_excel("sst gom.xlsx")

# Create a sequence of dates from Jan 1 to Dec 31
date_range <- seq(as.Date("2023-01-01"), as.Date("2023-12-31"), by = "month")

# Add a "date" column to the data frame
sst_data$date <- date_range

# Plot the four lines and shaded area between the upper and lower bound
my_plot <- ggplot(sst_data, aes(x = date)) +
  
  geom_ribbon(aes(ymin = `mean-2sig`, ymax = `mean+2sig`),
              fill = "#CCCCFF", alpha = 0.5) +
  geom_ribbon(aes(ymin = `mean-1sig`, ymax = `mean+1sig`),
              fill = "#BFE7FF", alpha = 0.7) +
  geom_line(aes(y = `2022`, color = "2022"), size = 1.5) +
  geom_line(aes(y = `2023`, color = "2023"), size = 1.5) +
  geom_line(aes(y = `climatological mean`, color = "1982-2011 mean"), size = 1.5) +
  labs(x = "Month", y = "SST (°C)", color = "") +
  scale_x_date(date_labels = "%b", date_breaks = "1 month", expand = c(0, 0)) +
  scale_color_manual(values = c("2022" = "#00E272", "2023" = "#FE6A35", "1982-2011 mean" = "#544FC5")) +
  theme_bw() +
  theme(
    text = element_text(family = "Calibri", size = 12),
    panel.grid.major = element_line(color = "grey80"),
    panel.grid.minor = element_blank(),
    legend.position = c(0.03, 1.1),
    legend.justification = c(0, 1),
    legend.title = element_text(size = 16),
    legend.text = element_text(size = 16),
    legend.background = element_rect(fill = "transparent"),
    axis.text = element_text(size = 16),
    axis.title = element_text(size = 16),
    plot.margin = margin(1, 1, 1, 1, "cm")  # Adjust the margins for padding
  )

# Save the plot as a PNG file with padding
ggsave("Figure 3.png", plot = my_plot, width = 8, height = 4, units = "in", dpi = 600)
