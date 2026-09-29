# H-UNIFIED6 Red Team: RESULT

**Date:** 2026-09-29
**Verdict: H-UNIFIED6 DOWNGRADED (not killed).**
**Target:** `unified6_learn.zag` at `ad82aba60` (H-UNIFIED6 SURVIVES 20/20).
**Prereg:** `u6_adversary/PREREG_U6_ADV.md`, committed alone at `029e2abd7` before any attack code or execution.
**Purity:** Pure Zag throughout. No Python at any stage. Zero pre-prereg execution of any kind.

## Summary

One of four preregistered attacks succeeds. X-U6-2 demonstrates that digit-magnitude overflow silently wraps: a 20-digit input is committed to the causal store as a mod-2^32 residue with the parser returning 0 ("clean parse") and no trace of any kind. No frozen kill bar is broken (K-U6-1..K-U6-5 never promised magnitude validation), the mechanism is not killed, and all 20/20 frozen checks reproduce byte-identically. But the R1 headline claim — "0 means a clean parse," "a caller that ignores stdout still learns ... the anomaly rides in the return value" — is false as literally stated: for magnitude overflow the caller learns nothing and acts on wrapped values, which is exactly the H1 hazard class R1 was built to close. The "programmatic anomaly flag" claim narrows to skipped bytes and field-count overflow. X-U6-1, X-U6-3, and X-U6-4 fail: those defenses hold exactly as claimed.

## Preregistration and commit lineage

- Prereg frozen BEFORE any attack code or execution: `u6_adversary/PREREG_U6_ADV.md`, commit `029e2abd7`.
- Attack artifacts and result: this commit. Only adversary-owned paths staged; concurrent workers' files untouched (verified via `git status` before and after staging).
- Ancestor check: `git merge-base --is-ancestor 029e2abd7 HEAD` must return true (verified at commit time).
- Target implementation: `unified6_learn.zag` at `ad82aba60`; toolchain `znc 2026.07.0-dev (edition 2026)` at `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.
- No worker-count claims (unverified per standing correction).

## Methodology

Two adversary harnesses, each = committed `unified6_learn.zag` lines 1-1283 (mechanism region; `fn main` begins at line 1285), verified byte-identical via `cmp` against `git show ad82aba60:...unified6_learn.zag`, with `main()` replaced by the attack drivers:
- `u6_adversary/u6_adv.zag`: X-U6-1 battery + X-U6-3 (no panic risk in any fixture).
- `u6_adversary/u6_adv_mag.zag`: X-U6-2 magnitude probes only (panic-isolated per the prereg method, so a crash cannot contaminate other evidence).
Every attack executed 3 times; all three runs byte-identical (cmp). All evidence below comes from the byte-identical runs. Binaries lived in `/tmp/u6adv` only; none committed.

## Attack-by-attack results

### X-U6-1: parse-return bypass — FAILS (defense holds)

Theory: reach the "unreachable" -1 branch at a handler, i.e. find a gate-passing input where `parse_ints` returns -1, writes past `out.len`, or panics. The unreachability argument (field_kind counts exactly cap ints; parse_ints writes one i32 per digit run) was tested empirically.

Raw (`U6_ADV_RAW.txt`, md5 `737bf2b78a411de4fe89bd4a314ff990`, 3/3 identical):
- F6a `handle_caus_learn(W,"0,0,0>0,0;00,01,10>20,30")` → return 2 (expect 2). Rules R0/R1 stored with exact values, including leading-zero inputs (`00`→0, `01`→1).
- F6b `handle_caus_learn(W,"123,456,789>10,20")` → return 1 (expect 1). `causal: new rule R2 IF s0==123 AND a==789 THEN s1:=20` — multi-digit values exact.
- F6c `handle_caus_query(W,"7,8,9")` → return 0, `QCAUS WITHHOLD: no rule fired`. No panic, no PARSE_SHAPE.
- F6d direct `parse_ints("1,0,0",0,5,view12)` → return 0, vals [1,0,0] (control: parser reachable normally).
- F7 informational direct `parse_ints("1,0,0,x",0,7,view12)` → return 1, vals [1,0,0]. The skip is counted per contract (3 values + 1 skipped byte); PARSE_GUARD trace fires verbatim. Not a kill per prereg (contract interpretation, documented).

Zero PARSE_SHAPE traces and zero -1 returns across the whole battery. The -1 branch is unreachable through the handlers exactly as claimed. X-U6-1 FAILS.

### X-U6-2: digit-magnitude gate bypass — SUCCEEDS on the prereg BOUNDARY branch (claim-narrowing)

Theory: `field_kind` has no per-int width limit and `parse_ints` accumulates `v=v*10+digit` with no width bound. A digit-valid segment passes both layers; i32 overflow semantics decide the outcome. The preregistered criteria: panic → DOWNGRADE (contradicts frozen "no panic is possible from the parser"); silent wrap with return 0 and no trace → BOUNDARY (real integrity gap, outside frozen-bar scope, reported as narrowed claim).

Raw (`U6_ADV_MAG_RAW.txt`, md5 `0a2bfb362cda7fa9aa57d749fdf411a8`, 3/3 identical, exit 0 every run — no panic):

- F2: `route_line("2147483648,0,0>1,2;2,0,0>3,4")` → code 2 (CAUS_LEARN, as expected: field_kind counts `2147483648` as one int). `handle_caus_learn(W,"2147483648,0,0>1,2")` →
  `causal: new rule R0 IF s0==-2147483648 AND a==0 THEN s1:=2`
  `ULEARN: 1 stored, 0 corroborated, 0 quarantined, 0 dropped (store full)`
  Return 1. Input 2147483648 (2^31) stored as -2147483648. No PARSE_GUARD, no PARSE_SHAPE, no USHAPE. The parser returned 0 ("clean parse").
- F1: `route_line("99999999999999999999,0,0>1,2;2,0,0>3,4")` → code 2. `handle_caus_learn` on the same line →
  `causal: new rule R1 IF s0==1661992959 AND a==0 THEN s1:=2`
  `causal: new rule R2 IF s0==2 AND a==0 THEN s1:=4`
  `ULEARN: 2 stored, ...` Return 2. Input 99999999999999999999 stored as 1661992959 (mod-2^32 residue). No trace of any kind.
- F3: `handle_caus_learn(W,"123456789012345678901234567890,1,2>3,4")` →
  `causal: new rule R3 IF s0==1312754386 AND a==2 THEN s1:=4`
  Return 1. 30-digit input stored as 1312754386. No trace.
- F1q: `handle_caus_query(W,"99999999999999999999,0,0")` → `QCAUS [99999999999999999999,0,0] -> s0=255 s1=2`, return 1. The query wraps identically, so the corrupted rule fires on the corrupted query: the system is self-consistent but wrong relative to the true input. (s0=255 is the low byte of the wrapped key, per cpredict's `out[0]=s0 as u8`; s1=2 is the predicted effect.)

No panic occurred, so the prereg's DOWNGRADE branch (crash through the defended path) does not fire. But the BOUNDARY branch fires on all three magnitude fixtures: wrapped/truncated i32 values committed with return 0 and zero traces.

Why this narrows the claim rather than merely observing it: the frozen R1 contract states "0 means a clean parse," and the result doc's causal interpretation states "a caller that ignores stdout still learns that bytes were skipped or that the field overflowed the buffer, because the anomaly rides in the return value." For magnitude overflow the caller learns nothing: return 0, no trace, and the stored rule bears a residue of the true input. This is precisely the H1 hazard class R1 was built to close ("a direct white-box caller that ignores stdout could act on split/shifted values" — here, wrapped values). R1 closes H1 for skipped bytes and field-count overflow; digit-magnitude overflow remains unflagged. The "programmatic anomaly flag" claim narrows to those two cases. Per loop precedent (claim-narrowing without bar-break, cf. H-INTENT-UNIFIED4), the verdict is DOWNGRADED, not killed. No frozen bar is broken: K-U6-2's "bad shape" means field-count shape, and the result doc's limitation 1 already concedes the parser is "capacity-safe but not a validator."

A future H-UNIFIED7 repair would be a magnitude check in `parse_ints` (e.g., flag digit runs exceeding 10 digits with a trace and a distinct return code, or saturate loudly). Not attempted here (red-team scope).

### X-U6-3: USHAPE silent loss — FAILS (defense holds)

Raw (`U6_ADV_RAW.txt`, same 3/3-identical runs):
- F4 `handle_caus_learn(W,"1,0,0>2,1;BADSEG;3,3,3>4,4")` → exactly one `USHAPE: segment skipped (expected 3-int>2-int episode) [BADSEG] (H-UNIFIED6)` trace; both good episodes stored (R3, R4); return 2 (expect 2).
- F5 `handle_caus_learn(W,"BAD1;BAD2;NOSEP")` → exactly three USHAPE traces (one per segment, including the missing-separator case via gt<0); return 0 (expect 0); store unchanged.

Every malformed segment is dropped loudly; the return value counts only stored episodes. No silent loss, no accounting mismatch. X-U6-3 FAILS.

### X-U6-4: regression + source audit — FAILS (no finding; holds)

- Rebuilt `unified6_learn.zag` from the committed blob at `ad82aba60` with the pinned toolchain, unmodified. stdout is byte-identical to committed `UNIFIED6_RAW_OUTPUT.txt` (md5 `4d6eee84e8f058cadc544f61a44fddb0`, matches the result doc). 3/3 runs byte-identical.
- `=== RESULT: 20/20 ===` present; every check line ends PASS; no FAIL.
- Frozen lines 2-125: zero PARSE_GUARD, zero PARSE_SHAPE, zero USHAPE (all 14 anomaly-trace lines sit on lines 127+ inside the K-U5-1/K-U6-1/K-U6-2 blocks, as designed).
- Source audit: u5→u6 diff is exactly the frozen change set (parse_ints i32 return + cap check + PARSE_SHAPE; handler field_kind gates + USHAPE branches; K-U6-1/K-U6-2 main blocks; v5→v6 header). `unified5_learn.zag` untouched since `ecd214a1b`. No test-answer literals in the mechanism region (lines 1-1283). Implementation faithful to PREREG_UNIFIED6.md.
- X-U6-4 FAILS (no finding).

## What the verdict means

H-UNIFIED6's mechanism survives: the parser is capacity-safe (no write past `out.len` demonstrated anywhere), the -1 branch is genuinely unreachable through the handlers, every malformed segment is refused loudly with exact accounting, and all 20/20 frozen checks reproduce byte-identically with a clean source audit. What changes is the R1 claim's scope: the programmatic anomaly flag covers skipped non-digit bytes and field-count overflow, but NOT digit-magnitude overflow — inputs like `2147483648` or a 20-digit run wrap silently to mod-2^32 residues, are committed as rules, and report return 0 ("clean parse") with no trace. Any downstream consumer trusting the return value acts on corrupted keys without any signal. That is a narrowed claim, hence DOWNGRADED; it is not a kill because no frozen bar covers magnitude and the store/memory-safety properties all hold.

## Governance disclosures

- Pure Zag throughout; no Python at any stage. No pre-prereg execution of any kind (not even a toolchain semantics probe; the overflow semantics were unknown to the red team until the preregistered F1/F2/F3 runs).
- No binaries or build caches committed (binaries lived in `/tmp/u6adv` only). No em dashes in loop documentation.
- Staging discipline: `git status` inspected before and after `git add`; only the 5 files under `u6_adversary/` staged. Numerous untracked files from concurrent workers left untouched.
- `git merge-base --is-ancestor 029e2abd7 HEAD` verified: prereg strictly precedes all attack artifacts.
- The word "panic" appears once in `U6_ADV_MAG_RAW.txt`: it is the harness banner "(panic-isolated)", not a crash. All runs exited 0.
- Raw evidence: `u6_adversary/U6_ADV_RAW.txt` (md5 `737bf2b78a411de4fe89bd4a314ff990`, 3/3 identical), `u6_adversary/U6_ADV_MAG_RAW.txt` (md5 `0a2bfb362cda7fa9aa57d749fdf411a8`, 3/3 identical).

## Recommended follow-ups for the research director

1. H-UNIFIED7 repair: magnitude validation in `parse_ints` (flag digit runs > 10 digits with a distinct trace + return code, or saturate loudly). The F2 fixture (`2147483648,0,0>1,2` must not commit `s0==-2147483648` silently) is the ready regression test.
2. The paper's H-UNIFIED6 section needs the narrowed R1 claim written in full: "programmatic anomaly flag for skipped bytes and field-count overflow; digit-magnitude overflow wraps silently (known gap)."
3. Consider whether other numeric parsers in the tree (`intent_learn`, `bridge_learn`'s `pextract`, FDCR paths) share the unbounded-accumulator pattern; the wrap is a toolchain-semantics property, not a U6-local bug.

## Files

- Prereg: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/u6_adversary/PREREG_U6_ADV.md` (commit `029e2abd7`)
- Result: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/u6_adversary/U6_ADV_RESULT.md` (this file)
- Harness A (X-U6-1, X-U6-3): `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/u6_adversary/u6_adv.zag` (mechanism cmp-verified byte-identical to committed lines 1-1283)
- Harness B (X-U6-2): `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/u6_adversary/u6_adv_mag.zag`
- Raw: `u6_adversary/U6_ADV_RAW.txt`, `u6_adversary/U6_ADV_MAG_RAW.txt`
