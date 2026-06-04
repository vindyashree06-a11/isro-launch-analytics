import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Mission Analytics",
    page_icon="📊",
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

    df = df.dropna(subset=["Launch Date"])

    df["Year"] = df["Launch Date"].dt.year
    df["Month"] = df["Launch Date"].dt.month
    df["Month Name"] = df["Launch Date"].dt.month_name()
    df["Quarter"] = df["Launch Date"].dt.quarter

    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class='hero'>
        <h1>📊 Mission Analytics</h1>
        <p>Deep Exploration of ISRO Launch Trends & Growth</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("🔍 Filters")

if (
    "Year" not in df.columns
    or df["Year"].isna().all()
):

    st.error(
        "Year column is empty."
    )

    st.stop()

min_year = int(
    df["Year"]
    .dropna()
    .min()
)

max_year = int(
    df["Year"]
    .dropna()
    .max()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (
        min_year,
        max_year
    )
)

filtered_df = df[
    (
        df["Year"] >= year_range[0]
    )
    &
    (
        df["Year"] <= year_range[1]
    )
]

if filtered_df.empty:

    st.warning(
        "No records found for selected range."
    )

    st.stop()
# year_range = st.sidebar.slider(
#     "Select Year Range",
#     int(df["Year"].min()),
#     int(df["Year"].max()),
#     (
#         int(df["Year"].min()),
#         int(df["Year"].max())
#     )
# )

# filtered_df = df[
#     (df["Year"] >= year_range[0]) &
#     (df["Year"] <= year_range[1])
# ]

# =====================================================
# KPI SECTION
# =====================================================

total_launches = len(filtered_df)

active_years = (
    filtered_df["Year"].nunique()
)

avg_launches = round(
    total_launches / active_years,
    2
)

peak_year = (
    filtered_df["Year"]
    .value_counts()
    .idxmax()
)

peak_launches = (
    filtered_df["Year"]
    .value_counts()
    .max()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Total Launches",
    total_launches
)

col2.metric(
    "📅 Active Years",
    active_years
)

col3.metric(
    "📈 Avg Launches / Year",
    avg_launches
)

col4.metric(
    "🏆 Peak Year",
    peak_year
)

st.markdown("---")

# =====================================================
# YEARLY TREND
# =====================================================

st.subheader("📈 Annual Launch Trend")

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
    title="Year-wise Launch Activity"
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# CUMULATIVE GROWTH
# =====================================================

st.subheader("🚀 Cumulative Launch Growth")

yearly["Cumulative Launches"] = (
    yearly["Launch Count"]
    .cumsum()
)

fig_growth = px.area(
    yearly,
    x="Year",
    y="Cumulative Launches",
    title="Cumulative Launch Growth"
)

fig_growth.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# =====================================================
# YEAR-OVER-YEAR GROWTH
# =====================================================

st.subheader("📊 Year-over-Year Growth")

yearly["Growth %"] = (
    yearly["Launch Count"]
    .pct_change() * 100
)

fig_yoy = px.bar(
    yearly,
    x="Year",
    y="Growth %",
    text_auto=".1f",
    title="YoY Launch Growth (%)"
)

fig_yoy.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_yoy,
    use_container_width=True
)

# =====================================================
# MONTHLY ANALYSIS
# =====================================================

st.subheader("🗓 Monthly Launch Distribution")

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

monthly = (
    filtered_df
    .groupby("Month Name")
    .size()
    .reset_index(name="Launch Count")
)

monthly["Month Name"] = pd.Categorical(
    monthly["Month Name"],
    categories=month_order,
    ordered=True
)

monthly = monthly.sort_values(
    "Month Name"
)

fig_month = px.bar(
    monthly,
    x="Month Name",
    y="Launch Count",
    title="Launches by Month"
)

fig_month.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Launch Heatmap")

heat_df = (
    filtered_df
    .groupby(
        ["Year", "Month"]
    )
    .size()
    .reset_index(name="Launch Count")
)

pivot = heat_df.pivot(
    index="Month",
    columns="Year",
    values="Launch Count"
).fillna(0)

fig_heat = px.imshow(
    pivot,
    labels=dict(
        x="Year",
        y="Month",
        color="Launches"
    ),
    aspect="auto"
)

fig_heat.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# =====================================================
# QUARTER ANALYSIS
# =====================================================

st.subheader("📆 Quarterly Analysis")

quarterly = (
    filtered_df
    .groupby("Quarter")
    .size()
    .reset_index(name="Launch Count")
)

fig_quarter = px.pie(
    quarterly,
    names="Quarter",
    values="Launch Count",
    hole=0.45,
    title="Launches by Quarter"
)

fig_quarter.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_quarter,
    use_container_width=True
)

# =====================================================
# TOP YEARS
# =====================================================

st.subheader("🏆 Top Launch Years")

top_years = (
    filtered_df["Year"]
    .value_counts()
    .reset_index()
)

top_years.columns = [
    "Year",
    "Launch Count"
]

top_years = top_years.sort_values(
    "Launch Count",
    ascending=False
).head(10)

fig_top = px.bar(
    top_years,
    x="Year",
    y="Launch Count",
    text="Launch Count",
    title="Top 10 Launch Years"
)

fig_top.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

# =====================================================
# MISSION TIMELINE
# =====================================================

st.subheader("📍 Mission Timeline")

timeline_df = filtered_df.copy()

timeline_df["Mission"] = (
    timeline_df["Launch Vehicle"]
    .astype(str)
)

fig_timeline = px.scatter(
    timeline_df,
    x="Launch Date",
    y="Launch Vehicle",
    color="Application",
    hover_data=[
        "Orbit Type",
        "Remarks"
    ]
    if "Remarks" in timeline_df.columns
    else None,
    title="Mission Timeline"
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
# INSIGHTS
# =====================================================

st.subheader("🧠 Automated Insights")

best_month = (
    monthly.sort_values(
        "Launch Count",
        ascending=False
    )
    .iloc[0]["Month Name"]
)

st.markdown(
    f"""
<div class='insight-box'>

### Key Findings

✅ Total missions analyzed: **{total_launches}**

✅ Peak launch year: **{peak_year}**
with **{peak_launches} launches**

✅ Average launches per year:
**{avg_launches}**

✅ Most active launch month:
**{best_month}**

✅ Active operational span:
**{active_years} years**

</div>
""",
    unsafe_allow_html=True
)

# =====================================================
# RAW DATA EXPLORER
# =====================================================

st.subheader("📋 Mission Explorer")

search = st.text_input(
    "Search Launch Vehicle / Application"
)

display_df = filtered_df.copy()

if search:

    display_df = display_df[
        display_df.astype(str)
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
    display_df,
    use_container_width=True,
    height=500
)

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class='footer'>
        🚀 ISRO Mission Analytics Dashboard
        <br>
        Mission Trends • Growth Analytics • Historical Exploration
    </div>
    """,
    unsafe_allow_html=True
)
