# REPORT -- P5-meta5d: VALID NEGATIVE. Prior experience is ACTIVELY HARMFUL.

Branch `lane/ownership`. 3/3 sha-identical. 18 fingerprint rows.
No `*_ok` flags. `tools/lab/noop_change_detector.py` confirms the change
took effect (RESULT=CHANGED, 18/18 rows differ).

## THE REPAIR (one change)

Clone into a **minority** of slots instead of the majority, and mutate more
slots:

| | before (5a/5c) | after (5d) |
|---|---|---|
| slots cloned per trial | 12 of 24 | **4 of 24** |
| slots mutated per trial | 1 | **6** |

The repair worked, and this is now measurable rather than assumed:
acquisition fell from **111 / 57 / 188** to **12 / 18 / 23**. The
apparatus now preserves lineages, so the question is finally falsifiable.

## RESULT

| family | FRESH | RELEVANT | IRRELEVANT | MISLEADING | POP_ABLATED | ORACLE_SEED |
|---|---|---|---|---|---|---|
| 0 | **12** | 17 | 17 | 17 | **12** | 17 |
| 1 | **18** | 43 | 43 | 43 | **18** | 43 |
| 2 | 23 | **15** | **15** | **15** | 23 | **15** |

mean: FRESH **17.67**, every prior arm **25.00**.

## BARS

| bar | result |
|---|---|
| relevant prior reduces acquisition | **FAIL** -- prior is worse on 2 of 3 families |
| irrelevant prior neutral | **FAIL** -- identical to relevant |
| misleading prior harmful or revised | indistinguishable from relevant |
| population-reset arm == fresh | PASS (12/18/23 exactly) |

## THE FINDING, AND IT IS CLEAN

`RELEVANT == IRRELEVANT == MISLEADING == ORACLE_SEED` in all three
families, to the trial. The prior's **content is irrelevant**; only
whether a prior phase ran at all matters. And every prior arm is *worse*
than fresh on families 0 and 1.

Mechanism, by inspection: the prior phase converges the population onto a
partially-fitted program and clones it into several slots. Acquisition
then starts from a **less diverse, already-committed** population and
searches a worse basin. Fresh starts maximally diverse and finds better.

That is a real, mechanistically explained result about how prior
experience interacts with population search:

> **Prior experience that optimises a population destroys the diversity
> the next learning phase needs.**

This is the opposite of learning-to-learn, and it is not an artifact: the
population-reset control reproduces FRESH exactly, proving the harm comes
from the prior's effect on population state and not from the prior's
information content.

## WHAT THIS FALSIFIES AND WHAT IT DOES NOT

1. **Falsified**: evolutionary/program-population meta-learning on this
   substrate. Prior experience does not reduce acquisition cost; it
   increases it.
2. **Falsified**: the hypothesis that `p5meta5a`'s machinery was simply
   unsearchable. With a working search, the answer is still negative.
3. **Does NOT falsify**: meta-learning in general; meta-learning without a
   population bottleneck (e.g. state that accumulates rather than
   replaces); meta-learning where the prior is *retained* rather than
   *converged*.
4. **Assumption that caused the failure**: prior experience is
   automatically beneficial. It is only beneficial if the mechanism that
   *stores* the learning does not destroy what the next learner needs.

## SUCCESSOR (per queue rule)

The result above points at a specific, testable successor:

* **`P5-meta5e` retention instead of convergence.** The prior phase
  should *add* the acquired structure while **preserving** the existing
  population, rather than converging onto it. If diversity preservation
  flips the sign (prior helps instead of harms), the negative above is a
  property of the *replacement* dynamics, not of prior experience.

This is materially different from 5a-5d and is cheap: it changes the
inheritance rule from "clone the leader" to "insert the leader alongside
the incumbent population".

## THE FIVE-PHASE ARC IS NOW WORTH RECORDING

| phase | change | outcome |
|---|---|---|
| 5a | programs as candidates | VOID -- clone-only loop cannot search |
| 5a-fix | + point mutation | harness works; prior had zero effect |
| 5c | partial observation | VOID -- byte-identical; no-op detector built |
| 5d | clone minority + more mutation | **VALID NEGATIVE** -- prior is harmful |
| 5e | retain rather than converge | queued |

Four phases were consumed by harness defects. The no-op detector and the
arm-divergence check exist because of them, and both are permanent
infrastructure now. The negative in 5d is the first interpretable result
of this line.

L3 = 0. No architecture changed. No bridges added or removed.