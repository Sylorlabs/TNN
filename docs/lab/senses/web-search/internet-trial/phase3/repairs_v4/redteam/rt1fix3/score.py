#!/usr/bin/env python3
"""Deterministic scorer: engine output tags vs corpus oracle column. No RNG."""
import sys

OMAP = {"0": 0, "NEUTRAL": 0, "1": 1, "AFFIRM": 1, "2": 2, "DENY": 2, "3": 3}
SKIP = {"INFO", "VOID", ""}

def main():
    corpus, out = sys.argv[1], sys.argv[2]
    want = {}
    with open(corpus, encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip():
                continue
            p = ln.split("\t")
            if len(p) < 4:
                continue
            o = p[3].strip()
            if o in SKIP:
                continue
            want[p[0]] = OMAP[o]
    got = {}
    with open(out, encoding="utf-8") as f:
        for ln in f:
            p = ln.rstrip("\n").split(" ")
            if len(p) >= 2:
                got[p[0]] = int(p[1])
    miss = []
    for i, w in sorted(want.items()):
        g = got.get(i)
        if g != w:
            miss.append((i, w, g))
    extra = sorted(set(got) - set(want))
    print(f"{corpus}: scored={len(want)} mismatches={len(miss)}" + ("" if not extra else f" extra_ids={extra}"))
    for i, w, g in miss:
        print(f"  MISS {i}: oracle={w} engine={g}")

main()
