# PREREG AMENDMENT A1 (pre-execution, one document, no numeric bar relaxed)

Filed under PREREG section 9 ("one pre-execution amendment ... only for an internal
inconsistency in this document, committed alone, and no numeric bar may be relaxed").
Committed alone, before any `.zag` exists in this lane. No run has occurred.

## The inconsistency

PREREG section 5, "Predicted utilities", case 2 reads:

> case 2: D `255-32=223` vs I `255-32=223` (**predicted TIE**, broken to DERIVE by
> lower cost 3 vs 4) vs P `199`.

Two statements in the same clause cannot both hold. `255-32` is `W_COST*cost = 32`,
i.e. `cost = 4` for **both** D and I; but the tie is then said to be "broken by lower
cost 3 vs 4", which requires `cost(D) = 3`. `cost = 3` and `cost = 4` cannot both be
the cost of D.

PREREG section 4 resolves it unambiguously and is not amended:

> DERIVE | closure record count + 1 result alloc

Fixture 2 stores one DER record `(1,30,5)` supported by two OBS leaves
`(1,10,3)` and `(3,10,5)`. The DER record is the **conclusion**, not a member of the
closure that proves it. Closure record count `= 2`. Therefore `cost(D) = 2 + 1 = 3`.
`cost(I) = probe cost 3 + 1 = 4`.

## The corrected arithmetic (case 2 only)

| quantity | was | is |
|---|---|---|
| `cost(DERIVE)` | 4 | 3 |
| `utility(DERIVE)` | 223 | `255-24 = 231` |
| `utility(INQUIRE)` | 223 | 223 (unchanged) |
| tie D vs I? | predicted | **no tie**; DERIVE leads by 8 = exactly one cost step |

## What is NOT changed

- **No kill bar is relaxed, added, removed or reworded.** K-CHOICES still demands
  case 2 `== DERIVE`.
- **No predicted choice changes.** DERIVE was the predicted choice for case 2 under
  both readings (strict win at 231 vs 223, or tie-break win at cost 3 vs 4).
- Sections 1-4 and 6-8 are untouched.
- PREREG section 7's `PO_ABL_NOPRICE` prediction ("ties everywhere go to PREDICT
  (scanned first)") is **NOT amended**. It is falsifiable against section 4's frozen
  scan order (`RETRIEVE, DERIVE, CONSTRAIN, INQUIRE, CONSTRUCT, PREDICT` -- PREDICT is
  scanned LAST) and is therefore a *prediction about the world*, not an internal
  inconsistency. It is retained verbatim and will be reported as FALSIFIED or
  CONFIRMED as executed. Same for `PO_ABL_PRIORWILD`'s "PREDICT wins 5 of 6".
- PREREG section 6 K-PRIOR-ADVERSARIAL's clause "PREDICT must stop winning case 6" is
  **NOT amended** even though the main table never has PREDICT winning case 6 (CONSTRUCT
  does). It is retained verbatim; the vacuity of that clause is reported, not fixed.

## Consequence for the report

Case 2's margin is now **one cost step (8 points)** on a 255 scale. That is reported
as a boundary, in addition to the near-tie the prereg already flagged.