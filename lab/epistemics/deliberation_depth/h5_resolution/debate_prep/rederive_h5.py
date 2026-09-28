#!/usr/bin/env python3
"""Independent re-derivation of H5 key numbers from RAW per-run records.

Does NOT trust the `correct` field: recomputes accuracy from verdict==ground_truth
and cross-checks the `correct` field for consistency. All comparisons against
RESULTS_H5.md expected values are reported as PASS/FLAG.
"""
import json, os, re, sys

SWEEP = os.path.expanduser("~/workspace/scratch-h5/sweep")
CFGS = ["d1", "d2", "d4", "d8", "deep16", "adaptive"]
BATS = ["admit", "revoke", "logic", "trap", "cost"]
N = {"admit": 248, "revoke": 113, "logic": 264, "trap": 127, "cost": 125}

flags = []
def check(name, actual, expect, tol=0.0):
    ok = abs(actual - expect) <= tol if isinstance(expect, float) else actual == expect
    print(f"{'PASS' if ok else 'FLAG'} {name}: actual={actual!r} expect={expect!r}")
    if not ok: flags.append(name)

def load(cfg, bat, rep="A"):
    rows = []
    with open(f"{SWEEP}/{cfg}_{bat}_{rep}.jsonl") as f:
        for l in f:
            l = l.strip()
            if l: rows.append(json.loads(l))
    return rows

print("== 1. parse counts per cell (A rep) ==")
for bat in BATS:
    for cfg in CFGS:
        rows = load(cfg, bat)
        check(f"parse {cfg}_{bat}", len(rows), N[bat])

print("\n== 2. A/B byte-identical (jsonl + ledger) ==")
det_ok = True
for cfg in CFGS:
    for bat in BATS:
        for ext in ("jsonl", "ledger", "stdout"):
            a = open(f"{SWEEP}/{cfg}_{bat}_A.{ext}", "rb").read()
            b = open(f"{SWEEP}/{cfg}_{bat}_B.{ext}", "rb").read()
            if a != b:
                det_ok = False; print(f"  MISMATCH {cfg}_{bat}.{ext}")
check("A/B determinism all 60 cells x 3 files", det_ok, True)

print("\n== 3. `correct` field consistency (verdict==GT vs correct flag) ==")
incons = 0
for cfg in CFGS:
    for bat in BATS:
        for r in load(cfg, bat):
            if (r["verdict"] == r["ground_truth"]) != bool(r["correct"]):
                incons += 1
check("correct-field inconsistencies", incons, 0)

print("\n== 4. accuracy curves (recomputed from verdict==GT) ==")
acc, rds = {}, {}
for bat in BATS:
    acc[bat] = {}; rds[bat] = {}
    for cfg in CFGS:
        rows = load(cfg, bat)
        acc[bat][cfg] = sum(1 for r in rows if r["verdict"] == r["ground_truth"]) / len(rows)
        rds[bat][cfg] = sum(r["rounds_used"] for r in rows) / len(rows)

trap_exp_acc = {"d1": 0.000, "d2": 0.331, "d4": 0.961, "d8": 1.000, "deep16": 1.000, "adaptive": 1.000}
for cfg, e in trap_exp_acc.items():
    check(f"trap acc {cfg}", round(acc["trap"][cfg], 3), e, tol=0.0005)
check("trap n", N["trap"], 127)

pool_n = sum(N.values())
for cfg in CFGS:
    correct = sum(int(acc[bat][cfg] * N[bat]) for bat in BATS)  # counts are exact; safer: recompute below
    # recompute directly from records for exactness
    tot = corr = 0
    for bat in BATS:
        rows = load(cfg, bat)
        tot += len(rows); corr += sum(1 for r in rows if r["verdict"] == r["ground_truth"])
    check(f"pooled acc {cfg} (n={tot})", round(corr / tot, 3),
          {"d1": 0.855, "d2": 0.903, "d4": 0.994, "d8": 1.000, "deep16": 1.000, "adaptive": 1.000}[cfg], tol=0.0005)
check("pooled n", pool_n, 877)

print("\n  trap correct counts:", {c: sum(1 for r in load(c, "trap") if r["verdict"] == r["ground_truth"]) for c in CFGS})

print("\n== 5. mean rounds per battery per config ==")
exp_rounds = {
    "admit":  {"d1": 1.00, "d2": 1.97, "d4": 3.63, "d8": 6.20, "deep16": 9.11, "adaptive": 4.15},
    "revoke": {"d1": 1.00, "d2": 2.00, "d4": 3.16, "d8": 5.10, "deep16": 5.63, "adaptive": 3.72},
    "logic":  {"d1": 1.00, "d2": 2.00, "d4": 2.06, "d8": 2.11, "deep16": 2.12, "adaptive": 2.07},
    "trap":   {"d1": 1.00, "d2": 2.00, "d4": 3.48, "d8": 3.81, "deep16": 3.81, "adaptive": 3.81},
    "cost":   {"d1": 1.00, "d2": 2.00, "d4": 4.00, "d8": 5.48, "deep16": 5.48, "adaptive": 4.84},
}
for bat in BATS:
    for cfg in CFGS:
        check(f"mean rounds {bat} {cfg}", round(rds[bat][cfg], 2), exp_rounds[bat][cfg], tol=0.005)
    print(f"   {bat}: exact means " + " ".join(f"{c}={rds[bat][c]:.4f}" for c in CFGS))

print("\n== 6. adaptive early stops: adaptive rounds_used < deep16 rounds_used per item ==")
exp_early = {"admit": 181, "revoke": 63, "logic": 3, "trap": 0, "cost": 40}
early_detail = {}
for bat in BATS:
    deep = {r["id"]: r["rounds_used"] for r in load("deep16", bat)}
    adap = load("adaptive", bat)
    early = [r["id"] for r in adap if r["rounds_used"] < deep[r["id"]]]
    also_equal = sum(1 for r in adap if r["rounds_used"] == deep[r["id"]])
    greater = [r["id"] for r in adap if r["rounds_used"] > deep[r["id"]]]
    check(f"early stops {bat}", len(early), exp_early[bat])
    print(f"   {bat}: early={len(early)}/{len(adap)} equal={also_equal} adaptive_gt_deep16={len(greater)}")
    early_detail[bat] = early

print("\n== 7. cap-hit rate from adaptive ledgers ==")
tot_cap = tot_items = 0
for bat in BATS:
    ncap = ntot = 0
    with open(f"{SWEEP}/adaptive_{bat}_A.ledger") as f:
        for l in f:
            if '"action":"VERDICT"' in l and "cap=" in l:
                ntot += 1
                if "cap=1" in l: ncap += 1
    check(f"cap {bat}", (ncap, ntot), (0, N[bat]))
    tot_cap += ncap; tot_items += ntot
check("cap pooled", (tot_cap, tot_items), (0, 877))

print("\n== 8. C6-wason d4->d8 gap ==")
# family membership from redteam source battery
fam = {}
try:
    with open(os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/redteam/trap_battery.jsonl")) as f:
        for l in f:
            l = l.strip()
            if l:
                o = json.loads(l); fam[o["id"]] = o.get("attack_class")
except FileNotFoundError:
    print("   trap_battery.jsonl missing locally")
wason_d4 = [r for r in load("d4", "trap") if fam.get(r["id"]) == "C6-wason-selection"]
wason_d8 = [r for r in load("d8", "trap") if fam.get(r["id"]) == "C6-wason-selection"]
print(f"   C6-wason items: d4 found={len(wason_d4)}, d8 found={len(wason_d8)}")
wrong_d4 = [r["id"] for r in wason_d4 if r["verdict"] != r["ground_truth"]]
wrong_d8 = [r["id"] for r in wason_d8 if r["verdict"] != r["ground_truth"]]
check("wason n", len(wason_d4), 5)
check("wason d4 wrong", len(wrong_d4), 5)
check("wason d8 wrong", len(wrong_d8), 0)
# trap items still wrong at d4: families
d4_wrong = [(r["id"], fam.get(r["id"])) for r in load("d4", "trap") if r["verdict"] != r["ground_truth"]]
print(f"   trap wrong at d4: {len(d4_wrong)} total")
byfam = {}
for i, f in d4_wrong: byfam[f] = byfam.get(f, 0) + 1
print(f"   by family: {byfam}")

print("\n== 9. adaptive == deep16 rounds on trap items ==")
deep = {r["id"]: r["rounds_used"] for r in load("deep16", "trap")}
adap = load("adaptive", "trap")
same = sum(1 for r in adap if r["rounds_used"] == deep[r["id"]])
check("trap adaptive==deep16 items", same, 127)

print("\n== 10. ledger VERDICT rounds vs jsonl rounds_used (offset check) ==")
rec = {r["id"]: r["rounds_used"] for r in load("adaptive", "trap")[:3]}
import re
offsets = set()
with open(f"{SWEEP}/adaptive_trap_A.ledger") as f:
    for l in f:
        if '"action":"VERDICT"' in l:
            m = re.search(r'"item":"([^"]+)".*"round":(\d+)', l)
            m2 = re.search(r'rounds=(\d+)', l)
            if m and m2 and m.group(1) in rec:
                offsets.add((int(m.group(2)), int(m2.group(1)), rec[m.group(1)]))
print(f"   (ledger_round, ledger_rounds=, jsonl_rounds_used) samples: {sorted(offsets)}")

print("\n== 11. confidence sensor spot-check (conf_final distribution) ==")
confs = {}
for bat in BATS:
    for cfg in ["adaptive", "d4"]:
        rows = load(cfg, bat)
        confs[(bat, cfg)] = sorted(set(r["confidence"] for r in rows))[:6]
print("   distinct confidence values (first 6) per (bat,cfg):", confs)

print("\n== 12. frozen knee rule mechanics ==")
# d(p) = acc(p) - acc(p/2) in pp, p in {2,4,8,16}; knee = smallest p with d(p)<1 and all later <1
for scope, accs in [("trap", acc["trap"]), ("pooled", None)]:
    if scope == "pooled":
        accs = {}
        for cfg in CFGS:
            tot = corr = 0
            for bat in BATS:
                rows = load(cfg, bat)
                tot += len(rows); corr += sum(1 for r in rows if r["verdict"] == r["ground_truth"])
            accs[cfg] = corr / tot
    ds = {p: (accs[f"d{p}"] if p != 16 else accs["deep16"]) - accs[f"d{p//2}"] for p in (2, 4, 8, 16)}
    print(f"   {scope}: " + " ".join(f"d({p})={ds[p]*100:+.3f}pp" for p in (2, 4, 8, 16)))
    knee = None
    for i, p in enumerate((2, 4, 8, 16)):
        if ds[p] * 100 < 1 and all(ds[q] * 100 < 1 for q in (2, 4, 8, 16)[i:]):
            knee = p; break
    print(f"   {scope}: frozen-rule knee = {knee} (KNEE-BEYOND-RANGE if None)")

print("\n== SUMMARY ==")
if flags:
    print(f"FLAGS RAISED ({len(flags)}):")
    for f in flags: print(f"  - {f}")
else:
    print("ALL CHECKS PASS — no discrepancies vs RESULTS_H5.md.")
sys.exit(1 if flags else 0)
