"""
=========================================================
ISRO Mission Analytics
Forecasting Engine
=========================================================

Supports:
- Prophet Forecasting
- Future Launch Prediction
- Confidence Intervals
- Trend Analysis
- Moving Average
- Anomaly Detection
- Forecast Metrics
=========================================================
"""

import pandas as pd
import numpy as np

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# =====================================================
# PREPARE PROPHET DATA
# =====================================================

def prepare_prophet_dataset(df):
    """
    Convert launch data into Prophet format

    Returns:
        ds | y
    """

    yearly = (
        df.groupby("Year")
        .size()
        .reset_index(name="y")
    )

    yearly["ds"] = pd.to_datetime(
        yearly["Year"].astype(str)
    )

    return yearly[["ds", "y"]]


# =====================================================
# TRAIN MODEL
# =====================================================

def train_prophet_model(
    prophet_df,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05
):
    """
    Train Prophet model
    """

    model = Prophet(
        yearly_seasonality=yearly_seasonality,
        changepoint_prior_scale=changepoint_prior_scale
    )

    model.fit(prophet_df)

    return model


# =====================================================
# GENERATE FORECAST
# =====================================================

def generate_forecast(
    model,
    years=5
):
    """
    Generate future forecast
    """

    future = model.make_future_dataframe(
        periods=years,
        freq="Y"
    )

    forecast = model.predict(future)

    return forecast


# =====================================================
# COMPLETE PIPELINE
# =====================================================

def forecast_launches(
    df,
    years=5
):
    """
    Full forecasting pipeline
    """

    prophet_df = prepare_prophet_dataset(df)

    model = train_prophet_model(
        prophet_df
    )

    forecast = generate_forecast(
        model,
        years
    )

    return {
        "model": model,
        "historical": prophet_df,
        "forecast": forecast
    }


# =====================================================
# FORECAST SUMMARY
# =====================================================

def forecast_summary(
    forecast,
    future_years=5
):
    """
    Executive forecast summary
    """

    future = forecast.tail(
        future_years
    )

    summary = {

        "average_prediction":
            round(
                future["yhat"].mean(),
                2
            ),

        "maximum_prediction":
            round(
                future["yhat"].max(),
                2
            ),

        "minimum_prediction":
            round(
                future["yhat"].min(),
                2
            ),

        "upper_bound":
            round(
                future["yhat_upper"].max(),
                2
            ),

        "lower_bound":
            round(
                future["yhat_lower"].min(),
                2
            )
    }

    return summary


# =====================================================
# MOVING AVERAGE
# =====================================================

def moving_average(
    yearly_df,
    window=3
):
    """
    Calculate moving average
    """

    data = yearly_df.copy()

    data["Moving_Average"] = (
        data["Launch_Count"]
        .rolling(window)
        .mean()
    )

    return data


# =====================================================
# TREND ANALYSIS
# =====================================================

def launch_trend_analysis(df):
    """
    Historical launch trend
    """

    yearly = (
        df.groupby("Year")
        .size()
        .reset_index(name="Launch_Count")
    )

    yearly["Growth_%"] = (
        yearly["Launch_Count"]
        .pct_change()
        * 100
    )

    yearly["Cumulative"] = (
        yearly["Launch_Count"]
        .cumsum()
    )

    return yearly


# =====================================================
# CONFIDENCE INTERVAL TABLE
# =====================================================

def confidence_interval_table(
    forecast
):
    """
    Forecast intervals
    """

    return forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ].rename(
        columns={
            "ds": "Date",
            "yhat": "Prediction",
            "yhat_lower": "Lower_Bound",
            "yhat_upper": "Upper_Bound"
        }
    )


# =====================================================
# ANOMALY DETECTION
# =====================================================

def detect_anomalies(
    yearly_df,
    threshold=2.0
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

    data["Z_Score"] = (
        data["Launch_Count"]
        - mean
    ) / std

    data["Anomaly"] = (
        np.abs(
            data["Z_Score"]
        ) > threshold
    )

    return data


# =====================================================
# FORECAST GROWTH RATE
# =====================================================

def forecast_growth_rate(
    historical,
    forecast,
    years=5
):
    """
    Growth from latest actual
    """

    latest_actual = (
        historical["y"]
        .iloc[-1]
    )

    future_value = (
        forecast["yhat"]
        .tail(years)
        .iloc[-1]
    )

    growth = (
        (
            future_value
            - latest_actual
        )
        / latest_actual
    ) * 100

    return round(
        growth,
        2
    )


# =====================================================
# MODEL EVALUATION
# =====================================================

def evaluate_forecast(
    actual,
    predicted
):
    """
    Evaluate prediction quality
    """

    mae = mean_absolute_error(
        actual,
        predicted
    )

    mse = mean_squared_error(
        actual,
        predicted
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        actual,
        predicted
    )

    return {
        "MAE": round(mae, 3),
        "MSE": round(mse, 3),
        "RMSE": round(rmse, 3),
        "R2": round(r2, 3)
    }


# =====================================================
# BACKTEST MODEL
# =====================================================

def backtest_prophet(
    prophet_df,
    test_size=5
):
    """
    Historical validation
    """

    train = prophet_df[:-test_size]

    test = prophet_df[-test_size:]

    model = Prophet()

    model.fit(train)

    future = model.make_future_dataframe(
        periods=test_size,
        freq="Y"
    )

    forecast = model.predict(
        future
    )

    predictions = (
        forecast["yhat"]
        .tail(test_size)
        .values
    )

    metrics = evaluate_forecast(
        test["y"].values,
        predictions
    )

    return {
        "metrics": metrics,
        "actual": test,
        "predicted": predictions
    }


# =====================================================
# FORECAST EXPORT
# =====================================================

def export_forecast_csv(
    forecast
):
    """
    Convert forecast to CSV
    """

    return forecast.to_csv(
        index=False
    ).encode("utf-8")


# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

def executive_forecast_insights(
    historical,
    forecast,
    years=5
):
    """
    Generate business insights
    """

    growth = forecast_growth_rate(
        historical,
        forecast,
        years
    )

    avg_future = round(
        forecast["yhat"]
        .tail(years)
        .mean(),
        2
    )

    peak_future = round(
        forecast["yhat"]
        .tail(years)
        .max(),
        2
    )

    return {
        "Forecast Growth %":
            growth,

        "Average Future Launches":
            avg_future,

        "Peak Forecast Launches":
            peak_future,

        "Forecast Horizon":
            years
    }


# =====================================================
# VEHICLE FORECAST
# =====================================================

def vehicle_forecast_dataset(
    df,
    vehicle_name
):
    """
    Forecast launches
    for specific vehicle
    """

    vehicle_df = df[
        df["Launch_Vehicle"]
        == vehicle_name
    ]

    yearly = (
        vehicle_df.groupby("Year")
        .size()
        .reset_index(name="y")
    )

    yearly["ds"] = pd.to_datetime(
        yearly["Year"].astype(str)
    )

    return yearly[
        ["ds", "y"]
    ]


# =====================================================
# ORBIT FORECAST
# =====================================================

def orbit_forecast_dataset(
    df,
    orbit_name
):
    """
    Forecast launches
    for specific orbit
    """

    orbit_df = df[
        df["Orbit_Type"]
        == orbit_name
    ]

    yearly = (
        orbit_df.groupby("Year")
        .size()
        .reset_index(name="y")
    )

    yearly["ds"] = pd.to_datetime(
        yearly["Year"].astype(str)
    )

    return yearly[
        ["ds", "y"]
    ]
