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
    if sel_fy:
        fil_df=fil_df[fil_df["FY"].isin(sel_fy)]
    with col2:
        sel_td = st.multiselect("Time_Of_Day", sorted(df["Day / Night"].dropna().unique()))
    if sel_td:
        fil_df=fil_df[fil_df["Day / Night"].isin(sel_td)]
    with col3:
        sel_so = st.multiselect("State_Office", sorted(df["SO"].dropna().unique()))
    if sel_so:
        fil_df=fil_df[fil_df["SO"].isin(sel_so)]
    with col4:
        sel_tt = st.multiselect("TT_Type", sorted(df["Type of TT "].dropna().unique()))
    if sel_tt:
        fil_df=fil_df[fil_df["Type of TT "].isin(sel_tt)]
    tab1,tab2,=st.tabs(["Data","Chart"])
    with tab1:
            st.dataframe(fil_df)
