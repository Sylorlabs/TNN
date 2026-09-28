# §13 nested-N stress cell — diagnostic execution (2026-09-25)

**Prereg:** `PREREG_STRENGTH_V2.md` §13 (preregistered optional stress
cell; runs after the main verdict by dated note, no re-approval required).
**Formula:** `wrong(m,v) = 1` iff `(3m + 7v + 9) mod 10 < 2` — every wrong
memory is also important (100 strong mistakes/variant; the maximum-harshness
world). **Scope:** arms C and C-P3 at S1 only (the killed hybrid arms).
**Status:** diagnostic, not promotional.

## Method

Scratch copy of the frozen trial sources; the single-line wrongness
closed form swapped in `strength_learner.zag` (`lr_wrong`) and
`strength_checker.zag` (`ck_wrong`) — the checker is compiled into the
trial binary via `@import`, so it re-derives under the same formula.
Rebuilt with the pinned toolchain; ran C/C-P3 × VUP/WBS/JI × variants 0–2
× 2 runs (36 cells). Frozen sources untouched.

## Integrity

All 36 cells: exit 0, `ST_DONE`, `ST_INVALID 0`, r1/r2 byte-identical,
independent checker 0 failures.

## Results (all variants identical within arm)

| arm | curriculum | drops | key metric |
|---|---|---|---|
| C | VUP | 470 | retention 9/9 (degenerate — only 9 important admitted) |
| C | WBS | 446 | R_wbs 24/24 = 100% (rigidity holds) |
| C | JI | — | implants 1/1 rejected; junk 21/21 = 100% retained |
| C-P3 | VUP | 470 | retention 9/9 (identical to C) |
| C-P3 | WBS | 446 | R_wbs 24/24 = 100% |
| C-P3 | JI | — | implants 1/1; junk 21/21 = 100% |

Compare the main trial (independent I): C VUP drops 470, WBS drops 434 /
R_wbs 36/36 = 100%, JI junk 100%.

## Reading

1. **The harshness world does not rescue the hybrid.** Under nested — 2×
   the strong-mistake load, every wrong memory important-looking — C and
   C-P3 freeze with the identical signature (470 VUP drops, ~3824
   abandons, degenerate 9/9 retention). The freeze is structural (graded
   protection with no citation source), not a function of the wrong-rate.
2. **Rigidity is not the failure mode.** R_wbs = 100% under both formulas.
   The hybrid revises what it admits; it just admits almost nothing and
   drops everything else.
3. **P3 still has zero effect under harshness.** C-P3 ≡ C on every metric,
   as in the main trial.
4. The denominator shift in ST_METRIC 2 (36 → 24) reflects fewer wrong
   memories reaching strong-mistake status under the frozen store, not a
   rigidity change — both are 100%.

## Disposition

Diagnostic complete per §13. No verdict change: C and C-P3 remain killed
at S1 under both wrongness formulas. The nested formula stays rejected as
the default (rigged world) and adopted only as this diagnostic.
