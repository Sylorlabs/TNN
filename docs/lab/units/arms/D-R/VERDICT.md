# VERDICT — Arm D-R (reuse-gated commit), Track A closeout

**Date:** 2026-09-21
**Arm:** D-R — Reuse-gated commit (CUT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PROVISIONAL** — blocked on scale + D comparison (blockers below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> >50% of final vocabulary still uncommitted at end of 10x while D commits and wins on M3 — gating is pure delay.

## Kill-criterion evaluation

**NOT EVALUATED.** The criterion requires 10x evidence from D-R **and**
D's M3 for comparison. Neither exists:

1. D-R cannot complete the 1x battery (blocker A below), so 10x was not
   attempted.
2. D has published no verdict, scorecard, or M3 evidence
   (`units/arms/D/` contains only BUILD_LOG.md and cl/) — the binding
   comparison cannot be performed honestly.

## What was proven (v2 implementation)

1. **Corrected reuse-gate semantics:** fixes the v1 bug where proposals
   never promoted (NCOMMITTED always 0). Pass 1 creates `JUST_SELF`
   proposals at second occurrence; walk references proposals;
   `d_add_occ` promotes at refs≥2; raw unmatched runs stay proposed
   forever (never commit); tiling is exact greedy longest-match (all
   lengths 64..3).
2. **Sub-quadratic proposal structure:** group by 3-byte prefix (radix
   sort, O(n)); sort each group by 64B suffix (radix sort, O(n) total);
   LCP via byte compare; maximal intervals via monotonic stack; 2nd
   smallest via segment tree (G≥128) or scan (G<128). All identity
   decisions memcmp-verified; sort only organizes candidates.
3. **Equivalence on 100KB (binding requirement):** synthetic (102,400B):
   744 proposal events byte-identical to validated Python v5 reference;
   real (102,400B): 99,471 events byte-identical. NCOMMITTED=3 (syn) /
   3481 (real); NOCC=1600 / 18016.
4. **Determinism:** zero RNG in decision paths; two runs byte-identical.

## Blockers (why PROVISIONAL, not PASS)

1. **1x battery BLOCKED — scale panic.** The implementation panics on
   inputs ≥3MB: per-group allocation leaks (hfree is trace-only; ~19K
   groups × per-group buffers exhaust memory). The 5.4MB prose and 9.5MB
   code corpora cannot be processed. This is a resource bug, not a
   correctness bug — the algorithm is sound — but the 1x battery is a
   hard requirement and it cannot complete.
2. **10x NOT ATTEMPTED** (requires 1x pass; also `read_file` caps at
   33.5MB so 54MB/95MB inputs would need streaming).
3. **D comparison BLOCKED** (D has no verdict — see above).

This is **not a PASS** (the battery bar is unmet) and **not a KILL**
(the kill criterion's 10x evidence does not exist). It is PROVISIONAL
with proven 100KB correctness.

## Evidence trail

- Source: `cl/arm.zag` (v2).
- Spec: `docs/ARM_SPEC.md`; build log: `docs/BUILD_LOG.md`.
- Prior verdict draft: `docs/VERDICT.md` (BLOCKED; this verdict concurs,
   quotes the frozen criterion verbatim, and promotes it to the arm
   root per closeout convention).
- 1x battery outputs (partial): `work/battery_1x/` (m1/m2 run logs).

## What would unblock

1. Fix per-group allocation leaks (buffer reuse sized for max observed G,
   or real `nio_free` in hfree); re-run 100KB equivalence for no
   regression; run 1x battery on 5.4MB/9.5MB inputs.
2. Attempt 10x (requires streaming for 54MB/95MB inputs).
3. Re-check D for a verdict, then evaluate the kill criterion
   mechanically (>50% uncommitted at 10x while D commits and wins on M3).

**Result: D-R PROVISIONAL — 100KB-correct, 1x-blocked on scale, kill
criterion unevaluable without 10x + D.**
