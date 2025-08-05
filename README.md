## For developing
1. (Optional) Create virtual python environment
```
python -m venv .venv
```

2. (Optional) Activate venv environment

- For Windows
```
.venv\Scripts\activate.bat
```

- For Linux/Mac
```
source .venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

## Local testing commands
1. Lint (Pylint)
```
pylint --ignore=tests app
```

2. SCA (pip-audit)
```
pip-audit
```

3. Unit tests (pytest)
```
coverage run -m pytest
```

4. Code coverage (coverage)
```
coverage report --fail-under=70
```

## Docker
1. Build docker image
```
docker build -f ./docker/Dockerfile -t flask-ml .
```

2. Run docker container. Access at http://localhost:5001 or  http://127.0.0.1:5001/
```
docker run -d \
  --name flask-ml \
  -p 5001:5001 \
  -v docker_app_csv:/data/csv \
  -e RAW_CSV=/data/csv/places.csv \
  -e CATEGORISED_CSV=/data/csv/places_categorised.csv \
  -e RAW_RATINGS_CSV=/data/csv/ratings.csv \
  -e KEYWORDS_RATINGS_CSV=/data/csv/ratings_keywords.csv \
  flask-ml
```

3. (Optional) Test recommend API (e.g., With interest "Culture")
```
curl -X POST http://127.0.0.1:5001/recommend \
  -H "Content-Type: application/json" \
  -d '{"interests":["Culture"]}'

```

4. Stop and delete docker container
```
docker rm -f flask-ml
```