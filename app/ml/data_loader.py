import os
import pandas as pd
from app.ml.categories import assign_categories

# paths inside container
RAW_CSV = os.environ.get("RAW_CSV", "/data/csv/places.csv")
CATEGORISED_CSV = os.environ.get("CATEGORISED_CSV", "/data/csv/places_categorised.csv")

def load_raw_places():
    return pd.read_csv(RAW_CSV)

def needs_refresh():
    if not os.path.exists(CATEGORISED_CSV):
        return True
    raw_mtime = os.path.getmtime(RAW_CSV)
    cat_mtime = os.path.getmtime(CATEGORISED_CSV)
    return raw_mtime > cat_mtime

# refresh categories for places and persist to CATEGORISED_CSV
def refresh_categories(threshold=0.5, top_n=3):

    df = load_raw_places()

    combined_texts = []
    for _, row in df.iterrows():
        title = row.get("name", "") or ""
        desc = row.get("description", "") or ""
        interest_cats = row.get("interestCategories", "")

        if isinstance(interest_cats, list):
            interest_text = " ".join(interest_cats)
        elif isinstance(interest_cats, str):
            interest_text = interest_cats
        else:
            interest_text = ""

        text = f"{title} {desc} {interest_text}".strip().lower()
        combined_texts.append(text)

    zs_tags = assign_categories(combined_texts, threshold=threshold, top_n=top_n)
    df["categories"] = zs_tags

    # save file
    df.to_csv(CATEGORISED_CSV, index=False)
    print(f"[data_loader] Refreshed categories for {len(df)} places into {CATEGORISED_CSV}")
    return df

