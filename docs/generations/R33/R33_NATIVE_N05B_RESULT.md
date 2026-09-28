# R33-N05B — bounded durable telemetry corrective regression passed

The sole frozen BUILD02 primary exited0. All41 scheduled children were reaped;
749 checks from successfully completed children and406 parent checks matched.
Five deliberate exit73 deaths and one parent-enforced SIGKILL were expected.
The native result reports404 parent checks before its result-write/close checks;
the terminal zero-failure marker also passed. This is one corrective engineering
batch, not41 experiments, new science, or learner training.

Evidence: [native result](R33_NATIVE_N05B_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[parent log](R33_NATIVE_N05B_RUN_PRIMARY_V1/supervisor.stdout),
[ABI guard](R33_NATIVE_N05B_RUN_PRIMARY_V1/abi.stdout), and
[protocol](R33_NATIVE_N05B_DURABLE_TELEMETRY/PREREGISTRATION.md).

## Actual results and architecture delta

The runtime guard measured eight-byte integer stride and intact adjacent
allocations/configuration. The corrected native allocator and alias extents
remove the four-byte native-storage assumption; four-byte signed wire encoding
remains unchanged. Out-of-range encoding was refused without output mutation,
and minimum/maximum signed values roundtripped exactly. A far-tail alias was
rejected. N05A's source, failure, and13 retained files remain frozen and verified.

Fresh processes reconstructed all168 metric words, the entire accumulator, and
every causal byte. All54 deliberately missing causal slots stayed missing.
Understanding, teacher competence, transfer and calibration stayed unmeasured.
Normal append, duplicate/stale input refusal, capacity exhaustion, all32 failed
reservations, five commit-boundary deaths, real SIGKILL, explicit prepublication
failure and indeterminate postpublication acknowledgment behaved as registered.
All eight corruption cases rejected with the registered error and no usable
recovered state. Continued append after recovery retained spent reservations.

Build01's pre-exposure type-check failure remains preserved. Builds02/03 are
byte-identical, SHA256
`a363689b653960ced6f9fb6028b89c5a0bfcdea4f7c191ee94dd81d1fbc6fd49`.
All24 freeze pins verified before sole admission. Native result SHA256
`c62c55c4692ebd58341fdc60cd629e45e99f4405bb82de9b54282aec4592103c`;
parent stdout SHA256
`135b0d837863442bd6430d85f641abe7ee4ef67d4c81d24f49b5c87e489e0f5a`.

## Actual process resources and limits

Summed child CPU1,168,828us; summed observed nonmonotonic child wall1,350,587us;
peak child RSS4,079,616bytes. Host time displayed1.65s and maximumRSS12,320,768bytes.
No surviving n05b process matched the post-run process check. Fixture resource
fields are separate, and RSS remains observation rather than hard containment.

Qualified only: trusted single-writer native process-death telemetry engineering,
bounded to16 events,32 attempts and six64-byte causal payload slots. Not qualified:
hardware power-cut durability, hostile modification protection, authentication,
complete learner state/schema, physical sensors, native parent migration or
causal understanding. Integrity digests are not signatures or human grants.

## Next dependency

Continue sensory byte-to-observer fidelity and durable raw-evidence linkage,
parent semantic/source closure and protected-runtime authority. No training gate
is opened by this component pass. R27 stays60423/restarts0;15 diagnostic batches
including preserved failures, zero R33 training, no canonical change or promotion.
The eighteen-stage R33 program remains incomplete.
