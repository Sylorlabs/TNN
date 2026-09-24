#!/usr/bin/env python3
"""Score FS-GR1 bars from eval outputs."""
import os, math, re

FORK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-GR1"
EV = os.path.join(FORK, "evidence", "eval")

BASE_FI_RATE = {"colordisc":0.0, "colorconst":0.0, "shapetrans":0.0, "pitchdisc":0.0}
BASE_REC = {"colordisc":92.00, "colorconst":98.40, "shapetrans":86.3333, "pitchdisc":93.50}

def wilson_ucb(k, n, z=1.96):
    if n == 0: return 1.0
    p = k / n
    z2 = z*z
    den = 1 + z2/n
    num = p + z2/(2*n) + z*math.sqrt(p*(1-p)/n + z2/(4*n*n))
    return num / den

def parse_gate_raw(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if not line: continue
        # fixture=... task=... judgment=... challenge=... outcome=... disp=... admit=...
        d = dict(kv.split("=",1) for kv in line.split() if "=" in kv)
        rows.append(d)
    return rows

def get_truth(fixture_path):
    # fixture_path is like .../e2b_adv_motiondir_33802.r2fx or r2fx_t1_i30000_f1
    # For adv: need to map to actual file. The fixture= field is a short id.
    # Let's use the formation TSV which has full paths.
    return None

# Load formation TSVs (full paths -> judgment)
def load_form_tsv(path):
    d = {}
    for line in open(path):
        line=line.strip()
        if not line: continue
        parts = line.split("\t")
        fp = parts[0]
        # task=..., judgment=...
        td = dict(kv.split("=",1) for kv in parts[1:] if "=" in kv)
        d[fp] = td
    return d

# Load truth for adv fixtures
def load_truth():
    # From manifest? Actually truth is in .truth sidecar files
    # The gate raw has fixture= short id; need to map.
    # Simpler: parse the adv list which has full paths, and for each get truth from .truth file
    truth = {}
    for listname in ["b_adv_e2b.list", "b_ctrl_e2b.list"]:
        for line in open(os.path.join(EV, listname)):
            fp = line.strip()
            if not fp: continue
            tp = fp + ".truth"
            if os.path.exists(tp):
                t = open(tp).read().strip()
                # format "truth=N" or similar
                if "=" in t:
                    t = t.split("=",1)[1]
                truth[fp] = t
    return truth

print("Loading...", flush=True)
adv_form = load_form_tsv(os.path.join(EV, "adv_formation_r1.tsv"))
ctrl_form = load_form_tsv(os.path.join(EV, "ctrl_formation_r1.tsv"))
adv_gate = parse_gate_raw(os.path.join(EV, "adv_gate_raw_r1.txt"))
ctrl_gate = parse_gate_raw(os.path.join(EV, "ctrl_gate_raw_r1.txt"))
truth = load_truth()
print(f"adv_gate={len(adv_gate)} ctrl_gate={len(ctrl_gate)} truth={len(truth)}", flush=True)

# Map gate rows to full paths via formation TSV order
# (gate raw fixture= is short id; formation TSV has full path in order)
adv_paths = list(adv_form.keys())
ctrl_paths = list(ctrl_form.keys())

# Score per task
from collections import defaultdict
adv_by_task = defaultdict(list)
ctrl_by_task = defaultdict(list)

for i, g in enumerate(adv_gate):
    if i >= len(adv_paths): break
    fp = adv_paths[i]
    task = adv_form[fp].get("task", "unknown")
    adv_by_task[task].append((fp, g))

for i, g in enumerate(ctrl_gate):
    if i >= len(ctrl_paths): break
    fp = ctrl_paths[i]
    task = ctrl_form[fp].get("task", "unknown")
    ctrl_by_task[task].append((fp, g))

print("\n=== ADVERSARIAL FI ===")
for task in sorted(adv_by_task):
    rows = adv_by_task[task]
    n = len(rows)
    fi = 0
    for fp, g in rows:
        judg = g.get("judgment", "")
        outc = g.get("outcome", "")
        disp = g.get("disp", "")
        t = truth.get(fp, "")
        # FI: formation wrong (judgment != truth) AND challenge agrees (outcome == judgment) AND installed
        # Note: outcome=-1 or UNRESOLVED means no agreement
        if judg != t and outc == judg and disp == "INSTALL":
            fi += 1
    ucb = wilson_ucb(fi, n)
    rate = 100.0*fi/n if n else 0
    print(f"{task}: FI={fi}/{n} rate={rate:.4f}% UCB={100*ucb:.4f}%")

print("\n=== CONTROL RECALL ===")
for task in sorted(ctrl_by_task):
    rows = ctrl_by_task[task]
    n = len(rows)
    rec = 0
    for fp, g in rows:
        judg = g.get("judgment", "")
        outc = g.get("outcome", "")
        t = truth.get(fp, "")
        # Recall: formation correct (judgment == truth) AND challenge agrees (outcome == judgment)
        if judg == t and outc == judg:
            rec += 1
    rate = 100.0*rec/n if n else 0
    print(f"{task}: recall={rec}/{n} = {rate:.4f}%")

print("\n=== BARS ===")
# Bar 1: motiondir FI UCB ≤1%
mrows = adv_by_task.get("motiondir", [])
mfi = sum(1 for fp,g in mrows if g.get("judgment","") != truth.get(fp,"") and g.get("outcome","")==g.get("judgment","") and g.get("disp","")=="INSTALL")
mucb = wilson_ucb(mfi, len(mrows))
print(f"Bar1 motiondir FI UCB: {mfi}/{len(mrows)} UCB={100*mucb:.4f}% ≤1%: {mucb <= 0.01} {'PASS' if mucb<=0.01 else 'FAIL'}")
# Bar 2: timbredisc recall ≥85%
trows = ctrl_by_task.get("timbredisc", [])
trec = sum(1 for fp,g in trows if g.get("judgment","")==truth.get(fp,"") and g.get("outcome","")==g.get("judgment",""))
trec_rate = trec/len(trows) if trows else 0
print(f"Bar2 timbredisc recall: {trec}/{len(trows)} = {100*trec_rate:.2f}% ≥85%: {trec_rate>=0.85} {'PASS' if trec_rate>=0.85 else 'FAIL'}")
# Bar 3: no-regression
print("Bar3 no-regression (other four):")
all_pass = True
for task in ["colordisc","colorconst","shapetrans","pitchdisc"]:
    arows = adv_by_task.get(task, [])
    afi = sum(1 for fp,g in arows if g.get("judgment","") != truth.get(fp,"") and g.get("outcome","")==g.get("judgment","") and g.get("disp","")=="INSTALL")
    afi_rate = 100.0*afi/len(arows) if arows else 0
    fi_ok = afi_rate <= BASE_FI_RATE[task] + 1.0
    crows = ctrl_by_task.get(task, [])
    crec = sum(1 for fp,g in crows if g.get("judgment","")==truth.get(fp,"") and g.get("outcome","")==g.get("judgment",""))
    crec_rate = 100.0*crec/len(crows) if crows else 0
    rec_ok = crec_rate >= BASE_REC[task] - 1.0
    ok = fi_ok and rec_ok
    all_pass = all_pass and ok
    print(f"  {task}: FI {afi}/{len(arows)}={afi_rate:.4f}% (≤{BASE_FI_RATE[task]+1.0}%) {'OK' if fi_ok else 'FAIL'}; recall {crec}/{len(crows)}={crec_rate:.2f}% (≥{BASE_REC[task]-1.0}%) {'OK' if rec_ok else 'FAIL'}")
print(f"Bar3: {'PASS' if all_pass else 'FAIL'}")
