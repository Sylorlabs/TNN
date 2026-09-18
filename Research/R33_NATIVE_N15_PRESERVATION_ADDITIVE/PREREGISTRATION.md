# R33-N15 preservation/additive stability-plasticity diagnostic

Identity: `r33-native-n15-preservation-additive-microlearner-v1`.
Preregistered 2026-09-07 after independent exact-evidence review V3.
Owner: main agent, sole registry writer and launcher.

This is a bounded native-Zag synthetic microlearner scientific diagnostic. It is not a recovered or behaviorally continuous R27 learner, not a newborn replacement, not a large integrated R33 training campaign, and not promotion evidence. R27 remains canonical at development step 60,423 with zero newborn restarts.

## Scientific question

Can a zero-initialized additive specialist, optionally combined with training-only preservation gating, move the stability/plasticity frontier relative to shared-parameter rewriting, strict preservation, frozen-parent, and reduced/thinned-update controls?

The intended result is mechanism-direction evidence for a later continuing learner. Even a full N15 pass cannot establish original-R27 continuity, end-to-end sensing, general cognition, durable full learner state, authority, or R33>R27 promotion.

## Frozen reviewed identity

Independent V1 and V2 reviews returned `REQUEST_CHANGES` before scientific exposure. Their blockers were corrected and retained in `INDEPENDENT_REVIEW_V1.md` and `INDEPENDENT_REVIEW_V2.md`.

Independent V3 returned `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`, report SHA256 `d58cb2700126dd78da845013561c262c21054253018d9a8632ef13a73bc091e1`.

Reviewed candidate:

- `driver.zag` SHA256 `1ca75e7cae4f0fbf03e15b1d637c56f4c740e5897f3bbe28a4e6a10bfe0300a7`.
- `CONFIG.json` SHA256 `1105d3a91004048c5d88a4c0d848b5b7d15b1ecbc8328dff13aeda787559465c`.
- `DESIGN.md` SHA256 `369e6d789273635ff733885d172b4d65b9947b04b3db56cf8c6813b1f052a4ce`.
- `AUTHORING_HISTORY.md` SHA256 `e5249a105f98700677dc1c71f52fa189a4ddf690af65d0617bd13571ce37fea0`.
- selected BUILD_09 and comparison BUILD_10 are byte-identical 115,712-byte arm64 Mach-O binaries, SHA256 `1f7b78d9f90153de1182887f813af70c884c6d59286e7c31e78fa62c936b4d3a`.
- compiler `Research/toolchain/znc_macos_arm64_7cacbfc0` SHA256 `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`, flags `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.
- Smoke03, Smoke06 and Smoke07 stdout are byte-identical, SHA256 `4c88eae9d8bc3422810a0cef1b423466857f0915414ed1fcab20d01f66dee58f`. Smoke is authoring evidence only.

No development, validation, or confirmation namespace had been exposed at preregistration.

## Development stage

Invoke selected BUILD_09 in mode `dev` exactly once. Namespace is 510000. The binary executes 12 frozen arms over 8 development populations, exactly 96 arm-population exposures.

The native selector is authoritative. Eligibility requires, for one non-frozen arm, positive `new_gain` in every development population, maximum final-old deficit <=4, and total new gain >=128. Eligible arms are ordered by smallest total `old_lost`, then largest minimum `new_gain`, then largest total `new_gain`, then lowest arm id. If no arm qualifies, fallback chooses the non-frozen positive-aggregate-new-gain arm with minimum total `old_lost`; ascending traversal gives the lowest arm id on an exact loss tie, and native gate=0.

If no non-frozen arm has positive aggregate new gain, the native selector emits `N15_DEV_SELECTION,-1,0`. That is terminal `DEVELOPMENT_NO_POSITIVE_GAIN_CANDIDATE`: development is consumed and validation/confirmation are forbidden.

After development settles, the exact native `N15_DEV_SELECTION,<arm>,<gate>` line and full stdout SHA256 are frozen before any holdout exposure. No external process may recompute or replace the native scientific selection.

## Validation stage

If development selected a real arm 1..11, invoke `validate <selected-arm> <development-gate>` exactly once. Namespace is 610000, 12 untouched populations. Fixed controls are arms 0,1,4,8; the selected arm is added only when distinct. Thus validation contains 48 or 60 arm-population exposures.

A real selected arm with development gate0 is allowed exactly one exploratory validation; the native holdout gate is forced to0 by the upstream bit and confirmation is forbidden.

For qualification, the native validation gate requires all frozen CONFIG conditions: positive selected-arm new gain in every population; max final-old deficit <=4; max pointwise `old_lost` <=8; total `old_lost` <=48; total new gain >=192; at least half arm1's total new gain with at most one quarter arm1's total old loss; total new gain greater than arm4; and, for selected arm10/11, at least half arm8's total new gain with at most half arm8's total old loss.

The exact native `N15_HOLDOUT_GATE,N15_VAL,<arm>,<upstream>,<gate>` line and validation stdout SHA256 are frozen before confirmation.

## Confirmation stage

Confirmation is admissible only if the native validation gate equals1. Invoke `confirm <same-selected-arm> 1` exactly once. Namespace is 710000, 12 untouched populations, same fixed controls and same frozen native holdout gate. Confirmation contains 48 or 60 arm-population exposures.

Full N15 scientific success requires native development gate1, native validation gate1, and native confirmation gate1. No threshold, source, mechanism, arm, seed, control, or budget may change after exposure.

## Measurement and leakage controls

Every arm starts from the same synthetic parent within a population. New learning sees only new-training examples. Preservation uses a fixed subset of old training anchors. Additive routing uses only unlabeled old/new training-input prototypes. Old/new probe outcomes are evaluator-only and occur after learning; they never fit, accept, reject, gate, stop, retry, or route a learner update.

Retain every per-arm/population row: parent/final old correctness, pointwise old losses/rescues, parent/final new correctness and new gain, proposals, accepted/rejected/skipped updates, anchor loss, and parent update count. Retain native arm summaries and gates. Report regressions and population reversals, not just averages.

## Resource and execution contract

Each scientific stage has one actual invocation maximum, including failure. First invocation consumes that stage. No retry or rerun is permitted. The maximum campaign exposure is 216 arm-population runs when a non-control arm is selected and all three stages execute.

Operational shell capture may record stdout/stderr/hash/resource accounting; it may not act as the scientific evaluator. Per-stage guard is 60 CPU seconds, output capture limit is 1,048,576 bytes, and observed maximum resident set acceptance ceiling is 67,108,864 bytes. These are operational bounds, not hostile-host containment.

Exclusive evidence roots:

- development: `Research/R33_NATIVE_N15_DEV_PRIMARY_V1`
- validation: `Research/R33_NATIVE_N15_VALIDATION_PRIMARY_V1`
- confirmation: `Research/R33_NATIVE_N15_CONFIRMATION_PRIMARY_V1`

No stage mutates R27, any consumed R33/R32 primary, or canonical state. Scientific microlearner training occurs only inside the synthetic N15 process. Canonical mutation=false, learner authority=false, promotion=false.
