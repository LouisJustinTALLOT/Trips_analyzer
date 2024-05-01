import pandas as pd
import geopandas as gpd
import shapely as shp
import matplotlib.pyplot as plt
import json


def load_data(data_location: str) -> gpd.GeoDataFrame:
    return gpd.read_file(data_location)


def plot_interactive_map(gdf: gpd.GeoDataFrame, show: bool = False):
    return gdf.explore(legend=False)


def unpack_tag(tag_series: str) -> pd.DataFrame:
    list_tags = [json.loads(tag) for tag in tag_series]

    tag_names = []
    for tag in list_tags:
        tag_names.append([x["name"] for x in tag])

    colors = []
    for tag in list_tags:
        colors.append([x["color"] for x in tag])

    return pd.DataFrame({"type": pd.Series(tag_names), "color": pd.Series(colors)})


def clean_mapstr_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf.drop(columns="userComment", inplace=True)
    gdf.drop(columns="icon", inplace=True)
    gdf.join(unpack_tag(gdf["tags"]))
    
    
    
def mapstr_stats(gpd: gpd.GeoDataFrame)-> str:
    stats = ""
    stats += f"Number of places visited: {len(gpd)}\n"
    
    return stats
