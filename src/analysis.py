import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
import os
from itertools import product
from collections import defaultdict, Counter

# Folder where analysis.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute path to movies.csv
df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..","data-driven-blog-post","data", "movies_clean.csv")))

# Data Preparation
df["Cast"] = df["Cast"].apply(ast.literal_eval)
df["Director"] = df["Director"].apply(ast.literal_eval)
df["Providers"] = df["Providers"].apply(ast.literal_eval)
df["Genres"] = df["Genres"].apply(lambda x: ast.literal_eval(x))

#----------------------
# EDA 
#----------------------
# Highest‑rated genres
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

# Rating vs. duration
plt.figure(figsize=(8, 5)) #(X,y)
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

# Average Movie Length per Genre
avg_duration = (
    genre_df.groupby("Genres")["Duration"]
    .mean()
    .sort_values(ascending=False)
)

print("Average Duration per Genre:")
print(avg_duration)

# Plot
plt.figure(figsize=(14, 8))
bars = plt.bar(avg_duration.index, avg_duration.values, color="seagreen")

plt.title("Average Movie Duration by Genre")
plt.ylabel("Duration (minutes)")
plt.xlabel("Genre")

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha="right")

# Add vertical data labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 1,
        f"{height:.1f}",
        ha="center",
        va="bottom",
        rotation=45
    )

plt.tight_layout()
plt.show()

#----------------------
# Genre Analysis
#----------------------
# 1. Cluster Movies by Genre Combinations
df["Genre Combo"] = df["Genres"].apply(tuple) # Convert list → tuple so it can be grouped

genre_clusters = df.groupby("Genre Combo").size().sort_values(ascending=False)

print("Genre Combination Clusters:")
print(genre_clusters)

# 3. Genres combined with animation
animated_movies = df[df["Genres"].apply(lambda g: "Animation" in g)]
# Flatten all genres from animation movies
all_genres = [genre for genres in animated_movies["Genres"] for genre in genres]

# Count them
genre_counts = Counter(all_genres)

# Remove Animation itself
genre_counts.pop("Animation", None)

# Convert to a sorted Series
genre_counts = pd.Series(genre_counts).sort_values(ascending=False)

plt.figure(figsize=(14, 8))
bars = plt.bar(genre_counts.index, genre_counts.values, color="seagreen")

plt.title("Genres Common with Animation")
plt.ylabel("Count")

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha="right")

# Add vertical data labels
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        str(height),
        ha='center',
        va='bottom',
        rotation=45
    )

plt.tight_layout()
plt.show()
print(genre_counts)
#----------------------
# Director Analysis
#----------------------
# 1. Top‑Rated Directors
# Explode directors into separate rows
director_df = df.explode("Director")

# Compute average rating per director
director_ratings = (
    director_df.groupby("Director")["IMDb Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("Top‑Rated Directors:")
print(director_ratings.head(10))

# Visualize
plt.figure(figsize=(10, 6))
plt.barh(director_ratings.head(10).index, director_ratings.head(10).values, color="darkgreen")
plt.xlabel("Average IMDb Rating")
plt.title("Top‑Rated Directors")
plt.tight_layout()
plt.show()


# 2. Director-Actor Collab
collab_counter = Counter()
pair_ratings = defaultdict(list)
for _, row in df.iterrows():
    directors = row["Director"]
    actors = row["Cast"]
    rating = row["IMDb Rating"]

    # Count every director–actor pair
    for d, a in product(directors, actors):
        collab_counter[(d, a)] += 1
        pair_ratings[(d, a)].append(rating)

avg_pair_ratings = {
    (d, a): sum(ratings) / len(ratings)
    for (d, a), ratings in pair_ratings.items()
}

# Convert to DataFrame for easy sorting
ratings_df = (
    pd.DataFrame([
        {"Director": d, "Actor": a, "Avg_Rating": avg, "Count": len(pair_ratings[(d, a)])}
        for (d, a), avg in avg_pair_ratings.items()
    ])
    .sort_values(by="Count", ascending=False)
)

print(ratings_df.head(20))

# Take top 10 by collaboration count
top10 = ratings_df.sort_values("Count", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top10,
    x="Count",
    y=top10["Director"] + " & " + top10["Actor"],
    palette="Blues_r"
)

plt.title("Top 10 Director–Actor Collaborations (by Count)")
plt.xlabel("Number of Movies Together")
plt.ylabel("Director–Actor Pair")
plt.tight_layout()
plt.show()

#----------------------
# Cast Analysis
#----------------------
# 1. Actor Frequency
actor_counter = Counter()

for cast_list in df["Cast"]:
    actor_counter.update(cast_list)

top_20_actors = actor_counter.most_common(20)

print("Top 20 Most Frequent Actors:")
for actor, count in top_20_actors:
    print(f"{actor}: {count} movies")

actors, counts = zip(*top_20_actors)

plt.figure(figsize=(10, 8))
plt.barh(actors, counts, color="teal")
plt.xlabel("Number of Movies")
plt.title("Top 20 Most Frequent Actors")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 2. Star Power
# Explode actors into rows
actor_df = df.explode("Cast")

# Compute average rating per actor
actor_avg_rating = (
    actor_df.groupby("Cast")["IMDb Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("Top 20 Highest-Rated Actors (by average movie rating):")
print(actor_avg_rating.head(20))
plt.figure(figsize=(10, 8))
plt.barh(actor_avg_rating.head(20).index, actor_avg_rating.head(20).values, color="darkgreen")
plt.xlabel("Average IMDb Rating")
plt.title("Top 20 Actors by Average Movie Rating")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()