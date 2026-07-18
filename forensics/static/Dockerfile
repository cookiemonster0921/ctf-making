FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy scipy Pillow

WORKDIR /app
COPY generate.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8091
ENTRYPOINT ["./entrypoint.sh"]
