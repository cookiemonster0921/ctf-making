Title: Static
Description: Our threat-intel team intercepted this audio file from a suspicious endpoint. There's nothing audible that makes sense — just noise. But maybe the problem isn't what you hear.
Category: Forensics
Difficulty: Medium

## Setup

```bash
docker compose up --build -d
```

Players download the file from:

    http://<host>:8091/challenge.wav

Tear down:

```bash
docker compose down
```

## Notes for organizers

- `generate.py` reads `FLAG` from the environment and synthesises a WAV file
  whose spectrogram renders the flag as visible text in the 1000–8000 Hz band.
- Each column of the internal image becomes a time slice of the audio; each row
  maps to a sine-wave frequency.  The result sounds like broadband noise but
  is unambiguous in any spectrogram viewer.
- The flag value can be changed by editing `.env` and restarting (`docker compose
  up --build -d`); no other files need to change.
- See `solution.txt` for the verified walkthrough and two solve methods (Audacity
  GUI and Python one-liner).
