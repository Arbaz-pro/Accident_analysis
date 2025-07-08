import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(page_title="Excel Data Statistical Analyzer", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "upload"
# Go back button
if st.session_state.page == "analyze":
    if st.button("Go Back"):
        st.session_state.page = "upload"
        st.session_state.df = None

if st.session_state.page == "upload":
    st.title("Upload Excel or CSV File")
    uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["csv", "xlsx"])
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        else:
            df = pd.read_excel(uploaded_file)       
        st.session_state.df = df
        st.session_state.page = "analyze"
        st.rerun()
elif st.session_state.page == "analyze":
    df = st.session_state.df
    fil_df=df.copy()
    col1, col2, col3, col4, = st.columns(4)
    with col1:
        sel_fy = st.multiselect("Financial_Year", sorted(df["FY"].dropna().unique()))
    with col2:
        sel_td = st.multiselect("Time_Of_Day", sorted(df["Day / Night"].dropna().unique()))
    with col3:
        sel_so = st.multiselect("State_Office", sorted(df["SO"].dropna().unique()))
    with col4:
        sel_tt = st.multiselect("TT_Type", sorted(df["Type of TT "].dropna().unique()))
    tab1,tab2,=st.tabs("Data","Chart")
    
