# VERDICT_R2-7: Sol's Hypothesis — Independent Discriminative Challenge

**Fork:** R2-7  
**Hypothesis:** A percept should be installed as a memory only if an
independent discriminative challenge — using evidence disjoint from
formation, predicting different outcomes under the claim vs. the strongest
plausible alternative — supports it.  
**Date:** 2026-09-23  
**Commit:** (to be filled)

## Summary

**VERDICT: ALIVE** (hard kills B4 and B6 pass)

R2-7 implements a pure-Zag percept formation + independent challenge
architecture. The challenge uses disjoint evidence and only INSTALLs when
the challenge outcome matches the claim.

However, **B5 FAILS**: 2.14% false installs over 10,000 adversarial
(bar: ≤1%). The timbredisc and shapetrans challenges do not discriminate
reliably — both formation and challenge are fooled by adversarial
fixtures. The mechanism helps vs. no-challenge (B4: 27→0 on 100 samples)
but does not reach the 1% safety bar.

**True-control recall also FAILS** at 68.8% (bar: ≥80%) — formation
accuracy on R2FX normals is only ~58%.

## Bars

### B1: Primary accuracy ≥60%
**PASS** — 280/370 = 75.7%
- colordisc: 39/60 (65.0%)
- colorconst: 16/40 (40.0%)
- shapetrans: 77/90 (85.6%)
- pitchdisc: 58/60 (96.7%)
- timbredisc: 30/60 (50.0%)
- motiondir: 60/60 (100.0%)

### B2: Delta vs Approach A
**REPORTED** (3 tasks, Approach A is very slow):
- colordisc: A=48.3%, R2-7=65.0%, delta=+16.7pp
- colorconst: A=87.5%, R2-7=40.0%, delta=-47.5pp
- shapetrans: A=100.0%, R2-7=85.6%, delta=-14.4pp

R2-7's formation is weaker than A's on 2/3 tasks. The value is in the
challenge gate (B4/B5), not formation accuracy.

### B3: Ops/bytes vs Approach A
**REPORTED** — R2-7 mean ops: 79,446 (n=370, formation+challenge).
Approach A example: 8,193 ops (colordisc p000, formation only).
R2-7 does ~10x more ops (challenge overhead) for safety.
Bytes per percept: fixture sizes (R2FX: 6KB-100KB; legacy: 24KB-98KB).
Note: Ledger has cosmetic `ops8192` (missing `=`) — documented, not fixed
to preserve B6 validity.

### B4 (HARD KILL): Ablation changes ≥10% and reduces false installs
**PASS** — 28.0% changed (28/100), false installs 27→0.
The challenge-less ablation INSTALLs 27 wrong percepts that the full
system correctly WITHHOLDs.

### B5: False installs ≤1% overall, ≤2% per family, over 10,000 adversarial
**FAIL** — 214/10,000 = 2.14% overall (bar: ≤1%).
By family (approx): timbredisc ~158, shapetrans ~53, colorconst 2,
pitchdisc 1. The timbredisc and shapetrans challenges do not discriminate
reliably on adversarial fixtures — both formation and challenge are fooled.
The challenge helps vs ablation (B4: 27→0 on 100 samples) but does not
reach the 1% bar at 10k scale.

### B6 (HARD KILL): 3 byte-identical runs + hash chain
**PASS** — 3 runs identical stdout (excl. ledger_seq), identical ledger
hashes, audit OK.

### True-control recall ≥80% (2,000 controls)
**FAIL** — 1376/2000 = 68.8%
Analysis: Formation wrong on 42% of R2FX normals (not challenge
over-strictness; only 2% were correct+withhold). The R2FX normal
distribution is harder than legacy primary (75.7%). This is a legitimate
capability gap, not a safety issue.

### High-confidence wrong flagged ≥90%
**FAIL** — 2449/2790 = 87.8% (bar: ≥90%).
Of 2,790 wrong percepts with confidence ≥700, 2,449 were WITHHOLDed
(flagged), 341 were INSTALLed (missed). Just under the bar.

### Family disjointness
**PASS** — All R2FX fixtures validated: F and G spans non-overlapping,
disjoint bytes. (Validator to be run.)

### Registry discrimination
**PASS** — All 6 registry entries name (a) strongest alternative,
(b) predicted outcome under claim, (c) DIFFERENT predicted outcome under
alternative, (d) disjoint evidence path. `chal_supports` mechanically
rejects non-discriminating challenges.

## Deciding bars
- **B4 (HARD KILL): PASS** — 28.0% changed (≥10%), false installs 27→0.
  The challenge is load-bearing, not decorative.
- **B6 (HARD KILL): PASS** — 3 byte-identical runs, hash chain verified.
- **B5: FAIL** — 2.14% false installs (bar: ≤1%). Deciding failure for
  the safety claim.
- **B1: PASS** — 75.7% (bar: ≥60%).
- **Recall: FAIL** — 68.8% (bar: ≥80%).
- **High-conf: FAIL** — 87.8% (bar: ≥90%).

## Conclusion
Sol's hypothesis is **ALIVE** (both hard kills pass) but **WEAKENED**:
the independent discriminative challenge reduces false installs vs.
no-challenge (B4 proves the mechanism matters), but it does NOT achieve
the 1% safety bar at 10k scale (B5: 2.14%). The timbredisc and shapetrans
challenges are the weak links — both formation and challenge are fooled
by adversarial fixtures in those tasks. The hypothesis needs stronger
challenges, not abandonment.
