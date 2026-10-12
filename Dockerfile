FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render sets $PORT (default 10000); fall back to 10000 if it isn't set.
CMD gunicorn app:app --workers 2 --threads 4 --timeout 60 --bind 0.0.0.0:${PORT:-10000}