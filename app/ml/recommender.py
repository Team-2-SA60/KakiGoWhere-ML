import pandas as pd
from operator import itemgetter

RAW_CSV = "../data/places.csv"

# load csv, count how many of the user's interests appear and return the top_k (id, name) tuples
def recommend(interests, top_k=3):
    df = pd.read_csv(RAW_CSV)
    places = []

    for _, row in df.iterrows():
        # count matches
        count = 0
        for interest in interests:
            if interest in row["categories"]:
                count += 1
        places.append((row["id"], row["name"], count))

    # sort by match count descending
    places.sort(key=itemgetter(2), reverse=True)

    # return just the ids & names of the top_k
    return [(pid, name) for pid, name, _ in places[:top_k]]

# if __name__ == "__main__":
#     sample_interests = ["Museums", "Culture"]
#     print(f"Now recommending for {sample_interests!r}")
#     recs = recommend(sample_interests, top_k=3)
#
#     for pid, name in recs:
#         print(f"  • [{pid}] {name}")
