#!/bin/bash
set -e
mkdir -p /data
python3 /app/generate.py
echo "Serving challenge at http://0.0.0.0:8092/"
exec python3 -m http.server 8092 --directory /data
