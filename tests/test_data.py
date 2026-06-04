"""
=========================================================
ISRO Mission Analytics
Unit Tests
=========================================================

Run:

pytest tests/test_data.py -v

=========================================================
"""

import pandas as pd
import pytest

from src.data_loader import (
    load_data,
    get_dataset_summary,
    filter_data
)

from src.preprocessing import (
    preprocess_data,
    calculate_success_rate,
    create_yearly_summary,
    prepare_prophet_data
)

from src.analytics import (
    total_launches,
    total_vehicles,
    total_orbits,
    yearly_launches,
    executive_insights
)

from src.forecasting import (
    prepare_prophet_dataset
)


# =====================================================
# SAMPLE DATA
# =====================================================

@pytest.fixture
def sample_df():

    data = {
        "Launch_Date": [
            "2020-01-01",
            "2021-03-15",
            "2022-07-20",
            "2023-09-10"
        ],
        "Launch_Vehicle": [
            "PSLV",
            "GSLV",
            "PSLV",
            "LVM3"
        ],
        "Orbit_Type": [
            "LEO",
            "GTO",
            "LEO",
            "GEO"
        ],
        "Application": [
            "Communication",
            "Navigation",
            "Earth Observation",
            "Scientific"
        ],
        "Remarks": [
            "Successful Mission",
            "Successful Mission",
            "Mission failed",
            "Successful Mission"
        ]
    }

    df = pd.DataFrame(data)

    df["Launch_Date"] = pd.to_datetime(
        df["Launch_Date"]
    )

    return df


# =====================================================
# DATA LOADER TESTS
# =====================================================

def test_dataframe_exists(sample_df):

    assert isinstance(
        sample_df,
        pd.DataFrame
    )


def test_required_columns(sample_df):

    required = [
        "Launch_Date",
        "Launch_Vehicle",
        "Orbit_Type",
        "Application",
        "Remarks"
    ]

    for col in required:

        assert col in sample_df.columns


# =====================================================
# PREPROCESSING TESTS
# =====================================================

def test_preprocessing_pipeline(sample_df):

    df = preprocess_data(
        sample_df
    )

    assert "Year" in df.columns

    assert "Month" in df.columns

    assert "Quarter" in df.columns

    assert "Mission_Status" in df.columns


def test_success_rate(sample_df):

    df = preprocess_data(
        sample_df
    )

    rate = calculate_success_rate(
        df
    )

    assert isinstance(
        rate,
        float
    )

    assert 0 <= rate <= 100


def test_yearly_summary(sample_df):

    df = preprocess_data(
        sample_df
    )

    yearly = create_yearly_summary(
        df
    )

    assert len(yearly) > 0

    assert "Launch_Count" in yearly.columns


# =====================================================
# ANALYTICS TESTS
# =====================================================

def test_total_launches(sample_df):

    df = preprocess_data(
        sample_df
    )

    result = total_launches(
        df
    )

    assert result == 4


def test_total_vehicles(sample_df):

    df = preprocess_data(
        sample_df
    )

    result = total_vehicles(
        df
    )

    assert result == 3


def test_total_orbits(sample_df):

    df = preprocess_data(
        sample_df
    )

    result = total_orbits(
        df
    )

    assert result == 3


def test_yearly_launches(sample_df):

    df = preprocess_data(
        sample_df
    )

    result = yearly_launches(
        df
    )

    assert len(result) > 0

    assert "Launch_Count" in result.columns


def test_executive_insights(sample_df):

    df = preprocess_data(
        sample_df
    )

    insights = executive_insights(
        df
    )

    assert isinstance(
        insights,
        dict
    )

    assert "Total Launches" in insights


# =====================================================
# FILTER TESTS
# =====================================================

def test_filter_vehicle(sample_df):

    df = preprocess_data(
        sample_df
    )

    filtered = filter_data(
        df,
        vehicle="PSLV"
    )

    assert len(filtered) == 2


def test_filter_orbit(sample_df):

    df = preprocess_data(
        sample_df
    )

    filtered = filter_data(
        df,
        orbit="LEO"
    )

    assert len(filtered) == 2


# =====================================================
# SUMMARY TESTS
# =====================================================

def test_dataset_summary(sample_df):

    df = preprocess_data(
        sample_df
    )

    summary = get_dataset_summary(
        df
    )

    assert isinstance(
        summary,
        dict
    )

    assert "rows" in summary


# =====================================================
# FORECASTING TESTS
# =====================================================

def test_prophet_preparation(sample_df):

    df = preprocess_data(
        sample_df
    )

    prophet_df = prepare_prophet_data(
        df
    )

    assert "ds" in prophet_df.columns

    assert "y" in prophet_df.columns


def test_forecasting_dataset(sample_df):

    df = preprocess_data(
        df=sample_df
    )

    forecast_df = (
        prepare_prophet_dataset(df)
    )

    assert isinstance(
        forecast_df,
        pd.DataFrame
    )

    assert "ds" in forecast_df.columns

    assert "y" in forecast_df.columns


# =====================================================
# DATA QUALITY TESTS
# =====================================================

def test_no_null_launch_vehicle(sample_df):

    assert (
        sample_df["Launch_Vehicle"]
        .isna()
        .sum()
        == 0
    )


def test_no_null_orbit(sample_df):

    assert (
        sample_df["Orbit_Type"]
        .isna()
        .sum()
        == 0
    )


def test_unique_vehicle_count(sample_df):

    count = (
        sample_df["Launch_Vehicle"]
        .nunique()
    )

    assert count == 3


# =====================================================
# EDGE CASES
# =====================================================

def test_empty_dataframe():

    empty_df = pd.DataFrame(
        columns=[
            "Launch_Date",
            "Launch_Vehicle",
            "Orbit_Type",
            "Application",
            "Remarks"
        ]
    )

    assert len(empty_df) == 0


def test_single_record():

    df = pd.DataFrame({

        "Launch_Date": [
            pd.Timestamp(
                "2024-01-01"
            )
        ],

        "Launch_Vehicle": [
            "PSLV"
        ],

        "Orbit_Type": [
            "LEO"
        ],

        "Application": [
            "Scientific"
        ],

        "Remarks": [
            "Success"
        ]
    })

    processed = preprocess_data(
        df
    )

    assert len(processed) == 1


# =====================================================
# INTEGRATION TEST
# =====================================================

def test_full_pipeline(sample_df):

    df = preprocess_data(
        sample_df
    )

    insights = executive_insights(
        df
    )

    prophet_df = prepare_prophet_data(
        df
    )

    assert len(df) > 0

    assert len(insights) > 0

    assert len(prophet_df) > 0
