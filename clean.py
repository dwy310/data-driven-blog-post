import pandas as pd
import numpy as np
import re

# Load CSV
df = pd.read_csv("movies.csv")

def check_missing_values(column):
    nan_percentage = df[column].isnull().sum() / df[column].size
    print(f'"{column}" column consists of {nan_percentage:.2%} missing values.')

for column in df.columns:
    check_missing_values(column)

# --- Clean IMDb Rating ---
df["IMDb Rating"] = df["IMDb Rating"].str.extract(r"(\d+\.\d+)").astype(float)

# --- Convert Duration to minutes ---
def duration_to_minutes(x):
    h = re.search(r"(\d+)h", x)
    m = re.search(r"(\d+)min", x)
    hours = int(h.group(1)) if h else 0
    mins = int(m.group(1)) if m else 0
    return hours * 60 + mins

df["Duration_min"] = df["Duration"].apply(duration_to_minutes)

# --- Expand genres into list ---
df["Genres"] = df["Genres"].str.split(", ")