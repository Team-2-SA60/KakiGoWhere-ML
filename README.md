#### For developing
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

#### Local testing commands
1. Lint (Pylint)
```
pylint ./**/*.py
```

2. SCA (pip-audit)
```
pip-audit
```

3. Code coverage (coverage)
```
coverage report /app/*
```

4. Unit tests (pytest)
```
pytest app/tests/testapi.py
```