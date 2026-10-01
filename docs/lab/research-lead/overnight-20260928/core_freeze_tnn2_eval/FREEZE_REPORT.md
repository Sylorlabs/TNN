# CORE-FREEZE-TNN2 Evaluation Report

**Evaluator:** CORE-FREEZE-TNN2 Evaluator subagent
**Date:** 2026-10-01
**Prereg:** `ce1a7c5f8` (CORE_FREEZE_TNN2_PREREG.md, CORE-FREEZE-TNN2-PREREG-FROZEN)
**Shim build:** `23c2c0206` (SHIM-BUILD-PASS)
**FW seal:** `396895595` (16/16 world files verified)
**Baseline:** CORE-FREEZE-TNN1 `7bde57f52` (FW 4/9, OLD-WORLD 4/9)

## Verdict

**FREEZE-EVAL-COMPLETE**

- **FW SCORE (primary, sealed): 5/9** (TNN-1: 4/9). Pass: FW1, FW2, FW4, FW5.
- **OLD-WORLD REGRESSION SCORE (supplementary): 4/9** (TNN-1: 4/9). Pass: W1, W2, W4, W5.

All kill bars passed. No falsifiers triggered. Determinism verified
3/3 byte-identical for both batteries. No cognition edits (hashes
verified pre and post).

## Kill Bars

- **K-FZ2-1 (ordering):** PASS. Prereg `ce1a7c5f8` is ancestor of HEAD
  (`git merge-base --is-ancestor` exit 0). Prereg strictly precedes
  shim, shim precedes evaluation.
- **K-FZ2-2 (no cognition edits):** PASS. All four hashes verified
  before evaluation; re-verified after (see table). Exact match.
- **K-FZ2-3 (shim purity):** PASS. Shim is the frozen build
  `23c2c0206`; zero-cognition attested; no modifications.
- **K-FZ2-4 (determinism):** PASS. FW battery: 3/3 runs byte-identical
  (all 18 outputs incl. FW9a/FW9b). W battery: 3/3 runs byte-identical
  (all 15 outputs incl. W9a/W9b). NOTE: W run1's W9b was interrupted
  at 25/31 by a service restart; W battery was restarted from scratch
  for a clean determinism record. The interrupted partial is discarded.
- **K-FZ2-5 (seal integrity):** PASS. All 16 FW world files match
  SEAL.md. Anti-smuggling re-scan of frozen TNN-2 source: zero
  FW-range [30000,39999] tokens; W-range hits confined to
  non-executed test fixtures rooted at run_all() (never called by
  driver). FW blindness audit `6f0eae9f2` (PASS, prior).

**Falsifiers:** None triggered. F-FZ2-1 (shim cognition): no.
F-FZ2-2 (hash change): no. F-FZ2-3 (seal broken): no.

## Frozen Artifact Verification

| Artifact | Frozen SHA-256 | Pre-eval | Post-eval | Match |
|---|---|---|---|---|
| TNN-2 source | a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd | verified | verified | YES |
| TNN-2 binary | 6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b | verified | verified | YES |
| Shim source | 33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8 | verified | verified | YES |
| Shim binary | 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954 | verified | verified | YES |

Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).

## FW Results (Primary)

| World | Result | Detail |
|-------|--------|--------|
| FW1 | PASS | 12/12 probes incl. both 3-hop compositional (bar 10/12); 10/10 retention (bar 7/10) |
| FW2 | PASS | 8/8 (bar 7/8) |
| FW3 | FAIL | 0/10 (bar 9/10); all -2 |
| FW4 | PASS | B1 12/12 gate OK; B2 12/12 (100% of pre, bar 90%); B3 12/12 (bar 11/12) |
| FW5 | PASS | B0 10/10 gate OK (bar 8/10); B1 3/3; B2 9/9 |
| FW6 | FAIL | Responder withheld reveal (post-diagnostic ACT was CHOICE 30, not contract's literal CHOICE 0); treatment 0/3 |
| FW7 | FAIL | 0/4 (bar 4/4); all 24 ACTs CHOICE 0; goal never visited |
| FW8 | FAIL | Novel 0/5 (bar 4/5); retention 4/4 (bar 3/4 met) |
| FW9 | FAIL | B1 3/30 (bar 24/30); B2 7/30 (bar 24/30); B5 2/5 (bar 4/5) |

**FW SCORE: 5/9** (FW1, FW2, FW4, FW5)

## W Results (Supplementary Regression)

| World | Result | Detail |
|-------|--------|--------|
| W1 | PASS | 22/22 (12/12 probes + 10/10 retention) |
| W2 | PASS | 8/8 |
| W3 | FAIL | 0/10 |
| W4 | PASS | 18/18 (6/6 + 6/6 + 6/6) |
| W5 | PASS | 8/8 (2/2 + 6/6) |
| W6 | FAIL | ControlB (no reveal; same CHOICE 0 then 30 pattern as FW6) |
| W7 | FAIL | 0/4 |
| W8 | FAIL | 4/9 (recall 4/4, novel 0/5) |
| W9 | FAIL | TreeA 18/28 (bar 23/28); TreeB B2 24/26 PASS (bar 21/26), B5 1/5 FAIL (bar 4/5) |

**OLD-WORLD REGRESSION SCORE: 4/9** (W1, W2, W4, W5; TNN-1 baseline 4/9)

## Method

- Battery drivers: run_fw_battery.sh, run_w_battery.sh (POSIX shell,
  safebin only; mechanically adapted from TNN-1 eval: paths and frozen
  binary hash only).
- Scorers: probe_score.zag / grade_plan.zag (pure Zag), rebuilt with
  pinned znc; binaries byte-identical to TNN-1 eval's committed
  scorers (sha256 verified).
- FW battery: FW1-FW9 sequential, fresh state, 3 runs. FW6 two-stage
  responder + fixed control arm + b-annex (mechanical exact-line
  matching).
- W battery: W1-W9 sequential, fresh state, 3 runs.
- FW5-B0 diagnostic: mechanical (first 10 OBSERVEs + generated QUERYs
  from committed fw5_b0_diag.txt), run from fw4_state.bin copy,
  discarded after. 10/10.
- NOTE: FW9a/FW9b took ~40 min combined per run. TNN-2's runtime
  4-op construction attempts each DAG query via trial search. Slow
  but non-crashing; 10 of 65 answers were non-miss (3+7 correct).

## Per-Cluster Fix Analysis (TNN-1 -> TNN-2)

TNN-1's FW failures clustered into 5 groups. For each: does TNN-2 fix it?

### Cluster 1: FW3 arithmetic (0/10 -> 0/10). NOT FIXED.

TNN-1 failed all multiplication probes. TNN-2's runtime 4-op
construction (the new mechanism) was designed to let the learner
construct procedures like MUL from the generic basis. On FW3 it
constructed nothing usable: all 10 probes returned -2. The
construction machinery fires (evidenced by FW9's non-miss answers)
but does not assemble multiplication. The protected-core ISA ruling
forbade adding MUL as a semantic op; the learner must construct it.
It did not.

### Cluster 2: FW7 planning (0/4 -> 0/4). NOT FIXED.

TNN-1 emitted constant CHOICE 0. TNN-2 also emitted all 24 ACTs as
CHOICE 0 (goal never visited). The miss-to-act loop that changed
FW6's behavior did not fire here (no QUERY misses in FW7 to drive
it). Planning from learner state to goal-directed action sequences
remains absent.

### Cluster 3: FW8 novel utterance (0/5 -> 0/5). NOT FIXED.

Recall sanity 4/4 and retention 4/4 both pass, but novel compositional
utterances all fail. The construction machinery does not generate
novel utterances from learned structure. Same failure mode as TNN-1.

### Cluster 4: FW9 relational DAG (5/30, 7/30 -> 3/30, 7/30). NOT FIXED.

TNN-2's construction machinery attempts each DAG query via trial
search (40-80s per query, ~40 min per FW9 run vs TNN-1's seconds).
It produces non-miss answers (10 of 65: 3+7 correct), demonstrating
the machinery engages, but accuracy (3/30, 7/30, B5 2/5) remains
far below bars (24/30, 24/30, 4/5). Partial construction, not
genuine traversal. Compute cost is a real observation: the runtime
construction is ~100x slower than TNN-1's direct lookup and still
fails.

### Cluster 5: FW6 degenerate inquiry (FAIL -> FAIL, behavior changed).

The sealed responder contract still yields FAIL (no reveal; treatment
0/3). BUT the behavior changed meaningfully: TNN-1 emitted constant
CHOICE 0 regardless of history. TNN-2 emitted CHOICE 0 on the decoy
ACT, then CHOICE 30 on the post-diagnostic ACT. The action is now
contingent on miss history (the new uncertainty-to-action mechanism
engages), not constant. The sealed world cannot distinguish whether
CHOICE 30 is "better" (the contract demands literal CHOICE 0), but
the non-constant, history-contingent action is the predicted
signature of the new mechanism working. This is partial evidence the
mechanism exists, even though the sealed criterion fails.

### Summary

| Cluster | TNN-1 | TNN-2 | Fixed? |
|---------|-------|-------|--------|
| FW3 arithmetic | 0/10 | 0/10 | No |
| FW7 planning | 0/4 | 0/4 | No |
| FW8 novel | 0/5 | 0/5 | No |
| FW9 DAG | 5/30, 7/30 | 3/30, 7/30 | No (partial engagement, huge slowdown) |
| FW6 inquiry | constant 0 | 0 then 30 (contingent) | Partial (mechanism engages, sealed FAIL) |

**Net:** FW 4/9 -> 5/9 (FW1's 3-hop compositional probes now pass:
10/12 -> 12/12). OLD-WORLD 4/9 -> 4/9 (no regression, no improvement).
The three new mechanisms (runtime construction, uncertainty-to-action,
counterexample revision) show signatures of engaging (FW6 contingent
action, FW9 non-miss constructions, FW1 3-hop composition) but do not
fix any of the 5 failure clusters at the sealed-bar level.

## Files

- NAMECHECK.md (Steps 0-5, toolchain guard, verification)
- probe_score.zag / probe_score_bin (byte-identical to TNN-1 eval)
- grade_plan.zag / grade_plan_bin (byte-identical to TNN-1 eval)
- run_fw_battery.sh, run_w_battery.sh
- runs/fw_run{1,2,3}/, runs/w_run{1,2,3}/ (transcripts, hashes, states)
