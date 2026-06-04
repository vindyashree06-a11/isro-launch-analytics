"""
====================================================
ISRO Mission Analytics
Chart Library
Reusable Plotly Visualizations
====================================================
"""

import plotly.express as px
import plotly.graph_objects as go


# ====================================================
# GLOBAL CONFIG
# ====================================================

PLOTLY_TEMPLATE = "plotly_dark"

DEFAULT_HEIGHT = 500


# ====================================================
# KPI COLOR HELPERS
# ====================================================

def apply_layout(fig, title=None, height=DEFAULT_HEIGHT):

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        title=title,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return fig


# ====================================================
# YEARLY TREND
# ====================================================

def yearly_trend_chart(df):

    fig = px.line(
        df,
        x="Year",
        y="Launch_Count",
        markers=True
    )

    return apply_layout(
        fig,
        "Annual Launch Trend"
    )


# ====================================================
# CUMULATIVE TREND
# ====================================================

def cumulative_launch_chart(df):

    fig = px.area(
        df,
        x="Year",
        y="Cumulative_Launches"
    )

    return apply_layout(
        fig,
        "Cumulative Launch Growth"
    )


# ====================================================
# YOY GROWTH
# ====================================================

def yoy_growth_chart(df):

    fig = px.bar(
        df,
        x="Year",
        y="Growth_%",
        text_auto=".1f"
    )

    return apply_layout(
        fig,
        "Year-over-Year Growth"
    )


# ====================================================
# VEHICLE DISTRIBUTION
# ====================================================

def vehicle_distribution_chart(df):

    fig = px.bar(
        df,
        x="Vehicle",
        y="Launches",
        text="Launches"
    )

    return apply_layout(
        fig,
        "Launch Vehicle Distribution"
    )


# ====================================================
# VEHICLE PIE
# ====================================================

def vehicle_share_chart(df):

    fig = px.pie(
        df,
        names="Vehicle",
        values="Launches",
        hole=0.45
    )

    return apply_layout(
        fig,
        "Vehicle Share"
    )


# ====================================================
# ORBIT DISTRIBUTION
# ====================================================

def orbit_distribution_chart(df):

    fig = px.bar(
        df,
        x="Orbit",
        y="Launches",
        text="Launches"
    )

    return apply_layout(
        fig,
        "Orbit Distribution"
    )


# ====================================================
# ORBIT PIE
# ====================================================

def orbit_share_chart(df):

    fig = px.pie(
        df,
        names="Orbit",
        values="Launches",
        hole=0.45
    )

    return apply_layout(
        fig,
        "Orbit Share"
    )


# ====================================================
# APPLICATION DISTRIBUTION
# ====================================================

def application_distribution_chart(df):

    fig = px.bar(
        df,
        x="Application",
        y="Launches",
        text="Launches"
    )

    return apply_layout(
        fig,
        "Application Distribution"
    )


# ====================================================
# MONTHLY TREND
# ====================================================

def monthly_launch_chart(df):

    fig = px.bar(
        df,
        x="Month_Name",
        y="Launch_Count"
    )

    return apply_layout(
        fig,
        "Monthly Launch Analysis"
    )


# ====================================================
# HEATMAP
# ====================================================

def heatmap_chart(
    pivot_df,
    title="Heatmap"
):

    fig = px.imshow(
        pivot_df,
        aspect="auto",
        labels=dict(
            color="Launches"
        )
    )

    return apply_layout(
        fig,
        title,
        height=650
    )


# ====================================================
# VEHICLE TREND
# ====================================================

def vehicle_trend_chart(df):

    fig = px.line(
        df,
        x="Year",
        y="Launches",
        color="Launch_Vehicle",
        markers=True
    )

    return apply_layout(
        fig,
        "Vehicle Evolution",
        650
    )


# ====================================================
# ORBIT TREND
# ====================================================

def orbit_trend_chart(df):

    fig = px.line(
        df,
        x="Year",
        y="Launches",
        color="Orbit_Type",
        markers=True
    )

    return apply_layout(
        fig,
        "Orbit Evolution",
        650
    )


# ====================================================
# SUNBURST
# ====================================================

def sunburst_chart(
    df,
    path,
    values
):

    fig = px.sunburst(
        df,
        path=path,
        values=values
    )

    return apply_layout(
        fig,
        "Hierarchy Analysis",
        700
    )


# ====================================================
# TREEMAP
# ====================================================

def treemap_chart(
    df,
    path,
    values
):

    fig = px.treemap(
        df,
        path=path,
        values=values
    )

    return apply_layout(
        fig,
        "Treemap Analysis",
        650
    )


# ====================================================
# TIMELINE
# ====================================================

def mission_timeline_chart(
    df,
    y_col,
    color_col
):

    fig = px.scatter(
        df,
        x="Launch_Date",
        y=y_col,
        color=color_col
    )

    return apply_layout(
        fig,
        "Mission Timeline",
        650
    )


# ====================================================
# RADAR CHART
# ====================================================

def radar_vehicle_chart(df):

    fig = go.Figure()

    for _, row in df.iterrows():

        fig.add_trace(
            go.Scatterpolar(
                r=[
                    row["Launches"],
                    row["Orbit_Diversity"],
                    row["Mission_Diversity"]
                ],
                theta=[
                    "Launches",
                    "Orbit Diversity",
                    "Mission Diversity"
                ],
                fill="toself",
                name=row["Launch_Vehicle"]
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        template=PLOTLY_TEMPLATE,
        height=700
    )

    return fig


# ====================================================
# FORECAST CHART
# ====================================================

def forecast_chart(
    historical,
    forecast
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical["ds"],
            y=historical["y"],
            mode="lines+markers",
            name="Historical"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Forecast"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_upper"],
            line=dict(width=0),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_lower"],
            fill="tonexty",
            name="Confidence Interval"
        )
    )

    return apply_layout(
        fig,
        "Launch Forecast",
        700
    )


# ====================================================
# MOVING AVERAGE
# ====================================================

def moving_average_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Launches"],
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["3-Year MA"],
            name="Moving Average"
        )
    )

    return apply_layout(
        fig,
        "Trend Smoothing"
    )


# ====================================================
# ANOMALY CHART
# ====================================================

def anomaly_chart(df):

    fig = px.scatter(
        df,
        x="Year",
        y="Launch_Count",
        color="Anomaly"
    )

    return apply_layout(
        fig,
        "Anomaly Detection"
    )


# ====================================================
# SANKEY DIAGRAM
# ====================================================

def sankey_chart(
    labels,
    source,
    target,
    values
):

    fig = go.Figure(
        go.Sankey(
            node=dict(
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=values
            )
        )
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=700
    )

    return fig


# ====================================================
# KPI GAUGE
# ====================================================

def gauge_chart(
    value,
    title="Success Rate"
):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=350
    )

    return fig


# ====================================================
# EXECUTIVE SCORECARD
# ====================================================

def scorecard_chart(
    value,
    title
):

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=value,
            title={"text": title}
        )
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=250
    )

    return fig
