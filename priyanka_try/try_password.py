import streamlit as st
import pandas as pd


# Read data from CSV files
df_districts = pd.read_csv(r'districts.csv')
df_province = pd.read_csv(r'list_of_provinces_of_nepal-2804j.csv')



st.set_page_config(
    page_title="Nepal Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

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
