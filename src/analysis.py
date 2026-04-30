import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from itertools import product
from collections import Counter

#----------------------
# Rating Analysis
#----------------------
# 1. Load data
url = "https://raw.githubusercontent.com/dwy310/data-driven-blog-post/main/data/movies_clean.csv"
df = pd.read_csv(url)

df["Cast"] = df["Cast"].apply(ast.literal_eval)
df["Director"] = df["Director"].apply(ast.literal_eval)
df["Providers"] = df["Providers"].apply(ast.literal_eval)

# 2. Highest‑rated genres
# Parse Genres from string representation of list → actual Python list
df["Genres"] = df["Genres"].apply(lambda x: ast.literal_eval(x))

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
plt.figure(figsize=(10, 5))
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
plt.xlim(2000, df["Year"].max())
plt.ylim(0, 10)
plt.xticks(range(2000, df["Year"].max() + 1, 10))
plt.tight_layout()
plt.show()

print("Correlation (Rating vs Year):", df["Year"].corr(df["IMDb Rating"]))


# 5. Rating vs. duration
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

#----------------------
# Genre Analysis
#----------------------
# 1. Most Common Genres
# Count frequency
genre_counts = genre_df["Genres"].value_counts()

print("Most Common Genres:")
print(genre_counts)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(genre_counts.index, genre_counts.values, color="steelblue")
plt.xlabel("Count")
plt.title("Most Common Genres")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 2. Cluster Movies by Genre Combinations
# Convert list → tuple so it can be grouped
df["Genre Combo"] = df["Genres"].apply(tuple)

genre_clusters = df.groupby("Genre Combo").size().sort_values(ascending=False)

print("Genre Combination Clusters:")
print(genre_clusters)

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
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# 2. Director Genre Specialization
collab_counter = Counter()

for _, row in df.iterrows():
    directors = row["Director"]
    actors = row["Cast"]
    
    # Count every director–actor pair
    for d, a in product(directors, actors):
        collab_counter[(d, a)] += 1

print("Top Director–Actor Collaborations:")
for (director, actor), count in collab_counter.most_common(20):
    print(f"{director} & {actor} → {count} movies")

# 3. Get top 10 director–actor pairs
top = collab_counter.most_common(10)

# Build a graph with only those edges
G = nx.Graph()

for (director, actor), count in top:
    G.add_edge(director, actor, weight=count)

# Visualise
plt.figure(figsize=(10, 8))

# Use circular layout (no SciPy needed)
pos = nx.circular_layout(G)

# Node sizes scaled by number of connections
nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="lightblue")

# Edge width scaled by collaboration count
nx.draw_networkx_edges(
    G, pos,
    width=[count for (_, _), count in top]
)

# Labels
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Top 5 Director–Actor Collaborations")
plt.axis("off")
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

# 2. Actor-Director Collaboration
top5 = collab_counter.most_common(10)

G = nx.Graph()

for (director, actor), count in top5:
    G.add_edge(director, actor, weight=count)

plt.figure(figsize=(10, 8))
pos = nx.circular_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=1200, node_color="lightblue")
nx.draw_networkx_edges(G, pos, width=[count for (_, _), count in top5])
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Top Director–Actor Collaborations")
plt.axis("off")
plt.show()

# 3. Star Power
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

#----------------------
# Duration Analysis
#----------------------
# 1. Duration Distribution
plt.figure(figsize=(10, 6))
plt.hist(df["Duration"], bins=20, color="skyblue", edgecolor="black")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Movies")
plt.title("Distribution of Movie Durations")
plt.tight_layout()
plt.show()

#----------------------
# Providers Analysis
#----------------------
# 1. Providers by number of movies
provider_df = df.explode("Providers")

provider_counts = (
    provider_df["Providers"]
    .value_counts()
    .sort_values(ascending=False)
)
top20_providers = provider_counts.head(20)
print(top20_providers)
plt.figure(figsize=(12, 8))
plt.barh(top20_providers.index, top20_providers.values, color="teal")
plt.xlabel("Number of Movies")
plt.title("Top 20 Providers by Number of Movies")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()