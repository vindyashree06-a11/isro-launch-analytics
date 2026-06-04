import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Vehicle Performance",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# LOAD CSS
# =====================================================

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/ISRO mission launches.csv"
    )

    df.columns = df.columns.str.strip()

    df["Launch Date"] = pd.to_datetime(
        df["Launch Date"],
        errors="coerce"
    )

    df["Year"] = df["Launch Date"].dt.year

    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class='hero'>
        <h1>🚀 Launch Vehicle Performance</h1>
        <p>
        Analyze vehicle utilization, growth,
        mission diversity and historical trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🚀 Vehicle Filters")

vehicle_list = sorted(
    df["Launch Vehicle"]
    .dropna()
    .unique()
)

selected_vehicle = st.sidebar.selectbox(
    "Select Vehicle",
    ["All"] + vehicle_list
)

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df.copy()

if selected_vehicle != "All":

    filtered_df = filtered_df[
        filtered_df["Launch Vehicle"]
        == selected_vehicle
    ]

# =====================================================
# KPI SECTION
# =====================================================

total_launches = len(filtered_df)

unique_orbits = (
    filtered_df["Orbit Type"]
    .nunique()
)

unique_apps = (
    filtered_df["Application"]
    .nunique()
)

active_years = (
    filtered_df["Year"]
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Launches",
    total_launches
)

col2.metric(
    "🌍 Orbit Types",
    unique_orbits
)

col3.metric(
    "📡 Applications",
    unique_apps
)

col4.metric(
    "📅 Active Years",
    active_years
)

st.markdown("---")

# =====================================================
# VEHICLE RANKING
# =====================================================

st.subheader("🏆 Launch Vehicle Ranking")

vehicle_counts = (
    df["Launch Vehicle"]
    .value_counts()
    .reset_index()
)

vehicle_counts.columns = [
    "Vehicle",
    "Launches"
]

fig_rank = px.bar(
    vehicle_counts,
    x="Vehicle",
    y="Launches",
    text="Launches",
    title="Launches by Vehicle"
)

fig_rank.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# =====================================================
# MARKET SHARE
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig_pie = px.pie(
        vehicle_counts,
        names="Vehicle",
        values="Launches",
        hole=0.45,
        title="Vehicle Market Share"
    )

    fig_pie.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

with col2:

    fig_treemap = px.treemap(
        vehicle_counts,
        path=["Vehicle"],
        values="Launches",
        title="Vehicle Usage Treemap"
    )

    fig_treemap.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_treemap,
        use_container_width=True
    )

# =====================================================
# VEHICLE TREND
# =====================================================

st.subheader("📈 Vehicle Trend Over Time")

trend = (
    df.groupby(
        ["Year", "Launch Vehicle"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_trend = px.line(
    trend,
    x="Year",
    y="Launches",
    color="Launch Vehicle",
    markers=True,
    title="Vehicle Evolution"
)

fig_trend.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# =====================================================
# VEHICLE LIFECYCLE
# =====================================================

st.subheader("📅 Vehicle Lifecycle Analysis")

life = (
    df.groupby("Launch Vehicle")
    .agg(
        First_Year=("Year", "min"),
        Last_Year=("Year", "max"),
        Launches=("Year", "count")
    )
    .reset_index()
)

life["Operational Span"] = (
    life["Last_Year"]
    - life["First_Year"]
) + 1

st.dataframe(
    life,
    use_container_width=True
)

# =====================================================
# ORBIT ANALYSIS
# =====================================================

st.subheader("🌍 Vehicle vs Orbit")

orbit_analysis = (
    filtered_df.groupby(
        ["Launch Vehicle", "Orbit Type"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_orbit = px.sunburst(
    orbit_analysis,
    path=[
        "Launch Vehicle",
        "Orbit Type"
    ],
    values="Launches"
)

fig_orbit.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(
    fig_orbit,
    use_container_width=True
)

# =====================================================
# APPLICATION ANALYSIS
# =====================================================

st.subheader("📡 Vehicle vs Application")

app_analysis = (
    filtered_df.groupby(
        ["Launch Vehicle", "Application"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_app = px.bar(
    app_analysis,
    x="Launch Vehicle",
    y="Launches",
    color="Application",
    title="Vehicle Mission Diversity"
)

fig_app.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_app,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Vehicle Heatmap")

heat_df = (
    df.groupby(
        ["Launch Vehicle", "Year"]
    )
    .size()
    .reset_index(name="Launches")
)

pivot = heat_df.pivot(
    index="Launch Vehicle",
    columns="Year",
    values="Launches"
).fillna(0)

fig_heat = px.imshow(
    pivot,
    labels=dict(
        x="Year",
        y="Vehicle",
        color="Launches"
    ),
    aspect="auto"
)

fig_heat.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# =====================================================
# RADAR CHART
# =====================================================

st.subheader("🎯 Vehicle Benchmark Radar")

radar = (
    df.groupby("Launch Vehicle")
    .agg(
        Launches=("Launch Vehicle", "count"),
        Orbits=("Orbit Type", "nunique"),
        Applications=("Application", "nunique")
    )
    .reset_index()
)

top5 = radar.sort_values(
    "Launches",
    ascending=False
).head(5)

fig_radar = go.Figure()

for _, row in top5.iterrows():

    fig_radar.add_trace(
        go.Scatterpolar(
            r=[
                row["Launches"],
                row["Orbits"],
                row["Applications"]
            ],
            theta=[
                "Launches",
                "Orbit Diversity",
                "Mission Diversity"
            ],
            fill="toself",
            name=row["Launch Vehicle"]
        )
    )

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig_radar,
    use_container_width=True
)

# =====================================================
# GROWTH ANALYSIS
# =====================================================

st.subheader("📊 Vehicle Growth Analysis")

growth = (
    df.groupby(
        ["Year", "Launch Vehicle"]
    )
    .size()
    .reset_index(name="Launches")
)

growth["Growth"] = (
    growth.groupby("Launch Vehicle")
    ["Launches"]
    .pct_change() * 100
)

fig_growth = px.line(
    growth,
    x="Year",
    y="Growth",
    color="Launch Vehicle",
    title="Year-over-Year Vehicle Growth"
)

fig_growth.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("🧠 AI Insights")

top_vehicle = (
    vehicle_counts
    .sort_values(
        "Launches",
        ascending=False
    )
    .iloc[0]["Vehicle"]
)

top_launches = (
    vehicle_counts
    .sort_values(
        "Launches",
        ascending=False
    )
    .iloc[0]["Launches"]
)

longest_span = (
    life.sort_values(
        "Operational Span",
        ascending=False
    )
    .iloc[0]
)

st.markdown(
    f"""
<div class='insight-box'>

### Key Findings

🚀 Most utilized vehicle:
**{top_vehicle}**

🚀 Total launches:
**{top_launches}**

🌍 Vehicle diversity:
**{len(vehicle_counts)} vehicles**

📅 Longest operational vehicle:
**{longest_span['Launch Vehicle']}**

📈 Operational span:
**{longest_span['Operational Span']} years**

📡 Mission categories supported:
**{df['Application'].nunique()}**

</div>
""",
    unsafe_allow_html=True
)

# =====================================================
# VEHICLE EXPLORER
# =====================================================

st.subheader("🔍 Vehicle Explorer")

st.dataframe(
    filtered_df.sort_values(
        "Launch Date",
        ascending=False
    ),
    use_container_width=True,
    height=500
)

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class='footer'>
        🚀 ISRO Vehicle Performance Analytics
        <br>
        Launch Vehicles • Utilization • Diversity • Growth
    </div>
    """,
    unsafe_allow_html=True
)
