# Hypothesis D K4-Clean Rerun on Battery v2: Result

## Verdict

**D-V2-FAIL.** Kill bars: K1 PASS, K2 PASS, K3 PASS. No falsifier fired.
The observed matrix mismatches the frozen v2 prediction on one cell
(T3 parity): predicted SOLVE, observed FAIL at 1,000,000 evaluations.
This is the second T3 FAIL for D (v1 also failed at 20/32 in 1M evals),
so per Battery v2 section 4 this triggers a D-search review, not a
third run.

## Outcomes (3/3 runs byte-identical, md5 782e34d57b8b0d508401e70878ca66c1)

| Task | VM | Verdict | Evals | Best | Solution / best program | Hidden |
|------|----|---------|-------|------|------------------------|--------|
| T0 2x+1 | full | SOLVE | 39082 | 9/9 | [PUSH:1 PUSH:-2 IN0 MUL SUB] | 16/16 |
| T1 abs | P | FAIL | 1000000 | 9/17 | [IN0] | 4/8 |
| T2 x mod 3 | full | SOLVE | 217103 | 17/17 | [IN0 PUSH:-3 MOD] | 17/17 |
| T3 parity | full | FAIL | 1000000 | 20/32 | [PUSH:9 IN1 IN0 SUB MOD] | 24/39 |
| T4 nested abs (carried) | P | FAIL | 1000000 | 5/17 | [PUSH:-2 IN0 ADD] | 4/8 |
| T5 fragcomp (carried) | P | FAIL | 1000000 | 7/17 | [PUSH:-2 PUSH:-2 IN0 MUL SUB] | 4/8 |
| T4 fresh | P | FAIL | 1000000 | 5/17 | [PUSH:-2 IN0 ADD] | 4/8 |
| T5 fresh | P | FAIL | 1000000 | 7/17 | [PUSH:-2 PUSH:-2 IN0 MUL SUB] | 4/8 |

Carry sizes (persistent archive): T0 654, T1 2335, T2 3901, T3 11930,
T4 3082, T5 3143. Carry filtering on P-VM tasks dropped 482 programs
entering T1 and 9572 entering T4 (all contained an ablated opcode);
0 dropped entering T5. PVM_TRAPS total is 0 on every P-VM evaluation:
no ablated opcode ever executed under GENEXEC2-P.

## Predictions vs outcomes (Battery v2 section 4, D column)

- T0 SOLVE: **confirmed**. Same solution as v1 ([PUSH:1 PUSH:-2 IN0 MUL
  SUB], computing 1+2x), found via single-op replace
  (PUSH -9 to PUSH 1) at the same eval count (39082) and from the same
  parent niche (21840) as v1. The deceptive prefix
  [IN0 PUSH:2 MUL PUSH:1] was never generated (0 PREFIX_EVAL and
  0 PREFIX_INSERT events in 6.4M evals across 3 runs); the predicted
  prefix mechanism remains UNCONFIRMED, as in v1.
- T1 FAIL: **confirmed**. v1 solved abs via the MOD trick
  ([IN0 PUSH:-2 IN0 MUL MOD NEG NEG]); on the P-VM that route is
  closed (MOD traps; the universe excludes it). Best P-VM program
  reaches only 9/17. TRICK_CHECK silent.
- T2 SOLVE: **confirmed**. Cleaner solution than v1:
  [IN0 PUSH:-3 MOD] (3 ops) vs v1's 11-op program.
- T3 SOLVE: **prediction WRONG, second FAIL**. Best 20/32, identical
  to v1's best score and best program ([PUSH:9 IN1 IN0 SUB MOD]).
  The 8-op parity chain was not found in 1M evals on either run
  generation. Per the frozen Battery v2 prereg, a second FAIL on
  v2-T3 triggers a D-search review instead of a third run.
- T4 FAIL: **confirmed** (carried and fresh). TRICK_CHECK silent.
- T5 FAIL: **confirmed** (carried and fresh). TRICK_CHECK silent.

## Falsifier and control status

- F-TRICK: silent on all six P-VM task instances. No jump-free
  GENEXEC2-P solve of a conditional task occurred.
- F-SMUG: clean. PVM_TRAPS 0 on every P-VM task; both solutions are
  on full-VM tasks; OPCAP_OK 1 on both solves (lengths 5 and 3,
  under the 40-op cap).
- F-TIMEOUT: no task timed out. All tasks ended by SOLVE or by
  evaluation budget exhaustion (1,000,000).
- D-F1: not fired (T0 solved). The control is valid.

## v2-SOLVE audit

Both SOLVEs satisfy the v2 definition: exact train score n/n AND
total ops <= 40 (5 and 3 ops; D has no CALLs and no fragment bodies).
Hidden accuracy is reported separately and does not affect SOLVE.

## Determinism

Three full runs (T0-T5 plus T4/T5 fresh reruns). Byte-identical on
all output lines including WALL_MS (md5 782e34d57b8b0d508401e70878ca66c1
for all three raw files). WALL_MS reads 0 on every task in v1 and v2
alike: the raw clock_gettime path returns 0 in this environment, so
the 1,000,000-evaluation budget is the binding budget in both
generations, exactly as the frozen design targeted. No TIMEOUT is
possible or occurred; this is a pre-existing platform condition,
unchanged from v1.

## Governance

- Prereg commit 2a32cb75e (PREREG_HYPD_V2.md, alone commit) strictly
  precedes the implementation commit (verified with
  git merge-base --is-ancestor before this result was accepted).
- K1 (prereg frozen first): PASS.
- K2 (v2 tasks complete): PASS. T0-T5 plus fresh T4/T5 reruns, all
  under the frozen protocol; raw logs committed.
- K3 (zero Python): PASS. No python3 invocation at any stage of
  this rerun: authoring, implementation, build, runs, byte checks,
  or verification. All checks used shell tools (grep, diff, md5sum).
- No em/en dashes or non-ASCII bytes in hyp_d_v2 files
  (shell byte-verified).
- Only owned paths (docs/lab/research-lead/overnight-20260928/hyp_d_v2/)
  are committed. Commits stay local; nothing is pushed.

## Raw artifacts

- HYPD_V2_RAW_1.txt, HYPD_V2_RAW_2.txt, HYPD_V2_RAW_3.txt (full traces)
- HYPD_V2_RAW_1.err, HYPD_V2_RAW_2.err, HYPD_V2_RAW_3.err
- hyp_d_v2.zag (implementation), hyp_d_v2_bin (compiled binary)
- BUILD.sh (build and run script)

## Interpretation for the battery

The v2 discrimination held where it was load-bearing: the MOD-based
abs shortcut is killed on the P-VM (T1 17/17 in v1 becomes 9/17),
and D remains FAIL on all three P-VM conditional tasks with the
trap audit at zero. The T3 anomaly is now a repeated, deterministic
finding across two independent implementations: D's MAP-Elites does
not find the 8-op parity chain in 1M evals despite theory predicting
a solution exists. That is a D-search adequacy question, not a VM
question, and the frozen battery routes it to a D-search review.

Builder label: D-V2-FAIL.
