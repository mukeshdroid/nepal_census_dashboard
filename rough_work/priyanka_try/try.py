import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nepal Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

# Read data from CSV files
df_districts = pd.read_csv(r'c:\Users\ASUS\Downloads\districts.csv')
df_province = pd.read_csv(r'c:\Users\ASUS\Downloads\list_of_provinces_of_nepal-2804j.csv')

with st.sidebar:
    st.title('Filter Data')
    select_by = st.selectbox("Select by", ['Province', 'District', 'Local Level'])

    if select_by == 'Province':
        options = df_province['Province'].unique()
    elif select_by == 'District':
        options = df_districts['Districts'].unique()
    else:
        options = []  # Define options for Local Level if available

    selected_option = st.selectbox("Select", options)
