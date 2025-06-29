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
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    import streamlit as st

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

    # Load data
    flights = pd.read_csv("Airports_P 1.csv")
    airports = pd.read_csv("airports.csv")

    # Filter and enrich
    ord_flights = flights[flights['Destination_airport'] == 'ORD']
    ord_enriched = ord_flights.merge(
        airports[['IATA', 'AIRPORT', 'CITY', 'STATE', 'COUNTRY', 'LATITUDE', 'LONGITUDE']],
        how='left', left_on='Origin_airport', right_on='IATA'
    ).rename(columns={
        'AIRPORT': 'Origin_airport_name',
        'CITY': 'Origin_city',
        'STATE': 'Origin_state',
        'COUNTRY': 'Origin_country',
        'LATITUDE': 'Origin_latitude',
        'LONGITUDE': 'Origin_longitude'
    })

    ord_enriched_unique = ord_enriched.drop_duplicates(subset='Origin_airport')

    # Flight path map
    st.subheader("📺 Flight Paths into O'Hare")
    st.markdown("""
    This interactive map visualizes **unique flight routes into Chicago O'Hare International Airport (ORD)**.

    - Each line = a direct flight from a U.S. origin airport.
    - Color indicates **origin state**.
    - Hover to see origin airport, city, and state.
    """)

    unique_states = ord_enriched_unique['Origin_state'].unique()
    color_pool = px.colors.qualitative.Alphabet + px.colors.qualitative.Set3 + px.colors.qualitative.Dark24
    color_map = {state: color.replace('rgb', 'rgba').replace(')', ',0.5)') for state, color in zip(unique_states, color_pool)}

    flight_paths = [
        go.Scattergeo(
            locationmode='USA-states',
            lon=[row['Origin_longitude'], -87.9073],
            lat=[row['Origin_latitude'], 41.9742],
            mode='lines',
            line=dict(width=1, color=color_map[row['Origin_state']]),
            hoverinfo='text',
            text=f"{row['Origin_airport_name']} ({row['Origin_city']}, {row['Origin_state']})",
            name=row['Origin_state']
        ) for _, row in ord_enriched_unique.iterrows()
    ]

    fig = go.Figure(data=flight_paths)
    fig.update_layout(
        title="Unique Flight Routes into Chicago O'Hare (ORD) by Origin State",
        geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(243, 243, 243)',
                 subunitwidth=1, countrywidth=1, subunitcolor='rgb(217, 217, 217)', countrycolor='rgb(217, 217, 217)'),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Flights by state
    st.subheader("📊 Number of Flights into O'Hare by State")
    state_counts = ord_enriched['Origin_state'].value_counts().reset_index()
    state_counts.columns = ['Origin_state', 'Flight_Count']
    fig2 = go.Figure(go.Bar(
        x=state_counts['Origin_state'], y=state_counts['Flight_Count'],
        text=state_counts['Flight_Count'], textposition='outside', marker_color='green'))
    fig2.update_layout(
        title="Flights into Chicago O'Hare (ORD) by Origin State",
        xaxis_title="Origin State", yaxis_title="Number of Flights",
        xaxis_tickangle=-45, bargap=0.2, margin=dict(l=20, r=20, t=60, b=40))
    st.plotly_chart(fig2, use_container_width=True)

    # Stacked bar: population by city/state
    st.subheader("🏢 Origin City Populations by State")
    data = ord_enriched_unique[['Origin_state', 'Origin_city', 'Origin_airport_name', 'Origin_population']].dropna()
    state_totals = data.groupby('Origin_state')['Origin_population'].sum().sort_values(ascending=False)
    data['hover_text'] = data['Origin_airport_name'] + "<br>Population: " + data['Origin_population'].astype(int).astype(str)
    fig3 = px.bar(
        data, x='Origin_state', y='Origin_population', color='Origin_city', text='hover_text',
        category_orders={'Origin_state': state_totals.index.tolist()},
        labels={'Origin_population': 'Population', 'Origin_state': 'State'},
        title='Stacked Bar: Origin City Populations by State')
    fig3.update_traces(hoverinfo='text', texttemplate=None)
    fig3.update_layout(barmode='stack', xaxis_tickangle=-45, yaxis_title='Total Population (Sum)',
                       showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig3, use_container_width=True)

    # Population-normalized flight count
    st.subheader("✈️ Flights per 100,000 Residents by State")
    pop_by_state = ord_enriched_unique.groupby('Origin_state')['Origin_population'].sum().reset_index()
    flights_by_state = ord_enriched.groupby('Origin_state').size().reset_index(name='Flight_Count')
    combined = pd.merge(pop_by_state, flights_by_state, on='Origin_state')
    combined['Flights_per_100k'] = (combined['Flight_Count'] / combined['Origin_population']) * 100000
    combined['hover_text'] = "State: " + combined['Origin_state'] + "<br>Flights: " + combined['Flight_Count'].astype(str) + "<br>Population: " + combined['Origin_population'].astype(int).astype(str)
    combined = combined.sort_values(by='Flights_per_100k', ascending=False)
    fig4 = px.bar(
        combined, x='Flights_per_100k', y='Origin_state', orientation='h',
        text=combined['Flights_per_100k'].round(1),
        labels={'Flights_per_100k': 'Flights per 100,000 Residents', 'Origin_state': 'State'},
        title='Flights into ORD per 100,000 Residents by State')
    fig4.update_traces(hoverinfo='text', hovertext=combined['hover_text'], marker_color='darkgreen', textposition='outside')
    fig4.update_layout(xaxis_title='Flights per 100,000 Residents', yaxis_title='Origin State',
                       showlegend=False, margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig4, use_container_width=True)

    # Choropleth
    st.subheader("🌍 Choropleth Map: Flights per 100,000 Residents")
    fig5 = px.choropleth(
        combined,
        locations='Origin_state', locationmode='USA-states', color='Flights_per_100k',
        color_continuous_scale='Greens', scope='usa',
        hover_data={'Flights_per_100k': ':.1f', 'Flight_Count': True, 'Origin_population': True, 'Origin_state': False},
        labels={'Flights_per_100k': 'Flights per 100,000'},
        title='Flights into ORD per 100,000 Residents by State')
    fig5.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig5, use_container_width=True)


with tab2:
    st.header("University Student Admissions Dashboard")

    # Row 1 - Two columns, 50/50
    st.markdown("## Admissions and Enrollment")

    col1_row1, col2_row1 = st.columns(2)

     with col1_row1:
        st.subheader("Total Applications, Admissions, and Enrollment Over Time")

        # Load data
        students = pd.read_csv('university_student_dashboard_data.csv')

        # Create a combined 'Term Label' for x-axis (e.g., "2015 Spring")
        students['Term_Label'] = students['Year'].astype(str) + ' ' + students['Term']

        # Sort chronologically
        students = students.sort_values(by=['Year', 'Term'])

        # Reorder columns: largest first (Applications → Admitted → Enrolled)
        category_order = ['Enrolled', 'Admitted', 'Applications']

        # Melt with correct stacking order
        melted = students.melt(
            id_vars='Term_Label',
            value_vars=category_order,
            var_name='Category',
            value_name='Count'
        )

        # Reverse stacking order (largest on bottom)
        melted['Category'] = pd.Categorical(melted['Category'], categories=category_order, ordered=True)

        # Create stacked area chart
        fig = px.area(
            melted,
            x='Term_Label',
            y='Count',
            color='Category',
            category_orders={'Category': category_order},
            title='Applications, Admitted, and Enrolled by Term',
            labels={'Term_Label': 'Term', 'Count': 'Number of Students'},
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            margin=dict(l=40, r=40, t=50, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)


    with col2_row1:
        st.subheader("Enrollment by Deparment Over Time")

    # Spacer
    st.markdown("---")

    # Row 2 - Two columns, 75/25
    st.markdown("## Satisfaction, Retention, and Growth Rates")

    col1_row2, col2_row2 = st.columns([3, 1])

    with col1_row2:
        st.subheader("Department Growth and Satisfaction Rates")

    with col2_row2:
        st.subheader("Variations in Fall + Spring Semesters")



with tab3:
    st.header("Gender Pay Gap Visualizations: Best & Worst")
    st.write("Conclude with key insights, recommendations, or downloads.")

