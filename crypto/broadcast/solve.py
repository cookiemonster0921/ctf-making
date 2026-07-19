#!/usr/bin/env python3
"""
Håstad Broadcast Attack solver for the 'broadcast' challenge.

Usage:
    python3 solve.py
"""
import json


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def modinv(a, m):
    _, x, _ = extended_gcd(a % m, m)
    return x % m


def icbrt(n):
    """Integer cube root via Newton-Raphson (exact, no floating point)."""
    if n == 0:
        return 0
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        x1 = (2 * x + n // (x * x)) // 3
        if x1 >= x:
            return x
        x = x1


data = json.load(open('challenge.json'))
keys = data['keys']
n = [k['n'] for k in keys]
c = [k['c'] for k in keys]

N  = n[0] * n[1] * n[2]
Ns = [N // ni for ni in n]
M  = sum(c[i] * Ns[i] * modinv(Ns[i], n[i]) for i in range(3)) % N

m = icbrt(M)
assert m ** 3 == M, 'M is not a perfect cube — something went wrong'

flag = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
print(flag)
