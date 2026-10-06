# REPORT -- P5-meta5e: THE PRIOR HAS NO EFFECTIVE CHANNEL. Insensitivity, not learning.

Branch `lane/ownership`. 3/3 sha-identical. No `*_ok` flags.
`noop_change_detector`: RESULT=CHANGED (12/18 rows), so the edits took effect.

## RESULT

| family | FRESH | RELEVANT | IRRELEVANT | MISLEADING | POP_ABLATED | ORACLE_SEED |
|---|---|---|---|---|---|---|
| 0 | 12 | 12 | 12 | 12 | 12 | 12 |
| 1 | 18 | 18 | 18 | 18 | 18 | 18 |
| 2 | 23 | 23 | 23 | 23 | 23 | 23 |

**All six arms identical, in every family, to the trial.** Mean 17.67 for
every arm.

## THE ARC ACROSS 5d AND 5e

| variant | prior's effect on the population | outcome |
|---|---|---|
| `5d` clone leader over slots + mutate 75x in prior | replaced | prior **HARMFUL** (25.00 vs 17.67) |
| `5e` elitist retention + no prior mutation | preserved | prior **NEUTRAL** (17.67 = 17.67) |

5d's preregistered question was: *is the negative about replacement
dynamics, or about prior experience itself?* The answer is now precise:

**Neither. The acquisition phase is insensitive to the starting
population.** Replacing it hurts; preserving it does nothing; both are
consistent with acquisition ignoring its initial condition entirely and
converging to its own attractor over 300 trials of a 6-mutation search.

## WHY THE FIRST 5e ATTEMPT WAS A NO-OP (caught by the new detector)

The first 5e edit produced byte-identical output.
`noop_change_detector.py` flagged it immediately, which is exactly what
that instrument was built for one phase earlier.

Root cause, and it is a *fourth* instance of the same defect class:

* the prior loop ran `TRIALS()/4 = 75` iterations, each calling
  `mutate()` once -- **75 mutations applied before acquisition starts**,
  versus 6 per acquisition trial. The population was heavily randomised by
  the prior phase regardless of what the inheritance rule did, so
  "retention" could not matter.
* `AGE` was incremented and **never read**, so "retain the fittest" was
  decorative.

Both fixed: the prior no longer mutates, and inheritance became elitist
(acquired program installed only where it strictly beats the incumbent on
observed answers).

## THE STRUCTURAL FINDING

The prior phase has **exactly one channel** through which it could
influence acquisition: the population. Everything else is severed:

* `OBS` is rebuilt empty each family and revealed one answer per trial;
* `POBS` is prior-phase-only and discarded before acquisition;
* `AGE` is written and never read.

And on that one channel, the effect is asymmetric and unhelpful:
replacing the population **hurts** (5d), preserving it does **nothing**
(5e).

> **Neither destroying nor preserving prior-learned structure helps. The
> substrate's acquisition dynamics dominate initial conditions entirely.**

So the P5-meta question is not merely unanswered on this substrate. It is
**unaskable in this form**: any prior that can only act through a
population that acquisition overwrites is untestable.

## WHAT THIS FALSIFIES AND WHAT IT DOES NOT

1. **Falsified**: evolutionary / program-population meta-learning on this
   substrate, under both replacement (5d) and retention (5e) dynamics.
2. **Falsified**: the 5d hypothesis that prior experience is harmful
   *because it replaces the population*. Preservation removes the harm and
   the benefit is still zero, so replacement was not the cause either.
3. **Does NOT falsify**: meta-learning that acts through a channel
   acquisition does not overwrite (accumulated state, not population).
4. **Does NOT falsify**: meta-learning where acquisition is *short* enough
   that the starting condition still matters. 300 trials may simply be too
   many for any seed to matter.

## SUCCESSOR (per queue rule)

Two materially distinct options, both cheap, and they attack different
halves of the insensitivity:

* **`P5-meta5f` short acquisition.** Cut trials so acquisition cannot
  wash out its initial condition (e.g. 10-20 trials instead of 300). If the
  prior is inert at 300 and *active* at 15, the finding is about search
  horizon, not about meta-learning.
* **`P5-meta5g` non-population carrier.** Give the prior a channel that
  acquisition *cannot* overwrite -- accumulated state that biases sampling
  rather than a population that gets replaced. This is the only variant
  where prior experience could plausibly help.

Both are cheap falsifiers. Neither is a tuning change in the sense that
matters: 5f changes the measurement scale, 5g changes the mechanism class.

## INSTRUMENTATION NOTE

`noop_change_detector.py` earned its place within one phase: it caught a
no-op edit that would otherwise have been reported as "prior experience is
neutral because elitist retention preserves diversity" -- a plausible and
wrong conclusion, since the edit had not taken effect at all.

L3 = 0. No architecture changed. No bridges added or removed.