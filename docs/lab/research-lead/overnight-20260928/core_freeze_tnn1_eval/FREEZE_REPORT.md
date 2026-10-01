# CORE-FREEZE-TNN1 Evaluation Report

**Evaluator:** CORE-FREEZE-TNN1 Evaluator subagent
**Date:** 2026-09-30/10-01
**Prereg:** `60f1ff0bf` (CORE_FREEZE_TNN1_PREREG.md)
**Shim build:** `58d2268e7`
**FW seal:** `396895595`

## Verdict

**FREEZE-EVAL-COMPLETE**

- **FW SCORE (primary, sealed): 4/9**
- **OLD-WORLD REGRESSION SCORE (supplementary): 4/9** (original freeze: 1/9)

## Kill Bars

- **K-FZ1 (ordering):** PASS. Prereg `60f1ff0bf` is ancestor of HEAD.
- **K-FZ2 (no cognition edits):** PASS. All four hashes verified before AND after battery:
  - TNN-1 src `d3895083c9f8b5b0f82ac1c74b11eb2c90341059fcf9e37be30b9c085de0cc6b`
  - TNN-1 bin `efa36ecd0604a8e3f650e0fef715a25c2383f271f20349c6e26a8f91116507a1`
  - shim src `167f4fd3ba3febc5e260dc1c84c8cb7b6ae82cad634c64e41b498130609ce8f9`
  - shim bin `9007e084e93b81cc508f6b5e73200080b70454e84201f0d3e7c3baa4f35c64e0`
- **K-FZ3 (shim purity):** PASS. Shim is the frozen build; no modifications.
- **K-FZ4 (determinism):** PASS. 3/3 runs byte-identical per world (stdout and state hashes) for both FW and W batteries.
- **K-FZ5 (seal integrity):** PASS. All 16 FW world files match SEAL.md. All 15 W world files match committed RUN_RESULTS.md. Anti-smuggling re-scan of new TNN-1 source: zero FW-range [30000,39999] integers; W-range hits (7001, 8001-8004, 9001) confined to non-executed test fixtures in `run_all()` (never called by driver main), cleared as non-smuggling.

**Falsifiers:** None triggered. F-FZ1 (shim cognition): no. F-FZ2 (hash change): no. F-FZ3 (seal broken): no.

## FW Results (Primary)

| World | Result | Detail |
|-------|--------|--------|
| FW1 | PASS | 10/12 probes (bar 10/12), 10/10 retention (bar 7/10) |
| FW2 | PASS | 8/8 (bar 7/8) |
| FW3 | FAIL | 0/10 (bar 9/10) |
| FW4 | PASS | B1 12/12 gate OK; B2 12/12 (100% of pre, bar 90%); B3 12/12 (bar 11/12) |
| FW5 | PASS | B0 10/10 gate OK (bar 8/10); B1 3/3; B2 9/9 |
| FW6 | FAIL (degenerate) | B1 3/3, B2 0/3 numerically met; B4 FAIL. All CHOICE lines constant "CHOICE 0" (5/5). Adversary reading: WORLD-FAIL. Literalist reading: numeric pass. |
| FW7 | FAIL | 0/4 (bar 4/4). Grader: 4 instances, 0 visited goal. |
| FW8 | FAIL | Novel 0/5 (bar 4/5); retention 4/4 (bar 3/4 met) |
| FW9 | FAIL | B1 5/30 (bar 24/30); B2 9/30 (bar 24/30); B5 0/5 (bar 4/5) |

**FW SCORE: 4/9** (FW1, FW2, FW4, FW5)

FW6 detail: Treatment released phaseB1 then phaseB2 (diagnostic ANSWER 35001 35501 -2 + CHOICE 0 fired). Control arm (fixed controlA->controlB->controlB2 from S5 copy) scored 0/3. B6b annex released controlB->controlB2 (diagnostic 77 as designed), scored 0/3 with first probe answering 77 (misinformation uptake confirmed).

## W Results (Supplementary Regression)

| World | Result | Detail |
|-------|--------|--------|
| W1 | PASS | 10/12 + 10/10 |
| W2 | PASS | 8/8 |
| W3 | FAIL | 0/10 |
| W4 | PASS | 6/6, 6/6 (100%), 6/6 |
| W5 | PASS | 2/2, 6/6 |
| W6 | FAIL (degenerate) | B1 3/3, B2 0/3 numerically; CHOICE constant 0 |
| W7 | FAIL | 0/4 |
| W8 | FAIL | Recall 4/4, novel 0/5 |
| W9 | FAIL | 14/28, 14/26, 0/5 |

**OLD-WORLD REGRESSION SCORE: 4/9** (W1, W2, W4, W5), up from 1/9 in the original freeze.

## Method

- Battery drivers: `run_fw_battery.sh`, `run_w_battery.sh` (POSIX shell, safebin only).
- Scorers: `probe_score.zag` (pure Zag, with [lo,hi) range support), `grade_plan.zag` (pure Zag plan grader).
- FW battery: FW1-FW9 sequential, fresh state, 3 runs. FW6 two-stage responder + fixed control arm + b-annex.
- W battery: W1-W9 sequential, fresh state, 3 runs. W6 responder + control + w6b annex.
- FW5-B0 diagnostic: mechanical (first 10 OBSERVEs + generated QUERYs), run from S4 copy, discarded after. 10/10.

## Files

- `NAMECHECK.md` (Steps 0-4, toolchain guard)
- `probe_score.zag` / `probe_score_bin`
- `grade_plan.zag` / `grade_plan_bin`
- `run_fw_battery.sh`, `run_w_battery.sh`
- `fw5_b0_diag.txt`
- `runs/fw_run{1,2,3}/`, `runs/w_run{1,2,3}/` (transcripts, hashes, states)

## Notes for Root-Cause Clustering

Failure clusters for the next generation (per Micah's directive, not per-world patches):
1. **Arithmetic/composition (FW3, W3):** 0/10 on both. The frozen core cannot construct multiplication from the ISA basis.
2. **Planning (FW7, W7):** 0/4 on both. The grader shows the system never reaches the goal; actions do not compose toward the target.
3. **Novel utterance (FW8, W8):** 0/5 novel on both, despite 4/4 retention. The system recalls but does not generate novel forms.
4. **Relational DAG (FW9, W9):** 5/30 and 9/30 (FW), 14/28 and 14/26 (W). Multi-hop relational inference fails.
5. **Active inquiry (FW6, W6):** Degenerate constant-action mechanism. The interface's single-element action alphabet cannot express contingent inquiry.

Passing: FW1/FW2 (associative recall), FW4 (law change/revert), FW5 (targeted update without collateral damage), and W1/W2/W4/W5 (regression).
