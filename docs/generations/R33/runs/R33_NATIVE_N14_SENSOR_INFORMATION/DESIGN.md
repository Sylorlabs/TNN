# R33-N14 — bounded sensory information-preservation candidate

Status: **REVIEW V1 REQUESTED CHANGES; CORRECTED CANDIDATE PENDING REVIEW V2.**

Identity: `r33-native-n14-sensor-information-preservation-v1`.

N14 is a distinct nonlearning engineering candidate after the consumed N06 S0
sensor/trace/observer result. It does not rerun N06. The unchanged N06 sensor
implementation is copied byte-for-byte into this candidate and exercised only by a
new driver after independent exact-source review, preregistration, freeze and separate
admission.

## Question

Within the already-declared encoded-file envelope, does the observer preserve enough
information to reconstruct the exact admitted `TNNRAW01` packet from observer-visible
sample/pixel values plus all twelve physical metadata fields, after durable storage and
fresh-process reload?

An exact reconstruction is a bounded S1 information-preservation certificate for the
tested encoding: it detects hidden normalization, clipping, resampling, subsampling,
channel reordering, pixel reordering, sign loss and metadata loss. It is not natural
perception, learned representation quality, physical-device qualification or S2 transfer.

## Frozen candidate envelope

- PCM16LE: mono/stereo, 8,000..192,000 Hz, payload <=131,072 bytes.
- RGB8: interleaved three-channel, 1..64 by 1..64 pixels.
- Exact `TNNRAW01` 64-byte header and N06 durable sensor path.
- Clock `7`, timebase `1,000,000`, contiguous ordinal and nondecreasing tick.
- No semantic word/phoneme/object labels or evaluator IDs enter `sn_observe`.
- No learner, optimizer, training, canonical mutation, authority grant or promotion.

## Positive reconstruction battery

The new driver authors eight deterministic engineering packets and admits them through
the unchanged sensor path:

1. PCM mono 8 kHz minimum-rate maximum payload containing every one of the
   65,536 signed PCM16 codewords exactly once.
2. PCM stereo 192 kHz maximum-rate alternating extrema.
3. Empty PCM payload.
4. PCM order twin A with an impulse at an odd sample position.
5. PCM order twin B with the same sample multiset but impulse at a different position.
6. RGB 1x1 boundary frame.
7. RGB 64x64 frame with all byte values recurring across ordered channels/pixels.
8. RGB equal-histogram order twin of fixture 7 with a deterministic rotation.

For every packet, the driver obtains only `sn_observe` values and its twelve physical
metadata fields, re-encodes a packet from those outputs, recomputes the registered Adler
integrity words, and requires byte-for-byte equality with the original packet. It also
requires the order twins to remain unequal after reconstruction while retaining their
equal aggregate sums. The entire reconstruction battery repeats in a fresh process over
the durable records.

## Negative boundary battery

A separate new ledger must reject malformed candidates without changing committed state,
causal bytes, attempt quota, blob quota or event count:

- PCM rate 7,999 and 192,001.
- PCM channels 0 and 3.
- PCM odd payload length / item-count mismatch.
- PCM payload 131,074 bytes (boundary +2 wire bytes; over the 131,072-byte envelope).
- RGB width 0 and 65.
- RGB height 0 and 65.
- RGB channel count 2 and 4.
- RGB item-count/payload mismatch.
- Corrupted packet integrity word.

These are parser/admission controls, not scientific worlds.

## Acceptance boundaries

The candidate may eventually claim only bounded encoded-file S1 information preservation
if all reviewed children, counts, resource checks, exact reconstruction checks, fresh
reload checks, refusal no-mutation checks and terminal parent marker succeed once.

It may not claim physical microphone/camera fidelity, natural-scene/speech perception,
learned abstraction usefulness, S2 transfer, original R27 behavior recovery, full parent
migration, hostile-host isolation, learner authority, training readiness or R33 completion.
N06 and every other consumed primary remain consumed and must not be rerun.

## Review V1 corrections

Independent evidence-only review V1 found two preregistration blockers before any
execution. The supervisor incorrectly named superseded BUILD_01 and accepted any positive
child check count. The corrected source binds the prospective runtime path to BUILD_05
and statically requires exact successful-child check totals 79/70/33 for write/replay/
refusals. It also requires the exact number of `CHECK,` lines, exact total newline count,
a unique parseable `N14_CHILD_COUNTS,<expected>,0` record and `N14_CHILD_PASS` at the
end of capture. The invalid child remains required to be silent exit2. New corrected
BUILD_05/06 identities and independent review V2 are mandatory before registration.
