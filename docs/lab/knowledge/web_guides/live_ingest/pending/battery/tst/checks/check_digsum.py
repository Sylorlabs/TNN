#!/usr/bin/env python3
"""PROTO DIGSUM check program (frozen battery fixture).

Reads the fixture input path from argv[1]: "M S" where M is a decimal
integer string and S an integer. Exits 0 iff the sum of M's decimal
digits == S, else 1. Deterministic.
"""
import sys


def main():
    with open(sys.argv[1]) as f:
        parts = f.read().split()
    m, s = parts[0], int(parts[1])
    ok = m.isdigit() and sum(int(d) for d in m) == s
    sys.exit(0 if ok else 1)


main()
