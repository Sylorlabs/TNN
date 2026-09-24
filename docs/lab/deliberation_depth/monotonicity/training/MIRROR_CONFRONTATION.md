# P/O Mirror Theorem — Explicit Confrontation (H5 Training Wave, CORRECTED)

**Date:** 2026-09-24 (corrected rerun after field-index bugfix)
**Frozen authority:** `deliberation_depth/monotonicity/training/PREREG_TRAINING.md` §7

## What the mirror theorem says (as used by this wave)

The P/O mirror theorem constrains **release and correctness**: for the
fixed release skeleton (release iff the depth-t leader equals the depth-1
leader), P-family and O-family correctness are complementary mirrors —
wherever both release, exactly one side's answer pattern holds, and no
admissible mechanism can break that complementarity by changing *when*
it releases. Its later prediction — "no admissible mechanism meets all
SHIP gates" — was stated over release/correctness behavior, **not** over
confidence calibration.

## What training could and could not touch

- **MT-CONF (10×/100×)** reuses M4's release skeleton verbatim: release iff
  `L_t == L_1`, identical correctness on every cell (proven: 5240/5240
  cells identical to M4 at both scales). Training touched **only** the
  confidence mapping. It cannot break — or confirm — any part of the
  mirror theorem that reasons about release/correctness.
- **MT-FULL** adds a learned abstention gate, but the gate is a **strict
  subset operator**: every MT-FULL release is an M4 release with identical
  correctness (0 subset violations over 5240 cells; 1222 abstentions).
  Abstaining a subset of releases cannot create a release the skeleton
  forbids, so the mirror complementarity is preserved on every cell
  MT-FULL releases. Wherever P and O both release under MT-FULL, they
  release exactly M4's cells, and the mirrored correctness stands.

## Confrontation result (corrected numbers)

1. **The mirror theorem's release/correctness reasoning is untouched.**
   P/O mirrored correctness remains complementary wherever both release —
   verified cell-for-cell against M4. Training had no path to challenge it,
   and did not.

2. **The confidence-calibration challenge failed for H-0** (the dimension
   the mirror theorem did not constrain): the confidence head collapsed to
   a degenerate zero (mean released confidence 0 < 0.05 guard) instead of
   learning depth-conditional calibration, and strict G-rises persisted on
   redteam at both scales. H is falsified under the strict reading and
   unsupported under the refined reading.

3. **The gate challenge is the interesting one.** MT-FULL — with correct
   features — meets the *letter* of every preregistered bar: 0
   transitions, 0 V1/V2, 0 strict G-rises, §1 unbroken, and the redteam
   SHIP-(v) frontier moves 0.500→0.833 released-accuracy. Does this
   overturn the mirror theorem's "no admissible mechanism meets all SHIP
   gates" prediction? **Not honestly:**
   - The V1/V2 bars are passed **trivially**: conf≡0 makes
     conf-rising-while-wrong arithmetically impossible. That is the
     degenerate head doing the work, not the gate.
   - The gate's G-rise elimination works by **selective abstention**
     (1222/5240 cells, 23%), including correct cells it was never asked
     to sacrifice (all cost releases at d4+, D-family broadly). A bar
     that can be cleared by answering less is a bar that does not measure
     what its name claims.
   - The **trap frontier — the adversarial core of SHIP-(v) — is
     completely untouched** (0.000, still below the 0.386 M0 floor; the
     gate abstained zero trap cells beyond M4's skeleton), and redteam
     remains below its 1.000 floor (0.833).

   A mechanism that meets the gates by going silent and abstaining a
   quarter of its releases — while the hardest adversarial family does
   not move at all — is degenerate compliance, not a counterexample to
   the prediction's intent. The prediction stands in spirit; the wave's
   real finding is about the **bars themselves**: as preregistered, they
   do not rule out degenerate compliance, and any future "meets all SHIP
   gates" claim needs an anti-degeneracy clause on the gate (e.g. a
   release-rate floor) as well as on the confidence head.

## Honest statement

This experiment tested whether *training* could succeed where *mechanism
design* (M0–M7) failed. On H-0 (Micah's hypothesis): no — the
preregistered loss has no gradient path to calibration; the head learns
silence and the G-rise signature survives on redteam. On the secondary
gate question: partially — a margin-keyed abstention gate clears every
preregistered bar literally and moves the redteam frontier, but it does
so partly by abstention volume, leaves trap untouched, and inherits a
degenerate confidence head. Neither result breaks the P/O mirror
theorem; the gate result exposes that the bars, as written, admit
degenerate compliance — a finding for the next prereg, not a victory
for this one.
