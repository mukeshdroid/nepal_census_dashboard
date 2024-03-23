#imports
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd

#
df_geometry = gpd.read_file("data/nepal-districts.geojson")

# configure page
st.set_page_config(
    page_title="Nepal Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#dataframe
df_nepal = pd.read_csv('data/smallcase_district_random.csv')

#sidebar
with st.sidebar:
    st.title('🏂 Nepal Population Dashboard')
    

#define cholropleth map   
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df,
                               geojson=df_geometry,
                               featureidkey='properties.DIST_EN',
                               locations=input_id,
                               color=input_column,
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_nepal.number)),
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth.update_geos(fitbounds="locations", visible=True)


  
choropleth = make_choropleth(df_nepal, 'DM', 'number', 'Reds')
st.plotly_chart(choropleth, use_container_width=True)

