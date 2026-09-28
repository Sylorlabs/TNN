# PREREG — V4 confirmatory trial: two-tier corroborated-sequence rule

**STATUS: HELD. DO NOT RUN. Awaiting Micah's explicit word.**
Drafted 2026-09-24 by the PAMs Round-2 debate crew (round 3) as a document
only. No trial is authorized; no build is authorized; no battery may be run
under this prereg until Micah says go.

## 1. Question under test

Micah ruled the pointwise-revision ban MODIFIED: single-trial revision is
proven unsafe (trial 1145: WRONG, conf=874, margin=10410, strong=1, agree=1,
dominated its correct incumbent on every axis), and revision on a single
AGREEING PAIR is proven unsafe (contradiction-matrix cell CC1: two WRONG
high-conf corroborators agreeing within tolerance trigger REVISED_INSTALL —
false permanent install under both corroboration gates G1 and G2,
preregistered known-unsafe, 30/30 matrix cells otherwise PASS).

The two-tier rule: revision is permitted only for corroborated sequences of
length ≥2 (two agreeing high-conf PASS challengers) AND the pair passes the
CC1 margin guard (agreement above a frozen separation margin) AND neither
challenger is within F5 exemplar distance of the negative bank.

Question: does this live machinery recover the R2-4 withheld truths
(621 conflict-withheld, offline replay 621/621 recovered at 0 false installs)
at 0 false installs on frozen adversarial streams, and does it move RK-3
toward the 85% bar?

## 2. Method (test-first discipline)

- Pure Zag. Zero RNG. Three runs, byte-identical (sha256 match) or the run
  is void.
- This prereg is committed ALONE before any build output exists. The gate
  under test is implemented from this prereg, not the reverse.
- Battery: frozen RK-3 battery (1,102 correct high-conf trials), frozen
  red-team streams (clean / withhold / install / decoy, 288+288+44+52 as in
  the hardening battery), frozen contradiction-matrix CC1 cell trials.

## 3. Kill bars (any one kills)

- KB-V4-1 (liveness): RK-3 < 85% → KILL. The two-tier machinery exists only
  to reach the bar the offline replay promised (86.6% claim); below 85% it is
  machinery without a mission.
- KB-V4-2 (safety): any false install on the frozen decoy or install streams
  → KILL. H6's bar (0 false on clean) is the floor; a revision mechanism
  must not score below the no-revision gate on safety.
- KB-V4-3 (CC1 regression): any REVISED_INSTALL on the CC1 wrong-pair
  trials → KILL. The margin guard + F5 preconditions are load-bearing; if the
  live pair-path re-opens the preregistered-unsafe cell, the two-tier rule
  is dead in its live form.
- KB-V4-4 (determinism): runs not byte-identical → VOID, rebuild, re-run.

## 4. What this prereg does NOT cover

- The F5 300-near-exemplar-correct-percept red-team (in flight, separate crew,
  separate prereg).
- The CC1 margin-guard verification (in flight, separate crew).
- Sense-side work on the 278 never-PASS trials (offense leg, separate preregs).

## 5. Governance

Held per Micah's ruling 2026-09-24: the V4 confirmatory trial for the
two-tier rule does not run without his word. Drafting the prereg is not
authorization. When he says go, the test coordinator dispatches a crew under
this prereg, committed alone before any build.
