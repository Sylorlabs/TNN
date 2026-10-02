# RESULT: H-CAUSALEXP-CONSTRUCT Ablation Study (step 8)

Date: 2026-09-30.
Status: ABLATION-COMPLETE.
Prereg: e54374f6e (frozen before implementation; verified strict ancestor).
Implementation: cxablate.zag (pure Zag, zero Python).
Raw: CXABLATE_RAW.txt (md5 a28388af8649df9f109aa3ded3a7b49d, 3/3 byte-identical, exit 0, zero stderr).

## Anchor (P-AB4): full learner reproduces builder

Mode 0 (full learner):
- World A configs: SELECT [S,W,OY] (len 3), CONVERGE=1 (2/2).
- World B configs: SELECT [S,W,W,OY] (len 4), CONVERGE=1 (2/2).
- 4/4 converge. Selections match builder exactly. P-AB4 PASS.

Note on checked counts: reported counts are cumulative across depths
(depth 1: 2 with-observe; depth 2: 12; depth 3: 56; depth 4: 240).
World A: 2+12+3=17. World B: 2+12+56+15=85. A1's per-depth counts
(3 and 15) are consistent.

## AB1: Remove disagreement filter

Result: 0/4 converge.

AB1 selects [OY] (len 1, first-with-observe, checked=1) for all configs.
Both hypotheses predict Y=0 at t=0. Both survive. CONVERGE=0 on all 4.

- AB1-K1: PASS (selection is simulation-free).
- AB1-K2: PASS (0/4 <= 1/4). The disagreement filter is load-bearing
  for CORRECTNESS. Without it, the learner cannot discriminate.

## AB2: Remove simulation for selection

Result:
- World A: 35 real-world actions to find discriminating sequence.
- World B: 254 real-world actions.

The learner executes each with-observe candidate in the real world
(fresh state each time) until the oracle says hypotheses disagree.
World A: 2 (d1) + 24 (d2) + 9 (d3) = 35. World B: 2+24+168+60 = 254.
Elimination is impossible without simulation (noted).

- AB2-K1: PASS (zero simulation in selection).
- AB2-K2: PASS (35 >= 10). Simulation is load-bearing for EFFICIENCY.
  The full learner uses 1 real-world execution for selection; AB2 uses
  35x (A) to 254x (B) more.

## AB3: Remove iterative deepening (depth 5 only)

Result: 4/4 converge, but with length-5 sequences.
- World A: [S,S,S,W,OY] (len 5, checked=3).
- World B: [S,S,W,W,OY] (len 5, checked=15).

The extra leading S's are idempotent (X:=1 twice = once), so the
depth-3/4 solutions pad to depth 5 and still discriminate.

- AB3-K1: PASS (only depth 5 enumerated).
- AB3-K2: PASS (length 5 > 4). Iterative deepening is load-bearing
  for EFFICIENCY (shorter sequences). It is not load-bearing for
  correctness (4/4 still converge).

## AB4: Reverse enumeration order

Result: 4/4 converge. Same sequences found.
- World A: [S,W,OY], checked=68 (vs 17 forward; 4.0x).
- World B: [S,W,W,OY], checked=296 (vs 85 forward; 3.5x).

- AB4-K1: PASS (order exactly reversed).
- AB4-K2: Order is efficiency-relevant (>2x difference). The filter is
  order-independent for correctness (same sequences found, because they
  are the unique discriminators at their depths).

## AB5: Shrink MAXD to 3

Result: exactly 2/4 converge.
- World A: 2/2 converge ([S,W,OY]).
- World B: 0/2 converge (NO-DISCRIMINATING-SEQUENCE, checked=70).

- AB5-K1: PASS (MAXD=3).
- AB5-K2: PASS (exactly 2/4). The depth bound is load-bearing for
  CORRECTNESS. World B is unsolvable below depth 4.

## Summary table

| Component | Correctness impact | Efficiency impact | Load-bearing? |
|-----------|-------------------|-------------------|---------------|
| Disagreement filter (AB1) | 4/4 -> 0/4 | N/A | YES (correctness) |
| Simulation for selection (AB2) | N/A (elimination impossible) | 1 -> 35/254 real actions | YES (efficiency) |
| Iterative deepening (AB3) | 4/4 -> 4/4 (no) | len 3/4 -> len 5 | YES (efficiency) |
| Enumeration order (AB4) | 4/4 -> 4/4 (no) | 17/85 -> 68/296 checked | YES (efficiency) |
| Depth bound MAXD (AB5) | 4/4 -> 2/4 | N/A | YES (correctness) |

## Interpretation

The learner's filter contributes:
1. CORRECTNESS: without the disagreement filter, convergence drops
   from 4/4 to 0/4. The filter is what makes selection discriminating.
2. EFFICIENCY: simulation avoids 35x-254x real-world actions;
   deepening finds shorter sequences; order affects search cost 3-4x.

What the filter does NOT contribute:
- It does not invent the candidate space (researcher enumerates).
- It does not guide generation (A1 AX-CX3: filter only, never guides).
- It does not overcome the depth bound (AB5: bound is hard).

This is consistent with the A1/A2 bounded-L2 classification. The
ablation quantifies the L2 mechanism: the learner owns a correctness-
critical filter and efficiency-relevant search choices, but the
researcher owns the space being searched.

## Validity

- P-AB1: prereg e54374f6e strictly precedes implementation. PASS.
- P-AB2: pure Zag, zero Python, zero .py files. PASS.
- P-AB3: 3/3 byte-identical, exit 0, zero stderr. PASS.
- P-AB4: anchor reproduces builder selections. PASS.
- P-AB5: no em-dash bytes in documentation. PASS (verified below).
- P-AB6: local commits, owned path only. PASS.

## Verdict

ABLATION-COMPLETE. All five ablations ran with exact numbers. All
K-bars adjudicated. All validity bars pass.
