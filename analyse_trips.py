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

    names = []
    colors = []
    tag_color_mapping = {}
    for tag in list_tags:
        tag_names = []
        tag_colors= []
        for x in tag:
            tag_names.append(x["name"])
            tag_colors.append(x["color"])
            tag_color_mapping[x["name"]] = x["color"]
        names.append(tag_names)
        colors.append(tag_colors)

    return pd.DataFrame({"type": pd.Series(names), "color": pd.Series(colors)}), tag_color_mapping


def clean_mapstr_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf.drop(columns="userComment", inplace=True)
    gdf.drop(columns="icon", inplace=True)
    gdf_tags, tag_color_mapping = unpack_tag(gdf["tags"])
    gdf.join(gdf_tags)
    print(tag_color_mapping)


def mapstr_stats(gpd: gpd.GeoDataFrame) -> str:
    stats = ""
    stats += f"Number of places visited: {len(gpd)}\n"

    return stats
