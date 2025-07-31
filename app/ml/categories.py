from transformers import pipeline

# pre-defined labels
CATEGORY_LABELS = [
    "Food and Beverage",
    "Gardens and Nature",
    "Museums",
    "Culture",
    "Entertainment",
    "Theme Parks",
    "Wildlife and Zoos",
    "Shopping",
    "Heritage Sites"
]

# instantiate Zero-shot Natural Language Inference (NLI) model for use
classifier = pipeline(
    task="zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1, # use CPU; set to 0 for GPU if available
    multi_label=True
)

# using the name + desc of each place, return a list of interest labels where confidence >= threshold
def assign_categories(docs, threshold=0.5, top_n=3):
    all_tags = []
    for text in docs:
        out    = classifier(text, CATEGORY_LABELS,
                            hypothesis_template="This text is about {}.")
        labs   = out["labels"][:top_n] # limit up to 3
        scores = out["scores"][:top_n]

        # keep all above threshold
        tags = []
        for lbl, sc in zip(labs, scores):
            if sc >= threshold:
                tags.append(lbl)

        # fallback to highest if none pass
        if not tags:
            tags = [labs[0]]
        all_tags.append(tags)
    return all_tags