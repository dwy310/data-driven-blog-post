import pandas as pd
import numpy as np
import re
import os
import ast

# 1. Load CSV
# Folder where clean.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute path to movies.csv
df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..","data-driven-blog-post","data", "movies.csv")))

# Remove rows where Year, IMDb Rating, and Duration are all "N/A"
df = df[~(
    df["Year"].isna() &
    df["IMDb Rating"].isna() &
    df["Duration"].isna()
)]

# 2. Check % of missing values in each column
def check_missing_values(column):
    nan_percentage = df[column].isnull().sum() / df[column].size
    print(f'"{column}" column consists of {nan_percentage:.2%} missing values.')

for column in df.columns:
    check_missing_values(column)

# 3. Clean Year column
#    - Extract year from "(2025)" style strings
#    - Fill missing using Title
def extract_year_from_title(title):
    match = re.search(r"\((\d{4})\)", str(title))
    if match:
        return int(match.group(1))
    return np.nan

# Extract year if Year contains "(2025)" or similar
df["Year"] = df["Year"].astype(str).str.extract(r"(\d{4})")

# Fill remaining NaN with 0 and convert to int
df["Year"] = df["Year"].fillna(0).astype(int)
 
# 4. Replace missing values
# Rating, Duration → 0
df["IMDb Rating"] = df["IMDb Rating"].fillna(0)
df["Duration"] = df["Duration"].fillna("0")

# Remove rows where Cast or Director are "N/A"
df = df[
    (df["Cast"] != "N/A") &
    (df["Director"] != "N/A")
]

# 5. Convert Duration to minutes
def duration_to_minutes(x):
    if not isinstance(x, str):
        return 0
    h = re.search(r"(\d+)h", x)
    m = re.search(r"(\d+)min", x)
    hours = int(h.group(1)) if h else 0
    mins = int(m.group(1)) if m else 0
    return hours * 60 + mins

df["Duration"] = df["Duration"].apply(duration_to_minutes)

# 6. Clean IMDb Rating (extract numeric part)
df["IMDb Rating"] = df["IMDb Rating"].astype(str).str.extract(r"(\d+\.\d+)").astype(float)

# 7. Expand variables into list
df["Genres"] = df["Genres"].str.split(", ")
df["Cast"] = df["Cast"].str.split(", ")
df["Director"] = df["Director"].str.split(", ")
df["Providers"] = df["Providers"].str.split(", ")


# 8. Split IMDb Rating into:
# Extract review count text e.g. "143k"
df["Review Count Raw"] = df["IMDb Rating"].astype(str).str.extract(r"\((.*?)\)")

# Extract numeric rating
df["IMDb Rating"] = df["IMDb Rating"].astype(str).str.extract(r"(\d+\.\d+)").astype(float)

# Drop the temporary column
df.drop(columns=["Review Count Raw"], inplace=True)

# 9. Save clean data into CSV in data folder
df.to_csv(
    os.path.abspath(os.path.join(BASE_DIR, "..", "data-driven-blog-post", "data", "movies_clean1.csv")),
    index=False
)

print(df.dtypes)

