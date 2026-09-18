# R33-N18 — frozen-parent native-surrogate composite design

Status: **DESIGN-ONLY; REVIEW REQUESTED; NOT REGISTERED; NOT PREREGISTERED;
NOT RESERVED; NOT FROZEN; NOT ADMITTED; NOT EXECUTED**.

## Decision forced by review

The proposed shortcut—keep the canonical R27 file unchanged and attach the
qualified N16 arm19 learner—does not, by itself, establish that the native
execution path is canonical R27. Byte custody proves non-mutation, not
behavioral continuity. N18 therefore cannot currently claim that a composite
beats canonical R27.

N18 is retained as a design packet for the first admissible point at which one
of these prerequisites is true:

1. N17 reaches `FULL_NATIVE_R27_CONTINUITY_QUALIFIED`; or
2. the governing methodology is prospectively amended, before any N18
   exposure, to define a separate `FROZEN_PARENT_NATIVE_SURROGATE_COMPOSITE`
   benchmark class.

Under route 2, the result remains a native-surrogate benchmark and may not be
reported as an R27 descendant, canonical win, promotion, learner-authority
grant or canonical mutation.

## Question

With the canonical R27 bytes held immutable, does a native sidecar implementing
the already-qualified N16 arm19 mechanism improve new-task acquisition while
preserving old-task behavior, compared with the same native parent path alone?

This is a paired composite-vs-parent question. It is not a request to mutate
R27, retrain N16, or infer continuity from digest equality alone.

## Immutable parent and mechanism pins

- canonical R27 accepted-state bytes: SHA256
  `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`;
- original release ZIP: SHA256
  `7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e`;
- canonical development step: `60423`;
- canonical newborn restarts: `0`;
- N16 selected mechanism: arm `19`,
  `additive_training_mean_projection_gate_75pct_dual512_preservation_tolerance1`;
- N16 selected binary: SHA256
  `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`;
- N16 synthetic qualification evidence: `Research/R33_N16_CLOSEOUT_SUMMARY.md`;
- N16 final independent review: `Research/R33_NATIVE_N16_SUPPORT_ROUTING/POSTRUN_INDEPENDENT_REVIEW.md`;
- governing contract: `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md`.

N16 arm19 is treated as a frozen algorithmic identity. No R27 observation may
retune its projection threshold, support size, tolerance, routing rule,
update dose, or preservation rule.

## Required parent-path prerequisite

Before registration, the candidate must contain a native parent-path identity
that is explicitly classified by the governing contract as either:

- `FULL_NATIVE_R27_CONTINUITY_QUALIFIED` from N17; or
- a prospectively approved, separately named surrogate-parent class with its
  own source, evaluator and claim boundary.

An R27 raw hash, recovered source, historical 33/33 receipt, or reproduced
semantic digest is not sufficient by itself. N18 must not use a partial N17
level as an implicit behavioral substitute.

## Conditions

Every condition starts from the same immutable parent bytes and the same
fresh, paired population inputs. Each condition receives a private run-local
working copy; the canonical R27 file is opened read-only and is verified
byte-for-byte before and after every stage.

The exact parent-to-sidecar data boundary is separately specified in
`SIDECAR_INTERFACE_CONTRACT.md`. That boundary is currently unresolved and is
a `DEFERRED_BLOCKER`; the existing synthetic N16 16-coordinate interface may
not be treated as a drop-in R27 representation.

The future run-local C0 parent copy may learn under the fixed parent protocol,
but it is never the canonical R27 file. C0, C1 and C2 start from byte-identical
private copies; C3 starts from the same parent bytes plus only its predeclared
randomized sidecar state. No condition may write the canonical file.

| ID | Condition | Purpose |
|---|---|---|
| C0 | parent-only native path | baseline parent learning and evaluation |
| C1 | matched no-op adapter | separates sidecar interface/wrapper effects from learning |
| C2 | frozen N16 arm19 sidecar | primary composite condition |
| C3 | matched randomized/untrained sidecar | tests whether any gain requires the trained arm19 mechanism |

C1 must perform the same adapter calls, allocation schedule, telemetry shape
and resource accounting as C2 while contributing exactly zero output delta.
C3 must use the same sidecar shape and budget as C2, but its parameters or
route assignments are generated from a frozen independent seed and it receives
no accepted updates. C3 is a negative control, not a fifth tuning opportunity.

The parent-only path and composite path must use the same parent inputs,
training dose, scoring, seed schedule, resource limits and evaluator. A
condition may not inspect another condition's outputs during training or
evaluation.

## Fresh staged exposure

No stage is currently authorized. If the prerequisite and review gates pass,
the following fresh namespaces are reserved once and then consumed by their
first actual invocation:

- development: namespace `1210000`, 10 paired populations, 4 conditions = 40
  condition-population exposures;
- validation: namespace `1310000`, 16 paired populations, 4 conditions = 64
  exposures;
- confirmation: namespace `1410000`, 16 paired populations, 4 conditions = 64
  exposures.

Maximum campaign exposure is `168` condition-population runs. Development,
validation and confirmation populations are mutually disjoint. Conditions are
paired within a population; this is intentional and is part of the design.
No N16 population or namespace may be reused.

There is no arm search. Arm19 is fixed before exposure. Development can only
qualify the fixed comparison protocol and check the preregistered feasibility
guards; it cannot select a new sidecar, threshold, or control.

## Training/evaluation separation

For each population:

1. Generate old-support and new-training inputs from fixed training-side seed
   offsets.
2. Run the parent-only or composite training path using only those inputs.
3. Generate old and new probes from separate evaluator-only offsets after
   training.
4. Score parent and final behavior using the same native evaluator.

Old probes, new probes, task identifiers, evaluator bits and holdout outcomes
may not fit, route, accept, reject, stop, retry or retune any sidecar update.
Training targets are permitted only on the fixed old-support and new-training
records declared in `SIDECAR_INTERFACE_CONTRACT.md`; evaluator/probe/holdout
truth is never delivered to the sidecar. The sidecar may use the two
training-side old-support sets in the already-qualified N16 preservation role,
but those sets remain distinct from evaluator probes.

The sidecar may emit a residual contribution and telemetry, but it may not
rewrite the canonical parent bytes, alter the parent development step, change
newborn-restart metadata, grant learner authority, or publish a promotion.

## Primary endpoints and fixed win rule

The following rule is fixed at design time and must not be changed after the
first exposure. Each population has `512` old probes and `512` new probes.

For condition `c`, define:

- `old_lost[c]`: old probes correct before training but incorrect after;
- `new_gain[c]`: new probes incorrect before training but correct after;
- `old_accuracy[c]`: final correct old probes divided by 512;
- `new_accuracy[c]`: final correct new probes divided by 512.

The primary confirmation win for C2 over C0 requires all of the following:

- C2 has strictly greater aggregate `new_gain` than C0;
- C2 has at least 12 of 16 populations with `new_gain[C2] > new_gain[C0]`;
- C2 has no more than 4 additional `old_lost` than C0 in any population;
- aggregate `old_lost[C2] - old_lost[C0] <= 16`;
- C2 has no lower aggregate `old_accuracy` than C0 by more than 0.01;
- the native confirmation gate reports success without external rescoring.

The comparison is paired by population. C1 is a true no-op control: every
pre-training count, final count, decision, old-loss, new-gain, update count,
route count and refusal result must equal C0 exactly. Any C1/C0 mismatch is an
interface failure and invalidates the stage. C3 must not satisfy the C2 primary
win rule. In addition, if C3 has aggregate new gain greater than C0 while its
aggregate old-loss increase is at most 16, N18 is classified as a nonspecific
sidecar/budget effect and fails mechanistically even if C2 also wins.

The confirmation gate also requires positive new gain for C2 in at least 14 of
16 populations and no population-level old-accuracy decrease greater than
`4/512`. These are fixed feasibility guards, not post hoc interpretation.

Development and validation use the same endpoint definitions. Development is
not allowed to alter the thresholds. Validation gate success is required for
confirmation; a failed stage consumes that stage and forbids retry.

The stage gates are fixed as follows. Development passes only if C2 has greater
aggregate new gain than C0, exceeds C0 in at least 7 of 10 populations, has no
more than 4 additional old losses in any population, has aggregate additional
old loss at most 10, and C1/C3 satisfy their exact control rules. Validation
passes only if C2 has greater aggregate new gain than C0, exceeds C0 in at least
12 of 16 populations, has positive new gain in at least 12 populations, has no
more than 4 additional old losses in any population, has aggregate additional
old loss at most 16, and C1/C3 satisfy their exact control rules. Confirmation
uses the stricter primary rule above plus at least 14 of 16 populations with
positive C2 new gain and the `4/512` per-population old-accuracy guard. A failed
development or validation gate prevents the next stage; each failed stage
remains consumed.

Baseline correctness must be identical across C0-C3 before training. Any
baseline mismatch is a population-integrity failure, not a score to be
adjusted. Aggregate old accuracy is pooled integer correctness over all 16 x
512 old probes (denominator 8192); no per-population rounding is used.

There is one confirmatory hypothesis only: C2 versus C0 under the fixed primary
rule. C1 and C3 are integrity controls, not additional claims. No p-value,
threshold, endpoint, condition, or secondary metric may be selected after
exposure; all other rows are descriptive and cannot rescue a failed gate.

The C3 nonspecific-benefit sentinel is stage-relative and exact: in development
it fails N18 if C3 aggregate new gain exceeds C0 while C3 aggregate old-loss
increase is at most 10; in validation or confirmation the corresponding limit
is 16. This sentinel is evaluated natively before the stage gate and applies
even if C3 does not meet the full C2 win rule.

## Failure and claim rules

- A C2 win is a **composite benchmark result**, not a descendant identity,
  canonical mutation or promotion.
- Under the amendment route, the strongest permitted label is
  `NATIVE_SURROGATE_COMPOSITE_BEATS_SURROGATE_PARENT`; the words
  “beats canonical R27” are prohibited.
- Under the full N17 route, a qualifying result may be reported as a
  frozen-parent composite outperforming the qualified native R27 path, but it
  still does not authorize mutation or promotion without separate authority.
- A C2 result without C0/C1/C3 integrity is inconclusive.
- A digest-only N17 result, historical verifier receipt, or raw-file match may
  not be used to upgrade an inconclusive result.
- Every first invocation consumes its stage, including process failure,
  partial output, resource refusal or a failed native gate.

## Exact required controls before admission

The final candidate must include fixed native controls for:

- changed canonical-parent byte and postrun byte identity;
- changed R27 format, step, restarts and R26 linkage;
- N10 map-manifest or page tamper;
- C0/C1/C2/C3 condition selection and output-delta identity;
- sidecar update-count, route, support, tolerance and seed perturbations;
- holdout label/result injection attempts;
- old/new probe contamination of training or acceptance;
- parent state write attempts, canonical hash drift and run-local-copy escape;
- deterministic replay of each condition with identical inputs;
- randomized/untrained C3 non-equivalence to trained C2;
- resource overrun and explicit capacity refusal;
- literal expected-result substitution in place of native recomputation.

The sidecar interface contract and the complete pre-freeze manifest checklist
are required pre-admission controls. They must fail closed until the exact R27
feature mapping, encoding, residual composition, arm19 mapped-space semantics,
every input hash, seed collision check and expected negative outcome have been
independently pinned.

Each control must fail closed and must be frozen before any admission. No
control may be removed or weakened after exposure.

## Required native implementation boundary

New cognition, sidecar learning, parent-path evaluation, telemetry and
scientific gating must be native Zag. Python, pickle loading, historical
reducers/classes/globals, `torch.load`, historical verifier execution and
hidden foreign evaluators are forbidden. The existing N16 binary may be used
as an immutable mechanism reference only; a final N18 source/build must be
separately authored, reviewed, pinned and frozen.

Operational hashing, file inspection and receipt capture remain tooling only.
No operational parser may become the scientific selector or gate.

## Current disposition

N18 is a design candidate only. It creates no registry entry, no reservation,
no binary, no scientific population and no canonical-state change. Independent
review must examine this design, `VERIFY_CONTRACT.md`, `SOURCE_REFERENCE_INDEX.json`,
`SIDECAR_INTERFACE_CONTRACT.md`, `PREFREEZE_MANIFEST_REQUIREMENTS.md`, `AMENDMENT_REQUEST.md`, the governing contract, N17's current blocker and N16's
consumed closeout before any preregistration or implementation authority is
considered.
