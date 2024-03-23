import requests
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
import streamlit as st

# get Spain municipal boundaries
with open("data/nepal-with-districts.geojson","r") as file:
    jsonData = json.load(file)

# get some cities in Spain
df = (
    pd.json_normalize(
        requests.get(
            "https://opendata.arcgis.com/datasets/6996f03a1b364dbab4008d99380370ed_0.geojson"
        ).json()["features"]
    )
    .loc[
        lambda d: d["properties.CNTRY_NAME"].eq("Nepal"),
        ["properties.CITY_NAME", "geometry.coordinates"],
    ]
    .assign(
        lon=lambda d: d["geometry.coordinates"].apply(lambda v: v[0]),
        lat=lambda d: d["geometry.coordinates"].apply(lambda v: v[1]),
    )
)
df

# scatter the cities and add layer that shows municiple boundary
mapbox_nepal = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="properties.CITY_NAME").update_layout(
    mapbox={
        "style": "open-street-map",
        "zoom": 5.5,
        "layers": [
            {
                "source": jsonData,
                "type": "line",
                "color": "green",
                "line": {"width": 1},
            }
        ],
    }
)

st.plotly_chart(mapbox_nepal, use_container_width=True)