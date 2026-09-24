#!/usr/bin/env python3
"""Reproduce the H5 integration-probe error taxonomy (evidence 3).

Runs the verified harness binary over each frozen battery/red-team file and
tabulates per-line parse errors. Usage:
  python3 characterize_errors.py <delib_harness> <cfg> <outdir>
Writes <outdir>/error_taxonomy.tsv and prints the summary table.
Deterministic: every file is run twice and the two outputs are cmp-compared.
"""
import json, os, subprocess, sys

BIN, CFG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth")
FILES = {
    "admit":  "batteries/admit_battery.jsonl",
    "revoke":  "batteries/revoke_battery.jsonl",
    "logic":   "batteries/logic_battery.jsonl",
    "trap":    "redteam/trap_battery.jsonl",
    "cost":    "redteam/cost_attacks.jsonl",
}
os.makedirs(OUT, exist_ok=True)

def run(items, res, led):
    p = subprocess.run([BIN, items, CFG, res, led],
                       capture_output=True, text=True)
    return p.returncode

def err_dist(res):
    d = {}
    for line in open(res):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if "error" in o:
            d[o["error"]] = d.get(o["error"], 0) + 1
    return d

rows = []
for name, rel in FILES.items():
    items = os.path.join(BASE, rel)
    n = sum(1 for l in open(items) if l.strip())
    r1, l1 = os.path.join(OUT, name + "_A.jsonl"), os.path.join(OUT, name + "_A.ledger")
    r2, l2 = os.path.join(OUT, name + "_B.jsonl"), os.path.join(OUT, name + "_B.ledger")
    rc1, rc2 = run(items, r1, l1), run(items, r2, l2)
    det_r = open(r1, "rb").read() == open(r2, "rb").read()
    det_l = open(l1, "rb").read() == open(l2, "rb").read()
    d = err_dist(r1)
    verdicts = sum(1 for l in open(r1) if '"verdict"' in l)
    rows.append((name, n, rc1, rc2, det_r and det_l, verdicts, d))
    print("%-7s n=%3d exit_A=%3d exit_B=%3d byte_identical=%s verdicts=%d errors=%s"
          % (name, n, rc1, rc2, det_r and det_l, verdicts, d))

with open(os.path.join(OUT, "error_taxonomy.tsv"), "w") as f:
    f.write("file\tn\texit_A\texit_B\tbyte_identical\tverdicts\terrors\n")
    for name, n, rc1, rc2, det, v, d in rows:
        f.write("%s\t%d\t%d\t%d\t%s\t%d\t%s\n"
                % (name, n, rc1, rc2, det, v, json.dumps(d, sort_keys=True)))
print("wrote", os.path.join(OUT, "error_taxonomy.tsv"))
tot_v = sum(r[5] for r in rows)
tot_n = sum(r[1] for r in rows)
print("TOTAL: %d/%d items produced verdicts" % (tot_v, tot_n))
