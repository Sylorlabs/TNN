# H-UNIFIED8 Independent Red Team: RESULT (U8-ADV)

**Date:** 2026-09-29
**Verdict: H-UNIFIED8 SURVIVES.** All four preregistered attacks failed.
No silent corruption, no loud false positives, no regression, no source
deviation. Classification unchanged: bounded L2 integration repair (parser
hardening). Not L3.

## Lineage (prereg strictly first)

- Prereg `u8_adversary/PREREG_U8_ADV.md` committed alone as `26ce81603`
  before any harness was written, built, or run. No amendments.
- Harness `u8_adversary/u8_adv.zag` = lines 1..1366 of the committed
  `unified8_learn.zag` (full mechanism region, extracted from
  `git show HEAD:...` and cmp-verified byte-identical) with `main()` replaced
  by attack drivers. The real unmodified `parse_ints`,
  `handle_caus_learn`, `handle_caus_revise`, `handle_caus_query`,
  `caus_active_count` are called. No mechanism edits.
- Toolchain `znc 2026.07.0-dev (edition 2026)`. Builds in /tmp/u8adv only.
  No binaries committed.
- Raw: `u8_adversary/U8_ADV_RAW_OUTPUT.txt`, 3/3 runs byte-identical (cmp),
  exit 0. 33/33 attack checks PASS, zero FAIL lines.
- Pure Zag throughout: no Python at any stage, including analysis and
  verification. Shell used only for build orchestration, grep, cmp, md5sum.
- Only owned paths staged: `u8_adversary/`. Concurrent workers untouched.

## X-U8-1 (Edge): handler-level significant-digit cases. FAILED (defense holds)

- E1 PASS: `handle_caus_learn("000,000,000>000,000")` stored 1 rule
  (R0 IF s0==0 AND a==0 THEN s1:=0). All-zero fields parse to 0 cleanly.
- E2 PASS: 28-char zero-padded 1 learn stored 1 rule (s0==1). No PARSE_MAG.
- E3 PASS: zero-padded exact i32 max `"00000000002147483647"` learn stored 1
  rule (s0==2147483647). No PARSE_MAG.
- E4 PASS: zero-padded max+1 `"00000000002147483648"` learn stored 0 rules,
  active count 0, exactly one PARSE_MAG trace plus one USHAPE (parser
  magnitude) trace. Genuine overflow rejected loudly, nothing committed.
- E5 PASS: on the E2 store, query `"0000000001,000,000"` and `"1,0,0"` both
  fired with identical predictions (`s0=1 s1=2`). Padding introduces no
  withhold and no answer change.
- E6 PASS: `parse_ints` on a 100-zero run returns 0 with value 0.

## X-U8-2 (Fuzz): 10-significant-digit boundary with leading zeros. FAILED (defense holds)

All 20 hand-derived (rc, value) expectations matched exactly:

- F1 `"00000000002147483647"` -> (0, 2147483647). F2 `"00000000002147483648"`
  -> -2. F3 `"0002147483647"` -> (0, 2147483647). F4 `"0002147483648"` -> -2.
- F5 `"09999999999"` -> -2. F6 `"009999999999"` -> -2 (11 significant nines).
- F7 `"0000000000999999999"` -> (0, 999999999). F8 `"00000000001000000000"`
  -> (0, 1000000000). F9 `"00000000003000000000"` -> -2.
- F10 `"00000000002147483640"` -> (0, 2147483640).
  F11 `"00000000002147483646"` -> (0, 2147483646).
- F12 50-char zero-padded 1 -> (0, 1). F13 50 zeros -> (0, 0).
- F14 `"10000000000"` -> -2. F15 `"010000000000"` -> -2 (11 sig digits).
  F16 `"0010000000000"` -> -2 (10^10). F17 `"0001000000000"` -> (0, 10^9).
- F18 `"2147483647"` -> (0, 2147483647). F19 `"2147483648"` -> -2.
  F20 `"0"` -> (0, 0).

PARSE_MAG traces appear exactly on the nine expected -2 cases, zero elsewhere.

## X-U8-3 (Interaction): leading zeros vs comma/field splitting. FAILED (defense holds)

- I1 PASS: `"00000000001,2,3"` -> [1,2,3].
- I2 PASS: `"000,00000000002147483647,0"` -> [0,2147483647,0].
- I3 PASS: `"1,00000000000000000001"` -> [1,1].
- I4 PASS: `"000000000000,5"` -> [0,5].
- I5 PASS: learn `"000,000,001>000,002"` stored rule (0,0,1)->(0,2); queries
  `"000,000,001"` and `"0,0,1"` both fired with identical predictions.
- I6 PASS: `"7,00000000000000000000008"` -> [7,8] (trailing run at hi).
- I7 PASS: learn `"1,2,0000000000000003>4,5"` and plain `"1,2,3>4,5"` produce
  byte-identical behavior: both fire on `"1,2,3"` (s0=1 s1=5), both withhold
  on `"1,2,4"`. The zero-padded act parsed as exactly 3.

## X-U8-4 (Regression and source audit). FAILED (defense holds)

- Rebuilt the committed `unified8_learn.zag` unmodified: 3/3 runs
  byte-identical, md5 `df52b05db95dd560f8e3f7643e0bdec1` (matches the frozen
  H-UNIFIED8 raw hash), `=== RESULT: 23/23 ===`, zero FAIL lines, exit 0.
- unified7 -> unified8 diff is exactly the frozen R9 change set and nothing
  else: header note, parse_ints contract comment, `d` -> `sig` counting with
  the `(dig!=0 || sig>0)` significant-digit guard, K-U8-1 block, verdict
  strings. No handler edits, no other mechanism edits.
- unified8 output up to the K-U8-1 banner is byte-identical to the committed
  UNIFIED7_RAW_OUTPUT.txt (excluding znc: build-artifact lines and the final
  22/22 verdict block that the K-U8-1 insertion displaced). All 22 frozen
  fixture outputs unchanged: the repair alters behavior only on runs with
  11+ total digits but fewer than 11 significant digits, which no frozen
  fixture contains.
- 8 PARSE_MAG traces total (4 K-U7-1, 3 K-U7-2, 1 K-U8-1 genuine-overflow);
  `s0==-2147483648` appears zero times.
- No test-answer literals in the parse_ints/handler mechanism region beyond
  the algorithm constants (214748364 / 2147483647 in the exact pre-fold
  check itself).

## Analysis

The significant-digit counting is correct by construction and the red team
found no implementation slip: (a) the guard `(dig!=0 || sig>0)` counts
exactly the significant digits; (b) `sig` reaches 9 with `v` holding the
9-significant-digit prefix (<= 999999999, exact in i32), so the 10th-digit
check `v > 214748364 || (v == 214748364 && dig > 7)` is exact and the fold
cannot overflow i32; (c) 11+ significant digits imply value >= 10^10, so the
unconditional rejection is exact; (d) for runs with no leading zeros `sig`
tracks the old `d` exactly, so R9 behavior is provably identical to R8 on
all non-zero-padded inputs, which the byte-identical frozen-fixture prefix
confirms empirically. The one residual from H-UNIFIED7 red team (X-U7-3
false positive on zero-padded runs) is closed, and no new boundary class
was found: every rejection observed was a genuine i32 overflow, every
fitting value parsed to its exact value at every level (parser return code,
committed store value, query behavior).

## Files (branch `tnn-native-lab`, `docs/lab/research-lead/overnight-20260928/u8_adversary/`)

- `PREREG_U8_ADV.md` (commit `26ce81603`, frozen before any attack work)
- `u8_adv.zag` (adversary harness: committed mechanism region + attack main)
- `U8_ADV_RAW_OUTPUT.txt` (3/3 byte-identical runs, exit 0)
- `U8_ADV_RESULT.md` (this file)
