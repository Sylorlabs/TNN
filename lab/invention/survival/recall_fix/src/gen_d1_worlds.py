#!/usr/bin/env python3
"""Generate 12 TIDELOCK v2 variants (45 ints each), disjoint from Experiment 1.
Home (d1_h0..d1_h5): default knobs.
Shift A (d1_a0..d1_a2): storm-invert — storms hit OUTSIDE the zone (10/tick),
  inside is safe. Fleeing (home h2) is lethal; staying is correct.
Shift B (d1_b0..d1_b2): move-rot — every LEFT/RIGHT move costs 6 energy.
  Foraging (home h1) is lethal; sitting and eating drifted motes is correct.
Knob order: basal_in basal_out storm_dmg combine_cost eat_near eat_deep
             zone_lo zone_hi eat_cost zone_cost storm_out move_cost
"""
import random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'worlds')
os.makedirs(OUT, exist_ok=True)

# Exp1 first-33 vectors (for disjointness check)
exp1 = os.path.join(os.path.dirname(__file__), '..', '..', 'exp1',
                    'docs', 'lab', 'invention', 'survival', 'worlds')
exp1_vecs = set()
for f in sorted(os.listdir(exp1)):
    if f.startswith('v') and f.endswith('.txt'):
        ints = tuple(int(l) for l in open(os.path.join(exp1, f))
                     if l.strip() and not l.startswith('#'))
        exp1_vecs.add(ints[:33])

def gen(rng, name, knobs, comment, in_zone=False):
    # 33 base ints (Exp1 layout)
    void_a = rng.choice([9, 10, 11])
    if in_zone:
        # force zone occupancy: start and motes inside 6..8 (zone 6..17, left of void)
        start = rng.choice([6, 7, 8])
    else:
        start = rng.choice([2, 3, 4])
    storms = [rng.choice([120, 140, 160, 170]) + 200*i for i in range(3)]
    # Ensure at least 2 crystals on the left side (cells 0..void_a-1) for P/homesteader.
    crystals = rng.sample([c for c in range(void_a) if c not in (void_a, void_a+1)], 2)
    remaining = [c for c in range(24) if c not in crystals and c not in (void_a, void_a+1)]
    crystals += rng.sample(remaining, 2)
    rng.shuffle(crystals)
    near, used = [], set()
    while len(near) < 18:
        if in_zone:
            p = rng.randrange(4, 12)
        else:
            p = rng.randrange(0, 10)
        if p in used or p in (void_a, void_a+1): continue
        used.add(p)
        near += [p, rng.choice([-2,-1,1,2]), p]
    deep = []
    while len(deep) < 6:
        p = rng.randrange(12, 24)
        if p in used or p in (void_a, void_a+1): continue
        used.add(p)
        deep += [p, rng.choice([-2,-1,1,2]), p]
    ints = [void_a, start] + storms + crystals + near + deep
    assert len(ints) == 33, len(ints)
    assert tuple(ints) not in exp1_vecs, f"{name} collides with Exp1!"
    exp1_vecs.add(tuple(ints))
    ints += knobs
    assert len(ints) == 45, len(ints)
    with open(os.path.join(OUT, name + '.txt'), 'w') as f:
        f.write(f"# TIDELOCK v2 variant {name}. {comment}\n")
        f.write('\n'.join(map(str, ints)) + '\n')

HOME = [1, 1, 4, 0, 30, 40, 6, 17, 0, 0, 0, 0]
SH_A = [1, 1, 0, 0, 30, 40, 6, 17, 0, 0, 10, 0]   # storm-invert
SH_B = [1, 1, 4, 0, 30, 40, 6, 17, 0, 0, 0, 6]    # move-rot

rng = random.Random(20260927)
for i in range(6):
    gen(rng, f'd1_h{i}', HOME, 'home regime, default knobs')
for i in range(3):
    gen(rng, f'd1_a{i}', SH_A, 'SHIFT A (storm-invert): storms hit outside the zone', in_zone=True)
for i in range(3):
    gen(rng, f'd1_b{i}', SH_B, 'SHIFT B (move-rot): every move costs 6 energy')
print('wrote 12 variants')
