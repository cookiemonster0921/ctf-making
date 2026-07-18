Title: Two Keys, One Lock
Description: An intercepted communication channel was used to send two encrypted messages. The operators insisted their encryption was unbreakable. They were wrong about one thing.
Category: Crypto
Difficulty: Medium

## Setup (no Docker needed)

Players receive three files:
- `ciphertext_a.hex` — the encrypted flag
- `ciphertext_b.hex` — a second encrypted message
- `plaintext_b.txt`  — the plaintext of the second message

To regenerate all three files after changing the flag:

```bash
# Edit .env to set your flag, then:
python3 generate.py
```

Note: running `generate.py` also regenerates the key, so the hex files change
even if the flag does not. Commit all three generated files to your CTF platform.

## Notes for organizers

- Both ciphertexts were XOR'd with the **same** random key (one-time pad reuse).
- The key is longer than both messages, so XOR with the known message extracts
  the exact key bytes needed to decrypt the flag.
- The flag length must be ≤ len(KNOWN_MESSAGE) in `generate.py`. The current
  default known message supports flags up to ~300 characters.
- See `solution.txt` for the complete walkthrough.
