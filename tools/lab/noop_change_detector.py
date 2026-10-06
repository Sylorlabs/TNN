#!/usr/bin/env python3
"""NO-OP-CHANGE DETECTOR.

p5meta5c produced byte-identical tables after a SUBSTANTIVE change to both the
fitness function and the observation schedule. Identical numbers after a real
edit mean the edit did not take effect -- that is an instrumentation fault, and
treating it as a scientific finding wasted a phase.

This tool compares two raw tables and reports whether any arm changed. If a
declared substantive change produced zero difference, it fails loudly.

Usage: noop_change_detector.py <before.txt> <after.txt> --substantive
Exit 0 = something changed (expected). Exit 2 = NO-OP (suspicious).
"""
import sys


def sig(path):
    out = {}
    for line in open(path):
        f = line.split()
        if not f or f[0] not in ("FP", "T", "R", "G", "Q"):
            continue
        d = {}
        for x in f[1:]:
            if "=" in x:
                k, v = x.split("=", 1)
                d[k] = v
        key = (d.get("regime", d.get("rg", "?")), d.get("arm", "?"))
        # COSMETIC fields are ignored: the experiment label and the seed
        # changing is not a behavioural change. Comparing them made a real
        # no-op look like a change.
        out[key] = tuple(sorted((k, v) for k, v in d.items()
                                if k not in ("exp", "seed")))
    return out


def main():
    a, b = sig(sys.argv[1]), sig(sys.argv[2])
    common = set(a) & set(b)
    if not common:
        print("RESULT=INCOMPARABLE (no shared rows)")
        sys.exit(2)
    changed = [k for k in common if a[k] != b[k]]
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    print(f"shared rows: {len(common)}   changed: {len(changed)}")
    if only_a:
        print(f"rows only in before: {len(only_a)} {only_a[:5]}")
    if only_b:
        print(f"rows only in after : {len(only_b)} {only_b[:5]}")
    if not changed:
        print("RESULT=NO-OP-CHANGE  a substantive edit produced IDENTICAL output.")
        print("  Treat as an instrumentation fault: the edit did not take effect.")
        sys.exit(2)
    print("RESULT=CHANGED")
    for k in sorted(changed)[:5]:
        print(f"  {k}: {a[k]} -> {b[k]}")
    sys.exit(0)


if __name__ == "__main__":
    main()
