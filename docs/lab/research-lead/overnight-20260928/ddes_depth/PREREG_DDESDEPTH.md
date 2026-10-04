# PREREG: DDES Sealed Depth Test (L>=8)

Frozen before any implementation or test execution. This prereg commits
the sealed world design and the kill bars. Any amendment must be
committed transparently and re-frozen before implementation; no bar may
be altered after seeing results.

## Context

DDES Promotion Assessment (b75886067) found DO NOT PROMOTE. Remaining
work item 1 in information order: sealed L>=8 depth run on the repaired
binary (deferred K-NX3 sub-bar from PREREG_DDES.md).

K-NX3 requires: after freeze, the adversary supplies a world requiring
L actions with L >= 8, where L exceeds every length constant in source
(there must be none). The learner must converge with exactly 1 real
execution.

Target: repaired DDES (ddesr.zag, REPAIR-PASS 17c97a2cd). The repair
added eff_waits(t*) = max(t*, 1). For t* >= 1 behavior is identical to
the frozen BUILD-PASS binary.

## Sealed World G (designed now, frozen here)

The DDES author never saw these delays. Frozen worlds use delays
0,1,2,3,4,5,7. World G uses 9 and 8.

H0 = [(X,Z,9),(Z,Y,0)]
H1 = [(X,Y,8)]

Variables: X=0, Z=1, Y=2.

Analytic derivation (frozen expectation):
- H0 arrivals: X=0, Z=9, Y=9.
- H1 arrivals: X=0, Z=INF, Y=8.
- Frontier: Y differs (9 vs 8). Earliest t* = min(9,8) = 8.
- Target: (V*=2, t*=8), schema=1 (set-X).
- Plan: [S] then 8x[W] then [OY]. Length 10. L=10 >= 8.

Both truth configs are tested (truth=H0 and truth=H1).

Frozen expectations per config:
- cfg0 (truth=H0): TARGET V*=2 t*=8. PLAN [S,W,W,W,W,W,W,W,W,OY].
  EXEC real=0 (Y arrives at t=9; observation after 8 waits sees 0).
  PRED h0=0 (9<=8 false), h1=1 (8<=8 true).
  SURVIVE h0, ELIM h1, CONVERGE-OK.
- cfg1 (truth=H1): TARGET V*=2 t*=8. PLAN [S,W,W,W,W,W,W,W,W,OY].
  EXEC real=1 (Y arrives at t=8).
  PRED h0=0, h1=1.
  ELIM h0, SURVIVE h1, CONVERGE-OK.

## Method (frozen)

A new Zag file reuses the DDES driver functions verbatim from the
frozen ddesr.zag (compute_arrivals, compute_frontier, eff_waits,
synthesize_plan, predict, world_step, ddes_world, plus the packed
world block helpers). Only a new load_world_G and a new main() running
World G both configs are added. No logic changes. This mirrors the
adversary precedent (killer.zag reused frozen DDES functions verbatim).

The new file is compiled with znc and run 3 times. Byte-identical
outputs required.

## Kill bars (all must pass)

- K1 (sealed): this prereg is committed alone before any test code
  exists. The delays 9 and 8 appear in no frozen DDES source file.
  Verified by grep over ddes/ and ddes_repair/ before implementation.
  Kill: any evidence the world was visible to the DDES author, or
  prereg not strictly preceding implementation (verified via
  git merge-base --is-ancestor).
- K2 (depth convergence): both configs CONVERGE-OK. Each config
  assembles exactly 1 plan (plans_built increments by exactly 1 per
  config). Plan length is exactly 10 actions (>= 8). Exactly 1 real
  execution per config (the driver performs one execution; no retry).
  The surviving hypothesis matches truth on both configs.
  Kill: CONVERGE-FAIL on either config, plan length < 8, more than 1
  plan assembled per config, or wrong survivor.
- K3 (purity): pure Zag, zero Python at any stage (source, build,
  execution, analysis). Zero em-dash bytes in all committed files
  (byte-checked with grep -P). Kill: any Python invocation or any
  em-dash byte.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
