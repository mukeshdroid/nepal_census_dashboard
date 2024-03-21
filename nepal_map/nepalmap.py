import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots

import os


#####################################################################################################################
### LOADING FILES

@st.cache

# LOAD DATAFRAME FUNCTION
def load_data(path):
    df = pd.read_csv(path)
    return df

# LOAD GEIJASON FILE
with open("data/district.geojson") as response:
    geo = json.load(response)




# Add title and header
# st.title("Renewable Energy Production in Switzerland")
# st.header("Energy Production by Cantons (MWH) ")

# Geographic Map
fig = go.Figure(
    go.Choroplethmapbox(
        geojson=geo,
        locations=None,
        featureidkey=None,
        z=None,
        colorscale="sunsetdark",
        # zmin=0,
        # zmax=500000,
        marker_opacity=0.5,
        marker_line_width=0,
    )
)
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": 28.39, "lon": 84.13},
    width=800,
    height=600,
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)
#fig.write_image("fig1.png")
