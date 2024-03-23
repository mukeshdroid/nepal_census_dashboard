# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.graph_objects as go
# from urllib.request import urlopen
# import json
# from copy import deepcopy
# from plotly.subplots import make_subplots
# import numpy as np
# import geopandas as gpd
# import folium
# import matplotlib.pyplot as plt
# import os


import folium
import streamlit as st

from streamlit_folium import st_folium

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)



df_places = gpd.read_file('data/nepal-with-districts.geojson')

st.map()

