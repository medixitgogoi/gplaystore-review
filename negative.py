import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --------------------------------------------------
# 1. Download VADER (run once)
# --------------------------------------------------
nltk.download("vader_lexicon")

# --------------------------------------------------
# 2. FILE PATHS
# --------------------------------------------------
INPUT_FILE = "data/category_reviews.csv"
OUTPUT_FILE = "data/strong_negative_reviews.csv"

# --------------------------------------------------
# 3. Load Data
# --------------------------------------------------
print("Loading data...")

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8",
    engine="python"
)

# Check required columns
if "content" not in df.columns or "score" not in df.columns:
    raise ValueError("Required columns 'content' and/or 'score' not found.")

# Clean content
df["content"] = df["content"].fillna("").astype(str)

print("Total Reviews:", len(df))

# --------------------------------------------------
# 4. Initialize VADER
# --------------------------------------------------
sia = SentimentIntensityAnalyzer()

# --------------------------------------------------
# 5. Calculate Compound Score
# --------------------------------------------------
def get_compound(text):
    return sia.polarity_scores(text)["compound"]

print("Running sentiment analysis...")

df["compound"] = df["content"].apply(get_compound)

# --------------------------------------------------
# 6. Filter ONLY Strong Negative (<= -0.5)
# --------------------------------------------------
strong_df = df[df["compound"] <= -0.5]

print("Strong Negative Reviews Found:", len(strong_df))

# --------------------------------------------------
# 7. Keep ONLY content + score
# --------------------------------------------------
# strong_df = strong_df[["content", "score"]]
strong_df = strong_df[["content"]]

# --------------------------------------------------
# 8. Save File
# --------------------------------------------------
strong_df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print("Done 🚀")
