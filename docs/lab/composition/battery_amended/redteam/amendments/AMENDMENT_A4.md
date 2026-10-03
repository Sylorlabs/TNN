# Amendment 2026-09-27 — A4: K6 scope — covered pairs only

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 4). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

K6 (the memorization check) as frozen reads as applying to every pair — but
some pairs have zero bigram-clean P2 inputs (inputs sharing no bigram with
any training input), so the check cannot run on them. Holding those pairs to
an unperformable check would manufacture false "unverifiable" verdicts.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §7 "Chance baselines
and KILL BARS (frozen)":

> - **K6 — memorization check:** red-team must fail to explain combo success
>   via surface memorization (success holds on inputs sharing no bigram with
>   any training input). If it explains it → battery VOID, generator fixed.

## Enacted change

Append to the K6 bullet (scope clarification — the bar's *definition* is
unchanged, its *coverage* is):

> K6 is adjudicated only on ordered pairs whose P2 inputs include
> bigram-clean items (inputs sharing no bigram with any training input).
> Pairs with zero bigram-clean P2 inputs are excluded from K6: the check
> cannot run on them. Their results stand as reported but carry no K6
> verdict. The full battery must compute and document the covered-pair set
> under its own (salted, per A2) generator — the pilot's excluded pairs,
> (1,0) and (3,1), are the motivating instance, not a frozen list.

**Why the covered set is re-computed, not frozen.** The proposal named the
pilot's two uncovered pairs, (1,0) and (3,1), on the pilot's 12-pair
instrument. The full battery runs 6 parts (30 ordered pairs) under the
salted A2 generator, which changes bigram-clean coverage — and the frozen
full-battery run independently found five uncovered pairs on the unsalted
generator: (0,4), (2,0), (3,1), (4,3), (5,4). Freezing the pilot's pair list
would scope K6 to the wrong instrument. The signed principle — *K6 applies
only where it can run* — is enacted; the pair list is a measured property
of the actual battery, documented in its report.

## Evidence

- `pilot/REDTEAM_REPORT.md`, Family 1, §1c — "CLEAR with caveat": "36/48 P2
  inputs share **no** bigram with any training string (inputs + single-rule
  outputs), so the red-team memorization check can run on a large subset.
  Caveat: pairs **(1,0) and (3,1) have zero bigram-clean inputs** — K6 must be
  scoped to the 10 covered pairs or restated."
- D1 full-battery run (frozen prereg, 2026-09-27): 5 of 30 pairs have no
  bigram-clean inputs on the unsalted generator — (0,4), (2,0), (3,1),
  (4,3), (5,4) — confirming the coverage gap is real on the full instrument
  too, and that the excluded set is instrument-dependent.

## Effect

- K6 adjudicated on covered pairs only; uncovered pairs documented, not
  silently dropped.
- If the red team explains success via surface memorization on any covered
  pair, the battery is still VOID and the generator still gets fixed — the
  teeth don't move.
- No other kill bar changes.
