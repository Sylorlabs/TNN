# Amendment 2026-09-27 — A1: K1 kill bar — chance must include a wrong-order baseline

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 1). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

An agent that masters the parts, retrieves them correctly, but applies them
**backwards** — a genuine composition failure — scores 10/48 = 20.8% on the
pilot instrument, above the frozen K1 kill line of 14.2%. As frozen, the
headline kill bar would let a demonstrated composition failure pass as
composition.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §7 "Chance baselines
and KILL BARS (frozen)":

> Baselines: NULL arm (identity output) and SINGLE-RULE arm (applies only the
> first retrieved part). `chance` = max(NULL, SINGLE-RULE) accuracy.
>
> - **K1 — chance kills composition:** combo accuracy ≤ chance + 0.10 →
>   composition claim KILLED (clean negative; this is a finding, not a failure).

## Enacted change

Replace the two quoted paragraphs with:

> Baselines: NULL arm (identity output), SINGLE-RULE arm (applies only the
> first retrieved part), and WRONG-ORDER arm (retrieves the correct parts and
> applies them in the wrong order — masters parts, retrieves correctly,
> composes backwards). `chance` = max(NULL, SINGLE-RULE, WRONG-ORDER) accuracy,
> measured on the actual full-battery instrument.
>
> - **K1 — chance kills composition:** combo accuracy ≤ chance + 0.10 →
>   composition claim KILLED (clean negative; this is a finding, not a failure).

The full battery ships `wrongord` as a permanent reference mode alongside the
other reference agents.

Note on numbers: the pilot instrument (12 pairs × 4 items) measured
wrongord at 10/48 = 20.8%, which would move that instrument's K1 line from
14.2% to 30.8%. The full battery (30 pairs × 4 items, salted generator per
A2) re-measures all three arms on its own instrument; the kill line is
whatever `chance + 0.10` computes to there. The 30.8% figure is the pilot
demonstration, not a frozen number.

## Why

"Composition failure" is exactly what the wrong-order agent does — and the
frozen bar didn't catch it. The bar whose entire job is to kill the
composition claim when composition isn't real must beat every dumb strategy,
including backwards composition.

## Evidence

- `pilot/REDTEAM_REPORT.md`, Family 4, §4a: red-team `wrongord` mode scored
  **10/48 = 20.8% > frozen K1 line 14.2%**.
- Root cause (§4c): parts (1,3)/(3,1) — DUP-FIRST and DROP-LAST — commute on
  all inputs (verified algebraically and 8/8 in the wrongord run), so 8 of 48
  items are free to any order-insensitive strategy; plus 2 length-2
  coincidences where a 1-char intermediate makes order irrelevant.

## Effect

- K1 kills at ≤ chance + 0.10 where chance includes the wrong-order baseline.
- No other kill bar, taxonomy code, or threshold changes.
