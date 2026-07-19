Title: Palimpsest
Description: A palimpsest is a manuscript where earlier text was scraped away and written over — but traces of the original remain. We intercepted this transmission. The original message is in there somewhere.
Category: Crypto
Difficulty: Medium

## Setup (no Docker needed)

Players receive `challenge.txt`. No server is required.

To regenerate `challenge.txt` after changing the flag:

```bash
# Edit .env to set your flag, then:
python3 generate.py
```

Commit the updated `challenge.txt` to your CTF platform.

## Notes for organizers

- The flag is encoded through four successive layers:
    1. **Base85 (ASCII85, `!-u`)** — encodes raw bytes as printable ASCII
    2. **ROT13**  — rotates alphabetic characters by 13 positions
    3. **Reverse** — reverses the entire character sequence
    4. **Base32** — produces the final A-Z/2-7 output in `challenge.txt`
- No key is needed; all four operations are deterministic and key-free.
  The challenge is identifying what was applied and in what order.
- Intended to be solved with **CyberChef**: From Base32 → Reverse → ROT13 → From Base85
  (all default settings — Base85 alphabet `!-u` is the CyberChef default).
- `generate.py` also contains a `decode()` function for organiser verification.
- See `solution.txt` for the walkthrough.
