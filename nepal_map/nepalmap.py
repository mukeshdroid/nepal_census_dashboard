import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots
import numpy as np
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import os


#####################################################################################################################
### LOADING FILES


#read in once
df_places = gpd.read_file('data/nepal-with-districts.geojson')

df_places.explore()

