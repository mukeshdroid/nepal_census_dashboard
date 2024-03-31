# imports
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd

# configure page
st.set_page_config(
    page_title="Nepal Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded",
)

#------------------------LOGIN PAGE-------------------------------------------------
def credentials_entered():
    if st.session_state["user"].strip()=="admin" and  st.session_state["psswd"].strip()=="admin":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if not st.session_state["psswd"]:
            st.warning("Please enter your password")
        elif not st.session_state["user"]:
            st.warning("Please enter username")
        else:
            st.error("Invalid Username / Password")

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label = "Username",value = "",key = "user",on_change=credentials_entered)
        st.text_input(label = "Password",value = "",key = "psswd",type = "password",on_change=credentials_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label = "Username",value = "",key = "user",on_change=credentials_entered)
            st.text_input(label = "Password",value = "",key = "psswd",type="password",on_change=credentials_entered)
            return False
if authenticate_user():
    st.title('Nepal Dashboard')

        

    alt.themes.enable("dark")

    # dataframe
    df_nepal = pd.read_csv("data/districts_complete.csv")
    df_province = pd.read_csv("data/province_complete.csv")
    #load nepal's geometry divided at district level
    df_geometry = gpd.read_file("data/nepal-districts_filtered.geojson")

    #----------------------------GLOBAL VARIABLES--------------------------------
    level = "country"


    #------------------------------DEFINE FUNCTIONS-------------------------------
    # define cholropleth map
    def make_choropleth(input_df, input_id, input_column, input_color_theme):
        choropleth = px.choropleth(
            genData(),
            geojson=gen_geoJSON(),
            featureidkey="properties.DIST_EN",
            locations=input_id,
            color=input_column,
            color_continuous_scale=input_color_theme,
            # range_color=(0, max(df_nepal.number)),
            labels={info_on: info_on},
        )
        choropleth.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
        )
        return choropleth.update_geos(fitbounds="locations", visible=True)



    #top 6 lowest and highest population 2021
    def compute_top5population(df):
        df_top5population = df.sort_values(['Population2021'],ascending=False).head(6)[["Name","Population2021"]].rename(columns={'Population2021': 'Population'})
        return df_top5population

    #top 6 lowest and highest population 2021
    def compute_low5population(df):
        df_low5population = df.sort_values(['Population2021'],ascending=True).head(6)[["Name","Population2021"]].rename(columns={'Population2021': 'Population'})
        return df_low5population

    #generate line chart to show the increase of population by province
    def genlinechart_province(df):

        df_temp = df[["Name", "Population1981","Population1991","Population2001","Population2011","Population2021"]]
        df_temp = df_temp.rename(columns={"Population1981" : 1981,"Population1991" : 1991,"Population2001" : 2001,"Population2011" : 2011,"Population2021":2021})
        return df_temp.set_index('Name').T

    #generate pie chart to show contribution of population by selected level of detail
    def genpiechart_province(df):
            fig = px.pie(df, values='Population2021', names='Name',
                    title=f'Population Division of '+level,
                    height=300, width=200)
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
            return fig

    #generate geoJSON File based on the input
    def gen_geoJSON():
        if level == 'country':
            return df_geometry
        
        if level == 'province':
            select_province_index = province_list.index(select_province) + 1
            return df_geometry[df_geometry['ADM1_EN'] == str(select_province_index)]
        
        if level == 'district':
            return df_geometry[df_geometry['DIST_EN'] == select_district]
        
    #generate census dataframe based on input
    def genData():
        if level == 'country':
            return df_nepal
        
        if level == 'province':
            return df_nepal[df_nepal['Province'] == select_province]
        
        if level == 'district':
            return df_nepal[df_nepal['Name'] == select_district]

        

    #generate a list of district for each province
    def get_districtsinprov():
        province_district_dict = dict()
        for i in range(1, 8):
            df_temp = df_geometry[df_geometry["ADM1_EN"].isin([str(i)])]
            province_district_dict[province_list[i - 1]] = list(df_temp.DIST_EN)
        return province_district_dict



    #------------------------------------LAYOUT---------------------------------------------

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

        province_district_dict = get_districtsinprov()

        select_province = st.selectbox("Select Province", province_list)

        # start of form that gathers district and data info and only updates when 'show info' button is clicked.
        with st.form("user_input", clear_on_submit=False, border=False):
            # dropdown for district
            select_district = st.selectbox(
                "Select District", province_district_dict[select_province]
            )

            info_on = st.radio(
                "Paramter to color map by:",
                ["Population2021","Sex_Ratio","Population_Density","Poverty","Literacy","StudentTeacher_ratio"],
            )


            level = st.radio("Level of Detail",["country","province","district"])

            st.form_submit_button("Generate Data")

            #info section
            st.info('Built by [Priyanka](https://www.linkedin.com/in/priyanka-panta-8451b4251/) and [Mukesh](https://www.linkedin.com/in/tiwarimukesh12/) \n Checkout code at [Github Repo](https://www.google.com)', icon="🖋️")
            
            #source Information
            st.info('Source Details: \n [Code for Nepal](https://github.com/CodeforNepal/data)', icon="ℹ️")






    if level=='country':
        st.write('####', info_on,'data of Nepal')
        choropleth = make_choropleth(df_nepal, "Name", info_on, "Reds")
        st.plotly_chart(choropleth, use_container_width=True)
                
        col1_1, col1_2 = st.columns(2)

        with col1_1:
            st.write('Population Growth amongst ', level, 'from 1981 to 2021' )
            st.line_chart(genlinechart_province(df_province))


        with col1_2:
            st.plotly_chart(genpiechart_province(df_province), use_container_width=True)


        col2_1, col2_2, col2_3 = st.columns(3)

        with col2_1:
            st.table(compute_top5population(genData()))

        with col2_2:
            st.table(compute_low5population(genData()))

        with col2_3:
            st.table(compute_top5population(genData()))

    if level=='province':

        st.write('####', info_on,'data of ' , select_province , ' Province')
        choropleth = make_choropleth(df_nepal, "Name", info_on, "Reds")
        st.plotly_chart(choropleth, use_container_width=True)

        col1_1, col1_2, col1_3 = st.columns([0.55,0.225,0.225])

        with col1_1:
            st.plotly_chart(genpiechart_province(genData()), use_container_width=True)



        with col1_2:
            st.write('Least Populated')
            st.table(compute_low5population(genData()))

        with col1_3:
            st.write('Most Populated')
            st.table(compute_top5population(genData()))

        st.write('Population Growth amongst ', level, 'from 1981 to 2021' )
        st.line_chart(genlinechart_province(genData()))




    if level=='district':
        col1_1, col1_2 = st.columns([0.6,0.4])

        with col1_1:
            st.write('####', info_on,' data of ' , select_district)
            choropleth = make_choropleth(df_nepal, "Name", info_on, "Reds")
            st.plotly_chart(choropleth, use_container_width=True)

        with col1_2:
            st.write('### About',select_district)
            st.table(genData().transpose())
