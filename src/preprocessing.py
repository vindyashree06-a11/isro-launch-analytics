```python
"""
=================================================
ISRO Mission Analytics
Data Preprocessing Module
=================================================
"""

import pandas as pd
import numpy as np


# =================================================
# COLUMN STANDARDIZATION
# =================================================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names
    """

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
    )

    return df


# =================================================
# REMOVE DUPLICATES
# =================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate records
    """

    return df.drop_duplicates()


# =================================================
# HANDLE MISSING VALUES
# =================================================

def handle_missing_values(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Basic missing value treatment
    """

    text_columns = [
        "Launch_Vehicle",
        "Orbit_Type",
        "Application",
        "Remarks"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = df[col].fillna(
                "Unknown"
            )

    return df


# =================================================
# DATE FEATURES
# =================================================

def create_date_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create time-based features
    """

    if "Launch_Date" not in df.columns:
        return df

    df["Year"] = (
        df["Launch_Date"]
        .dt.year
    )

    df["Month"] = (
        df["Launch_Date"]
        .dt.month
    )

    df["Month_Name"] = (
        df["Launch_Date"]
        .dt.month_name()
    )

    df["Quarter"] = (
        df["Launch_Date"]
        .dt.quarter
    )

    df["Day"] = (
        df["Launch_Date"]
        .dt.day
    )

    df["Weekday"] = (
        df["Launch_Date"]
        .dt.day_name()
    )

    return df


# =================================================
# MISSION STATUS EXTRACTION
# =================================================

def extract_mission_status(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Extract mission status from remarks
    """

    if "Remarks" not in df.columns:

        df["Mission_Status"] = "Unknown"

        return df

    df["Mission_Status"] = "Success"

    failure_keywords = [
        "failed",
        "failure",
        "unsuccessful",
        "destroyed",
        "loss",
        "partial failure"
    ]

    df["Mission_Status"] = np.where(

        df["Remarks"]
        .astype(str)
        .str.lower()
        .str.contains(
            "|".join(failure_keywords),
            na=False
        ),

        "Failed",

        "Success"
    )

    return df


# =================================================
# SUCCESS RATE
# =================================================

def calculate_success_rate(
    df: pd.DataFrame
) -> float:
    """
    Mission success rate
    """

    if "Mission_Status" not in df.columns:

        return 0

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


# =================================================
# YEARLY AGGREGATION
# =================================================

def create_yearly_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Launches per year
    """

    return (
        df.groupby("Year")
        .size()
        .reset_index(
            name="Launch_Count"
        )
        .sort_values("Year")
    )


# =================================================
# MONTHLY AGGREGATION
# =================================================

def create_monthly_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Launches by month
    """

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


# =================================================
# VEHICLE AGGREGATION
# =================================================

def vehicle_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Vehicle statistics
    """

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
            )
        )
        .reset_index()
    )


# =================================================
# ORBIT AGGREGATION
# =================================================

def orbit_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Orbit statistics
    """

    return (
        df.groupby("Orbit_Type")
        .agg(
            Launches=(
                "Orbit_Type",
                "count"
            ),
            Applications=(
                "Application",
                "nunique"
            ),
            Vehicles=(
                "Launch_Vehicle",
                "nunique"
            )
        )
        .reset_index()
    )


# =================================================
# APPLICATION AGGREGATION
# =================================================

def application_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Application statistics
    """

    return (
        df.groupby("Application")
        .agg(
            Launches=(
                "Application",
                "count"
            )
        )
        .reset_index()
    )


# =================================================
# CUMULATIVE LAUNCHES
# =================================================

def cumulative_launches(
    yearly_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Running total launches
    """

    yearly_df = yearly_df.copy()

    yearly_df["Cumulative_Launches"] = (
        yearly_df["Launch_Count"]
        .cumsum()
    )

    return yearly_df


# =================================================
# YEAR OVER YEAR GROWTH
# =================================================

def growth_rate(
    yearly_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate YoY growth
    """

    yearly_df = yearly_df.copy()

    yearly_df["Growth_%"] = (
        yearly_df["Launch_Count"]
        .pct_change()
        * 100
    )

    return yearly_df


# =================================================
# PROPHET DATA PREP
# =================================================

def prepare_prophet_data(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Prophet-ready dataset
    """

    yearly = (
        df.groupby("Year")
        .size()
        .reset_index(
            name="y"
        )
    )

    yearly["ds"] = pd.to_datetime(
        yearly["Year"].astype(str)
    )

    return yearly[
        ["ds", "y"]
    ]


# =================================================
# ANOMALY DETECTION
# =================================================

def detect_anomalies(
    yearly_df: pd.DataFrame,
    threshold: float = 2.0
):
    """
    Z-score anomaly detection
    """

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


# =================================================
# FULL PIPELINE
# =================================================

def preprocess_data(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline
    """

    df = standardize_columns(df)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    df = create_date_features(df)

    df = extract_mission_status(df)

    return df
```
