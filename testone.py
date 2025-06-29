import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
st.set_page_config(page_title="My Streamlit Dashboard", layout="wide")
st.title("📊 My Interactive Dashboard")

# Sidebar (optional)
st.sidebar.header("See ")
st.sidebar.write("Use the tabs above to explore different views.")

# Main tab setup
tab1, tab2, tab3 = st.tabs(["Q1: Airports", "Q2: University Dashboard", "Q3: Best & Worst Graph"])

with tab1:
    st.header("Chicago O'Hare Airport")
    st.write("This is a high-level overview of the data or project. You can add summaries, charts, or KPIs here.")


with tab2:
    st.header("University Student Admissions Dashboard")
    st.write("Add interactive graphs, filtering, or analysis in this section.")


with tab3:
    st.header("Gender Pay Gap Visualizations: Best & Worst")
    st.write("Conclude with key insights, recommendations, or downloads.")

