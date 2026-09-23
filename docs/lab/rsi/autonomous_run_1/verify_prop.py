#!/usr/bin/env python3
"""Frozen scorer for the autonomous run's prop-mode tests.

Usage: verify_prop.py <runs-dir> <battery-csv> <mode-tag> <champ-acc> <champ-wrong> <champ-cost> <p-dacc> <p-dwrong> <p-cost>
  mode-tag: e.g. prop_c1 (log files: <mode-tag>_0..4.log)
  champ-*: current champion's REAL measured scores (from the frozen verdict
           for round 0, from prior kept measurements later)
  p-*: the proposer's published predictions (deltas + exact cost)

Checks (mirrors the frozen R4C oracle's bars):
  DET: 5/5 byte-identical logs.
  SEP: item fields == CSV fields exactly; subject source contains no gt
       (the caller passes --src to enable the grep check).
  SCORES vs gt from the CSV.
  PREDICTION VERDICT: acc in [champ_acc+p_dacc-1, champ_acc+p_dacc+1],
    wrong in [champ_wrong+p_dwrong-1, champ_wrong+p_dwrong+1], cost == p_cost,
    RECALL == 10000, COST-quiet == 200.
  NOREG: acc >= champ_acc and wrong <= champ_wrong (any degradation = FAIL).
Exits 0 with HIT/MISS verdict printed; exits 2 on bar failure.
"""
import csv, glob, os, sys

def fail(msg):
    print("BAR-FAIL:", msg); sys.exit(2)

def sat(v, a, op):
    return (v == a) if op == 0 else ((v < a) if op == 1 else (v > a))

(runs, csvpath, tag, ca, cw, cc, pd_a, pd_w, pc) = sys.argv[1:10]
ca, cw, cc, pd_a, pd_w, pc = int(ca), int(cw), int(cc), int(pd_a), int(pd_w), int(pc)
src = sys.argv[10] if len(sys.argv) > 10 else None

batt = {}
with open(csvpath) as f:
    for row in csv.DictReader(f):
        i = int(row["id"])
        batt[i] = dict(key=int(row["key"]), vold=int(row["vold"]),
                       vnew=int(row["vnew"]),
                       rels=[(int(row["a1"]), int(row["op1"])),
                             (int(row["a2"]), int(row["op2"])),
                             (int(row["a3"]), int(row["op3"]))],
                       cidx=int(row["cidx"]), caval=int(row["caval"]),
                       gt=row["gt"], cls=row["class"])

files = sorted(glob.glob(os.path.join(runs, f"{tag}_*.log")))
assert len(files) == 5, f"want 5 logs, have {len(files)}"
bodies = [open(f).read() for f in files]
if len(set(bodies)) != 1:
    fail("DET: logs differ across reps")
body = bodies[0]
if "R4C_DONE" not in body:
    fail("DET: log malformed")
print("DET: PASS (5/5 byte-identical)")

items, fields = {}, {}
for line in body.splitlines():
    if line.startswith("R4C_ITEMFIELDS,"):
        kv = dict(p.split("=") for p in line.split(",")[1:])
        iid = int(kv["id"])
        fields[iid] = {k: int(v) for k, v in kv.items() if k != "id"}
    elif line.startswith("R4C_ITEM,"):
        kv = dict(p.split("=") for p in line.split(",")[1:])
        items[int(kv["id"])] = (kv["verdict"], int(kv["ops"]), int(kv["consult"]))
if set(items) != set(batt) or set(fields) != set(batt):
    fail("SEP: item coverage != 24")
for i, b in batt.items():
    f = fields[i]
    want = dict(key=b["key"], vold=b["vold"], vnew=b["vnew"],
                a1=b["rels"][0][0], op1=b["rels"][0][1],
                a2=b["rels"][1][0], op2=b["rels"][1][1],
                a3=b["rels"][2][0], op3=b["rels"][2][1],
                cidx=b["cidx"], caval=b["caval"])
    if f != want:
        fail(f"SEP: item {i} fields drift from CSV")
if src:
    s = open(src).read()
    # the subject must never read a gt-carrying file (verdict labels like
    # "NEW" legitimately appear in vname(); only file references are checked)
    if "battery_r4c.csv" in s or "proxy_battery" in s or "proxy_table" in s:
        fail("SEP: subject source references a gt-carrying file")
print("SEP: PASS (fields match CSV)")

acc = wrong = cost = cons = 0
recall_ok = costq_ok = False
for line in body.splitlines():
    if line.startswith("R4C_BATT,id=RECALL,metric="):
        recall_ok = line.strip().endswith("10000")
    if line.startswith("R4C_BATT,id=COST,metric="):
        costq_ok = line.strip().endswith("200")
neither_ids = [i for i, b in batt.items() if b["cls"] == "NEITHER"]
for i, b in batt.items():
    v, ops, c = items[i]
    cost += ops; cons += c
    if v == b["gt"]: acc += 1
    elif v in ("NEW", "OLD"): wrong += 1

print(f"SCORES: acc={acc}/24 wrong={wrong}/24 cost={cost} consults={cons} "
      f"recall={'10000' if recall_ok else 'BROKEN'} costq={'200' if costq_ok else 'BROKEN'}")
if not (recall_ok and costq_ok):
    fail("NOREG: distractor batteries moved")

exp_acc_lo, exp_acc_hi = ca + pd_a - 1, ca + pd_a + 1
exp_wrong_lo, exp_wrong_hi = cw + pd_w - 1, cw + pd_w + 1
hits = (exp_acc_lo <= acc <= exp_acc_hi and
        exp_wrong_lo <= wrong <= exp_wrong_hi and
        cost == pc)
noreg = (acc >= ca and wrong <= cw)
print(f"PREDICTED: acc in [{exp_acc_lo},{exp_acc_hi}] wrong in [{exp_wrong_lo},{exp_wrong_hi}] cost=={pc}")
print("PREDICTION-VERDICT:", "HIT" if hits else "MISS")
print("NO-DEGRADATION:", "PASS" if noreg else "FAIL")
if not noreg:
    fail("G4: metric degradation vs champion")
sys.exit(0 if hits else 1)
