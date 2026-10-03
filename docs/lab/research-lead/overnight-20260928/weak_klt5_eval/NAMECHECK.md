# NAMECHECK: Weak K-LT-5 Evaluator

## Step 0: Toolchain Guard

- Date: 2026-10-01
- Role: EVALUATOR ONLY (independent; did not build H3-lite Node 1, did not design the sealed world)
- Safebin: activated at session start via the standard loop
- `which python3 python` in safebin PATH: returned nothing (guard-check-done)
- Forbidden executables invoked: zero
- All computation: pure Zag via pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files, mechanical translation of the sealed world file into Zag source lines

## Step 1: Sealed World Hash Verification

- File: `docs/lab/research-lead/overnight-20260928/weak_klt5_world/world_sealed.txt`
- Expected SHA-256: `20ed8d698e168661b54b6c510b994a33f02c615edaee6509efb15d9998f4fa90`
- Measured SHA-256: `20ed8d698e168661b54b6c510b994a33f02c615edaee6509efb15d9998f4fa90`
- Result: MATCH. Evaluation authorized to proceed.

## Step 2: Independent R1-R5 Structural Checks (evaluator's own verification)

- Line counts: 160 TEACH, 40 PROBE, 1 SETUP TAG8 (matches sealed header)
- R4: zero TEACH lines with relation 50 (trial forced on every probe)
- R2: 40 distinct probe subjects (1001 through 1040)
- R3/R5: all 40 probes use relation 50, expected 4, flags 0
- Result: all structural requirements satisfied

## Step 3: Frozen Artifacts (read-only, never modified)

- Prereg: `docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md` (FROZEN)
- H3-lite Node 1 build: commit `45c55ed83` (unfrozen variant, read as input)
- Frozen TNN-2 base: `h3n1_base.zag` from the Node 1 build directory (verbatim frozen copy, SHA-256 `a29972ca...` family; re-verified before use)
- Sealed world: read-only; contents never published in the evaluation report

## Scope

EVALUATOR ONLY. No implementation changes to H3-lite. No prereg modification.
No sealed world contents in the report (hashes and metrics only).
Nothing pushed. Paper untouched.

## Deliverables

- `NAMECHECK.md` (this file)
- `WEAK_KLT5_EVAL.md` (method, measurements, verdict; no sealed data)
- `wld_data.inc` (mechanical translation of sealed world into Zag lines)
- `wkl_driver_node1.zag` (eval driver for Node 1 variant)
- `wkl_driver_frozen.zag` (eval driver for frozen base, C3 control)
- `wkl_node1_bin`, `wkl_frozen_bin` (compiled evaluators)
- `run1.txt`, `run2.txt`, `run3.txt` (Node 1 evaluator, 3 runs)
- `frozen1.txt`, `frozen2.txt`, `frozen3.txt` (frozen control, 3 runs)
