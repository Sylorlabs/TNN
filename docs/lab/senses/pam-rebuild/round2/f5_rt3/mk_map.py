#!/usr/bin/env python3
"""RT-3 mapping ledger generator (H-PAM-17 oracle queries).

Deterministic grid enumeration, zero RNG. Each fixture is the 17-field
backtest-style format (no SET= field -> BACKTEST set); judg=RICH,
truth=RICH (truth never enters the decision path). Fixture names carry
the grid id so map outputs can be joined back to coordinates.

Grids (preregistered):
  G1: conf 540..880 step 2 (171) x meas 2400..2900 step 10 (51) = 8721
  G2: conf 690..730 step 2 (21)  x meas 600..4700 step 20 (206) = 4326
  G3: conf 400..1000 step 50 (13) x meas 400..4800 step 200 (23) = 299
Total 13,346 oracle queries <= 20,000 budget. Ledgers chunked to <=500
fixtures (binary's 200KB ledger buffer).
"""
import json

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt3"

def frange(a, b, s):
    v, out = a, []
    while v <= b:
        out.append(v)
        v += s
    return out

GRIDS = {
    "g1": (frange(540, 880, 2), frange(2400, 2900, 10)),
    "g2": (frange(690, 730, 2), frange(600, 4700, 20)),
    "g3": (frange(400, 1000, 50), frange(400, 4800, 200)),
}

def line(gid, n, c, m):
    fx = "rt4_TMB-5_MAP_%s_%05d.r24" % (gid, n)
    f = ["0" * 64, "0" * 64, "0", "3", fx, "2", "1", "RICH", str(c), "0",
         str(m), "0" * 64, "RICH", "1", str(c), "DISP=ACCEPT_INSTALL",
         "DETAIL=rt3_map_" + gid]
    return "|".join(f), (fx, c, m)

index = {}   # ledger path -> list of (fx, c, m)
allpts = []  # (gid, fx, c, m) in global order
for gid, (cs, ms) in GRIDS.items():
    n = 0
    for m in ms:
        for c in cs:
            l, meta = line(gid, n, c, m)
            allpts.append((gid,) + meta + (l,))
            n += 1
    print(gid, "points:", n)

# chunk into <=500-fixture ledgers, keeping grid order
CH = 500
ledgers = []
for i in range(0, len(allpts), CH):
    chunk = allpts[i:i + CH]
    p = "%s/map_%02d.txt" % (D, len(ledgers))
    open(p, "w").write("\n".join(l for _, _, _, _, l in chunk) + "\n")
    ledgers.append(p)
    for gid, fx, c, m, _ in chunk:
        index[fx] = {"grid": gid, "conf": c, "meas": m, "ledger": p}

json.dump({"ledgers": ledgers,
           "n_points": len(allpts),
           "n_ledgers": len(ledgers)},
          open(D + "/map_index.json", "w"), indent=1)
json.dump(index, open(D + "/map_points.json", "w"), indent=1)
print("total points:", len(allpts), "ledgers:", len(ledgers))
assert len(allpts) <= 20000
