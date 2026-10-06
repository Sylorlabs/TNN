# REPORT -- P5-meta5f: SEARCH HORIZON RULED OUT. The measurement is saturated at both ends.

Branch `lane/ownership`. 3/3 sha-identical. 108 fingerprint rows.
No `*_ok` flags.

## THE TEST

`p5meta5e` found acquisition insensitive to its starting population over
300 trials. `p5meta5f` asks whether the blocker is simply the **search
horizon**: if the prior is inert at 300 trials but *active* at short
horizons, the finding was about horizon rather than about meta-learning.

Horizons swept: **8, 15, 30, 60, 150, 300** (a 37x range). Mechanism
unchanged from 5e.

## RESULT: ALL ARMS IDENTICAL AT EVERY HORIZON

| family | horizon | FRESH | RELEVANT | IRRELEVANT | MISLEADING | POP_ABLATED | ORACLE_SEED |
|---|---|---|---|---|---|---|---|
| 0 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| 0 | 30 | 5 | 5 | 5 | 5 | 5 | 5 |
| 0 | 300 | 7 | 7 | 7 | 7 | 7 | 7 |
| 1 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| 1 | 30 | 4 | 4 | 4 | 4 | 4 | 4 |
| 1 | 300 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| 2 | 30 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 300 | 1 | 1 | 1 | 1 | 1 | 1 |

(full table in `run.txt`, 108 rows)

**Search horizon is ruled out.** The prior is inert at every horizon
tested, including 8 trials where acquisition barely runs.

## WHY -- AND IT IS A MEASUREMENT SATURATION, NOT A FINDING

The two ends of the sweep fail for **opposite** reasons:

* **Long horizon (300):** search washes out the initial condition. 300
  trials of 6-mutation search converges to its own attractor whatever the
  starting population.
* **Short horizon (8):** the task is *too easy to distinguish starts*.
  With 8 of 10 training answers revealed, the fitness signal is nearly
  complete, so the family is solved almost immediately **from any
  starting population**.

There is no horizon in between where the prior could show an effect. The
measurement is **saturated at both ends**, which is why every column is
identical.

This is a genuine methodological result and it retires the search-horizon
hypothesis cleanly.

## DEFECT FOUND

The not-acquired fallback used `TRIALS()` (300) instead of the current
horizon, so horizons 8 and 15 reported 300 and the short end of the sweep
was masked in the first run. Fixed. The detector did **not** catch this
one, because the first run was a *first* run -- there was no prior table
to compare against. Recorded as a coverage limit: the no-op detector
catches no-op *edits*, not wrong *first* runs.

## WHAT THIS FALSIFIES AND WHAT IT DOES NOT

1. **Falsified**: the search-horizon explanation for the P5-meta
   inertness. Not a horizon effect.
2. **Falsified**: evolutionary / program-population meta-learning on this
   substrate across a 37x horizon range.
3. **Does NOT falsify**: meta-learning through a channel acquisition does
   not overwrite. The population has now been shown inert to *both*
   replacement (5d: harmful) and preservation (5e: neutral), and inert
   across horizon (5f).
4. **Does NOT falsify**: meta-learning in substrates with no population
   bottleneck and no easily-saturated fitness signal.

## WHERE THE BLOCKER NOW STANDS

Three independent attacks on "why doesn't prior experience help?" have
all landed on the same wall, and the wall is now well characterised:

| attack | result |
|---|---|
| 5d -- preserve/replace dynamics | replacement **harms** (25.00 vs 17.67) |
| 5e -- elitist retention | preservation is **neutral** (17.67 = 17.67) |
| 5f -- horizon 8..300 (37x) | **neutral at every horizon** |

> The population is the prior's only channel; acquisition overwrites it
> at long horizons, saturates it at short horizons, and is indifferent
> to it in between.

So `P5-meta` is not blocked on measurement any more. It is blocked on
**mechanism**: no variant of "store the prior in a population" can be
tested here, because the population is either destroyed or ignored.

## SUCCESSOR (per queue rule)

`P5-meta5g` is now the only remaining option on this line and it changes
the mechanism class rather than the parameters:

> Give the prior a carrier that acquisition **cannot overwrite** --
> accumulated state that biases *sampling* rather than a population that
> gets replaced or ignored.

If `P5-meta5g` also shows no prior effect, the honest conclusion is that
this substrate cannot exhibit meta-learning at all, and the line should be
closed with that finding rather than continued. That is a legitimate
outcome and cheaper than another parameter sweep.

## ARC SUMMARY (5a -> 5f)

| phase | change | outcome |
|---|---|---|
| 5a | programs as candidates | VOID -- clone-only, cannot search |
| 5a-fix | + point mutation | harness works; prior inert |
| 5c | partial observation | VOID -- no-op, caught by detector |
| 5d | clone minority, more mutation | prior **HARMFUL** |
| 5e | elitist retention | prior **NEUTRAL** |
| 5f | 37x horizon sweep | prior **NEUTRAL at all horizons** |

Six phases, one harness class of defect (intervention never reaching the
mechanism), two permanent instruments built because of it, and a blocker
now specified precisely enough to decide whether to continue.

L3 = 0. No architecture changed. No bridges added or removed.