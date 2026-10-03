# EPISODIC-PRESSURE RESULT

Worker: Episodic-Pressure Worker
Date: 2026-09-30 PDT
Prereg: PREREG_EPISODIC.md (2e0c6ed10), frozen before implementation.
Status: COMPLETE

## Verdict

**EPISODIC-PRESSURE-BLEED**

All three kill bars pass. Episodic pressure bleeds sleepers that a single
wave spares: cumulative sleeper survival after 3 episodes is 7/10 vs the
9/10 single-wave baseline, losing almost exactly one unproven newcomer per
episode via revolving-door re-establishment.

## What was tested

Three separated 30-item pressure waves (flood rel 99; subjs 300..329,
400..429, 500..529) against the continuing learner (control POLICY=0,
FIFO ties; learner core carried over from churn_learn.zag, 5db2712af;
eviction policy unchanged). Between waves: earn ALL surviving flood items
(2x queries each) plus first-use probe a frozen subset of 2 sleepers
(IW1: 48,49; IW2: 46,47; IW3: all remaining unprobed survivors).
Setup E0 mirrors churn C1-C2: 12 foundation (each queried 1x), 10 Group A
(each queried 2x), 10 never-queried sleepers (40..49, rel 20).

## Measurements (3/3 byte-identical runs, sha256
d12dffa34a04f9861a5adb012f51c9c4c52ecc793346dd707296921c714d6c91,
exit 0, zero stderr)

| Check | Frozen prediction | Observed |
|---|---|---|
| EP1_SLEEP | 9/10 | 9/10 |
| EP2_SLEEP | 8/10 | 8/10 |
| EP3_SLEEP | 7/10 | 7/10 |
| IW earned-flood counts | 5, 6, 7 | 5, 6, 7 |
| EP1 first eviction | (40,20) | EVICT 40 20 |
| EP2 first eviction | (41,20) | EVICT 41 20 |
| EP3 first eviction | (42,20) | EVICT 42 20 |
| Door re-establishment | same-slot churn after each first eviction | EP1: 304..328; EP2: 400..428; EP3: 500..528 |
| Earned-flood survival | 100% across episodes 2-3 | 5/5 through EP2, 6/6 through EP3 |
| Probed sleepers survive | 48,49,46,47 all survive | yes (imp 11+ after probing) |
| IW3 unprobed-survivor probe | 3/3 (43,44,45) | 3/3 |
| FINAL_COMP | 4/4 | 4/4 |
| FINAL_FOUND | 12/12 | 12/12 |
| FINAL_EARNED | 10/10 | 10/10 |
| FOUND_EVICT | 0 | 0 |

Total EVICT lines: 86 (26 + 30 + 30), matching the predicted per-episode
counts. Every frozen prediction matched exactly, including the per-episode
first-evection victims and the door-slot churn sequences.

## Mechanism

The revolving door re-establishes every episode. Inter-wave earning
promotes all flood survivors (including the door occupant) to importance
21, so when the next wave arrives the ONLY importance-1 items left are the
unproven sleepers; the first eviction takes the lowest-index one
(41, then 42), and the door re-forms at its slot. The policy is doing
exactly what the consequence policy is designed to do: protect
demonstrated utility, sacrifice the undemonstrated. The bleed victims
(40,41,42) were never queried; no signal available to the policy could
have distinguished them from junk.

## Kill-bar evaluation

- K1 (prereg precedence): PASS. Prereg 2e0c6ed10 strictly precedes the
  implementation commit (verified with git merge-base --is-ancestor).
- K2 (episodic question answered): PASS. All 3 episodes complete;
  per-episode sleeper counts 9/10, 8/10, 7/10 exactly as frozen;
  cumulative 7/10 < 9/10 baseline; door re-establishment EVICT-confirmed
  per episode; earned-flood survival 100%; final probes and recall all at
  frozen values. Verdict per the frozen rule: BLEED.
- K3 (purity and determinism): PASS. Pure Zag, zero Python at every step
  (build, runs, analysis used only znc, shell, grep, awk, sha256sum).
  3/3 byte-identical runs, exit 0, zero stderr. No em dashes
  (check_no_dash.sh clean).

## Implementation-bug disclosure

The first build's E0 queried only (1,10) as a setup check instead of all
12 foundation items as the prereg requires ("each queried 1x"). That run
deviated from the prereg: the 11 unqueried foundation items sat at
importance 1, the door established at a foundation slot, and sleepers
survived 10/10/10 while foundation bled (FINAL_FOUND 9/12). The bug was a
clear implementation deviation from the frozen prereg, not a bar change:
E0 was corrected to query all 12 foundation items (the churn C1 block
verbatim), the binary was rebuilt, and all committed evidence comes from
the corrected 3/3 runs. The buggy outputs were overwritten, never
committed. No frozen bar was altered.

## Honest scope notes

- Exact-match retrieval; integer-coded episodes; synthetic world.
- One arm (control policy only); the LIFO-tie variant question is settled.
- The 9/10 comparator is the churn control single-wave measurement.
- The POLICY flag is a researcher-set build constant, not learned.
- The inter-wave blanket earning (earn ALL flood survivors) is the
  researcher-designed regime; see the recommendation for why it matters.

## Key follow-up finding (mechanism analysis, not a new run)

The bleed is driven by the inter-wave EARNING, not by the waves. Earning
the door occupant launders junk to proven status (importance 21), leaving
sleepers as the only unproven victims. Naive variants cannot fix this:
rotation and LIFO ties only change WHICH unproven item dies (the victim
set is the same); an age-based grace window cannot help because the
victims are old by episode 2. What would change the outcome is NOT
earning the most recent arrival: the door occupant is always the
highest-subj flood survivor, so a recency-guarded earning rule ("earn all
surviving flood except the highest-subj") would leave the unproven door
occupant in place to absorb the next wave's first eviction, predicting
9/10 sleepers across all episodes.

## Recommendation (next step for the retention-policy lane)

Run the recency-guarded earning variant: identical 3-episode battery, but
the inter-wave phase earns all surviving flood items EXCEPT the
highest-subj survivor (the prior wave's door occupant). Frozen prediction:
EP1/EP2/EP3 sleepers 9/10, 9/10, 9/10 with each wave's first EVICT taking
the prior door occupant (329, then 429). Rationale: this directly tests
whether the bleed is caused by earning-laundering and whether the policy
contains episodic pressure once junk is not promoted past unproven
newcomers. If it contains (9/10), the lane closes with a concrete,
implementable earning discipline. If it still bleeds, the victim-set
analysis says no tie-break or grace variant can do better without a new
signal (provenance or probe), and the lane should close with the bleed
documented as the designed consequence-policy tradeoff.
