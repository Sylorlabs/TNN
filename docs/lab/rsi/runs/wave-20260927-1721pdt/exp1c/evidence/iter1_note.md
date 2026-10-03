# EXP1c Iteration 1 Evidence Note
Wave 20260927-1721pdt, retune iteration 1 (vel=0, lo<hi stationarity family).

## Provenance
- Frozen prereg: docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md at 8b456736b
- Addendum: docs/lab/rsi/runs/wave-20260927-1721pdt/preregs/ADDENDUM_EXP1c_1721.md at 763983e3a62b119edf5eb16a5e67307e0ef86798
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1 (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef)
- World: lab/invention/survival/src/world.zag (blob fff8af2493bc6dbe9de6fc76f9a6206d887d586a)

## Implementation
From-scratch pure Zag, no Python. Four source files under exp1c/src/:
- x1c_params.zag: variant parameter block, rule checks, frozen-world application
- x1c_variants.zag: 12 vel=0 lo<hi variants, self-labeled RETUNE ITERATION 1
- x1c_agents.zag: P/R/Z/I arms, calibration strategies
- x1c_runner.zag: five modes (check, variants, calibrate, run, bound)

Critical correctness fixes during implementation:
1. The frozen world uses w.apos (not w.pos), W_NCELLS (not w.ncell), storms as TIME windows O_STORMS/O_STORME (not spatial), and its own w_step (no reimplementation).
2. Toolchain _zag_malloc can return overlapping blocks on successive calls; fixed by single-allocation arena partitioning in main and by removing _zag_malloc from the print-flush path.

## Mode check (gates calibration in-code)
CHECK_OK. Two violations found and fixed during development (variant 1 home-in-range, variant 5 respawn-on-start); final check passes all 12.

## Calibration medians (two independent methods agree)
- p_ward: 1200 / 1200 AGREE
- forage: 1200 / 1200 AGREE
- lampfarm: 11 / 11 AGREE
- cachefarm: 1200 / 1200 AGREE
- z: 45 / 45 AGREE

Gates:
- C1 median_p_ward=1200 >= 960: PASS
- C2 median_z=45 < 300: PASS
- C3 3 of 4 strategies >= 720: PASS

## Full experiment (144,000 agent-ticks, two byte-identical runs)
SHA-256 of both runs: 4aea7251fcf74d4702c8a0e9debbc7b9465fbd4e36740953ddaa6943c34272fa

Medians (both methods agree):
- P: 1200, Z: 45, R: 1200, Is: 81, Ii: 81

Kill bars:
- K1 median_Is=81 <= median_R=1200: KILL (I arm terminated)
- K2 median_Is=81 > median_Z=45: PASS
- K3 median_P=1200 >= 960: PASS (positive control valid)
- K6 ablation median 81 < original 81 is false; 81 >= 81 FIRES on the Is arm by the frozen rule (equal medians trigger). The ablated traces replaced 0 TAKE/DROP/COMBINE actions, indicating the I arm never reached those actions before death.
- K7: VOID (no post-enumeration plans observed; enumeration never completes)

## Section 7 bound reproduction
FROZEN CLAIM: 399 sketches complete before tick 600 of 1200.
MEASURED: 0 of 24 I-arm runs completed enumeration; max enum tick -1 (none).
RESULT: NOT-MET. The frozen arithmetic (7+49+343=399 plans, 1134 primitive actions minimum) is inconsistent with completion before tick 600 under one action per tick. Reported honestly; requirement not weakened.

## Verdict
C1 PASS, C2 PASS, C3 PASS. Full experiment ran. K1 KILL fires on the I arm. Section 7 bound not reproduced. Per binding requirement (f), iteration 2 (boundary-trap family) is now required.

## Known issues
- Ablation TSV orig_ticks column shows incorrect values for variants 4-10 (memory integrity issue under investigation); ablated_ticks and medians are correct; K6 verdict unaffected.
- Probe files probe1-9.zag in src/ are scratch; to be removed before final commit.

## Hashes
See iter1_hashes.txt for SHA-256 of all evidence files.
