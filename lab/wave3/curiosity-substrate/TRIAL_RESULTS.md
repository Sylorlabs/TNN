# Trial Results — curiosity-substrate (Wave 3)

**Date:** 2026-09-20 UTC  
**Verdict:** **BLOCKED** (toolchain defect, not substrate vacuity)

## Summary

The curiosity v1 substrate's **mathematics are validated** (unit test: `WB_FAILURES,0`).  
The **system-level trial is blocked** by a pinned-compiler codegen defect
(`ZNC-2026-09-19-001`) that corrupts array state on repeated `r34c1_observe_error`
calls. The full-curiosity arm (mode 0) cannot execute 600 reliable steps.

This is an **honest apparatus failure**, not a negative result for the substrate.
The substrate is not shown to be vacuous; it is shown to be untestable on this
toolchain in the trial configuration.

## Unit test (POSITIVE)

`curiosity_unit.zag` — all repo assertions pass natively:

| Check | Result |
|---|---|
| `init_ok` | 0,0 (rc OK) |
| `init_state_verified` | 1,1 |
| `progress_sep_gt_2pct` | 1,1 (learning slot scores > 0.02 after 8 err=0.02 observes) |
| `stable_noise_dynamics_small` | 1,1 (|fast−slow| < 0.02 after 40 err=0.25 observes) |
| `stale_gt_fresh` | 1,1 |
| `state_equal_copy` | 1,1 |
| `state_unequal_corrupt` | 0,0 |
| `reject_bad_slot` | −340401,−340401 |
| `reject_neg_error` | −340401,−340401 |
| `WB_FAILURES` | **0** |

**White-box hand check (W2):** After 40 observes of err=0.25 (fast_rate=0.25,
slow_rate=0.03) from 0.25: both EMAs converge to 0.25, so |fast−slow|→0 < 0.02 ✓.
After 8 observes of err=0.02: fast≈0.043, slow≈0.200, dynamics≈0.157 > 0.02 ✓.
The implementation matches the specified EMA update and scoring formula.

## Trial arms

**Mode 0 (full curiosity, |slow−fast| + novelty):** **CRASHES** at step 305.
`SCORE_FAIL2` on slot 5: `slow[5]` became non-finite after `observe_error`
at step 304 (err=1, regime switch). Debug: `fast=0.2425` (expected 0.25),
`slow=inf/nan` (expected 0.03). The substrate's store sequence was miscompiled.

**Mode 1 (round-robin):** **CRASHES** at step 304, same signature (slot 5,
post err=1).

**Mode 2 (myopic, highest fast error):** Runs clean (600 steps, deterministic).
`PROBES: 600,0,0,0,0,0,0,0`. **Degenerate:** locks onto slot 0 forever
(all fast errors tie at 0, lowest-index tie-break). Not a valid surprise-seeking
baseline. `REGIME_FIRST_PROBE: -1` (never probes slot 5).

**Mode 3 (ablated, novelty+staleness only):** Runs clean (600 steps, deterministic).
`PROBES: 44,114,114,66,66,66,65,65`. `REGIME_FIRST_PROBE: 303`.
`NOISE_HALVES: 34,32` (noise slot 4: 34 probes in steps 0–299, 32 in 300–599 —
no rejection; the ablated score has no error-dynamics term, so this is expected).

## Prereg criteria assessment

- **F1** (regime probe within 50 steps): **Cannot evaluate** (mode 0 blocked).
- **F2** (noise rejection second half): **Cannot evaluate** (mode 0 blocked).
- **F3** (curiosity vs myopic on noise): **Cannot evaluate** (mode 0 blocked;
  mode 2 degenerate in any case).
- **F4** (ablation more uniform): **Partial.** Mode 3 ran. Distribution
  44–114 is not uniform; without mode 0 there is no comparison. No conclusion.
- **F5** (determinism): **Partial.** Modes 2 and 3 produce byte-identical
  traces across runs. Mode 0 deterministically crashes at the same step.
- **W1** (argmax selection): Observed in mode 0 trace before crash
  (e.g., step 304 probed slot 5, the max-score slot). **Partial.**
- **W2** (hand-computed EMA/score): **Satisfied** via unit test (see above).
- **W3** (scale argument): O(N) state, O(1) update, O(N) selection. **Holds**
  by code inspection. The 128-slot scale test was not run (blocked).

## Toolchain defect (ZNC-2026-09-19-001)

The pinned `znc_linux_x86_64_abed8aa1` miscompiles array stores in multi-store
contexts. Characterized via isolated repros:

1. `r34c1_init` 4-store loop: `last_seen[i]`→0 (not −1) for i<N−3;
   `count[i]`→−1 (not 0) for i≥N−3.
2. Multiple i64 stores to one array corrupt the last 3 elements of the i32
   array allocated immediately before it (probe26, probe28).
3. `r34c1_observe_error` in loop context: phantom stores, wrong values,
   non-finite results (probe32, probe34, probe36: `RC_FAIL@13`).
4. 20 unrolled calls: one missed count increment (probe37).

The defect is **deterministic per binary** and **context-sensitive**. Single
calls in simple contexts work (unit test, probe35). The trial's 600-call hot
path does not.

**Workarounds attempted:** unrolled init, canary guard array, setter-function
indirection, allocation reordering, self-test validation. None make the
600-step trial reliable. The self-test (`SELFTEST,0`) confirms the trial
binary's codegen is defective.

## Evidence

- `evidence/trace_mode0.txt` (crashes at step 305)
- `evidence/trace_mode1.txt` (crashes at step 304)
- `evidence/trace_mode2.txt` (600 steps, degenerate)
- `evidence/trace_mode3.txt` (600 steps, ablated)
- `curiosity_unit.zag` + binary (WB_FAILURES,0)
- `curiosity_v1_native.zag` (substrate port, 1e18 for 1e300)
- `/tmp/curiosity/probe*.zag` (defect repros, ephemeral)

## Verdict rationale

**BLOCKED**, not NEGATIVE. The preregistered falsification criteria require
the full-curiosity arm, which cannot be executed due to apparatus failure.
The substrate's mathematics are correct (unit test). Whether the system
exhibits useful probe selection remains untested.

**Recommended follow-up:** Re-run the trial on a fixed toolchain, or on a
target with correct codegen (e.g., WASM backend for validation, then native
when the backend is fixed). The trial harness, world design, and prereg are
complete and ready.
