# PREREG H-UNIFIED8: Significant-Digit Magnitude Validation in parse_ints (addresses X-U7-3)

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified7_learn.zag` (H-UNIFIED7, R8; SURVIVES 22/22, red team SURVIVES with one documented boundary X-U7-3), copied verbatim then repaired. New file `unified8_learn.zag`; `unified7_learn.zag` untouched.
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED7 SURVIVES 22/22. Independent red team (`u7_adversary/U7_ADV_RESULT.md`, prereg `3ffd96b9f`, result content committed in `19020185e`): X-U7-1, X-U7-2, X-U7-4 FAIL (defenses hold). X-U7-3 SUCCEEDS on the preregistered BOUNDARY branch: loud conservative false positive, not a kill, not a downgrade.

The boundary (frozen in U7_ADV_RESULT.md): the R8 11+ digit rule is length-based, not value-based. `"00000000001"` (11 digits, value 1) and `"00000000000000000001"` (20 digits, value 1) return -2 with PARSE_MAG. The trace message "digit run exceeds i32 range" is factually false for these inputs, and the PREREG_UNIFIED7 justification ("A run of 11 or more digits always has value >= 10^10 > 2147483647, so it is rejected unconditionally") is false for zero-padded runs. The rejection is loud (trace plus -2 code plus handler USHAPE skip), so the X-U6-2 hazard class (a caller acting on silently wrapped values with no signal) is not recreated. REPAIRED HERE (R9).

## The repair (frozen): R9 significant-digit counting

The parser judges a digit run by its SIGNIFICANT digits: leading zeros do not count toward the run length used for magnitude validation. Detection remains exact with no wider type:

- 11 or more significant digits always have value >= 10^10 > 2147483647, so the run is rejected unconditionally. This statement is now genuinely true (11 significant digits imply value >= 10^10).
- Exactly 10 significant digits: the run is valid iff its value <= 2147483647, checked before folding the 10th significant digit exactly as in R8. The 9-significant-digit prefix v9 satisfies v9 <= 999999999 (fits i32 exactly), so the test `v9 > 214748364 || (v9 == 214748364 && digit > 7)` is exact.
- 9 or fewer significant digits always fit i32. An all-zero run has value 0.

Implementation (frozen): inside the digit-accumulation loop, a digit is significant iff it is nonzero or a significant digit was already seen. Leading zeros are consumed but not folded and do not increment the significant count. The total-digit counter is replaced by the significant-digit counter in the magnitude decision. Once mag_bad is set, remaining digits are consumed without folding (as in R8).

On magnitude overflow: unchanged from R8. One loud PARSE_MAG trace, immediate return of -2 (MAGNITUDE_OVERFLOW), no value from the field committed. Return-code space unchanged: >= 0 means skipped-byte count, -1 means SHAPE_OVERFLOW, -2 means MAGNITUDE_OVERFLOW.

Doc-justification correction (frozen, required by the red team): the in-code contract comment states the rule in terms of SIGNIFICANT digits. The R8 claim "a run of 11+ digits is always > 2147483647 (min 10^10)" is SUPERSEDED by "11+ significant digits". The PARSE_MAG trace text is kept byte-verbatim from H-UNIFIED7 (including the H-UNIFIED7 tag, which marks the trace's introduction); it is now factually accurate on every path that emits it.

## Handler integration

Unchanged from R8. No handler edits. The three call sites keep their `< 0` guards and distinguishing traces.

## What does NOT change (frozen)

- All other parse_ints behavior: skip counting, PARSE_GUARD, SHAPE_OVERFLOW semantics, value recovery on valid inputs.
- All frozen main() test blocks K-U1-* through K-U7-2: kept verbatim; they must all still PASS with unchanged output. No frozen fixture contains a run with 11+ total digits but fewer than 11 significant digits; the X-U7-1 accept probe "0000000000" parses to value 0 under both R8 and R9.
- `unified5_learn.zag`, `unified6_learn.zag`, `unified7_learn.zag` untouched.

## Frozen kill bars

- K-U8-1: zero-padded runs judged by significant digits (parser-level, new block):
  - `parse_ints("00000000001",0,11)` returns 0 with value 1.
  - `parse_ints("00000000000000000001",0,20)` returns 0 with value 1.
  - `parse_ints("0000000000",0,10)` returns 0 with value 0.
  - `parse_ints("00000000002147483647",0,20)` returns 0 with value 2147483647 (exact max, zero-padded).
  - `parse_ints("00000000002147483648",0,20)` returns -2 (genuinely overflows).
- K-U8-2: all 22 frozen blocks from H-UNIFIED7 still PASS (expected total 23/23: 22 preserved + 1 new). Additionally, unified8 output up to the new K-U8-1 banner is byte-identical to the rebuilt frozen unified7 binary's output: the repair changes behavior only on runs with 11+ total digits but fewer than 11 significant digits, which no frozen fixture contains.
- K-U8-3: 3/3 runs byte-identical (cmp).

Kill criteria: any K-U8-1 assertion fails, any preserved block fails, the byte-identity prefix check fails, or any non-determinism -> H-UNIFIED8 KILLED (not adopted).
