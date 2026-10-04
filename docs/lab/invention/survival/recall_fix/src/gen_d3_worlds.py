#!/usr/bin/env python3
"""Generate 8 TOOL variants.
Home (d3_h0..d3_h3): no degradation.
Shifted (d3_s0..d3_s3): TOOL_0 degrades to 0 by tick 300 (silent).
Format: [T, tplen, pattern[tplen], base[12], nbrk, (tool,t_start,t_end,cond_end) x nbrk]
Base table (task x tool):
  Task 0: [100, 60, 40, 20]
  Task 1: [20, 100, 60, 40]
  Task 2: [40, 20, 100, 60]
"""
import random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'worlds')
os.makedirs(OUT, exist_ok=True)

BASE = [100,60,40,20,  20,100,60,40,  40,20,100,60]

def gen(name, breaks, comment):
    T = 600
    tplen = 9
    # Fixed pattern: each task 3 times per 9-tick cycle.
    import random as r
    prng = r.Random(99)
    base = [0,1,2] * 3
    prng.shuffle(base)
    ints = [T, tplen] + base + BASE + [len(breaks)//4] + breaks
    assert len(ints) == 3 + 9 + 12 + len(breaks), len(ints)
    with open(os.path.join(OUT, name + '.txt'), 'w') as f:
        f.write(f"# TOOL variant {name}. {comment}\n")
        f.write('\n'.join(map(str, ints)) + '\n')

for i in range(4):
    gen(f'd3_h{i}', [], 'home regime: tools do not degrade')
for i in range(4):
    gen(f'd3_s{i}', [0, 0, 300, 0], 'SHIFTED: TOOL_0 degrades to 0 by tick 300 (silent)')
print('wrote 8 variants')
