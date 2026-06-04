```python
"""
===========================================
ISRO Mission Analytics
Data Loader Module
===========================================
"""

import pandas as pd
import streamlit as st


# ===========================================
# CONFIG
# ===========================================

DEFAULT_DATA_PATH = (
    "data/ISRO mission launches.csv"
)


# ===========================================
# LOAD DATASET
# ===========================================

@st.cache_data
def load_data(
    file_path: str = DEFAULT_DATA_PATH
) -> pd.DataFrame:
    """
    Load ISRO mission dataset

    Parameters
    ----------
    file_path : str

    Returns
    -------
    pd.DataFrame
    """

    df = pd.read_csv(file_path)

    df = clean_columns(df)

    df = parse_dates(df)

    df = create_features(df)

    return df


# ===========================================
# CLEAN COLUMN NAMES
# ===========================================

def clean_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Standardize column names
    """

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


# ===========================================
# DATE PARSING
# ===========================================

def parse_dates(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert launch date
    """

    possible_date_cols = [
        "Launch_Date",
        "LaunchDate",
        "Date"
    ]

    for col in possible_date_cols:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            break

    return df


# ===========================================
# FEATURE ENGINEERING
# ===========================================

def create_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create additional features
    """

    if "Launch_Date" in df.columns:

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

    return df


# ===========================================
# DATA SUMMARY
# ===========================================

def get_dataset_summary(
    df: pd.DataFrame
) -> dict:
    """
    Generate dataset summary
    """

    summary = {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "vehicles":
            df["Launch_Vehicle"].nunique()
            if "Launch_Vehicle" in df.columns
            else 0,

        "orbits":
            df["Orbit_Type"].nunique()
            if "Orbit_Type" in df.columns
            else 0,

        "applications":
            df["Application"].nunique()
            if "Application" in df.columns
            else 0
    }

    return summary


# ===========================================
# FILTER DATA
# ===========================================

def filter_data(
    df: pd.DataFrame,
    vehicle=None,
    orbit=None,
    application=None,
    year_range=None
):
    """
    Dynamic filtering
    """

    filtered = df.copy()

    if vehicle and vehicle != "All":

        filtered = filtered[
            filtered["Launch_Vehicle"]
            == vehicle
        ]

    if orbit and orbit != "All":

        filtered = filtered[
            filtered["Orbit_Type"]
            == orbit
        ]

    if application and application != "All":

        filtered = filtered[
            filtered["Application"]
            == application
        ]

    if year_range:

        filtered = filtered[
            (
                filtered["Year"]
                >= year_range[0]
            )
            &
            (
                filtered["Year"]
                <= year_range[1]
            )
        ]

    return filtered


# ===========================================
# YEARLY LAUNCHES
# ===========================================

def yearly_launches(
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
    )


# ===========================================
# VEHICLE STATS
# ===========================================

def vehicle_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Vehicle launch counts
    """

    return (
        df["Launch_Vehicle"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index":
                    "Vehicle",
                "Launch_Vehicle":
                    "Launch_Count"
            }
        )
    )


# ===========================================
# ORBIT STATS
# ===========================================

def orbit_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Orbit distribution
    """

    return (
        df["Orbit_Type"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index":
                    "Orbit",
                "Orbit_Type":
                    "Launch_Count"
            }
        )
    )


# ===========================================
# APPLICATION STATS
# ===========================================

def application_statistics(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Application distribution
    """

    return (
        df["Application"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index":
                    "Application_Name",
                "Application":
                    "Launch_Count"
            }
        )
    )


# ===========================================
# TOP VEHICLE
# ===========================================

def get_top_vehicle(
    df: pd.DataFrame
):
    """
    Most used vehicle
    """

    return (
        df["Launch_Vehicle"]
        .value_counts()
        .idxmax()
    )


# ===========================================
# TOP ORBIT
# ===========================================

def get_top_orbit(
    df: pd.DataFrame
):
    """
    Most used orbit
    """

    return (
        df["Orbit_Type"]
        .value_counts()
        .idxmax()
    )


# ===========================================
# TOP APPLICATION
# ===========================================

def get_top_application(
    df: pd.DataFrame
):
    """
    Most common application
    """

    return (
        df["Application"]
        .value_counts()
        .idxmax()
    )


# ===========================================
# EXPORT CSV
# ===========================================

def export_csv(
    df: pd.DataFrame
):
    """
    Convert dataframe to CSV
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ===========================================
# HEALTH CHECK
# ===========================================

def validate_dataset(
    df: pd.DataFrame
):
    """
    Validate required columns
    """

    required_columns = [

        "Launch_Date",

        "Launch_Vehicle",

        "Orbit_Type",

        "Application"
    ]

    missing = [

        col
        for col in required_columns
        if col not in df.columns
    ]

    return {

        "valid":
            len(missing) == 0,

        "missing":
            missing
    }
```
