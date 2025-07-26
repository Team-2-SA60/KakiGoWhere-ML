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
1. Build docker iamge
```
docker build -f ./docker/Dockerfile -t flask-ml .
```

2. Run docker container. Access at http://localhost:5000
```
docker run -d --name flask-ml -p 5000:5000 -t flask-ml 
```

3. Stop and delete docker container
```
docker rm -f flask-ml
```