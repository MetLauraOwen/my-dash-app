#random testing to script to trial rpy2

library(ggplot2)
library(maps)
library(sf)
library(ncdf4)

fig_path <- "/home/users/laura.owen/hackathon_may_2025/figures/temp/"

###############################################################################
# read in city df and select top cities
###############################################################################
city_df = read.csv('~/old-home/data/users/lowen/extremes/heatwaves/HadUKGrid/dur-clim/coords/UK_cities.csv')
city_df <- city_df[1:30,]

uk_map <- map_data("world", region = "UK")

png(paste0(fig_path, "UK_cities.png"), width = 1100, height = 1300)
ggplot() +
  geom_polygon(data = uk_map, aes(x = long, y = lat, group = group), 
               fill = "lightblue", color = "gray") +
  geom_point(data = city_df, aes(x = longitude, y = latitude), color = "red", size = 3) +
  coord_quickmap() +
  theme_minimal() +
  labs(title = "City Coordinates on UK Map",
       x = "Longitude", y = "Latitude")
dev.off()

