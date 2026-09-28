# PREREG — T-05 WORST-CASE POLARITY LOSS (direct test of the v2 mean-vs-maximum diagnosis)

- **Status:** FROZEN v1 — written BEFORE any T-05 training or measurement.
  Any change requires version bump + note + retrain + re-measure.
- **Date:** 2026-09-24
- **Crew:** H5 training-backlog crew (subagent b0e6708d)
- **Backlog entry:** HYPOTHESIS_BACKLOG_TRAINING.md T-05 (grok H-17).
  Kill bars verbatim from the backlog (§3). §4 records the loss-form
  substitution (MSE for log-loss) and the non-degeneracy guards — not
  bar changes, but load-bearing definitions.

## §1 Claim (verbatim from backlog)

Log loss cannot express "never": on a double-labeled (cloned-pair) state
it settles at c=1/2, and G=1/2 on a wrong O item still violates
L-OVERCONF. Only a worst-case loss over polarity pairs —
c ≤ min_polarities 1[correct], i.e. c=0 wherever either polarity is
wrong — matches the law's universal quantifier.

## §2 Mechanism (verbatim from backlog)

L-OVERCONF is a universal quantifier over items, not an average. The
training-side expression of the bind (not an escape from it): the
training signal uses both labels, the decision rule uses neither.

## §3 Kill bars (verbatim from backlog)

Worst-case arm leaves O G(64) > 0.1 or O V2 > 5% → KILLED. Or the
log-loss arm reaches G ≤ 0 on O → the "only worst-case" part of the
claim is KILLED.

## §4 Training intervention (frozen; v2 machinery, two-arm loss)

**v2 AMENDMENT (2026-09-24, before any 100× run — go/no-go FAILED on the
v1 design, diagnosed, amended):** the v1 design kept v2's G-batch and
theater guardrails. The 10× go/no-go failed on (d) both arms and (c-L):
the G-batch is a GLOBAL-bias instrument that (i) dominated the dynamics
(b → −27k, phase-C crushes / phase-A recovers oscillation), (ii) shifted
Arm L's fixed point far below 500 (6 at 10× — voiding the
substitution-validity check), and (iii) confounded attribution — any Arm
W "win" could be G-batch suppression, not worst-case loss. The theater
term likewise opposes Arm L's 500 fixed point on O wrong→wrong chains.
Both guardrails are REMOVED in v2. Both arms now run the backlog-literal
PURE per-cell loss (no G-batch, no theater). The claim under test is the
polarity aggregation (mean vs worst-case) — the guardrails were
confounds, not controls. Retrain + re-measure from scratch under v2.

**Common to both arms** (identical to PREREG_TRAINING_V2.md §4/§5 unless
noted): 8-feature linear head C = clamp((Σwᵢfᵢ)/1000 + b, 0, 1000);
init w1=1000/rest 0/b=0 (M4-with-harness-confidence start); frozen input
training/features/features.tsv (SHA-256 4682190c…65a897d); phases
A→B→C in fixed order (A=admit/revoke/logic/cost, B=P/D even, C=trap/O
even/redteam); heldout = odd replicates (never trained); 10× go/no-go
then 100× (600 epochs); DIV2=40000 representable updates; weight clamp
±2,000,000; M4 release skeleton FROZEN (answer channel untouched — the
confidence head is the only trainable locus, per v2 §1 scope delimiter).
Zero RNG; train A/B byte-compare; policy build A/B; eval legs A/B.
NO G-batch, NO theater term (v2 amendment — see above).

**Mirror construction.** Mirrorable families = {P, O} only — the
polarity pair of the backlog. Everywhere else (admit, revoke, logic,
cost, D, trap, redteam) is non-mirrorable and uses the ordinary
single-grade target in BOTH arms. (The backlog names logic/admit as
examples; the construction "clone prompt, flip label" is defined only
for the P/O pair, so D — a ceiling family with its own trajectory —
stays single-grade. Recorded explicitly so the choice is auditable.)

**Arm W (worst-case).** On a released P/O training cell the two grades
are (Y, 1−Y) — exactly one polarity is wrong, always — so "c=0 wherever
either polarity is wrong" gives target T=0 on EVERY released P/O cell:
L = (C−0)². On non-mirrorable cells: L = (C−Y)² with Y=1000/0
(v2-identical).

**Arm L (log-loss control).** On a released P/O training cell the
double-labeled log-loss optimum is the grade mean, T=500: L = (C−500)².
On non-mirrorable cells: v2-identical (C−Y)² form.

**Loss-form substitution (recorded, not hidden).** The backlog says
"log loss"; the program's frozen standard since v1/v2 is MSE, and the
claim's content is the AGGREGATION (mean vs worst-case over
polarities), not log-vs-square. Both arms use MSE so the ONLY
difference between arms is the polarity aggregation. If Arm L does not
settle at ≈500 on P/O cells, the substitution failed and the run is
void.

**10× go/no-go (per arm, pure form):** (a) final weights ≠ init;
(b) P/O mean conf moved toward the arm target — (b-W) < 300, (b-L) in
[300, 700]; (c) phase-A loss decreased pass 1 vs pass 0 (machinery
check; phase A has no P/O cells). Otherwise stop and diagnose.

## §5 Predicted observable (backlog, with program units)

- Arm W: released P/O cells at d32/d64 mean c < 50 (0.05); V2 = 0 and
  V1 = 0 on O; G(d) ≤ 0 on O at all depths; P accuracy trajectory still
  rises with depth (guaranteed by the frozen M4 skeleton — checked, not
  discovered; P becomes underconfident post-flip, allowed one-sided).
- Arm L: released P/O cells at d32/d64 mean c ≈ 500 (0.5); O G(64) ≈
  +0.5; law violated (V2 > 0 or strict G-rise on O).

## §6 Non-degeneracy guards (standing requirement from the H-0 re-verification)

The H-0 re-verification proved preregistered bars admit degenerate
compliance (conf=0 + abstention volume). T-05's Arm W is DESIGNED to
output ~0 on P/O — the guards below separate a genuine worst-case win
from degenerate suppression. If any guard fails, the law numbers are
reported but do NOT count as satisfying the kill bar:

- **D1 (no universal suppression):** at eval, on LOGIC released correct
  cells, Arm W keeps mean c ≥ 500 AND correct−wrong separation ≥ 200
  (v2's non-degeneracy bars, program units).
- **D2 (no mirror leakage):** the worst-case target touches ONLY P/O
  training cells. Post-hoc: per-family mean-c ratio Arm W / v2-100× —
  if logic or admit mean c falls by >50% vs v2-100×, the arm learned
  T-23-style global shrinkage, not worst-case polarity handling →
  reported as degenerate, kill bar NOT satisfied.
- **D3 (answer channel untouched):** release rule frozen; P d64 accuracy
  (released-only) within 0.10 of v2-100× P d64. Else the confidence
  loss leaked into the answer channel → run void as a
  confidence-only claim.
- **D4 (guardrail removal check):** v2-amended design has no theater and
  no G-batch; the log's v2/gviol columns must read 0 every epoch
  (confirms the confounds are actually off).

## §7 L-OVERCONF reading (recorded)

PRIMARY: strict — G(d+1) ≤ G(d) per family with zero V1/V2. The kill
bar's absolute thresholds (O G(64) ≤ 0.1, O V2 ≤ 5%) are evaluated as
stated under the strict reading; refined-reading numbers (G
zero-crossings, V1/V2) reported alongside. T-05's predicted observable
(G(d) ≤ 0 on O all d) satisfies both readings if achieved.

## §8 Deciding batteries

P and O (ceiling battery, depths 1,2,4,8,16,32,64); logic 264 + admit
248 (depths 1,2,4,8,16) as non-mirror controls; trap 127 + D 40
(D inside the ceiling battery; trap depths 1,2,4,8,16). 22 legs × 2
arms × A/B. Kill bar evaluated on the eval legs (live batteries =
held-out w.r.t. training by construction).

## §9 Deliverables

(a) this prereg; (b) train5.zag + A/B build SHAs; (c) per-arm 10×/100×
params + logs, A/B byte-identical; (d) per-arm policy binaries A/B
byte-identical; (e) eval legs A/B byte-identical; (f) RESULTS_T05.md
(kill-bar evaluation under both readings, guard outcomes,
predicted-observable check); (g) VERDICT_T05.md.

---
*End of PREREG_T05.md v1 — 2026-09-24, frozen before any T-05 training.*
