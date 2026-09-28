#!/usr/bin/env python3
"""Generate SEALED held-out variants (D2/D3-style, different shifts).
D2 held-out (d2_hs0..d2_hs3): ROTATION shift (not inversion).
  Home: s=0->RETREAT, s=3->APPROACH.
  Held-out shift: rotate actions (APPROACH->HOLD->RETREAT->APPROACH).
  Table: s=0: [0,+10,0] (HOLD best, was RETREAT)
         s=1: [0,0,+5]?? Let's define clearly.
D3 held-out (d3_hs0..d3_hs3): TOOL_1 degrades (not TOOL_0), faster schedule.
These are SEALED: committed before the fix is implemented. D must handle them
without having seen them.
"""
import random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'worlds', 'sealed')
os.makedirs(OUT, exist_ok=True)

# D2 held-out: ROTATION. Home table:
#   s=0: [-10,0,+10] (RETREAT). s=3: [+10,0,-10] (APPROACH).
# Rotated: s=0: [0,+10,-10]?? Let me define a clean rotation.
# Rotation: new_r(a) = old_r((a+1)%3) for the affected rows.
# s=0 home: [-10,0,10]. Rotated: [0,10,-10] (HOLD best).
# s=3 home: [10,0,-10]. Rotated: [0,-10,10] (RETREAT best? No...)
# Actually, let's do: s=0: [0,10,-10] (HOLD +10), s=3: [-10,0,10] (RETREAT +10).
# This is different from inversion (which was [10,0,-10] and [-10,0,10]).
ROT_TABLE = [0,10,-10,  0,5,0,  0,5,0,  -10,0,10]

def gen_d2(name):
    T = 600
    plen = 8
    prng = random.Random(42)
    base = [(0,0),(0,1),(1,0),(1,1)] * 2
    prng.shuffle(base)
    pat = []
    for f1,f2 in base:
        pat += [f1,f2]
    ints = [T, plen] + pat + ROT_TABLE
    with open(os.path.join(OUT, name + '.txt'), 'w') as f:
        f.write(f"# SEALED held-out SHIFT variant {name}. ROTATION shift.\n")
        f.write('\n'.join(map(str, ints)) + '\n')

# D3 held-out: TOOL_2 degrades to 10 by tick 200 (faster, different tool).
BASE = [100,60,40,20,  20,100,60,40,  40,20,100,60]

def gen_d3(name):
    T = 600
    tplen = 9
    prng = random.Random(99)
    base = [0,1,2] * 3
    prng.shuffle(base)
    breaks = [2, 0, 200, 10]  # tool 2, start 0, end 200, cond_end 10
    ints = [T, tplen] + base + BASE + [1] + breaks
    with open(os.path.join(OUT, name + '.txt'), 'w') as f:
        f.write(f"# SEALED held-out TOOL variant {name}. TOOL_2 degrades.\n")
        f.write('\n'.join(map(str, ints)) + '\n')

for i in range(4):
    gen_d2(f'd2_hs{i}')
    gen_d3(f'd3_hs{i}')

# Log SHA-256 of all sealed files
import hashlib
shas = {}
for f in sorted(os.listdir(OUT)):
    if f.endswith('.txt'):
        h = hashlib.sha256()
        with open(os.path.join(OUT, f), 'rb') as fh:
            h.update(fh.read())
        shas[f] = h.hexdigest()

with open(os.path.join(OUT, 'SHA_LOG.txt'), 'w') as f:
    f.write("# Sealed held-out family SHA-256 log. Committed BEFORE the fix.\n")
    f.write("# Generated 2026-09-27. Do not modify.\n")
    for fn, sha in sorted(shas.items()):
        f.write(f"{sha}  {fn}\n")

print(f"Sealed {len(shas)} files.")
for fn, sha in sorted(shas.items()):
    print(f"  {fn}: {sha[:16]}...")
