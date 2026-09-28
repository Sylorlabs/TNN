# Amendment 2026-09-27 — A2: Generator — per-phase token salt (formula resolved)

**Status: APPROVED by Micah, 2026-09-27** (~15:21 PDT; recorded in the
governance bundle `SIGNATURE_SHEET.md`, item 1 fix 2). Enacted 2026-09-27.
The frozen prereg text is left byte-intact; this dated amendment governs.

## What it changes

The frozen token formula has a hidden regularity: any two tokens whose
indices agree mod 4 are *exact Caesar shifts of each other*. The red team
demonstrated a "shift-memorizer" that memorizes the 24 training examples,
detects the shift for each probe, and shifts the memorized output — scoring
**24/24 on the P0 mastery gate without implementing any rule**. Such an
agent passes the gate, then its P2 failures misclassify as (c) combination
failure when the truth is (a) it never learned the parts — and K2's void
protection never fires. The gate would certify mastery that doesn't exist.

## Frozen text reference

`PREREG.md` (frozen 2026-09-27, commit `6ca9e042110ca`), §4 "Combination
generator (deterministic, zero RNG)":

> Inputs are counter-derived tokens (`tok(i)`, length 2+i%4, bytes
> (97+(7i+13k+k*k)%26)) — disjoint index ranges per phase (train 0–5, P0 6–13,
> P2 14–61, P3 62–69). The quadratic term (k²) breaks accidental palindromes
> that made the P3 reflex probe insensitive in the first pilot build. No RNG
> anywhere: same binary, same bytes, every run.

## Enacted change

In §4, the token byte formula is replaced with:

> Inputs are counter-derived tokens (`tok(i)`, length 2+i%4). The byte formula
> is `97 + (7i + C_phase·k + k²) mod 26`, where the linear coefficient
> `C_phase` is a fixed per-phase salt: **train = 13, P0 = 17, P2 = 19,
> P3 = 23**. The quadratic term (k²) is unchanged — it still breaks accidental
> palindromes. Index ranges stay disjoint per phase (train 0–5, P0 6–13,
> P2 14–61, P3 62–69). No RNG anywhere: same binary, same bytes, every run.

**Why this formula.** Under the frozen formula, `tok(i1)[k] − tok(i2)[k] =
7(i1−i2) mod 26` for every position k — a pure Caesar shift between any two
same-length tokens, within or across phases. With the salt, the cross-phase
difference is `7(i1−i2) + (C_a − C_b)·k mod 26`, which varies with k (the
coefficient differences 2, 4, 6, 8, 10 never satisfy `(C_a−C_b)·k ≡ 0 mod 26`
for token positions k = 1..5) — so tokens from different phases are **not**
Caesar shifts of one another. Within a phase the pilot-validated structure
is preserved (same-mod-4 tokens are still mutual Caesar shifts *within* the
phase — harmless, since the memorizer attack is cross-phase: mapping test
tokens back to *training* tokens). As a side effect this also kills the
frozen run's byte-identical-input finding (66/600 P2 inputs byte-identical
to training inputs): P2 tokens now differ from training tokens at every
position k ≥ 1.

**Mandatory verification gate.** Before the full battery is built, the red
team's shift-exhaustion test (all cross-phase token pairs checked for
shift-equivalence) must be re-run on the salted token stream and must find
**zero** cross-phase shift pairs. The test result is committed with the
battery. (Recommended, not required: the independent red team should also
try a *linear*-shift memorizer — a per-token offset+slope map — as a bonus
attack; it is not a gate because fitting offset+slope per token pair is
already genuine transformation-learning, not memorization.)

## Evidence

- `pilot/REDTEAM_REPORT.md`, Family 1, §1a: "verified exhaustively for all
  70×70 pairs" — same-mod-4 indices give exact Caesar shifts; every P0 probe
  token (6–11) and every P2/P3 token is a Caesar shift of a training token;
  shift-memorizer scores 24/24 on P0 "without implementing any rule".
- §5a states the constraint this formula satisfies: the salt must be in the
  *k-dependent* coefficients, because an additive constant is still a Caesar
  shift.
- D1 full-battery run (frozen prereg, 2026-09-27): salted-generator audit
  found exact period 52 and 66/600 P2 inputs byte-identical to training —
  independent confirmation the unsalted generator leaks across phases.

## Effect

- The §4 generator carries the resolved per-phase salt; the deliberate
  ambiguity in the proposal (exact formula left to the builder) is resolved
  here, not deferred.
- K2's void protection becomes meaningful: a passing P0 genuinely means the
  parts were learned, so (a)-vs-(c) attribution downstream can be trusted.
- All runs stay deterministic and byte-identical (fixed constants, zero RNG).
- The full battery re-validates the instrument under the salted generator
  (all reference modes re-run, shift-exhaustion re-run) before the real
  learner runs.
