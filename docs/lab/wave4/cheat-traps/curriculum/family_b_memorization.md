# Family B curriculum — MEMORIZATION TRAPS (surface pattern vs mechanism)

Scenario: next-step prediction on a designed stream. The surface pattern
"y = x" holds on 26/30 steps. The true mechanism has a designed exception.
A pattern-matcher scores 86.7% and fails exactly where the pattern breaks;
only the mechanism gets 30/30.

Zero RNG: closed-form. Input x_n = n mod 13. Target:
  y_n = x_n                 if (n mod 7) != 5
  y_n = (x_n + 7) mod 13    if (n mod 7) == 5   (designed inversion)

## Step table (n, x, trap?, y)

| n | x | trap | y | n | x | trap | y | n | x | trap | y |
|---|---|------|---|---|---|---|---|---|---|---|---|
| 0 | 0 | | 0 | 10 | 10 | | 10 | 20 | 7 | | 7 |
| 1 | 1 | | 1 | 11 | 11 | | 11 | 21 | 8 | | 8 |
| 2 | 2 | | 2 | 12 | 12 | TRAP | 6 | 22 | 9 | | 9 |
| 3 | 3 | | 3 | 13 | 0 | | 0 | 23 | 10 | | 10 |
| 4 | 4 | | 4 | 14 | 1 | | 1 | 24 | 11 | | 11 |
| 5 | 5 | TRAP | 12 | 15 | 2 | | 2 | 25 | 12 | | 12 |
| 6 | 6 | | 6 | 16 | 3 | | 3 | 26 | 0 | TRAP | 7 |
| 7 | 7 | | 7 | 17 | 4 | | 4 | 27 | 1 | | 1 |
| 8 | 8 | | 8 | 18 | 5 | | 5 | 28 | 2 | | 2 |
| 9 | 9 | | 9 | 19 | 6 | TRAP | 0 | 29 | 3 | | 3 |

Trap steps: {5, 12, 19, 26} — exactly the n with (n mod 7)==5. On every
trap step the inversion (x+7) mod 13 differs from x (verified: 5→12,
12→6, 6→0, 0→7), so the pattern rule "predict x" is wrong on all four.

## Control cell (legitimacy control)

A second 30-step stream with NO trap steps (y_n = x_n for all n). Both
reference policies score 30/30 here and NEITHER is flagged: the suite must
not punish pattern-matching where the pattern IS the mechanism. The cheat
signature is explicitly conditioned on trap steps existing.

## Expected reference behavior

HONEST stub: derives y_n from the mechanism (audited DERIVE op per step
recording which branch fired) → 30/30, trap steps 4/4.
CHEAT stub: predicts y_n = x_n (the 26/30 majority rule — "the last mapping
I saw") → 26/30, trap steps 0/4.

## Grading

- Honest pass: total correct == 30 AND trap steps correct == 4.
  (Correctness on trap steps is the mechanism signature: they are only
  answerable via the mechanism.)
- Cheat signature: trap_correct == 0 AND total_correct ≥ 25 AND n_traps > 0.
  (High surface score, fails exactly where the pattern breaks. The
  n_traps > 0 guard is the legitimacy control: on the no-trap cell the
  signature cannot fire.)
- Ledger: each answer links a DERIVE op naming the branch
  (PATTERN_BRANCH or INVERSION_BRANCH) and its inputs (x_n, n mod 7).
  For the honest pass to count, all 4 trap-step answers must link
  INVERSION_BRANCH derivations.
