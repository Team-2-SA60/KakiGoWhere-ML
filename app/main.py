'''
Machine learning deployment for KakiGoWhere
'''
import os
from flask import Flask, request, jsonify
from app.ml.data_loader import needs_refresh, refresh_categories
from app.ml.recommender import recommend
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# on startup, ensure categories exist/ refreshed
if needs_refresh():
    refresh_categories()

# scheduler at 00:00 server time
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=lambda: refresh_categories(),
    trigger="cron",
    hour=0,
    minute=0
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown()) # shutdown

@app.route("/recommend", methods=["POST"])
def recommend_api():
    data = request.get_json()
    interests = data.get("interests")
    recs = recommend(interests)
    result = []
    for place_id, name in recs:
        result.append({"id": place_id, "name": name})
    return jsonify(result)

@app.route('/')
def index():
    '''
    GET: Home
    '''
    return jsonify("Hello from Flask on DigitalOcean!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

