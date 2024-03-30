# imports
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
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

# dataframe
df_nepal = pd.read_csv("data/smallcase_district_random.csv")
df_districtinfo = pd.read_csv

with st.sidebar:

    st.title("Filter Data")

    # Go over the geojson file and create a dict where the key is province which contains the list of districts it contains

    province_list = [
        "Koshi",
        "Madhesh",
        "Bagmati",
        "Gandaki",
        "Lumbini",
        "Karnali",
        "Sudurpashchim",
    ]
    province_district_dict = dict()
    for i in range(1, 8):
        df_temp = df_geometry[df_geometry["ADM1_EN"].isin([str(i)])]
        province_district_dict[province_list[i - 1]] = list(df_temp.DIST_EN)

    select_province = st.selectbox("Select Province", province_list)

    # start of form that gathers district and data info and only updates when 'show info' button is clicked.
    with st.form("user_input", clear_on_submit=False, border=False):
        # dropdown for district
        select_district = st.selectbox(
            "Select District", province_district_dict[select_province]
        )

        # radio buttons for info type
        info_on = st.radio(
            "What do you want to see information about?",
            ["Population", "Literacy Rate", "Sex Raio", "Poverty"],
        )

        st.form_submit_button("Show Info")

        #info section
        st.info('Built by [Priyanka](https://www.google.com) and [Mukesh](https://www.google.com) \n Checkout code at [Github Repo](https://www.google.com)', icon="ℹ️")

# define cholropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(
        input_df,
        geojson=df_geometry,
        featureidkey="properties.DIST_EN",
        locations=input_id,
        color=input_column,
        color_continuous_scale=input_color_theme,
        range_color=(0, max(df_nepal.number)),
        labels={"population": "Population"},
    )
    choropleth.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
    )
    return choropleth.update_geos(fitbounds="locations", visible=True)


choropleth = make_choropleth(df_nepal, "DM", "number", "Reds")
st.plotly_chart(choropleth, use_container_width=True)
