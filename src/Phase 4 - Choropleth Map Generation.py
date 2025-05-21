import pandas as pd
import plotly.express as px
import json
import urllib.request
import os

# === Load Dataset ===
df = pd.read_csv("acs_full_with_shootings.csv")

# === Drop rows with missing data ===
df = df.dropna(subset=["State", "killings_per_100k"])

# === Load US States GeoJSON ===
geo_url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
with urllib.request.urlopen(geo_url) as response:
    us_states_geojson = json.load(response)

# === Output Folder ===
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# === Plot Choropleth Using Full State Names ===
fig = px.choropleth(
    df,
    geojson=us_states_geojson,
    locations="State",  # ✅ match full state names
    featureidkey="properties.name",  # ✅ tells plotly where to match
    color="killings_per_100k",
    color_continuous_scale="Reds",
    scope="usa",
    hover_name="State",
    labels={"killings_per_100k": "Killings per 100k"},
    title="Police Killings per 100k by U.S. State"
)

# === Save + Show ===
fig.write_html(f"{output_dir}/choropleth_killings_per_100k.html")
fig.show()
