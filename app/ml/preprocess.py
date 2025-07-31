import pandas as pd
from ml.categories import assign_categories

RAW_CSV       = "../data/places.csv"

# load a CSV file and return the df, docs (name + desc of place)
def load_corpus(source):
    df = pd.read_csv(source)

    docs = []
    for _, row in df.iterrows():
        title = row["name"]
        desc  = row.get("description", "") or ""
        docs.append(f"{title} {desc}".lower())
    return df, docs

# write new "categories" back to csv file
def preprocess_categories(threshold=0.5, top_n=3):
    df, docs = load_corpus(RAW_CSV)
    zs_tags = assign_categories(docs, threshold, top_n)

    df["categories"] = zs_tags
    df.to_csv(RAW_CSV, index=False)
    print(f"Updated {len(df)} places with categories in {RAW_CSV}")
    return df