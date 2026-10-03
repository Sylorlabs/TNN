# H-UNIFIED8: RESULT (R9 significant-digit magnitude validation)

**Date:** 2026-09-29
**Verdict: H-UNIFIED8 SURVIVES (23/23).** The X-U7-3 boundary (spurious PARSE_MAG on zero-padded runs) is closed at the mechanism level, and the R8 doc justification is corrected. Classification: bounded L2 integration repair (parser hardening). Not L3.

## Lineage (prereg strictly first)

- Prereg `PREREG_UNIFIED8.md` committed alone as `718f98359` before any implementation edit, build, or run. No amendments. `git merge-base --is-ancestor` verified at result commit.
- `unified8_learn.zag` = committed `unified7_learn.zag` copied verbatim (cmp-verified), plus exactly the frozen R9 change set. `unified7_learn.zag` untouched. The committed `unified8_learn.zag` is cmp-verified byte-identical to the tested source.
- Source diff u7->u8 is exactly the frozen change set: file header note, parse_ints contract-comment correction, digit-loop significant-digit counting (d replaced by sig), K-U8-1 test block, verdict strings. No handler edits.

## The repair (R9)

`parse_ints` judges a digit run by its SIGNIFICANT digits: leading zeros are consumed but not folded and do not increment the significant-digit counter. 11+ significant digits are rejected unconditionally (value >= 10^10 > 2147483647, now genuinely true); 10 significant digits use the exact R8 pre-fold check against 2147483647; 9 or fewer significant digits always fit; an all-zero run yields value 0. On overflow the parser emits the same loud PARSE_MAG trace (byte-verbatim from H-UNIFIED7, including the H-UNIFIED7 tag that marks the trace's introduction; now factually accurate on every path that emits it) and returns -2 (MAGNITUDE_OVERFLOW) immediately; no value from the field is committed. Return-code space unchanged. Handlers unchanged: the three call sites keep their `< 0` guards.

Doc-justification correction (required by the red team): the in-code contract comment now states the rule in terms of SIGNIFICANT digits. The R8 claim "a run of 11+ digits is always > 2147483647 (min 10^10)" is SUPERSEDED for zero-padded runs.

## Frozen kill-bar evidence

Raw: `UNIFIED8_RAW_OUTPUT.txt` (md5 `df52b05db95dd560f8e3f7643e0bdec1`), 3/3 runs byte-identical (cmp), exit 0, built with `znc 2026.07.0-dev (edition 2026)`. Zero FAIL lines.

- **K-U8-1 PASS:** `parse_ints("00000000001",0,11)` returns 0 with value 1; `parse_ints("00000000000000000001",0,20)` returns 0 with value 1; `parse_ints("0000000000",0,10)` returns 0 with value 0; `parse_ints("00000000002147483647",0,20)` returns 0 with value 2147483647 (exact max, zero-padded); `parse_ints("00000000002147483648",0,20)` returns -2 with PARSE_MAG (genuinely overflows). The X-U7-3 false positive is gone and genuine zero-padded overflow is still caught loudly.
- **K-U8-2 PASS:** all 22 preserved blocks PASS (23/23 total). The rebuilt frozen unified7 binary reproduces the committed `UNIFIED7_RAW_OUTPUT.txt` exactly (md5 `1db7ed6ea1b51c8b6cd9c2d8a5422e80`); unified8 output up to the new K-U8-1 banner is byte-identical to it (excluding `znc:` build-artifact lines). The repair changes behavior only on runs with 11+ total digits but fewer than 11 significant digits, which no frozen fixture contains. 8 PARSE_MAG traces total (4 K-U7-1, 3 K-U7-2, 1 K-U8-1 genuine-overflow); `s0==-2147483648` appears zero times (grep-verified).
- **K-U8-3 PASS:** 3/3 runs byte-identical (cmp).

## Governance disclosures

- Prereg committed alone (`718f98359`) before the verbatim copy and any edit; strict-ancestor ordering verified via `git merge-base --is-ancestor` at result commit.
- Only owned paths staged and committed: `PREREG_UNIFIED8.md`, `unified8_learn.zag`, `UNIFIED8_RAW_OUTPUT.txt`, `UNIFIED8_RESULT.md`. Concurrent workers' files untouched; no broad `git add`.
- Pure Zag throughout: no Python at any stage, including analysis and verification.
- No binaries committed (builds in /tmp/u8 only).
- No em dashes in loop documentation.
- All commits local; no push authorized or attempted.

## Files (branch `tnn-native-lab`, `docs/lab/research-lead/overnight-20260928/`)

- `PREREG_UNIFIED8.md` (commit `718f98359`)
- `unified8_learn.zag`
- `UNIFIED8_RAW_OUTPUT.txt`
- `UNIFIED8_RESULT.md` (this file)
