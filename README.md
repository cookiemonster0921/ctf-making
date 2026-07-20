# Techfest CTF 2026 Challenges

Challenge repository for the 2026 Techfest CTF event run by the UTS Cyber Security Society.

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

## Requirements

| Requirement | Windows | macOS | Linux |
|---|---|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | ✅ | ✅ | ✅ |
| Python 3.8+ | ✅ | ✅ | ✅ |
| `curl` (for web challenge testing) | ✅ Win 10+ built-in | ✅ | ✅ |
| `nc` / `ncat` (for PWN testing) | via [nmap](https://nmap.org/) or WSL | ✅ | ✅ |

> **Windows users**: All `.sh` files in this repo are Docker **entrypoint scripts** — they
> run *inside* Linux containers and are never executed directly on your machine.
> You only ever need to run `docker compose` and `python` commands from your terminal.

---

## Setup (all platforms)

**Step 1 — copy all `.env` files at once (cross-platform):**

```
python setup.py
```

This walks every challenge directory and copies `.env.example` → `.env`.
Re-run with `--force` to overwrite existing `.env` files.

**Step 2 — set your flags:**

Open each `.env` file and replace the placeholder with your real flag:
```
FLAG=CSEC{your_flag_here}
```

---

### Docker challenges (PWN / WEB / AI / Forensics)

```
cd <category>/<challenge-name>
docker compose up --build -d
```

To stop:
```
docker compose down
```

> `docker compose` is identical on Windows, macOS, and Linux when Docker Desktop is installed.

---

### Crypto challenges (no Docker)

Each crypto challenge has a `generate.py` that reads the flag from `.env` and
writes the challenge artifact(s). Distribute those files to players.

```
cd crypto/<challenge-name>
python generate.py
```

> Use `python` or `python3` depending on your system. No external packages required.

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
- Use `.env.example` as the template, or run `python setup.py` to copy all at once.
- Each challenge has a `solution.txt` with a full walkthrough — keep this
  out of players' hands during the event.
