'''
This script performs the full exploratory analysis for the movie dataset after
cleaning. It loads the processed CSV produced by clean.py and generates all
figures and tables used in the final blog post.

The analysis covers:
- Descriptive statistics for ratings, runtimes, and release years.
- Genre‑level summaries, including frequency counts and average IMDb ratings.
- Actor and director analyses, such as top performers and collaboration patterns.
- Visualisations including bar charts, histograms and scatter plots.

This script forms the analytical core of the project, transforming the
cleaned dataset into interpretable insights and publication‑ready visuals.
'''

import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from itertools import product
from collections import defaultdict, Counter

# Folder where analysis.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute path to movies_clean.csv
df = pd.read_csv(os.path.abspath(os.path.join(BASE_DIR, "..","data", "movies_clean.csv")))

# Data Preparation
# Convert list-like strings into list objects 
df["Cast"] = df["Cast"].apply(ast.literal_eval)
df["Director"] = df["Director"].apply(ast.literal_eval)
df["Providers"] = df["Providers"].apply(ast.literal_eval)
df["Genres"] = df["Genres"].apply(lambda x: ast.literal_eval(x))

#----------------------
# Prelimanary EDA 
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

plt.figure(figsize=(14, 8))
bars = plt.bar(avg_duration.index, avg_duration.values, color="seagreen")

plt.title("Average Movie Duration by Genre")
plt.ylabel("Duration (minutes)")
plt.xlabel("Genre")
plt.xticks(rotation=45, ha="right")
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
# Cluster Movies by Genre Combinations
df["Genre Combo"] = df["Genres"].apply(tuple) # Convert list → tuple so it can be grouped

genre_clusters = df.groupby("Genre Combo").size().sort_values(ascending=False)

print("Genre Combination Clusters:")
print(genre_clusters)

# Genres combined with animation
animated_movies = df[df["Genres"].apply(lambda g: "Animation" in g)]
all_genres = [genre for genres in animated_movies["Genres"] for genre in genres]
genre_counts = Counter(all_genres)
genre_counts.pop("Animation", None)
genre_counts = pd.Series(genre_counts).sort_values(ascending=False)

plt.figure(figsize=(14, 8))
bars = plt.bar(genre_counts.index, genre_counts.values, color="seagreen")
plt.title("Genres Common with Animation")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
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
# Top‑Rated Directors
director_df = df.explode("Director") # Explode directors into separate rows
director_ratings = (
    director_df.groupby("Director")["IMDb Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("Top‑Rated Directors:")
print(director_ratings.head(10))

plt.figure(figsize=(10, 6))
plt.barh(director_ratings.head(10).index, director_ratings.head(10).values, color="darkgreen")
plt.xlabel("Average IMDb Rating")
plt.title("Top‑Rated Directors")
plt.tight_layout()
plt.show()


# Director-Actor Collab
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

ratings_df = ( # Convert to DataFrame for easy sorting
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
# Actor Frequency
actor_counter = Counter()

for cast_list in df["Cast"]: # Exclude Unknown in Cast list
    cleaned_cast = [actor for actor in cast_list if actor != "Unknown"]
    actor_counter.update(cleaned_cast)

top_20_actors = actor_counter.most_common(20)

print("Top 20 Most Frequent Actors:")
for actor, count in top_20_actors:
    print(f"{actor}: {count} movies")

actors, counts = zip(*top_20_actors) # Unpack the list of (actor, count) tuples into two separate lists:

plt.figure(figsize=(10, 8))
plt.barh(actors, counts, color="teal")
plt.xlabel("Number of Movies")
plt.title("Top 20 Most Frequent Actors")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Frequent Actors Average IMDB Rating
actors = [actor for actor, _ in top_20_actors] # Extract actor names
counts = {actor: count for actor, count in top_20_actors}

actor_avg_ratings = {} # Compute average IMDb rating for each actor
for actor in actors:
    # Filter rows where actor appears in the Cast list
    actor_movies = df[df["Cast"].apply(lambda x: actor in x)]
    avg_rating = actor_movies["IMDb Rating"].mean()
    actor_avg_ratings[actor] = avg_rating

ratings_df = ( # Convert to DataFrame
    pd.DataFrame({
        "Actor": list(actor_avg_ratings.keys()),
        "Avg_Rating": list(actor_avg_ratings.values()),
        "Count": [counts[a] for a in actors],
    })
    .sort_values(by="Count", ascending=False)
)

print("Average IMDb Rating for the Same Top 20 Frequent Actors:")
print(ratings_df)

plt.figure(figsize=(10, 8))
plt.barh(ratings_df["Actor"], ratings_df["Avg_Rating"], color="darkred")
plt.xlabel("Average IMDb Rating")
plt.title("Average IMDb Rating of the Top 20 Most Frequent Actors")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Star Power
actor_df = df.explode("Cast") # Explode actors into rows
actor_avg_rating = ( # Compute average rating per actor
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