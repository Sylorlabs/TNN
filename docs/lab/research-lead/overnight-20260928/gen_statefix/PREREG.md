# PREREG: GEN-STATEFIX (follow-up to GEN-SUBSUMES-U C397)

Date: 2026-10-03. Worker: GEN-STATEFIX.
Lane: `docs/lab/research-lead/overnight-20260928/gen_statefix/`
Branch: `lane-genstatefix-20261003` (isolated; explicit pathspecs only).

## 1. Question

GEN-SUBSUMES-U (verdict PARTIAL, boundary characterized) found that GEN
reproduces U's 5 pipeline pairs + diamond, but fails P5 (sequential contract
growth): `gen_solve` resets tries/found/ans/pool/widened but NOT the
per-query tried1/tried2 tables (keyed by pool index). The census proved
representation-level contract growth is intact; the defect is trial-state
scoping only.

This lane lands the specified fix: reset the tried1 (2304..3328) and tried2
(count at 3328) regions in `gen_solve` alongside the existing resets, then
rerun the 5 pipeline pairs + diamond + P5 sequential growth. Frozen
predictions: P5 now passes (ANS=3, no widening), all prior GEN results
unchanged. If that holds, the verdict upgrades to SUBSUMES and U is retired.

## 2. The fix (specified before implementation)

In `gen_solve`, immediately after the existing resets, insert exactly this
hunk. It is the ONLY source change relative to `gsu_gen.zag` (equivalently,
to `d6_gen.zag` lines 1-239):

```
  // GEN-STATEFIX: per-query tried-state scoping. Clear tried1 (2304..3328)
  // and tried2 (count at 3328) so a later query on the same arena
  // re-enumerates the trial space. Contract-growth state lives in the
  // census-visible masks, not in these tables.
  let zti:i32=0;
  while(zti<256){
    set32(A,2304+zti*4,0);
    zti=zti+1;
  }
  set32(A,3328,0);
```

Rationale: tried1 is 4 maps x 64 pool indices x 4 bytes = 1024 bytes
(256 i32 cells) at 2304..3328; tried2 entries are governed by the count at
3328, so resetting the count suffices. The done set (3660) is re-zeroed by
every `gen_record` call and the visit stack (3596) is locally indexed, so
they need no reset. No other line of the composer changes: no redesign, no
new mechanism, no new opcode.

## 3. Build plan (implementation follows this prereg commit)

`gsf_gen.zag`: `d6_gen.zag` lines 1-239 plus the Sec 2 hunk (main at line
240 excluded).

Assembly `gsf_full_gsu.zag` (the 9-arm subsumes battery, pure concatenation):
1. Lines 1-301: byte-verbatim copy of `d6_base.zag` (canonical GEN base).
2. Next: `gsf_gen.zag` (fixed composer).
3. Next: byte-verbatim copy of `gsu_world.zag` (pair5 world region).
4. Next: byte-verbatim copy of `gsu_main.zag` (9-arm driver; the only arm
   exercising multi-query arena reuse is P5).

Assembly `gsf_full_diamond.zag` (the diamond battery, pure concatenation):
1. Lines 1-301: byte-verbatim copy of `d6_base.zag`.
2. Next: `gsf_gen.zag` (same fixed composer).
3. Next: byte-verbatim copy of `d6_gen.zag` lines 240-270 (diamond world +
   gen main: P1, P2a, P2b, P3, Q1 diamond, census, Q2).

Build: pinned safebin znc (2026.07.0-dev). Run each binary 3x.

## 4. Arms and frozen predictions

Battery A (gsu rerun): the 9 arms of GEN-SUBSUMES-U. Predicted stdout is
`gsu_run1.txt` with the P5 block replaced by:

```
INTER=52
INTER=-2
INTER=51
INTER=1
INTER=53
INTER=-2
INTER=52
INTER=1
INTER=-2
INTER=3
ARM=GEN PROB=P5 ANS=3 TRIES=10
```

Derivation (frozen, from the fixed sources): P2b leaves m0 inmask=1
outmask=3 (census). P5 query (51,1,2,3,4) on the same arena. Round 1
pool=[51], all arity-1 cells admitted (kind(51)=1 in inmask=1): (0,0)
WALK(51,81)=52 added; (1,0) COUNT(51,82)=-2; (2,0) IDENT(51)=51 already in
pool; (3,0) COUNT(51,81)=1 added. TRIES=4. Round 2 pool=[51,52,1], (m,0)
skipped as tried: (0,1) WALK(52,81)=53 added; (1,1) COUNT(52,82)=-2; (2,1)
IDENT(52)=52 exists; (3,1) COUNT(52,81)=1 exists. TRIES=8. Round 3
pool=[51,52,1,53]: (m,2) cells rejected (kind(1)=2 not in inmask=1);
(0,3) WALK(53,81)=-2; (1,3) COUNT(53,82)=3=exp SUCCESS. TRIES=10. No quiet
round occurs, so no WIDEN=1 fires.

All other Battery A blocks (P1, P2a, P2b, census, P3, Q1, Q2, Q3, Q4) are
predicted BYTE-IDENTICAL to `gsu_run1.txt` (single queries on fresh arenas;
the reset is a no-op on already-zero tables).

Battery B (diamond rerun): P1, P2a, P2b, P3, Q1 (diamond), census, Q2, all
single queries on fresh arenas. Predicted stdout BYTE-IDENTICAL to
`g1_run1.txt`.

## 5. Kill bars

- K1 GROWTH FIXED: Battery A P5 block reads `ARM=GEN PROB=P5 ANS=3` with no
  WIDEN=1 line. (TRIES predicted 10 by the Sec 4 derivation; reported
  honestly if it differs; a TRIES miss does not fail K1.)
- K2 NO REGRESSION (subsumes battery): every other Battery A stdout block
  byte-identical to `gsu_run1.txt`; stderr empty.
- K3 NO REGRESSION (diamond battery): Battery B stdout byte-identical to
  `g1_run1.txt`; stderr empty.
- K4 DETERMINISM: 3/3 runs byte-identical per battery (sha256 recorded);
  stderr empty.
- K5 FIDELITY: (a) `gsf_base.zag` diff empty vs `d6_base.zag`;
  `gsf_world.zag` diff empty vs `gsu_world.zag`; `gsf_main.zag` diff empty
  vs `gsu_main.zag`; (b) every assembled region diffs empty against its
  reference; (c) `gsf_gen.zag` diff vs `gsu_gen.zag` shows ONLY the Sec 2
  hunk.
- K6 TOOLCHAIN: safebin active for every command; `which python3` and
  `which python` return nothing; zero forbidden-executable invocations;
  pure Zag; shell only for znc/binary/git/assembly/byte-verification.
- K7 HYGIENE: zero em/en dash bytes in all lane docs (byte-verified).

On TRIES: equality with U's P5 (TRIES=4) is NOT required and NOT a kill
bar (precedent: GEN-SUBSUMES-U PREREG Sec 5).

## 6. Verdict mapping (frozen)

- K1-K7 all PASS: UPGRADE-TO-SUBSUMES. GEN reproduces U's 5 pipeline
  pairs, honest failures, fresh learning, the diamond, AND sequential
  contract growth on one arena. Recommend retiring U as a separate
  mechanism; U becomes the documented restriction of GEN (single-round
  linear pool, predicted handshake, stateless trial enumeration).
- K1 FAIL (P5 not ANS=3): the fix analysis is wrong; document the actual
  P5 behavior and the mechanism cause. Verdict stays PARTIAL.
- K2 or K3 FAIL (any other block diverges): the fix introduced a
  regression; document it; NOT-SUBSUMES pending a redesign.

## 7. What this establishes (and does not)

Establishes: whether the tried-state scoping defect was the sole cause of
GEN's P5 failure, and whether the reset preserves every prior GEN result.

Does not establish: try-efficiency parity (explicitly out of scope);
behavior on non-pipeline shapes beyond the diamond; the side-effecting-MAP
open question (all MAPs here are pure); multi-query reuse beyond one
sequential growth step.

## 8. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0 guard),
`gsf_base.zag`, `gsf_gen.zag` (fixed composer), `gsf_world.zag`,
`gsf_main.zag`, `gsf_full_gsu.zag`, `gsf_full_diamond.zag`, `gsf_bin_gsu`,
`gsf_bin_diamond`, `gsf_gsu_run1/2/3.txt` (+ `.err`), 
`gsf_diamond_run1/2/3.txt` (+ `.err`), REPORT.md.

Opaque identifiers: all entity/relation identifiers are opaque integers.
World-builder comments inherited verbatim from the frozen sources may
contain domain words; they are copied for byte-fidelity and are not this
experiment's design language.
