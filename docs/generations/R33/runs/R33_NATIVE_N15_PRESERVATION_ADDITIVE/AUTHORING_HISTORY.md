# R33-N15 authoring history

## Smoke 01 — single engineering fixture, superseded

The first compile-only candidate used a one-sided new-prototype gate. On the fixed smoke namespace 410000, ordinary shared rewriting gained 321/512 new-probe successes but reduced old-probe correctness from 501/512 to 141/512. Shared preservation tolerance0 retained 501/512 old correctness but had -2 new gain. The strongest initial additive arm gained 318 but lost151 old successes; additive+preservation retained 484–488 old correctness with +27/+28 gain. This exposed a gate-locality defect before development exposure.

## Smoke 02 — final gate shape chosen before development

The candidate was revised to a generic two-prototype gate estimated from unlabeled old/new training inputs. No probe label or success membership enters the gate. On the same fixed engineering fixture, ordinary shared rewriting again collapsed old correctness to141/512 with +321 new gain. Additive+preservation arms10/11 retained498/501 old correctness while gaining +111/+187 new successes. This smoke is authoring evidence only and is not part of development, validation, confirmation, or a promotion claim.

After Smoke02 the gate shape/radii, training epochs, update rule, arm matrix, population namespaces and selection criterion are frozen for the development campaign. The only subsequent source change before freeze is native in-program implementation of the already-written CONFIG selection rule so no non-Zag scientific evaluator is needed.

## Pre-development holdout/evaluator correction — no scientific exposure

Static pre-registration inspection found two control-flow defects before any development population was exposed. First, the CONFIG fallback can select arm1, while the initial holdout entrypoint rejected selected arms below2 and would therefore have made a legal fallback impossible to inspect. Second, validation rows were emitted without a native validation-to-confirmation gate, which is insufficient under the native-only scientific-evaluator contract.

The correction changes only outcome telemetry, holdout admissibility, fixed-control de-duplication, and native aggregation/gating. It does not change any learner update, additive routing radius, preservation tolerance, training epoch, training/probe example, seed namespace, development arm, or development selection criterion. The corrected binary will be double-built and run only on the already-disclosed smoke fixture before independent re-review. Exact smoke-row equivalence to the final pre-correction smoke is required before development admission.

Corrected BUILD_07 and BUILD_08 compiled independently with the pinned macOS-arm64 compiler and are byte-identical, SHA256 `468ab52ccb70906fb7348dfb5cfabf5489ace31e959a1f9e096be63947badaf9`. Corrected source SHA256 before this authoring-history receipt was `3df68397b27b4498169dda6775a6b6031839d3cfc9a8ee30b0544467eee71122`; CONFIG SHA256 is `57b86aea678e88cb18110a4b523eaeda088ebbeb2a6d3c93e10ca37ed2052397`; DESIGN SHA256 is `6bf37e0e640e45919fdd70fd0121aa856c5863cc48208c5c9fb0e1694142cbf3`.

BUILD_07 Smoke04 and BUILD_08 Smoke05 each reproduced the final pre-correction Smoke03 stdout byte-for-byte. All three smoke stdout files SHA256 to `4c88eae9d8bc3422810a0cef1b423466857f0915414ed1fcab20d01f66dee58f`. Smoke remains engineering/authoring evidence only and allocates no development, validation, or confirmation population.

Independent review V1 of the earlier BUILD_05/06 identity returned `REQUEST_CHANGES`. It independently identified the arm1 holdout mismatch and missing native validation gate, and additionally found that the development fallback silently used total new gain as an undeclared equal-loss tie-break. The V1 report is retained in `INDEPENDENT_REVIEW_V1.md`; no scientific exposure occurred.

The fallback is now corrected to the literal CONFIG rule: among non-frozen arms with positive aggregate new gain, minimize total `old_lost`; ascending arm traversal preserves the lowest arm id on an exact loss tie. Inter-stage binding is also made explicit in CONFIG/DESIGN: development native selection is frozen before validation, validation native gate is frozen before confirmation, the selected arm cannot change, and each stage is single-invocation/no-rerun. Because the fallback source changed after BUILD_07/08, a new double build and smoke-equivalence check is required before V2 review or preregistration.

BUILD_09 and BUILD_10 are the corrected V2-review candidate. They compiled independently with the pinned native compiler, both compiler stderr receipts are zero bytes, and the binaries are byte-identical SHA256 `1f7b78d9f90153de1182887f813af70c884c6d59286e7c31e78fa62c936b4d3a`. Smoke06 from BUILD_09 and Smoke07 from BUILD_10 each reproduce Smoke03 byte-for-byte. No development, validation, or confirmation seed namespace has been executed.

Independent review V2 returned `REQUEST_CHANGES` on one remaining edge case while confirming all three V1 blockers closed. The native development selector can legitimately emit `-1,0` if no non-frozen arm has positive aggregate new gain. The V2 protocol had not explicitly bound that sentinel. `INDEPENDENT_REVIEW_V2.md` preserves the review. CONFIG/DESIGN now define `-1` as terminal `DEVELOPMENT_NO_POSITIVE_GAIN_CANDIDATE`: development is consumed and no holdout population may be exposed. This change does not modify `driver.zag` or either BUILD_09/10 binary.
