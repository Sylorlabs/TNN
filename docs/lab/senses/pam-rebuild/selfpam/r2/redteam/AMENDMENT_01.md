# ATTACK PREREG AMENDMENT 01 — SS surface-similarity operationalization

Date: 2026-09-23. Amends `ATTACK_PREREG.md` (frozen 2026-09-23, commit
`11e8015a340a9bc0c053833a26540b02e942c3b3`). Committed alone before any
validator or attack run, per the prereg's own amendment rule.

## What changes

The prereg's battery-validity checklist specified "SS token overlap ≥90%"
for the C-PARA-SS (same-surface, meaning-divergent) pairs. That figure is
hereby REPLACED by the following operational check:

> **SS surface check:** token-level edit distance ≤ 3 between the two
> members of every C-PARA-SS pair (tokens = whitespace-split,
> lowercased, trailing punctuation stripped; substitution/insertion/
> deletion each cost 1). Rationale: a "same-surface" pair is one
> differing by a single localized edit. The maximum in this battery is
> exactly 3, attained only by E_NEG (do-support negation: one verb-form
> substitution + two insertions, e.g. "sat" → "did not sit", all inside
> the verb cluster).

The Dice token-overlap distribution is still computed and reported for
the record, but it is NOT a pass/fail bar.

## Why the 90% figure was wrong

The 90% number was written without computing what single-edit transforms
score on the battery's sentence lengths (4–8 tokens). Measured on the
frozen C-PARA-SS set (150 pairs, built 2026-09-23 by the deterministic
`build_para` harness):

- token edit distance: 95 pairs at 1, 19 at 2, 36 at 3 (all E_NEG) — max 3
- Dice overlap: range 0.667–0.889, mean ≈ 0.78

A single substituted token in a 6-token sentence caps Dice at ≈0.83; the
90% bar is unachievable for ANY genuine same-surface pair at this
sentence length. The corpus is correct (every pair is one localized
edit); the threshold was miscalibrated. This amendment fixes the
operationalization while preserving the check's intent: catching pairs
whose surfaces accidentally diverged (a broken transform emitting
unrelated text would score edit distance ≥ 4 and be caught).

## What does NOT change

- All M1–M7 kill bars and W-specific bars: unchanged.
- All corpus counts: unchanged.
- The THEATER signature (pass M1–M3, fail M4/M5): unchanged.
- No fork has been attacked; no validator has been run. This amendment
  precedes all runs.
