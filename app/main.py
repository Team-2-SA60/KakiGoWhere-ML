'''
Machine learning deployment for KakiGoWhere
'''
from flask import Flask, request, jsonify
from ml.data_loader import update_new_places
from ml.preprocess import preprocess_categories
from ml.recommender import recommend

# update for new places
update_new_places()
# tag them with zero-shot categories
preprocess_categories()

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend_api():
    data      = request.get_json(force=True)
    interests = data["interests"]
    top_k     = data.get("top_k", 3)

    recs = recommend(interests, top_k=top_k)
    return jsonify([{"id":pid,"name":name} for pid,name in recs])

@app.route('/')
def index():
    '''
    GET: Home
    '''
    return jsonify("Hello from Flask on DigitalOcean!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
