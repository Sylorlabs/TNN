# R33-N06 — bounded sensor-to-durable-trace-to-observer integration

Identity: r33-native-n06-raw-sensor-trace-observer-v1. One primary,16 supervised
child modes. Native Zag only, engineering fixtures only; no learner, training,
canonical mutation, new authority, or physical device acquisition.

## Hypothesis and changed-variable / hardcoding ledger

Exact byte-originated PCM16LE and RGB8 packets can be bound to a durable native
event, recovered in a fresh process and exposed as every original signed sample
or pixel channel, with exact physical metadata and fail-closed evidence links.
This integrates the known C02 packet boundary and N05B durable accumulator with
a new full-raw observer. Known extrema, equal-histogram and unsampled-position
counterexample shapes are declared reused engineering controls, not fresh
learning evidence or repeated old primaries. No old generator runs.

Allowed changes: raw-blob reservations, digest binding, bounded sensor admission,
complete-payload recovery and observer API, plus native fixtures/supervision.
Forbidden: changing frozen imports, N05A negatives, sensory filtering/normalizing/
resampling, semantic segment boundaries, teacher/optimizer/learner state, grants
or canonical identity. Fixture patterns and expected values are evaluator-only.
The observer API has no expected answer or scenario identifier argument.

## Encoding, lifetime and authority boundaries

Use C02's exact 64-byte TNNRAW01 header: PCM16LE mono/stereo at8000..192000Hz,
payload0..131072bytes, or interleaved RGB8 frames1..64 by1..64. Clock is the
declared stream clock; this version admits timebase1,000,000 only, contiguous
ordinals and nondecreasing ticks. All12 metadata fields survive exactly.
Sample/frame boundaries are physical encoding, never word/phoneme boundaries.

Each raw blob is an exclusive immutable blob-N.bin reservation, synced before
trace commit. Blob capacity32 is separate from journal capacity16 and retained
attempt capacity32. Failed/unpublished blobs remain visible and consume their
own quota; fresh recovery does not expose them as observations. A new append
after an orphan uses the next blob ordinal, never overwrites the orphan.
The evidence causal slot holds an explicit36-byte reference: blob ordinal and
whole-packet SHA256. Its own digest binds that reference. TE_PAYLOAD hashes only
raw sample bytes; identical sample payloads are counted as local repeats, not
fresh science just because timestamps differ. Other five causal slots remain
missing. No generated explanation or learner-reasoning claim is introduced.

Recovery checks the frozen root/event chain and all referenced raw packets,
metadata, full-packet and sample-payload digests before returning usable state.
The generic observer stages complete outputs, refuses undersized/aliased buffers
without mutation and preserves excess output capacity. All signed PCM codewords
and every maximum-frame RGB channel are checked in the full integrated path.

## Sole primary schedule and exact falsifiers

1. Invalid mode exits2 silently.
2–3. Normal writer and fresh replay: ten packet fixtures comprising all65,536
PCM codewords in one maximum mono packet; a64x64RGB frame;24-sample zero/odd-index
impulse twins; two equal-histogram reordered RGB frames; empty PCM; stereo
alternating extrema at192kHz; an exact-payload repeat with a new ordinal; and
an8000Hz case. Compare every observer value and all12 metadata fields to the
literal source formula, verify raw bytes, retained tails and local replay count.
4. Invalid packet/checksum/rate, wrong clock/timebase, duplicate/gapped ordinal,
backward tick, short output, alias and out-of-range observation controls must
refuse without telemetry, blob quota, input or output mutation.
5–6. Sixteen committed packets and fresh reload; seventeenth refuses-8205 with
no extra blob or event.
7–8. Thirty-two native injected partial raw writes and fresh reload; all32
orphan reservations remain, zero events, thirty-third refuses-8205.
9–10. Exit73 after full raw sync but before telemetry reservation, then fresh
recovery: one orphan, zero events; continued append uses blob2 and retains blob1.
11–16. Three new corruption setups and fresh rejections: payload corruption
(-8203), truncated referenced blob(-8201), missing middle blob(-8204). Preserve
each original under a separate preimage or retained filename before mutation.
Rejections expose no accumulator/causal buffers or open descriptors.

Any unexpected assertion, missing terminal marker, wrong exit/signal, incomplete
capture, unaccounted loss, or resource violation fails the primary and stops
subsequent modes. Preserve every outcome and freeze all sources/oracles before
exposure. Exact observed comparison/check counts come from native counters.
Prospective comparison totals are377,264 observer values and636 metadata fields:
two ten-packet traversals, two sixteen-packet traversals, and one maximum-PCM
traversal after raw-only crash recovery. The parent requires both totals exactly;
these are planned counts until the native primary actually reports them.

## Resources, artifacts, qualification limits and next dependency

Parent60s/1MiB per-file/core0/fd64; ordinary child15s/262144bytes per-file;
observed child RSS <=256MiB. Hard RSS/hostile process isolation is not established.
The tested compiler uses eight-byte integer storage; signed wire words are four
bytes. All new execution/evaluation/supervision is Zag; shell only handles
inspection, compiler invocation, copying and artifact checksums.

Freeze source/config/protocol/reservation/review, all imports, compiler and two
builds before one native admission. Preserve raw files, preimages, process logs,
native counters/results, resources, analysis/architecture delta, checksums,
consumed registry, current state, journal and handoff. Main engineering review
does not replace an independent scientific or protected-authority verdict.

Pass can establish only this bounded encoded-file S0/observer-access engineering
lane. It does not establish physical microphone/camera acquisition, natural
perception S2, an integrated learner, complete causal telemetry, parent migration,
global freshness, power-cut guarantees, signatures, grants or R33 completion.
Parent source/semantic closure and runtime authority remain dependent gates.
