import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
st.set_page_config(page_title="My Streamlit Dashboard", layout="wide")
st.title("Bridget Anna Sibley Test 1 DSA 506")

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

    st.markdown("""
    ### Learnings:
    
    As a major international airport and travel hub, **Chicago O'Hare** is a destination flight for airports around the world.  
    The following graphic supports this knowledge — the sheer number of airport flights is clearly visible.  
    Few patterns are visible otherwise, as color can only distinguish between limited variables.
    """)
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
    st.markdown("""
    ### Learnings:
    
    This graphic more clearly shows which airports send the most flights to **Chicago**.  
    The top four states have unclear reasons for being so: **New York** and **California**, with large state populations and more than one international travel hub, are logical front runners — but otherwise there isn't a clear pattern?
    """)

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
    st.markdown("""
    ### Learnings:
    
    Examining the populations represented by airports sending flights to **Chicago**, more is revealed.  
    **New York** has two large airports that service the largest population in the country.  
    This graphic shows that one reason a state may send more flights to Chicago than another is if it happens to have airports servicing a large population of people.
    """)

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
    st.markdown("""
    ### Learnings:
    
    When examining how many flights are sent to **Chicago per capita** by state, additional findings emerge.  
    The states with high numbers of flights per capita tend to be **small population states** without major travel hubs or international airports—outliers rather than meaningful trends.  
    Interestingly, **New York**, despite sending the most total flights to Chicago, has one of the **lowest numbers of flights per capita**.
    """)

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
    st.markdown("""
    ### Learnings:
    
    Another view of the **number of flights to Chicago per capita**.  
    Areas to consider investigating in the future include **why Vermont and Iowa** have such high numbers of flights to Chicago.
    """)


with tab2:
    st.markdown("""
    ### Problem 2: University Student Admissions Dashboard
    
    An academic institution wants to monitor their admission process and students' satisfaction.  
    Design a university dashboard that tracks student admissions, retention, and satisfaction using the dataset `university_student_dashboard_data.csv`.
    
    **Metrics & KPIs:**
    1. Total applications, admissions, and enrollments per term  
    2. Retention rate trends over time  
    3. Student satisfaction scores over the years  
    4. Enrollment breakdown by department (Engineering, Business, Arts, Science)  
    5. Comparison between Spring vs. Fall term trends  
    6. Comparison of trends between departments, retention rates, and satisfaction levels  
    
    **Dashboard Implementation:**
    1. Create a prototype in Python using Streamlit (hosted on Streamlit Cloud)  
    2. Ensure the dashboard provides insights on student trends over multiple years  
    3. Provide key findings and actionable insights  
    """)


    # Load and prepare data
    students = pd.read_csv('university_student_dashboard_data.csv')
    students['Term_Label'] = students['Year'].astype(str) + ' ' + students['Term']

    # Year Filter Below Header
    st.markdown("Use the dropdown below to filter by academic year:")
    all_years = sorted(students['Year'].unique())
    selected_years = st.multiselect(
        label="Select Year(s):",
        options=all_years,
        default=all_years
    )

    filtered_students = students[students['Year'].isin(selected_years)].copy()

    # Row 1 - Two columns
    st.markdown("## Admissions and Enrollment")
    col1_row1, col2_row1 = st.columns(2)

    with col1_row1:
        st.subheader("Total Applications, Admissions, and Enrollment Over Time")

        category_order = ['Enrolled', 'Admitted', 'Applications']
        melted = filtered_students.melt(
            id_vars='Term_Label',
            value_vars=category_order,
            var_name='Category',
            value_name='Count'
        )
        melted['Category'] = pd.Categorical(melted['Category'], categories=category_order, ordered=True)

        fig_admissions = px.area(
            melted,
            x='Term_Label',
            y='Count',
            color='Category',
            category_orders={'Category': category_order},
            title='Applications, Admitted, and Enrolled by Term',
            labels={'Term_Label': 'Term', 'Count': 'Number of Students'},
        )

        fig_admissions.update_layout(
            xaxis_tickangle=-45,
            margin=dict(l=40, r=40, t=50, b=40)
        )

        st.plotly_chart(fig_admissions, use_container_width=True)

    with col2_row1:
        st.subheader("Enrollment by Department Over Time")

        majors = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        filtered_students['Total_Enrolled'] = filtered_students[majors].sum(axis=1)

        fig_departments = go.Figure()
        for i, major in enumerate(majors):
            percent = (filtered_students[major] / filtered_students['Total_Enrolled'] * 100).round(1)
            hover_text = (
                "<b>Term:</b> " + filtered_students['Term_Label'] + "<br>" +
                f"<b>{major}:</b> " + filtered_students[major].map('{:,}'.format) +
                " (" + percent.map('{:.1f}'.format) + "% of total)"
            )

            fig_departments.add_trace(go.Scatter(
                x=filtered_students['Term_Label'],
                y=filtered_students[major],
                mode='lines',
                name=major,
                stackgroup='one',
                line=dict(width=0.5),
                marker=dict(color=colors[i]),
                hoverinfo='text',
                hovertext=hover_text,
                opacity=0.9
            ))

        fig_departments.update_layout(
            title='Enrolled Students by Major Over Time (% in Hover)',
            xaxis=dict(title='Term', tickangle=-45),
            yaxis=dict(title='Number of Enrolled Students'),
            showlegend=True,
            margin=dict(l=40, r=40, t=60, b=40),
            legend_title_text='Major'
        )

        st.plotly_chart(fig_departments, use_container_width=True)

    # Spacer
    st.markdown("---")

    # Row 2 - Two columns, 75/25
    st.markdown("## Satisfaction, Retention, and Growth Rates")
    col1_row2, col2_row2 = st.columns([7,5])

    with col1_row2:
        st.subheader("Department Growth and Satisfaction Rates")

        subjects = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
        subject_colors = {
            'Engineering Enrolled': '#1f77b4',
            'Business Enrolled': '#ff7f0e',
            'Arts Enrolled': '#2ca02c',
            'Science Enrolled': '#d62728'
        }

        yearly = filtered_students.groupby('Year')[subjects + ['Student Satisfaction (%)']].sum().reset_index()
        growth = yearly.copy()
        for subject in subjects:
            growth[subject] = yearly[subject].pct_change() * 100
        growth['Satisfaction Change'] = yearly['Student Satisfaction (%)'].diff()

        fig_growth_satisfaction = go.Figure()
        for subject in subjects:
            fig_growth_satisfaction.add_trace(go.Bar(
                x=growth['Year'],
                y=growth[subject],
                name=subject.replace(' Enrolled', ''),
                marker_color=subject_colors[subject],
                hovertemplate=f"%{{y:.1f}}% change<br><b>{subject.replace(' Enrolled', '')}</b><br>Year: %{{x}}<extra></extra>"
            ))

        fig_growth_satisfaction.add_trace(go.Scatter(
            x=growth['Year'],
            y=growth['Satisfaction Change'],
            mode='lines+markers',
            name='Change in Satisfaction Rate (%)',
            line=dict(color='black', width=3, dash='dot'),
            marker=dict(size=7),
            yaxis='y2',
            hovertemplate="Change: %{y:.1f}%<br>Year: %{x}<extra></extra>"
        ))

        for year in growth['Year'][1:]:
            fig_growth_satisfaction.add_vline(
                x=year - 0.5,
                line=dict(color='lightgray', width=1, dash='dash'),
                layer='below'
            )

        fig_growth_satisfaction.update_layout(
            title='Year-over-Year Enrollment Growth by Subject Area<br>with Change in Student Satisfaction Rate',
            xaxis_title='Year',
            yaxis=dict(title='Enrollment Growth (%)'),
            yaxis2=dict(
                title='Change in Satisfaction Rate (%)',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            barmode='group',
            legend=dict(
                title='Metric',
                x=1.05,
                y=1,
                xanchor='left',
                yanchor='top'
            ),
            margin=dict(l=80, r=200, t=100, b=80),
            hovermode='x unified',
            plot_bgcolor='white'
        )

        st.plotly_chart(fig_growth_satisfaction, use_container_width=True)

with col2_row2:
        st.subheader("Retention and Satisfaction Over Time")
        fig_rates = go.Figure()

        # Add Retention Rate line
        fig_rates.add_trace(go.Scatter(
            x=filtered_students['Term_Label'],
            y=filtered_students['Retention Rate (%)'],
            mode='lines+markers',
            name='Retention Rate (%)',
            line=dict(color='darkgreen', width=3),
            marker=dict(size=6)
        ))
    
        # Add Satisfaction Rate line
        fig_rates.add_trace(go.Scatter(
            x=filtered_students['Term_Label'],
            y=filtered_students['Student Satisfaction (%)'],
            mode='lines+markers',
            name='Student Satisfaction (%)',
            line=dict(color='royalblue', width=3),
            marker=dict(size=6)
        ))
    
        # Layout
        fig_rates.update_layout(
            title='Student Satisfaction and Retention Rates Over Time',
            xaxis=dict(title='Term', tickangle=-45),
            yaxis=dict(title='Percent (%)', tickformat=".0f"),
            showlegend=True,
            legend_title_text='Metric',
            margin=dict(l=40, r=40, t=60, b=60)
        )
    
        st.plotly_chart(fig_rates, use_container_width=True)



        
with tab3:
    st.markdown("""
### Problem 3: Gender Pay Gap Visualizations: Best & Worst

Find a real-world dataset from an open-source repository (Kaggle, Data.gov, UCI Machine Learning Repository, Open Data Portals).  
Perform an Exploratory Data Analysis (EDA) and create two visualizations for the same insight:

1. **The WORST possible plot**: A poorly designed visualization that misrepresents the data, is cluttered, lacks readability, or is misleading.  
2. **The IMPROVED version**: A refined visualization that enhances clarity, conveys insight effectively, and follows best practices in visual analytics.  
   
Include a brief explanation comparing both visualizations.
""")

    col1_row2, _ = st.columns([1, 0.01])  # single wide column, slight spacing

    with col1_row2:
        st.subheader("Ugly Earnings Chart")

                    
        # Load dataset
        genderpay = pd.read_csv('Glassdoor Gender Pay Gap.csv')

        # Calculate total earnings
        genderpay['TotalPay'] = genderpay['BasePay'] + genderpay['Bonus']
        totals = genderpay.groupby('Gender')['TotalPay'].sum()

        # Plotting
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(totals.index, totals.values, color='orange')

        # Add labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + height * 0.02,
                f'${int(height):,}',
                ha='center',
                color='orange',
                fontsize=12,
                weight='bold'
            )

        # Styling
        ax.set_title('Total Earnings by Gender', color='orange', fontsize=14, weight='bold')
        ax.set_ylabel('Total Earnings ($)', color='orange', fontsize=12)
        ax.spines['bottom'].set_color('orange')
        ax.spines['left'].set_color('orange')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Better Chart Highlighting Gender Pay Disparities")
        
        # Header
        st.header("Gender Pay Gap Across Dimensions")
        
        # Load dataset
        genderpay = pd.read_csv('Glassdoor Gender Pay Gap.csv')
        
        # Create TotalPay column
        genderpay['TotalPay'] = genderpay['BasePay'] + genderpay['Bonus']
        
        # Define dimensions and display names
        group_cols = ['JobTitle', 'Education', 'Dept', 'Seniority', 'PerfEval', 'Age']
        dimension_labels = {
            'JobTitle': 'Job Title',
            'Education': 'Education Level',
            'Dept': 'Department',
            'Seniority': 'Seniority Level',
            'PerfEval': 'Performance Evaluation',
            'Age': 'Age Group'
        }
        
        # Process data into normalized earnings ratios
        all_results = []
        for col in group_cols:
            group = genderpay.groupby([col, 'Gender'])['TotalPay'].mean().reset_index()
            pivot = group.pivot(index=col, columns='Gender', values='TotalPay')
            pivot['Male_ratio'] = pivot['Male'] / pivot[['Male', 'Female']].max(axis=1)
            pivot['Female_ratio'] = pivot['Female'] / pivot[['Male', 'Female']].max(axis=1)
            result = pivot[['Male_ratio', 'Female_ratio']].rename(columns={'Male_ratio': 'Male', 'Female_ratio': 'Female'}).reset_index()
            result['Dimension'] = dimension_labels[col]
            result = result.rename(columns={col: 'Category'})
            all_results.append(result)
        
        # Combine into one dataframe
        final_df = pd.concat(all_results, ignore_index=True)
        final_df = final_df[['Dimension', 'Category', 'Male', 'Female']]
        
        # Compute summary
        def compute_summary(group):
            num_groups = group['Category'].nunique()
            avg_male = int(round(group['Male'].mean() * 100))
            avg_female = int(round(group['Female'].mean() * 100))
            avg_gap = int(round((group['Male'] - group['Female']).abs().mean() * 100))
            female_less = (group['Female'] < group['Male']).sum()
            percent_female_less = int(round((female_less / num_groups) * 100))
            return pd.Series({
                'Number of Categories': num_groups,
                '% of Categories Where Women Earn Less': percent_female_less,
                'Average Male Earnings (%)': avg_male,
                'Average Female Earnings (%)': avg_female,
                'Average Earnings Gap (%)': avg_gap
            })
        
        summary = final_df.groupby('Dimension').apply(compute_summary).reset_index()
        
        # Dropdown to view by dimension
        dimension_choice = st.selectbox("Select Dimension to View Category-Level Pay Ratios:", sorted(final_df['Dimension'].unique()))
        filtered_view = final_df[final_df['Dimension'] == dimension_choice]
        
        # Show tables
        st.subheader("For Every $1 Made by a Man, Women will Earn Less by Almost All Dimensions.")
        st.dataframe(filtered_view.style.format({'Male': '{:.2%}', 'Female': '{:.2%}'}))
        
    


    


