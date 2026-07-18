#!/usr/bin/env python3
"""
One-Time Pad key-reuse challenge.

Two messages are encrypted with the SAME random key:

  ciphertext_a = flag  XOR key[:len(flag)]
  ciphertext_b = msg_b XOR key[:len(msg_b)]

Players receive:
  - ciphertext_a.hex  (the encrypted flag)
  - ciphertext_b.hex  (an encrypted known message)
  - plaintext_b.txt   (the known message in cleartext)

Recovery:
  1. key_fragment = bytes.fromhex(ciphertext_b) XOR plaintext_b.encode()
  2. flag          = bytes.fromhex(ciphertext_a) XOR key_fragment[:len(ciphertext_a)//2]

Run this script to regenerate all three files whenever the flag changes:

    FLAG='CSEC{your_flag_here}' python3 generate.py
"""
import os
import secrets

KNOWN_MESSAGE = (
    "OPERATIONAL MEMO: The encryption system uses a one-time pad with a "
    "randomly generated key. Under no circumstances should the same key "
    "be used more than once. Violation of this policy constitutes a "
    "critical security incident and must be reported immediately to the "
    "information security team without delay."
)


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, key))


def main():
    load_env()
    flag  = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    here  = os.path.dirname(__file__)

    msg_a = flag.encode()
    msg_b = KNOWN_MESSAGE.encode()

    assert len(msg_b) >= len(msg_a), (
        f'Flag ({len(msg_a)} bytes) exceeds known-message length ({len(msg_b)} bytes). '
        f'Make the flag shorter or expand KNOWN_MESSAGE.'
    )

    key      = secrets.token_bytes(len(msg_b))
    ct_a     = xor_bytes(msg_a, key)
    ct_b     = xor_bytes(msg_b, key)

    # Verify round-trip
    recovered = xor_bytes(ct_a, xor_bytes(ct_b, msg_b))
    assert recovered == msg_a, 'Round-trip check failed!'

    with open(os.path.join(here, 'ciphertext_a.hex'), 'w') as f:
        f.write(ct_a.hex() + '\n')

    with open(os.path.join(here, 'ciphertext_b.hex'), 'w') as f:
        f.write(ct_b.hex() + '\n')

    with open(os.path.join(here, 'plaintext_b.txt'), 'w') as f:
        f.write(KNOWN_MESSAGE + '\n')

    print('Generated: ciphertext_a.hex, ciphertext_b.hex, plaintext_b.txt')
    print(f'Flag length: {len(msg_a)} bytes  |  Key length: {len(key)} bytes')


if __name__ == '__main__':
    main()
