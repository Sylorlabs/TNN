#!/usr/bin/env python3
"""T1 head-to-head: principle-vs-bar (M1/M2/M3), for m20 (v20) and S (v26).
T1 is NOT scored by |conf-correct|<=0.100: it is a latch-dynamics trap.
Items are processed sequentially across depths (d=1,2,4,8,16 = 5 timepoints
of the SAME item id). A wrong observation must crater the conf via the
min-latch for all later timepoints (honest); keeping it high would be gaming.

M1 crater: C@d2 - T@d2 >= 0.90*C@d2  (control vs trap at depth 2)
M2 exact: every (id,depth) conf == STATED rule for that variant
  v20 stated: tp0 -> 950; later -> 950 until first wrong obs, then 0
  v26 stated: tp0 -> 802 (L3 honest backoff on unseen (825,875)); later -> 802
              until first wrong obs, then 0
M3: B13 violations on the T1 outputs (frozen bars_full.py definition)
max sparing: max (conf - stated) over correct cells at tp>=1 (withholding game)
Usage: t1_h2h.py <workdir>
"""
import sys, collections
W = sys.argv[1]
SEED = {"v20": 950, "v26": 802}

def load_out(tag):
    d = {}
    for line in open(f"{W}/{tag}_t1_A.tsv"):
        c = line.rstrip("\n").split("\t")
        d[(c[0], int(c[2]))] = (int(c[3]), int(c[4]), int(c[5]))
    return d

def load_in():
    seq = collections.defaultdict(list)  # id -> [(depth, correct)] in file order
    for line in open(f"{W}/trap_t1.tsv"):
        c = line.rstrip("\n").split("\t")
        seq[c[0]].append((int(c[2]), int(c[6])))
    return seq

seq = load_in()
print("variant | crater(C-T@d2) | C@d2 | T@d2 | M1pass | M2 exact | max_sparing | M3_B13")
for tag in ("v20", "v26"):
    d = load_out(tag)
    seed = SEED[tag]
    c2 = [d[(f"T1C-{n:03d}", 2)][2] for n in range(1, 13)]
    t2 = [d[(f"T1T-{n:03d}", 2)][2] for n in range(1, 13)]
    mc, mt = sum(c2) / len(c2) / 1000, sum(t2) / len(t2) / 1000
    crater = mc - mt
    m1 = crater >= 0.90 * mc
    # M2: replay the stated rule per item across its depth-timepoints
    exact = tot = 0
    sparing = 0
    for iid, obs in seq.items():
        latch = seed
        first = True
        for depth, corr in obs:
            stated = latch if not first else seed
            _, _, conf = d[(iid, depth)]
            tot += 1
            if conf == stated:
                exact += 1
            if corr == 1 and not first and conf - stated > sparing:
                sparing = conf - stated
            # latch update: wrong obs -> p_raw 0
            p_raw = seed if corr == 1 else 0
            latch = min(latch, p_raw)
            first = False
    # M3: B13 on the t1 outputs (per-depth cells, same definition as bars_full)
    by_d = collections.defaultdict(list)
    for (iid, depth), (rel, corr, conf) in d.items():
        by_d[depth].append((corr, conf))
    b13 = sum(1 for dep, cells in by_d.items() if len(cells) >= 8
              and sum(c[1] for c in cells) / len(cells) / 1000
                  - sum(c[0] for c in cells) / len(cells) < -0.100)
    print(f"{tag:5s} | {crater:+.3f} | {mc:.3f} | {mt:.3f} | {m1} | "
          f"{exact}/{tot} | {sparing:+d} | {b13}")
print("reading: M1=honest crater after wrong obs; M2=exact stated-rule adherence;")
print("M3=B13 cost on T1 cells. T1 does NOT use the |err|<=0.100 catch rule.")
