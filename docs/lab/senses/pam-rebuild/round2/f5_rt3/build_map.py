#!/usr/bin/env python3
"""RT-3 map builder: parse the 27 mapping runs into the observed map.

The map is built ONLY from observed binary decisions (black-box oracle).
Outputs map.json: (conf,meas) -> {blocked, decision}. Also reports the
post-hoc map-vs-analytic agreement (analysis, not a scorer assertion).
"""
import json

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt3"
pts = json.load(open(D + "/map_points.json"))
idx = json.load(open(D + "/map_index.json"))

mp = {}
n_trials = 0
dup_agree = 0
dup_total = 0
for li in range(idx["n_ledgers"]):
    for l in open("%s/run_map_%02d.out" % (D, li)):
        if l.startswith(("SETSUM", "BACKTEST", "DELAYBAR", "HIST", "SERIAL",
                         "SANITY")):
            continue
        f = l.rstrip("\n").split("\t")
        fx, blk, dec = f[1], f[3], f[5]
        q = pts[fx]
        k = "%d,%d" % (q["conf"], q["meas"])
        v = {"blocked": blk == "BLOCKED", "decision": dec}
        if k in mp:
            dup_total += 1
            assert mp[k] == v, "duplicate grid point disagrees: " + k
            dup_agree += 1
        mp[k] = v
        n_trials += 1

print("map points:", len(mp), "trials parsed:", n_trials)
print("duplicate grid points (cross-grid re-queries):", dup_total,
      "all agreeing:", dup_agree == dup_total)
assert n_trials == idx["n_points"] == 13346
assert dup_agree == dup_total

# post-hoc: agreement with the analytic geometry (frozen consts)
EX = [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632),
      (713, 2627)]

def ablocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EX)

def arep(c, m):
    n = 0
    for dc, dm in [(-10, -200), (0, 0), (10, 200)]:
        if any(abs(c + dc - ec) <= 130 and abs(m + dm - em) <= 950
               for ec, em in EX):
            n += 1
    return n

def adec(c, m):
    if not ablocked(c, m):
        return "ALLOWED"
    return "WITHHOLD" if arep(c, m) >= 2 else "CONFIRM_INSTALL"

# decision word used by the binary for allowed percepts is "-" in field 6;
# normalize: unblocked -> ALLOWED
agree = 0
dis = []
for k, v in mp.items():
    c, m = (int(x) for x in k.split(","))
    exp = adec(c, m)
    got = v["decision"]
    if got == "-":
        got = "ALLOWED"
    if got == exp and (v["blocked"] == ablocked(c, m)):
        agree += 1
    else:
        dis.append((k, got, exp))
print("map-vs-analytic agreement: %d/%d = %.4f" % (agree, len(mp),
                                                   agree / len(mp)))
if dis:
    print("disagreements (first 10):", dis[:10])

json.dump(mp, open(D + "/map.json", "w"))
print("wrote map.json")
