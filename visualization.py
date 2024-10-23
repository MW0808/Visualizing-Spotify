"""
CSC111 Project 2: Wrap Mapped, Unpacked
Authors: Colleen Chang, Richard Lin, Roy Liu, Mina (Chieh-Yi) Wu

File Description
=============================================================================
This file contains functions necessary to visualize tree data.

"""
import python_ta

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import geopandas as gpd
import country_converter as coco

import storage


def all_options_table(available_set: set, kind: str) -> None:
    """
    Displays a table listing all the options in the given set for the program.

    Preconditions:
        - available_set != set()
        - type in {'continent', 'country', 'city', 'song'}
    """
    if kind == 'continent':
        fig = go.Figure(data=[go.Table(header={"values": ['Continents']},
                                       cells={"values": [sorted(list(available_set))]})
                              ])
    elif kind == 'country':
        fig = go.Figure(data=[go.Table(header={"values": ['Countries']},
                                       cells={"values": [sorted(list(available_set))]})
                              ])
    elif kind == 'city':
        fig = go.Figure(data=[go.Table(header={"values": ['Cities']},
                                       cells={"values": [sorted(list(available_set))]})
                              ])
    else:
        fig = go.Figure(data=[go.Table(header={"values": ['Songs']},
                                       cells={"values": [sorted(list(available_set))]})
                              ])
    fig.show()


def generate_region_df_by_streams(data: storage.Tree, kind: str) -> pd.DataFrame:
    """
    Returns a processed dataframe listing the names of the members of the specified region, "Streams" for the total
    number of streams among the specified region's top 5 songs, and 5 columns listing the top songs for each member of
    the region.

    Since ISO3 codes are a preset for go.Choropleth and px.Choropleth, dataframes with a column listing counties will
    also have a column listing their corresponding ISO3 codes.

    Preconditions:
        - data.is_empty is False
        - kind in {"continent", "country", "city"}
    """
    region_to_streams = data.get_region_streams(kind)
    region_top_5 = data.get_region_top_songs(kind)

    if kind == "continent":
        df_dict = {"continent": [name.lower() for name in region_to_streams],
                   "streams": [region_to_streams[name] for name in region_to_streams],
                   "Top 1 Song": [region_top_5[code][0] for code in region_top_5],
                   "Top 2 Song": [region_top_5[code][1] for code in region_top_5],
                   "Top 3 Song": [region_top_5[code][2] for code in region_top_5],
                   "Top 4 Song": [region_top_5[code][3] for code in region_top_5],
                   "Top 5 Song": [region_top_5[code][4] for code in region_top_5]
                   }
        return pd.DataFrame(data=df_dict).sort_values("continent")
    elif kind == "country":
        df_dict = {"country": list(region_to_streams),
                   "iso3": [coco.convert(names=name, to='ISO3') for name in region_to_streams],
                   "streams": [region_to_streams[code] for code in region_to_streams],
                   "Top 1 Song": [region_top_5[code][0] for code in region_top_5],
                   "Top 2 Song": [region_top_5[code][1] for code in region_top_5],
                   "Top 3 Song": [region_top_5[code][2] for code in region_top_5],
                   "Top 4 Song": [region_top_5[code][3] for code in region_top_5],
                   "Top 5 Song": [region_top_5[code][4] for code in region_top_5]
                   }

        return pd.DataFrame(data=df_dict).sort_values("country")
    else:
        df_dict = {"city_ascii": [name[0] for name in region_to_streams],
                   "iso3": [coco.convert(names=name[1], to='ISO3') for name in region_to_streams],
                   "streams": [region_to_streams[name] for name in region_to_streams],
                   "Top 1 Song": [region_top_5[code][0] for code in region_top_5],
                   "Top 2 Song": [region_top_5[code][1] for code in region_top_5],
                   "Top 3 Song": [region_top_5[code][2] for code in region_top_5],
                   "Top 4 Song": [region_top_5[code][3] for code in region_top_5],
                   "Top 5 Song": [region_top_5[code][4] for code in region_top_5]
                   }

        return pd.DataFrame(data=df_dict).sort_values("city_ascii")


def generate_region_df_by_score(data: storage.Tree, songs: list[str], kind: str, ranked: bool = False) -> pd.DataFrame:
    """
    Returns a processed dataframe listing the names of the members of the specified region, "Streams" for the total
    number of streams among the specified region's top 5 songs, and 5 columns listing the top songs for each member of
    the region.

    Since ISO3 codes are a preset for go.Choropleth and px.Choropleth, dataframes with a column listing counties will
    also have a column listing their corresponding ISO3 codes.

    Preconditions:
        - data.is_empty is False
        - kind in {"continent", "country", "city"}
    """
    region_to_scores = data.get_region_scores(songs, kind, ranked)

    if kind == "continent":
        df_dict = {"continent": [name.lower() for name in region_to_scores],
                   "scores": [region_to_scores[name] for name in region_to_scores]}
        return pd.DataFrame(data=df_dict).sort_values("continent")
    elif kind == "country":
        df_dict = {"country": list(region_to_scores),
                   "iso3": [coco.convert(names=name, to='ISO3') for name in region_to_scores],
                   "scores": [region_to_scores[code] for code in region_to_scores]}

        return pd.DataFrame(data=df_dict).sort_values("country")
    else:
        df_dict = {"city_ascii": [name[0] for name in region_to_scores],
                   "iso3": [coco.convert(names=name[1], to='ISO3') for name in region_to_scores],
                   "scores": [region_to_scores[name] for name in region_to_scores]}

        return pd.DataFrame(data=df_dict).sort_values("city_ascii")


def visualize_world_song_data(kind: str, stat: str, table: pd.DataFrame) -> None:
    """
    Visualizes data using functions from Storage.py

    Preconditions
        - kind in {'continent', 'country', 'city'}
        - stat in {'scores', 'streams'}
    """
    if kind == 'continent':
        # DATA FRAMES FOR COUNTRIES:
        # where "table" = generate_region_df_by_streams(data, "continent")
        ct_df = table

        # add column with proper names to display
        ct_df['continent_title'] = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

        # alter continent names to merge with dataframe from json file
        ct_df['continent'] = ct_df['continent'].apply(lambda x: x.replace(" ", ""))

        # LOAD GEO DATA: latitude and longitude mapped for cities in the world
        cont = requests.get(
            "https://gist.githubusercontent.com/cmunns/76fb72646a68202e6bde/raw/"
            "8f954b3ca01835bee4af9ae50dfe73eb6ab88fca/continents.json"
        )
        gdf = gpd.GeoDataFrame.from_features(cont.json())
        # alter continent names to merge later
        gdf['continent'] = gdf['continent'].apply(lambda x: x.lower())

        # merge dataframes
        gdf = gdf.merge(ct_df).sort_values('continent')

        # generate plot
        if stat == 'streams':
            fig = px.choropleth(gdf,
                                geojson=gdf.geometry,
                                locations=gdf.index,
                                color="streams",
                                color_continuous_scale="Reds",
                                )
            fig.update_traces(customdata=np.stack((gdf['continent_title'],
                                                   gdf['Top 1 Song'],
                                                   gdf['Top 2 Song'],
                                                   gdf['Top 3 Song'],
                                                   gdf['Top 4 Song'],
                                                   gdf['Top 5 Song']), axis=-1),
                              hovertemplate="<b>Continent: %{customdata[0]} </b><br>"
                                            "1st Top Song: %{customdata[1]}<br>"
                                            "2nd Top Song: %{customdata[2]}<br>"
                                            "3rd Top Song: %{customdata[3]}<br>"
                                            "4th Top Song: %{customdata[4]}<br>"
                                            "5th Top Song: %{customdata[5]}</b>")
            fig.update_layout(title="Top 5 Streamed Songs by Continent During the First Week of 2024")
        else:
            fig = px.choropleth(gdf,
                                geojson=gdf.geometry,
                                locations=gdf.index,
                                color="scores",
                                color_continuous_scale="Reds",
                                hover_data="scores"
                                )
            fig.update_traces(customdata=np.stack((ct_df['continent_title'],
                                                   ct_df['scores']), axis=-1),
                              hovertemplate="<b>Continent: %{customdata[0]} </b><br>"
                                            "Similarity Score: %{customdata[1]}</b>")
            fig.update_layout(title="Similarity Scores by Continent Based on Top 5 Streamed Songs"
                                    " During the First Week of 2024")

        fig.show()

    elif kind == 'country':
        # DATA FRAMES FOR COUNTRIES: ISO3 code preset for go.Choropleth
        # where "table" = generate_region_df_by_streams(data, "country")
        cy_df = table

        # generate plot
        if stat == 'streams':
            fig = go.Figure(data=go.Choropleth(locations=cy_df['iso3'],
                                               text=cy_df['iso3'],
                                               z=cy_df['streams'],
                                               customdata=np.stack((cy_df['country'],
                                                                    cy_df['Top 1 Song'],
                                                                    cy_df['Top 2 Song'],
                                                                    cy_df['Top 3 Song'],
                                                                    cy_df['Top 4 Song'],
                                                                    cy_df['Top 5 Song']), axis=-1),
                                               hovertemplate="<b>Country: %{customdata[0]} </b><br>"
                                                             "1st Top Song: %{customdata[1]}<br>"
                                                             "2nd Top Song: %{customdata[2]}<br>"
                                                             "3rd Top Song: %{customdata[3]}<br>"
                                                             "4th Top Song: %{customdata[4]}<br>"
                                                             "5th Top Song: %{customdata[5]}</b>",
                                               colorscale='Greens', autocolorscale=False, reversescale=False,
                                               colorbar_title={'text': "streams"}
                                               ))
            fig.update_layout(title="Top 5 Streamed Songs by Country During the First Week of 2024")
        else:
            fig = go.Figure(data=go.Choropleth(locations=cy_df['iso3'],
                                               text=cy_df['iso3'],
                                               z=cy_df['scores'],
                                               customdata=np.stack((cy_df['country'],
                                                                    cy_df['scores']), axis=-1),
                                               hovertemplate="<b>Country: %{customdata[0]} </b><br>"
                                                             "Similarity Score: %{customdata[1]}</b>",
                                               colorscale='Greens', autocolorscale=False, reversescale=False,
                                               colorbar_title={'text': "scores"}))
            fig.update_layout(title="Similarity Scores by Country Based on Top 5 Streamed Songs"
                                    " During the First Week of 2024")

        fig.show()

    else:
        # DATA FRAMES FOR CITIES
        # where "table" = generate_region_df_by_streams(data, "city")
        ci_df = table

        # LOAD GEO DATA: latitude and longitude mapped for cities in the world
        # downloaded locally as original from "simplemaps" was altered to update old city names
        cities = pd.read_csv('worldcities.csv')

        # merge data frames to drop rows with cities not in the data frames above
        cities = cities.merge(ci_df).drop_duplicates(subset='city', keep='first')

        # generate plot
        if stat == 'streams':
            fig = px.scatter_geo(cities, lat='lat', lon='lng',
                                 color='streams',
                                 hover_name='city')
            fig.update_traces(customdata=np.stack((cities['city'],
                                                   cities['Top 1 Song'],
                                                   cities['Top 2 Song'],
                                                   cities['Top 3 Song'],
                                                   cities['Top 4 Song'],
                                                   cities['Top 5 Song']), axis=-1),
                              hovertemplate="<b>City: %{customdata[0]} </b><br>"
                                            "1st Top Song: %{customdata[1]}<br>"
                                            "2nd Top Song: %{customdata[2]}<br>"
                                            "3rd Top Song: %{customdata[3]}<br>"
                                            "4th Top Song: %{customdata[4]}<br>"
                                            "5th Top Song: %{customdata[5]}</b>")
            fig.update_layout(title='Top 5 Streamed Songs by City During the First Week of 2024')
        else:
            fig = px.scatter_geo(cities, lat='lat', lon='lng',
                                 color='scores',
                                 hover_name='city')
            fig.update_traces(customdata=np.stack((cities['city'],
                                                   cities['scores']), axis=-1),
                              hovertemplate="<b>City: %{customdata[0]} </b><br>"
                                            "Similarity Score: %{customdata[1]}</b>")
            fig.update_layout(title="Similarity Scores by City Based on Top 5 Streamed Songs"
                                    " During the First Week of 2024")

        fig.show()


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['plotly.express', 'plotly.graph_objects', 'pandas', 'geopandas',
                          'numpy', 'requests', 'country_converter', 'storage'],
        'max-line-length': 120
    })
