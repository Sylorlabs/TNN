# R33-N06 — bounded raw sensor/trace/observer integration passed

The sole frozen BUILD01 primary exited0 and reaped all16 registered children.
All727 completed-child checks and163 parent checks matched. Native comparison
counters exactly met the preregistered377,264 sample/pixel values and636 physical
metadata fields. One deliberate raw-before-trace exit73 was expected. These
counts describe known engineering fixtures, not independent natural examples.

Evidence: [native result](R33_NATIVE_N06_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[parent log](R33_NATIVE_N06_RUN_PRIMARY_V1/supervisor.stdout),
[normal fresh replay](R33_NATIVE_N06_RUN_PRIMARY_V1/normal-replay.stdout),
[raw-only crash recovery](R33_NATIVE_N06_RUN_PRIMARY_V1/crash-replay.stdout),
and [protocol](R33_NATIVE_N06_SENSOR_TRACE/PREREGISTRATION.md).
The native result records161 parent checks before result-save/close; both final
checks and the terminal pass marker also succeeded, giving163 parent checks.

## Observed fidelity and failure behavior

Every signed PCM16 codeword, every maximum64x64 RGB8 pixel channel, the odd-index
impulse distinction, equal-histogram reordered pixels, empty PCM, stereo extrema,
rate endpoints and repeated raw payload traversed durable byte storage, fresh
recovery and the generic observer API. All12 physical metadata fields per packet
and complete raw bytes matched. Extra output capacity remained untouched.
The observer receives no scenario ID, expected answer or semantic boundaries.

Wrong clock/timebase/order, backwards tick, malformed/rate-invalid/checksum-bad
packets, short output and aliases were rejected without changing the admitted
state or quotas. Sixteen-event saturation refused the17th before a new blob.
All32 incomplete raw reservations remained charged with zero committed events;
reservation33 refused. Recovery after exit73 retained a complete raw orphan,
exposed no observation from it, and continued using blob2 without overwriting
blob1. Corrupted, truncated and missing-middle raw evidence rejected respectively
with-8203,-8201,-8204, empty state/causal buffers and closed handles.

Local payload repeat tracking counted the duplicate sample bytes as a replay
despite a changed timestamp; it is not a global scientific freshness audit.
Only the evidence slot is populated with an exact blob/digest reference. Other
causal roles and understanding remain unmeasured rather than invented.

## Source, resource and qualification boundaries

All27 source/config/compiler/build pins verified before admission at
2026-09-06T02:15:03Z. Two independent builds were byte-identical:
`b375cf44faebc300821c70151e0e346c39743c0bba2c6c67a48bb9709f8f44da`.
Native result SHA256:
`29259317825b887ae1f8d8dddcf6ee7184c3d4bbc32d8efe98c616789a7a487d`.
Parent stdout SHA256:
`956cf70fd68b52603517c2221865141310674712073a03d5dda2bc74b852083e`.

Summed child CPU2,344,465us; summed observed nonmonotonic wall2,508,929us;
peak child RSS12,976,128bytes. Host2.74s/maxRSS12,976,128bytes. No surviving n06
process matched the post-run scoped process check. RSS is observed, not a hard
containment guarantee. No historical primary, Python or learner executed.

This advances only the bounded encoded-file S0/observer-access engineering lane:
PCM16LE mono/stereo8000..192000Hz, at most131072 payload bytes, and RGB8 frames
up to64x64,16 committed events/32 raw reservations/32 telemetry attempts. It
does not qualify physical devices, natural perception S2, a continuing learner,
full causal schema, power-cut safety, hostile isolation, signed authority or
full parent migration. The C02/N05B imports and all older evidence are unchanged.

## Next dependency and architecture diff

New components add a separately charged raw-blob reservation namespace, full
packet/sample hashes bound into telemetry, fail-closed full-evidence recovery,
and exact observer delivery. No learned representation, optimizer, teacher or
accepted parent was changed. Parent source/semantic-digest closure and protected
runtime authority must precede training and later scientific milestones.

R27 remains canonical60423/restarts0. Sixteen diagnostic batches including
preserved failures, zero R33 learner training or promotion. The full eighteen-
stage R33 program remains incomplete; this is not a completion certificate.
