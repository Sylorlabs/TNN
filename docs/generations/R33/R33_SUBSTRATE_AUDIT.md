# R33 sensory, hardcoding and observability source audit

Audit date: 2026-09-05. Method: local source inspection and immutable identity
checks, not a new native learning run. **No modality is certified end-to-end.**
Scope and pinned bytes: [audit scope](R33_AUDIT_SCOPE.json).

## Distinct paths

The latest E51AJ executable assembles a synthetic evidence/action-value harness
through `.github/scripts/e51aj_assemble.py`. Its assembled source and retained
ZIP were hash-checked during this audit against the E51AJ evidence package.
The broader `tnn_r32_epistemic_chunking.zag` contains prototype sensory, memory,
Foundry and trace facilities. A result from one path does not qualify another.

E51AJ receives 32 projected current-state values plus a preceding same-trajectory
projection, not natural waveform/video input. `e50_batch_column` maps projected
coordinates 3 and 5 to record columns 32 and 33. Columns 34–37 are outcome
targets, not features. `e51ai_feature_pair` checks bounds and zeroes the lag at
t=0; this is useful local isolation evidence, not full information-flow proof.
The assembler reuses these functions with the AJ namespace. No assembler or
experiment was rerun for this audit.

## Findings and required disposition

| ID | Source / location | Observed behavior | Qualification consequence / next falsifier |
|---|---|---|---|
| SA-01 | `tnn_r32_epistemic_chunking.zag:262`, `core_relational_signature8` | Mean subtraction, sorting and span normalization remove absolute level, receptor order and scale | Auxiliary invariant feature only. Permutations have identical signatures although raw arrays differ; verify an independent raw bypass before identity claims |
| SA-02 | Same file:356, `acoustic_window_distance` | Samples `start + floor(i*duration/width)`; width default 12 | Detail between sampled positions can disappear. An odd-index impulse in a 24-sample window is missed at width 12. Test actual raw ingress separately |
| SA-03 | Same file:1362, `r32_raw_temporal_signature` | Histograms hash microstate, pair and triple counts into finite bins | This is not raw waveform storage or exact full temporal order. Require collision witnesses and original-payload retrieval; do not certify it by its name |
| SA-04 | Same file:1487, `r32_temporal_pam_apply` and pooling | Fixed-point products in i32, rectification, clamping, then max/mean pooling | Negative values and order can be lost; overflow envelope unqualified. Count clipping/overflow and compare signed/raw routes before higher-level blame |
| SA-05 | Same file:57–67, `trace_emit` | Returns silently at 8,192 entries | Meaningful mutations after saturation may lack traces. Block white-box qualification until durable append/backpressure or explicit failure is enforced |
| SA-06 | Same file:881–904, `r31_segment` / `r31_reconstruct` | Output capacity stops processing without a completeness/error return | Reversibility requires sufficient capacity and a frozen/versioned codebook. Test truncation, codebook mutation, and nonnegative microstate preconditions; signed samples must not be treated as anonymous IDs |
| SA-07 | Same file:648, `lru_evict_candidate` | If every slot is marked protected, falls back to the oldest protected slot | `protected_exact` is a preference here, not inviolable authority. Protected retention needs a checked refusal/spill policy before M1 |
| SA-08 | Same file:608, `innate_system_fluency` | Accepts operation IDs 1–9 | Does not itself dispatch, authorize, meter or verify those operations. A passing recognition test is not system-function fluency or a rollback mechanism |
| SA-09 | Same file:244 and 1531, Foundry promotion helpers | Local score/regression thresholds return acceptance or change candidate status | No human grant, external root signature or transactional canary established by these functions. They may propose, not self-authorize, live deployment |
| SA-10 | E45 state tape and E51AI/AJ data construction | Ordered synthetic evidence becomes fixed state projections; only last accessible train state is selected | Synthetic chronology exists, but sufficiency for earlier states and natural action timing remains unqualified; preserve train-support versus probe-support distinction |
| SA-11 | Prototype trace wrappers:469–504,1330–1348,1469–1476 | Several confidence values/reason codes are fixed or formulaic; not all state is represented | Report recorded scalars as heuristics, not calibrated introspection. Require before/after state, exact parents, and missing-coverage flags |

The permutation and subsampling examples above are deductions from the source,
not newly measured native results. None proves that all callers discard their
raw arrays, or that the whole architecture is incapable of discrimination.
The failure is to have established a qualified complete path, not evidence for
a universal cognitive limit.

## Modality readiness

| Modality / boundary | Current supported evidence | Missing evidence | Status |
|---|---|---|---|
| Natural audio | Prototype template/temporal numerical operations | Byte/sample-rate/channel/clock fidelity, physical waveform reload, coarticulation, speaker/rate/noise transfer | NOT_QUALIFIED |
| Natural vision | Eight-dimensional synthetic invariant and episodic matching | Pixel/frame/encoding ingress, motion/occlusion/viewpoint/near-twin preservation and raw bypass | NOT_QUALIFIED |
| Synthetic temporal evidence | Native E51 lineage; explicit ordered tape and grounded projections | Full reachable-call isolation, overflow envelope, complete persistent brain reload | PARTIAL_NARROW_EVIDENCE |
| Action/consequence timing | Synthetic tape/cost construction | Physical timestamp/delay continuity, pending-action reload, asynchronous ordering | NOT_QUALIFIED |
| Trace integrity | Parent-coded prototype records, AJ coefficient/exposure logs | Lossless lifetime trace, durable transaction binding, complete mutable-state inventory | NOT_QUALIFIED |

## What was preserved

R27 state and R32 frozen sources/results were not modified. Baseline V1 digest
is pinned in the audit scope. AJ's assembled source and archive match their
published hashes; this audit did not rerun the archived verifier or scientific
binary and does not claim a new full archive validation.

## Hardcoding and next action

The [default-hardcoding inventory](R33_BIRTH_SUBSTRATE_HARDCODING_PLAN.md)
classifies every capability family in the inspected prototype, including
hand-authored memory, identity, testimony, observation and diagnosis biases.
It does not certify every transitive historical harness constant as generic.
Before importing any such harness into R33, complete its call-boundary audit.

The first native audit batch should produce bounded witnesses for SA-01,
SA-02, SA-05, SA-06 and SA-07 without invoking world generators or training.
Full raw-ingress implementation and adversarial sensor qualification follow;
capacity and preservation campaigns remain behind the relevant gates.
