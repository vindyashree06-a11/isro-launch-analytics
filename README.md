# 🚀 ISRO Mission Analytics Dashboard

A modern, interactive analytics platform built using **Streamlit**, **Plotly**, and **Machine Learning** to analyze historical ISRO mission launches and generate actionable insights through advanced visualizations, KPI dashboards, and predictive analytics.

---

## 🌟 Project Overview

The ISRO Mission Analytics Dashboard provides a comprehensive analysis of India's space launch history using publicly available mission launch data.

The dashboard enables users to:

* Analyze launch trends over time
* Explore launch vehicle performance
* Understand orbit and mission application distributions
* Monitor mission success metrics
* Generate automated insights
* Forecast future launch activity using time-series models

This project demonstrates practical applications of:

* Data Analytics
* Business Intelligence
* Data Visualization
* Exploratory Data Analysis (EDA)
* Machine Learning Forecasting
* Interactive Dashboard Development

---

## 🎯 Objectives

The primary objectives of this project are:

* Transform raw mission launch data into meaningful insights
* Provide interactive exploration capabilities
* Visualize ISRO's growth and technological evolution
* Identify trends across launch vehicles and mission types
* Predict future launch activity

---

## 🛰 Dataset Information

The dataset contains historical ISRO launch records including:

| Column         | Description                |
| -------------- | -------------------------- |
| Launch Date    | Mission launch date        |
| Launch Vehicle | Vehicle used for launch    |
| Orbit Type     | Target orbit               |
| Application    | Mission application        |
| Remarks        | Mission details and status |

### Key Launch Vehicles

* PSLV
* GSLV
* GSLV Mk III / LVM3
* SSLV
* ASLV
* SLV

### Mission Applications

* Communication
* Navigation
* Earth Observation
* Scientific Missions
* Planetary Exploration
* Technology Demonstration

---

# 📂 Project Structure

```text
isro-launch-analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── ISRO mission launches.csv
│
├── assets/
│   ├── isro_logo.png
│   ├── style.css
│   └── banner.png
│
├── pages/
│   ├── 1_Executive_Dashboard.py
│   ├── 2_Mission_Analytics.py
│   ├── 3_Vehicle_Performance.py
│   ├── 4_Orbit_Insights.py
│   └── 5_Predictive_Analytics.py
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analytics.py
│   ├── charts.py
│   └── forecasting.py
│
├── screenshots/
│   ├── dashboard.png
│   ├── forecasting.png
│   └── vehicle_analysis.png
│
└── tests/
    └── test_data.py
```

---

# 📊 Dashboard Features

## 1. Executive Dashboard

High-level KPIs:

* Total Launches
* Mission Success Rate
* Launch Vehicles Used
* Orbit Categories
* Mission Applications

### KPI Cards

```text
🚀 Total Launches
🛰 Launch Vehicles
🌍 Orbit Types
📈 Success Rate
```

---

## 2. Mission Analytics

Interactive analysis of:

* Year-wise launches
* Monthly trends
* Growth rate
* Historical milestones

Visualizations:

* Line Charts
* Area Charts
* Time-Series Analysis

---

## 3. Launch Vehicle Performance

Compare launch vehicles based on:

* Number of launches
* Success ratio
* Usage trends
* Historical growth

Visualizations:

* Bar Charts
* Pie Charts
* Radar Charts

---

## 4. Orbit Analytics

Analyze missions across:

* LEO
* GEO
* GTO
* Polar Orbit
* Sun-Synchronous Orbit
* Lunar Orbit

Visualizations:

* Treemaps
* Donut Charts
* Heatmaps

---

## 5. Mission Applications

Explore mission objectives:

* Communication
* Navigation
* Earth Observation
* Scientific Research
* Technology Demonstration

Visualizations:

* Sunburst Charts
* Sankey Diagrams
* Hierarchical Trees

---

## 6. AI-Powered Insights

Automatically generated insights such as:

* Most used launch vehicle
* Peak launch year
* Highest growth period
* Orbit dominance
* Application trends

Example:

```text
✓ PSLV accounts for 58% of total launches

✓ Peak launch activity occurred in 2017

✓ Earth Observation missions dominate the dataset

✓ LEO remains the most frequently used orbit
```

---

## 7. Predictive Analytics

Forecast future launch activity using:

### Models

* ARIMA
* Prophet
* Exponential Smoothing

Predictions:

* Annual launch count
* Growth trajectory
* Vehicle demand forecast

Example Output:

```text
2026 → 8 launches

2027 → 10 launches

2028 → 12 launches
```

---

# 📈 Visualizations Included

## Trend Analysis

* Launches per year
* Rolling averages
* Growth trends

## Distribution Analysis

* Vehicle share
* Orbit distribution
* Mission applications

## Advanced Charts

* Sankey Diagram
* Sunburst Chart
* Treemap
* Heatmap
* Bubble Chart
* Geographic Maps

---

# 🛠 Technology Stack

## Frontend

* Streamlit

## Data Processing

* Pandas
* NumPy

## Visualization

* Plotly
* Matplotlib

## Machine Learning

* Scikit-Learn
* Prophet

## Deployment

* Streamlit Cloud
* GitHub

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/isro-launch-analytics.git

cd isro-launch-analytics
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📦 Requirements

```txt
streamlit
pandas
numpy
plotly
matplotlib
scikit-learn
prophet
streamlit-extras
streamlit-option-menu
```

---

# 🌐 Deployment

## GitHub

```bash
git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/yourusername/isro-launch-analytics.git

git push -u origin main
```

---

## Streamlit Cloud

1. Push project to GitHub
2. Login to Streamlit Cloud
3. Connect repository
4. Select branch
5. Deploy

Your application will be available at:

```text
https://your-app-name.streamlit.app
```

---

# 📸 Dashboard Preview

## Executive Dashboard

Displays:

* KPI Cards
* Launch Trend
* Mission Overview

---

## Vehicle Performance

Displays:

* Vehicle comparison
* Success metrics
* Trend evolution

---

## Predictive Analytics

Displays:

* Forecast charts
* Future launch predictions
* Confidence intervals

---

# 📚 Business Insights Generated

The dashboard can answer questions such as:

* Which launch vehicle is most frequently used?
* Which year had the highest launch activity?
* What orbit type dominates ISRO missions?
* Which applications are growing fastest?
* What launch activity is expected in the coming years?

---

# Future Enhancements

* Real-time ISRO launch tracking
* Satellite analytics module
* Global space agency comparison
* NLP-based mission report analysis
* GenAI-powered chatbot
* Satellite orbit visualization
* Launch cost estimation models

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork repository
2. Create feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Add new feature"
```

4. Push branch

```bash
git push origin feature-name
```

5. Open Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Your Name**

Data Analytics | Machine Learning | Business Intelligence | Streamlit Developer

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.

⭐ Star the repository

🚀 Share with fellow data enthusiasts

🛰 Explore the future of space analytics
