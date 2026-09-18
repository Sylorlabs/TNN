# R33-B000 — five native boundary defects confirmed

Executed once on 2026-09-05. Status: `EXPECTED_WITNESSES_MATCHED`, with no
observation mismatch. This is a **negative substrate result**, not sensory or
authority qualification. R27 remains canonical, step60,423, zero newborn restarts.

Evidence: [complete result](R33_B000_RUN_PRIMARY_V1/RESULT.json),
[native stdout](R33_B000_RUN_PRIMARY_V1/native.stdout),
[manifest](R33_B000_RUN_PRIMARY_V1/MANIFEST.json), and
[execution status](R33_B000_EXECUTION_STATUS.json).

| Witness | Native observation and control | Supported conclusion |
|---|---|---|
| W1 visual | Ascending and reversed eight-channel raw arrays produced identical signatures; changing the final channel to8 changed the signature | The tested transform loses channel order. This is not a claim that every vision route loses it. |
| W2 acoustic | Distances were0 for silence,0 for the index1 impulse,100 for the index2 impulse; raw arrays retained both impulses | The selected duration24/width12 window misses an unsampled detail. Other windows were not tested. |
| W3 trace | 8,193 attempts retained8,192 records and missed one; 8,191/8,192 controls were intact, stored-field mismatches0 and guards unchanged | Saturation silently drops an event in this prototype trace helper. |
| W4 protection | All-protected selected slot0; mixed protection selected1; unprotected selected0; empty returned−1 | The helper can select protected storage. No deletion was performed. |
| W5 reconstruction | Capacity2 yielded10/20 and untouched tail sentinel; capacity3 preserved10/20/30 for both segmentation and reconstruction; codebook unchanged | Output limits silently omit the tail under these conditions. |

The eight copied helper bodies, fixtures and expected observations were not
modified after preregistration. The rebuilt binary matched the earlier compile-
only binary exactly: SHA-256 `31c964cea11f59d4795ad5405985acd3d2954105405d14b90356fc8b9daa6470`.
Native stdout SHA-256: `fcedc24ec616194f670c7eb2189e36d8e9564496a21081595dc172e4793900dd`.
Result SHA-256: `35dbb169fecdd27ca30253cc6cc1fa57d5b227df709e146fc34369eb7725646a`.

## Resources and validation

Runtime exit0; stdout4,210 bytes; stderr0. Measured wall0.271660416s,
CPU0.010517s and peak RSS2,801,664 bytes. Wall includes sandbox/startup/capture,
not only helper operations. Compilation was measured separately: wall0.232055167s,
CPU0.221540s, peak RSS10,862,592 bytes. These are one-run engineering measurements,
not capability-per-compute claims. All registered measured ceilings held.

The [launch supplement](R33_B000_LAUNCH_CONTRACT.md) records the actual controls
and missing hard RSS/read-isolation guarantees. No live learner or shadow module
was admitted. Final checks passed71 external tests,18 unchanged original pins,
the inherited source pins and9 retained run artifacts. The external parser
reproduced the saved result. The historical authoring tests now use the recorded
pre-execution snapshot; current execution is checked separately by
`python3 -B Research/r33_execution_validate.py` and
`python3 -B -m unittest discover -s Research -p 'test_r33_execution.py'`.

## Evidence and architecture consequences

Fixture namespace `r33-b000-literal-boundary-v1` now has one consumed primary
exposure. Any reproduction must be separately recorded and cannot become fresh
generalization evidence. No old E51 stages, training, accepted checkpoint,
R32 cognitive source or canonical state was changed. B000 is not AJ's entrypoint.

The justified next implementation is a separate native component with exact
raw transport, explicit capacity failures, protected-slot refusal and admission
of a trace record before an in-memory update. Its boundary tests must include
malformed input, signed values, aliasing, overflow, stale versions and negative
controls. Copying an array alone cannot qualify natural sensory ingress;
in-memory update ordering cannot qualify durable crash recovery or M0–M7.
Those remain explicit gates of B001 and the full R33 master plan.
