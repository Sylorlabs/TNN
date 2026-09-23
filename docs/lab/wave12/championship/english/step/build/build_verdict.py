#!/usr/bin/env python3
"""Build STEP_ENGLISH_VERDICT.md from frozen evidence.

Reads:
- step/corpus/SHA256.txt + corpus.json (faithfulness inventory)
- step/legs/tnn/legA/evidence/logs/m2.bind.rep*.log + m2.btrap.rep*.log
  (class-4 Track-5 composite, same metric definitions as analyze_m2.py)
- step/legs/tnn/legB/evidence/logs/stepb.log (class-4 direct §B.7)
- step/legs/tnn/legC/evidence/logs/stepc.log (class-3 teacher leg §B.7 +
  teaching/mastery numbers)
Verifies the legB/legC teacher-state digests match.
Writes STEP_ENGLISH_VERDICT.md next to this script's step root.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))  # step/build
STEP = os.path.dirname(HERE)                        # step
LEGS = os.path.join(STEP, "legs", "tnn")

CORPUS_SHA = open(os.path.join(STEP, "corpus", "SHA256.txt")).read().strip()
corpus = json.load(open(os.path.join(STEP, "corpus", "corpus.json")))
INV = corpus["error_inventory"]
FALSE_IDS = corpus["false_ids"]

# ---------- legA: Track-5 per-rep metrics ----------
LOGDIR_A = os.path.join(LEGS, "legA", "evidence", "logs")
RES = {}
for rep in range(12):
    for mode in ("bind", "btrap"):
        p = os.path.join(LOGDIR_A, f"m2.{mode}.rep{rep}.log")
        with open(p) as f:
            for line in f:
                m = re.match(r"RESULT,(\w+),(\d+),(\d+),([\w_]+),(-?\d+),(-?\d+)", line.strip())
                if m:
                    RES[(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4))] = \
                        (int(m.group(5)), int(m.group(6)))

def get(rep, scale, metric):
    return RES[("M2", rep, scale, metric)]

def rep_metrics(rep):
    d1, _ = get(rep, 1, "d1")
    d2, d2n = get(rep, 1, "d2")
    d3, _ = get(rep, 1, "d3")
    mastery = (d1/40 + d2/d2n + d3/120) / 3
    rf, _ = get(rep, 1, "rev_false")
    rg, _ = get(rep, 1, "rev_genuine")
    revis = min(rf/12, rg/20)
    traps = [get(rep, 1, "trap_" + fam)[0]/20 for fam in ["1","2","3","4","6","7","8"]]
    hallu, _ = get(rep, 1, "hallu")
    k1, _ = get(rep, 1, "k1"); k2, _ = get(rep, 1, "k2")
    ref, _ = get(rep, 1, "refusal")
    integrity = (sum(traps) + (1 - hallu/20) + k1 + k2 + ref) / (len(traps) + 4)
    r2, _ = get(rep, 1, "r2"); r3, _ = get(rep, 1, "r3")
    retention = min(1.0, r3/r2) if r2 > 0 else 0.0
    esc, _ = get(rep, 1, "esc"); ops, _ = get(rep, 1, "ops"); eps, _ = get(rep, 1, "eps")
    esc_per_100ep = esc/eps*100 if eps > 0 else 0.0
    cost = 1/(1 + esc_per_100ep + 0.1*ops/eps) if eps > 0 else 0.0
    comp = 0.30*mastery + 0.25*revis + 0.25*integrity + 0.10*retention + 0.10*cost
    return (mastery, revis, integrity, retention, cost, comp)

MET = [rep_metrics(r) for r in range(12)]
MEAN = [sum(m[i] for m in MET)/12 for i in range(6)]

# ---------- legB: class-4 direct §B.7 ----------
def parse_slices(path, prefix):
    slices = {}
    run = None
    teach_digest = None
    for line in open(path):
        line = line.strip()
        m = re.match(rf"{prefix}_SLICE,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)", line)
        if m:
            s = int(m.group(1))
            slices[s] = {"hits": int(m.group(2)), "nears": int(m.group(3)),
                         "misses": int(m.group(4)), "score_x10": int(m.group(5)),
                         "pass": int(m.group(6))}
        m = re.match(rf"{prefix}_RUN,(.*)", line)
        if m:
            run = [int(x) for x in m.group(1).split(",")]
        m = re.match(rf"{prefix}_TEACH_DIGEST,([0-9a-f]+)", line)
        if m:
            teach_digest = m.group(1)
    return slices, run, teach_digest

SLB, RUNB, DIGB = parse_slices(os.path.join(LEGS, "legB", "evidence", "logs", "stepb.log"), "STEPB")
# ---------- legC: class-3 teacher leg ----------
SLC, RUNC, DIGC = parse_slices(os.path.join(LEGS, "legC", "evidence", "logs", "stepc.log"), "STEPC")
# legC slice lines carry extra fields: adopts, mastery/24, tripwire
SLC2 = {}
for line in open(os.path.join(LEGS, "legC", "evidence", "logs", "stepc.log")):
    m = re.match(r"STEPC_SLICE,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)", line.strip())
    if m:
        g = [int(x) for x in m.groups()]
        SLC2[g[0]] = {"hits": g[1], "nears": g[2], "misses": g[3], "score_x10": g[4],
                      "pass": g[5], "adopts": g[6], "mastery24": g[7], "tripwire": g[8]}

assert DIGB == DIGC, f"teacher-state digest mismatch: legB {DIGB} vs legC {DIGC}"

def f(x): return f"{x:.4f}"

L = []
L.append("# STEP championship English verdict (step-3.7-flash:free, real-English box)")
L.append("")
L.append(f"Corpus sha256: `{CORPUS_SHA}`")
L.append(f"Teacher-state digest (legB == legC): `{DIGB}` — MATCH")
L.append("")
L.append("## Faithfulness (model text vs trainer-supplied claims, 240 ids)")
L.append("")
L.append("| check | definition | count |")
L.append("|---|---|---|")
for k in ("E_dump", "E_obs", "E_prb", "inconsistent", "distract_value!= obs_value",
          "sentence_missing_value"):
    if k in INV:
        L.append(f"| {k} |  | {INV[k]['n']} |")
L.append("")
L.append(f"False ids ({len(FALSE_IDS)}): reproduced vs flagged/corrected — see "
         "`corpus/ERROR_INVENTORY.md` §2.")
L.append("")
L.append("## Class 4 — Track 5 (D2 arm, 12 reps; weights 30/25/25/10/10)")
L.append("")
L.append("| rep | mastery | revisab | integrity | retent | cost | composite |")
L.append("|---|---|---|---|---|---|---|")
for r in range(12):
    m = MET[r]
    L.append(f"| {r} | " + " | ".join(f(x) for x in m) + " |")
L.append("| mean | " + " | ".join(f(x) for x in MEAN) + " |")
L.append("")
L.append("Toy comparison: toy step-3.7-flash Zharovia composite mean was 0.9911; "
         f"English mean is {f(MEAN[5])}.")
L.append("")
L.append("## Class 4 — §B.7 direct (flaw-only, tid=51; exact hits /12 per slice, bar ≥10/12)")
L.append("")
L.append("| slice | hits | nears | misses | score_x10 | pass |")
L.append("|---|---|---|---|---|---|")
tot_h = 0
for s in range(8):
    d = SLB[s]
    tot_h += d["hits"]
    L.append(f"| {s} | {d['hits']} | {d['nears']} | {d['misses']} | {d['score_x10']} | "
             + ("PASS" if d["pass"] else "FAIL") + " |")
L.append("")
L.append(f"Total: {tot_h}/96 flaw hits; slices passing strict bar: {RUNB[1]}/8. "
         f"(RUN line: total_hits={RUNB[0]}, total_pass={RUNB[1]}, fails={RUNB[2]})")
L.append("")
L.append("## Class 3 — teacher leg (tid=41; flaw-first then clean teaching)")
L.append("")
L.append("§B.7 per slice (flaw exam administered by the teacher):")
L.append("")
L.append("| slice | hits | nears | misses | pass |")
L.append("|---|---|---|---|---|")
tot_hc = 0
for s in range(8):
    d = SLC2[s]
    tot_hc += d["hits"]
    L.append(f"| {s} | {d['hits']} | {d['nears']} | {d['misses']} | "
             + ("PASS" if d["pass"] else "FAIL") + " |")
L.append("")
L.append(f"Total: {tot_hc}/96 flaw hits; slices passing strict bar: {RUNC[1]}/8.")
L.append("")
L.append("Teaching / mastery numbers:")
L.append("")
L.append("| slice | clean adopts | mastery/24 |")
L.append("|---|---|---|")
for s in range(8):
    d = SLC2[s]
    L.append(f"| {s} | {d['adopts']} | {d['mastery24']} |")
L.append("")
L.append(f"Totals: clean adopted={RUNC[2]}, final mastery={RUNC[3]}/192, fails={RUNC[4]}.")
L.append("")
L.append("Toy comparison: toy class-3 teach3 composite was 0.9822; the English teacher leg")
L.append(f"reaches final mastery {RUNC[3]}/192 with {RUNC[2]} clean adoptions and "
         f"{tot_hc}/96 flaw hits.")
L.append("")
L.append("## Verdict")
L.append("")
L.append("- §B.7 batteries (legs B and C) are value-agnostic: they operate on proposal")
L.append("  spans, grounding, and confidence only. They received NO content adaptation")
L.append("  for the English port — identical machinery to the Zharovia run.")
L.append("- Track-5 D2 battery: two-hop letter→position→wordlen chained lookup, the")
L.append("  English structural analog of the Zharovia landmark→ruler→year chain.")
L.append("- All legs ran N=5 byte-identical; pure Zag, zero RNG (static scan PASS).")
L.append("- Corpus is a frozen artifact of step-3.7-flash:free at temperature 0, seed 42;")
L.append("  claim reference is the trainer-supplied values in facts.json.")

out = os.path.join(STEP, "STEP_ENGLISH_VERDICT.md")
open(out, "w").write("\n".join(L) + "\n")
print("\n".join(L))
print(f"\nwrote {out}")
