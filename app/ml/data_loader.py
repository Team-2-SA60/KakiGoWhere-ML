import os
import pandas as pd
import requests

RAW_CSV = "../data/places.csv"
API_URL = "http://localhost:8080/api/places"

def fetch_raw_places():
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

def load_existing():
    if os.path.exists(RAW_CSV):
        return pd.read_csv(RAW_CSV)
    return pd.DataFrame(columns=["id", "kmlId", "name", "description", "interestCategories"])

# flatten [{'id':1,'name':'museum'}, ...] into "museum, ..." or return "" if empty
def flatten_interests(ic_list):
    if not isinstance(ic_list, list):
        return ""
    names = []
    for entry in ic_list:
        nm = entry.get("name")
        if nm:
            names.append(nm.strip())
    return ", ".join(names)

def save_places(df):
    cols = ["id", "kmlId", "name", "description", "interestCategories"]
    df_subset = df[cols]
    df_subset.to_csv(RAW_CSV, index=False)
    print(f"Saved {len(df)} places to {RAW_CSV}")

def update_new_places():
    # load existing
    existing = load_existing()
    # fetch all
    raw = fetch_raw_places()
    # flatten interestCategories
    flat_ic  = []
    for _, row in raw.iterrows():
        flat_ic.append(flatten_interests(row.get("interestCategories")))
    raw["interestCategories"] = flat_ic

    # find only new IDs
    old_ids  = set(existing["id"].astype(int))
    new_mask = raw["id"].astype(int).apply(lambda x: x not in old_ids)
    new_rows = raw[new_mask].copy()
    if new_rows.empty:
        print("No new places to add.")
        return existing

    # append and save
    combined = pd.concat([existing, new_rows], ignore_index=True)
    save_places(combined)
    return combined

