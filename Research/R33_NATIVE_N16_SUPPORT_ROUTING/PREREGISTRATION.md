# R33-N16 broader-support / localized-routing preregistration

Identity: `r33-native-n16-support-routing-frontier-v1`.
Preregistered 2026-09-08 UTC after independent pre-run review V3.
Owner: main agent, sole registry writer and launcher.

R33-N16 is a bounded native-Zag synthetic stability/plasticity mechanism
diagnostic. It is not canonical R27, does not load or emulate the accepted R27
learner, and cannot establish R27 behavioral continuity or promotion. R27
remains canonical at development step 60,423 with zero newborn restarts.

## Scientific question

N15 showed a bounded stability/plasticity signal: additive specialization plus
preservation retained useful new learning, but protected anchors did not
generalize to unseen old behavior. N16 tests, with fresh populations, whether
broader training-side old-support protection and more selective specialist
routing move that synthetic frontier.

## Reviewed identity

Independent V1 and V2 returned `REQUEST_CHANGES` before scientific exposure;
their exact reports are retained. V3 returned
`APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`, SHA256
`eaba6a1d9aad92f68927e529269ae891848cd7c8f1070a2d9624de91a7ef3eeb`.

The exact V3 reviewed-input manifest is
`PRE_REVIEW_V3_INPUTS.sha256`, SHA256
`02c4016fee3cac4b74d8c5c82056bfc1a377d19aac2db58e3d55ef676dcd7cb1`,
26 entries verified.

- `driver.zag`: `ab6f9bc44ebb1ccdd06971a47ef70fd094f5bdc21101d5f26b4107bf7900bc46`
- `CONFIG.json`: `4a72fbdd2ba7cbc2b09a8cacf493d0550533dd8ecd1b8e6530936b4341d957c7`
- `DESIGN.md`: `95f9c96bd2d52db3eac8c7d49c2f45e1c1672d4f96f60e7198d69c32f5bd95e0`
- `AUTHORING_HISTORY.md`: `53300cbeda22900714010d26cb219a75c917deefb548330410c932e534ca0d2d`
- selected BUILD_11 and comparison BUILD_12: byte-identical 148,736-byte
  arm64 Mach-O binaries, SHA256
  `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`
- compiler `Research/toolchain/znc_macos_arm64_7cacbfc0`: SHA256
  `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`,
  flags `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`
- Smoke10/11 stdout: byte-identical SHA256
  `073f47cbfd9fe9cffd5976b2c5d3284dea08bf94426433953dbdeea8dd8e9dca`.
  Smoke is authoring evidence only and uses namespace 810000.

No development, validation, or confirmation population had been exposed at
preregistration.

## Development

Invoke selected BUILD_11 in mode `dev` exactly once. Development namespace is
910000. The native binary executes all 21 frozen arms over 10 fresh
populations: exactly 210 arm-population exposures.

The native selector is authoritative. A non-frozen arm is eligible only if it
has positive `new_gain` in every development population, maximum final-old
deficit <=4, maximum pointwise `old_lost` <=6, total `old_lost` <=40, and total
`new_gain` >=800. Eligible arms are ordered by smallest total `old_lost`, then
largest minimum `new_gain`, then largest total `new_gain`, then lowest arm id.
If no arm is eligible, native fallback chooses a non-frozen arm with positive
aggregate new gain minimizing total `old_lost`; gate=0. If native selection is
`N16_DEV_SELECTION,-1,0`, development is a terminal negative and no holdout may
run.

The exact native selection line and complete development stdout hash must be
frozen before any validation exposure. No external process may recompute or
replace the native scientific selection.

## Validation

If development selects a real arm 1..20, invoke
`validate <selected-arm> <development-gate>` exactly once on namespace 1010000
and 16 untouched populations. Fixed controls are arms 0,1,3,4,6,8,14,17; the
selected arm is added only when distinct. Thus validation contains exactly 128
or 144 arm-population exposures.

A real selected arm with development gate0 may receive exactly one exploratory
validation with upstream0; the native validation gate is forced to0 and
confirmation is forbidden.

With upstream1, selected-arm qualification requires positive new gain in every
population, max final-old deficit <=4, max pointwise `old_lost` <=6, total
`old_lost` <=48, and total `new_gain` >=1600. It must retain at least 35% of
arm1 new gain while using at most 2% of arm1 old loss, and at least 80% of arm4
new gain while using at most half arm4 old loss. Preserved eight-cluster arms
9-12 additionally compare against arm6 (>=80% new gain, no greater old loss)
and arm8 (>=40% new gain, <=one-quarter old loss). Arm15 additionally compares
against arm14 at >=40% new gain and <=one-quarter old loss. Arms18/19 compare
against arm17 at the same 40% / one-quarter thresholds.

## Confirmation

Confirmation is admissible only if the native validation gate equals1. Invoke
`confirm <same-selected-arm> 1` exactly once on namespace 1110000 with the same
16-population control matrix and frozen holdout gate. Confirmation contains 128
or 144 arm-population exposures. Full N16 scientific qualification requires
native development gate1, native validation gate1, and native confirmation
gate1.

## Support, routing, and leakage controls

Old/new probes are evaluator-only and occur after training. Probe correctness,
probe membership, gate-hit telemetry, evaluator bits, or held-out outcomes may
not fit, accept, reject, route, stop, retry, or retune a learner update.

The second old-support set is training-side, not a probe. Dual-support
preservation arms2/6/7/11/12/19 evaluate synthetic old-target correctness on
those support inputs and use resulting protected-behavior loss only to accept
or reject proposed updates. Occupancy arms14/15 additionally use unlabeled
support-input occupancy counts for their routing veto. The support set never
contributes probe outcomes, task ids, evaluator bits, or gradient/update fitting.

Eight-cluster and projection routing use only training-input geometry. No task
id, probe membership, target truth, held-out correctness, or evaluator bit is a
routing input.

Retain every per-population arm row, native arm summary, native selection/gate,
old losses/rescues, new gains, routing hits, proposal/accept/reject/skip counts,
and preservation loss/check counts. Negative results and population reversals
must be retained.

## Execution contract

Each scientific stage has one actual invocation maximum. The first invocation
consumes that stage regardless of exit status or partial output. No retry,
rerun, retuning, arm substitution, threshold change, population reuse, or
post-exposure mechanism change is allowed.

Maximum campaign exposure is 498 arm-population runs: 210 development plus up
to 144 validation plus up to 144 confirmation. Operational shell capture may
record stdout/stderr/hash/resource accounting but may not become a scientific
evaluator. Per-stage prospective CPU guard is 180 seconds, capture limit is
1,048,576 bytes, and observed RSS acceptance ceiling is 67,108,864 bytes.

Exclusive evidence roots:

- development: `Research/R33_NATIVE_N16_DEV_PRIMARY_V1`
- validation: `Research/R33_NATIVE_N16_VALIDATION_PRIMARY_V1`
- confirmation: `Research/R33_NATIVE_N16_CONFIRMATION_PRIMARY_V1`

Preregistration and independent review do not authorize execution. Exact freeze
and a separate per-stage admission are required before each invocation.
Canonical mutation=false, learner authority=false, promotion=false.
