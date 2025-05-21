# 🔬 Data Science Case Study — Analyzing Police Killings in America Using ACS + ML + GeoVisuals

This is my **most extensive project in data analysis and data science so far**, built as a complete, multi-phase case study.

The project explores police killings across U.S. states using demographic and socioeconomic data from the **American Community Survey (ACS)** combined with national police fatality records.

It spans the full data science pipeline — from exploration and visualization to machine learning modeling, geospatial mapping, and Streamlit dashboard deployment — all organized into clear, progressive phases.

---

## 📁 Project Phases

### 🧩 Phase 1 — EDA & Correlation
Basic data exploration:
- Summary stats
- Null values
- Correlation matrix & heatmap
- Distribution of police killings per 100k
- Top 10 states by total police killings

📄 File: `Phase 1 - EDA & Correlation.py`

---

### 📊 Phase 2 — Static Visuals & Trends
Seaborn-based plots:
- Income, poverty vs killings
- Racial demographic correlations

📄 File: `Phase 2 - Static Visuals & Trends.py`

---

### 🧭 Phase 3 — Interactive Visualizations
Plotly-based interactive graphs:
- Income vs killings (size = poverty)
- Black population vs killings
- Interactive bar chart by state

📄 File: `Phase 3 - Interactive Visuals.py`

---

### 🗺️ Phase 4 — Choropleth Map
Interactive map of killings per 100k by U.S. state using Plotly & GeoJSON.

📄 File: `Phase 4 - Choropleth Map Generation.py`

---

### 🧠 Phase 5 — ML Modeling & Prediction
- Cleans numeric data
- Builds Random Forest & Linear Regression models
- Predicts killings per 100k based on state features
- Exports feature importances and prediction results

📄 File: `Phase 5 - ML Modeling & Prediction.py`

---

### 🚀 Phase 6 — Streamlit Dashboard
Final interactive app:
- View predictions vs actual
- Feature importances
- Correlation heatmap
- Embedded choropleth map

📄 File: `Phase 6 - Streamlit Dashboard.py`

Run with:

```bash
streamlit run "Phase 6 - Streamlit Dashboard.py"
