FROM python:3.11-slim

WORKDIR /app
COPY generate.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8092
ENTRYPOINT ["./entrypoint.sh"]
