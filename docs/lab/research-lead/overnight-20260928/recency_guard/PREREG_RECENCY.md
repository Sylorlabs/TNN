# PREREG: Recency-Guarded Earning Experiment (RECENCY-GUARD)

Status: FROZEN. Committed alone before any implementation.
Date: 2026-09-30 PDT.
Parent: EPISODIC-PRESSURE-BLEED (prereg 2e0c6ed10, evidence in 9c6ee8ba8,
verdict+provenance 136588de5); CHURN-REVISION-PASS (18fb10434, 5db2712af).

## Question

Does a recency-guarded earning discipline contain the episodic sleeper bleed?
The episodic experiment showed 9/10 -> 8/10 -> 7/10 sleepers across three
separated 30-item waves with inter-wave earning: each new episode sacrificed
the next-lowest-index unproven sleeper because inter-wave earning laundered
all surviving flood junk to proven status (importance 21), leaving sleepers
as the only unproven eviction victims. Mechanism analysis: naive variants
(rotation, LIFO ties, age-grace) cannot change the victim set, but NOT
earning the most recent arrival (the prior wave's door occupant, always the
highest-subj flood survivor; the rule needs no door knowledge) leaves the
unproven door occupant in place to absorb the next wave's first eviction,
re-establishing the revolving door at its slot instead of at a sleeper slot.

## Design (one arm: control POLICY=0, FIFO ties; single changed rule)

Identical to the episodic battery except the inter-wave earning rule.

Setup (E0), mirrors churn C1-C2 and episodic E0 exactly:
- 12 foundation rules (subj 1..9, rel 10/11/12), each queried 1x.
- 10 Group A newcomers (subj 10..19, rel 30), each queried 2x (earned).
- 10 sleepers (subj 40..49, rel 20), NEVER queried.

Episode e in {1,2,3}:
- Wave: 30 new flood items, rel 99, subj 300+100*(e-1) .. 329+100*(e-1).
- Inter-wave (RECENCY-GUARDED): earn all surviving flood items with 2x
  queries each EXCEPT the highest-subj survivor (the most recent arrival).
  Then first-use probe a frozen subset of 2 sleepers: IW1 probes 48,49;
  IW2 probes 46,47; IW3 probes all remaining unprobed survivors (43,44,45).

Final (after IW3): 4 two-hop compositions through sleeper premises;
final foundation 12/12 and Group A 10/10 recall; FOUND_EVICT.

The learner core is carried over byte-identical from episodic.zag
(9c6ee8ba8) except the earning function (earn_all_flood_except_max) and
main(); the eviction policy is unchanged.

## Frozen predictions

- E0: E0_SLEEP 10/10, E0_EARNED 10/10 (identical setup to episodic).
- EP1 (unchanged regime): first eviction (40,20); door re-establishes at its
  slot for the remaining 25 evictions; EVICT victims: (40,20) then
  (304..328,99); EP1_SLEEP 9/10.
- IW1: 5 flood survivors {300,301,302,303,329}; IW1_EARNED 4 (329 excluded);
  IW1_PROBE 2/2.
- EP2: first eviction (329,99) at the door slot; door re-establishes there;
  EVICT victims: (329,99) then (400..428,99); ZERO sleeper evictions;
  EP2_SLEEP 9/10.
- IW2: 5 flood survivors {300,301,302,303,429}; IW2_EARNED 4 (429 excluded);
  IW2_PROBE 2/2.
- EP3: first eviction (429,99) at the door slot; door re-establishes there;
  EVICT victims: (429,99) then (500..528,99); ZERO sleeper evictions;
  EP3_SLEEP 9/10.
- IW3: 5 flood survivors {300,301,302,303,529}; IW3_EARNED 4 (529 excluded);
  IW3_PROBE_UNPROBED 3/3.
- Total EVICT lines: 86 (26+30+30), same count as episodic, different victims.
- Earned flood: 100% of earned flood items survive episodes 2-3.
- Probed sleepers (48,49 after IW1; 46,47 after IW2): all survive.
- Compositions through sleeper premises: 4/4.
- Foundation 12/12, Group A 10/10, FOUND_EVICT 0 at final.
- Cumulative sleeper survival after 3 episodes: 9/10, vs the 7/10 episodic
  baseline and the 9/10 single-wave baseline from the churn control arm.

## Verdict rule

- RECENCY-GUARD-CONTAINED: cumulative sleeper survival >= 9/10 AND the
  door-absorption mechanism is EVICT-confirmed (EP2 first eviction takes
  (329,99), EP3 first takes (429,99), zero sleeper evictions in EP2/EP3).
  Closes the lane with the concrete earning discipline: inter-wave earning
  skips the most recent arrival.
- RECENCY-GUARD-STILL-BLEEDS: cumulative sleeper survival < 9/10 OR any
  sleeper evicted in EP2/EP3. Closes the lane with the bleed documented as
  the designed consequence-policy tradeoff (protect demonstrated utility,
  sacrifice the undemonstrated); no further tie-break or grace variants.
This is the terminal experiment for the retention-policy lane; no follow-up
variants after this regardless of outcome.

## Kill bars

- K1: this prereg strictly precedes implementation (merge-base verified).
- K2: all 3 episodes complete; per-episode sleeper counts, cumulative
  survival vs the 7/10 episodic baseline, EVICT door-absorption pattern,
  earned counts, final probes, all measured against the frozen predictions;
  verdict per the rule above.
- K3: pure Zag, zero Python at every step; 3/3 byte-identical runs,
  exit 0, zero stderr; no em dashes (shell-only check_no_dash.sh).

## Honest scope

- Exact-match retrieval; integer-coded episodes; synthetic world.
- One arm (control policy only); the LIFO-tie variant question is settled.
- The 9/10 comparator is the churn control single-wave measurement; the
  7/10 comparator is the episodic three-wave measurement.
- The POLICY flag and the recency-guard rule are researcher-set build
  constants, not learned.
- The eviction policy (importance formula, FIFO ties, revolving door) is
  unchanged from churn/episodic; only the earning rule differs.
