FROM python:3.13-slim

# Set directory
WORKDIR /app

# Get requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to control transformers cache location inside container
ENV TRANSFORMERS_CACHE=/app/cache/huggingface

# Pre-download the zero-shot model so it won't download at runtime
RUN python -c "from transformers import pipeline; pipeline('zero-shot-classification', model='facebook/bart-large-mnli', device=-1)"

# Copy app files
COPY app/ .

EXPOSE 5001

# Set flask app file
ENV FLASK_APP=main

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]