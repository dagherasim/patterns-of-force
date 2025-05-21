import streamlit as st
import streamlit.components.v1 as components  # Needed to embed HTML map
import pandas as pd

# === Page Config ===
st.set_page_config(page_title="US Police Killings ML Dashboard", layout="wide")
st.title("🚔 US Police Killings — Machine Learning Dashboard")

# === Load Predictions ===
st.subheader("📋 Model Predictions vs Actual (Random Forest)")
try:
    pred_df = pd.read_csv("data/ml_rf_predictions.csv")
    st.dataframe(pred_df)
except FileNotFoundError:
    st.error("⚠️ File not found: data/ml_rf_predictions.csv")

# === ML Metrics Summary ===
st.subheader("📏 Model Performance Summary")
st.markdown("""
- **Model:** Random Forest Regressor  
- **Target:** Killings per 100k  
""")

# Optionally display actual values if you want to hardcode them in:
st.markdown("""
**Example Metrics:**  
- **R² Score:** ~0.71  
- **RMSE:** ~0.39  
""")

# === Top Feature Importances ===
st.subheader("🔥 Top Feature Importances")
try:
    st.image("plots/ml_feature_importance_top30.png", caption="Top 30 Most Influential Features", use_column_width=True)
except FileNotFoundError:
    st.warning("⚠️ Feature importance image not found.")

# === Actual vs Predicted Scatterplot ===
st.subheader("🎯 Actual vs Predicted Killings per 100k")
try:
    st.image("plots/ml_predicted_vs_actual.png", use_column_width=True)
except FileNotFoundError:
    st.warning("⚠️ Prediction scatterplot image not found.")

# === Correlation Heatmap ===
st.subheader("🌡️ Correlation Heatmap")
try:
    st.image("plots/eda_correlation_heatmap.png", caption="Correlation Between All Variables", use_column_width=True)
except FileNotFoundError:
    st.warning("⚠️ Correlation heatmap image not found.")

# === Choropleth Map ===
st.subheader("🗺️ Choropleth Map – Killings per 100k by State")
try:
    with open("plots/choropleth_killings_per_100k.html", 'r', encoding='utf-8') as f:
        choropleth_html = f.read()
    components.html(choropleth_html, height=600)
except FileNotFoundError:
    st.error("⚠️ Choropleth map not found. Make sure 'plots/choropleth_killings_per_100k.html' exists.")

# === Footer ===
st.markdown("---")
st.markdown("Built by Gherasim Denis Andrei")
