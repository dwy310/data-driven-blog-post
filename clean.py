import pandas as pd
import numpy as np
import re
import ast

# 1. Load CSV
df = pd.read_csv("movies.csv")
 
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

# Cast and Director → "Unknown"
df["Cast"] = df["Cast"].fillna("Unknown")
df["Director"] = df["Director"].fillna("Unknown")

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
df["Genres"] = df["Genres"].apply(ast.literal_eval)
df["Cast"] = df["Cast"].apply(ast.literal_eval)
df["Director"] = df["Director"].apply(ast.literal_eval)
df["Providers"] = df["Providers"].apply(ast.literal_eval)



# 8. Split IMDb Rating into:
# Extract review count text e.g. "143k"
df["Review Count Raw"] = df["IMDb Rating"].astype(str).str.extract(r"\((.*?)\)")

# Extract numeric rating
df["IMDb Rating"] = df["IMDb Rating"].astype(str).str.extract(r"(\d+\.\d+)").astype(float)

# Drop the temporary column
df.drop(columns=["Review Count Raw"], inplace=True)

# 9. Save clean data into CSV
df.to_csv("movies_clean.csv", index=False)

print(df.dtypes)

