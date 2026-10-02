# PREREG: H-UNIFIED7 Red Team (U7-ADV)

**Date:** 2026-09-29
**Target:** `unified7_learn.zag` on `tnn-native-lab` at HEAD (H-UNIFIED7,
R8 magnitude validation; result commit `11a85fc55`, prereg `5c92d3bdd`).
**Toolchain:** `znc 2026.07.0-dev (edition 2026)`, same as builder.
**Status:** FROZEN. Committed before any attack fixture, attack code,
build, or execution. No amendments after freezing.

## Mission

Assume the H-UNIFIED7 repair claim is false. Attack it. The repair
claim (from `UNIFIED7_RESULT.md`):

- R8: `parse_ints` gains exact magnitude validation with no wider
  type. 11+ digit runs rejected unconditionally; 10-digit runs checked
  before folding the 10th digit (`v9 > 214748364 ||
  (v9 == 214748364 && dig > 7)`); 9-or-fewer-digit runs always fit.
- On overflow: one loud `PARSE_MAG` trace, return -2
  (MAGNITUDE_OVERFLOW); no value from the field committed.
- Handlers (`handle_caus_learn`, `handle_caus_revise`,
  `handle_caus_query`) widen to `if(<0)` with magnitude-specific
  USHAPE traces. No wrapped key reaches `cpredict`.
- 22/22 pass, 3/3 deterministic, md5
  `1db7ed6ea1b51c8b6cd9c2d8a5422e80`.

## Method (frozen)

1. Build adversary harness `u7_adv.zag`: the committed
   `unified7_learn.zag` mechanism region copied byte-verbatim
   (verified with `cmp` against `git show HEAD:unified7_learn.zag`),
   with `main()` replaced by attack drivers that call the real,
   unmodified `parse_ints`, `handle_caus_learn`,
   `handle_caus_revise`, `handle_caus_query`.
2. Pure Zag throughout: hand-written fixtures, `znc` builds in
   `/tmp/u7adv` only (never committed), outputs compared with
   `cmp`/`md5sum`/`grep`. No Python at any stage.
3. Every empirical attack is run 3 times; runs must be byte-identical
   (`cmp`) to count as evidence.
4. No attack fixture, harness line, build, or run exists before this
   prereg is committed. Verified by the author at commit time.

## Attacks

### X-U7-1 (10-digit boundary fuzz)

Enumerate 10-digit runs straddling the i32-max boundary, checking
return code AND committed value:

- Accept set (must return 0 with exact value): `2147483640`,
  `2147483641`, `2147483642`, `2147483643`, `2147483644`,
  `2147483645`, `2147483646`, `2147483647`.
- Reject set (must return -2, no value committed): `2147483648`,
  `2147483649`, `9999999999`, `3000000000`.
- Shape anchors: `999999999` (9-digit, must 0),
  `1000000000` (10-digit, must 0, value 1000000000),
  `10000000000` (11-digit, must -2),
  `21474836470` (11-digit, must -2).

KILL criterion: any 10-digit run whose numeric VALUE is <=
2147483647 returns -2 (false reject on the value-exact path), or any
10-digit run whose VALUE is > 2147483647 returns >= 0 (silent accept
/ wrap). Either fires => H-UNIFIED7 KILLED (the boundary check is
unsound, and the exactness claim is false).

Note: the 11+ digit length-based path is deliberately excluded from
the kill criterion here; it is attacked separately as X-U7-3.

### X-U7-2 (downstream -2 handling)

Drive -2 through every real handler path and enumerate every
`parse_ints` call site in mechanism (non-`main`) code:

- `handle_caus_learn(W, "2147483648,0,0>1,2")` => 0 stored, loud
  traces, store empty.
- `handle_caus_revise(W, "!99999999999999999999,0,0>1,2")` => 0
  stored, loud traces.
- `handle_caus_query(W, "2147483648,0,0")` => withhold (return 0),
  magnitude trace.
- Mixed positions: `handle_caus_learn(W, "1,2147483648,3>4,5")`
  (overflow in a middle field) and
  `handle_caus_learn(W, "1,2>2147483648,5")` (overflow in the right
  field) => whole segment skipped loudly, zero commits.
- Static audit: every `parse_ints` call site outside `main()` test
  blocks must check `< 0` before any `get32` read of the out buffer.

KILL criterion: any handler path where `parse_ints` returns -2 and
the handler (a) reads `get32` from the out buffer anyway, (b)
commits a rule / answers a query from wrapped values, or (c) returns
without a loud trace; or any mechanism call site that fails the
static `< 0` check. Any fires => H-UNIFIED7 KILLED (the -2 code does
not contain the hazard downstream).

### X-U7-3 (spurious PARSE_MAG on legitimate values)

Zero-padded digit runs whose numeric VALUE fits i32:

- `"00000000001"` (11 digits, value 1)
- `"00000000000000000001"` (20 digits, value 1)
- `"0000000000"` (10 digits, value 0; control: the value-exact path
  must accept this)

SUCCESS criterion: any in-range VALUE (<= 2147483647) rejected with
`PARSE_MAG`.

Verdict mapping (frozen here, before execution): a success on X-U7-3
is a BOUNDARY finding, NOT a kill and NOT a downgrade. Rationale,
frozen in advance: the rejection is loud (`PARSE_MAG` trace, -2
code, handler USHAPE skip), so the X-U6-2 hazard class the repair
was built to close (caller acting on silently wrapped values with no
signal) is not recreated; no frozen kill bar governs zero-padded
runs. If it succeeds, the repair doc's justification
("11+ digits ... value >= 10^10 > 2147483647, overflow guaranteed")
is factually false for zero-padded runs and must be corrected, and
the conservative false positive is recorded as a known residual.

### X-U7-4 (regression + source audit)

- Rebuild the committed `unified7_learn.zag` unmodified with `znc`;
  run 3 times. All three outputs must be byte-identical (`cmp`) and
  md5 must equal the frozen `1db7ed6ea1b51c8b6cd9c2d8a5422e80`.
  Output must contain `=== RESULT: 22/22 ===` and zero `FAIL` lines.
- Source audit: the unified6 -> unified7 diff is exactly the frozen
  R8 change set (header note, `parse_ints` digit-run tracking +
  MAGNITUDE_OVERFLOW branch, three handler guard widenings with
  distinguishing traces, K-U7-1/K-U7-2 blocks, verdict strings); no
  test-answer literals in the `parse_ints`/handler mechanism region;
  the -2 return is produced only by the magnitude branch.

KILL criterion: any md5 mismatch, any `FAIL` line, non-identical
runs, or an audit finding of undeclared behavior change =>
H-UNIFIED7 KILLED.

## Verdict rules (frozen)

- Any KILL criterion fires => report H-UNIFIED7 KILLED, or
  DOWNGRADED if the finding narrows the claim without breaking a
  frozen bar (judged honestly at the time, with the bar named).
- X-U7-3 success => BOUNDARY (documented residual + doc correction),
  no kill, no downgrade.
- All four attacks fail to meet their criteria => H-UNIFIED7
  SURVIVES this red team.

## Governance (frozen)

- Pure Zag. No Python at any stage, including debugging.
- Only `u7_adversary/`-owned paths staged/committed. Concurrent
  workers' files untouched. No broad `git add`.
- No binaries committed (builds in `/tmp/u7adv` only).
- No em dashes in loop documentation.
- On `.git/index.lock` contention: wait for the live lock, never
  remove it.
