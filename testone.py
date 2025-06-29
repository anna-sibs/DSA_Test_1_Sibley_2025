import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# App title
st.set_page_config(page_title="My Streamlit Dashboard", layout="wide")
st.title("📊 My Interactive Dashboard")

# Sidebar (optional)
st.sidebar.header("Navigation")
st.sidebar.write("Use the tabs above to explore different views.")

# Main tab setup
tab1, tab2, tab3 = st.tabs(["📈 Overview", "📂 Detailed Analysis", "📋 Summary & Insights"])

# -------- TAB 1: Overview --------
with tab1:
    st.header("Overview")
    st.write("This is a high-level overview of the data or project. You can add summaries, charts, or KPIs here.")
    
    # Example placeholder chart
    sample_data = pd.DataFrame({
        "Category": ["A", "B", "C"],
        "Value": [100, 200, 150]
    })
    st.bar_chart(sample_data.set_index("Category"))

# -------- TAB 2: Detailed Analysis --------
with tab2:
    st.header("Detailed Analysis")
    st.write("Add interactive graphs, filtering, or analysis in this section.")

    # Example interactive plot
    df = px.data.gapminder().query("year == 2007")
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                     hover_name="country", log_x=True, size_max=60)
    st.plotly_chart(fig, use_container_width=True)

# -------- TAB 3: Summary & Insights --------
with tab3:
    st.header("Summary & Insights")
    st.write("Conclude with key insights, recommendations, or downloads.")

    st.markdown("""
    - ✅ Key takeaway 1  
    - ✅ Key takeaway 2  
    - 📎 Add download buttons or export links here  
    """)

    # Optional file export
    st.download_button("📥 Download Sample CSV", data=sample_data.to_csv(index=False),
                       file_name="sample_data.csv", mime="text/csv")
