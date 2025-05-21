import pandas as pd
import plotly.express as px
import os

# === Load Data ===
df = pd.read_csv("acs_full_with_shootings.csv")

# === Identify Columns ===
income_col = [col for col in df.columns if "Median household income" in col][0]
poverty_col = [col for col in df.columns if "Pov_Total:" in col][0]
race_black_col = [col for col in df.columns if "Race_Black or African American alone" in col][0]
race_white_col = [col for col in df.columns if "Race_White alone" in col][0]

# === Clean numeric columns (remove commas and convert) ===
def clean_numeric_column(df, col):
    return pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")

df[poverty_col] = clean_numeric_column(df, poverty_col)
df[income_col] = clean_numeric_column(df, income_col)
df[race_black_col] = clean_numeric_column(df, race_black_col)
df[race_white_col] = clean_numeric_column(df, race_white_col)

# === Output Directory ===
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# === 1. Interactive Scatter: Income vs Killings ===
fig1 = px.scatter(df, 
    x=income_col, 
    y="killings_per_100k",
    hover_name="State",
    color="State",
    size=poverty_col,
    title="Interactive: Income vs Killings per 100k (Size = Poverty)",
    labels={"killings_per_100k": "Killings per 100k"}
)
fig1.write_html(f"{output_dir}/interactive_income_vs_killings.html")
fig1.show()

# === 2. Interactive Scatter: % Black Pop vs Killings ===
fig2 = px.scatter(df,
    x=race_black_col,
    y="killings_per_100k",
    hover_name="State",
    color="State",
    size=poverty_col,
    title="Black Population vs Killings per 100k (Size = Poverty)",
    labels={"killings_per_100k": "Killings per 100k"}
)
fig2.write_html(f"{output_dir}/interactive_black_vs_killings.html")
fig2.show()

# === 3. Interactive Bar Chart: Killings per 100k by State ===
fig3 = px.bar(df.sort_values("killings_per_100k", ascending=False),
    x="State",
    y="killings_per_100k",
    color="killings_per_100k",
    title="Killings per 100k - Interactive Bar Chart",
    labels={"killings_per_100k": "Killings per 100k"}
)
fig3.write_html(f"{output_dir}/interactive_bar_killings_per_100k.html")
fig3.show()
