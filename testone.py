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

    Select one major airport from the U.S. & using available flight route data:

    **Goals:**
    1. Map all the direct routes from the selected airport.
    2. Perform Exploratory Data Analysis (EDA) to understand:
        - Popular routes
        - Airport connectivity
        - Operational performance
    """)
    import plotly.graph_objects as go
import plotly.express as px

st.subheader("🗺️ Flight Paths into O'Hare")
# Ensure data is loaded and merged
flights = pd.read_csv("Airports_P 1.csv")     # Flight data
airports = pd.read_csv("airports.csv")        # Airport metadata

# Filter flights arriving at ORD
ord_flights = flights[flights['Destination_airport'] == 'ORD']

# Merge airport info into ORD flight records
ord_enriched = ord_flights.merge(
    airports[['IATA', 'AIRPORT', 'CITY', 'STATE', 'COUNTRY', 'LATITUDE', 'LONGITUDE']],
    how='left',
    left_on='Origin_airport',
    right_on='IATA'
)

# Rename for clarity
ord_enriched = ord_enriched.rename(columns={
    'AIRPORT': 'Origin_airport_name',
    'CITY': 'Origin_city',
    'STATE': 'Origin_state',
    'COUNTRY': 'Origin_country',
    'LATITUDE': 'Origin_latitude',
    'LONGITUDE': 'Origin_longitude'
})

# Drop duplicates by origin airport (if needed)
ord_enriched_unique = ord_enriched.drop_duplicates(subset='Origin_airport')

st.markdown("""
This interactive map visualizes **unique flight routes into Chicago O'Hare International Airport (ORD)**. Each route line represents a direct connection from a U.S. airport, and the color indicates the **origin state** of the flight.

- Hover over a route to see the **origin airport name, city, and state**.
- All lines are displayed at **50% transparency** to reveal route density visually.
""")

# Get a list of unique states
unique_states = ord_enriched_unique['Origin_state'].unique()

# Use a long Plotly qualitative color scale
color_pool = px.colors.qualitative.Alphabet + px.colors.qualitative.Set3 + px.colors.qualitative.Dark24
if len(unique_states) > len(color_pool):
    st.error("Not enough unique colors for the number of states.")
else:
    # Create color map with 50% transparency
    color_map = {
        state: color.replace('rgb', 'rgba').replace(')', ',0.5)')
        for state, color in zip(unique_states, color_pool)
    }

    # Create flight path lines
    flight_paths = []
    for i, row in ord_enriched_unique.iterrows():
        state = row['Origin_state']
        color = color_map[state]

        flight_paths.append(
            go.Scattergeo(
                locationmode='USA-states',
                lon=[row['Origin_longitude'], -87.9073],
                lat=[row['Origin_latitude'], 41.9742],
                mode='lines',
                line=dict(width=1, color=color),
                hoverinfo='text',
                text=f"{row['Origin_airport_name']} ({row['Origin_city']}, {row['Origin_state']})",
                name=row['Origin_state']
            )
        )

    # Plot the map
    fig = go.Figure(data=flight_paths)

    fig.update_layout(
        title="Unique Flight Routes into Chicago O'Hare (ORD) by Origin State",
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor='rgb(217, 217, 217)',
            countrycolor='rgb(217, 217, 217)'
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Number of Flights into O'Hare by State")

st.markdown("""
This bar chart shows the **volume of flights into Chicago O'Hare (ORD)**, grouped by the **state of the origin airport**.

- The chart helps highlight which states send the most flights to ORD.
- Use this to identify regional concentrations, travel corridors, or high-traffic partnerships.
""")

# Count flights per origin state
state_counts = ord_enriched['Origin_state'].value_counts().reset_index()
state_counts.columns = ['Origin_state', 'Flight_Count']
state_counts = state_counts.sort_values(by='Flight_Count', ascending=False)

# Create bar chart
fig2 = go.Figure(go.Bar(
    x=state_counts['Origin_state'],
    y=state_counts['Flight_Count'],
    text=state_counts['Flight_Count'],
    textposition='outside',
    marker_color='green'
))

fig2.update_layout(
    title="Flights into Chicago O'Hare (ORD) by Origin State",
    xaxis_title="Origin State",
    yaxis_title="Number of Flights",
    xaxis_tickangle=-45,
    bargap=0.2,
    margin=dict(l=20, r=20, t=60, b=40)
)

st.plotly_chart(fig2, use_container_width=True)




with tab2:
    st.header("University Student Admissions Dashboard")
    st.write("Add interactive graphs, filtering, or analysis in this section.")


with tab3:
    st.header("Gender Pay Gap Visualizations: Best & Worst")
    st.write("Conclude with key insights, recommendations, or downloads.")

