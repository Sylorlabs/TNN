# PREREG: H-UNIFIED8 Independent Red Team (U8-ADV)

**Date:** 2026-09-29
**Target:** H-UNIFIED8 SURVIVES (23/23), R9 significant-digit magnitude validation.
**Assumption under test:** the R9 claim is false. The repair judges digit runs by
SIGNIFICANT digits: leading zeros are consumed but not folded and do not increment
the significant-digit counter `sig`; 11+ significant digits are rejected
unconditionally; 10 significant digits use the exact R8 pre-fold check
(`v > 214748364 || (v == 214748364 && dig > 7)`); 9 or fewer always fit; all-zero
runs yield value 0. On overflow: PARSE_MAG trace + return -2, no value committed.
Handlers unchanged.

**Method:** adversary harness `u8_adv.zag` = lines 1..1366 of the committed
`unified8_learn.zag` (full mechanism region, cmp-verified byte-identical to
`git show HEAD:...`) with `main()` replaced by attack drivers calling the real,
unmodified `parse_ints`, `handle_caus_learn`, `handle_caus_revise`,
`handle_caus_query`, `caus_active_count`. Toolchain `znc 2026.07.0-dev
(edition 2026)`. Every empirical attack run 3 times; all runs must be
byte-identical (cmp). Pure Zag throughout; shell only for build orchestration
(znc), grep, cmp, md5sum. No Python at any stage.

## X-U8-1 (Edge): significant-digit edge cases at handler level

Drive zero-padded and all-zero inputs through the real handlers.

- E1: `handle_caus_learn(W,"000,000,000>000,000")`. Expect: parses clean (rc 0
  on both fields), learns normally (nstored >= 1), zero PARSE_MAG traces, zero
  USHAPE traces.
- E2: `handle_caus_learn(W,"0000000000000000000000000001,0,0>1,2")`
  (28-char zero-padded 1, value 1). Expect: nstored >= 1, zero PARSE_MAG.
- E3: `handle_caus_learn(W,"00000000002147483647,0,0>1,2")` (zero-padded exact
  i32 max). Expect: nstored >= 1, zero PARSE_MAG.
- E4: `handle_caus_learn(W,"00000000002147483648,0,0>1,2")` (zero-padded max+1,
  genuine overflow). Expect: 0 stored, exactly one PARSE_MAG trace, one USHAPE
  (parser magnitude) trace.
- E5: after E2, `handle_caus_query` on zero-padded `"0000000001,000,000"` vs
  plain `"1,0,0"`. Expect: identical return codes and identical behavior (no
  withhold introduced by padding).
- E6: `parse_ints` on a 100-zero run. Expect: rc 0, value 0.

**Kill criterion:** any PARSE_MAG or -2 on a value that fits i32; any committed
value that differs from the hand-derived value (silent wrap); any USHAPE
withhold on a zero-padded valid query. Silent corruption -> KILL. A loud
conservative rejection (trace + -2, no commit) on a fitting value ->
DOWNGRADE (new boundary class, not a kill).

## X-U8-2 (Fuzz): 10-significant-digit boundary with leading zeros

Hand-derived battery. Each entry: input, expected rc, expected value (when
rc == 0). All expectations derived by hand before any run.

- F1:  "00000000002147483647" -> 0, 2147483647
- F2:  "00000000002147483648" -> -2
- F3:  "0002147483647" -> 0, 2147483647
- F4:  "0002147483648" -> -2
- F5:  "09999999999" -> -2
- F6:  "009999999999" -> -2
- F7:  "0000000000999999999" -> 0, 999999999
- F8:  "00000000001000000000" -> 0, 1000000000
- F9:  "00000000003000000000" -> -2
- F10: "00000000002147483640" -> 0, 2147483640
- F11: "00000000002147483646" -> 0, 2147483646
- F12: 50-char zero-padded 1 -> 0, 1
- F13: 50 zeros -> 0, 0
- F14: "10000000000" -> -2
- F15: "010000000000" -> -2
- F16: "0010000000000" -> -2
- F17: "0001000000000" -> 0, 1000000000
- F18: "2147483647" -> 0, 2147483647
- F19: "2147483648" -> -2
- F20: "0" -> 0, 0

**Kill criterion:** any observed (rc, value) pair differing from the table ->
KILL if the value is silently wrong, DOWNGRADE if loud-conservative on a
fitting value.

## X-U8-3 (Interaction): leading-zero consumption vs comma/field splitting

- I1: `parse_ints("00000000001,2,3",0,13,out)` -> rc 0, out = [1,2,3].
- I2: `parse_ints("000,00000000002147483647,0",0,26,out)` -> rc 0,
  out = [0,2147483647,0].
- I3: `parse_ints("1,00000000000000000001",0,21,out)` -> rc 0, out = [1,1].
- I4: `parse_ints("000000000000,5",0,13,out)` -> rc 0, out = [0,5].
- I5: `handle_caus_learn(W,"000,000,001>000,002")` then query zero-padded vs
  plain forms of the learned state. Expect: same prediction both forms.
- I6: `parse_ints("7,00000000000000000000008",0,25,out)` -> rc 0, out = [7,8].
- I7: `handle_caus_learn(W,"1,2,0000000000000003>4,5")` -> learns with
  s0=1, s1=2, act=3 (verify via query prediction matching the plain
  `"1,2,3>4,5"` learned rule).

**Kill criterion:** any field-boundary misparse (wrong value, wrong field
count, -2 on valid input, value from one field landing in another slot) ->
KILL.

## X-U8-4 (Regression and source audit)

- Rebuild the committed `unified8_learn.zag` unmodified: 3/3 runs
  byte-identical, md5 must equal the frozen `df52b05db95dd560f8e3f7643e0bdec1`,
  `=== RESULT: 23/23 ===` (or the file's verdict line), zero FAIL lines.
- Diff unified7 -> unified8 must be exactly the frozen R9 change set (header
  note, parse_ints contract comment, d->sig counting change, K-U8-1 block,
  verdict strings). No other mechanism edits.
- unified8 output up to the K-U8-1 banner must be byte-identical to the
  committed UNIFIED7_RAW_OUTPUT.txt (excluding znc: build-artifact lines):
  the repair changes behavior only on runs with 11+ total digits but fewer
  than 11 significant digits, which no frozen fixture contains.
- No test-answer literals in the parse_ints/handler mechanism region beyond
  the algorithm constants (214748364 / 2147483647 in the check itself).

**Kill criterion:** any FAIL line, any md5 mismatch, any non-frozen diff hunk,
any behavioral delta on frozen fixtures -> KILL.

## Verdict rule

- Any kill criterion firing on SILENT corruption (wrong value committed or
  used, wrapped value reaching a handler) -> H-UNIFIED8 KILLED.
- Any kill criterion firing as LOUD conservative rejection (trace + -2, zero
  commits) on a value that fits i32 -> H-UNIFIED8 DOWNGRADED (new boundary
  class; the X-U6-2 silent hazard is not recreated).
- X-U8-4 failure -> KILL (evidence integrity).
- All four attacks fail with defenses holding -> H-UNIFIED8 SURVIVES.
