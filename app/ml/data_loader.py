import os
import pandas as pd
import json
from app.ml.categories import assign_categories
from app.ml.adjectives import extract_adjectives

# paths inside container
RAW_CSV = os.environ.get("RAW_CSV", "/data/csv/places.csv")
CATEGORISED_CSV = os.environ.get("CATEGORISED_CSV", "/data/csv/places_categorised.csv")
RAW_RATINGS_CSV     = os.environ.get("RAW_RATINGS_CSV", "/uploads/csv/ratings.csv")
KEYWORDS_RATINGS_CSV = os.environ.get("KEYWORDS_RATINGS_CSV", "/uploads/csv/ratings_keywords.csv")


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
    print(f"Refreshed categories for {len(df)} places into {CATEGORISED_CSV}")
    return df

# below for ratings_keywords.csv
def needs_refresh_ratings():
    if not os.path.exists(KEYWORDS_RATINGS_CSV):
        return True
    return os.path.getmtime(RAW_RATINGS_CSV) > os.path.getmtime(KEYWORDS_RATINGS_CSV)

def refresh_ratings_keywords(common_n=3, noteworthy_n=3):
    df = pd.read_csv(RAW_RATINGS_CSV)

    # group comments per place
    grouped = df.groupby("placeId")["comment"].apply(list)

    records = []
    for place_id, comments in grouped.items():
        common, noteworthy = extract_adjectives(
            comments,
            common_n=common_n,
            noteworthy_n=noteworthy_n
        )
        records.append({
            "placeId": place_id,
            "common_keywords": json.dumps(common),
            "noteworthy_keywords": json.dumps(noteworthy)
        })

    # persist to new csv
    out_df = pd.DataFrame(records)
    out_df.to_csv(KEYWORDS_RATINGS_CSV, index=False)
    print(f"Refreshed keywords for {len(records)} places into {KEYWORDS_RATINGS_CSV}")
    return out_df