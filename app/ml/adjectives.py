import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from operator import itemgetter

# no. of tokens to scan before/after an ADJ for negation
FRONT_WINDOW = 3
BACK_WINDOW  = 0
NEG_TOKENS   = {"not", "never"}
GENERIC_ADJECTIVES = {  "daily", "weekly", "monthly", "yearly", "annual",
                        "hourly", "seasonal", "occasional", "frequent",
                        "infrequent", "regular", "sporadic", "periodic"}

# drop NER (natural entity recognition) for speed
nlp = spacy.load("en_core_web_sm", disable=["ner"])

def extract_terms(texts):
    documents_adjectives = []
    
    # process batch of 32 ratings
    for doc in nlp.pipe(texts, batch_size=32):
        terms = []
        for token in doc:
            # pick only alphabetic adjectives
            if token.pos_ == "ADJ" and token.is_alpha and not token.is_stop and token.lemma_.lower() not in GENERIC_ADJECTIVES:
                # negation based on dependency parser
                negation = None
                for child in token.children:
                    if child.dep_ == "neg":
                        negation = child.lemma_.lower()
                        break
                        
                # fallback negation based on tokens (not, never)
                if not negation:
                    start = max(0, token.i - FRONT_WINDOW)
                    end = token.i + BACK_WINDOW + 1
                    for i in range(start, end):
                        if i != token.i and doc[i].lemma_.lower() in {"not", "never"}:
                            negation = doc[i].lemma_.lower()
                            break
                            
                # normalise to base form
                base = token.lemma_.lower()
                
                # build term with negation if present
                if negation:
                    terms.append(negation + " " + base)
                else:
                    terms.append(base)
        documents_adjectives.append(terms)
        
    return documents_adjectives

def get_common_adjectives(documents_adjectives, top_n):
    counter = Counter()
    
    for terms in documents_adjectives:
        counter.update(terms)
    
    # returns (term, count) pairs
    return [term for term, _ in counter.most_common(top_n)]

def get_noteworthy_adjectives(documents_adjectives, common, top_n):
    unique_terms = {term for terms in documents_adjectives for term in terms}
    
    docs_for_tfidf = [" ".join(terms) for terms in documents_adjectives]
    
    # build with unigram and bigrams which count "not big" as one feature
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(docs_for_tfidf)
    
    # get all the terms out and sum TF-IDF scores for each term across all docs
    terms_all = vectorizer.get_feature_names_out()
    scores_sum   = tfidf_matrix.sum(axis=0).A1 # flatten to 1D arr
    
    # pair term with their score
    term_score_pairs = list(zip(terms_all, scores_sum))
    # sort in desc order
    term_score_pairs.sort(key=itemgetter(1), reverse=True)

    noteworthy = []
    for term, _ in term_score_pairs:
        # only include those in unique terms & not in common
        if term in unique_terms and term not in common:
            noteworthy.append(term)
            if len(noteworthy) == top_n:
                break
    
    return noteworthy

def extract_adjectives(texts, common_n=3, noteworthy_n=3):
    
    documents_adjectives = extract_terms(texts)
    common = get_common_adjectives(documents_adjectives, common_n)
    # skip anything already in 'common'
    noteworthy = get_noteworthy_adjectives(
        documents_adjectives,
        common,
        noteworthy_n
    )
    return common, noteworthy