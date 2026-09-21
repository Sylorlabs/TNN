# G2 VERDICT — KILLED

**Date:** 2026-09-21
**Arm:** G2 — Deliberate cuts under pressure (family DELIBERATE)
**Binding criterion (frozen, `ALPHABET_G-L.md:145-147`, `briefs/G2.json`):**

> Recall-quality advantage over G1 at matched occupancy < 2 absolute points on byte-exact recall,
> OR deliberation cost per pressure event > 50× G1's sweep with no quality advantage — deliberation buys nothing.

## Adjudication

### Branch 1 — recall-quality advantage (FIRES → KILL)

Byte-exact recall at matched occupancy (identical corpora, identical unit counts):

| Corpus | G1 recall | G2 recall | Advantage (G2 − G1) |
|--------|-----------|-----------|---------------------|
| prose (84,731 units) | 100.0 | 100.0 | **0.0** |
| code (148,678 units) | 100.0 | 100.0 | **0.0** |

0.0 < 2 absolute points. **Branch 1 fires. The arm is killed.**

Under M3 pressure the picture is worse, not better: valuable survival is 100.0 for both arms, but fresh recall is 94.6 (G1) vs 0.0 (G2, `FROZEN-UNDER-PRESSURE`). G2's deliberation did not buy recall quality anywhere it was measured.

### Branch 2 — deliberation cost (does not fire; recorded for completeness)

- G2 deliberation cost: 258 ledger entries per pressure session (2 sessions, 516 entries in M3).
- G1 has no deliberation; its M3 management total is 18,590 entries. No reading of "sweep" puts G2's per-event cost above 50× G1's.
- "No quality advantage" holds (0.0 points), but the cost-ratio prong does not. Branch 2 does not fire. The OR is already satisfied by branch 1.

## Result

**G2 is KILLED by branch 1 of its frozen kill criterion.** Deliberation bought nothing: zero recall advantage at matched occupancy, and under churn pressure the arm froze while the non-deliberating comparator kept 94.6 fresh recall.

No 10x. No appeal — the criterion is binding and was applied literally.

## Evidence

- `work/runs/leg_m1_1x_prose/a/stdout.txt` — `m1_recall_tenths: 1000, m1_boundary_tenths: 1000`
- `work/runs/leg_m1_1x_code/a/stdout.txt` — `m1_recall_tenths: 1000, m1_boundary_tenths: 1000`
- `work/runs/leg_m3_1x/a/stdout.txt` — `FROZEN-UNDER-PRESSURE`, `delib_entries=516`
- G1 comparator: `units/arms/G1/ARM_SPEC.md` (M1 100.0/100.0 both corpora; M3 fresh 94.6)
- Scorecard: `scorecard.json`
