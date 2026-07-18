Title: Broadcast
Description: A message was sent simultaneously to three different recipients, each with their own public key. All three used the same encryption exponent. One mathematician's theorem from 1988 makes this a problem.
Category: Crypto
Difficulty: Hard

## Setup (no Docker needed)

Players receive `challenge.json`. No server is required.

To regenerate `challenge.json` after changing the flag (requires `sympy`):

```bash
pip install sympy
# Edit .env to set your flag (max 40 characters), then:
python3 generate.py
```

## Notes for organizers

- The flag is converted to an integer (`m`), then encrypted as `m^3 mod n_i`
  for three independent 512-bit RSA moduli (`n1, n2, n3`), all with `e = 3`.
- The three ciphertexts, combined via the Chinese Remainder Theorem, yield
  `m^3 mod (n1·n2·n3)`.  Since `m < each n_i`, no reduction occurred, so
  `m^3 mod N = m^3` exactly — and the integer cube root gives `m`.
- **Flag length limit**: the flag as bytes must be < 512 bits (64 bytes).
  Typical flags of 25–40 characters are fine.
- `generate.py` verifies the round-trip before writing the file.
- See `solution.txt` for the complete mathematical walkthrough and Python
  solve script.
