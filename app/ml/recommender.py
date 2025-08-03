import pandas as pd
import ast
from operator import itemgetter
import os

CATEGORISED_CSV = os.environ.get("CATEGORISED_CSV", "/data/csv/places_categorised.csv")
DEFAULT_TOP_K = 3

# cache loaded dataframe
_df_cache = None

def _load_df():
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    try:
        _df_cache = pd.read_csv(CATEGORISED_CSV)
    except Exception:
        _df_cache = pd.DataFrame()
    return _df_cache

# parse categories list/ string into list of lowercase strings
def normalize_list_field(raw):
    if isinstance(raw, list):
        return [s.lower() for s in raw if isinstance(s, str)]

    if isinstance(raw, str):
        # parse a Python literal list
        try:
            parsed = ast.literal_eval(raw)
            if isinstance(parsed, list):
                return [str(s).lower() for s in parsed if isinstance(s, str)]
        except Exception:
            pass

        # fallback: split on commas, strip quotes/brackets
        stripped = raw.strip().strip("[]")
        parts = stripped.split(",")
        cleaned = []
        for part in parts:
            part = part.strip().strip("'\"")
            if part:
                cleaned.append(part.lower())
        return cleaned

    return []

# get list of interests from Tourist, return a dict with place id + name
def recommend(interests, top_k=DEFAULT_TOP_K):
    # load CSV
    df = _load_df()
    if df.empty:
        return []

    user_interests = normalize_list_field(interests)

    scored = []

    for _, row in df.iterrows():
        # skip malformed rows
        try:
            place_id = int(row["id"])
        except Exception:
            continue
        name = row.get("name", "")

        categories = normalize_list_field(row.get("categories", ""))

        # count overlap in categories
        match_count = 0
        for interest in user_interests:
            if interest in categories:
                match_count += 1

        scored.append((place_id, name, match_count))

    # sort by descending match_count
    scored.sort(key=itemgetter(2), reverse=True)

    # take top_k with positive score (optional: you can include zero-score if you want fallback)
    recommendations = []
    for place_id, name, score in scored[:top_k]:
        recommendations.append((place_id, name))

    return recommendations