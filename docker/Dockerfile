FROM python:3.13-slim

# Set directory
WORKDIR /app

# Get requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ .

EXPOSE 5001

# Set flask app file
ENV FLASK_APP=main

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]