FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates

EXPOSE 8090

CMD ["gunicorn", "--bind", "0.0.0.0:8090", "--workers", "2", "--timeout", "120", "app:app"]
