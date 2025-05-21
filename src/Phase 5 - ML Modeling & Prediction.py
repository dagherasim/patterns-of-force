import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Load Dataset ===
df = pd.read_csv("acs_full_with_shootings.csv")

# === Filter only rows with valid target
df = df[df["killings_per_100k"].notna()].copy()

# ✅ Extract State column BEFORE cleaning
if "State" in df.columns:
    state_values = df["State"].fillna("N/A").values
else:
    state_values = ["N/A"] * len(df)

# === Clean commas and convert all numeric-looking columns ===
df_cleaned = df.copy()
for col in df_cleaned.columns:
    if df_cleaned[col].dtype == 'object':
        df_cleaned[col] = df_cleaned[col].astype(str).str.replace(",", "").str.strip()
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")

# === Identify usable numeric features ===
numeric_cols = df_cleaned.select_dtypes(include='number').columns.tolist()
excluded = ["killings_per_100k", "total_police_killings", "Population"]
feature_cols = [col for col in numeric_cols if col not in excluded]

# === Safety Check ===
print("📋 Numeric columns found:", numeric_cols)
print("✅ Features used:", feature_cols)
assert len(feature_cols) > 0, "No usable numeric features found."

# === Feature matrix and target ===
X = df_cleaned[feature_cols].fillna(0)
y = df_cleaned["killings_per_100k"].fillna(0)

# === Train/Test Split INCLUDING state
X_train, X_test, y_train, y_test, state_train, state_test = train_test_split(
    X, y, state_values, test_size=0.2, random_state=42
)

# === Linear Regression ===
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# === Random Forest Regression ===
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# === Metrics ===
print("📏 Linear Regression:")
print("  R² Score:", r2_score(y_test, y_pred_lr))
print("  RMSE:", mean_squared_error(y_test, y_pred_lr, squared=False))

print("\n🌲 Random Forest:")
print("  R² Score:", r2_score(y_test, y_pred_rf))
print("  RMSE:", mean_squared_error(y_test, y_pred_rf, squared=False))

# === Feature Importance Plot ===
importances = rf.feature_importances_
feat_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
feat_df = feat_df.sort_values(by="Importance", ascending=False)

# === Save Plots Directory ===
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# === Stylized Feature Importance Plot (Top 30) ===
plt.figure(figsize=(10, 14))
sns.barplot(
    data=feat_df.head(30),
    x="Importance", y="Feature",
    palette="viridis"
)
plt.title("Top 30 Feature Importances (Random Forest)", fontsize=16, weight='bold')
plt.xlabel("Importance", fontsize=12)
plt.ylabel("Feature", fontsize=12)
plt.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f"{output_dir}/ml_feature_importance_top30.png")
plt.show()

# === Save Predictions CSV ===
os.makedirs("data", exist_ok=True)

pred_df = pd.DataFrame({
    "State": state_test,
    "Actual": y_test,
    "Predicted": y_pred_rf
})
pred_df.to_csv("data/ml_rf_predictions.csv", index=False)

# === Plot Actual vs Predicted ===
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred_rf)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual Killings per 100k")
plt.ylabel("Predicted Killings per 100k")
plt.title("Actual vs Predicted Killings per 100k (Random Forest)")
plt.tight_layout()
plt.savefig(f"{output_dir}/ml_predicted_vs_actual.png")
plt.show()
