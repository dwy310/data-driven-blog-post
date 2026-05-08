'''
This script cleans and prepares the raw movie metadata scraped from JustWatch.
The raw dataset contains mixed formats, list-like strings, embedded years in
titles, and non‑numeric rating fields. The goal of this file is to convert the
scraped data into a consistent, analysis‑ready structure.

Key cleaning steps include:
- Converting list‑formatted strings (Genres, Cast, Director, Providers) into
  real Python lists using ast.literal_eval.
- Extracting release years from title strings when the Year field is missing.
- Cleaning IMDb ratings by isolating the numeric component and converting it
  to float.
- Removing rows where Year, IMDb Rating, and Duration are all missing.
- Standardising column types and validating the dataset for NaN values.

The cleaned dataset produced by this script is used throughout the analysis
pipeline to generate figures, tables, and the final blog post.
'''
import pandas as pd
import numpy as np
import re
import os
import ast

# Load CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Folder where clean.py lives

# Build absolute path to movies.csv
df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..","data", "movies.csv")))

# 1. Remove rows where Year, IMDb Rating, and Duration are all "N/A"
df = df[~(
    df["Year"].isna() &
    df["IMDb Rating"].isna() &
    df["Duration"].isna()
)]

# Check % of missing values in each column
def check_missing_values(column):
    nan_percentage = df[column].isnull().sum() / df[column].size
    print(f'"{column}" column consists of {nan_percentage:.2%} missing values.')

for column in df.columns:
    check_missing_values(column)

# 2. Extract year if Year contains "(2025)" or similar
df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})")
 
# 3. Replace missing values
# Fill Year NaN with 0 and convert to int
df["Year"] = df["Year"].fillna(0).astype(int)
# Rating and Duration → 0
df["IMDb Rating"] = df["IMDb Rating"].fillna(0)
df["Duration"] = df["Duration"].fillna("0")
# Cast and Director → "Unknown"
df["Cast"] = df["Cast"].fillna("Unknown")
df["Director"] = df["Director"].fillna("Unknown")

# 4. Convert Duration to minutes
def duration_to_minutes(x):
    if not isinstance(x, str):
        return 0
    h = re.search(r"(\d+)h", x)
    m = re.search(r"(\d+)min", x)
    hours = int(h.group(1)) if h else 0
    mins = int(m.group(1)) if m else 0
    return hours * 60 + mins

df["Duration"] = df["Duration"].apply(duration_to_minutes)

# 5. Clean IMDb Rating (extract numeric part) eg. "7.8 (143k)" → "7.8"
df["IMDb Rating"] = df["IMDb Rating"].astype(str).str.extract(r"(\d+\.\d+)").astype(float)

# 6. Expand variables into list
df["Genres"] = df["Genres"].str.split(", ")
df["Cast"] = df["Cast"].str.split(", ")
df["Director"] = df["Director"].str.split(", ")
df["Providers"] = df["Providers"].str.split(", ")

# 7. Save clean data into CSV in data folder
df.to_csv(
    os.path.abspath(os.path.join(BASE_DIR, "..", "data", "movies_clean1.csv")),
    index=False
)

print(df.dtypes)

