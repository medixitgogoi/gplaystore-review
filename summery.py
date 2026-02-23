import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from tqdm import tqdm
from google import genai

# ------------------------------------------------
# CONFIG
# ------------------------------------------------
INPUT_FILE = "data/strong_negative_reviews.csv"
N_CLUSTERS = 8
MODEL_NAME = "gemini-3-flash-preview"

# ------------------------------------------------
# LOAD REVIEWS
# ------------------------------------------------
df = pd.read_csv(INPUT_FILE)
df["content"] = df["content"].astype(str)
texts = df["content"].tolist()

print(f"Total Reviews: {len(texts)}")

# ------------------------------------------------
# STEP 1: EMBEDDINGS
# ------------------------------------------------
print("Generating embeddings...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(texts, show_progress_bar=True)

# ------------------------------------------------
# STEP 2: CLUSTERING
# ------------------------------------------------
print("Clustering complaints...")
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42)
clusters = kmeans.fit_predict(embeddings)

df["cluster"] = clusters
cluster_groups = df.groupby("cluster")["content"].apply(list)

# ------------------------------------------------
# STEP 3: GEMINI CLIENT
# ------------------------------------------------
# Reads GEMINI_API_KEY automatically
client = genai.Client(api_key="")

# ------------------------------------------------
# STEP 4: SUMMARIZE EACH CLUSTER
# ------------------------------------------------
results = []

for cluster_id, reviews in tqdm(cluster_groups.items()):
    sample_reviews = " ".join(reviews[:25])

    prompt = f"""
You are a senior product manager.

These user reviews describe similar complaints.

Provide structured output:

Problem:
User Impact:
Suggested Fix:
Severity: High / Medium / Low

Reviews:
{sample_reviews}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    results.append(response.text)

# ------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------
print("\n=== ACTIONABLE PAIN POINTS ===\n")

for r in results:
    print(r)
    print("\n------------------------\n")

# ------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------
with open("data/gemini_actionable_pain_points.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(results))

print("Saved to data/gemini_actionable_pain_points.txt")
