# PREREG: H-UNIFIED6 Independent Red Team

**Date:** 2026-09-29
**Status:** FROZEN. No attack code exists yet. All attack execution must strictly descend from this commit.
**Target:** `unified6_learn.zag` at `ad82aba60` (H-UNIFIED6 SURVIVES 20/20), mechanism region lines 1-1283 (everything before `fn main`).
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.
**Stance:** Assume H-UNIFIED6 is false. Attacks succeed only on preregistered criteria below.

## Background

H-UNIFIED6 claims two closures over H-UNIFIED5 residuals:
- R1: `parse_ints` returns a programmatic anomaly code: >= 0 = skipped non-digit byte count (0 = clean parse); -1 = SHAPE_OVERFLOW (field holds more values than `out.len/4`; parser stops at capacity, emits one PARSE_SHAPE trace, NEVER writes past `out.len`).
- R2: handler-layer shape verification as second layer: `handle_caus_learn` and `handle_caus_revise` require each segment to be exactly 3-int `>` 2-int via `field_kind` on both sides of the separator; `handle_caus_query` requires exactly one 3-int tuple. Malformed input emits USHAPE, is skipped, never parsed, never committed, never panics. A `parse_ints` return of -1 at the handlers is stated UNREACHABLE given the `field_kind` gate.

Frozen prereg text (PREREG_UNIFIED6.md): "no panic is possible from the parser, and no silent arena corruption is possible through a short view."

## Attack surface (from source reading only, no execution yet)

1. `route_line` never calls `parse_ints`; classification is `field_kind`-only. All `parse_ints` call sites are the three gated handlers plus the K-U6-1/K-U6-2 in-binary probes.
2. The `field_kind` gate admits ONLY digit/comma shapes with exact int counts (3 left, 2 right). `parse_ints` writes exactly one i32 per digit run. Post-gate, digit runs == int count == capacity. The -1 branch requires a (cap+1)-th value, which the gate makes impossible. Unreachability argument is sound on reading; X-U6-1 tests it empirically.
3. `parse_ints` accumulates each value as `v=v*10+((b[i] as i32)-48)` with NO width bound. `field_kind` counts a 20-digit run as one int and passes it. i32 overflow semantics of the toolchain are UNKNOWN to this red team (no probe run yet, by design). X-U6-2 tests the consequences through the defended path.
4. Every skip path in the handlers emits a USHAPE trace. X-U6-3 tests for any silent drop or accounting mismatch.

## Attacks and frozen kill criteria

### X-U6-1: parse-return bypass (reach the "unreachable" -1)

Battery of gate-passing shapes through the real handlers (direct calls + route_line classification), asserting the -1 branch never fires:
- F6a: `handle_caus_learn(W,"0,0,0>0,0;00,01,10>20,30")` — expect return 2, zero PARSE_SHAPE traces, values exact.
- F6b: `handle_caus_learn(W,"123,456,789>10,20")` — expect return 1, values [123,456,789,10,20] committed, zero PARSE_SHAPE.
- F6c: `handle_caus_query(W,"7,8,9")` after learning — expect no PANIC, no PARSE_SHAPE.
- F6d: direct `parse_ints("1,0,0",0,5,view12)` — expect return 0 (control: parser reachable normally).
- F7 (informational, direct call): `parse_ints("1,0,0,x",0,7,view12)` — document the return (contract interpretation: 3 values + 1 skip; NOT a kill either way).

**KILL iff:** any handler-reachable input causes `parse_ints` to return -1 (the "unreachable" USHAPE-parser-capacity branch fires), or any write past `out.len` is demonstrated (canary corruption), or the parser panics. **FAILS iff:** zero PARSE_SHAPE traces and zero -1 returns across the whole battery, 3/3 runs.

### X-U6-2: shape-gate bypass via digit magnitude

`field_kind` has no per-int width limit; the parser has no width bound. Fixtures (frozen):
- F1: `route_line("99999999999999999999,0,0>1,2;2,0,0>3,4")` must classify CAUS_LEARN (code 2); then `handle_caus_learn` on the same line.
- F2: `handle_caus_learn(W,"2147483648,0,0>1,2")` (exactly 2^31).
- F3: `handle_caus_learn(W,"123456789012345678901234567890,1,2>3,4")` (30 digits).
- F1q: `handle_caus_query(W,"99999999999999999999,0,0")` direct.

Record for each: exit status (0 vs panic), full stdout, the committed/stored values where observable, and the `parse_ints` return where bound.

**DOWNGRADE iff:** any gate-passing fixture causes a panic in `parse_ints` or the handlers. This directly contradicts the frozen "no panic is possible from the parser" and R2 "never panics": a crash-class hazard reachable through the defended path.
**BOUNDARY (disclosed, not a kill) iff:** no panic, but a wrapped/truncated i32 value is committed with return 0 ("clean parse") and no trace. Digit magnitude is outside the frozen field-count bars (K-U6-2's "bad shape" means field-count shape; the result doc's limitation 1 already concedes the parser is "capacity-safe but not a validator"). A silent wrong value is a real integrity gap and will be reported as a narrowed claim, not a bar break.
**FAILS iff:** neither occurs (e.g., honest refusal or exact handling), 3/3 runs.

### X-U6-3: USHAPE silent loss

- F4: `handle_caus_learn(W,"1,0,0>2,1;BADSEG;3,3,3>4,4")` direct. Expect: exactly one USHAPE trace (the BADSEG segment), return value 2 (both good episodes stored), no other trace lines.
- F5: `handle_caus_learn(W,"BAD1;BAD2;NOSEP")` direct. Expect: return 0, exactly three USHAPE traces, store unchanged.

**KILL iff:** any malformed segment is dropped with NO USHAPE/PARSE_SHAPE trace, or the return value counts a skipped segment as stored, or a bad episode is committed. **FAILS iff:** every skip is traced and accounting is exact, 3/3 runs.

### X-U6-4: regression + source audit

- Rebuild `unified6_learn.zag` from the committed blob at `ad82aba60` with the pinned toolchain (`znc 2026.07.0-dev (edition 2026)`), unmodified.
- stdout must be byte-identical to committed `UNIFIED6_RAW_OUTPUT.txt` (md5 `4d6eee84e8f058cadc544f61a44fddb0`); 3/3 runs byte-identical.
- The 20/20 in-binary checks must pass; grep over frozen output lines 2-125: zero PARSE_GUARD, zero PARSE_SHAPE, zero USHAPE.
- Source audit: the committed implementation must match the frozen PREREG_UNIFIED6.md design (R1 contract, R2 gates, K-U6-1/K-U6-2 blocks); `unified5_learn.zag` untouched; no test-answer literals in mechanism regions (lines 1-1283).

**DOWNGRADE iff:** rebuilt output deviates from the committed raw evidence, or 3/3 determinism fails, or any frozen check regresses. **KILL iff:** the source audit finds the implementation diverging from the frozen design in a behavior-changing way, or test-answer literals in the mechanism region. **FAILS iff:** all hold.

## Method

- Adversary harness `u6_adversary/u6_adv.zag` = committed `unified6_learn.zag` lines 1-1283 (mechanism region), verified byte-identical via `cmp` against `git show ad82aba60:...unified6_learn.zag`, with `main()` replaced by the attack drivers above. A separate minimal `main()` binary is used for any panic probe so a crash cannot contaminate other evidence.
- Every attack executed 3 times; all evidence from byte-identical runs only.
- No worker-count claims (unverified per standing correction).

## Deliverables

- `u6_adversary/PREREG_U6_ADV.md` (this file)
- `u6_adversary/u6_adv.zag`, `u6_adversary/U6_ADV_RAW.txt`, `u6_adversary/U6_ADV_RESULT.md`
- Committed to `tnn-native-lab`. Only adversary-owned paths staged.

## Classification note

A DOWNGRADE here narrows the H-UNIFIED6 claim; it does not kill the mechanism unless a frozen bar is broken. BOUNDARY findings are reported as narrowed claims with exact fixtures. The frozen K-U6-1..K-U6-5 bars are not re-litigated; only the four attacks above can change the verdict.
