# FREEZE: C1 Smallest-Consistent-K Revision (FROZEN)

Date: 2026-09-30. Worker: C1 Smallest-Consistent-K Revision Worker.
Status: FREEZE-FROZEN. Committed alone after the prereg (22e2554b8), before any runs.

## The variant

`contestant_smallk.zag` (1132 lines) is the frozen C1-CLEAN contestant
(b8d38d9c8:docs/lab/research-lead/overnight-20260928/c1_clean/contestant.zag)
with exactly one line changed (line 807):

BEFORE: `if(streq(rs,dout)==1){found=k;}`
AFTER:  `if(streq(rs,dout)==1 && found<0){found=k;}`

This changes the rotation class per-demo key selection from largest-match-k
to smallest-consistent-k. Verified by `diff`: exactly one line differs.
No other source line changed.

## Build

Compiled with the pinned toolchain
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` (sha256 prefix 498abcb5):
`znc build contestant_smallk.zag -o contestant_smallk_bin`
Build exit 0 (6 analyzer warnings, same as the original; non-strict mode).
Binary: `contestant_smallk_bin` (145K).

## Hashes

See `hashes.txt` in this directory:
- contestant_smallk.zag: 659a082a15d1366e96a846320d9968f80608eed220aebf6db2f89b94e9d9ed57
- contestant_smallk_bin: 84524109798bb8ae58b54b14563d7e7e9ccc7575f6b1e19de245d6d0533e3b2a

## Reuse

The F-E family sealed worlds from 6e03b2fa5 are reused byte-identical
(sha256 verified before running; not regenerated). The diag and agg
instruments are reused byte-identical from the F-E freeze (0d8bdc111).
Only the contestant binary is swapped.

## Ordering

Prereg 22e2554b8 < this freeze < results (to come).
Verifiable via `git merge-base --is-ancestor`.
