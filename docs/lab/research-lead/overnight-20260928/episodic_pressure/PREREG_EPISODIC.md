# PREREG: Episodic-Pressure Experiment (EPISODIC)

Status: FROZEN. Committed alone before any implementation.
Date: 2026-09-30 PDT.
Parent: CHURN-REVISION-PASS (prereg 18fb10434, implementation 5db2712af);
LEARNER-STRESS-PASS (prereg 4ca3a7196, implementation daa9bf2fc).

## Question

Does repeated, separated memory pressure bleed never-queried newcomers
("sleepers") that a single pressure wave spares? The churn revision found
the revolving-door mechanism: one slot absorbs all sustained evictions, so
a single 30-item wave killed only 1/10 sleepers (9/10 survived; the
policy-fine falsifier triggered; the single-wave churn hypothesis was
REJECTED). Between waves, surviving flood items are earned (queried),
changing the eviction landscape: the next episode's first eviction should
fall on the next-lowest-index unproven sleeper, and the door should
re-establish there. This experiment tests the hypothesis in the regime
where it might actually hold.

## Design (one arm: control POLICY=0, FIFO ties, the current policy)

Setup (E0), mirrors churn C1-C2 exactly:
- 12 foundation rules (subj 1..9, rel 10/11/12), each queried 1x.
- 10 Group A newcomers (subj 10..19, rel 30), each queried 2x (earned).
- 10 sleepers (subj 40..49, rel 20), NEVER queried.

Episode e in {1,2,3}:
- Wave: 30 new flood items, rel 99, subj 300+100*(e-1) .. 329+100*(e-1)
  (waves use 300..329, 400..429, 500..529), each learn()ed once.
- Inter-wave: earn ALL surviving flood items (2x queries each); first-use
  probe a frozen subset of 2 sleepers: IW1 probes 48,49; IW2 probes 46,47;
  IW3 probes all remaining unprobed survivors (the highest-index
  sleepers are never eviction targets, so probing them does not perturb
  the bleed measurement; it tests earning-by-probing orthogonally).

Final (after IW3): 4 two-hop compositions through sleeper premises;
final foundation 12/12 and Group A 10/10 recall; FOUND_EVICT.

## Frozen predictions

- E1_SLEEP 9/10 (replicates churn control C3); first eviction (40,20);
  door re-establishes at its slot for the remaining 25 evictions.
- E2_SLEEP 8/10; first eviction (41,20); door re-establishes at its slot.
- E3_SLEEP 7/10; first eviction (42,20); door re-establishes at its slot.
- IW earned-flood counts: 5, 6, 7 (door occupant included from IW2 on).
- Cumulative sleeper survival after 3 episodes: 7/10, vs the 9/10
  single-wave baseline from the churn control arm.
- Earned flood: 100% of inter-wave-earned flood items survive episodes 2-3
  (importance 21 protects them; only unproven newcomers are evicted).
- Probed sleepers (48,49 after IW1; 46,47 after IW2): all survive.
- IW3 first-use probe of unprobed survivors (43,44,45): 3/3.
- Compositions through sleeper premises: 4/4.
- Foundation 12/12, Group A 10/10, FOUND_EVICT 0 at final.

## Verdict rule

- EPISODIC-PRESSURE-BLEED: cumulative sleeper survival < 9/10 AND the
  per-episode revolving-door re-establishment is EVICT-confirmed (each
  episode's first eviction takes the predicted next-lowest-index unproven
  sleeper, and subsequent evictions of that episode hit the same slot).
- EPISODIC-PRESSURE-CONTAINED: cumulative sleeper survival >= 9/10
  (the policy holds even under episodic pressure).
Both branches are honest outcomes. The CONTAINED branch is the falsifier:
it would show the revolving-door protection extends across episodes.

## Kill bars

- K1: this prereg strictly precedes implementation (merge-base verified).
- K2: all 3 episodes complete; per-episode sleeper counts, cumulative
  survival vs the 9/10 baseline, EVICT door pattern, earned-flood
  survival, final probes, all measured against the frozen predictions;
  verdict per the rule above.
- K3: pure Zag, zero Python at every step; 3/3 byte-identical runs,
  exit 0, zero stderr; no em dashes (shell-only check_no_dash.sh).

## Honest scope

- Exact-match retrieval; integer-coded episodes; synthetic world.
- One arm (control policy only); the LIFO-tie variant question is settled
  (rejected hypothesis; frozen bar blocked adoption).
- The 9/10 comparator is the churn control single-wave measurement.
- The POLICY flag is a researcher-set build constant, not learned.
- Learner core is carried over byte-identical from churn_learn.zag
  (5db2712af) except the new main(); the eviction policy is unchanged.
