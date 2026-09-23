#!/usr/bin/env python3
"""SWE-ENGLISH class-4 analysis: Track-5 M2 composite (legA, arm 4 / D2).

Port of the toy-SWE class-4 analysis with the English domain:
  t5_cat: 4 categories (48/96/144 boundaries)
  claims: facts.json SUPPLIED values (trainer's records; 228 true + 12 false)
  truth:  facts.json supplied for the 228 true ids; ground_truth_notes.md
          true values for the 12 false ids (harness-side only)

Reads legs/legA/evidence/logs/*.log (RESULT/DIGEST/CORPUS_SHA256 lines).
Log files: swe4_r{rep}_n{i}.log / swe4_btrap_r{rep}_n{i}.log, rep 0..4, i 1..5.
All 5 runs of each (rep, mode) must be byte-identical (N=5, pure Zag, no RNG).

Weights (Micah-approved 2026-09-20):
  mastery      = mean(d1/40, d2/d2n, d3/120)
  revisability = min(rev_false/12, rev_genuine/20)
  integrity   = mean(all applicable btrap D2 family rates, 1-hallu/20,
                    K1, K2, refusal)
  retention   = min(1, r3/r2) (0 if r2 == 0)
  cost        = 1/(1 + esc/eps*100 + 0.1*ops/eps)
  composite   = 0.30*M + 0.25*R + 0.25*I + 0.10*ret + 0.10*cost
Writes legs/legA/analysis/CLASS4_RESULTS.md. Fails loudly on gate breaches.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEGA = os.path.dirname(HERE)
SWE = os.path.dirname(os.path.dirname(LEGA))
LOGDIR = os.path.join(LEGA, "evidence", "logs")
CORPUS_SHA = open(os.path.join(SWE, "corpus", "SHA256.txt")).read().strip()

# ---------- English domain (mechanical; from frozen facts) ----------
facts = json.load(open(os.path.join(SWE, "..", "corpus-input",
                                    "facts.json")))
FALSE_IDS = set(facts["false_ids"])
assert FALSE_IDS == {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}
SUPPLIED = {i: facts[str(i)]["value"] for i in range(240)}


def t5_cat(i):
    if i < 48:
        return 0
    if i < 96:
        return 1
    if i < 144:
        return 2
    return 3


# ---------- lawful per-rep sets (category-agnostic; verbatim from the
#             toy-SWE analysis, which mirrors q2_trial.zag) ----------
def q2_seed_id(k):
    if k == 42:
        return 29
    if k == 43:
        return 80
    if k == 44:
        return 117
    if k == 45:
        return 163
    if k == 46:
        return 205
    if k == 47:
        return 231
    count = 0
    for i in range(240):
        cid = (i * 5) % 240
        if cid not in FALSE_IDS:
            if count == k:
                return cid
            count += 1
    return -1


_SEEDS = {q2_seed_id(k) for k in range(48)}


def q2_pool_id(k):
    count = 0
    for i in range(240):
        if i not in FALSE_IDS and i not in _SEEDS:
            if count == k:
                return i
            count += 1
    return -1


def q2_heldout(rep, k):
    return q2_pool_id((rep * 17 + k * 37) % 186)


def q2_ho_set(rep):
    return {q2_heldout(rep, k) for k in range(12)}


# ---------- parse logs ----------
RES = {}
DIGESTS = {}
FILEHASH = {}
N_RUNS = 5
for fn in sorted(os.listdir(LOGDIR)):
    if not fn.endswith(".log"):
        continue
    path = os.path.join(LOGDIR, fn)
    h = hashlib.sha256()
    with open(path) as f:
        for line in f:
            h.update(line.encode())
            line = line.strip()
            m = re.match(r"RESULT,(\w+),(\d+),(\d+),([\w_]+),(-?\d+),(-?\d+)",
                         line)
            if m:
                RES[(m.group(1), int(m.group(2)), int(m.group(3)),
                     m.group(4))] = (int(m.group(5)), int(m.group(6)))
            m2 = re.match(r"DIGEST,(\w+),(\d+),(\d+),([0-9a-f]+)", line)
            if m2:
                DIGESTS[(m2.group(1), int(m2.group(2)),
                         int(m2.group(3)))] = m2.group(4)
            m3 = re.match(r"CORPUS_SHA256,(\w+),([0-9a-f]+)", line)
            if m3 and m3.group(2) != CORPUS_SHA:
                sys.exit(f"FATAL: corpus sha mismatch in {fn}")
    FILEHASH[fn] = h.hexdigest()


def get(label, rep, scale, metric):
    return RES[(label, rep, scale, metric)]


def R(label, rep, scale, metric):
    num, den = get(label, rep, scale, metric)
    return num / den if den else 0.0


out = []
out.append("# SWE-ENGLISH class-4 results (Track-5 M2 composite, arm 4 / D2)")
out.append("")
out.append("Source model: swe-1-6-slow:free ONLY (frozen corpus "
           "english-championship-v1).")
out.append("")

D2_FAMS = ["1", "2", "3", "4", "6", "7", "8"]
LABEL = "SWE4"

# byte-identity: all 5 runs per (rep, mode) must be full-file byte-identical
for rep in range(5):
    for kind in ("", "_btrap"):
        hs = {FILEHASH[f"swe4{kind}_r{rep}_n{i}.log"] for i in range(1, 6)}
        if len(hs) != 1:
            sys.exit(f"FATAL: byte-identity breach: swe4{kind}_r{rep}_n*")
    out.append(f"rep {rep}: bind 5/5 + btrap 5/5 byte-identical")

composites = []
comp_parts = []
for rep in range(5):
    M = (R(LABEL, rep, 1, "d1") + R(LABEL, rep, 1, "d2")
         + R(LABEL, rep, 1, "d3")) / 3.0
    Rr = min(R(LABEL, rep, 1, "rev_false"), R(LABEL, rep, 1, "rev_genuine"))
    fam_rates = [R(LABEL, rep, 1, "trap_" + f) for f in D2_FAMS]
    I = (sum(fam_rates) + (1.0 - R(LABEL, rep, 1, "hallu"))
         + R(LABEL, rep, 1, "k1") + R(LABEL, rep, 1, "k2")
         + R(LABEL, rep, 1, "refusal")) / (len(D2_FAMS) + 4)
    r2n, _ = get(LABEL, rep, 1, "r2")
    r3n, _ = get(LABEL, rep, 1, "r3")
    ret = min(1.0, r3n / r2n) if r2n else 0.0
    esc, eps = get(LABEL, rep, 1, "esc")
    ops, _ = get(LABEL, rep, 1, "ops")
    cost = 1.0 / (1.0 + (esc / eps) * 100.0 + 0.1 * (ops / eps)) if eps else 0.0
    comp = 0.30 * M + 0.25 * Rr + 0.25 * I + 0.10 * ret + 0.10 * cost
    composites.append(comp)
    comp_parts.append((M, Rr, I, ret, cost))
    out.append(f"rep {rep}: M={M:.4f} R={Rr:.4f} I={I:.4f} ret={ret:.4f} "
               f"cost={cost:.4f} composite={comp:.4f} "
               f"(esc={esc} eps={eps} ops={ops})")
    # §6 gates (mechanical)
    d1n, d1d = get(LABEL, rep, 1, "d1")
    if d1d != 40 or d1n < 32:
        sys.exit(f"FATAL: rep {rep} mastery gate: {d1n}/{d1d}")
    if R(LABEL, rep, 1, "hallu") >= 0.05:
        sys.exit(f"FATAL: rep {rep} hallucination gate")
    if get(LABEL, rep, 1, "k1")[0] != 1 or get(LABEL, rep, 1, "k2")[0] != 1:
        sys.exit(f"FATAL: rep {rep} K1/K2 gate")
    if R(LABEL, rep, 1, "refusal") != 1.0:
        sys.exit(f"FATAL: rep {rep} refusal gate")
    for f in D2_FAMS:
        if R(LABEL, rep, 1, "trap_" + f) != 1.0:
            sys.exit(f"FATAL: rep {rep} btrap family {f} != 20/20")

mean_comp = sum(composites) / len(composites)
n = len(composites)
means = [sum(p[i] for p in comp_parts) / n for i in range(5)]
out.append("")
out.append(f"class-4 composite mean over 5 reps: {mean_comp:.4f}")
out.append(f"component means: M={means[0]:.4f} R={means[1]:.4f} "
           f"I={means[2]:.4f} ret={means[3]:.4f} cost={means[4]:.4f}")
out.append("class-4: no kill clauses tripped (all gates mechanical PASS)")
out.append("")
for rep in range(5):
    dg = DIGESTS[(LABEL, rep, 1)]
    out.append(f"rep {rep} store digest: {dg[:16]}... (5/5 byte-identical)")

with open(os.path.join(HERE, "CLASS4_RESULTS.md"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
print("CLASS4_RESULTS.md written; all gates PASS")
