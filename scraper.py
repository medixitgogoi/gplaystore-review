import os
import pandas as pd
from google_play_scraper import Sort, reviews_all, search

# 1. Setup the data folder
if not os.path.exists('data'):
    os.makedirs('data')

# 2. Fetch only 5 apps from the category
# You can change "finance" to "productivity", "education", etc.
category_keyword = "lifestyle"
print(f"Searching for top 5 apps in: {category_keyword}...")

apps = search(
    category_keyword,
    lang="en",
    country="us",
    n_hits=5  # <--- This limits the number of apps
)

all_reviews = []

# 3. Loop through the 5 apps
for index, app in enumerate(apps):
    app_id = app['appId']
    print(f"({index + 1}/5) Scraping reviews for: {app_id}")
    
    try:
        # Fetching all reviews for these specific apps
        result= reviews_all(
            app_id,
            sleep_milliseconds=1000,
            lang='en',
            country='us',
            sort=Sort.NEWEST
        )
        
        # Tag each review with its App ID
        for r in result:
            r['appId'] = app_id
        
        all_reviews.extend(result)
        print(f"   Successfully fetched {len(result)} reviews.")
        
    except Exception as e:
        print(f"   Skipping {app_id} due to error: {e}")

# 4. Save and Summary
if all_reviews:
    df = pd.DataFrame(all_reviews)
    df.to_csv('data/category_reviews.csv', index=False)
    print("\n" + "="*30)
    print(f"DONE! Total reviews collected: {len(all_reviews)}")
    print(f"File saved to: data/category_reviews.csv")
    print("="*30)
else:
    print("No reviews were collected.")