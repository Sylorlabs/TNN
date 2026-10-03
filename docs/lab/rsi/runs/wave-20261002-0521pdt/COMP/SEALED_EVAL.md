# SEALED_EVAL: COMP comparative adversarial composition battery

Wave: wave-20261002-0521pdt. Lane: COMP. Worker: subagent 6d98415a.
Prereg: PREREG_COMP.md frozen alone at cc9acf48e (amended, incl A1),
original freeze 23dc15498. KB1-KB7 per prereg section 4.
Binaries rebuilt from frozen sources under safebin (pure Zag, no Python).

## Build and determinism record

- Sources: cmp_full_a/b/c.zag SHAs match prereg exactly
  (fbb4e80d..., 5729296d..., a6845b9e...). D base = lines 1-1677 of
  cmp_full_c (cut point verified: line 1678 starts the C mechanism
  comment; compose_on/compose_try/ev_query all lie after 1677).
  Note: prereg prints a base SHA 0e2cafe2... that matches no computable
  prefix of the current cmp_full_c.zag (head -n 1677 = dc0e86d4...);
  lineage is instead verified through the full-file SHA (a6845b9e...,
  frozen) plus the exact cut point. Recorded as a provenance gap, not
  a design change.
- Note: prereg says A uses lines 1-1859; assembly needs 1-1860 (line
  1860 is the closing brace of ev_query; without it nothing compiles).
  Mechanism code identical otherwise. Recorded, not a design change.
- 3x byte-identical builds per binary (znc, safebin): all five
  binaries reproduce exactly; lane binaries match (see build_sha256.txt).
  Rebuilt A/B/C/C0 are byte-identical to the 0221 wave's binaries
  (same sources, same toolchain). bin_d is new (0221 never produced it;
  its compile_d.txt showed a syntax error from a stale patch_d that has
  since been fixed in the source adopted here).
- KB1 (3x byte-identical runs): B, C, C0, D HOLD (sha256 equal across
  run_{m}1/2/3; see matrix). A: run 1 never completed (see below);
  KB1 UNVERIFIABLE for A, A's results unadoptable this wave.

## Result matrix (run 1; runs 2/3 byte-identical where complete)

Legend: PASS/FAIL per frozen mechanical thresholds. (g) = mechanism
trace marker confirms the mechanism (not the shared trial path)
produced the answer. (t) = static analysis + marker absence shows the
shared substrate trial path (t2_trial, k<=4 taught-path assembly)
produced the answer, not the mechanism. INC = incomplete (no result).

| test  | A      | B        | C        | C0   | D        |
|-------|--------|----------|----------|------|----------|
| COMP3 | FAIL   | FAIL     | PASS (g) | -    | PASS (g) |
| COMP5 | FAIL   | FAIL     | FAIL (g) | -    | PASS (g) |
| COMP2 | PASS   | PASS     | PASS (g) | -    | PASS (g) |
| B-ABL | -      | PASS (*) | -        | -    | -        |
| D2    | PASS   | PASS     | PASS (g) | -    | PASS (g) |
| D3H   | PASS   | PASS (t) | PASS (g) | -    | PASS (g) |
| D4    | INC    | FAIL     | PASS (g) | -    | PASS (g) |
| PART  | INC    | PASS (t) | PASS (t) | -    | PASS (g) |
| NOSUP | INC    | FAIL     | FAIL (g) | -    | PASS (g) |
| REV   | INC    | PASS     | PASS (g) | -    | PASS (g) |
| REUSE | INC    | FAIL     | PASS (g) | -    | PASS (g) |
| ADVA  | INC    | PASS     | PASS (t) | -    | PASS (g) |
| SINGLE| INC    | PASS     | PASS (t) | -    | PASS (g) |
| C0-3  | -      | -        | -        | PASS | -        |

(*) B-ABL: ablation genuinely removed all type-15 edges
(couse15 1 -> 0; compose_try scan uses the same liveness check, and no
"COMPOSE pairs=" line was emitted), yet ans=105. The answer came from
the substrate trial path (t2_trial assembles the taught 4-edge Z path,
k<=4, verifies vs expected). The control is confounded: it proves the
co-use gating works, but cannot isolate co-use as the cause of B's
composition. See KB6.

Attribution evidence:
- D: "SAT-SEGS n=" in all 11 supervised tests, "SAT-FIX n=3 term=108"
  in NOSUP. All 12 D passes are mechanism-attributed.
- C: "COMP-SEGS n=" in COMP3/COMP2/D2/D3H/D4/REV/REUSE (genuine);
  absent in PART/ADVA/SINGLE (trial artifacts). C's cc_candidates
  requires full-relseq walks (no prefixes) and t2_lu_first (no
  backtracking), so PART and ADVA cannot be C's compose.
- B: "COMPOSE pairs=1" marks edge scans, not success. cb_stage
  requires exact plen match, so PART (E2 plen 3 from 103: only a
  2-value path exists) and D3H (E1 plen 3 from 101: only a 2-value
  path exists) are provably trial artifacts. COMP2/D2/REV staging
  checks out constructively (genuine).
- A: "CX-STAT" on success only. Completed passes: COMP2, D2, D3H.

Isolating tests (mechanism genuinely isolated from trial): COMP3,
COMP5, D4 (>4 steps, beyond trial k<=4), NOSUP (no expected answer).
On these: A 0/2 (rest INC), B 0/4, C 2/4, D 4/4.

## KB scoring

- KB1 determinism: HOLD for B, C, C0, D (3/3 byte-identical).
  UNVERIFIABLE for A (no complete run; results void for the wave).
- KB2 subsumption: D passes every test C passes (10/10) HOLD;
  every test B passes (8/8 completed) HOLD; every test A passes
  (3/3 completed: COMP2, D2, D3H) HOLD on available evidence.
  No axis failed.
- KB3 strict extension: D passes COMP5 and NOSUP, both of which C
  genuinely fails (cap binds at 3 segments; no unsupervised path).
  Both are isolating tests. HOLD (2/2 required).
- KB4 no-COMPOSE_MODE: (a) patch_d.zag has zero code occurrences of
  "compose" (3 hits, all in comments explaining the absence);
  full_d.zag contains zero compose_try references; D's ev_query is
  exactly activate -> satisfy -> trial -> bootstrap (verified in
  source). No flag, no mode, no separate compose or rebind stage
  in the pipeline (rebind_try exists as dead code in the base,
  unwired). HOLD. (b) C0 ans=-2 on COMP3 HOLD.
- KB5 architecture accounting: zero new modes, bridges, handlers,
  semantic cases, opcodes (grep-verified on patch_d.zag); ISA
  unchanged (substrate region copied verbatim); no new MAP/edge
  types (D uses LINK14; type-14 edges pre-exist in cmp_full_b/c,
  including C's own composite promotion). Cognition lines added:
  patch_d.zag 350 total, 299 non-comment non-blank code lines,
  7 new fns (d_relseq, d_chain_tail, d_maxdepth, d_satisfy,
  d_assemble, d_query, d_fixpoint). Driver/shims/asm (471+32+22
  lines) counted as harness, not cognition. HOLD.
- KB6 battery validity: B/COMP2 HOLD (couse15=1, COMPOSE fired);
  B-ABL FAILS the validity condition (see *): BUILD-FAIL for the
  B history-causality comparison only; C/COMP3 HOLD; A/COMP2 HOLD;
  D/SINGLE HOLD (SAT-SEGS n=1 through satisfy, no rebind stage).
- KB7 collapse decision: no completed test exists where a mechanism
  passes and D fails (D 12/12; all others' passes are subsets).
  COLLAPSE-SUPPORTED on the subsumption evidence, with caveats:
  KB1 unverifiable for A, KB6 B-ABL comparison BUILD-FAIL, and the
  ADV-A exhaustive-grounding axis untested (A incomplete).

## Prediction calibration (not kill bars)

D: 12/12 predicted PASS, 12/12 actual. A/B/C predictions were poor:
C passed D3H (3 segments fit its cap; predicted FAIL), B and C
passed PART and ADVA via the trial path (predicted FAIL), B passed
D2 and ADVA (predicted pair-bound FAIL). The trial path (t2_trial,
k<=4) was underestimated as a confound in the prereg predictions.
Bars were not moved; calibration recorded only.

## A-column incompleteness

bin_a run 1 stalled ~50+ min in T-D4's goal query (A's compose_try is
O(MAPs^2 x paths^2) with t2_gather over 40 distractor facts; no
CX-STAT success emitted). D completed its full 12-test suite
including D4 in the same window. This is a computational-robustness
finding favoring D, and it leaves A's D4/PART/NOSUP/REV/REUSE/ADVA/
SINGLE unmeasured. It does not affect KB7 (D failed nothing).

## Run artifact sha256s (run 1; runs 2/3 identical)

- run_b: 9acddbc12bf444bb03a93c489b3bb002ada17d2501df9891e66e54af507ddf3a
- run_c: 9bec2bb693ae5716f52e9d1899ac324875975ecb198232f9e46a299fbbf75aa0
- run_c0: 69977c20f7df823f203b9f7cf2e19363b83bc0d2360d8a94ac0085bba34617c2
- run_d: 501c06f5fd3c56609afbfd3085ecb80c9b2c8d8f7783629108
- binaries: bin_a be4bf8da..., bin_b c8750fc3..., bin_c b247dbba...,
  bin_c0 7a3e266e..., bin_d 4325a9be... (full list in build_sha256.txt)
