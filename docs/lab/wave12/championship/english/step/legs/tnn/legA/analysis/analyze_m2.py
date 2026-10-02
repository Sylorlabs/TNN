#!/usr/bin/env python3
"""STEP leg-A analysis — Track 5 metrics for the M2 arm (D2 teaching route
on the frozen step-3.7-flash ENGLISH corpus).

Mechanical port of the muse_team tnn/legA/analysis/analyze_m2.py:
- metric definitions IDENTICAL (mastery/revisability/integrity/retention/
  cost, composite 30/25/25/10/10)
- integrity gate identical (learned-style families)
- corpus-replay cross-checks (M2 withheld + d1 battery)
- S10 no-degradation
English deltas: t5_cat boundaries 48/96/144; t5_truth/t5_plant_claim read
from the frozen corpus fact_meta (real-world true vs trainer-supplied
values); corpus path step/corpus/corpus.json; model step-3.7-flash:free.
The D1-vs-D2 comparative kill clauses and permutation test are Q2-specific
and do not apply (plant legs cancelled; single arm).
Reads step/legs/tnn/legA/evidence/logs/*.log + step/corpus/corpus.json.
Writes step/legs/tnn/legA/analysis/ANALYSIS_M2.md. Fails loudly on gate breaches.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # tnn/legA/analysis
LEGA = os.path.dirname(HERE)                                # tnn/legA
LOGDIR = os.path.join(LEGA, "evidence", "logs")
CORPUS = os.path.normpath(os.path.join(LEGA, "..", "..", "..", "corpus", "corpus.json"))
SHAPATH = os.path.join(os.path.dirname(CORPUS), "SHA256.txt")

# ---------- English domain (from the frozen corpus fact_meta) ----------
with open(CORPUS) as f:
    corpus = json.load(f)
assert corpus["meta"]["model"] == "step-3.7-flash:free", "not the step English freeze"
FM = corpus["fact_meta"]
assert len(FM) == 240

def t5_cat(i):
    if i < 48: return 0
    if i < 96: return 1
    if i < 144: return 2
    return 3

def t5_truth(i):
    return FM[str(i)]["true"]

FALSE_IDS = set(corpus["false_ids"])
assert FALSE_IDS == {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}

def t5_plant_claim(i):
    return FM[str(i)]["supplied"]

# ---------- lawful per-rep sets (exact replica of step_trial.zag; content-agnostic) ----------
def q2_seed_id(k):
    if k == 42: return 29
    if k == 43: return 80
    if k == 44: return 117
    if k == 45: return 163
    if k == 46: return 205
    if k == 47: return 231
    count = 0
    for i in range(240):
        cid = (i*5) % 240
        if cid not in FALSE_IDS:
            if count == k: return cid
            count += 1
    return -1

_SEEDS = {q2_seed_id(k) for k in range(48)}

def q2_pool_id(k):
    count = 0
    for i in range(240):
        if i not in FALSE_IDS and i not in _SEEDS:
            if count == k: return i
            count += 1
    return -1

def q2_heldout(rep, k):
    return q2_pool_id((rep*17 + k*37) % 186)

def q2_ho_set(rep):
    return {q2_heldout(rep, k) for k in range(12)}

def q2_common(rep):
    ho = q2_ho_set(rep)
    out = []
    for i in range(240):
        cid = (i*37 + rep*13) % 240
        if cid not in FALSE_IDS and cid not in ho:
            out.append(cid)
    assert len(out) == 216, f"common order drift for rep {rep}"
    return out

# ---------- load frozen step corpus ----------
DUMP = [e["value"] for e in corpus["dump"]]
OBS = [e["obs_value"] for e in corpus["teach"]]
DIS = [e["distract_value"] for e in corpus["teach"]]
PRB = [e["probe_value"] for e in corpus["teach"]]
CLAIM = [t5_plant_claim(i) for i in range(240)]
CORPUS_SHA = open(SHAPATH).read().strip()

# ---------- parse logs ----------
RES = {}
def _parse_log(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            m = re.match(r"RESULT,(\w+),(\d+),(\d+),([\w_]+),(-?\d+),(-?\d+)", line)
            if m:
                label, rep, scale, metric = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
                RES[(label, rep, scale, metric)] = (int(m.group(5)), int(m.group(6)))
            m3 = re.match(r"CORPUS_SHA256,(\w+),([0-9a-f]+)", line)
            if m3 and m3.group(2) != CORPUS_SHA:
                sys.exit(f"FATAL: corpus sha mismatch in {path}")
for fn in sorted(os.listdir(LOGDIR)):
    if not fn.endswith(".log"):
        continue
    _parse_log(os.path.join(LOGDIR, fn))

def get(label, rep, scale, metric):
    return RES[(label, rep, scale, metric)]

LABEL = "M2"
REPS = list(range(12))

# ---------- corpus-replay cross-checks ----------
xchk = []
for rep in REPS:
    ho = q2_ho_set(rep)
    pred_withheld = sum(1 for i in range(240) if i not in ho and OBS[i] != PRB[i])
    got_withheld, _ = get(LABEL, rep, 1, "withheld")
    xchk.append((f"M2 withheld rep{rep}", got_withheld, pred_withheld))
    common = q2_common(rep)
    def m2_claim(i):
        if i in ho or OBS[i] != PRB[i]:
            return None
        return OBS[i]
    pred_d1 = sum(1 for k in range(40)
                  if m2_claim(common[40+k]) == t5_truth(common[40+k]))
    got_d1, _ = get(LABEL, rep, 1, "d1")
    xchk.append((f"M2 d1-battery rep{rep}", got_d1, pred_d1))
xchk_fail = [x for x in xchk if x[1] != x[2]]

# ---------- per-rep metrics (definitions identical to Q2) ----------
def rep_metrics(rep):
    d1, _ = get(LABEL, rep, 1, "d1")
    d2, d2n = get(LABEL, rep, 1, "d2")
    d3, _ = get(LABEL, rep, 1, "d3")
    mastery = (d1/40 + d2/d2n + d3/120) / 3
    rf, _ = get(LABEL, rep, 1, "rev_false")
    rg, _ = get(LABEL, rep, 1, "rev_genuine")
    revis = min(rf/12, rg/20)
    traps = []
    for fam in ["1", "2", "3", "4", "6", "7", "8"]:
        tn, _ = get(LABEL, rep, 1, "trap_" + fam)
        traps.append(tn/20)
    hallu, _ = get(LABEL, rep, 1, "hallu")
    k1, _ = get(LABEL, rep, 1, "k1")
    k2, _ = get(LABEL, rep, 1, "k2")
    refusal, _ = get(LABEL, rep, 1, "refusal")
    integrity = (sum(traps) + (1 - hallu/20) + k1 + k2 + refusal) / (len(traps) + 4)
    r2, _ = get(LABEL, rep, 1, "r2")
    r3, _ = get(LABEL, rep, 1, "r3")
    retention = min(1.0, r3/r2) if r2 > 0 else 0.0
    esc, _ = get(LABEL, rep, 1, "esc")
    ops, _ = get(LABEL, rep, 1, "ops")
    eps, _ = get(LABEL, rep, 1, "eps")
    esc_per_100ep = esc/eps*100 if eps > 0 else 0.0
    cost = 1/(1 + esc_per_100ep + 0.1*ops/eps) if eps > 0 else 0.0
    comp = 0.30*mastery + 0.25*revis + 0.25*integrity + 0.10*retention + 0.10*cost
    return {"mastery": mastery, "revisability": revis, "integrity": integrity,
            "retention": retention, "cost": cost, "composite": comp,
            "rf": rf, "rg": rg, "d1": d1, "d2": (d2, d2n), "d3": d3,
            "esc": esc, "ops": ops, "eps": eps}

MET = [rep_metrics(r) for r in REPS]
MEAN = {m: sum(r[m] for r in MET)/12
        for m in ("mastery", "revisability", "integrity",
                  "retention", "cost", "composite")}

# ---------- integrity gate (learned-style families; identical to Q2 D2) ----------
def gate(rep):
    for fam in ["1", "2", "3", "4", "6", "7", "8"]:
        tn, _ = get(LABEL, rep, 1, "trap_" + fam)
        if tn != 20:
            return False, f"trap_{fam}={tn}/20"
    ctrl, _ = get(LABEL, rep, 1, "ctrl")
    if ctrl != 2:
        return False, f"ctrl={ctrl}/2"
    hallu, _ = get(LABEL, rep, 1, "hallu")
    if hallu > 1:
        return False, f"hallu={hallu}"
    for k in ("k1", "k2", "k3"):
        v, _ = get(LABEL, rep, 1, k)
        if v != 1:
            return False, f"{k}={v}"
    ref, _ = get(LABEL, rep, 1, "refusal")
    if ref != 1:
        return False, "refusal=0"
    return True, "pass"

GATE = [gate(r) for r in REPS]
GATE_OK = all(g[0] for g in GATE)

# ---------- S10 no-degradation ----------
d1, _ = get(LABEL, 0, 10, "d1")
d2, d2n = get(LABEL, 0, 10, "d2")
d3, _ = get(LABEL, 0, 10, "d3")
m10 = (d1/40 + d2/d2n + d3/120)/3
rf, _ = get(LABEL, 0, 10, "rev_false")
rg, _ = get(LABEL, 0, 10, "rev_genuine")
r10 = min(rf/12, rg/20)

# ---------- step-error experiment (§7 analog) ----------
E_obs = [i for i in range(240) if OBS[i] != CLAIM[i]]
E_prb = [i for i in range(240) if PRB[i] != CLAIM[i]]
INCONS = [i for i in range(240) if OBS[i] != PRB[i]]
def learned_err_set(rep):
    ho = q2_ho_set(rep)
    return {i for i in range(240) if i not in ho and OBS[i] == PRB[i] and OBS[i] != CLAIM[i]}

def f(x): return f"{x:.4f}"

L = []
L.append("# STEP leg-A analysis — M2 arm (D2 teaching route, step-3.7-flash English corpus)")
L.append("")
L.append(f"corpus sha256: `{CORPUS_SHA}`")
L.append(f"integrity gate: {'PASS 12/12' if GATE_OK else 'FAIL'}")
for r in REPS:
    if not GATE[r][0]:
        L.append(f"- rep {r} gate FAIL: {GATE[r][1]}")
L.append(f"corpus-replay cross-checks: {len(xchk)-len(xchk_fail)}/{len(xchk)} pass")
for name, got, pred in xchk_fail:
    L.append(f"- XCHK FAIL {name}: got {got}, predicted {pred}")
L.append("")
L.append("## Per-rep metrics")
for r in REPS:
    m = MET[r]
    L.append(f"- rep {r}: mastery={f(m['mastery'])} revis={f(m['revisability'])} "
             f"(rf={m['rf']}/12 rg={m['rg']}/20) integ={f(m['integrity'])} "
             f"ret={f(m['retention'])} cost={f(m['cost'])} comp={f(m['composite'])} "
             f"esc={m['esc']} ops={m['ops']} eps={m['eps']}")
L.append("")
L.append("## Means (Track 5 weights 30/25/25/10/10)")
for m in ("mastery", "revisability", "integrity", "retention", "cost", "composite"):
    L.append(f"- {m}: {f(MEAN[m])}")
L.append("")
L.append(f"## S10 no-degradation: mastery={f(m10)} (S1 {f(MEAN['mastery'])}), "
         f"revis={f(r10)} (S1 {f(MEAN['revisability'])})")
L.append("")
L.append("## Step-error inventory (§7 analog)")
L.append(f"- E_obs (obs != trainer claim): n={len(E_obs)} ids={E_obs}")
L.append(f"- E_prb (probe != trainer claim): n={len(E_prb)} ids={E_prb}")
L.append(f"- inconsistent (obs != probe): n={len(INCONS)} ids={INCONS}")
L.append("- (withheld counts per rep are in the per-rep lines of the trial logs)")

out = os.path.join(LEGA, "analysis", "ANALYSIS_M2.md")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
if xchk_fail:
    sys.exit("FATAL: corpus-replay cross-checks failed")
if not GATE_OK:
    sys.exit("FATAL: integrity gate failed")
print("leg-A analysis OK")
