# Scale-rot battery — FROZEN PREREG

**Status:** FROZEN 2026-09-27. **Line:** B3 scale-rot. **Branch:** `tnn-native-lab`.
**Standing law:** nothing should degrade with more scale or power — scale-rot is a defect, not a result to accept.

## Objective

Test whether adopted TNN mechanisms hold behavior and determinism at 1x / 10x / 100x scale.
Scale-rot = any accuracy/behavior degradation, any verdict flip on identical item content,
any determinism break, or any crash that appears only at larger scale.

## Mechanisms under test

| # | Mechanism | Frozen source (origin/tnn-native-lab) | Scale dimension |
|---|-----------|----------------------------------------|-----------------|
| M1 | one-brain v3 deliberation | `docs/lab/onebrain3/impl/onebrain_v3.zag` + `docs/lab/onebrain3/v6.tsv` | problem count: 44 → 440 → 4400 (deterministic replication, IDs suffixed `_s00`…; item content identical) |
| M2 | dialogue deliberation (frozen R4 build) | `docs/lab/dialogue/deliberation/build/deliberate_frozen_r4.zag` + `docs/lab/dialogue/round4/{battery,kb,gaz}.txt` | problem count: 33 probes → 330 → 3300 (deterministic replication of DIALOGUE blocks, IDs suffixed `_sNN`) |
| M3a | production chunker (57Q battery) | `docs/lab/mg_chunking_promote/{battery1,intake}.zag` | fixed 57-question regression battery (baseline reproduction + determinism) |
| M3b | production chunker (text length) | `docs/lab/mg_chunking_promote/scale_text.zag` (this battery's driver, committed here) through live `tnn_intake` | input text length: 60 → 600 → 6000 words (~0.4KB → ~4KB → ~37KB), 5-word cycle text, closed-form expected answers |
| M4 | native epistemics | `docs/lab/epistemic_native/` | **BLOCKED ON DEPENDENCY** — scale leg runs only after a passing label-blind Phase-1 verdict lands on origin (frozen prereg `bbaa88099`, K6: ≥8/10 contradicted held-out lies classified as lies). Train-LOO evidence alone (`d758a876c`) does not qualify. |

## Metrics (per leg)

1. **Pass rate** vs frozen expected answers (M1/M2/M3a) or closed-form expectations (M3b).
2. **Per-item verdict flips**: for replicated legs, each higher-leg item's verdict compared against its 1x twin (same content, suffixed ID). Any flip = scale-rot signal.
3. **Byte determinism**: every leg run twice; SHA-256 of full stdout compared. Any difference = FAIL.
4. **Robustness**: rc==0, no panic, no stderr crash on well-formed input at every leg.

## Kill bars (frozen — set from standing law, NOT from pilot values)

- **K1 (determinism, absolute):** any byte difference between two runs of the same leg → FAIL the mechanism's scale claim.
- **K2 (no flips, absolute):** any per-item verdict flip between 1x and a higher leg on identical item content → scale-rot FAIL. (Deterministic systems must give the same answer to the same item regardless of batch size or position.)
- **K3 (no crash, absolute):** any panic / rc≠0 / truncated output on well-formed input at any leg → scale-rot FAIL and a P0 work order to the owning line.
- **K4 (no accuracy rot):** pass-rate drop >5 percentage points at a higher leg vs 1x → scale-rot FAIL.
- **K5 (disk gate):** no leg may run while home-disk free <2GB. A leg that cannot run under K5 is reported BLOCKED ON DISK, never approximated.

## Execution order

1. Commit this prereg first (API replay onto current origin head).
2. Official confirmation runs AFTER the prereg commit (1x + 10x per mechanism; 100x only if K5 allows).
3. Write REPORT.md; commit.

## Pre-freeze disclosure

Engineering/pipeline pilots for M1 (1x: 23/44; 10x: 230/440, 0 flips) and M2
(1x: 27/33; 10x: 270/330, 0 flips) ran BEFORE this prereg was written, to validate
the replication harness. They are disclosed here and are NOT official evidence.
Bars above were frozen from standing law (zero flips, zero nondeterminism, zero
crashes tolerated), not tuned to the pilot values. Official legs re-run the same
commands after this commit.

## Out of scope

Fixing defects found (owning lines fix; this battery files work orders). 100x legs
while K5 blocks. M4 until its dependency lands.
