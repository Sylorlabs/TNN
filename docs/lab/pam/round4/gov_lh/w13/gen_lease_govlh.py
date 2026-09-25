#!/usr/bin/env python3
"""gen_lease_govlh.py — W13 GOV-LH extended lease streams (PREREG_W13_GOVLH.md).

Deterministic (zero RNG). Extends the gen_lease.py family to 10x/100x scale
plus an adversarial colluding-pair family.

Families (granted_at = stream ordinal; row format identical to gen_lease.py):
  BASE-N: N genuine (C-pass rows[i mod 910]; channel i%3; tag i//2) +
          N//200 unique-tag falses (the 30 frozen wrongs cycled, then B rows
          cycled; tag 1000000+j — unique, never corroborated).
          Interleave: unique false #j at stream positions with pos%201==200.
  ADV-N:  BASE-N + N//200 colluding false pairs. Pair j: F1 at ordinal g_j,
          F2 at g_j+1 (first free stream positions with pos%2000 in
          {1000,1001}); shared tag 2000000+j; channels g_j%3, (g_j+1)%3
          (differ); |dgranted|=1 <= 3. Two-channel adversary timed so F2 is
          genuinely within its first window when F1 is checked, and F1's
          renewal is fresh state when F2 is checked.

Usage: gen_lease_govlh.py {base,adv} {1x,10x,100x}   (1x = N=10000, extra sanity leg; NOT in the frozen §7 battery)
Writes w13_stream_{base,adv}_{10x,100x}.txt next to this script.
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"

def passes_m1(conf, mrg, s, a):
    return conf >= 705 and mrg >= 3588

def main():
    fam, scale = sys.argv[1], sys.argv[2]
    assert fam in ("base", "adv") and scale in ("1x", "10x", "100x")
    N = {"1x": 10000, "10x": 100000, "100x": 1000000}[scale]

    c_pass, wrongs, b_rows = [], [], []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        k = f[0]
        if k == "C":
            cf, mg, s, a = int(f[1]), int(f[2]), int(f[3]), int(f[4])
            if passes_m1(cf, mg, s, a):
                c_pass.append((cf, mg, s, a))
        elif k == "W":
            wrongs.append((int(f[1]), int(f[2]), 1, 1))
        elif k == "P":
            wrongs.append((int(f[2]), int(f[3]), 1, 1))
        elif k == "B":
            b_rows.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
    assert len(c_pass) == 910, len(c_pass)
    assert len(wrongs) == 30
    assert len(b_rows) >= 20

    gen, ufs, pairs = [], [], []
    for i in range(N):
        cf, mg, s, a = c_pass[i % 910]
        gen.append([i, "G", i % 3, i // 2, cf, mg, s, a])
    nuniq = N // 200
    fpool = wrongs + b_rows
    for j in range(nuniq):
        cf, mg, s, a = fpool[j % len(fpool)]
        lid = N + j
        ufs.append([lid, "F", lid % 3, 1000000 + j, cf, mg, s, a])
    npairs = N // 200 if fam == "adv" else 0
    for j in range(npairs):
        cf, mg, s, a = fpool[j % len(fpool)]
        lid1 = N + nuniq + 2 * j
        lid2 = lid1 + 1
        # channels assigned at placement (need ordinal g)
        pairs.append(([lid1, "F", None, 2000000 + j, cf, mg, s, a],
                      [lid2, "F", None, 2000000 + j, cf, mg, s, a]))

    stream = []
    gi = ui = pi = 0
    pos = 0
    while gi < N or ui < nuniq or pi < npairs:
        if pi < npairs and pos % 2000 == 1000:
            e1, e2 = pairs[pi]
            g = pos
            e1[2] = g % 3
            e2[2] = (g + 1) % 3
            assert e1[2] != e2[2]
            stream.append(e1)
            stream.append(e2)
            pi += 1
            pos += 2
        elif ui < nuniq and pos % 201 == 200:
            stream.append(ufs[ui]); ui += 1; pos += 1
        elif gi < N:
            stream.append(gen[gi]); gi += 1; pos += 1
        else:
            pos += 1
    assert gi == N and ui == nuniq and pi == npairs
    assert sum(1 for e in stream if e[1] == "G") == N
    assert sum(1 for e in stream if e[1] == "F") == nuniq + 2 * npairs
    # tag pairing check: genuine tags pair, unique falses unique, pair tags pair
    from collections import Counter
    tc = Counter(e[3] for e in stream)
    assert all(v == 2 for t, v in tc.items() if t < 1000000), "genuine tag unpaired"
    assert all(v == 1 for t, v in tc.items() if 1000000 <= t < 2000000), "unique false tag dup"
    assert all(v == 2 for t, v in tc.items() if t >= 2000000), "pair tag unpaired"

    out = os.path.join(HERE, "w13_stream_%s_%s.txt" % (fam, scale))
    with open(out, "w") as fh:
        for e in stream:
            fh.write("%d|%s|%d|%d|%d|%d|%d|%d\n" % tuple(e))
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("%s: %d events sha256=%s" % (os.path.basename(out), len(stream), h))

if __name__ == "__main__":
    main()
