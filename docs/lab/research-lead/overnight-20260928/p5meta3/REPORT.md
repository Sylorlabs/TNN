# REPORT -- P5-meta3: NEGATIVE. The speedup is a fact cache, not learning-to-learn.

Branch `ownership`. Prereg `p5meta3/PREREG.md`. 3/3 sha-identical
`5f9db39b6a4fdde8d872...`. 24 fingerprint rows, arm audit PASS. Loop lint
CLEAN. No `*_ok` flags; all bars recomputed by `score53.py`.

## ACQUISITION COST (trials to 3 consecutive correct; 40 = never)

| family | FRESH | RELEVANT | IRRELEVANT | MISLEADING | META_ABLATED | ORACLE_META |
|---|---|---|---|---|---|---|
| 0 | 19 | 3 | 15 | 15 | 3 | 3 |
| 1 | 25 | 3 | 14 | 14 | 3 | 3 |
| 2 | 27 | 3 | 15 | 15 | 3 | 3 |
| 3 | 27 | 3 | 15 | 15 | 3 | 3 |
| **mean** | **24.50** | **3.00** | **14.75** | **14.75** | **3.00** | **3.00** |

## BARS

| bar | result |
|---|---|
| M1 RELEVANT < FRESH every family | **PASS** (3.00 vs 24.50) |
| M2 IRRELEVANT neutral (within 1 trial) | **FAIL** (diffs 4,11,12,12) |
| M3 MISLEADING harmful or revised | ambiguous — it neither hurt nor was revised |
| **M4 META_ABLATED loses the advantage** | **FAIL — ablation cost ZERO** |
| M5 ORACLE_META <= RELEVANT | PASS (tie, 3.00) |
| M6 no strategy menu / no family index in learner | PASS (0 occurrences) |

## VERDICT: NOT META-LEARNING. Retained task state.

The prereg made M4 decisive: *"If M1 holds but M4 fails, the result is
retained task state, not meta-learning."*

M1 holds dramatically. M4 fails **completely**: ablating the entire
learned machinery (`MACH`, zeroed) while **keeping** the retained facts
cost **zero** extra trials. `META_ABLATED` mean is 3.00, identical to
`RELEVANT`.

So the speedup is not learning machinery at all. It is that the prior
phase wrote the correct `(query, answer)` pairs into `FACTS`, and
acquisition then replays them. A cache, exactly what M4 was built to
expose.

## THE SECOND, UNPLANNED FINDING: IRRELEVANT PRIOR ALSO HELPED

M2 fails just as hard. Irrelevant prior (a different family) reduced
acquisition from 24.50 to **14.75** — a 40% improvement from experience on
a task with nothing to do with the target.

`MISLEADING` prior (same surface form, conflicting answers) gives the
*identical* 14.75. That is diagnostic: a genuinely conflicting prior
should be worse than a neutral one. Identical numbers mean the mechanism
is indifferent to the prior's content.

Cause, by inspection: `observe` bootstraps machine slot 0 from the first
observation (`a=1, b=0, c=ans, d=7, e=0`). That generic scaffold fits
*any* family partially, so any prior at all helps a little. The prior is
not being used as knowledge; it is being used as scaffolding.

**This is a confound that would have produced a false positive.** Had I
omitted the IRRELEVANT arm, M1 would have looked like clean evidence of
learning-to-learn.

## WHY THE INHERITED B5D FAILED, CONFIRMED

`lifetime_metalearn` B5D compared `err_T(E03)` with `err_T(E12)` —
episodes 3 and 12, i.e. **different families**. That bar measured task
difficulty. My successor fixed the criterion (within-family acquisition)
and the fixed criterion then produced a *cleaner negative*, which is the
point of fixing it: the inherited bar was not measuring what it claimed,
and replacing it removed the illusion rather than confirming the failure.

## SUCCESSOR GENERATION (required by the queue rule)

1. **Falsified**: fact-cached "meta-learning" on associative substrate;
   "learning-to-learn" measured as acquisition speedup with a retained-fact
   lookup available.
2. **Does NOT falsify**: genuine meta-learning; learning-to-learn in
   substrates where facts cannot be retained.
3. **Assumption that caused failure**: retained facts and learned
   machinery were both available, and the fact lookup dominated. Learning
   *speed* was measured where the fastest strategy is *not learning*.
4. **Smallest structurally different successor**: make retention
   *impossible* to exploit by measuring acquisition on queries that were
   never observed — i.e. transfer of the acquired *mapping* to unseen
   inputs, not replay on seen inputs. If the machinery is real it should
   predict unseen queries; a cache cannot.
5. **Architecture deletable?** Yes — the `MACH` slot machinery can be
   deleted entirely with no measured loss. That is a real simplification
   and should be applied to any successor that cannot show it earns its
   keep.

## STATUS

`P5-meta` remains **open** with a sharper question. The next experiment
must make fact-replay useless by construction. That is a design change,
not a tuning change.

L3 = 0. No architecture changed. No bridges added or removed. No modes,
routers, domain names or strategy menus.