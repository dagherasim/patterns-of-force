import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Load Data ===
df = pd.read_csv("acs_full_with_shootings.csv")

# === Set Plot Style and Directory ===
sns.set(style="whitegrid")
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# === Identify Columns Dynamically ===
income_col = [col for col in df.columns if "Median household income" in col][0]
poverty_col = [col for col in df.columns if "Pov_Total:" in col][0]

# === 1. Top 10 States by Killings Per 100k ===
top10_per_100k = df[["State", "killings_per_100k"]].sort_values(by="killings_per_100k", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top10_per_100k, x="killings_per_100k", y="State", palette="Reds_r")
plt.title("Top 10 States by Police Killings per 100k")
plt.xlabel("Killings per 100k")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(f"{output_dir}/top10_killings_per_100k.png")
plt.show()

# === 2. Poverty Rate vs Killings (Scatter) ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x=poverty_col, y="killings_per_100k", hue="State", palette="viridis", legend=False)
plt.title("Poverty vs Killings per 100k")
plt.xlabel("Total in Poverty")
plt.ylabel("Killings per 100k")
plt.tight_layout()
plt.savefig(f"{output_dir}/poverty_vs_killings.png")
plt.show()

# === 3. Median Income vs Killings (Scatter) ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x=income_col, y="killings_per_100k", hue="State", palette="coolwarm", legend=False)
plt.title("Median Income vs Killings per 100k")
plt.xlabel("Median Income (Inflation Adjusted)")
plt.ylabel("Killings per 100k")
plt.tight_layout()
plt.savefig(f"{output_dir}/income_vs_killings.png")
plt.show()

# === Identify Race Columns (auto-detect) ===
race_white_col = [col for col in df.columns if "Race_White alone" in col][0]
race_black_col = [col for col in df.columns if "Race_Black or African American alone" in col][0]

# === 4. Race (% White) vs Killings ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x=race_white_col, y="killings_per_100k", hue="State", palette="Blues", legend=False)
plt.title("White Population vs Killings per 100k")
plt.xlabel("White Population (Raw Count)")
plt.ylabel("Killings per 100k")
plt.tight_layout()
plt.savefig(f"{output_dir}/white_vs_killings.png")
plt.show()

# === 5. Race (% Black) vs Killings ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x=race_black_col, y="killings_per_100k", hue="State", palette="Purples", legend=False)
plt.title("Black Population vs Killings per 100k")
plt.xlabel("Black Population (Raw Count)")
plt.ylabel("Killings per 100k")
plt.tight_layout()
plt.savefig(f"{output_dir}/black_vs_killings.png")
plt.show()
