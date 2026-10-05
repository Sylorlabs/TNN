# REPORT -- FINDER OWNERSHIP C1761-C1800

Prereg `finder7/PREREG.md`. 3/3 sha256
`8cebd67e31226cfd3e33a9f0210eb64dd1f54e0448734dd114582c4a6a7baed1`
bars lint CLEAN, loop lint CLEAN.

**Headline: the learner's generated proposals failed every test
instance, while a two-step researcher heuristic solved all four.**

## WORLD

Capacity-constrained graph transformation. States are sets over labels
`1..4`; primitives are `DEL`, `INS`, `MOV` (24 edit codes). Solutions
vary in length and label identity, so there is no fixed menu of complete
forms and nothing can be memorised except a shape.

```
TRAIN  {1,2}->{3}   {1,2,3}->{4}   {2,3}->{1}
       {1,3}->{2,4} {3,4}->{1}     {1,2,3}->{3,4}
TEST   {1,2}->{4}   {2,3}->{1,4}   {1,3}->{2}   {1,2}->{3,4}
```

## RESULTS (proposals evaluated; all measurement on TEST)

| arm | what it is | proposals | instances failed |
|---|---|---|---|
| **C** | **researcher heuristic, 1-step-lookahead greedy** | **8** | **0** |
| G | fresh learner = full search | 694 | 0 |
| A | exhaustive researcher finder | 694 | 0 |
| H | misleading prior learner | 584 | 1 |
| F | **learned generation** | 3,840 | **4** |
| B | random proposals | 6,455 | 1 |
| D | learned ranking of proposals | 9,108 | 1 |
| E | facts-only reconstruction | 12,525 | 1 |

Per-test greedy cost: `[2 2 2 2]`. Every test instance has a two-edit
solution.

## BARS

```
B2 exhaustive solves all            1   world is solvable
B3 greedy worse than exhaustive     0   greedy is 87x CHEAPER
B4 F beats C                       0   F is 480x more expensive and fails all
B5 F beats D                       1   generation beats ranking on cost only
B6 fresh worse than F               0
B7 misleading worse than F         0
B8 facts-only worse than F          1
```

## FALSIFIERS: TWO OF FOUR DIED

| | prediction | outcome |
|---|---|---|
| `F-CAP` | capacity-constrained edits defeat naive greedy | **FALSIFIED** -- greedy solves all four in 2 steps each |
| `F-FINDER` | learned generation beats a researcher heuristic | **FALSIFIED** -- 3,840 and 4 failures vs 8 and 0 |
| `F-SHAPE` | the useful knowledge is the kind-shape | **survives, with a caveat below** |
| `F-PRIOR` | the prior is load-bearing, not facts-reconstructible | **survives** (B8) |

## WHY F FAILED -- MECHANISM, NOT VIBE

The learner harvested six kind-shapes from the TRAIN instances:

```
[INS,MOV,MOV]  [MOV,MOV,INS,INS]  [MOV,MOV,INS,INS]
[MOV,INS,INS,MOV]  [INS,MOV,MOV]  [INS,MOV,INS]
```

Every one is **three or four edits long**, because TRAIN instances
required three or four edits. Every TEST instance has a **two-edit**
solution.

So `F`, which generates only sequences matching a learned shape,
**never proposes anything of the right length**. It fails all four
instances not because its shapes are wrong but because its shapes are
*too long*.

> **Shape-restricted generation is brittle to solution-length shift.**

The learned knowledge transferred perfectly -- from a distribution with
no overlap with the test distribution.

## WHAT THE LEARNER DID AND DID NOT MOVE

Two genuine positives, both narrow:

* **F beats D: 3,840 vs 9,108.** Generation beats *ranking* of the same
  primitive alphabet. That is the phase's stated contrast, and it
  holds -- on cost, though F is worse on success.
* **F beats E: 3,840 vs 12,525.** The prior is not reconstructible from
  the fact table alone, so something about search history matters.

Both are real and both are dwarfed by the heuristic.

## THE CENTRAL NEGATIVE

```
researcher greedy    8 proposals, 0 failures
exhaustive finder  694 proposals, 0 failures
learned generation 3840 proposals, 4 failures
```

A one-step-lookahead greedy is **87x cheaper than exhaustive search**
and **480x cheaper than the learner's generator**. On this world the
researcher's *search procedure* is not the bottleneck the phase assumed
it was; it is so strong that no learner arm came close.

This is the same shape as the C1681 retraction, and I predicted it in
the prereg (`B4` was declared the decisive bar precisely so this could
be killed). The prediction was wrong and the bar did its job.

## A BAR THAT WAS BADLY SPECIFIED

`B7 misleading worse than F` passed on cost while `H` **failed an
instance and F failed four**. Comparing arms by proposals alone is
misleading when success rates differ. The prereg's metric was
proposals-to-first-success, which is only meaningful between arms with
equal success. Recorded as a bar-design defect; a proper metric would
have been `(proposals on solved) + (LIMIT on unsolved)`, which would
have ranked `C` first and `F` last, as the success data already shows.

## FOUR DEFECTS, ALL MINE

1. **`DEL` never removed bit 0.** `m & (0-bitof(x))` computes
   `-bitof(x)`; for `x=1` that is `-1`, all ones, so the AND was a
   no-op, and for `x=3` it cleared the wrong bit. Symptom: one TEST
   instance was unsolvable and `B2=0`. **The completeness bar caught
   it.** Fixed with `0-bitof(x)-1`.
2. **Alphabet had four malformed codes.** `NE=24` counts 12 MOV pairs,
   of which 4 have `a==b`; those were mapped to `MOV(x,0)`, and
   `bitof(0)=1` silently made them `MOV(x,1)`. Duplicated moves, not
   missing ones, but the alphabet was not what it claimed.
3. **Shape harvest used `L-1` for the length** while storing `L`
   kinds, so short shapes printed with a `-1` terminator inside them.
4. **Candidate pool stride collision.** Sequences were stored at
   stride 1 while each needs `MAXL` slots, so candidates overlapped.
   Caught by the compiler's arity check after a bad call.

Also two performance defects: ~11M small allocations inside the inner
loop (timeout), and concatenated numbers in the report making
`cap=2, hamming=4` print as `24`.

Defect 1 is the argument for `B2`. An arm that claims completeness is
exactly the arm that should be trusted to fail loudly, and it did.

## STANDING

```
learned generation beats learned ranking        YES  (cost; 3840 vs 9108)
learned generation beats a researcher heuristic NO   (3840/4fail vs 8/0fail)
learned generation solves novel instances       NO   (0 of 4)
shape knowledge transfers across length shift    NO   (the key negative)
the prior is not facts-reconstructible           YES
L3 = 0
```

## WHAT THIS ADDS TO THE PICTURE

Three independent experiments now say the same thing about different
mechanisms:

```
C1681  selection   -- a fixed heuristic ties the learner
C1691  selection   -- global credit ties fixed heuristics; only
                     query-scoping wins, and the key was chosen by me
C1800  generation  -- a fixed heuristic beats the learner outright
```

The recurring shape: **whenever a competent researcher procedure exists
for the task, the learner does not beat it.** What the learner reliably
does provide is *transfer without re-derivation* -- the query-scoped
credit result, and `D`'s ranking of 9,108 proposals against `E`'s
12,525, are both about cost, never about capability.

That reframes the next phase. The open question is not "can the learner
out-search the researcher" -- on these worlds it cannot. It is:

> Can the learner acquire a *search procedure* from experience, rather
> than a prior over proposals generated by the researcher's procedure?

That is PHASE 8's territory, and this lane is the evidence for why it
matters: `F` had access to experience and could only produce a prior,
while `C` simply computed the right answer in two steps.