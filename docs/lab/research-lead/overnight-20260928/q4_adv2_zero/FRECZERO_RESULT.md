# F-RECFOLD Zero-Python Rerun: Result

## Verdict: FREC-ZERO-FAIL

The Q4 discovery mechanism fails the F-RECFOLD second adversary family
under strictly zero-Python execution. B1 fails on all 3 instances.
This is a governance-clean measurement: zero Python was invoked at any
stage of this task, from task start through this document.

## Protocol

- Prereg: `PREREG_CLEAN.md` at commit `327f42116` (ancestry: this wave
  runs the protocol frozen there; no implementation change was made).
- Implementation: `frecfold_clean.zag` from
  `docs/lab/research-lead/overnight-20260928/q4_adv2_clean/`,
  SHA256 `659e0ca53f5c7b17077328d0a798324af294d57c8aac6968a79841d8cbde7450`
  (verified by recomputation before any run; no source change).
- Binary: committed `frecfold_clean_bin`,
  SHA256 `b0803a138df49a7ad110bc5995a4cf120ae24ba4886827a4cb58714674d6223e`
  (verified by recomputation; executed as committed, not rebuilt).
- Scope: Phase 1 only (3 instances x 5 seeds), matching the prior wave.

## Execution (shell only; zero Python)

- `zrun1.txt`, `zrun2.txt`, `zrun3.txt`: 3 full runs, exit code 0 each,
  stderr files `zrun*.err` all 0 bytes.
- Determinism: SHA256 of all three outputs is identical:
  `fef761afc5e72daa833e7bb4a12b1525efbffafef2294219bb7d650632f2d048`.
- Cross-worker check: this output is byte-identical (via `cmp`) to
  `../q4_adv2_clean/run1.txt` committed in the VOID wave. The
  measurements reproduce exactly across workers.
- Dash audit: shell grep for U+2013/U+2014 bytes returned no hits in
  any output file.
- Tool inventory for this wave: mkdir, sha256sum, cmp, grep, wc, git,
  the committed binary itself, file reads/writes. No python3 process
  was ever invoked.

## Results (identical in all 3 runs)

### Instance 1 (easy, repeated motif)
| Seed | ev_correct | TRUE |
|------|-----------|------|
| 11 | 25/32 | 40/64 |
| 22 | 29/32 | 44/64 |
| 33 | 26/32 | 46/64 |
| 44 | 25/32 | 46/64 |
| 55 | 25/32 | 44/64 |
B1: 0/5 seeds at 64/64. FAIL.

### Instance 2 (medium, nested chain)
| Seed | ev_correct | TRUE |
|------|-----------|------|
| 11 | 31/32 | 63/64 |
| 22 | 31/32 | 63/64 |
| 33 | 31/32 | 63/64 |
| 44 | 31/32 | 63/64 |
| 55 | 31/32 | 63/64 |
The mechanism selects 0-op constant-0 on all 5 seeds (the truth table
has 1/64 ones; constant prediction reaches 63/64). The 5-AND nested
chain is never discovered. This is a constant-prediction ceiling, not
structural discovery. B1: 0/5 at 64/64. FAIL.

### Instance 3 (hard, repeated XOR)
| Seed | ev_correct | TRUE |
|------|-----------|------|
| 11 | 23/32 | 32/64 |
| 22 | 22/32 | 32/64 |
| 33 | 27/32 | 40/64 |
| 44 | 22/32 | 32/64 |
| 55 | 22/32 | 32/64 |
4/5 seeds at chance (32/64). B1: 0/5 at 64/64. FAIL.

## Verdict against frozen bars

- B1 (amended multi-seed: 64/64 on >=4/5 seeds per instance): FAIL on
  all 3 instances (0/5, 0/5, 0/5).
- B2 (operator count <= 7 with growth trace): PASS on the kept forms
  (opc 0-7 observed; traces present).
- B3 (margin over best baseline >= 0.15 hard / >= 0.10 easy/medium):
  PARTIAL (I1 ~0.156 and I2 ~0.469 pass; I3 ~0.125 fails the 0.15 hard
  bar).
- B4 (structural audit): NOT APPLICABLE (B1 fails on every instance).
- Falsifiers: none fired (no seal leak, no budget exceed, memorization
  baseline does not reach 64/64).

## Kill bars for this wave

- K1 (zero Python, absolute, from task start): PASS. Verified by tool
  inventory above; no python3 invocation occurred.
- K2 (15/15 evaluations complete): PASS. All 3 instances x 5 seeds in
  each of the 3 runs.
- K3 (3/3 byte-identical): PASS. Single SHA256 across runs.

## Implication

The second C0-C adversary family defeats the Q4 discovery mechanism.
I2's 63/64 consistency sharpens the prior finding: the failure is
systematic (deterministic constant-prediction trap), not seed luck.
This wave contributes a governance-clean FAIL data point for the Q4
line under the promotion pipeline (implementation, sealed evaluation
steps complete; reproduction cross-worker confirmed by byte-identical
output).
