# R33-N14 encoded-sensor information-preservation result

Status: **NATIVE BOUNDED ENCODED-FILE S1 INFORMATION-PRESERVATION ENGINEERING PASS;
INDEPENDENT POSTRUN REVIEW PENDING.**

Identity: `r33-native-n14-sensor-information-preservation-v1`. Exactly one admitted
primary executed. This is deterministic nonlearning engineering evidence, not fresh
science, physical sensing, S2 learned perception, training, original behavior recovery,
full parent migration, protected authority, promotion or R33 completion.

## Native settlement

Selected reviewed/frozen BUILD_05 SHA256
`44a8911a56c159204d5be04dcacda1b657968cceba4e1be99dafd96c64d83653`
ran `supervise` once. The native command settled exit0 with terminal marker
`R33_N14_SENSOR_INFORMATION_PRESERVATION_ENGINEERING_PASS`.

All four direct children started and reaped with expected exits and zero native stderr:

| Child | Expected/observed exit | Accepted checks | Peak RSS bytes |
| --- | ---: | ---: | ---: |
| invalid | 2 / 2 | 0 | 1,409,024 |
| roundtrip-write | 0 / 0 | 79 | 8,962,048 |
| roundtrip-replay | 0 / 0 | 70 | 9,142,272 |
| refusals | 0 / 0 | 33 | 6,291,456 |

Successful-child total is exactly182 checks. The parent emitted48 CHECK rows with zero
failures;46 preceded native result publication, result-save was47 and root-close48.
Peak child RSS9,142,272 bytes leaves259,293,184 bytes below the frozen268,435,456-byte
observed ceiling.

## Exact information-preservation evidence

Both `roundtrip-write` and the separately launched fresh-process `roundtrip-replay`
completed all eight admitted packets. Each process contains exactly eight successful
`all_values_exact`, eight `metadata_exact`, eight `reconstructed_packet_exact`, and eight
`reconstruction_matches_durable_raw` checks. Thus every packet reconstructed from
observer-visible values plus the twelve physical metadata fields matched both its source
fixture and its durably reloaded raw bytes.

The persisted raw payload set contains exactly eight blobs with packet sizes:
131,136;80;64;112;112;67;12,352;12,352 bytes. The first packet is the maximum-envelope
mono PCM16 fixture whose source loop covers all65,536 signed codewords. The two PCM order
twins remain byte-distinct while both sum to1. The two 64x64 RGB order twins remain
byte-distinct while both sum to1,566,720. These are order/information controls, not claims
of semantic perception.

Fresh replay did not write new events: the durable `roundtrip` directory contains exactly
eight blobs, eight attempt records and eight event records after both children, supporting
the intended write-once/fresh-read schedule.

## Refusal evidence

The refusal child contains exactly14 successful malformed-packet refusals and14 exact
`refusal_no_state_effect` checks. It ends with event count0, blob count0 and attempts0;
the refusal directory contains no committed event or blob files. The cases cover PCM
rate/channel/length/envelope boundaries, RGB width/height/channel/item boundaries and
checksum corruption.

## Launch-wrapper operational defect

The native result itself passed. The outer wrapper attempted to record timestamps with
`/usr/bin/date`, but this host exposes `date` at `/bin/date`; therefore the intended
`start.utc` and `end.utc` files are retained as zero-byte evidence of that wrapper defect.
The binary was **not rerun**. Filesystem mtimes place those files at approximately
2026-09-07T00:59:27Z and 00:59:28Z, while `/usr/bin/time -lp` reports0.74seconds real
time. These mtimes are operational filesystem evidence, not substitutes for the failed
timestamp command output.

## Boundaries

This pass shows that, for the admitted deterministic PCM16LE/RGB8 encoded-file envelope,
the N06 observer path retained enough ordered values and physical metadata for exact packet
reconstruction after durable reload. It does not establish microphone/camera transport,
physical timing fidelity, natural-scene or speech understanding, S2 learning/generalization,
complete learner telemetry/state serialization, original R27 behavioral continuity,
protected human authority, training readiness or promotion.

R27 remains canonical at step60,423 with zero newborn restarts. No R33 training run or
canonical mutation occurred. N14 is consumed and must not be rerun. Independent postrun
review and immutable artifact/history closeout remain pending.
