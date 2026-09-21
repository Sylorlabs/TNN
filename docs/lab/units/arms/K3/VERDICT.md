# VERDICT — Arm K3 (content+position hybrid), Track A closeout

**Date:** 2026-09-21
**Arm:** K3 — Content+position hybrid (IDENT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PROVISIONAL** — blocked on performance + missing bake-off metrics (blockers below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Hybrid-promotion rule: if K3 beats both pure schemes on ≥3 of the 5 bake-off metrics → both pure schemes demoted to components and K3 becomes the identity substrate. (If K3 loses the bake-off, it dies as a candidate.)

## What was proven

- **Builds and runs correctly:** native binary builds (203KB), pure Zag,
  zero RNG; `m5-1x-baseline` completes with correct output; metrics-v1
  JSON emission format correct.
- **Mechanism as specified:** position IDs `(corpus << 24) | index`
  (eternal, never reused); content IDs SHA-256 per 64-byte chunk,
  deduplicated; revision re-points position → new payload with
  `OP_REVISE_LINK`.
- **Determinism:** zero RNG; allocation tracing ensures deterministic layout.

## Blockers (why PROVISIONAL, not adjudicated on the bake-off)

1. **1x battery incomplete — SHA-256 cost.** The design mandates SHA-256
   for every 64-byte unit; the pure-Zag substrate SHA-256 costs ~10–50ms
   per hash. Measured: m1-1x-prose (84,731 units) did not complete in
   6+ minutes; m2-1x (112,556 units) did not complete in 2+ minutes.
   Estimated full 1x battery (18 modes × 2 runs): 15+ hours. This is an
   honest engineering cost of content-addressing, not a correctness bug
   (hash-table load factor and 32MB `nio_alloc` issues were found and
   fixed along the way; they do not resolve the per-hash cost).
2. **Bake-off metrics unavailable.** The kill rule needs 5 bake-off
   metrics for K3 vs K1 vs L1. K3's 1x battery is incomplete (blocker 1);
   sibling K1/L1 bake-off results are not available to this crew.

This is **not** a bake-off loss — it is an inability to evaluate. Killing
K3 on performance grounds would be a new kill criterion requiring Micah's
re-approval (per program law: rule changes need re-approval).

## M1–M9 1x row (from `docs/lab/units/arms/K3/VERDICT.md`)

| Mode | Status |
|------|--------|
| M1 | ATTEMPTED — FAILED (84k units; SHA-256 too slow; 6+ min no completion) |
| M2 | ATTEMPTED — FAILED (112k units; 2+ min no completion) |
| M3/M4/M6/M8 | NOT ATTEMPTED (blocked by M1/M2 performance) |
| M5 | PASS (baseline only — empty store; full M5 not attempted) |
| M7 | NOT ATTEMPTED (blocked; also A7/A8 unfrozen) |
| 10x | NOT ATTEMPTED (1x incomplete) |

## Ambiguities (carried)

A15 provisional (64-remap ID-swap schedule; scorecard marked
PROVISIONAL-PENDING-FREEZE); A7/A8 (M7 edit/lookup schedules unfrozen);
A17 (M8 provisional combined M1+M3 interpretation).

## Evidence trail

- Source: `cl/arm.zag` (1,456 lines).
- Prior verdict draft: `docs/lab/units/arms/K3/VERDICT.md` (INCOMPLETE —
  performance blocker; this verdict concurs and promotes it to the
  closeout taxonomy).
- Scorecard: `docs/lab/units/arms/K3/scorecard.json` (schema
  `scorecard-v1`); canonical metrics-v1 scorecard written alongside this
  verdict as `scorecard_r1_1x.json`.
- Spec/build: `docs/lab/units/arms/K3/ARM_SPEC.md`,
  `docs/lab/units/arms/K3/BUILD_LOG.md`.

## What would unblock

(a) Performance: native SHA-256 (violates pure-Zag constraint), lazy
content hashing (design change), or a coordinator-granted performance
exemption measuring identity metrics not speed; (b) K1/L1 bake-off
metrics for the 5-metric comparison; then re-adjudicate the
hybrid-promotion rule mechanically.

**Result: K3 PROVISIONAL — builds and runs correctly; bake-off
unresolved (performance blocker + missing sibling metrics).**
