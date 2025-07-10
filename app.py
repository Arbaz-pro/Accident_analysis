import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import plotly.graph_objects as go

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
    fil_df["FY_short"] = fil_df["FY"].str[-5:]
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
        sel_tt = st.multiselect("TT_Type", sorted(df["Type of TT"].dropna().unique()))
        if sel_tt:
            fil_df=fil_df[fil_df["Type of TT"].isin(sel_tt)]
    tab1,tab2,=st.tabs(["Data","Chart"])
    with tab1:
            st.dataframe(fil_df)
    with tab2:
        sel_ch = st.selectbox("Type of Chart", ["State Wise Distribution", "Month Wise Distribution","Majority Causes","Injury & Fatality Overview"])
        if(sel_ch=="State Wise Distribution"):
            so_order = [
            "DSO", "PSO", "RSO", "UPSO-I", "UPSO-II", "WBSO", "OSO",
            "BSO", "GSO", "MSO", "MPSO", "TNSO", "KESO", "KASO", "TAPSO", "IOAOD"
        ]
            selected_years = fil_df["FY_short"].unique()
            selected_so = so_order
            
            # Create full combination of FY and Month
            full_index = pd.MultiIndex.from_product(
                [selected_so, selected_years],
                names=["SO", "FY"]
            )
            grouped = (
            fil_df.groupby(["SO", "FY_short"])
            .size()
            .reindex(full_index, fill_value=0)
            .reset_index(name="Total Accidents")
            )
            
            # Ensure 'SO' is a categorical type with specified order
            grouped["SO"] = pd.Categorical(grouped["SO"], categories=so_order, ordered=True)
            
            # Sort the DataFrame accordingly
            grouped = grouped.sort_values("SO")
            color_palette = ["#1f77b4", "#4c72b0", "#6baed6", "#9ecae1", "#b2df8a", "#a6cee3", "#fdbf6f", "#c7e9c0", "#fb9a99", "#d9d9d9"]
            fig = go.Figure()
            so_totals = grouped.groupby("SO")["Total Accidents"].sum().reindex(so_order)
            for i, fy in enumerate(selected_years):
                df_fy = grouped[grouped["FY"] == fy]
                # Build label: "FY\nCount"
                text_labels = [f"{fy} :- ({int(val)})" if val > 0 else "" for val in df_fy["Total Accidents"]]
                
                fig.add_trace(go.Bar(
                    x=df_fy["SO"],
                    y=df_fy["Total Accidents"],
                    name=fy,
                    text=text_labels,
                    textposition="inside",
                    marker_color=color_palette[i % len(color_palette)],
                    textfont=dict(size=12, color="white",family="Arial Black"),
                ))
            fig.add_trace(go.Scatter(
            x=so_totals.index,
            y=so_totals.values,
            mode="text",
            text=[f"{int(val)}" if val > 0 else "" for val in so_totals.values],
            textposition="top center",
            showlegend=False,
            textfont=dict(size=12, color="black",family="Arial Black"),
        ))
            fig.update_layout(
            height=700,         # Increase height (default is ~450)
            width=1400,  
            xaxis_tickangle=-45,
            barmode="stack",
            xaxis_title="SO",
            yaxis_title="Total Accidents",
            legend_title="Financial Year"
        )
            st.plotly_chart(fig, use_container_width=True)

        elif(sel_ch=="Month Wise Distribution"):
            st.subheader("Month Wise Distribution")
            month_order = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
            selected_years = fil_df["FY"].unique()
            selected_months = month_order
            
            # Create full combination of FY and Month
            full_index = pd.MultiIndex.from_product(
                [selected_months, selected_years],
                names=["Month", "FY"]
            )
            grouped = (
            fil_df.groupby(["Month", "FY"])
            .size()
            .reindex(full_index, fill_value=0)
            .reset_index(name="Total Accidents")
            )
            
            # Ensure 'Month' is a categorical type with specified order
            grouped["Month"] = pd.Categorical(grouped["Month"], categories=month_order, ordered=True)
            
            # Sort the DataFrame accordingly
            grouped = grouped.sort_values("Month")
            color_palette = ["#1f77b4", "#4c72b0", "#6baed6", "#9ecae1", "#b2df8a", "#a6cee3", "#fdbf6f", "#c7e9c0", "#fb9a99", "#d9d9d9"]
            fig = go.Figure()
            monthly_totals = grouped.groupby("Month")["Total Accidents"].sum().reindex(month_order)
            
            for i, fy in enumerate(selected_years):
                df_fy = grouped[grouped["FY"] == fy]
                # Build label: "FY\nCount"

                text_labels = [f"{fy} :- ({int(val)})" if val > 0 else "" for val in df_fy["Total Accidents"]]
                
                fig.add_trace(go.Bar(
                    x=df_fy["Month"],
                    y=df_fy["Total Accidents"],
                    name=fy,
                    text=text_labels,
                    textposition="inside",
                    marker_color=color_palette[i % len(color_palette)],
                    textfont=dict(size=12, color="white",family="Arial Black"),
                ))
            
            fig.add_trace(go.Scatter(
            x=monthly_totals.index,
            y=monthly_totals.values,
            mode="text",
            text=[f"{int(val)}" if val > 0 else "" for val in monthly_totals.values],
            textposition="top center",
            showlegend=False,
            textfont=dict(size=14, color="black",family="Arial Black"),
        ))
            fig.update_layout(
            height=700,         # Increase height (default is ~450)
            width=1400,  
            xaxis_tickangle=-45,
            barmode="stack",
            xaxis_title="Month",
            yaxis_title="Total Accidents",
            legend_title="Financial Year"
        )
            st.plotly_chart(fig, use_container_width=True)
            st.write("test",df_fy)
        elif(sel_ch=="Majority Causes"):
            cause_counts = fil_df["Cause / Category"].value_counts().reset_index()
            cause_counts.columns = ["Cause", "Count"]
            
            # Optional: Show top 10 causes only
            top_n = 7
            cause_counts = cause_counts.head(top_n)
            
            # Create pie chart
            fig = px.pie(
            cause_counts,
            names="Cause",
            values="Count",
            title=f"Top {top_n} Causes of Incidents",
            hole=0.4,  # Donut-style
            )
            
            fig.update_traces(
            textinfo="percent+label",  # show both
            textfont_size=14,
            marker=dict(line=dict(color="#000000", width=1))
            )
            fig.update_layout(
            height=700,         # Increase height (default is ~450)
            width=1400, )

            st.plotly_chart(fig, use_container_width=True)
        elif(sel_ch=="Injury & Fatality Overview"):
            group=fil_df.groupby("SO")["Injury Others"]
            st.write("test",group)
