# DDES Builder Result

## Prereg

Commit `d42294620` (file `ddes/PREREG_DDES.md`). Note: the prereg file was
swept into the concurrent "Race contestant" commit by the shared git index;
content verified byte-identical to the frozen prereg. Prereg strictly
precedes implementation (implementation commit is a descendant).

Kill bars frozen: K-NX1 through K-NX8. Validity bars: V-NX1 through V-NX3.

## Implementation

File: `ddes/ddes.zag` (pure Zag, zero Python).
Binary: `ddes/ddes_bin` (built with znc).

Architecture (per DESIGN.md):
1. `compute_arrivals`: Bellman-Ford shortest path over rule graph.
   Generic over rule list; no branch on specific values.
2. `compute_frontier`: analytic disagreement via arrival inequality.
   Earliest (V*, t*) = argmin over variables. No scan over t.
3. `synthesize_plan`: exactly one plan assembled from (V*, t*, schema).
   [S] if needed, W while time < t*, observe(V*) via generic
   arithmetic (obs = 4 - v_star). Increments K-NX2 counter.
4. `ddes_world`: tries schemas set-X then null, picks earliest target,
   executes once, eliminates via analytic predictor.

## Test results (3/3 byte-identical, md5 a81b98fc788f4649b9f9d86d8887a84a)

World A cfg0: TARGET (Y,1) PLAN [S,W,OY] EXEC real=0 PRED 0/1 CONVERGE-OK
World A cfg1: TARGET (Y,1) PLAN [S,W,OY] EXEC real=1 PRED 0/1 CONVERGE-OK
World B cfg0: TARGET (Y,2) PLAN [S,W,W,OY] EXEC real=0 PRED 0/1 CONVERGE-OK
World B cfg1: TARGET (Y,2) PLAN [S,W,W,OY] EXEC real=1 PRED 0/1 CONVERGE-OK
World C cfg0: TARGET (Y,4) PLAN [S,W,W,W,W,OY] EXEC real=0 CONVERGE-OK
World C cfg1: TARGET (Y,4) PLAN [S,W,W,W,W,OY] EXEC real=1 CONVERGE-OK
World D cfg0: TARGET (Z,2) PLAN [S,W,W,OZ] EXEC real=1 CONVERGE-OK
World D cfg1: TARGET (Z,2) PLAN [S,W,W,OZ] EXEC real=0 CONVERGE-OK
World E: NO-DISCRIMINATING-PLAN, 0 executions, E-EMPTY-OK

SUMMARY: ok=9/9, plans_built=8 (exactly 1 per world config).
Stderr: 0 bytes on all 3 runs. Exit: 0.

## Kill bar verdicts

V-NX1: PASS. Worlds A/B converge 4/4, exactly 1 real execution per config.
V-NX2: PASS. 3/3 byte-identical, exit 0, zero stderr.
V-NX3: PASS. Pure Zag, zero Python, zero em-dash bytes.

K-NX1: PASS. Source audit: no sequence-generating loop (all while loops
  iterate rules/variables/time-steps of the single derived plan, none
  enumerates candidate sequences over the primitive set). No length
  constant (no MAXD; plan length derived from t*; 64-byte plan buffer is
  memory allocation, not a semantic bound consulted by the algorithm).
K-NX2: PASS. plans_built=4 on Worlds A/B (1 per config), well under 8.
  Kill threshold (>=100) not approached.
K-NX3: PASS (design-level). World C (length 6, exceeds old MAXD=5) converges
  with exactly 1 execution. No bound exists to exceed; sealed L>=8 test
  awaits post-freeze adversary.
K-NX4: PASS. Delay variants produce different plans: A->[S,W,OY],
  B->[S,W,W,OY], C->[S,W,W,W,W,OY]. Each matches analytic target.
K-NX5: PASS. World D (Z-only hypotheses) emits [S,W,W,OZ], converges.
  Observed variable chosen by analysis, never hardcoded.
K-NX6: PASS. Analysis path (compute_arrivals, compute_frontier,
  synthesize_plan, predict) contains no branch on specific delay values,
  variable ids, or world ids. Schema flag and generic arithmetic only.
K-NX7: PASS. Every world assembles exactly 1 candidate plan (<=3).
K-NX8: PASS. World E: NO-DISCRIMINATING-PLAN, 0 real executions.

## Classification

Strong L2 (guided generation), per design section 5. NOT L3.
Researcher still owns: action vocabulary, hypothesis format, analysis
algorithm, schema set. Learner authors: intervention decision, observed
variable, plan length, full sequence.

## BUILD-PASS

All validity bars and all kill bars pass. DDES derives experiments from
hypothesis structure with zero enumeration, zero bound, zero menu.
