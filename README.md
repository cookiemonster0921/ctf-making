ctfs

Each challenge is fully self-contained in its own directory with no dependencies on other challenges.

---

## Categories

### PWN
| Challenge | Difficulty | Port | CVE |
|-----------|------------|------|-----|
| [lost-privileges](pwn/lost-privileges/) | Hard | 9001 | CVE-2021-3156 (Baron Samedit) |

### WEB
| Challenge | Difficulty | Port | CVE |
|-----------|------------|------|-----|
| [nothing-to-see-here](web/nothing-to-see-here/) | Medium | 8080 | CVE-2021-41773 (Apache path traversal) |

### AI
| Challenge | Difficulty | Port | Technique |
|-----------|------------|------|-----------|
| [help-desk](ai/help-desk/) | Medium | 8090 | LLM01:2025 Prompt Injection |

### Forensics
| Challenge | Difficulty | Port | Technique |
|-----------|------------|------|-----------|
| [static](forensics/static/) | Medium | 8091 | Audio spectrogram steganography |
| [noisy-neighbor](forensics/noisy-neighbor/) | Hard | 8092 | DNS exfiltration in PCAP |
| [extra-extra](forensics/extra-extra/) | Easy | 8093 | ZIP archive comment metadata |

### Crypto (no Docker required)
| Challenge | Difficulty | Technique |
|-----------|------------|-----------|
| [palimpsest](crypto/palimpsest/) | Medium | Multi-layer encoding (Base85 → ROT13 → Reverse → Base32) |
| [two-keys](crypto/two-keys/) | Medium | One-time pad key reuse |
| [broadcast](crypto/broadcast/) | Hard | RSA Håstad broadcast attack (e=3) |

---

## Setup

### Docker challenges (PWN / WEB / AI / Forensics)

Each Docker challenge is fully independent:

```bash
cd <category>/<challenge-name>/
cp .env.example .env
# Edit .env and set FLAG=CSEC{your_flag_here}
docker compose up --build -d
```

To stop:
```bash
docker compose down
```

### Crypto challenges (no Docker)

Each crypto challenge provides a `generate.py` that reads the flag from `.env`
and writes the challenge artifact(s):

```bash
cd crypto/<challenge-name>/
cp .env.example .env
# Edit .env and set FLAG=CSEC{your_flag_here}
python3 generate.py
# Commit the generated artifact files and distribute them to players
```

---

## Flag format

All flags use the format: `CSEC{...}`

---

## Misc ideas

See [MISC_IDEAS.md](MISC_IDEAS.md) for 10 challenge concepts that don't fit
standard categories (SSTV, Whitespace language, QR repair, printer tracking dots,
blockchain, custom binary protocol, and more).

---

## Notes

- `.env` files containing real flag values are excluded from version control via `.gitignore`.
- Use `.env.example` as the template when setting up each challenge.
- Each challenge has a `solution.txt` with a beginner-friendly walkthrough — keep this
  out of players' hands during the event.
