import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === Load Dataset ===
df = pd.read_csv("acs_full_with_shootings.csv")  # Adjust path if needed

# === BASIC DATA EXPLORATION ===
print("\n🔍 Basic Info:")
print(df.info())

print("\n🧮 Summary Statistics:")
print(df.describe(include='all'))

print("\n❗ Null Values per Column:")
print(df.isnull().sum().sort_values(ascending=False))

# === CORRELATION MATRIX ===
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

# === SAVE CORRELATION MATRIX ===
correlation_matrix.to_csv("data/eda_correlation_matrix.csv")

# === CORRELATION HEATMAP ===
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap of Numeric Variables")
plt.tight_layout()
plt.savefig("plots/eda_correlation_heatmap.png")
plt.show()

# === DISTRIBUTION: POLICE KILLINGS PER 100K ===
plt.figure(figsize=(10, 5))
sns.histplot(df["killings_per_100k"].dropna(), kde=True, bins=20)
plt.title("Distribution of Police Killings per 100k Population")
plt.xlabel("Killings per 100k")
plt.ylabel("Number of States")
plt.tight_layout()
plt.savefig("plots/eda_killings_per_100k_distribution.png")
plt.show()

# === TOP 10 STATES BY TOTAL POLICE KILLINGS ===
top_10_killings = df[["State", "total_police_killings"]] \
                    .sort_values(by="total_police_killings", ascending=False) \
                    .head(10)

print("\n🔫 Top 10 States by Total Police Killings:")
print(top_10_killings)

# === SAVE KEY OUTPUTS ===
top_10_killings.to_csv("data/eda_top10_states_by_killings.csv", index=False)
df.describe().to_csv("data/eda_summary.csv")
df.isnull().sum().sort_values(ascending=False).to_csv("data/eda_nulls.csv")
