import os
import pandas as pd
import requests

RAW_CSV = "../data/places.csv"
API_URL = "http://localhost:8080/api/placedtos"

def fetch_raw_places():
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

def load_existing():
    if os.path.exists(RAW_CSV):
        return pd.read_csv(RAW_CSV)
    return pd.DataFrame(columns=["id", "kmlId", "name", "description", "interestCategories"])

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
    # ensure every row has a list
    ic_list  = []
    for _, row in raw.iterrows():
        ic = row.get("interestCategories")
        if ic is None:
            ic_list.append([])
        else:
            ic_list.append(ic)
    raw["interestCategories"] = ic_list

    # find only new IDs
    old_ids = set()
    if "id" in existing.columns:
        for v in existing["id"].tolist():
            try:
                old_ids.add(int(v))
            except Exception:
                continue

    new_rows_list = []
    for _, row in raw.iterrows():
        try:
            rid = int(row["id"])
        except Exception:
            continue
        if rid not in old_ids:
            new_rows_list.append(row)

    if not new_rows_list:
        print("No new places to add.")
        return existing

    # append and save
    combined = pd.concat([existing, new_rows_list], ignore_index=True)
    save_places(combined)
    return combined

