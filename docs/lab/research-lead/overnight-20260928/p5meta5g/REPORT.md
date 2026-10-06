# REPORT -- P5-meta5g: VOID. Non-population carrier could not be made to work.

Branch `lane/ownership`. 3/3 sha-identical. 18 fingerprint rows.
No `*_ok` flags. `noop_change_detector`: RESULT=CHANGED.

## ATTEMPTED

The last option on this line. `p5meta5d`/`5e`/`5f` established the
population cannot carry a prior (replaced -> harmful, preserved ->
neutral, all horizons -> neutral). `5g` therefore changed the **mechanism
class**: acquisition samples programs from a persistent per-slot weight
table `PR` accumulated from prior experience, and the population array is
never consulted for selection, so the prior cannot be overwritten.

## RESULT: VOID

All six arms, all three families: **300 (never acquires)**, mean 300.00,
arms identical.

That is a harness fault, not a learner fact. Solutions provably exist on
the test band: **5 / 5 / 6** programs per family are correct on the whole
unseen band q=10..19. And a single-probe hit probability is 0.09-0.16, so
300 trials should succeed easily.

## TWO DEFECTS

1. **Switching carriers removed the exploration operator.** `5f` found
   solutions because `mutate()` ran during acquisition. `5g` stopped
   consulting the population, and the mutation went with it, leaving a
   fixed draw of <=24 of 64 programs. Any family whose solution was
   absent became unsolvable *structurally*. Fixed by restoring mutation
   inside the sampled carrier slot — which did not fix the result, so a
   second cause remains unidentified.
2. **Unidentified remaining cause.** With mutation restored inside the
   carrier, every family still reports 300 despite solutions existing and
   per-trial hit probability ~0.1. I did not isolate why, and I am not
   going to guess at it in a report.

## WHAT THIS ESTABLISHES

The productive finding here is negative and about **my own process**, not
about learners:

> Across seven phases on the P5-meta line (`p5meta3`, `p5meta4`,
> `p5meta5a`, `5a-fix`, `5c`, `5d`, `5e`, `5f`, `5g`), **nine** distinct
> defects were found, and **every one** had the same shape: the intended
> intervention never reached the mechanism under test.

| defect | intended | actual |
|---|---|---|
| `MACH` bootstrap | learn a mapping | content-independent scaffold |
| fact store | measurement | cache answered the queries |
| clone-only loop | search | cannot search |
| linear seeding | 24 programs | 4 distinct |
| full cloning | inherit best | population becomes 1 |
| fitness vs one value | fitness | category error, pinned |
| 75 prior mutations | retention | swamped any inheritance rule |
| `AGE` written | retain fittest | never read |
| carrier switch | bias sampling | removed exploration |

**Six of nine were visible only by comparing arms that should differ**,
which is why `tools/lab/arm_audit.py` exists. Two were caught by
`tools/lab/noop_change_detector.py` after it was built. One (the `5f`
horizon fallback) was caught by neither, because it was a wrong *first*
run with nothing to compare against.

## CLOSING DECISION FOR P5-meta

The queue's rule says: *if the last option fails, close with that finding
rather than continuing.* I am applying it.

**`P5-meta` is CLOSED as NOT-ESTABLISHED-IN-THIS-SUBSTRATE**, not as
refuted. The precise statement:

> Across every carrier tried -- fact store, population, retained
> population, non-population weight table -- and across a 37x horizon
> range, prior experience did not reduce acquisition cost. Where a prior
> acted by replacing population state it made acquisition *worse*. The
> experiments are void where the harness could not reach provably-existing
> solutions, so this is a **failure to demonstrate**, and the apparatus
> has consumed nine defects.

**What would reopen it:** a substrate where (a) a harness assertion
proves solutions are reachable before any result is read, and (b) the
prior's carrier provably survives acquisition. Both are *preconditions*,
not tuning. That is a specification for a substrate, not another
experiment on this one.

## THE GENERAL LESSON (this is the transferable part)

Nine defects, one shape. The lesson is not about any particular
mechanism:

> **An experiment whose intervention cannot be shown to reach the
> mechanism under test produces numbers, and those numbers will be
> interpreted.** The only defence that worked here was mechanical:
> compare arms that should differ, and compare runs before and after a
> declared change.

Both instruments now exist and both earned their place within one phase
of creation.

## STATUS

`P5-meta` CLOSED (not established in this substrate). Next CURRENT item
promoted from QUEUED per the queue rule: `P6-formal`
(`ZD2-PASS-DEGENERATE-POLICY`), which does not share this substrate's
defect profile. `lane/p5meta5b` remains live in parallel.

L3 = 0. No architecture changed. No bridges added or removed.