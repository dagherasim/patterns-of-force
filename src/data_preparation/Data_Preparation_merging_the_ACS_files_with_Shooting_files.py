import os
import pandas as pd

# Correct working directory for this script
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

print("[DEBUG] Using data directory:", DATA_DIR)
print("[DEBUG] Files available:", os.listdir(DATA_DIR))  # Leave this in for validation

# Load your files
education = pd.read_csv(os.path.join(DATA_DIR, "ACS_B15003_Education_By_State.csv"), low_memory=False)
race = pd.read_csv(os.path.join(DATA_DIR, "ACS_B02001_Race_By_State.csv"), low_memory=False)
employment = pd.read_csv(os.path.join(DATA_DIR, "ACS_B23025_Employment_By_State.csv"), low_memory=False)
income = pd.read_csv(os.path.join(DATA_DIR, "ACS_B19013_Income_By_State.csv"), low_memory=False)
poverty = pd.read_csv(os.path.join(DATA_DIR, "ACS_B17001_Poverty_By_State.csv"), low_memory=False)
shootings = pd.read_csv(os.path.join(DATA_DIR, "fatal-police-shootings-data.csv"), low_memory=False)

# === Reshape function ===
def reshape_acs(df, prefix):
    df_long = pd.melt(df, id_vars=[df.columns[0]], var_name="State_Measure", value_name="Value")
    df_long[['State', 'Measure']] = df_long['State_Measure'].str.split("!!", expand=True)
    df_long = df_long[df_long['Measure'] == "Estimate"]
    df_long = df_long.rename(columns={df.columns[0]: "Category"})
    df_pivot = df_long.pivot_table(index="State", columns="Category", values="Value", aggfunc="first")
    df_pivot.columns = [f"{prefix}_{col.strip()}" for col in df_pivot.columns]
    return df_pivot.reset_index()

# === Reshape and process each ACS file ===
education = reshape_acs(education, "Edu")
race = reshape_acs(race, "Race")
employment = reshape_acs(employment, "Emp")
income = reshape_acs(income, "Inc")
poverty = reshape_acs(poverty, "Pov")

# === Merge all ACS datasets ===
acs_merged = education \
    .merge(race, on="State", how="outer") \
    .merge(employment, on="State", how="outer") \
    .merge(income, on="State", how="outer") \
    .merge(poverty, on="State", how="outer")

# === Add state abbreviations ===
state_abbrev_map = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
acs_merged["state_abbr"] = acs_merged["State"].map(state_abbrev_map)

# === Merge police shootings data ===
shooting_stats = shootings.groupby("state").size().reset_index(name="total_police_killings")
final = pd.merge(acs_merged, shooting_stats, left_on="state_abbr", right_on="state", how="left")
final.drop(columns=["state"], inplace=True)

# === Normalize by population ===
population_col = next((col for col in final.columns if "Race_Total" in col), None)
if not population_col:
    raise ValueError("No column found containing 'Race_Total' for population.")

final["Population"] = pd.to_numeric(final[population_col].str.replace(",", ""), errors="coerce")
final["killings_per_100k"] = (final["total_police_killings"] / final["Population"]) * 100000

# === Save final dataset ===
final.to_csv("acs_full_with_shootings.csv", index=False)
print("✅ Final dataset saved as 'acs_full_with_shootings.csv'")
