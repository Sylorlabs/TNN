# H2-v2 Build Report

**Status:** H2V2-BUILD-COMPLETE.
**Prereg:** FROZEN `84a2a4ddf` (strictly precedes this build).
**Frozen source:** `tnn2.zag` SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
(canonical C160 `cabe77934541571c5313f65af2257d03a74b5bfe`).
**Date:** 2026-10-01.

## What was built

Evaluator binary `h2v2_bin` linking frozen TNN-2 cognition with a
driver-only `main`. Construction:

1. `h2v2_base.zag`: lines 1-1356 of frozen `tnn2.zag` (everything
   before the original `main` at line 1357). SHA-256 of this prefix:
   `701f90bd80339a092814c22c8b3ead9a8349a97d46c3e14840a7e1d866359d0c`,
   verified identical to the frozen source prefix.
2. Lines 1358-1591 of frozen source appended (ACT remediation port,
   test helpers; required because `run_all` references them, though
   `run_all` is never called by the driver).
3. `h2v2_driver.zag` appended: `t2_sig_v2`, world teachers, probe
   runner, calibration, and `main`. The sole `fn main` in the
   assembled file.

The frozen cognition (production paths `ev_query`, `ev_observe`,
`t2_trial`, `t2_try_verify`, `t2_gather`, `t2_exec`, `promote_graph`,
`activate`) is byte-identical to the canonical source. Only `main`
was replaced. No production function was modified.

## t2_sig_v2 (evaluator-side correction, per prereg R1)

`fn t2_sig_v2(W:[]u8, root:i32, sig:[]u8)i32`:

- Walk from `root` following SEQ edges, BRANCHEQ (tag 102)
  true-targets via field 12. Bound 32 cells.
- Per cell, record ONLY the tag: `sig[n*4] = tag`.
- No literal node dereferenced; no payload value enters the signature.
- Traversal order, tag validity rule ({101,102,103,104}), 32-cell
  bound, and edge conventions identical to frozen `t2_sig`.
- Sole change: removal of literal resolution.

This is measurement scaffolding, not cognition. It changes no learner
behavior, promotes no MAP, alters no accept/reject decision.

## TRIAL_ENTERED measurement (per prereg section 5)

Driver protocol per probe:

1. Fresh workspace (`tnn2_init`); teach world facts via `ev_observe`.
2. Assert `hg(W,16) == 0` before the probe query.
3. Call `ev_query(W, s, r_q, expected, flags)` (production path;
   never `mp_run` directly).
4. After return: `tried = hg(W,16) / 1024`.
5. `TRIAL_ENTERED = 1` iff `tried > 0`.

`t2_trial` writes `hs(W,16, tried*1024 + rejected)` on every
invocation (frozen line 664). `tnn2_init` zeroes header 16 (line 909).
No other production path writes it.

## Sealed worlds

Four worlds generated mechanically from prereg normative spec
(sections 10.1-10.4), pre-seal audited (10.5), sealed with SHA-256
in `SEAL_H2V2.md`, permissions `-rw-------`. Hashes verified by the
evaluator before the first probe. Worlds never executed before the
authorized evaluation.

- H2A-v2: `b9fd112edc370e17f34aaa50e9f9405576183ef4c0d2cf6f32b375992549935d`
- H2B-v2-B1: `8e70af8d8278960ec716f0cc899cf1eec953dbcce406f1875e3d3b012cb03c7f`
- H2B-v2-B2: `7d555cfda968a1f5be3b0650ad80104e7f22f6170acda112632a806a047ee831`
- H2C-v2: `91be6c3ad088f950afe97bc3acc101d70f518e31dfca9558d0fb406f6e9988b5`

## Calibration (per prereg section 4)

`t2_sig_v2` verified on frozen-assembled pairs before scoring:

- (i) 2-hop vs 3-hop: DIFFERENT (n=4 vs n=6). PASS.
- (ii) Two 2-hop, different literals: IDENTICAL (n=4, bytes equal). PASS.
- (iii) Chain vs sum: DIFFERENT (n=4 vs n=30). PASS.

Signatures:
- 2-hop: `102-101-102-101`
- 3-hop: `102-101-102-101-102-101`

Calibration passed. Evaluation proceeded to scoring.

## Pinned toolchain

`src/tools/toolchain/znc_linux_x86_64_abed8aa1`. Pure Zag. Safebin
active. Zero Python invocations. Zero em/en dashes in docs
(byte-verified).

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (evaluator only; frozen
  cognition untouched).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (frozen TNN-2 made none;
  see TEST_RESULTS.md).
- COGNITION LINES: 0 (evaluation only; driver is measurement).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
