# COMP-1 Prereg Amendment (dated 2026-09-30)

## Purpose

This amendment documents a process deviation in the COMP-1 build
(commit `170e39424`) relative to the frozen prereg (commit
`4f6f0c5c8`). It is a separate dated document. It does NOT modify,
retroactively alter, or reinterpret the frozen prereg. The frozen
bound stands as written.

## The deviation

The frozen prereg specifies, in the One-System accounting section:

- "Cognition source lines added: projected at most 150"
- "cognition source lines (bound 150)"
- "Exact count is an implementation measurement; growth past the
  bound without a fresh prereg fails review."
- K1 incorporates "the One-System accounting bound" by reference.

The implementation's fenced bootstrap miss-policy section
(`comp1.zag`, lines 459 through 632) contains 157 non-blank,
non-comment code lines. This is independently verified by shell
count of the committed source and matches the red team measurement
(commit `7ffc2dae4`).

Actual: 157 lines. Bound: 150 lines. Overage: 7 lines (4.7%).

## Materiality

The 7 extra lines sit in `mp_run`'s promotion block. They change no
capability claim, no template count, and no architectural metric.
All frozen predictions P1 through P5 held. All falsifiers F1 through
F7 were addressed. K2 (zero handlers/cases/modes/bridges) and K3
(pure Zag) hold. The deviation is process-level, not scientific.

## What the builder's report said

The BUILD_REPORT (commit `170e39424`) characterizes the 157-line
actual as "a +7 variance on a projection, not a kill-bar failure
(K1/K2/K3 govern the verdict)." The red team records that the
prereg's own language is stronger than that framing: it uses the
word "bound" three times and states that growth past it without a
fresh prereg "fails review." No fresh prereg was written before
implementation. This amendment documents the actual for
transparency; it does not endorse the weaker framing.

## Standing

- The frozen bound of 150 lines is NOT retroactively altered.
- This amendment freezes the 157-line actual as the documented
  implementation measurement, committed before any SURVIVES
  consideration.
- Any SURVIVES promotion decision for COMP-1 must cite this
  amendment alongside the frozen prereg and the red team report.
- Future builder waves should treat prereg "bound" language as a
  hard budget: growth past a bound requires a fresh prereg before
  implementation, per the frozen rule.

## Verification record

- Prereg commit: `4f6f0c5c8` (frozen alone, before implementation).
- Implementation commit: `170e39424` (BUILD-COMPLETE, 10/10 tests,
  3/3 byte-identical).
- Red team commit: `7ffc2dae4` (COMP1-REDTEAM-COMPLETE; process-level
  ATTACK-SUCCESS on this exact deviation).
- Amendment commit: this commit (dated 2026-09-30).
- K1 ordering preserved: this amendment comes after the build and
  red team, and alters no frozen bar.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: zero diff
  verified before and after commit.

## Verdict

COMP1-AMENDMENT-DRAFTED.
