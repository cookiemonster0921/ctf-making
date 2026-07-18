#!/usr/bin/env python3
"""
RSA Håstad Broadcast Attack challenge (e = 3).

The same message (the flag) is encrypted under three independent RSA
public keys, all sharing exponent e = 3.  This is the classic setup
for Håstad's broadcast attack:

  c_i = m^3 mod n_i   for i = 1, 2, 3

Because the moduli are pairwise coprime, the Chinese Remainder Theorem
lets us recover m^3 mod (n1*n2*n3).  Since m < each n_i, no modular
reduction occurred, so m^3 mod (n1*n2*n3) = m^3 exactly.
Taking the integer cube root yields m, which decodes to the flag.

Run this script to regenerate challenge.json whenever the flag changes:

    FLAG='CSEC{your_flag_here}' python3 generate.py

No external dependencies — uses a built-in Miller-Rabin primality test.
"""
import json
import os
import sys


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


def icbrt(n: int) -> int:
    """Return floor(n^(1/3)) for non-negative n using Newton-Raphson integer arithmetic."""
    if n == 0:
        return 0
    # Start with an upper-bound estimate based on bit length, then converge
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        x1 = (2 * x + n // (x * x)) // 3
        if x1 >= x:
            return x
        x = x1


def modinv(a: int, m: int) -> int:
    """Extended Euclidean modular inverse."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('No modular inverse')
    return x % m


def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def _miller_rabin(n: int, k: int = 20) -> bool:
    """Deterministic-ish Miller-Rabin primality test."""
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    import random as _rnd
    for _ in range(k):
        a = _rnd.randrange(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_prime(bits: int) -> int:
    """Generate a random probable prime with the given bit length."""
    import random as _rnd
    while True:
        # Top two bits set (so product has correct bit length), bottom bit set (odd)
        p = _rnd.getrandbits(bits) | (3 << (bits - 2)) | 1
        if _miller_rabin(p):
            return p


def gen_rsa_modulus(bits: int, e: int = 3):
    """Generate an RSA modulus of given bit length coprime with phi."""
    while True:
        p = _random_prime(bits // 2)
        q = _random_prime(bits // 2)
        if p == q:
            continue
        n   = p * q
        phi = (p - 1) * (q - 1)
        if extended_gcd(e, phi)[0] == 1:
            return n


def main():
    load_env()
    flag = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    here = os.path.dirname(__file__)

    m = int.from_bytes(flag.encode(), 'big')

    # Flag must fit in a 512-bit modulus (max 64 bytes / 512 bits)
    if m.bit_length() > 512:
        print(f'ERROR: Flag is {m.bit_length()} bits — max 512 bits (64 bytes).', file=sys.stderr)
        sys.exit(1)

    e = 3
    moduli = []
    ciphers = []

    print('Generating RSA moduli (this may take a few seconds)...')
    for i in range(3):
        while True:
            n = gen_rsa_modulus(512, e)
            if n > m:
                break
        c = pow(m, e, n)
        moduli.append(n)
        ciphers.append(c)
        print(f'  Key {i+1}: n ({n.bit_length()} bits), c ({c.bit_length()} bits)')

    # Verify with CRT
    N  = moduli[0] * moduli[1] * moduli[2]
    Ns = [N // n for n in moduli]
    M  = sum(ciphers[i] * Ns[i] * modinv(Ns[i], moduli[i]) for i in range(3)) % N
    assert icbrt(M) ** 3 == M, 'M is not a perfect cube — something went wrong'
    recovered = icbrt(M).to_bytes((icbrt(M).bit_length() + 7) // 8, 'big').decode()
    assert recovered == flag, f'Round-trip mismatch: {recovered!r} != {flag!r}'

    challenge = {
        'e': e,
        'note': 'Three recipients. Same message. Same small exponent. Different moduli.',
        'keys': [
            {'n': moduli[i], 'c': ciphers[i]} for i in range(3)
        ],
    }

    out = os.path.join(here, 'challenge.json')
    with open(out, 'w') as f:
        json.dump(challenge, f, indent=2)

    print(f'Generated {out}')


if __name__ == '__main__':
    main()
