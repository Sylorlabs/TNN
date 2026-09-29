# H-UNIFIED7 Red Team: RESULT (U7-ADV)

**Date:** 2026-09-29
**Verdict: H-UNIFIED7 SURVIVES this red team, with one documented
boundary (X-U7-3).** Three of four attacks fail with all defenses
holding; the fourth succeeds exactly as preregistered as a boundary
finding (loud conservative false positive; no kill, no downgrade).
**Target:** `unified7_learn.zag` (H-UNIFIED7, R8), committed at HEAD.
**Prereg:** `u7_adversary/PREREG_U7_ADV.md`, committed alone as
`3ffd96b9f` before any attack fixture, code, build, or run. No
amendments. `merge-base --is-ancestor` verified at result commit.
**Purity:** Pure Zag throughout (hand-written harness, fixtures,
drivers). Shell only for build orchestration (`znc`), `grep`,
`cmp`, `md5sum`. No Python at any stage.

## Method

Adversary harness `u7_adv.zag`: lines 1..1341 of the committed
`unified7_learn.zag` (full mechanism region, `cmp`-verified
byte-identical to `git show HEAD:...`, and committed-file md5 ==
worktree-file md5 `fad1573537d8eb049e87c67091f33861`) with `main()`
replaced by attack drivers calling the real, unmodified
`parse_ints`, `handle_caus_learn`, `handle_caus_revise`,
`handle_caus_query`, `caus_active_count`. Toolchain
`znc 2026.07.0-dev (edition 2026)`, same as builder. Every empirical
attack run 3 times; all runs byte-identical (`cmp`).

## X-U7-1 (10-digit boundary fuzz): FAILS, defense holds

18 checks, all PASS, 3/3 byte-identical. Accept set
(`2147483640`..`2147483647`, `999999999`, `1000000000`, `0`,
`0000000000`) all return 0 with exact values; reject set
(`2147483648`, `2147483649`, `9999999999`, `3000000000`,
`10000000000`, `21474836470`) all return -2 with `PARSE_MAG`. The
10-digit value-exact check
(`v>214748364 || (v==214748364 && dig>7)`) is empirically exact at
the boundary: no off-by-one in either direction. The kill criterion
does not fire.

## X-U7-2 (downstream -2 handling): FAILS, defense holds

Six handler paths driven through the real handlers, all skip loudly
with zero commits and an empty store (`active=0`):

- `handle_caus_learn("2147483648,0,0>1,2")` => 0 stored,
  `PARSE_MAG` + `USHAPE: segment skipped (parser magnitude)
  [2147483648,0,0>1,2] (H-UNIFIED7)`.
- `handle_caus_revise("!99999999999999999999,0,0>1,2")` => 0 stored,
  same loud pair.
- `handle_caus_query("2147483648,0,0")` => withhold (return 0),
  `QCAUS USHAPE WITHHOLD: parser magnitude (H-UNIFIED7)`.
- `handle_caus_learn("1,2147483648,3>4,5")` (middle-field overflow)
  => whole segment skipped loudly, 0 stored.
- `handle_caus_learn("1,2,3>2147483648,5")` (right-field first value)
  => skipped loudly, 0 stored.
- `handle_caus_learn("1,2,3>4,2147483648")` (right-field second
  value) => skipped loudly, 0 stored.

Static audit: all three mechanism `parse_ints` call sites
(`handle_caus_learn`, `handle_caus_revise`, `handle_caus_query`)
check `< 0` before any `get32` read of the out buffer. The only
other `return -2` in the file (line 750) is `field_kind`'s
pre-existing empty-field code, which can only reach the H-UNIFIED6
shape gate, never a parse-code comparison. No kill criterion fires.

## X-U7-3 (spurious PARSE_MAG on legitimate values): SUCCEEDS as
BOUNDARY (preregistered)

- `"00000000001"` (11 digits, value 1) => rc=-2 with `PARSE_MAG`.
- `"00000000000000000001"` (20 digits, value 1) => rc=-2 with
  `PARSE_MAG`.
- Control `"0000000000"` (10 digits, value 0) => rc=0, value 0.

The 11+ digit path is length-based, not value-based: it rejects
zero-padded runs whose numeric value fits i32. The trace message
"digit run exceeds i32 range" is factually false for these inputs,
and the repair doc's justification ("11+ digits ... value >= 10^10
> 2147483647, overflow guaranteed") is false for zero-padded runs.

Per the frozen verdict mapping this is a BOUNDARY, not a kill and
not a downgrade: the rejection is loud (trace + -2 code + handler
USHAPE skip), so the X-U6-2 hazard class the repair was built to
close (caller acting on silently wrapped values with no signal) is
not recreated, and no frozen kill bar governs zero-padded runs.
Required follow-up: correct the doc justification; record the
conservative false positive as a known residual. Suggested repair
direction for a future lane: count significant digits (strip leading
zeros) before applying the 11+ rule, or fold with the exact check
for runs up to a bounded significant length.

## X-U7-4 (regression + source audit): FAILS, defense holds

- Rebuilt the committed `unified7_learn.zag` unmodified: 3/3 runs
  byte-identical, md5 `1db7ed6ea1b51c8b6cd9c2d8a5422e80` matching the
  frozen hash exactly, `=== RESULT: 22/22 ===`, zero `FAIL` lines.
- Source audit: the unified6 -> unified7 diff is exactly the frozen
  R8 change set (header note, `parse_ints` digit-run tracking +
  MAGNITUDE_OVERFLOW branch, three handler guard widenings with
  distinguishing traces, K-U7-1/K-U7-2 blocks, verdict strings; 174
  diff lines, all accounted). No test-answer literals in the
  `parse_ints`/handler mechanism region (the constants 214748364 /
  2147483647 in code are the algorithm, appearing only in comments
  and the check itself). The -2 code is produced only by the
  `parse_ints` magnitude branch.

## Raw evidence

- `U7_ADV_RAW.txt`: attack runs, md5
  `3ba51a72b2333c22837a9b9723e36972`, 3/3 byte-identical, exit 0,
  `=== U7-ADV RESULT: pass=20 fail=0 ===`.
- `u7_adv.zag`: adversary harness (mechanism region cmp-verified
  byte-identical to committed lines 1..1341 + attack `main`).

## Governance disclosures

1. Prereg `3ffd96b9f` strictly precedes all attack work; verified
   via `merge-base --is-ancestor` at result commit.
2. Harness fixture bug, caught and corrected mid-run: the X-U7-2
   right-field probe was first written as `"1,2>2147483648,5"`
   (2-int left side), which tripped the H-UNIFIED6 shape gate instead
   of the magnitude path. Corrected to `"1,2,3>2147483648,5"` and
   added `"1,2,3>4,2147483648"` (second right value). All reported
   evidence is from the corrected harness, 3/3 deterministic. The
   prereg's frozen kill criteria are unaffected (the corrected
   fixtures are strictly stronger probes of the same criterion).
3. Pure Zag: no Python at any stage, including debugging.
4. Only `u7_adversary/`-owned paths staged/committed. Concurrent
   workers' files untouched. No broad `git add`.
5. No binaries committed (builds in `/tmp/u7adv` only).
6. No em dashes in loop documentation.
7. All commits local; no push authorized or attempted.

## Classification

Bounded L2 integration repair (parser hardening), red-team
surviving. Not L3. No L3 claim was made or attacked.

## Files (branch `tnn-native-lab`,
`docs/lab/research-lead/overnight-20260928/u7_adversary/`)

- `PREREG_U7_ADV.md` (commit `3ffd96b9f`)
- `U7_ADV_RESULT.md` (this file)
- `U7_ADV_RAW.txt`
- `u7_adv.zag`

## Suggested follow-ups for the parent

1. Doc-justification correction for the 11+ digit rule
   (zero-padded runs), recorded above as a boundary.
2. Optional future lane: significant-digit counting for the 11+
   path to remove the conservative false positive.
3. The paper's H-UNIFIED6/H-UNIFIED7 section needs this red-team
   result in full (paper lane).
