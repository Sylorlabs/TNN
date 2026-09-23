# C7 Redesign Directions — Design-Level Assessment

Date: 2026-09-20. Status: DESIGN ONLY. No implementation, no amendments,
no runs. For Micah's morning review.

## Direction 1: Non-inferiority bar (`cap5 >= cap4`)

**What it requires:** Bar change only. Prereg amendment with Micah's tap.
No mechanism change. No fresh run (can re-evaluate committed S10 data).

**No-rescue standing:** SOFTENS the bar (== → >=). BUT: under the current
(buggy) metric, S10 reads 914→897, so cap5 < cap4 → still FIRED. Direction 1
alone does not flip the outcome. It is a statistical correction — "survives
withdrawal" was never an equality claim — not a rescue. Risk: if combined
with a metric fix, the softer bar makes a flip easier; the combination needs
explicit scrutiny.

**Cost:** Minimal (amendment + re-analysis).

## Direction 2: Budget separation (separate cid budgets)

**What it requires:** Mechanism change (separate claim-id budgets for forced
vs proactive hypotheses) + full fresh S10 run + re-validation of all
controls + prereg amendment.

**No-rescue standing:** NEUTRAL to STRENGTHENING. This fixes the confound at
the source (no displacement possible), making forced-exclusion arithmetically
coherent. It does not soften any bar or redefine any metric — it changes the
system so the existing concepts apply cleanly. Deep-dive calls it "cleanest."

**Cost:** HIGH. Code change, full S10 re-run (hours), re-validate the entire
battery, new committed evidence. Also changes the system under test, so
prior S10 evidence does not transfer directly.

## Direction 3: Drop the double-count (`cap` = cok + ccon + mhyp)

**What it requires:** Metric change only. Prereg amendment with Micah's tap.
No mechanism change. Re-score committed S10 data (no fresh run needed).

**No-rescue standing:** CORRECTION of an objective mathematical bug — but it
FLIPS the S10 outcome (897→897 ALIVE), so it triggers no-rescue scrutiny.
The bug: L1 hypotheses counted twice (in mhyp AND tr.l1_opened), proven at
source level, predates the C5 redesign (baseline DC-2 had 12 double-counted).
Fixing it is symmetric and not outcome-driven — we would fix this bug even
if C7 had passed. It does not soften the bar (== stays). It does not address
displacement (622 vs 639 proactive remains invisible to the metric), but for
C7's question (teacher-dependence, not gate cost) that is correct scoping:
displacement is telemetry, not a bar input.

**Cost:** LOW. Amendment + re-score of committed data.

## Direction 4: Split the control (C7a withdrawal vs C7b asymmetry telemetry)

**What it requires:** Control-design change + prereg amendment. C7a keeps a
strict withdrawal comparison; C7b gets its own displacement bar as telemetry.
May need design work to isolate a "clean" withdrawal comparison and new runs
to baseline C7b.

**No-rescue standing:** NEUTRAL. Directly addresses the deep-dive's core
finding (control-design flaw under asymmetric mechanisms) rather than
patching the metric. Does not soften C7a; adds C7b as a new constraint.

**Cost:** MEDIUM-HIGH. Design work + possible new runs for C7b baselines.
Most new thinking required; most discretion in the design.

## Ranking (most principled first)

1. **Direction 3** — Objective mathematical bug fix; zero discretion;
   symmetric; proven at source; predates the controversy. The only direction
   that is "wrong to NOT fix" regardless of outcome.
2. **Direction 1** — Statistically correct formulation, but a judgment call
   about the right test; alone changes nothing in S10.
3. **Direction 2** — Cleanest mechanism fix, but high cost and invalidates
   prior S10 evidence by changing the system.
4. **Direction 4** — Addresses the deepest flaw but requires the most new
   design discretion.

**Recommendation:** Direction 3 (+ Direction 1 as companion — the deep-dive
pairs them as "cheapest"). Direction 3 fixes the ruler; Direction 1 fixes
the test. Together they give a coherent C7 without touching the system.
The flip (FAIL→ALIVE) must be Micah's explicit call, not automatic.
