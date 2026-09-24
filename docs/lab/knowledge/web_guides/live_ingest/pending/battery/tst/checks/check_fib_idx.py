#!/usr/bin/env python3
"""PROTO FIB-IDX check program (frozen battery fixture).

Reads the fixture input path from argv[1]: "N V" (integers).
Computes Fib(N) with Fib(0)=0, Fib(1)=1 by exact integer iteration.
Exits 0 iff Fib(N) == V, else 1. Deterministic.
"""
import sys


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    with open(sys.argv[1]) as f:
        parts = f.read().split()
    n, v = int(parts[0]), int(parts[1])
    sys.exit(0 if fib(n) == v else 1)


main()
