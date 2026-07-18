Title: Helpful Desk
Description: Jortelligence Corp's internal IT support chat is online. It's been told to keep a secret, and it insists it will. We're not so sure.
Category: AI
Difficulty: Medium

## Setup

```bash
cp .env.example .env
# edit .env and set FLAG=CSEC{...}
docker compose up --build -d
```

The chat UI is served on `http://localhost:8090`. Only the `web` service is exposed
to the host; the model backend runs on an internal Docker network and is not
reachable directly.

Bringing the stack down:

```bash
docker compose down
```

## Notes for organizers

- `ollama` service builds `qwen2.5:1.5b` into the image at build time (see
  `ollama/Dockerfile`), so no runtime network access is required once built.
- `web` service (Flask + gunicorn) holds the system prompt server-side,
  including the flag and refusal instructions, and forwards it plus the
  player's message to Ollama's `/api/chat` endpoint with `temperature=0`
  for consistent behavior. The model's raw response is returned to the
  player with no additional output filtering — the only defense is the
  system prompt itself.
- See `solution.txt` for the verified walkthrough and working payload.
