```python
"""
==================================================
ISRO Mission Analytics
Analytics Engine
==================================================
"""

import pandas as pd
import numpy as np


# ==================================================
# KPI FUNCTIONS
# ==================================================

def total_launches(df):
    return len(df)


def total_vehicles(df):
    return df["Launch_Vehicle"].nunique()


def total_orbits(df):
    return df["Orbit_Type"].nunique()


def total_applications(df):
    return df["Application"].nunique()


def active_years(df):
    return df["Year"].nunique()


# ==================================================
# SUCCESS METRICS
# ==================================================

def success_rate(df):

    if "Mission_Status" not in df.columns:
        return None

    success = len(
        df[
            df["Mission_Status"]
            == "Success"
        ]
    )

    total = len(df)

    if total == 0:
        return 0

    return round(
        success / total * 100,
        2
    )


# ==================================================
# TOP PERFORMERS
# ==================================================

def top_vehicle(df):

    return (
        df["Launch_Vehicle"]
        .value_counts()
        .idxmax()
    )


def top_orbit(df):

    return (
        df["Orbit_Type"]
        .value_counts()
        .idxmax()
    )


def top_application(df):

    return (
        df["Application"]
        .value_counts()
        .idxmax()
    )


def peak_year(df):

    return (
        df["Year"]
        .value_counts()
        .idxmax()
    )


# ==================================================
# YEARLY ANALYSIS
# ==================================================

def yearly_launches(df):

    return (
        df.groupby("Year")
        .size()
        .reset_index(
            name="Launch_Count"
        )
        .sort_values("Year")
    )


def cumulative_launches(df):

    yearly = yearly_launches(df)

    yearly["Cumulative_Launches"] = (
        yearly["Launch_Count"]
        .cumsum()
    )

    return yearly


def yearly_growth(df):

    yearly = yearly_launches(df)

    yearly["Growth_%"] = (
        yearly["Launch_Count"]
        .pct_change()
        * 100
    )

    return yearly


# ==================================================
# MONTHLY ANALYSIS
# ==================================================

def monthly_launches(df):

    return (
        df.groupby(
            [
                "Month",
                "Month_Name"
            ]
        )
        .size()
        .reset_index(
            name="Launch_Count"
        )
        .sort_values("Month")
    )


def busiest_month(df):

    monthly = monthly_launches(df)

    return monthly.loc[
        monthly["Launch_Count"].idxmax()
    ]


# ==================================================
# VEHICLE ANALYTICS
# ==================================================

def vehicle_distribution(df):

    return (
        df["Launch_Vehicle"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": "Vehicle",
                "Launch_Vehicle": "Launches"
            }
        )
    )


def vehicle_summary(df):

    return (
        df.groupby("Launch_Vehicle")
        .agg(
            Launches=(
                "Launch_Vehicle",
                "count"
            ),
            Orbit_Diversity=(
                "Orbit_Type",
                "nunique"
            ),
            Mission_Diversity=(
                "Application",
                "nunique"
            ),
            First_Year=(
                "Year",
                "min"
            ),
            Last_Year=(
                "Year",
                "max"
            )
        )
        .reset_index()
    )


def vehicle_lifecycle(df):

    vehicle = vehicle_summary(df)

    vehicle["Operational_Span"] = (
        vehicle["Last_Year"]
        - vehicle["First_Year"]
        + 1
    )

    return vehicle


# ==================================================
# ORBIT ANALYTICS
# ==================================================

def orbit_distribution(df):

    return (
        df["Orbit_Type"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": "Orbit",
                "Orbit_Type": "Launches"
            }
        )
    )


def orbit_summary(df):

    return (
        df.groupby("Orbit_Type")
        .agg(
            Launches=(
                "Orbit_Type",
                "count"
            ),
            Vehicles=(
                "Launch_Vehicle",
                "nunique"
            ),
            Applications=(
                "Application",
                "nunique"
            )
        )
        .reset_index()
    )


# ==================================================
# APPLICATION ANALYTICS
# ==================================================

def application_distribution(df):

    return (
        df["Application"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index":
                    "Application",
                "Application":
                    "Launches"
            }
        )
    )


# ==================================================
# DIVERSITY METRICS
# ==================================================

def orbit_diversity_score(df):

    return (
        df.groupby("Launch_Vehicle")
        ["Orbit_Type"]
        .nunique()
        .reset_index(
            name="Orbit_Diversity"
        )
    )


def mission_diversity_score(df):

    return (
        df.groupby("Launch_Vehicle")
        ["Application"]
        .nunique()
        .reset_index(
            name="Mission_Diversity"
        )
    )


# ==================================================
# HEATMAP DATA
# ==================================================

def vehicle_heatmap(df):

    heat = (
        df.groupby(
            [
                "Launch_Vehicle",
                "Year"
            ]
        )
        .size()
        .reset_index(
            name="Launches"
        )
    )

    return heat.pivot(
        index="Launch_Vehicle",
        columns="Year",
        values="Launches"
    ).fillna(0)


def orbit_heatmap(df):

    heat = (
        df.groupby(
            [
                "Orbit_Type",
                "Year"
            ]
        )
        .size()
        .reset_index(
            name="Launches"
        )
    )

    return heat.pivot(
        index="Orbit_Type",
        columns="Year",
        values="Launches"
    ).fillna(0)


# ==================================================
# ANOMALY DETECTION
# ==================================================

def detect_launch_anomalies(
    yearly_df,
    threshold=2.0
):

    data = yearly_df.copy()

    mean = (
        data["Launch_Count"]
        .mean()
    )

    std = (
        data["Launch_Count"]
        .std()
    )

    data["z_score"] = (
        data["Launch_Count"]
        - mean
    ) / std

    data["Anomaly"] = (
        np.abs(
            data["z_score"]
        ) > threshold
    )

    return data


# ==================================================
# FORECAST PREPARATION
# ==================================================

def prophet_dataset(df):

    yearly = (
        df.groupby("Year")
        .size()
        .reset_index(
            name="y"
        )
    )

    yearly["ds"] = pd.to_datetime(
        yearly["Year"]
        .astype(str)
    )

    return yearly[
        ["ds", "y"]
    ]


# ==================================================
# EXECUTIVE INSIGHTS
# ==================================================

def executive_insights(df):

    insights = {}

    insights["Total Launches"] = (
        total_launches(df)
    )

    insights["Top Vehicle"] = (
        top_vehicle(df)
    )

    insights["Top Orbit"] = (
        top_orbit(df)
    )

    insights["Top Application"] = (
        top_application(df)
    )

    insights["Peak Year"] = (
        peak_year(df)
    )

    if "Mission_Status" in df.columns:

        insights["Success Rate"] = (
            success_rate(df)
        )

    return insights


# ==================================================
# BENCHMARK SCORE
# ==================================================

def vehicle_benchmark(df):

    result = (
        df.groupby("Launch_Vehicle")
        .agg(
            Launches=(
                "Launch_Vehicle",
                "count"
            ),
            Orbit_Diversity=(
                "Orbit_Type",
                "nunique"
            ),
            Mission_Diversity=(
                "Application",
                "nunique"
            )
        )
        .reset_index()
    )

    result["Score"] = (
        result["Launches"] * 0.5
        +
        result["Orbit_Diversity"] * 0.25
        +
        result["Mission_Diversity"] * 0.25
    )

    return result.sort_values(
        "Score",
        ascending=False
    )


# ==================================================
# SEARCH UTILITY
# ==================================================

def search_missions(
    df,
    keyword
):

    return df[
        df.astype(str)
        .apply(
            lambda x:
            x.str.contains(
                keyword,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]


# ==================================================
# DATA QUALITY REPORT
# ==================================================

def data_quality_report(df):

    report = pd.DataFrame({

        "Column":
            df.columns,

        "Missing Values":
            df.isna().sum().values,

        "Data Type":
            df.dtypes.values,

        "Unique Values":
            [
                df[col].nunique()
                for col in df.columns
            ]
    })

    return report
```
