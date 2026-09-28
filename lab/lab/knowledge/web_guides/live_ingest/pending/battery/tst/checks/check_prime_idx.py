#!/usr/bin/env python3
"""PROTO PRIME-IDX check program (frozen battery fixture).

Reads the fixture input path from argv[1]: two integers "N V".
Recomputes the Nth prime deterministically (sieve with a proven-sufficient
upper bound) and exits 0 iff it equals V, else 1. Deterministic: no
network, no clock reads.
"""
import sys
import math


def nth_prime(n):
    small = [2, 3, 5, 7, 11, 13]
    if n <= len(small):
        return small[n - 1]
    # Rosser bound: for n >= 6, p_n < n * (log n + log log n)
    bound = int(n * (math.log(n) + math.log(math.log(n)))) + 10
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0] = 0
    sieve[1] = 0
    r = int(math.isqrt(bound))
    for p in range(2, r + 1):
        if sieve[p]:
            start = p * p
            sieve[start:bound + 1:p] = b"\x00" * ((bound - start) // p + 1)
    count = 0
    for i in range(2, bound + 1):
        if sieve[i]:
            count += 1
            if count == n:
                return i
    raise AssertionError("sieve bound too small for N=%d" % n)


def main():
    with open(sys.argv[1]) as f:
        parts = f.read().split()
    n, v = int(parts[0]), int(parts[1])
    sys.exit(0 if nth_prime(n) == v else 1)


main()
