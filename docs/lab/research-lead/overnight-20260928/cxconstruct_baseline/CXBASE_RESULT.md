# RESULT: H-CAUSALEXP-CONSTRUCT Simple-Baseline Comparison (cxconstruct_baseline)

Date: 2026-09-30.
Worker verdict: **BASELINE-LOSES**.
Prereg: `PREREG_CXBASE.md` (frozen at cf83b52be, before implementation).
Source: `cxbase.zag` (pure Zag, reimplements simulator + learner from
frozen prereg description, parameterized by hypothesis-pair).
Raw: `CXBASE_RAW.txt` (md5 dd7bcdad54483ceb77bd5609967ba364).

## Validity bars (all pass)

- P-CB1 (replication sanity): PASS. Reimplemented learner constructs
  [S,W,OY] (len 3) for World A and [S,W,W,OY] (len 4) for World B,
  matching the builder's result exactly. Converges 4/4 replication
  configs with exactly 1 real-world execution each.
  replication_ok=1.
- P-CB2 (single-primitive): PASS. All 4 primitives agree under both
  hypotheses in all 4 worlds (A,B,C,D): 16/16 agree. Extends K-CX1.
- P-CB3 (B1 executed): PASS. 200 trials per replication config done.
- P-CB4 (B3 executed): PASS. Greedy converges on all 4 configs.
- P-CB5 (B4 + generalization): PASS. Lookup misses on C,D (0/2);
  constructive learner converges 4/4 novel configs. novel_ok=1.
- P-CB6 (determinism): PASS. 3 runs, byte-identical (cmp), exit 0,
  zero stderr.
- P-CB7 (purity): PASS. Pure Zag (znc build; bash/cmp/md5sum only).
  Zero Python invocations. Zero em dash bytes (byte-verified).

## Baseline results (exact numbers)

B1 RANDOM+ELIMINATE (200 trials/config, seeded LCG, uniform lengths
1..5 with observe, 1 real-world execution per trial):
- cfg=0 (A,true=H0): 6/200 converge (3.0%)
- cfg=1 (A,true=H1): 6/200 converge (3.0%)
- cfg=2 (B,true=H0): 1/200 converge (0.5%)
- cfg=3 (B,true=H1): 1/200 converge (0.5%)
Interpretation: the density of discriminating sequences is 0.5-3%.
Random search is hopeless. The disagreement criterion is not finding
a needle in a haystack of needles; it is finding a needle in a
haystack of non-needles.

B2 SINGLE-PRIMITIVE: 0% discriminate (16/16 agree in all worlds).
Confirms the frozen hand proof computationally.

B3 GREEDY SHORTEST-FIRST TRIAL-AND-ERROR (real-world execution per
sequence until elimination):
- cfg=0,1 (World A): 17 executions to converge
- cfg=2,3 (World B): 85 executions to converge
Hand-verified: World A tries [OY],[OZ] (2), all 12 observing depth-2
(14 total), then [S,S,OY],[S,S,OZ] before [S,W,OY] (17). World B adds
all 56 observing depth-3 (70 total), then 14 observing depth-4 before
[S,W,W,OY] (85). The learner uses exactly 1. The simulation
pre-filter buys a 17x to 85x reduction in real-world actions.

B4 MEMORIZATION LOOKUP:
- Trained: (A->[S,W,OY], B->[S,W,W,OY]).
- World C (novel delays): NO-SEQUENCE (lookup miss).
- World D (novel structure): NO-SEQUENCE (lookup miss).
- Generalization: 0/2.
Meanwhile the CONSTRUCTIVE learner (same code, no retraining):
- World C: constructs [S,W,W,W,OY] (len 5, p0=0 p1=1), converges both
  configs with 1 execution each.
- World D: constructs [S,W,W,OZ] (len 4, p0=1 p1=0), converges both
  configs with 1 execution each. Note: OZ-based discrimination, a
  different observed variable than A/B/C; the machinery is not
  hardcoded to OY.
- Novel generalization: 4/4.

## Verdict: BASELINE-LOSES

Against frozen criteria:
- B1 density 0.5-3% < 25% threshold. LOSES.
- B2 0%. LOSES.
- B3 needs 17/85 executions >= 4 threshold (learner: 1). LOSES on
  efficiency despite matching correctness.
- B4 generalizes 0/2 while the constructive learner generalizes 4/4.
  LOSES on generalization.

No baseline matches the learner on correctness+efficency+
generalization. The hypothesis-driven disagreement criterion adds
real, measured value: (1) it finds discriminating interventions in a
space where 97-99.5% of candidates fail; (2) it does so with zero
real-world search cost (17-85x fewer executions than trial-and-error);
(3) the construction machinery generalizes to novel hypothesis pairs
(new delays, new observed variables) where a memorized table cannot.

## Honest limitations (per frozen prereg section 7)

- Worlds are synthetic and tiny.
- B1 density is for uniform lengths 1..5 with observe; other
  distributions differ.
- B3 isolates the simulation pre-filter, not search order.
- B4 tests pure lookup; nearest-neighbor might do better but was not
  the frozen question.
- Step 5 of promotion pipeline. Adversary, OOD, ablation, transfer,
  red team, governance remain.

## Files

- `PREREG_CXBASE.md` (frozen cf83b52be)
- `cxbase.zag` (implementation)
- `CXBASE_RAW.txt` (raw, md5 dd7bcdad54483ceb77bd5609967ba364)
- `CXBASE_RESULT.md` (this file)

Toolchain: znc 2026.07.0-dev (edition 2026). Commits local; nothing pushed.
