# VERDICT — Leg B: F5 tightened-window 35-window sweep

**Frozen prereg:** `PREREG_CREW6_HELD.md` §§B.1–B.5 (committed alone as
`8f4285f486f196daf01e4c435a61a9a0b857862e`, branch `tnn-native-lab`).
**Date:** 2026-09-25. **Authorization:** Micah's 2026-09-24 order — test evidence
only; ADOPTION of the F5 window is NOT resolved by this verdict.

## B.3 decision rule, applied mechanically

**OVERTURN the NO-GO** iff there EXISTS a swept window with ALL THREE:
retention ≥ 8/9, over-block ≤ 25% (≤ 75/300), far-control 0/60. Otherwise
CONFIRM the NO-GO.

### Decision: **OVERTURN the NO-GO**

Window **(rc=150, rm=1000)** satisfies all three bars:

| Bar (B.3) | Measured at (150,1000) | Result |
|---|---|---|
| retention ≥ 8/9 | 8/9 false accepts blocked | ✓ |
| over-block ≤ 25% (≤75/300) | 66/300 = 22.0% | ✓ |
| far-control 0/60 | 0/60 | ✓ |

The blocked-false set at (150,1000) is byte-identical to the frozen (150,2000)
set (8 falses, all via exemplar 10983; verified by diffing per-trial outputs).
true_blocked = 0/34 — no correct backtest candidate is blocked at any window.

## Full 35-window sweep data (retention vs over-block)

All runs 3/3 byte-identical; fixture SHAs verified against prereg pins before
every run. FAR blocked = 0/60 and true_blocked = 0/34 at **all 35 windows**
(omitted per-cell below; full table: `evidence/sweep_table.tsv`).

| rc\rm | 15 | 53 | 100 | 245 | 500 | 1000 | 2000 |
|---|---|---|---|---|---|---|---|
| 9 | 0/9, 0/300 | 0/9, 2/300 | 0/9, 3/300 | 0/9, 3/300 | 0/9, 6/300 | 0/9, 9/300 | 0/9, 15/300 |
| 25 | 0/9, 0/300 | 0/9, 5/300 | 0/9, 7/300 | 0/9, 7/300 | 0/9, 14/300 | 0/9, 21/300 | 0/9, 35/300 |
| 46 | 0/9, 0/300 | 0/9, 9/300 | 0/9, 11/300 | 0/9, 11/300 | 0/9, 22/300 | 1/9, 33/300 | 1/9, 55/300 |
| 80 | 0/9, 0/300 | 0/9, 14/300 | 0/9, 15/300 | 0/9, 15/300 | 0/9, 30/300 | 3/9, 45/300 | 3/9, 75/300 |
| 150 | 0/9, 0/300 | 0/9, 21/300 | 0/9, 22/300 | 1/9, 22/300 | 3/9, 44/300 | **8/9, 66/300** | 8/9, 110/300 |

Cells: "false_retention/9, near_over_block/300". Bold = the B.3 qualifier.

## Pareto frontier (retention vs over-block)

Non-dominated points (all with far 0/60, true_blocked 0/34):

| rc | rm | retention | over-block | pct |
|---|---|---|---|---|
| 9 | 15 | 0/9 | 0/300 | 0.0% |
| 150 | 245 | 1/9 | 22/300 | 7.3% |
| 150 | 500 | 3/9 | 44/300 | 14.7% |
| 150 | 1000 | 8/9 | 66/300 | 22.0% |

Notes: the (9,15) point is shared by all five rm=15 windows. The frozen anchor
(150,2000) is Pareto-dominated by (150,1000) — identical 8-false catch set, 44
fewer correct over-blocks.

## Anchor reproduction

- (9,15) block output byte-identical to frozen `f5_tightened/run1–3.out`
  (sha256 `170f53b3e4…`); (9,15) replay byte-identical to `replay1–3.out`
  (`1d6bee687b8…`).
- (150,2000) replay reproduces the frozen backtest: false_blocked=8/9,
  true_within=0/34.

## Boundary percepts

32 CORRECT TMB percepts from exemplar 10983 (conf 718, meas 2618), one per
(window, axis, side, inside/outside), run through the predicate at the frontier
window. Full table: `evidence/boundary_percepts.tsv`.

Result: the boundary does not separate. For every window with retention > 0,
inside-boundary corrects are BLOCKED; on the conf-minus side, "outside" probes
are also blocked via neighboring cluster exemplars (11024 at conf 713, meas
2626) — the cluster has real extent (conf 701–718, meas 2618–2647). This
confirms the preregistered B.2 expectation: falses and near-exemplar corrects
occupy the same neighborhood. The (150,1000) separator is a volume trade (66
correct over-blocks to hold the 8 falses), not a separating boundary.

## Scale confirmation (10x / 100x)

Frontier windows (9,15), (150,245), (150,500), (150,1000) plus both anchors,
exact fixture repetition, 3/3 byte-identical at every scale:

| window | 1x | 10x | 100x |
|---|---|---|---|
| (9,15) | 0/9, 0/300 | 0/90, 0/3000 | 0/900, 0/30000 |
| (150,245) | 1/9, 22/300 | 10/90, 220/3000 | 100/900, 2200/30000 |
| (150,500) | 3/9, 44/300 | 30/90, 440/3000 | 300/900, 4400/30000 |
| (150,1000) | 8/9, 66/300 | 80/90, 660/3000 | 800/900, 6600/30000 |
| (150,2000) | 8/9, 110/300 | 80/90, 1100/3000 | 800/900, 11000/30000 |

(cells: retention, near over-block; far 0/60 and true_blocked 0 at every scale).
Rates EXACTLY stable — no long-horizon drift over 36,000 trials.
Digests: `evidence/scale_digests.txt`; tables: `evidence/scale_confirm.tsv`.

## Honest caveats (not decision factors under B.3)

1. The over-block margin is thin: 66/300 = 22.0% against the 25% bar. This is
   9 percentage points better than the frozen window's 36.7%, but there is no
   slack for a stricter bar.
2. Retention jumps 3→8 between rm=500 and rm=1000 at rc=150 — one wide slab of
   measure space holds 5 of the 8 caught falses. The preregistered B.4 geometry
   ("retention can only rise at rm ≥ 245 AND rc ≥ 46") held for the first false;
   the full 8/9 required rm=1000, not rm=245.
3. The separator is volume, not a boundary: 66 correct percepts pay for the 8
   falses; the boundary probes show inside-boundary corrects are always blocked.
4. This verdict applies the frozen rule mechanically to the predicate's geometry.
   It does not change what the predicate IS (a pre-confirmation block rule with
   the delay model in f5_tight.zag), and the live-gate adoption decision remains
   Micah's.

## Evidence inventory (all under `~/workspace/pam_gov_lh/crew6_held/`)

- `src/f5_sweep.zag`, `src/f5_sweep_replay.zag` — parameterized binaries' sources
  (only rc/rm argv-parameterized; predicate logic frozen)
- `evidence/sweep_table.tsv` — full 35-window table
- `evidence/sweep_digests.txt` — 3/3 byte-identical run digests per window
- `evidence/pareto_frontier.tsv` — Pareto frontier
- `evidence/b3_decision.txt` — mechanical B.3 input/output
- `evidence/boundary_percepts.tsv` — 32 boundary-percept results
- `evidence/scale_confirm.tsv`, `evidence/scale_digests.txt` — 10x/100x tables and digests
- `gen/sweep_driver.py`, `gen/pareto.py`, `gen/boundary_gen.py`,
  `gen/scale_confirm.py` — glue scripts (no decision logic)
- `gen/f5_block_10x.txt`, `gen/f5_block_100x.txt`, `gen/f5_replay_10x.txt`,
  `gen/f5_replay_100x.txt` — exact-repetition scale fixtures
- Compiled binaries at `src/bin/` are LOCAL-ONLY, not for commit.
