FROM ollama/ollama:latest

# Bake the model weights into the image at BUILD time so the container
# never needs network access at runtime (fast, offline-reproducible startup).
# We start the ollama server in the background just long enough to pull
# the model, then let the build finish (the server process from this RUN
# layer is not kept around; the runtime CMD from the base image starts a
# fresh server when the container actually runs).
RUN nohup bash -c "ollama serve &" >/tmp/ollama-serve.log 2>&1 \
    && sleep 5 \
    && ollama pull qwen2.5:1.5b \
    && ollama list

# Sanity marker so we can confirm at build time the model is present.
ENV OLLAMA_BAKED_MODEL=qwen2.5:1.5b

EXPOSE 11434
