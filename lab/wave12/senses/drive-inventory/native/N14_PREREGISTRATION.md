# R33-N14 sensory information-preservation qualification

Identity: `r33-native-n14-sensor-information-preservation-v1`.
Preregistered 2026-09-07 after independent exact-evidence source review V2.
Owner: main agent, sole registry writer and launcher. Exactly one primary attempt,
including failure. This document is not a source freeze or launch admission.

## Question and bounded claim

Within the already-qualified encoded-file transport envelope, can the unchanged N06
observer preserve enough information that its visible values plus all twelve physical
metadata fields reconstruct the exact admitted `TNNRAW01` packet after durable storage
and fresh-process reload?

Success may establish only bounded encoded-file S1 information preservation for the
declared PCM16LE/RGB8 formats. It does not establish physical-device fidelity, natural
speech/vision understanding, S2 learned transfer, learner competence, original R27
behavior, full parent migration, protected authority, training readiness, promotion or
R33 completion.

## Reviewed identity

Independent review V1 returned `REQUEST_CHANGES` before any exposure. Its two blockers
were corrected: the supervisor now binds the selected BUILD_05 binary, and successful
children require exact output/check structure rather than a positive check count.

Independent review V2 returned `APPROVE_FOR_PREREGISTRATION — NO EXECUTION
AUTHORIZATION`. Saved report SHA256:
`97b5b69eb27fe5dd9dd1a4edbc79ddabb8d1651e3206802db68ebe3a8a66c607`.
The review is explicitly evidence-only: the reviewer evaluated the supplied exact source
and build bundle without claiming direct filesystem access, compilation or execution.

The 41-entry V2 input manifest verified before review and SHA256s to
`8e27db17f14c4145e1aff7a2302f17adfffe6cdad004b0a8e64e08344b231274`.
Current reviewed root driver SHA256 is
`ff3d80c67e6fbbaf7024bc45652421ce3f359ce8e2b17ba4660d2a2f7fd661e2`.
The copied N06 sensor source SHA256 is
`7d893af1984ee05ba128c496a8b0fda943fdd44f18fc377a023e847b5a194996`.

Select `BUILD_05/n14`; `BUILD_06/n14` is its byte-identical compile-only comparison.
Both are 429,440 bytes, SHA256
`44a8911a56c159204d5be04dcacda1b657968cceba4e1be99dafd96c64d83653`.
Compiler `Research/toolchain/znc_macos_arm64_7cacbfc0` SHA256 is
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`,
with `--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.
Compilation is not experiment evidence.

## Finite positive battery

Eight deterministic engineering packets are written once, then re-opened by a fresh
process and checked again:

1. mono 8 kHz PCM16 maximum payload containing every signed 16-bit codeword once;
2. stereo 192 kHz alternating signed extrema;
3. empty PCM;
4. PCM impulse-order twin A;
5. same-multiset PCM impulse-order twin B;
6. RGB8 1x1 boundary frame;
7. RGB8 64x64 ordered frame with every byte value recurring;
8. equal-histogram cyclic order twin of fixture 7.

For each packet, the child must obtain values and twelve metadata fields through
`sn_observe`, compare every value and metadata field to its deterministic source,
re-encode and reseal an exact packet, compare it to both the original fixture and the
durably loaded raw bytes, and leave a sentinel output slot untouched. The PCM/RGB order
twins must remain byte-distinct while retaining equal aggregate sums.

The successful logical observer schedule covers 90,171 values and 96 metadata fields per
write/replay process, 180,342 values and 192 metadata fields across both successful
processes. Those arithmetic totals are design provenance; acceptance is the exact native
check protocol rather than a post-hoc aggregate threshold.

## Negative battery

Fourteen malformed packets exercise PCM low/high rate, invalid PCM channels, odd/mismatched
PCM length, above-envelope payload, RGB low/high width, RGB low/high height, invalid RGB
channels, RGB item mismatch and checksum corruption. Every refusal snapshots complete
telemetry state, causal bytes, head, attempts, blob count and event count and requires no
change after refusal. No malformed fixture may create a committed event or blob.

## Exact child and parent acceptance

After separate freeze and admission, invoke selected BUILD_05 with `supervise` exactly
once. Four direct children run in order:

| mode | expected exit | expected successful checks |
| --- | ---: | ---: |
| invalid | 2 | 0 |
| roundtrip-write | 0 | 79 |
| roundtrip-replay | 0 | 70 |
| refusals | 0 | 33 |

Successful-child total is exactly 182 checks. The parent requires eight process/capture
checks for every child; invalid adds one silent-output check, while each successful child
adds four exact-log checks. Parent count is therefore 46 before native result publication,
47 after result write and 48 after root close. Any mismatch fails the primary.

Successful child capture must end in `N14_CHILD_PASS`, contain one parseable zero-failure
`N14_CHILD_COUNTS` record with the exact frozen count, contain exactly that many line-start
`CHECK,` records, and contain exactly expected+2 newline-delimited output records. The
invalid child must be silent. Every child must start/reap normally, have the expected exit,
zero signal/native stderr, complete capture and positive observed RSS no greater than
268,435,456 bytes.

Parent exit0 plus final marker
`R33_N14_SENSOR_INFORMATION_PRESERVATION_ENGINEERING_PASS` are mandatory. JSON alone
does not constitute acceptance.

## Resources, effects and failure policy

Parent guard is 90 seconds. Each work child has a 20-second deadline, capture is capped at
262,144 bytes, file descriptor/core limits are inherited from the native process guard, and
observed per-child RSS ceiling is 268,435,456 bytes. This is observed resource acceptance,
not hostile-host or hard memory isolation.

Exclusive native output root is `Research/R33_NATIVE_N14_RUN_PRIMARY_V1`. Outer command
capture is `Research/R33_NATIVE_N14_LAUNCH_PRIMARY_V1`. No other experiment directory may
be mutated. The run writes only new N14 durable fixture data, child captures and
`NATIVE_RESULT.json`; it does not mutate R27 or any consumed experiment evidence.

The first actual primary invocation consumes N14 regardless of outcome. On any failure,
retain all partial evidence, stop where the native supervisor stops, and do not retry,
retune expectations, change source, raise resource limits or rerun an older primary.

This is known deterministic engineering evidence, not a fresh scientific population.
Training=false, canonical mutation=false, learner authority=false, promotion=false.
