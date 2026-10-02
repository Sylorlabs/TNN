# R33-N14 authoring and build history

No N14 fixture, child mode, supervisor mode or primary has executed.

## BUILD_01 / BUILD_02 — superseded pre-review compile-only history

The initial candidate compiled successfully twice with empty compiler stderr and
byte-identical binaries. Both binaries SHA256 to
`c42dc8c29276a6930b53220ff397ca1c6d01e3c5bbf776f38d9dfbc895e79ee7`.

Before independent review or any exposure, the positive PCM minimum-rate fixture was
strengthened from a small mixed-sign sample to the maximum 131,072-byte mono payload
containing every signed PCM16 codeword exactly once. BUILD_01/02 remain retained as
superseded compile-only history and are not launch candidates.

## BUILD_03 / BUILD_04 — current exact candidate

The strengthened source compiled successfully twice with empty compiler stderr.
BUILD_03 and BUILD_04 are byte-identical, 429,440 bytes each, SHA256
`cf30ee893956f82690cc08c22b3fcf0032f96423d1414f2dc0cddace903a4a20`.

Current root driver SHA256:
`09d0d32ace31197ff5e2d9d70c792ff19e7be5a56665e523f14bb8ef7e8fdb8f`.

The candidate `sensor.zag` is byte-identical to the consumed N06 sensor source,
SHA256 `7d893af1984ee05ba128c496a8b0fda943fdd44f18fc377a023e847b5a194996`.
The BUILD_03/04 dependency copies are byte-identical to each other. Compiler is the
unchanged `znc_macos_arm64_7cacbfc0`, SHA256
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`, with
`--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.

BUILD_03 is the prospective selected binary only if exact-source independent review,
preregistration, unique reservation, complete freeze and separate admission all succeed.
Compilation alone is not exposure, qualification or launch authorization.

## Independent review V1 — REQUEST_CHANGES before any exposure

The first independent evidence-only source review found two blockers: `n14_run`
referenced superseded BUILD_01, and the supervisor accepted any positive child check
count. The report is retained as `INDEPENDENT_REVIEW_V1.md`. No N14 mode had executed.

The correction binds all supervised children to BUILD_05 and requires exact check totals:
79 for `roundtrip-write`, 70 for `roundtrip-replay`, and 33 for `refusals`. It also
requires the exact number of `CHECK,` lines, exact output newline count, unique parseable
zero-failure count record, and final `N14_CHILD_PASS` suffix. Static parent accounting is
46 checks before result write and 48 after result-write/root-close checks.

## BUILD_05 / BUILD_06 — corrected review-V2 candidate

Both corrected builds compiled successfully with empty compiler stderr, are byte-identical,
429,440 bytes each, and SHA256 to
`44a8911a56c159204d5be04dcacda1b657968cceba4e1be99dafd96c64d83653`.
Current root driver SHA256 is
`ff3d80c67e6fbbaf7024bc45652421ce3f359ce8e2b17ba4660d2a2f7fd661e2`.
BUILD_05 is the only prospective selected binary for review V2 and any later freeze;
BUILD_06 is compile-only identity confirmation. Neither has executed.
