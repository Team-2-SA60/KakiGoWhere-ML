'''
Machine learning deployment for KakiGoWhere
'''
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.ml.data_loader import needs_refresh, refresh_categories, needs_refresh_ratings, refresh_ratings_keywords, KEYWORDS_RATINGS_CSV
from app.ml.recommender import recommend
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import json
import pandas as pd

app = Flask(__name__)
CORS(app)

# setup cache for keywords for fast loading
_keyword_cache = {}

def load_keyword_cache():
    df = pd.read_csv(KEYWORDS_RATINGS_CSV)
    global _keyword_cache # assign at module level
    _keyword_cache = {
        int(r["placeId"]): {
            "common":     json.loads(r["common_keywords"]),
            "noteworthy": json.loads(r["noteworthy_keywords"])
        }
        for _, r in df.iterrows()
    }

# safe "job" functions to cover CSV reading or parsing failure
def refresh_categories_job():
    try:
        refresh_categories()
    except Exception as e:
        app.logger.error("Failed to refresh place categories", exc_info=e)

def refresh_ratings_keywords_job():
    try:
        refresh_ratings_keywords()
        load_keyword_cache()
    except Exception as e:
        app.logger.error("Failed to refresh ratings keywords", exc_info=e)

try :
    # on startup, call safe "jobs" and load keyword cache
    if needs_refresh():
        refresh_categories_job()
        
    if needs_refresh_ratings():
        refresh_ratings_keywords_job()
        
    load_keyword_cache()

    # scheduler at 00:00 server time
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=refresh_categories_job,
        trigger="cron",
        hour=0, minute=0
    )
    scheduler.add_job(
        func=refresh_ratings_keywords_job,
        trigger="cron",
        hour=0, minute=0
    )
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown()) # shutdown
except Exception as e:
    print(e)

@app.route("/recommend", methods=["POST"])
def recommend_api():
    data = request.get_json()
    interests = data.get("interests")
    recs = recommend(interests)
    result = []
    for place_id, name in recs:
        result.append({"id": place_id, "name": name})
    return jsonify(result)

@app.route("/adjectives", methods=["GET"])
def adjectives_api():
    raw_id = request.args.get("placeId")
    if raw_id is None:
        return jsonify({"error": "Missing placeId parameter"}), 400

    # convert to int
    try:
        place_id = int(raw_id)
    except ValueError:
        return jsonify({"error": "placeId must be an integer"}), 400

    # lookup in-memory cache
    entry = _keyword_cache.get(place_id)
    if entry is None:
        # empty list
        entry = {"common": [], "noteworthy": []}

    return jsonify({
        "placeId":   place_id,
        "common":    entry["common"],
        "noteworthy": entry["noteworthy"]
    })

@app.route('/')
def index():
    '''
    GET: Home
    '''
    return jsonify("Hello from Flask on DigitalOcean!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

