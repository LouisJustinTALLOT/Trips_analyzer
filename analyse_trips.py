import geopandas as gpd
import shapely as shp
import matplotlib.pyplot as plt

# Load the data
trips_gdf = gpd.read_file("mapstr_2024_04_24.geojson")
print(trips_gdf.loc[0])

trips_gdf.plot()
plt.show()

