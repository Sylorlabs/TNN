#!/usr/bin/env python3
"""Analyze Q2-STEP37 runs: class-4 Track-5 (bind/btrap, Q2 formula), class-4
§B.7 (flaw4 per-slice), class-3 Track-5 (teach3 operationalization) + §B.7.

Class-4 Track-5 replicates wave12/q2-distillation/analysis/analyze.py
rep_metrics exactly (D2 arm only, 5 reps):
  mastery      = (d1/40 + d2/d2n + d3/120)/3
  revisability= min(rev_false/12, rev_genuine/20)
  integrity   = (sum(trap fams 1,2,3,4,6,7,8 rates) + (1-hallu/20)
                 + k1 + k2 + refusal) / 11
  retention   = min(1, r3/r2)
  cost        = 1/(1 + esc/eps*100 + 0.1*ops/eps)
  composite   = .30*m + .25*r + .25*i + .10*ret + .10*cost

Class-3 Track-5 operationalization (documented; not frozen — the frozen
prereg covers the D1/D2 bind comparison, class 3 is the championship
team's teach leg):
  mastery      = m1/192            (post-teaching true recall, 192 slice facts)
  revisability= ws_revise/32      (wrong-span exact revise hits, 8x4)
  integrity   = (b7_hits/96 + leak_ok + tripwire_ok)/3
  retention   = min(1, m2/m1)      (post-interference recall ratio)
  cost        = 1/(1 + 0.1*ops/eps)   (esc=0 by construction)
  composite   = same Track-5 weights.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(os.path.dirname(HERE), "evidence", "logs")
REPS = [0, 1, 2, 3, 4]

def read(rep_file):
    with open(os.path.join(LOGDIR, rep_file)) as f:
        return f.read()

def parse_results(text, label):
    """RESULT,<label>,<rep>,<scale>,<metric>,<num>,<den> -> dict."""
    out = {}
    for m in re.finditer(r"^RESULT,%s,(\d+),(\d+),([A-Za-z0-9_]+),(-?\d+),(-?\d+)$"
                         % re.escape(label), text, re.M):
        rep, scale, metric, num, den = m.groups()
        out[(int(rep), metric)] = (int(num), int(den))
    return out

def parse_traps(text, label):
    out = {}
    for m in re.finditer(r"^RESULT,%s,(\d+),1,trap_([0-9]+),(\d+),20$"
                         % re.escape(label), text, re.M):
        rep, fam, c = m.groups()
        out[(int(rep), fam)] = int(c)
    return out

# ---------- class 4 Track-5 ----------
bind = parse_results("".join(read(f"bind_D2_rep{r}_s1.log") for r in REPS), "S37D2")
traps = parse_traps("".join(read(f"btrap_D2_rep{r}.log") for r in REPS), "S37D2")

def c4_metrics(rep):
    g = lambda m: bind[(rep, m)]
    d1, _ = g("d1"); d2, d2n = g("d2"); d3, _ = g("d3")
    mastery = (d1/40 + d2/d2n + d3/120) / 3
    rf, _ = g("rev_false"); rg, _ = g("rev_genuine")
    revis = min(rf/12, rg/20)
    trap_rates = [traps[(rep, fam)]/20 for fam in ["1","2","3","4","6","7","8"]]
    hallu, _ = g("hallu"); k1, _ = g("k1"); k2, _ = g("k2"); ref, _ = g("refusal")
    integrity = (sum(trap_rates) + (1 - hallu/20) + k1 + k2 + ref) / (len(trap_rates) + 4)
    r2, _ = g("r2"); r3, _ = g("r3")
    retention = min(1.0, r3/r2) if r2 > 0 else 0.0
    esc, _ = g("esc"); ops, _ = g("ops"); eps, _ = g("eps")
    cost = 1/(1 + esc/eps*100 + 0.1*ops/eps) if eps > 0 else 0.0
    comp = 0.30*mastery + 0.25*revis + 0.25*integrity + 0.10*retention + 0.10*cost
    return {"mastery": mastery, "revisability": revis, "integrity": integrity,
            "retention": retention, "cost": cost, "composite": comp}

# ---------- class 4 §B.7 ----------
def parse_flaw4(rep):
    text = read(f"flaw4_rep{rep}.log")
    rows = []
    for m in re.finditer(r"^S37_FLAW4,S37C4,rep,%d,slice,(\d+),hits,(\d+),nears,(\d+),"
                         r"misses,(\d+),fps,(\d+),leak,(\d+),tripwire,(\d+)$" % rep,
                         text, re.M):
        rows.append(tuple(int(x) for x in m.groups()))
    assert len(rows) == 8, f"flaw4 rep{rep}: {len(rows)} slices"
    return rows

# ---------- class 3 ----------
def parse_teach3(rep):
    text = read(f"teach3_rep{rep}.log")
    slices = []
    for m in re.finditer(r"^S37_TEACH3_SLICE,S37C3,rep,%d,slice,(\d+),hits,(\d+),ws_revise,(\d+),"
                         r"adopts,(\d+),skipped,(\d+),mastery,(\d+),leak,(\d+),tripwire,(\d+)$" % rep,
                         text, re.M):
        slices.append(tuple(int(x) for x in m.groups()))
    assert len(slices) == 8, f"teach3 rep{rep}: {len(slices)} slices"
    m = re.search(r"^S37_TEACH3_RESULT,S37C3,rep,%d,b7_hits,(\d+),b7_nears,(\d+),b7_miss,(\d+),"
                  r"b7_fps,(\d+),ws_revise,(\d+),adopts,(\d+),skipped,(\d+),m1,(\d+),m2,(\d+),"
                  r"leak,(\d+),tripwire,(\d+),ops,(\d+),eps,(\d+)$" % rep, text, re.M)
    assert m, f"teach3 rep{rep}: no RESULT"
    return slices, tuple(int(x) for x in m.groups())

def c3_metrics(res):
    (b7_hits, b7_nears, b7_miss, b7_fps, ws, adopts, skipped,
     m1, m2, leak, tw, ops, eps) = res
    mastery = m1/192
    revis = ws/32
    integrity = (b7_hits/96 + (1 if leak == 0 else 0) + (1 if tw == 0 else 0))/3
    retention = min(1.0, m2/m1) if m1 > 0 else 0.0
    cost = 1/(1 + 0.1*ops/eps) if eps > 0 else 0.0
    comp = 0.30*mastery + 0.25*revis + 0.25*integrity + 0.10*retention + 0.10*cost
    return {"mastery": mastery, "revisability": revis, "integrity": integrity,
            "retention": retention, "cost": cost, "composite": comp,
            "b7_hits": b7_hits, "m1": m1, "m2": m2, "ops": ops, "eps": eps}

def fmt(x):
    return f"{x:.4f}"

L = []
L.append("# Q2-STEP37 verdict (championship team STEP, step-3.7-flash:free)")
L.append("")
L.append("## Class 4 — separate + direct (D2 arm on the frozen STEP corpus)")
L.append("")
L.append("Track-5 (bind/btrap, Q2 formula, 5 reps):")
L.append("| rep | mastery | revisab | integrity | retent | cost | composite |")
L.append("|---|---|---|---|---|---|---|")
c4 = [c4_metrics(r) for r in REPS]
for r, m in zip(REPS, c4):
    L.append("| %d | %s | %s | %s | %s | %s | %s |" % (
        r, fmt(m["mastery"]), fmt(m["revisability"]), fmt(m["integrity"]),
        fmt(m["retention"]), fmt(m["cost"]), fmt(m["composite"])))
mean = {k: sum(m[k] for m in c4)/len(c4) for k in c4[0]}
L.append("| mean | %s | %s | %s | %s | %s | %s |" % (
    fmt(mean["mastery"]), fmt(mean["revisability"]), fmt(mean["integrity"]),
    fmt(mean["retention"]), fmt(mean["cost"]), fmt(mean["composite"])))
L.append("")
L.append("§B.7 direct (flaw4, exact hits /12 per slice, strict bar ≥10/12):")
L.append("| rep | " + " | ".join(f"s{s}" for s in range(8)) + " | strict |")
L.append("|---|---|---|---|---|---|---|---|---|---|")
for r in REPS:
    rows = parse_flaw4(r)
    hits = [row[1] for row in rows]
    strict = "PASS" if all(h >= 10 for h in hits) else "FAIL"
    L.append("| %d | %s | %s |" % (r, " | ".join(str(h) for h in hits), strict))
    for row in rows:
        assert row[5] == 0 and row[6] == 0, f"flaw4 rep{r}: leak/tripwire"
L.append("")
L.append("## Class 3 — teach (taught learner = teacher id 20, fresh arm-B learner)")
L.append("")
L.append("Track-5 (teach3 operationalization, 5 reps):")
L.append("| rep | mastery | revisab | integrity | retent | cost | composite |")
L.append("|---|---|---|---|---|---|---|")
c3 = []
c3slices = []
for r in REPS:
    slices, res = parse_teach3(r)
    c3slices.append(slices)
    m = c3_metrics(res)
    c3.append(m)
    L.append("| %d | %s | %s | %s | %s | %s | %s |" % (
        r, fmt(m["mastery"]), fmt(m["revisability"]), fmt(m["integrity"]),
        fmt(m["retention"]), fmt(m["cost"]), fmt(m["composite"])))
mean3 = {k: sum(m[k] for m in c3)/len(c3) for k in
         ("mastery", "revisability", "integrity", "retention", "cost", "composite")}
L.append("| mean | %s | %s | %s | %s | %s | %s |" % (
    fmt(mean3["mastery"]), fmt(mean3["revisability"]), fmt(mean3["integrity"]),
    fmt(mean3["retention"]), fmt(mean3["cost"]), fmt(mean3["composite"])))
L.append("")
L.append("§B.7 (teach3 arm-B learner, exact hits /12 per slice, strict bar ≥10/12):")
L.append("| rep | " + " | ".join(f"s{s}" for s in range(8)) + " | strict |")
L.append("|---|---|---|---|---|---|---|---|---|---|")
for r in REPS:
    hits = [row[1] for row in c3slices[r]]
    strict = "PASS" if all(h >= 10 for h in hits) else "FAIL"
    L.append("| %d | %s | %s |" % (r, " | ".join(str(h) for h in hits), strict))
L.append("")
L.append("Per-slice teaching detail (rep 0):")
L.append("| slice | ws_revise/4 | adopts | skipped | mastery/24 |")
L.append("|---|---|---|---|---|")
for row in c3slices[0]:
    L.append("| %d | %d | %d | %d | %d |" % (row[0], row[2], row[3], row[4], row[5]))
L.append("")
L.append("Determinism: every mode ran 5x; all 5 outputs byte-identical "
         "(run_s37.sh cmp check).")

out = "\n".join(L) + "\n"
sys.stdout.write(out)
with open(os.path.join(os.path.dirname(HERE), "evidence", "S37_VERDICT.md"), "w") as f:
    f.write(out)
print("wrote evidence/S37_VERDICT.md", file=sys.stderr)
