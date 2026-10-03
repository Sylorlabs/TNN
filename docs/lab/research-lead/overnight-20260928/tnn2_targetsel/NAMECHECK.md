# NAMECHECK: Target-Selection Policy Designer

## Step 0: Toolchain Guard

- Safebin activated: `export PATH="$HOME/safebin"` (36 allowed tools).
- `which python3 python` returns nothing in safebin PATH.
- Guard check output: `guard-check-done` (zero forbidden executables).
- This task is **design only**: no binaries compiled, no research computation run, no implementation.
- If a forbidden executable had been invoked, this wave would be PROCESS-FAIL.

## Task

Design a target-selection policy for graph composition in a hypothetical
TNN-2 successor. The MUL comparator (commit `e2e34a4ac`) identified
target-selection among accumulated MAPs as "the underexploited site of
learner authority": MUL Rung B had exactly one PROC (CALL target
trivial); TNN-2 accumulates many MAPs and has no design for choosing
among them.

## Scope discipline

- Owned path only: `docs/lab/research-lead/overnight-20260928/tnn2_targetsel/`.
- Read-only on: `tnn2_mulcompare/MUL_COMPARISON.md`,
  `tnn2_h3probe/H3_FEASIBILITY.md`, `tnn2_build/tnn2.zag` (frozen
  `f4de7ff46`).
- No source edits. No implementation. No em dashes. Paper untouched.

## Verdict on completion

TARGET-SELECTION-DESIGN-COMPLETE.
