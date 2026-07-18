#!/usr/bin/env python3
"""
Encode the flag through four successive layers:

  1. Base85  — encodes arbitrary bytes as printable ASCII
  2. ROT13   — rotates alphabetic characters by 13 positions
  3. Reverse — reverses the character sequence
  4. Base32  — final output (uppercase A-Z + digits 2-7, padded with =)

Run this script to regenerate challenge.txt whenever the flag changes:

    FLAG='CSEC{your_flag_here}' python3 generate.py

Players receive challenge.txt and must identify and reverse all four layers.
"""
import base64
import os


def rot13(s: str) -> str:
    out = []
    for c in s:
        if 'a' <= c <= 'z':
            out.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            out.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            out.append(c)
    return ''.join(out)


def encode(flag: str) -> str:
    step1 = base64.b85encode(flag.encode()).decode()   # Base85
    step2 = rot13(step1)                               # ROT13
    step3 = step2[::-1]                                # Reverse
    step4 = base64.b32encode(step3.encode()).decode()  # Base32
    return step4


def decode(ciphertext: str) -> str:
    """Reference decode — for organiser verification only."""
    step1 = base64.b32decode(ciphertext).decode()
    step2 = step1[::-1]
    step3 = rot13(step2)
    step4 = base64.b85decode(step3.encode()).decode()
    return step4


def load_env():
    """Load .env in the same directory if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def main():
    load_env()
    flag    = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    encoded = encode(flag)

    # Sanity check
    assert decode(encoded) == flag, 'Round-trip check failed!'

    out_path = os.path.join(os.path.dirname(__file__), 'challenge.txt')
    with open(out_path, 'w') as f:
        f.write('Intercepted transmission — contents unknown\n')
        f.write('-------------------------------------------\n')
        f.write(encoded + '\n')

    print(f'challenge.txt written ({len(encoded)} chars)')
    print(f'First 40 chars: {encoded[:40]}...')


if __name__ == '__main__':
    main()
