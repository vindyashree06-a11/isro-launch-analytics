import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

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

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/ISRO mission launches.csv"
    )

    df.columns = df.columns.str.strip()

    if "Launch Date" in df.columns:

        df["Launch Date"] = pd.to_datetime(
            df["Launch Date"],
            errors="coerce"
        )

        df["Year"] = df["Launch Date"].dt.year

        df["Month"] = df["Launch Date"].dt.month_name()

    return df


df = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image(
    "assets/isro_logo.png",
    width=180
)

st.sidebar.title("🚀 ISRO Analytics")

vehicles = ["All"] + sorted(
    df["Launch Vehicle"].dropna().unique().tolist()
)

applications = ["All"] + sorted(
    df["Application"].dropna().unique().tolist()
)

orbits = ["All"] + sorted(
    df["Orbit Type"].dropna().unique().tolist()
)

vehicle_filter = st.sidebar.selectbox(
    "Launch Vehicle",
    vehicles
)

application_filter = st.sidebar.selectbox(
    "Mission Application",
    applications
)

orbit_filter = st.sidebar.selectbox(
    "Orbit Type",
    orbits
)

# ==========================================
# FILTER DATA
# ==========================================

filtered_df = df.copy()

if vehicle_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Launch Vehicle"] == vehicle_filter
    ]

if application_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Application"] == application_filter
    ]

if orbit_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Orbit Type"] == orbit_filter
    ]

# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    """
    <div class='hero'>
        <h1>🚀 ISRO Mission Analytics</h1>
        <p>
        Executive Dashboard for Mission Launch Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_launches = len(filtered_df)

total_vehicles = (
    filtered_df["Launch Vehicle"]
    .nunique()
)

total_orbits = (
    filtered_df["Orbit Type"]
    .nunique()
)

total_apps = (
    filtered_df["Application"]
    .nunique()
)

# ==========================================
# KPI ROW
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🚀 Total Launches",
        f"{total_launches:,}"
    )

with col2:
    st.metric(
        "🛰 Vehicles",
        total_vehicles
    )

with col3:
    st.metric(
        "🌍 Orbit Types",
        total_orbits
    )

with col4:
    st.metric(
        "📡 Applications",
        total_apps
    )

st.markdown("---")

# ==========================================
# YEARLY TREND
# ==========================================

if "Year" in filtered_df.columns:

    yearly = (
        filtered_df
        .groupby("Year")
        .size()
        .reset_index(name="Launch Count")
    )

    fig = px.line(
        yearly,
        x="Year",
        y="Launch Count",
        markers=True,
        title="Year-wise Launch Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# PIE CHARTS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    vehicle_counts = (
        filtered_df["Launch Vehicle"]
        .value_counts()
        .reset_index()
    )

    vehicle_counts.columns = [
        "Vehicle",
        "Count"
    ]

    fig_vehicle = px.pie(
        vehicle_counts,
        names="Vehicle",
        values="Count",
        hole=0.5,
        title="Launch Vehicle Distribution"
    )

    fig_vehicle.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )

with col2:

    orbit_counts = (
        filtered_df["Orbit Type"]
        .value_counts()
        .reset_index()
    )

    orbit_counts.columns = [
        "Orbit",
        "Count"
    ]

    fig_orbit = px.pie(
        orbit_counts,
        names="Orbit",
        values="Count",
        hole=0.5,
        title="Orbit Distribution"
    )

    fig_orbit.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_orbit,
        use_container_width=True
    )

# ==========================================
# APPLICATION ANALYSIS
# ==========================================

st.subheader("📡 Mission Applications")

app_counts = (
    filtered_df["Application"]
    .value_counts()
    .reset_index()
)

app_counts.columns = [
    "Application",
    "Count"
]

fig_apps = px.bar(
    app_counts,
    x="Application",
    y="Count",
    text="Count",
    title="Mission Application Distribution"
)

fig_apps.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_apps,
    use_container_width=True
)

# ==========================================
# SUNBURST
# ==========================================

st.subheader("🌞 Mission Hierarchy")

try:

    fig_sunburst = px.sunburst(
        filtered_df,
        path=[
            "Application",
            "Launch Vehicle",
            "Orbit Type"
        ]
    )

    fig_sunburst.update_layout(
        template="plotly_dark",
        height=650
    )

    st.plotly_chart(
        fig_sunburst,
        use_container_width=True
    )

except:
    st.info(
        "Sunburst chart could not be generated."
    )

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader("🧠 AI Generated Insights")

top_vehicle = (
    filtered_df["Launch Vehicle"]
    .value_counts()
    .idxmax()
)

top_app = (
    filtered_df["Application"]
    .value_counts()
    .idxmax()
)

top_orbit = (
    filtered_df["Orbit Type"]
    .value_counts()
    .idxmax()
)

peak_year = (
    filtered_df["Year"]
    .value_counts()
    .idxmax()
)

st.markdown(
    f"""
    <div class='insight-box'>

    <h4>📊 Key Findings</h4>

    ✔ Most frequently used launch vehicle:
    <b>{top_vehicle}</b>

    <br><br>

    ✔ Most common mission application:
    <b>{top_app}</b>

    <br><br>

    ✔ Dominant orbit category:
    <b>{top_orbit}</b>

    <br><br>

    ✔ Peak launch activity year:
    <b>{peak_year}</b>

    <br><br>

    ✔ Total missions analyzed:
    <b>{total_launches}</b>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# RECENT MISSIONS
# ==========================================

st.subheader("📋 Recent Missions")

display_cols = []

for col in [
    "Launch Date",
    "Launch Vehicle",
    "Orbit Type",
    "Application",
    "Remarks"
]:
    if col in filtered_df.columns:
        display_cols.append(col)

recent = (
    filtered_df
    .sort_values(
        "Launch Date",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    recent[display_cols],
    use_container_width=True
)

# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class='footer'>
        🚀 ISRO Mission Analytics Dashboard
        <br>
        Built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True
)
