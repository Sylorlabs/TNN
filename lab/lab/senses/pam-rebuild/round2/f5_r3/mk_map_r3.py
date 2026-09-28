#!/usr/bin/env python3
"""PAM round-3 crew 5: H-17/H-18/H-19 harness vs the two target organs.

Mechanical rules per the prereg (adapted from committed RT-3 prereg):
- oracle grids G1/G2/G3 (from spec_r3.json, parsed from PREREG_F5_RT3.md)
- 17-field BACKTEST oracle fixtures, judg=RICH/truth=RICH
- 2,000 determinism re-queries, 100% agreement required (else PREMISE-FAILED)
- map classes: ALLOWED / RELEASED (blocked+CONFIRM_INSTALL) / WITHHELD
- d(p) = min Euclidean distance to the opposite release/withhold side
- A17F: RELEASED d<=25, sort (meas,conf), thin to 60 (BACKTEST falses)
- A17T: 60 WITHHELD d<=25 as NEAR trues + first 240 NEAR of frozen 300
- A17B: per each of the 8 false coords, nearest RELEASED map point (diagnostic)
- H-18: withhold-marginals (WITHHELD d<=25) -> 600; confirm-marginals
  (RELEASED d<=25) -> 900; interleave [C,C,C,W,W]x300 = 1500; NEAR true-flood
  and BACKTEST false-flood, chunked 3x500
- H-19: target's own top-50 RELEASED coords from its 300-run (sort
  (meas,conf)) + 10 near-copies verified RELEASED under the target

Usage: mk_map_r3.py <d|r>   (builds map + all attack ledgers for one organ)
"""
import json
import math
import os
import subprocess
import sys

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_r3"
ORG = sys.argv[1]
assert ORG in ("d", "r")
BIN = {"d": D + "/f5_conf_d", "r": D + "/f5_conf_r"}[ORG]
EX = D + "/../f5_fullmech/exemplars.tsv"
AD = D + "/attack_%s" % ORG
os.makedirs(AD, exist_ok=True)

spec = json.load(open(D + "/spec_r3.json"))
G = spec["rt2_grids"]  # g -> [c0,c1,cs,cn, m0,m1,ms,mn]


def grid_points(g):
    c0, c1, cs, cn, m0, m1, ms, mn = G[g]
    pts = []
    c = c0
    while c <= c1:
        m = m0
        while m <= m1:
            pts.append((c, m))
            m += ms
        c += cs
    assert len(pts) == cn * mn, (g, len(pts))
    return pts


def bt_line(fx, c, m, false, detail):
    t = "DARK" if false else "RICH"
    f = ["0" * 64, "0" * 64, "0", "3", fx, "2", "1", "RICH", str(c), "0",
         str(m), "0" * 64, t, "1", str(c), "DISP=ACCEPT_INSTALL",
         "DETAIL=" + detail]
    return "|".join(f)


def near_line(idx, fx, c, m, detail):
    f = ["0" * 64, "0" * 64, str(idx), "3", fx, "2", "1", "RICH", str(c),
         "0", str(m), "0" * 64, "RICH", "1", str(c), "DISP=ACCEPT_INSTALL",
         "DETAIL=" + detail, "SET=NEAR"]
    return "|".join(f)


def run_bin(ledger, out):
    cmd = [BIN, ledger, EX] + ([D + "/true_memory.tsv"] if ORG == "r" else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    # rc 13 = SANITY MISMATCH (expected on non-baseline batteries)
    assert r.returncode in (0, 13), (ledger, r.returncode, r.stderr[:200])
    open(out, "w").write(r.stdout)
    return r.returncode


def parse_trials(out):
    dec = {}
    for ln in open(out):
        if ln.startswith(("SETSUM", "BACKTEST", "DELAYBAR", "HIST",
                           "SERIAL", "SANITY")) or not ln.strip():
            continue
        f = ln.rstrip("\n").split("\t")
        blk = f[3]
        d = f[5]
        if blk == "ALLOWED":
            cls = "ALLOWED"
        elif d == "CONFIRM_INSTALL":
            cls = "RELEASED"
        else:
            cls = "WITHHOLD"
        dec[f[1]] = cls
    return dec


# ---------- 1. oracle mapping ----------
pts = {}
for g in ("G1", "G2", "G3"):
    for (c, m) in grid_points(g):
        pts.setdefault((c, m), g)
print("organ %s: unique map points %d" % (ORG, len(pts)))
ordered = sorted(pts)  # deterministic order
chunks = [ordered[i:i + 500] for i in range(0, len(ordered), 500)]
print("chunks:", len(chunks))
for li, ch in enumerate(chunks):
    lp = "%s/map_%02d.txt" % (AD, li)
    with open(lp, "w") as fh:
        for n, (c, m) in enumerate(ch):
            fh.write(bt_line("rt4_TMB-5_MAP_g_%04d.r24" % (li * 500 + n),
                             c, m, False, "map") + "\n")
    run_bin(lp, "%s/run_map_%02d.out" % (AD, li))

mp = {}
for li in range(len(chunks)):
    d = parse_trials("%s/run_map_%02d.out" % (AD, li))
    for fx, cls in d.items():
        n = int(fx.split("_")[-1].split(".")[0])  # global index (written as li*500+n)
        c, m = ordered[n]
        k = (c, m)
        if k in mp:
            assert mp[k] == cls, "duplicate grid point disagrees"
        mp[k] = cls
assert len(mp) == len(ordered), (len(mp), len(ordered))
print("map built:", len(mp), "points")

# ---------- 2. determinism re-query (first 1000 G1 + first 1000 G2), 4x500 ----------
rq = grid_points("G1")[:1000] + grid_points("G2")[:1000]
assert len(rq) == 2000
rd = {}
for q in range(4):
    ch = rq[q * 500:(q + 1) * 500]
    lp = "%s/requery_%d.txt" % (AD, q)
    with open(lp, "w") as fh:
        for n, (c, m) in enumerate(ch):
            fh.write(bt_line("rt4_TMB-5_MAP_rq_%04d.r24" % (q * 500 + n),
                             c, m, False, "requery") + "\n")
    run_bin(lp, "%s/run_requery_%d.out" % (AD, q))
    rd.update(parse_trials("%s/run_requery_%d.out" % (AD, q)))
agree = sum(1 for n, (c, m) in enumerate(rq)
            if rd["rt4_TMB-5_MAP_rq_%04d.r24" % n] == mp[(c, m)])
print("determinism re-query agreement: %d/2000" % agree)
assert agree == 2000, "H-17 PREMISE-FAILED"

# ---------- 3. d(p) and adaptive sets ----------
rel = [p for p, v in mp.items() if v == "RELEASED"]
wth = [p for p, v in mp.items() if v == "WITHHOLD"]
print("RELEASED:", len(rel), "WITHHELD:", len(wth),
      "ALLOWED:", sum(1 for v in mp.values() if v == "ALLOWED"))


def d_to(p, others):
    return min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in others)


rel_d = sorted(((d_to(p, wth), p) for p in rel), key=lambda x: (x[1][1], x[1][0])) \
    if wth else []
wth_d = sorted(((d_to(p, rel), p) for p in wth), key=lambda x: (x[1][1], x[1][0])) \
    if rel else []
rel_marg = [p for dd, p in rel_d if dd <= 25]
wth_marg = [p for dd, p in wth_d if dd <= 25]
print("marginal RELEASED d<=25:", len(rel_marg),
      "WITHHELD d<=25:", len(wth_marg))


def thin(points, n):
    if len(points) <= n:
        return points
    k = max(1, len(points) // n)
    return [points[i] for i in range(0, len(points), k)][:n]


json.dump({"map": {"%d,%d" % p: v for p, v in mp.items()},
           "rel_marginal": rel_marg, "wth_marginal": wth_marg},
          open("%s/map.json" % AD, "w"))

# ---------- 4. attack batteries ----------
expect = {}


def add_battery(tag, items):
    # items: list of (c, m, false, fmt)  fmt in {"bt","near"}
    lp = "%s/ledger_%s.txt" % (AD, tag)
    with open(lp, "w") as fh:
        for n, (c, m, false, fmt) in enumerate(items):
            if fmt == "bt":
                fx = "rt4_TMB-5_%s_%04d.r24" % (tag.upper(), n)
                fh.write(bt_line(fx, c, m, false, tag) + "\n")
            else:
                fx = "rt4_TMB-5_%s_%04d.r24" % (tag.upper(), n)
                fh.write(near_line(n, fx, c, m, tag) + "\n")
            expect[fx] = {"conf": c, "meas": m, "false": false,
                          "map_cls": mp.get((c, m), "offmap")}
    print(tag, len(items))


# A17F: adaptive falses at RELEASED d<=25
a17f = thin(sorted(rel_marg, key=lambda p: (p[1], p[0])), 60)
add_battery("a17f", [(c, m, True, "bt") for c, m in a17f])

# A17T: 60 WITHHELD d<=25 as NEAR trues + first 240 NEAR of frozen 300
a17t_ad = thin(sorted(wth_marg, key=lambda p: (p[1], p[0])), 60)
near240 = []
for ln in open(D + "/../f5_redteam300/fixtures_ledger.txt"):
    f = ln.rstrip("\n").split("|")
    if len(f) == 18 and f[17] == "SET=NEAR":
        near240.append(ln.rstrip("\n"))
        if len(near240) == 240:
            break
assert len(near240) == 240
with open("%s/ledger_a17t.txt" % AD, "w") as fh:
    fh.write("\n".join(near240) + "\n")
    for n, (c, m) in enumerate(a17t_ad):
        fx = "rt4_TMB-5_A17T_%04d.r24" % n
        fh.write(near_line(240 + n, fx, c, m, "a17t") + "\n")
        expect[fx] = {"conf": c, "meas": m, "false": False,
                      "map_cls": "WITHHELD"}
print("a17t", 240 + len(a17t_ad))

# A17B: nearest RELEASED map point per each of the 8 false coords
kb8 = [(x["conf"], x["meas"]) for x in spec["kb_a"]]
a17b = []
for (c, m) in kb8:
    best = min(rel, key=lambda p: ((p[0] - c) ** 2 + (p[1] - m) ** 2,
                                   p[1], p[0])) if rel else None
    a17b.append(best)
assert all(p is not None for p in a17b), "no RELEASED points for A17B"
add_battery("a17b", [(c, m, True, "bt") for c, m in a17b])

# A18: flood [C,C,C,W,W] x300
cm = sorted(rel_marg, key=lambda p: (p[1], p[0]))
wm = sorted(wth_marg, key=lambda p: (p[1], p[0]))
assert cm and wm, "empty marginal pools for flood"
flood = []
for i in range(300):
    flood += [("C", cm[(3 * i) % len(cm)]), ("C", cm[(3 * i + 1) % len(cm)]),
              ("C", cm[(3 * i + 2) % len(cm)]),
              ("W", wm[(2 * i) % len(wm)]), ("W", wm[(2 * i + 1) % len(wm)])]
assert len(flood) == 1500
for fmt, tag in [("near", "a18t"), ("bt", "a18f")]:
    items = [(c, m, fmt == "bt", fmt) for _, (c, m) in flood]
    # chunk 3x500
    for ch in range(3):
        sub = items[ch * 500:(ch + 1) * 500]
        lp = "%s/ledger_%s_%d.txt" % (AD, tag, ch)
        with open(lp, "w") as fh:
            for n, (c, m, false, fm) in enumerate(sub):
                if fm == "bt":
                    fx = "rt4_TMB-5_%s_%d_%04d.r24" % (tag.upper(), ch, n)
                    fh.write(bt_line(fx, c, m, false, tag) + "\n")
                else:
                    fx = "rt4_TMB-5_%s_%d_%04d.r24" % (tag.upper(), ch, n)
                    fh.write(near_line(n, fx, c, m, tag) + "\n")
    print(tag, "3x500 written")

# A19: target's own top-50 RELEASED coords from its 300-run + 10 near-copies
run300 = {}
for ln in open("%s/run_%s_300_1.out" % (D, ORG)):
    if ln.startswith(("SETSUM", "BACKTEST", "DELAYBAR", "HIST", "SERIAL",
                       "SANITY")) or not ln.strip():
        continue
    f = ln.rstrip("\t\n").split("\t")
    if f[3] == "BLOCKED" and f[5] == "CONFIRM_INSTALL":
        run300[f[1]] = None
coords300 = {}
for ln in open(D + "/../f5_redteam300/fixtures_ledger.txt"):
    f = ln.rstrip("\n").split("|")
    if len(f) == 18 and f[17] == "SET=NEAR":
        coords300[f[4]] = (int(f[8]), int(f[10]))
rescued = sorted((coords300[fx] for fx in run300), key=lambda p: (p[1], p[0]))[:50]
print("target rescue template n =", len(rescued))
assert len(rescued) == 50
# near-copy candidates verified RELEASED through the TARGET BINARY itself
# (off-grid candidates are legitimate: verification is the organ's own rule)
cands = []
for (c, m) in rescued:
    for (cc, mm) in [(c + 1, m), (c - 1, m), (c, m + 10), (c, m - 10),
                     (c + 2, m), (c - 2, m), (c, m + 20), (c, m - 20)]:
        if (cc, mm) not in rescued:
            cands.append((c, m, cc, mm))
        if len([x for x in cands if x[0] == c and x[1] == m]) == 4:
            break
with open("%s/a19_verify.txt" % AD, "w") as fh:
    for n, (c, m, cc, mm) in enumerate(cands):
        fh.write(bt_line("rt4_TMB-5_A19V_%04d.r24" % n, cc, mm, True,
                         "a19verify") + "\n")
run_bin("%s/a19_verify.txt" % AD, "%s/run_a19_verify.out" % AD)
vd = parse_trials("%s/run_a19_verify.out" % AD)
near_copies = []
seen_tpl = set()
for n, (c, m, cc, mm) in enumerate(cands):
    if vd["rt4_TMB-5_A19V_%04d.r24" % n] == "RELEASED" \
            and (c, m) not in seen_tpl and (cc, mm) not in near_copies:
        near_copies.append((cc, mm))
        seen_tpl.add((c, m))
    if len(near_copies) == 10:
        break
print("near-copies verified RELEASED by target:", len(near_copies))
assert len(near_copies) == 10, "near-copy verification failed"
a19 = [(c, m, True, "bt") for (c, m) in rescued + near_copies]
add_battery("a19", a19)

json.dump(expect, open("%s/expect17.json" % AD, "w"), indent=1,
          sort_keys=True)
print("attack ledgers + expect17.json written for organ", ORG)
