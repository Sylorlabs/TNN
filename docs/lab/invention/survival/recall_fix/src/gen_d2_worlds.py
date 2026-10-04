#!/usr/bin/env python3
"""Generate 12 SHIFT variants (signal patterns + reward tables).
Home (d2_h0..d2_h5): home table.
Shifted (d2_s0..d2_s5): inverted table (s=0 and s=3 rows swapped).
Format: [T, plen, (f1,f2) x plen, table[12]]
Table rows for s in [(0,0),(0,1),(1,0),(1,1)]: [r_approach, r_hold, r_retreat].
"""
import random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'worlds')
os.makedirs(OUT, exist_ok=True)

HOME_TABLE = [-10,0,10,  0,5,0,  0,5,0,  10,0,-10]
SHIFT_TABLE = [10,0,-10,  0,5,0,  0,5,0,  -10,0,10]

def gen(rng, name, table, comment):
    T = 600
    plen = 8
    # Fixed balanced pattern (same for all variants; only the table differs).
    # Each signal appears twice per 8-tick cycle.
    base = [(0,0),(0,1),(1,0),(1,1)] * 2
    # Deterministic shuffle with a fixed seed (not rng, so pattern is identical).
    prng = random.Random(42)
    prng.shuffle(base)
    pat = []
    for f1,f2 in base:
        pat += [f1,f2]
    ints = [T, plen] + pat + table
    assert len(ints) == 2 + 16 + 12 == 30, len(ints)
    with open(os.path.join(OUT, name + '.txt'), 'w') as f:
        f.write(f"# SHIFT variant {name}. {comment}\n")
        f.write('\n'.join(map(str, ints)) + '\n')

rng = random.Random(20260928)
for i in range(6):
    gen(rng, f'd2_h{i}', HOME_TABLE, 'home regime')
for i in range(6):
    gen(rng, f'd2_s{i}', SHIFT_TABLE, 'SHIFTED: signal meanings inverted for (0,0) and (1,1)')
print('wrote 12 variants')
