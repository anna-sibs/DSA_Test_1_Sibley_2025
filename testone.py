import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
st.set_page_config(page_title="My Streamlit Dashboard", layout="wide")
st.title("Bridget Anna Sibley Test 1 DSA 506")

# Sidebar (optional)
st.sidebar.header("See ")
st.sidebar.write("Use the tabs above to explore different views.")

# Main tab setup
tab1, tab2, tab3 = st.tabs(["Q1: Airports", "Q2: University Dashboard", "Q3: Best & Worst Graph"])

with tab1:
    st.header("🛫 Chicago O'Hare International Airport (ORD)")

    st.markdown("""
    ### ✈️ Problem 1: Flight Route Analysis

    Select one major airport from the U.S. East Coast (e.g., **JFK**, **ATL**, **MIA**, **BOS**, **PHL**, etc.). Using available flight route data:

    **Goals:**
    1. 🗺️ Map all the direct routes from the selected airport.
    2. 📊 Perform Exploratory Data Analysis (EDA) to understand:
        - Popular routes
        - Airport connectivity
        - Operational performance

    **Suggested EDA Questions:**
    - 🔝 What are the **top 5 destinations** by number of flights?
    - 🕒 How does **flight volume vary by time of day or season**?
    - 🧭 What percentage of flights are **domestic vs. international**?
    - 🛬 Are there any **hub airports with significant traffic connections**?
    - 🛫 What are the most **frequent airlines** operating from this airport?
    """)



with tab2:
    st.header("University Student Admissions Dashboard")
    st.write("Add interactive graphs, filtering, or analysis in this section.")


with tab3:
    st.header("Gender Pay Gap Visualizations: Best & Worst")
    st.write("Conclude with key insights, recommendations, or downloads.")

