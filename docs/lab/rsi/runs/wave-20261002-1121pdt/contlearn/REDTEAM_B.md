# REDTEAM_B: adversarial review of the scheduling exercise (b)

Status: RED-TEAM-COMPLETE. Wave: wave-20261002-1121pdt. Lane: CONTLEARN
(queue item 9, exercise b). Date: 2026-10-02. Every attack was executed
against the frozen sources and transcripts. Nothing here moves a kill
bar.

Note: hyphens only in this document; no em or en dashes.

## Attack 1: harness-smuggled timing (does the driver decide when to fire?)

- Call-site audit: sc_sched_scan is invoked in the driver's choke point
  after EVERY event (all three kind branches), unconditionally on
  learner state. The driver cannot selectively trigger or suppress the
  scan. The cadence is uniform and disclosed; the firing decision is
  computed core-side from learner state.
- pf_propose has exactly 1 call site per core, inside sc_sched_scan.
  The driver contains 0 pf_propose/pf_find calls (comment-excluded
  grep). No harness path writes proposals.
- Attack outcome: FAILED. The harness provides only the uniform
  cadence; the timing decision is learner-side.

## Attack 2: fixed-position hypothesis (does the fire track position, not state?)

- B-S1: the treat scheduler fires at evidx 5 in schedule A and evidx 83
  in schedule B (|83-5|=78 >= 50). A position-driven firer predicts
  identical evidx; the observed separation kills it.
- The two schedules place the three 850-misses at different positions
  (3/4/5 vs 21/52/83) among 18-90 interference events that never touch
  relation 850. The fire tracks the 3rd miss in both.
- Attack outcome: FAILED.

## Attack 3: the costume test (can a state-blind scheduler produce the same observables?)

- The costume fires at evidx 12 in both schedules, with fire-time
  unccount 4 (schedule A) vs 0 (schedule B). It produces the PROPOSAL
  line without the triggering state, proving state-blindness.
- The costume CANNOT produce B-S1 (its evidx is identical across
  schedules) and CANNOT produce the treat core's fire-time unccount=3
  in both schedules. The observables discriminate.
- Attack outcome: FAILED (the control does its job).

## Attack 4: negation control (does the scheduler fire without the state?)

- Ad-hoc red-team probe (rt_neg, not a verdict input): treat core run
  with only 2 UNCERTs for kind 850 ever accumulating. Result: no
  SCHED_FIRE, no PROPOSAL. The scheduler genuinely requires the
  threshold state; it does not fire spuriously.
- Attack outcome: FAILED.

## Attack 5: query-counting vs uncertainty (is it really UNCERT state?)

- The scheduler counts tag-30 UNCERT nodes (field24==850), not queries.
  UNCERT nodes are reified only on the miss path (miss_inquire); exact
  hits create none. In this battery all 850-queries miss until the
  episode, so 3 misses = 3 UNCERTs; the battery does not separate
  "3rd query" from "3rd UNCERT". Conceded limitation: the
  query-vs-uncertainty distinction is real in the mechanism but not
  differentially exercised here. The claim is "fires on accumulated
  UNCERT state", which the white-box SCHED_FIRE unccount=3 lines
  confirm directly.
- Attack outcome: PARTIALLY SUSTAINED as a scope note; the counted
  quantity is verified to be UNCERT nodes, not a query counter.

## Attack 6: episode authenticity (did the scheduler really initiate a learning episode?)

- After SCHED_FIRE, the episode query (98301,850) engages the trial
  (MACHINERY line, previously MACHINERY_SKIPPED), promotes a MAP for
  (98301,850) answering 98321 via the 860/861 chain, with type-1 DEP
  edges to both chain-fact nodes and to the proposal node
  (EPISODE_OK 1/1 white-box). Before the fire, the same query was
  refused by the gate. The proposal causally enables the episode.
- Attack outcome: FAILED.

## Findings carried to the verdict

- The learner-scheduled initiation claim survives all six attacks
  within its disclosed bound: proposal timing is driven by
  accumulated UNCERT learner state, schedule-independent, with a
  working negation control and a discriminating costume.
- Conceded bounds: proposal content is a fixed template (caveat 1);
  the scan cadence is fixed and disclosed; the scheduler targets the
  UNCERT subject (it does not choose what to learn about in a
  stronger sense); query-vs-uncertainty is not differentially
  exercised. Caveats 1, 3, 5, 6 bind. This is L2 evidence
  (state-driven control of initiation timing), not L3, not agency.
- No bar was moved. PREREG_B_AMEND1 corrected a prediction (B-S3
  3->4) transparently before implementation; the bar's logic
  (state-blindness) is unchanged and satisfied.
