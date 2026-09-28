#!/usr/bin/env python3
"""H5B fidelity gates FC1-FC7 (PREREG_H5B.md G4, ITEM_ENCODING_SPEC_CEILING.md G5).

FC1/FC2/FC3: independent argmax re-derivation (no harness).
FC4/FC5/FC6/FC7: run the H5B harness binary (bound prototype in FC7).
Usage: fidelity.py <battery.jsonl> <harness-bin> <config-dir> <workdir>
Exit 0 iff all gates pass.
"""
import json
import os
import re
import subprocess
import sys

BAT, BIN, CFGDIR, WORK = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(WORK, exist_ok=True)
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" " + detail if detail else ""))
    if not cond:
        fails.append(name)


def argmax(item, n_ev=None):
    hyps = [h["id"] for h in item["input"]["hypotheses"]]
    score = {h: 0 for h in hyps}
    evs = item["input"]["evidence"] if n_ev is None else item["input"]["evidence"][:n_ev]
    for e in evs:
        for h, w in e["supports"].items():
            score[h] += w
        for h, w in e["attacks"].items():
            score[h] -= w
    best = max(hyps, key=lambda h: (score[h], -hyps.index(h)))
    return best


def fam(item_id):
    return item_id.split("-")[1]  # P, O, D


items = [json.loads(l) for l in open(BAT) if l.strip()]
check("count==120", len(items) == 120, "n=%d" % len(items))

P = [it for it in items if fam(it["id"]) == "P"]
O = [it for it in items if fam(it["id"]) == "O"]
D = [it for it in items if fam(it["id"]) == "D"]
check("family sizes 40/40/40", len(P) == 40 and len(O) == 40 and len(D) == 40,
      "%d/%d/%d" % (len(P), len(O), len(D)))

# FC1: P full-stream argmax == GT
bad = [it["id"] for it in P if argmax(it) != it["ground_truth"]]
check("FC1 P full argmax==GT", not bad, "bad=%s" % bad[:3])

# FC2: O full-stream argmax == ADMIT (!= GT); first-5 argmax == GT
bad1 = [it["id"] for it in O if argmax(it) != "ADMIT"]
bad2 = [it["id"] for it in O if argmax(it) != it["ground_truth"]]
bad3 = [it["id"] for it in O if argmax(it, 5) != it["ground_truth"]]
check("FC2 O full argmax==ADMIT", not bad1, "bad=%s" % bad1[:3])
check("FC2 O full argmax!=GT on all 40", len(bad2) == 40, "n=%d unexpected=%s" % (len(bad2), bad2[:3]))
check("FC2 O first-5 argmax==GT", not bad3, "bad=%s" % bad3[:3])

# FC3: D full-stream argmax == GT
bad = [it["id"] for it in D if argmax(it) != it["ground_truth"]]
check("FC3 D full argmax==GT", not bad, "bad=%s" % bad[:3])


def run(cfg):
    rj = os.path.join(WORK, "r.jsonl")
    lg = os.path.join(WORK, "l.ledger")
    p = subprocess.run([BIN, BAT, os.path.join(CFGDIR, cfg + ".cfg"), rj, lg],
                       capture_output=True, text=True)
    recs = {}
    for l in open(rj):
        r = json.loads(l)
        recs[r["id"]] = r
    stops = {}
    for l in open(lg):
        try:
            e = json.loads(l)
        except Exception:
            continue
        if e.get("action") == "VERDICT":
            m = re.search(r"stop=([a-z]+)", e.get("detail", ""))
            stops[e["item"]] = m.group(1) if m else "?"
    return p.returncode, recs, stops


# FC4: parse 120/120 at d64
rc, recs, stops = run("d64")
check("FC4 parse 120/120 exit=0", rc == 0 and len(recs) == 120,
      "rc=%d n=%d" % (rc, len(recs)))

# FC5: depth-1 gates
rc, recs, stops = run("d1")
ok = rc == 0 and len(recs) == 120
p_ok = all(recs[it["id"]]["verdict"] == "ADMIT" for it in P)
d_pos = [it for it in D if int(it["id"].split("-")[2]) > 0]
d_z = [it for it in D if int(it["id"].split("-")[2]) == 0]
d_ok = all(recs[it["id"]]["verdict"] == "ADMIT" for it in d_pos)
d0_ok = all(recs[it["id"]]["verdict"] == "REJECT" for it in d_z)
o_ok = all(recs[it["id"]]["verdict"] == "REJECT" for it in O)
check("FC5 d1: P->ADMIT 40/40", ok and p_ok)
check("FC5 d1: D dose>0->ADMIT 30/30", ok and d_ok)
check("FC5 d1: D dose0->REJECT 10/10", ok and d0_ok)
check("FC5 d1: O->REJECT 40/40", ok and o_ok)

# FC6: adaptive stop rounds
rc, recs, stops = run("adaptive")
ok = rc == 0 and len(recs) == 120
p5 = all(recs[it["id"]]["rounds_used"] == 5 for it in P)
o5 = all(recs[it["id"]]["rounds_used"] == 5 for it in O)
exp = {0: 2, 1: 3, 2: 4, 6: 8}
d_ok = all(recs[it["id"]]["rounds_used"] == exp[int(it["id"].split("-")[2])]
           for it in D)
check("FC6 adaptive: P stop=5 40/40", ok and p5)
check("FC6 adaptive: O stop=5 40/40", ok and o5)
check("FC6 adaptive: D stop=2/3/4/8 by dose", ok and d_ok)

# FC7: bound prototype — refuses the round-5 stop, stops at the flip round
rc, recs, stops = run("bound")
ok = rc == 0 and len(recs) == 120 and len(stops) == 120
p7 = all(recs[it["id"]]["rounds_used"] == int(it["id"].split("-")[2])
         and recs[it["id"]]["verdict"] == it["ground_truth"]
         and stops[it["id"]] == "bound" for it in P)
o7 = all(recs[it["id"]]["rounds_used"] == int(it["id"].split("-")[2])
         and recs[it["id"]]["verdict"] == "ADMIT"
         and stops[it["id"]] == "bound" for it in O)
expb = {0: 1, 1: 2, 2: 3, 6: 7}
d7 = all(recs[it["id"]]["rounds_used"] == expb[int(it["id"].split("-")[2])]
         and recs[it["id"]]["verdict"] == it["ground_truth"]
         and stops[it["id"]] == "bound" for it in D)
check("FC7 bound: P refuses 5, stops at flip, correct 40/40", ok and p7)
check("FC7 bound: O refuses 5, stops at flip, wrong 40/40", ok and o7)
check("FC7 bound: D stops at dose+1, correct 40/40", ok and d7)

print("FIDELITY %s (%d failures)" % ("PASS" if not fails else "FAIL", len(fails)))
sys.exit(1 if fails else 0)
