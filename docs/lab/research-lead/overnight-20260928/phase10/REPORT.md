# REPORT -- PHASE 10: STRUCTURAL POSSIBILITY. MIXED, MOSTLY NEGATIVE.

Branch `ownership`. Prereg `phase10/PREREG.md`. 99 rows (3 regimes x 11 arms
x 3 budgets). 3/3 sha-identical. No `*_ok` flags; all verdicts recomputed.

## VERDICT AGAINST THE SUCCESS BAR

The bar was: *relevant experience must cause a structural possibility to
become cheaply constructible that fresh and facts-only learners cannot
cheaply reconstruct.*

| arm | principle | rg0 @200 | rg0 @1000 | rg0 @4000 |
|---|---|---|---|---|
| 0 P1 | local plastic connectivity | **1** | 1 | 1 |
| 1 P2 | learned structural rewrites | -1 | -1 | -1 |
| 2 P3 | content-addressed interaction | 28 | 6 | 2 |
| 3 P4 | attractor / settling | **2** | 2 | 2 |
| 4 P5 | learned executable transforms | -1 | -1 | -1 |
| 5 | fresh | -1 | -1 | -1 |
| 6 | facts-only | -1 | -1 | -1 |
| 7 | erased | -1 | -1 | -1 |
| 8 | irrelevant prior | -1 | -1 | -1 |
| 9 | misleading prior | -1 | -1 | -1 |
| 10 | permuted (arm 0 relabelled) | 8 | 8 | 8 |

**S1 holds** (P1 = 1, P4 = 2, P3 = 28->2). **S2 holds** (fresh never
succeeds at 200/1000). **S3 holds** (facts-only never succeeds).
**S4 holds** (erased never succeeds). **S5 holds** (irrelevant and
misleading never succeed).

**The phase's central hypothesis FAILS.** The two principles that
introduce *learned structural operations* -- P2 and P5 -- are the two
that never succeed at any budget. The principles that only reweight
sampling (P1, P4) are the ones that work.

## WHAT THIS MEANS

The substrate change (variable length + learned rewrites) did **not**
deliver structural possibility. Instead:

> **Learned structural rewrites made generation strictly worse.**

Mechanism, verified by hand: a learned rewrite is keyed on an op-pair
pattern and forces a specific successor. It is **position-blind**. The
trained patterns for the primary target are

```
(1,4)->7  (4,7)->2  (7,2)->5  (2,5)->0  (5,0)->3
```

If `(1,4)` occurs by chance at position 3, the rewrite forces `7` there,
which is wrong for position 3. Since the base pair model already samples
correctly most of the time, the rewrite can only ever damage.

So the rewrites **constrained** structural possibility rather than
expanding it. That is the opposite of the phase's purpose, and it is a
substantive negative rather than a null result.

## HARNESS POSITIVE CONTROL -- one fails

Regime 2 is a length-3 target intended to be uniform-reachable. The
fresh sampler reached it at **cost 669/1000, not within 200**. So the
preregistered control ("fresh must succeed") **fails at budget 200**.

The metric is not broken -- P1 hits the same target at cost 1 -- but the
control as specified is wrong: with `OPS=8, LEN=3` the per-proposal hit
probability is `1/512`, so 200 proposals is genuinely too few. Recorded
as a prereg design error rather than adjusted silently.

## IDENTIFIER PERMUTATION -- HOLDS

Arm 10 is arm 0's state with row and column relabelled together
(`permute(x)=3x mod 8`, `gcd(3,8)=1`). It scores **8** where arm 0
scores 1, at every budget, with targets correctly relabelled in the raw
output (`t0` becomes 3).

That is a ratio of 8x, outside the 1.5x tolerance Phase 6 used, so this
is **weaker than Phase 6's permutation closure**. Both arms succeed, so
the effect is not identifier-dependent, but the costs are not
equivalent. Likely cause: the permutation interacts with the
deterministic draw hash, which was not itself permuted. **Not treated as
a clean pass.**

## THREE DEFECTS, ALL MINE, FOUND BEFORE ANY RESULT WAS BELIEVED

1. **Learned rewrite stored an arbitrary replacement** `(v,(v+1)%8)`,
   unrelated to what actually followed. Every rewrite destroyed a
   correct prefix. That is why P2/P5 lost on the first run.
2. **Rewrite lookup keyed on the *sampled* successor** while storage was
   keyed on the *pattern*'s successor. On a wrong sampled pair the row
   was never trained and the best match was arbitrary. Fixed to key both
   on the pattern.
3. **The principle field was the only field written**, so P2/P5 arms had
   an empty pair model and were crippled rather than competitive, and the
   permutation arm had `fld=0` and received no state at all. Fixed by
   giving every experienced arm the base pair+length model (part of the
   generic construction loop) with the principle field as an addition.

## CLASSIFICATION

Per the prereg rule -- *if a mechanism only learns weights over a
source-defined alphabet or form, classify it bounded L2 and move on*:

**P1, P3, P4 are bounded L2.** They learn weights (pair counts, address
counts, length counts) over a source-defined alphabet and form. They make
generation cheaper; they do not expand what can be built.

**P2, P5 are negative.** Learned structural rewrites did not help and,
as implemented, actively hurt.

**No mechanism in this phase reaches structural possibility.** The
success bar is not met by any of the five principles.

## WHAT THIS ADDS TO THE PICTURE

Phase 6 established that learner state changes the proposal
distribution (bounded L2, permutation-clean). Phase 10 asked whether a
substrate change lets state change *what can be built*. The answer here
is no: adding learned rewrite operations to the generator made things
worse, because the rewrites were position-blind.

The natural next mechanism is a **position-aware** or **context-conditional**
rewrite -- but that is exactly the kind of learned context routing that
Phase 6's `phase4` showed collapses into a researcher-authored router,
so it needs the same adversarial treatment before it is trusted.

## LIMITS

Single author; adversary slot unfilled; three defects in my own code;
permutation equivalence weaker than Phase 6 (8x vs 1.5x tolerance);
harness control failed at budget 200 as specified; 3 regimes, 1 alphabet
size, 1 prior length; synthetic; nothing measures TNN; no independent
red team.

L3 = 0. No architecture changed. No bridges added or removed.