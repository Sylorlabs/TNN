# K-HB-1 Re-freeze - Principled Bar for H-B DELTA

**Date:** 2026-09-28 (overnight research session)
**Status:** FROZEN (this commit). Judgment of pre-existing measurements against
this bar follows immediately below - the measurements are not re-run (they are
deterministic and byte-identical); only the bar is new.
**Why:** The original K-HB-1 first appeared in the results commit (VOID as a
preregistered verdict). This bar is derived from H-B's design documents, which
predate the results. It is set post-observation but NOT fit to observation -
the derivation is transparent and the numbers below are justified from the
mechanism, not from 119/120.

## Derivation (from pre-existing design docs)

H-B DELTA (`docs/lab/composition/combiner_arch/hypo_b/BUILD.md`, committed
2026-09-27, before any salt results):

1. **Exact search, not approximation** (BUILD.md §Architecture items 4–6):
   per-slot provenance enumeration, mixed-radix ambiguity enumeration, exact
   integer affine fitting (Cramer's rule, exact divisibility required),
   byte-exact training verification before acceptance. An exact-search
   mechanism does not guess - it finds the program or withholds.
   → **Bar clause (a): zero wrong emissions** (confident incorrect predictions)
   on any probe. A single wrong emission falsifies the exact-search claim.

2. **In-schema rules with adequate teaching** (BUILD.md §Source identity):
   the D1 six (reverse, dupfirst, rotleft, droplast, upperfirst, sortchars) are
   all within the enumerated schema (COPY/MAP/EMIT, affine, six split
   conditions, sort fallback); teaching is 12 examples per rule, rule-major,
   the format the implementation expects. Exact search on adequate in-schema
   teaching must succeed.
   → **Bar clause (b): P0 = 48/48** (8/rule × 6 rules). A withhold or error on
   P0 is an induction failure, not honesty.

3. **Withhold as designed honest behavior** (BUILD.md §Architecture item 11):
   structural withhold codes (UNDERDET, NO_LENGTH_RULE, AMBIGUOUS, NO_PROGRAM,
   OOB, NO_CLAUSE). Withholds are first-class, but each must be justifiable as
   out-of-taught-distribution. Composition (P1) chains induced programs on
   intermediates the learner never saw in teaching - degenerate intermediates
   (e.g., length-1) are legitimately outside the induced program's domain.
   → **Bar clause (c): P1 = 100% correct-or-withhold**, with every withhold
   individually documented as out-of-distribution. Zero wrong emissions (per
   clause a).

4. **New in-schema rules** (BUILD.md §Capability battery): swap-first-last and
   sort-descending are within the affine/sort schema; H-B's build record claims
   8/8 on each at build time.
   → **Bar clause (d): P3 = 8/8.**

5. **Salt scope** (the H-A lesson): bars apply only where the teaching signal
   is preserved. H-B was evaluated on clean teaching + salted probes (8 salt
   families); the salt is a per-byte relabeling of probes, which does not
   affect H-B's positional mechanism. All 8 arms are valid.

## The frozen bar

**K-HB-1 (principled, frozen 2026-09-28):** H-B SURVIVES iff, on clean teaching
+ all 8 salt-probe families: (a) zero wrong emissions anywhere; (b) P0 = 48/48;
(c) P1 = 100% correct-or-withhold with each withhold documented as
out-of-distribution; (d) P3 = 8/8. Any wrong emission, any P0 shortfall, any
unjustified withhold, or any P3 shortfall → KILLED.

## Judgment (pre-existing deterministic measurements)

From `docs/lab/composition/combiner_arch/testing/TESTING.md` and committed
`raw/clean_hb_*/SCORES.json` (all 8 arms):

- (a) Zero wrong emissions: CONFIRMED (withheld 0 wrong on P0/P2; TESTING.md:
  "Zero wrong emissions anywhere").
- (b) P0 = 48/48 on all 8 arms: CONFIRMED.
- (c) P1 = 119/120 correct + 1 withhold on all 8 arms; the withhold is the
  same item every arm (r3+r2 droplast→rotleft, 2-byte input → length-1
  intermediate; no length-1 rotleft in teaching; affine program has no
  length-1 clause). Documented as out-of-distribution: JUSTIFIED.
- (d) P3 = 8/8 on all 8 arms: CONFIRMED.

**Verdict: H-B SURVIVES under principled K-HB-1.** The survival is now
verdict-grade (frozen bar, pre-existing measurements, transparent derivation).

## Standing qualifications (unchanged from Phase-1)

- H-B remains L1+ (parameter induction), not L2/L3: it discovers affine
  parameters via search but never the procedure; the 8 salts test one
  invariance property eight times; byte-op salt-riding untested; no length
  extrapolation beyond 2–5 tested.
- Order-sensitivity (rule-major teaching required) is a documented robustness
  gap, not a kill.
- The salted-teaching experiment (48/48 withholds in `raw/salted_hb_*`) is
  exploratory and outside this bar's scope.
