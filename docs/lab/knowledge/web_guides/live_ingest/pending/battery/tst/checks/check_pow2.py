#!/usr/bin/env python3
"""PROTO POW2 check program (frozen battery fixture).

Reads the fixture input path from argv[1]: "K V" (integers).
Exits 0 iff 2**K == V, else 1. Exact integer arithmetic, deterministic.
"""
import sys


def main():
    with open(sys.argv[1]) as f:
        parts = f.read().split()
    k, v = int(parts[0]), int(parts[1])
    sys.exit(0 if (1 << k) == v else 1)


main()
