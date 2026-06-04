import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Orbit Insights",
    page_icon="🌍",
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
        <h1>🌍 Orbit Insights</h1>
        <p>
        Analyze Orbit Utilization, Mission Distribution,
        Vehicle Relationships and Historical Trends
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🌍 Orbit Filters")

orbit_options = sorted(
    df["Orbit Type"]
    .dropna()
    .unique()
)

selected_orbit = st.sidebar.selectbox(
    "Select Orbit",
    ["All"] + orbit_options
)

# =====================================================
# FILTER DATA
# =====================================================

filtered_df = df.copy()

if selected_orbit != "All":

    filtered_df = filtered_df[
        filtered_df["Orbit Type"]
        == selected_orbit
    ]

# =====================================================
# KPI SECTION
# =====================================================

total_missions = len(filtered_df)

orbit_count = (
    filtered_df["Orbit Type"]
    .nunique()
)

vehicle_count = (
    filtered_df["Launch Vehicle"]
    .nunique()
)

application_count = (
    filtered_df["Application"]
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Missions",
    total_missions
)

col2.metric(
    "🌍 Orbit Types",
    orbit_count
)

col3.metric(
    "🛰 Vehicles",
    vehicle_count
)

col4.metric(
    "📡 Applications",
    application_count
)

st.markdown("---")

# =====================================================
# ORBIT DISTRIBUTION
# =====================================================

st.subheader("🌎 Orbit Distribution")

orbit_dist = (
    df["Orbit Type"]
    .value_counts()
    .reset_index()
)

orbit_dist.columns = [
    "Orbit",
    "Launches"
]

fig_orbit = px.bar(
    orbit_dist,
    x="Orbit",
    y="Launches",
    text="Launches",
    title="Orbit Utilization"
)

fig_orbit.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_orbit,
    use_container_width=True
)

# =====================================================
# DONUT CHART
# =====================================================

col1, col2 = st.columns(2)

with col1:

    fig_donut = px.pie(
        orbit_dist,
        names="Orbit",
        values="Launches",
        hole=0.5,
        title="Orbit Share"
    )

    fig_donut.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )

with col2:

    fig_tree = px.treemap(
        orbit_dist,
        path=["Orbit"],
        values="Launches",
        title="Orbit Treemap"
    )

    fig_tree.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )

# =====================================================
# ORBIT EVOLUTION
# =====================================================

st.subheader("📈 Orbit Evolution Over Time")

orbit_year = (
    df.groupby(
        ["Year", "Orbit Type"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_evolution = px.line(
    orbit_year,
    x="Year",
    y="Launches",
    color="Orbit Type",
    markers=True,
    title="Orbit Trends"
)

fig_evolution.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_evolution,
    use_container_width=True
)

# =====================================================
# ORBIT VS VEHICLE
# =====================================================

st.subheader("🚀 Orbit vs Vehicle")

orbit_vehicle = (
    filtered_df.groupby(
        ["Orbit Type", "Launch Vehicle"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_sunburst = px.sunburst(
    orbit_vehicle,
    path=[
        "Orbit Type",
        "Launch Vehicle"
    ],
    values="Launches"
)

fig_sunburst.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(
    fig_sunburst,
    use_container_width=True
)

# =====================================================
# APPLICATION MAPPING
# =====================================================

st.subheader("📡 Orbit vs Application")

orbit_app = (
    filtered_df.groupby(
        ["Orbit Type", "Application"]
    )
    .size()
    .reset_index(name="Launches")
)

fig_app = px.bar(
    orbit_app,
    x="Orbit Type",
    y="Launches",
    color="Application",
    title="Application Distribution Across Orbits"
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

st.subheader("🔥 Orbit Heatmap")

heat_df = (
    df.groupby(
        ["Orbit Type", "Year"]
    )
    .size()
    .reset_index(name="Launches")
)

pivot = heat_df.pivot(
    index="Orbit Type",
    columns="Year",
    values="Launches"
).fillna(0)

fig_heat = px.imshow(
    pivot,
    labels=dict(
        x="Year",
        y="Orbit",
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
# ORBIT DIVERSITY
# =====================================================

st.subheader("🌍 Vehicle Orbit Diversity")

diversity = (
    df.groupby("Launch Vehicle")
    .agg(
        Orbit_Diversity=(
            "Orbit Type",
            "nunique"
        )
    )
    .reset_index()
)

fig_diversity = px.bar(
    diversity,
    x="Launch Vehicle",
    y="Orbit_Diversity",
    text="Orbit_Diversity",
    title="Unique Orbit Types Supported"
)

fig_diversity.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_diversity,
    use_container_width=True
)

# =====================================================
# ORBIT TIMELINE
# =====================================================

st.subheader("📅 Orbit Mission Timeline")

fig_timeline = px.scatter(
    filtered_df,
    x="Launch Date",
    y="Orbit Type",
    color="Launch Vehicle",
    hover_data=[
        "Application"
    ],
    title="Mission Orbit Timeline"
)

fig_timeline.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(
    fig_timeline,
    use_container_width=True
)

# =====================================================
# TOP ORBITS
# =====================================================

st.subheader("🏆 Top Orbit Categories")

top_orbits = (
    df["Orbit Type"]
    .value_counts()
    .reset_index()
)

top_orbits.columns = [
    "Orbit",
    "Launches"
]

st.dataframe(
    top_orbits,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("🧠 Orbit Intelligence")

top_orbit = (
    orbit_dist.iloc[0]["Orbit"]
)

top_launches = (
    orbit_dist.iloc[0]["Launches"]
)

max_diversity = (
    diversity.sort_values(
        "Orbit_Diversity",
        ascending=False
    )
    .iloc[0]
)

st.markdown(
    f"""
<div class='insight-box'>

### Key Orbit Insights

🌍 Most utilized orbit:
**{top_orbit}**

🚀 Missions in orbit:
**{top_launches}**

🛰 Vehicle with highest orbit diversity:
**{max_diversity['Launch Vehicle']}**

📈 Supported orbit categories:
**{max_diversity['Orbit_Diversity']}**

📡 Total orbit types:
**{df['Orbit Type'].nunique()}**

🚀 Total missions analyzed:
**{len(df)}**

</div>
""",
    unsafe_allow_html=True
)

# =====================================================
# ORBIT EXPLORER
# =====================================================

st.subheader("🔍 Orbit Explorer")

search = st.text_input(
    "Search Orbit / Vehicle / Application"
)

explorer = filtered_df.copy()

if search:

    explorer = explorer[
        explorer.astype(str)
        .apply(
            lambda x:
            x.str.contains(
                search,
                case=False
            )
        )
        .any(axis=1)
    ]

st.dataframe(
    explorer.sort_values(
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
        🌍 Orbit Intelligence Dashboard
        <br>
        Orbit Trends • Utilization • Mission Mapping
    </div>
    """,
    unsafe_allow_html=True
)
