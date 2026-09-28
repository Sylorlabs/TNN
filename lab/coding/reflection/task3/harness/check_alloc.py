#!/usr/bin/env python3
"""Allocator bars (frozen 2026-09-22). Reads program stdout on stdin.
--mode real : full frozen sequence; op6 (D 64) must succeed; op10 (F 300) must fail.
--mode naive: prefix ops 1-7; op7 must FAIL (-1) -- proves discrimination.
Semantic checks on every op: bounds [0,256), no overlap among live blocks,
FREE names a live block."""
import sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--mode", choices=["real", "naive"], required=True)
mode = ap.parse_args().mode

SIZES = {"A": 32, "B": 32, "C": 32, "D0": 64, "E": 64, "F": 200, "G": 300}
POOL = 256
# frozen op sequence: (kind, id)
SEQ = [("ALLOC", "A"), ("ALLOC", "B"), ("ALLOC", "C"), ("ALLOC", "D0"),
       ("FREE", "A"), ("FREE", "B"), ("ALLOC", "E"), ("FREE", "C"),
       ("FREE", "D0"), ("FREE", "E"), ("ALLOC", "F"), ("ALLOC", "G")]
if mode == "naive":
    SEQ = SEQ[:7]

lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
fails = []
live = {}  # id -> (off, size)

def overlap(a0, s0, a1, s1):
    return not (a0 + s0 <= a1 or a1 + s1 <= a0)

oi = 0
for ln in lines:
    parts = ln.split()
    if oi >= len(SEQ):
        break
    kind, ident = SEQ[oi]
    if kind == "ALLOC":
        if len(parts) != 3 or parts[0] != "ALLOC" or parts[1] != ident:
            fails.append(f"op{oi+1}: want 'ALLOC {ident} <off>', got {ln!r}")
            break
        try:
            off = int(parts[2])
        except ValueError:
            fails.append(f"op{oi+1}: bad offset {parts[2]!r}")
            break
        sz = SIZES[ident]
        if off == -1:
            pass  # failure; checked below per-mode
        else:
            if not (0 <= off and off + sz <= POOL):
                fails.append(f"op{oi+1}: ALLOC {ident} off={off} out of pool bounds")
            for j, (o2, s2) in live.items():
                if overlap(off, sz, o2, s2):
                    fails.append(f"op{oi+1}: ALLOC {ident} [{off},{off+sz}) overlaps live {j}")
            live[ident] = (off, sz)
        oi += 1
    else:  # FREE
        if len(parts) != 3 or parts[0] != "FREE" or parts[1] != ident or parts[2] != "OK":
            fails.append(f"op{oi+1}: want 'FREE {ident} OK', got {ln!r}")
            break
        if ident not in live:
            fails.append(f"op{oi+1}: FREE {ident} not live")
        else:
            del live[ident]
        oi += 1

if oi != len(SEQ):
    fails.append(f"only {oi}/{len(SEQ)} ops matched")

# per-mode discriminating assertions (re-parse offsets from matched lines)
offs = {}
for ln in lines[:len(SEQ)]:
    p = ln.split()
    if p[0] == "ALLOC":
        offs[p[1]] = int(p[2])

if mode == "real":
    if offs.get("E", -1) < 0:
        fails.append("real: op7 ALLOC E 64 must SUCCEED (coalescing)")
    if offs.get("G", 0) != -1:
        fails.append("real: op12 ALLOC G 300 must FAIL (-1)")
    for i in ("A", "B", "C", "D0", "F"):
        if offs.get(i, -1) < 0:
            fails.append(f"real: ALLOC {i} must succeed")
    if not any(l == "DONE" for l in lines):
        fails.append("real: missing DONE line")
else:  # naive
    for i in ("A", "B", "C", "D0"):
        if offs.get(i, -1) < 0:
            fails.append(f"naive: ALLOC {i} must succeed")
    if offs.get("E", 0) != -1:
        fails.append("naive: op7 ALLOC E 64 must FAIL (-1) -- scenario does not discriminate")

if fails:
    for f in fails:
        print("FAIL:", f)
    print("RESULT: FAIL")
    sys.exit(1)
print(f"RESULT: PASS ({mode})")
