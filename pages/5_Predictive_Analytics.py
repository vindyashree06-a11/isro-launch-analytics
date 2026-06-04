import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from prophet import Prophet

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="🔮",
    layout="wide"
)

# ==========================================================
# LOAD CSS
# ==========================================================

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

# ==========================================================
# LOAD DATA
# ==========================================================

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

    df = df.dropna(
        subset=["Launch Date"]
    )

    df["Year"] = (
        df["Launch Date"]
        .dt.year
    )

    return df

df = load_data()

# ==========================================================
# HERO
# ==========================================================

st.markdown(
    """
    <div class='hero'>
        <h1>🔮 Predictive Analytics</h1>
        <p>
        Forecast Future ISRO Launch Activity
        Using Machine Learning
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# FORECAST SETTINGS
# ==========================================================

st.sidebar.title("⚙ Forecast Settings")

forecast_years = st.sidebar.slider(
    "Forecast Horizon (Years)",
    1,
    15,
    5
)

# ==========================================================
# PREPARE DATA
# ==========================================================

launches = (
    df.groupby("Year")
    .size()
    .reset_index(name="Launches")
)

launches["ds"] = pd.to_datetime(
    launches["Year"].astype(str)
)

launches["y"] = launches["Launches"]

prophet_df = launches[
    ["ds", "y"]
]

# ==========================================================
# KPI SECTION
# ==========================================================

total_launches = int(
    launches["Launches"].sum()
)

peak_year = int(
    launches.loc[
        launches["Launches"].idxmax()
    ]["Year"]
)

peak_launches = int(
    launches["Launches"].max()
)

avg_launches = round(
    launches["Launches"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Total Launches",
    total_launches
)

col2.metric(
    "📈 Avg / Year",
    avg_launches
)

col3.metric(
    "🏆 Peak Year",
    peak_year
)

col4.metric(
    "🛰 Peak Launches",
    peak_launches
)

st.markdown("---")

# ==========================================================
# HISTORICAL TREND
# ==========================================================

st.subheader("📊 Historical Launch Trend")

fig_hist = px.line(
    launches,
    x="Year",
    y="Launches",
    markers=True
)

fig_hist.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ==========================================================
# MOVING AVERAGE
# ==========================================================

st.subheader("📈 Trend Smoothing")

trend_df = launches.copy()

trend_df["3-Year MA"] = (
    trend_df["Launches"]
    .rolling(3)
    .mean()
)

fig_ma = go.Figure()

fig_ma.add_trace(
    go.Scatter(
        x=trend_df["Year"],
        y=trend_df["Launches"],
        name="Actual"
    )
)

fig_ma.add_trace(
    go.Scatter(
        x=trend_df["Year"],
        y=trend_df["3-Year MA"],
        name="Moving Average"
    )
)

fig_ma.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_ma,
    use_container_width=True
)

# ==========================================================
# PROPHET MODEL
# ==========================================================

st.subheader("🤖 Forecast Model")

with st.spinner(
    "Training Prophet Model..."
):

    model = Prophet(
        yearly_seasonality=True,
        changepoint_prior_scale=0.05
    )

    model.fit(
        prophet_df
    )

    future = model.make_future_dataframe(
        periods=forecast_years,
        freq="Y"
    )

    forecast = model.predict(
        future
    )

# ==========================================================
# FORECAST CHART
# ==========================================================

st.subheader("🚀 Future Launch Forecast")

fig_forecast = go.Figure()

fig_forecast.add_trace(
    go.Scatter(
        x=prophet_df["ds"],
        y=prophet_df["y"],
        mode="lines+markers",
        name="Historical"
    )
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode="lines",
        name="Forecast"
    )
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        line=dict(width=0),
        showlegend=False
    )
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        fill="tonexty",
        name="Confidence Interval"
    )
)

fig_forecast.update_layout(
    template="plotly_dark",
    height=650
)

st.plotly_chart(
    fig_forecast,
    use_container_width=True
)

# ==========================================================
# FORECAST COMPONENTS
# ==========================================================

st.subheader("📉 Trend Components")

forecast_view = forecast[
    [
        "ds",
        "trend",
        "yhat"
    ]
]

fig_components = px.line(
    forecast_view,
    x="ds",
    y=[
        "trend",
        "yhat"
    ]
)

fig_components.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_components,
    use_container_width=True
)

# ==========================================================
# FORECAST TABLE
# ==========================================================

st.subheader("📋 Forecast Results")

future_results = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
]

future_results.columns = [
    "Date",
    "Forecast",
    "Lower Bound",
    "Upper Bound"
]

st.dataframe(
    future_results.tail(
        forecast_years + 5
    ),
    use_container_width=True
)

# ==========================================================
# ANOMALY DETECTION
# ==========================================================

st.subheader("🚨 Launch Anomaly Detection")

z_score = (
    launches["Launches"]
    - launches["Launches"].mean()
) / launches["Launches"].std()

launches["Anomaly"] = (
    np.abs(z_score) > 2
)

anomalies = launches[
    launches["Anomaly"] == True
]

fig_anomaly = px.scatter(
    launches,
    x="Year",
    y="Launches",
    color="Anomaly",
    title="Launch Outlier Detection"
)

fig_anomaly.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig_anomaly,
    use_container_width=True
)

# ==========================================================
# FORECAST INSIGHTS
# ==========================================================

st.subheader("🧠 AI Forecast Insights")

future_launches = (
    forecast["yhat"]
    .tail(forecast_years)
)

avg_future = round(
    future_launches.mean(),
    2
)

max_future = round(
    future_launches.max(),
    2
)

growth = round(
    (
        future_launches.iloc[-1]
        - launches["Launches"].iloc[-1]
    )
    /
    launches["Launches"].iloc[-1]
    * 100,
    2
)

st.markdown(
    f"""
<div class='forecast-card'>

### Forecast Summary

🚀 Expected Average Launches:
<b>{avg_future}</b>

<br><br>

📈 Forecast Growth:
<b>{growth}%</b>

<br><br>

🛰 Peak Predicted Launches:
<b>{max_future}</b>

<br><br>

📅 Forecast Horizon:
<b>{forecast_years} Years</b>

<br><br>

🤖 Model:
<b>Facebook Prophet</b>

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DOWNLOAD FORECAST
# ==========================================================

st.subheader("⬇ Download Forecast")

csv = future_results.to_csv(
    index=False
)

st.download_button(
    label="Download Forecast CSV",
    data=csv,
    file_name="isro_forecast.csv",
    mime="text/csv"
)

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📄 Executive Summary")

summary = f"""
Historical launches analyzed: {total_launches}

Average launches per year: {avg_launches}

Peak launch year: {peak_year}

Forecast horizon: {forecast_years} years

Expected growth rate: {growth}%

Predicted average launches:
{avg_future}
"""

st.info(summary)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class='footer'>
        🔮 Predictive Analytics Dashboard
        <br>
        Forecasting • Trends • Anomaly Detection
    </div>
    """,
    unsafe_allow_html=True
)
