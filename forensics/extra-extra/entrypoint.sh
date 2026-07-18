#!/bin/bash
set -e
mkdir -p /data
python3 /app/generate.py
echo "Serving challenge at http://0.0.0.0:8093/"
exec python3 -m http.server 8093 --directory /data
