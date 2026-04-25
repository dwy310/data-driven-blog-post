import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Load data
df = pd.read_csv("movies_clean.csv")


# 2. Highest‑rated genres
genre_df = df.explode("Genres")

genre_ratings = (
    genre_df.groupby("Genres")["IMDb Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("Average IMDb Rating by Genre:")
print(genre_ratings)

plt.figure(figsize=(8, 5))
sns.barplot(
    x=genre_ratings.values,
    y=genre_ratings.index,
    palette="viridis"
)
plt.xlabel("Average IMDb Rating")
plt.ylabel("Genre")
plt.title("Highest‑Rated Genres")
plt.tight_layout()
plt.show()


# 3. Rating distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["IMDb Rating"].dropna(), bins=15, kde=True, color="steelblue")
plt.xlabel("IMDb Rating")
plt.ylabel("Count")
plt.title("Distribution of IMDb Ratings")
plt.tight_layout()
plt.show()


# 4. Rating vs. year
plt.figure(figsize=(8, 5))
sns.regplot(
    data=df,
    x="Year",
    y="IMDb Rating",
    scatter_kws={"alpha": 0.6},
    line_kws={"color": "red"}
)
plt.xlabel("Year")
plt.ylabel("IMDb Rating")
plt.title("IMDb Rating vs. Year")
plt.tight_layout()
plt.show()

print("Correlation (Rating vs Year):", df["Year"].corr(df["IMDb Rating"]))


# 5. Rating vs. duration
plt.figure(figsize=(8, 5))
sns.regplot(
    data=df,
    x="Duration",
    y="IMDb Rating",
    scatter_kws={"alpha": 0.6},
    line_kws={"color": "darkred"}
)
plt.xlabel("Duration (minutes)")
plt.ylabel("IMDb Rating")
plt.title("IMDb Rating vs. Duration")
plt.tight_layout()
plt.show()

print("Correlation (Rating vs Duration):", df["Duration"].corr(df["IMDb Rating"]))
