# F-B Kill Evaluation — DRAFT (pending M3)

## Disjunct 1: M3 < C-W's

**C-W M3** (scorecard_r1_1x.json):
- m3_survival_tenths: 100.0
- m3_fresh_recall_tenths: 100.0

**F-B M3** (pending):
- Expected: 100.0 / 100.0 (deterministic mechanism, valuable pinned).

**Evaluation:**
- If F-B = 100.0: NOT < C-W's 100.0 → disjunct does NOT fire.
- If F-B < 100.0: disjunct FIRES → KILLED.

The "both corpora" phrasing: C-W exposes a single combined M3 (not per-corpus).
F-B's M3 is also combined (1000 valuable across both corpora). The comparison
is on the combined metric. This ambiguity is documented; the mechanical
reading (F-B_M3 < C-W_M3) is applied.

## Disjunct 2: Within noise of F-S on all metrics

**"Within noise" operationalization:** Absolute difference < 0.5 percentage
points. Rationale: deterministic zero-RNG system; any difference ≥0.5 is
mechanism-driven, not noise. Documented here as the binding interpretation.

**F-S metrics** (scorecard_r1_1x.json):
| Metric | Prose | Code |
|--------|-------|------|
| M1 recall | 100.0 | 100.0 |
| M1 boundary | 100.0 | 100.0 |
| M2 content | 100.0 | 100.0 |
| M2 boundary | 100.0 | 100.0 |
| M3 survival | 100.0 | (combined) |
| M3 fresh | 100.0 | (combined) |
| M4 | 100.0 | 100.0 |
| M6 tax | 0.0 | 0.0 |

**F-B metrics** (pending, expected):
- M1/M2/M3/M4: 100.0 (deterministic)
- M6 tax: 0.0 (stateless)
- M5: FAIL (high ratio) — F-S did not report M5; cannot compare.
- M7: N/A (dedup) — F-S reported 50.0; different.

**Evaluation:**
- On M1/M2/M3/M4/M6: If F-B = F-S = 100.0/0.0, they are within noise.
- On M5: F-S has no data; the "all metrics" condition cannot be fully
  evaluated. Documented as an ambiguity.
- On M7: F-B is N/A (dedup); F-S is 50.0. Different, but M7 is not a
  "metric" in the kill-relevant sense (it's a capability probe).

**Preliminary:** If F-B matches F-S on M1/M2/M3/M4/M6 (all 100.0/0.0),
disjunct 2 FIRES → KILLED (redundant). The M5/M7 ambiguities do not save
it because the core metrics (M1-M4, M6) are identical.

**Counter-consideration:** F-B is the "cheaper sibling" — if F-B's M5 cost
were LOWER than F-S's, it would differentiate. But F-S did not report M5,
and F-B's M5 FAILs the bar. There is no evidence F-B is cheaper. The
"cheaper" hypothesis is not supported.

## Verdict implication

- If disjunct 1 fires: KILLED (worse than baseline).
- Else if disjunct 2 fires: KILLED (redundant vs F-S).
- Else if M5 fails: FAIL (not killed, but not passing).
- Else: PASS.

Expected: Disjunct 2 fires → **KILLED**.

## Addendum: Chunk-count difference

F-S prose: 211 chunks. F-B prose: ~4,311,129 chunks (20,000× more).

This is a VAST mechanistic difference, but it does not affect the kill
evaluation because:
1. The frozen kill criterion specifies "metrics" (M1-M9 scores), not
   descriptive statistics like chunk counts.
2. Chunk count manifests as M5 cost (which F-B FAILs). The cost is scored
   separately.
3. The redundancy rationale ("keep F-S, retire F-B") holds: if F-B achieves
   the same capability scores at 20,000× the chunk count (and higher M5 cost),
   it is not the "cheaper sibling" — it is a more expensive way to get the
   same scores.

The 20,000× difference is documented here as evidence that the mechanisms
are distinct, but the binding kill criterion is on the metric scores.

## CONFIRMED 2026-09-21: F-B M3 = 100.0 / 100.0

**F-B M3** (battery_out/m3-1x.r1.txt):
- m3_survival_tenths: 100.0
- m3_fresh_recall_tenths: 100.0
- m3_mgmt_entries: 8050 (field name to be corrected to m3_mgmt_entries)
- m3_weaken_handled: 50
- m3_freeze: 0

**Disjunct 1 evaluation:**
- C-W M3: 100.0 / 100.0
- F-B M3: 100.0 / 100.0
- 100.0 < 100.0? FALSE.
- **Disjunct 1 does NOT fire.**

**Disjunct 2 (partial):**
- F-S M3: 100.0 / 100.0
- F-B M3: 100.0 / 100.0
- Difference: 0.0 < 0.5 → within noise on M3.
- Awaiting M1/M2/M4/M6 for full evaluation.

## CONFIRMED 2026-09-21: F-B M1 prose = 100.0 / 100.0

**F-B M1 prose** (battery_out/m1-1x-prose.r1.txt):
- m1_recall_tenths: 100.0
- m1_boundary_tenths: 100.0
- m1_units: 4,402,039

**F-S M1 prose:** 100.0 / 100.0, 211 units.

**Within noise:** YES (Δ=0.0 on scores).

## CONFIRMED 2026-09-21: F-B M1 code = 100.0 / 100.0

**F-B M1 code:** 100.0 / 100.0, 5,287,970 units.
**F-S M1 code:** 100.0 / 100.0, 17,156 units.
**Within noise:** YES.

## CONFIRMED 2026-09-21: F-B M2 t1 = 100.0 / 100.0

**F-B M2 t1 prose:** 100.0 / 100.0, m9_shape=fast-then-flat.
**F-B M2 t1 code:** 100.0 / 100.0.
**F-S M2 t1:** 100.0 / 100.0.
**Within noise:** YES.

Service restart 2026-09-21 ~21:45 UTC killed the mode runner.
Restarted remaining modes (m2-t2 onward).

## CONFIRMED 2026-09-21: F-B M2 t2 = 100.0 / 100.0

**F-B M2 t2 prose:** 100.0 / 100.0.
**F-B M2 t2 code:** 100.0 / 100.0.
**Within noise:** YES (vs F-S 100.0).

## CONFIRMED 2026-09-21: F-B M2 t3 = 100.0 / 100.0

**F-B M2 t3-1x:** 100.0 / 100.0, 1 episode.
**Within noise:** YES.

## CONFIRMED 2026-09-21: F-B M4 = 100.0 / 100.0

**F-B M4 prose:** 100.0 / 100.0 (rev_boundary/rev_content).
**F-B M4 code:** 100.0 / 100.0.
**F-S M4:** 100.0 / 100.0.
**Within noise:** YES.

Note: M4 ran with old binary (field names m4_boundary_recall_tenths etc.);
values are 100.0. Post-processing will rename to m4_rev_*.

## CONFIRMED 2026-09-21: F-B M6 p2c = 100.0 / 100.0, tax 0.0

**F-B M6 p2c:** rec=100.0, bnd=100.0, rev=100.0, tax=0.0.
**F-S M6 p2c:** tax=0.0 (from scorecard).
**Within noise:** YES.
**Memorizer:** 0 matches, ok=1 (vacuous negative control works).

## CONFIRMED 2026-09-21: F-B M6 c2p = 100.0 / 100.0, tax 0.0

**F-B M6 c2p:** rec=100.0, bnd=100.0, rev=100.0, tax=0.0.
**Within noise:** YES.

## KILL EVALUATION COMPLETE

**Disjunct 1 (M3 < C-W's):** DOES NOT FIRE (100.0 !< 100.0).
**Disjunct 2 (within noise of F-S on all metrics):** FIRES.

All capability metrics (M1, M2, M3, M4, M6) are 100.0 for both F-B and F-S,
differences 0.0 < 0.5. F-B is redundant vs F-S per the frozen criterion.

**Binding verdict: KILLED.**
