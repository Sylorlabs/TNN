# Amendment 2026-09-27 — A5: Documented limitations (no bar change)

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 5). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

Nothing about construction, bars, or verdicts. Three things the red team
proved are real but aren't instrument defects get written into the record so
future readers — and future batteries — don't trip over them.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §3 P4:

> - **P4 — interference analysis:** per ordered-pair accuracy table.
>   Systematic order asymmetry (pair (i,j) ≤0.25 while (j,i) ≥0.75, parts
>   mastered in isolation) → (d).

The frozen prereg says nothing about commuting pairs, length-2 soft items, or
input-conditional interference.

## Enacted change

The following "Documented limitations" paragraph is annexed to the prereg
(placement editorial — with §7 or as an annex; the text below is the
substance). **No kill bar, taxonomy code, or threshold changes.**

> **Documented limitations (no bar change).**
>
> 1. *Commuting pairs.* Parts (1,3) and (3,1) — DUP-FIRST and DROP-LAST —
>    commute on all inputs: their compositions are order-insensitive by
>    construction, so 8 of the 48 pilot P2 items cannot test order
>    sensitivity (see also A1, which sets the chance floor for exactly this
>    reason). The full battery must verify that the added parts P5/P6 do not
>    commute with each other or with P1–P4, and must document the commuting
>    fraction of its item set.
> 2. *Length-2 soft items.* 4 pilot P2 items are freebies to multiple dumb
>    strategies (identity, first-rule-only, first-character heuristics)
>    because on length-2 inputs several strategies coincide. Intrinsic to
>    short inputs; recorded as a limitation, not a fix. The full battery
>    documents its own soft-item count.
> 3. *P4's asymmetry criterion is pair-systematic.* The 0.25/0.75 criterion
>    detects only pair-systematic interference. Demonstrated: an agent that
>    interferes only when DUP-FIRST is second AND the input is length 2
>    scores 3/4 on three pairs vs 4/4 reversed — a genuine order-asymmetric
>    defect — yet all its items stay (c) because 3/4 fails the criterion.
>    The full battery either narrows (d)'s definition explicitly to
>    pair-systematic asymmetry (making such cases (c) by definition and
>    documenting it), or adds a per-condition breakdown of P4 results. The
>    builder picks one and records the pick in the battery report.

**The point-3 fork (the proposal's deliberate ambiguity, kept open as
signed).** Micah signed A5 with this fork explicit: the builder chooses
between narrowing (d) or adding the per-condition breakdown, and records the
choice. The signature approves documenting the limitation with the fork —
it does not pick a side.

## Why

- If nobody writes down that 8 items can't test order, the wrong-order
  baseline in A1 looks like a surprise instead of a construction property —
  and a future 3-hop battery could quietly inherit commuting pairs as
  "hard" items.
- The length-2 freebies inflate every dumb baseline slightly; recording them
  keeps the baseline table honest.
- The P4 criterion's blindness to input-conditional interference is
  deliberate (the threshold avoids false positives), but "deliberate" has to
  be written down, or the next conditional-interference defect gets misfiled
  as plain (c) with no one noticing the instrument was blind to it.

## Evidence

- `pilot/REDTEAM_REPORT.md`, §4c: pairs (1,3)/(3,1) "commute on all inputs
  (DUPFIRST∘DROPLAST = DROPLAST∘DUPFIRST, verified algebraically and 8/8 in
  the wrongord run) → 8 free items for any order-insensitive strategy."
- §5b: "Consider noting the weight or verifying P5/P6 (full battery) don't
  commute." §5c: "4 items are freebies to multiple dumb strategies
  (identity, pi-only, pi-twice, first-char). Intrinsic to short inputs; note
  as a limitation rather than fix."
- §3c: `interf2` mode — corrupt only when DUPFIRST is second AND input
  length is 2: pairs (0,1),(2,1),(3,1) score 3/4 vs 4/4 reversed, "a genuine
  order-asymmetric defect — but `ca=3 > 1` fails the criterion, so all 9
  items stay **(c)** instead of **(d)**." Recommended fix #6.

## Effect

- Future battery reports must cite these three limitations where relevant
  (commuting fraction, soft-item count, P4's pair-systematic scope), and the
  full battery must check P5/P6 for commutation.
- No bar, threshold, or taxonomy change.
