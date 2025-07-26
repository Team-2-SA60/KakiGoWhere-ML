'''
Machine learning deployment for KakiGoWhere
'''
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    '''
    GET: Home
    '''
    return jsonify("Hello from Flask on DigitalOcean!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
