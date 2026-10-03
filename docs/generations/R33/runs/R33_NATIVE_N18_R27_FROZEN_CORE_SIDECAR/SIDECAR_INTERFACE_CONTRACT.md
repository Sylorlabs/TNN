# N18 sidecar interface contract — design boundary

This file is a design boundary, not an implementation. The exact mapping from
R27 native behavior into this sidecar ABI is unresolved while N17 continuity is
unresolved.

## Required interface

For each training example, a final native implementation must bind one exact
`N18-SIDECAR-ABI-1` record:

- `parent_feature`: exactly 16 signed little-endian `i32` coordinates;
- `parent_output`: one checked `i64` score;
- `training_target`: exactly `-1` or `+1`, present only for training-side
  records;
- `stream_role`: exactly `OLD_SUPPORT` or `NEW_TRAINING`, present only for
  training-side records;
- `population_seed` and `example_index`: checked `i32` provenance fields,
  never a routing or evaluator shortcut.

The 16-coordinate values must be produced by a fixed, nonlearning adapter from
the qualified parent representation. The adapter's source feature, ordering,
numeric scale, clipping and missing-value policy are still a deferred
prerequisite; N18 may not invent them from the synthetic N16 fixture.

For each evaluation example, the sidecar receives only the parent feature and
the parent output. It receives no target, stream role, seed, example index,
probe membership, evaluator bit or holdout outcome.

The sidecar state has exactly sixteen checked `i32` residual weights and one
checked `i32` residual bias. It returns one checked `i64` residual score,
`dot(weights,parent_feature)+bias`. Final binary choice is `+1` when
`parent_output + residual >= 0`, otherwise `-1`; checked overflow refuses the
record. C0 and C1 must use the same parent/output adapter and resource
schedule. C2 and C3 must use the same sidecar shape, including the bias term,
update budget, allocation schedule and telemetry schema. Non-binary or
multi-output parent behavior is a hard unsupported-interface refusal until a
separately reviewed ABI exists.

The canonical wire form has no implicit padding. A training record is exactly
88 bytes: version `u8=1`, role `u8` (`1=OLD_SUPPORT`, `2=NEW_TRAINING`), flags
`u16=0`, sixteen little-endian signed `i32` features, little-endian signed
`i64` parent output, little-endian signed `i32` target, little-endian signed
`i32` population seed and little-endian signed `i32` example index. An
evaluation record is exactly 76 bytes: version, role `u8=0`, flags, sixteen
features and parent output; target, seed and index are absent. A residual
response is version `u8=1`, status `u8`, signed little-endian `i64`
residual and signed `i8` final choice with no padding. Status values are fixed:
`0=OK`, `1=SKIPPED_NO_UPDATE`, `2=REFUSED_MALFORMED`, `3=REFUSED_RANGE`,
`4=REFUSED_OVERFLOW`, `5=REFUSED_UNSUPPORTED`. Only status0 may carry choice
`-1` or `+1`; every refusal or skip carries residual0 and choice0. Any wrong
length, version, role, flags, range, missing field or trailing byte refuses the
record and emits status2.

## N16 arm19 mapping that must be resolved

The consumed N16 implementation operates on a synthetic 16-coordinate integer
feature vector, a binary parent score and binary targets. N18 may use the
following source-level arm19 schedule only after the R27 adapter is pinned; it
may not silently pretend that N16's synthetic input is R27 behavior:

- 12 old-parent epochs;
- 6 new-training epochs;
- 256 old-training records, 256 old-support records and 256 new-training
  records per population;
- 512 evaluator probes per old/new probe set;
- additive zero-initialized residual state;
- 75% training-mean projection gate;
- dual old-support preservation with tolerance 1;
- update divisor 40 and source-order proposal/accept/reject behavior.

Before implementation, a new review must pin:

- the exact native R27 feature source and dimension;
- the deterministic mapping to any sidecar coordinate space;
- numeric scale, clipping and quantization rules;
- parent-output and target encoding;
- old-support/new-training stream construction;
- residual composition and output tie-breaking;
- update and preservation state layout, including sixteen i32 weights and one
  i32 bias;
- how the arm19 75% projection and dual512 tolerance1 rule operate in the
  mapped space; and
- whether the mapping itself is a fixed nonlearning adapter or introduces a
  separately qualified learner.

The exact condition dataflow is:

| Field | C0/C1/C2/C3 training | C0/C1/C2/C3 evaluation |
|---|---|---|
| parent_feature | allowed | allowed |
| parent_output | allowed | allowed |
| training_target | allowed only for predeclared old-support/new-training records | forbidden |
| stream_role | allowed only as the fixed predeclared training role | forbidden |
| population_seed/example_index | provenance only | absent from sidecar |
| probe truth | forbidden | forbidden |
| probe membership | forbidden | forbidden |
| evaluator/holdout outcome | forbidden | forbidden |
| another condition's state/output | forbidden | forbidden |

Training-side targets are therefore permitted only for the fixed old-support and
new-training streams. “Target truth” in the no-leakage rule means evaluator,
probe or holdout truth; it does not prohibit the declared training labels that
arm19 requires. Any record violating this table must be rejected before it can
affect state or telemetry.

## C3 randomized/untrained control

C3 uses the same ABI, feature mapping, projection metadata, allocations and
resource budget as C2, but its residual state is generated before any
population data from a fixed independent seed namespace. Its exact design-time
manifest fixes sixteen weights of +/-25, one bias of +/-16, total parameter L1
norm416, the checked hash/sign rule, nonzero guarantee, tie-breaking and zero
accepted updates. These magnitudes match the source-level one-update coordinate
and bias bounds without using any observed C2 result. C3's randomization
manifest must be complete before admission and may not depend on any observed
C2 result.

Until that manifest and the R27 adapter mapping are pinned, this interface
remains a `DEFERRED_BLOCKER` and no N18 binary may be authored.

Until those items are pinned and independently reviewed, the interface is a
`DEFERRED_BLOCKER`. No N18 source or binary may be authored as if the existing
N16 binary were a drop-in R27 adapter.

## Leakage and authority boundary

The interface must reject any call that includes holdout labels, probe
membership, evaluator results or another condition's state. The sidecar has no
authority to write canonical R27, change parent metadata, publish promotion or
grant learner authority. All mutable sidecar state is run-local and must be
included in the exact final evidence record.
