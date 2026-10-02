# Dated Amendment — Ruling 1: wrong-memory formula (independent I adopted)

**Date:** 2026-09-25. **Prereg:** `PREREG_STRENGTH_V2.md` (frozen 2026-09-20),
§4.1 / amendment-log entry 1.
**Status: RECOMMENDED — requires Micah's re-approval at adoption.**
(Micah's "run it" order of 2026-09-25 authorizes execution under this formula;
it does not constitute the adoption sign-off.)

## Background

The original strength-trial prereg specified `wrong(m,v) = 1` iff
`(5m + 11v + 7) mod 10 < 2`, intending ~20% wrong memories. Two independent
passes verified this formula yields **identically zero** wrong memories
(0/500 per variant) — the trial's first run was declared invalid on this
among other defects (2026-09-20). Per Micah's standing rule (when in doubt,
test both), wave-7 ran a preregistered formula comparison
(`wave7/formula-test-both/`, `PREREG_COMPARE.md` frozen before computation,
`FORMULA_COMPARE.md` results) between:

- **Version N (nested):** `wrong(m,v) = 1` iff `(3m + 7v + 9) mod 10 < 2` —
  every wrong memory is also important (100 strong mistakes/variant;
  P(wrong|important) = 0.667; base rate 0.20).
- **Version I (independent):** `wrong(m,v) = 1` iff `(m + 3) mod 10 < 3`,
  i.e. `m mod 10 ∈ {7,8,9}` — wrongness independent of importance
  (50 strong mistakes/variant; P(wrong|important) = 0.333 = base rate 0.30).

## The evidence (test-both)

| measure (per variant, S1, H=500) | N | I |
|---|---|---|
| wrong memories (yield) | 100 | 150 |
| wrong AND important (rigidity denominator) | 100 | 50 |
| right AND important (F_wbs denominator) | 50 | 100 |
| P(important \| wrong) | 1.000 | 0.333 |
| P(wrong \| important) | 0.667 | 0.333 |
| P(wrong) base rate | 0.20 | **0.30** |
| pressure-episode overlap | 0 | 0 |
| implant-episode overlap | {166, 416} (v2) | 0 |

Both pass all five preregistered hygiene criteria (C1–C5); neither starves
the test. The wave-7 verdict recommended I: it tests rigidity without
stacking the world, and its numbers are cleaner on every hygiene axis.

## The ruling

**ADOPT version I (independent) as the trial's wrong-memory formula.**
Version N is rejected as the default: it makes 2/3 of important-looking
memories wrong — a rigged world where a rigidity failure is contestable —
and is retained only as the preregistered optional stress cell (§13 of the
V2 prereg): same curricula, same bars, C/C-P3 at S1, runs after the main
verdict by dated note, diagnostic not promotional.

## Disclosed delta (flagged openly, not buried)

The adopted formula runs at a **30% wrong rate vs the original prereg's
20% intent**. The 20% target is unachievable with a clean closed form at
the required hygiene (the 20%-intent formula yields literally zero; the
nested 20% formula forces importance). The 30% rate is disclosed in
PREREG_STRENGTH_V2.md §4.1 and amendment-log entry 1, and repeated here so
no future reader mistakes it for the original intent.

## What this amendment does and does not do

- DOES adopt `(m + 3) mod 10 < 3` as the formula under which the 2026-09-20
  re-trial and the 2026-09-25 verification re-run executed.
- DOES record the 30%-vs-20% delta as a disclosed, dated deviation.
- DOES NOT change any kill bar, curriculum, metric, or verdict rule.
- DOES NOT claim Micah's adoption sign-off — that remains explicitly
  pending, per ruling 1's terms.

## Trial impact statement

All re-trial cells (S1: 27 cells × 2; S10/S100: 18 cells × 2) ran under
version I. The WBS rigidity denominator is 50/variant (vs 100 under N);
all bars were evaluated as preregistered. No verdict changes if the
formula is reverted — but the trial would then test a rigged world, which
is why N was rejected.
