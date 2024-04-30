import numpy as np
import pandas as pd
import geopandas as gpd
import shapely as shp
import matplotlib.pyplot as plt
import json

FRENCH_DEPARTEMENTS = "data/french-departements.geojson"
WORLD_COUNTRIES = "data/world-administrative-boundaries.geojson"


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
        tag_colors = []
        for x in tag:
            tag_names.append(x["name"])
            tag_colors.append(x["color"])
            tag_color_mapping[x["name"]] = x["color"]
        names.append(tag_names)
        colors.append(tag_colors)

    return (
        pd.DataFrame({"type": pd.Series(names), "color": pd.Series(colors)}),
        tag_color_mapping,
    )


def add_departement_info(
    gdf: gpd.GeoDataFrame, departements_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    joined = gpd.sjoin(gdf, departements_gdf, how="inner", predicate="intersects")
    gdf["departement"] = joined["nom"]
    return gdf.copy()


def add_world_info(
    gdf: gpd.GeoDataFrame, world_countries_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    joined = gpd.sjoin(gdf, world_countries_gdf, how="inner", predicate="intersects")
    gdf["country"] = joined["name_right"]
    gdf["country_FR"] = joined["french_short"]
    gdf["continent"] = joined["continent"]
    return gdf.copy()


def clean_mapstr_data(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf = gdf.copy()
    gdf.drop(columns="userComment", inplace=True)
    gdf.drop(columns="icon", inplace=True)
    gdf_tags, tag_color_mapping = unpack_tag(gdf["tags"])
    gdf.join(gdf_tags)
    print(tag_color_mapping)

    gdf = add_world_info(gdf)
    gdf = add_departement_info(gdf)


def mapstr_stats(gdf: gpd.GeoDataFrame) -> str:
    visited_departements = set(gdf["departement"])
    try:
        visited_departements.remove(np.nan)
    except KeyError:
        pass
    visited_countries = set(gdf["country"])
    try:
        visited_countries.remove(np.nan)
    except KeyError:
        pass
    visited_continents = set(gdf["continent"])
    try:
        visited_continents.remove(np.nan)
    except KeyError:
        pass

    stats = ""
    stats += f"Number of places visited: {len(gdf)}\n"
    stats += f"Number of countries visited: {len(visited_countries)}\n"
    stats += f"Number of continents visited: {len(visited_countries)}\n"
    stats += f"Number of French départements visited: {len(visited_departements)}\n"
    stats += f"Number of US states visited: \n"

    return stats
