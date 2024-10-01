import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import haversine as hs

lat_low = 49.002
lat_high = 49.494
long_low = -123.340
long_high = -122.313



grid_lat = np.linspace(lat_low, lat_high, num=10)
grid_long = np.linspace(long_low, long_high, num=10)
grid = [np.tile(grid_lat, grid_long.size), np.repeat(grid_long, grid_lat.size)]
boundary_points = pd.DataFrame({
    'latitude': grid[0],  
    'longitude': grid[1]
})

boundary_points_gdf = gpd.GeoDataFrame(
    boundary_points, 
    geometry=[Point(xy) for xy in zip(boundary_points['longitude'], boundary_points['latitude'])],
    crs="EPSG:4326"  # WGS84 coordinate system
)

center_points = []
distances = []
for i in range(9):
    for j in range(9):
        distances.append(hs.haversine((grid_lat[i], grid_long[j]), (grid_lat[i+1], grid_long[j+1])))
        center_points.append([(grid_lat[i]+grid_lat[i+1])/2, (grid_long[j]+grid_long[j+1])/2])

center_points = pd.DataFrame(center_points, columns=['latitude', 'longitude'])
center_points_gdf = gpd.GeoDataFrame(
    center_points, 
    geometry=[Point(xy) for xy in zip(center_points['longitude'], center_points['latitude'])],
    crs="EPSG:4326"  # WGS84 coordinate system
)

vancouver_map = gpd.read_file('metro_van\\Administrative_Boundaries.shp')
vancouver_map = vancouver_map.to_crs(epsg=4326)
fig, ax = plt.subplots(figsize=(10, 14))
vancouver_map.plot(ax=ax)  
boundary_points_gdf.plot(ax=ax, color='red', markersize=50, label='Boundary Points')  # Plot the points
center_points_gdf.plot(ax=ax, color='yellow', markersize=50, label='Center Points')
plt.legend()
plt.xlim(-123.2, -123.0)
plt.ylim(49.25, 49.35)
plt.show()
#plt.savefig('Images\\grid_points.png')