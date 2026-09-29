# Preregistration: H-EXP7 Independent Red Team (Adversary)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
attack fixture is written or any attack is executed. No Python
at any stage. Binaries in /tmp only, not committed.

## Mission

Independently attack the H-EXP7 repair claim. Assume it is
false. H-EXP7 claims SURVIVES (5/5): the TRANSITION TABLE and
TRANSITION-EVIDENCE lines close the two H-EXP6 red-team
downgrades (X-E6-1 from-blindness, X-E6-2 hidden per-action
base rate) without introducing a new overclaim.

The repair's stated purpose (PREREG_EXP7.md): "A planner at
temp==0 now sees that only action 1 ever effected the 0->2
transition" and "The 1-in-11 change no longer renders
identically to the 1-in-1 change."

## Attack hypotheses

X-E7-1 (From-value): The from-value counts are observed, but
the from-bucket is CLAMPED (raw 5 clamps to 2). The mechanism
possesses the raw from-value (ep_s) and discards the
raw-vs-clamped distinction. A from-bucket can therefore be
entirely artifactual: "from {2:c}" with zero raw from-2
transitions. A planner reading the from-value as evidence
about its own from-state is misled about reproducibility.

X-E7-2 (Rate): The (m/n) rate is change/outcome, NOT
change/attempt. The mechanism possesses the failed-attempt
episodes (from-0 no-ops have outcome temp==0, counted in
achv[a][0][0]) but the TRANSITION-EVIDENCE denominator n
counts only outcome==x episodes. A 1/1 rate can therefore
hide arbitrarily many failed from-state attempts. This is the
same information-possessed-but-discarded pattern as the
successful H-EXP6 X-E6-2 attack.

X-E7-3 (Clamp): The change predicate uses raw values
(ns != os) but buckets are clamped. A raw 5->2 transition
renders as "2->2": a self-loop inside a CHANGE table. A
"change" that renders as no-change is self-contradictory on
its face and misleads about what was observed.

X-E7-4 (Regression): Verify the 5/5 frozen H-EXP7 kill bars
still pass on the committed exp_invent7.zag. Any silent
change from the exp6 behavior (outside the 5 frozen
additions) is a finding.

## Frozen attack fixtures

All fixtures are S1 (= causal/cum_B.txt, the H-EXP6 base)
plus adversary episodes. S1 provides the ambiguity structure
that yields ranked picks. Fixture format:
T <t> <p> <l> | <a> | <nt> <np> <nl> (raw values; parse_int
accepts multi-digit non-negative integers; negative raw
values are NOT expressible).

J1 (X-E7-1, clamp-artifact from-value):
= S1 (11 episodes) plus:
T 5 0 0 | 0 | 2 0 0
T 5 0 0 | 0 | 2 0 0
(Action 0 changes temp raw 5->2 twice. Clamped: o=2, x=2.
There are ZERO raw from-2 temp changes by action 0 in J1.)
Expected honest rendering: action 0 temp==2 item shows
"from {2:2}". The attack succeeds if it does, because the
planner reads from-2 evidence that never existed in raw
terms. Control: S1 episodes give action 0 no temp->2 change
at all, so any from {2:} for action 0 temp==2 is purely the
adversary episodes.

R1 (X-E7-2, attempt-hiding rate):
= S1 (11 episodes) plus:
T 0 0 0 | 0 | 2 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 0 | 0 0 0
(Action 0: ONE temp 0->2 change, TEN temp 0->0 no-ops from
temp==0. True from-0 success rate: 1/11. The 10 no-ops have
outcome temp==0, so they do NOT enter the (m/n) denominator
for x=2.)
Expected honest rendering: action 0 temp==2 item shows
"from {0:1} (1/1)". The attack succeeds if it does, because
a perfect-looking 1/1 hides the 1/11 true from-0 rate.

C1 (X-E7-3, self-loop in change table):
= S1 (11 episodes) plus:
T 5 0 0 | 0 | 2 0 0
(Action 0 changes temp raw 5->2 once: a genuine raw change
that renders as clamped 2->2.)
The attack succeeds if the TRANSITION TABLE contains a
"2->2" cell for action 0 temp (a self-loop rendered inside a
table whose header says "change episodes"), or if the
TRANSITION-EVIDENCE from-list for temp==2 contains a from
entry equal to the to-value (o==x) for a genuine change.

## Frozen kill criteria

- KILL: any attack shows a frozen H-EXP7 kill bar (K-E7-1
  through K-E7-5) is false on the committed binary, or shows
  the TRANSITION-EVIDENCE making a factually false claim
  about the episode set (not merely a disclosed limit).
- DOWNGRADE: any attack shows the repair signal misleading a
  planner in a material way the frozen honest limits do not
  cover, while the 5/5 frozen bars still hold. The verdict
  becomes DOWNGRADED with the claim narrowed; the surviving
  bars stand.
- SURVIVES: all four attacks fail; the honest limits already
  cover the probed behaviors and no new overclaim is found.

Per-attack verdict rules (frozen):

- X-E7-1 SUCCEEDS (attack works) if J1 output shows action 0
  temp==2 with "from {2:" where the raw episodes contain
  zero from-2 changes. The legend discloses clamping but does
  NOT disclose that a from-bucket can be 100 percent
  artifact with no raw exemplar. If the output instead
  distinguishes raw from clamped (it cannot; the format has
  no such channel), the attack fails.
- X-E7-2 SUCCEEDS if R1 output shows "from {0:1} (1/1)" for
  action 0 temp==2 while the fixture contains 10 from-0
  no-ops. The (m/n) legend defines the denominator as
  "observed outcomes," so a strict reading is accurate; the
  attack succeeds on the planner-misleading criterion (a
  perfect rate hiding a 1/11 true rate), which the honest
  limits ("does not measure robustness") do not cover as an
  active-misleading hazard.
- X-E7-3 SUCCEEDS if C1 output renders "2->2" in the
  TRANSITION TABLE or an o==x from entry for a genuine raw
  change. The honest limit documents "5->2 renders as 2->2"
  as a rendering convention; the attack succeeds if the
  rendering is shown to be self-contradictory in context
  (a change tabulated as a self-loop), which the limit does
  not address.
- X-E7-4 SUCCEEDS (regression clean) if K-E7-1, K-E7-2,
  K-E7-3, K-E7-4, K-E7-5 all reproduce on the committed
  binary. Any failure is reported as KILL.

## Honest limits of this red team (frozen)

- Single-episode non-reproducibility is already disclosed
  ("A single transition episode does not prove the action
  can reproduce the transition on demand"); attacks do not
  target it.
- The clamp rendering convention ("5->2 renders as 2->2")
  is disclosed; X-E7-1 and X-E7-3 target what the disclosure
  does NOT cover (artifactual from-buckets with no raw
  exemplar; self-loop changes in a change table).
- Cross-variable confounding (the transition depending on
  another variable's value) is disclosed as "not causal
  attribution" and "state-as-combination reachability is not
  computed"; attacks do not target it.
- Negative raw values cannot be expressed in fixtures
  (parse_int reads digits only); clamp-artifact attacks use
  raw > 2 only.
- Classification target remains bounded L2; no L3 claim is
  attacked because none is made.

## Method (frozen)

1. Commit this prereg alone.
2. Write J1, R1, C1 fixtures (Zag fixture text files).
3. Build exp_invent7.zag with znc 2026.07.0-dev in /tmp;
   verify byte-identical to committed source via cmp of a
   fresh checkout (or build from the committed path
   directly, which is what was done).
4. Run binary on J1, R1, C1 (3/3 determinism each) and on
   the 7 frozen fixtures for X-E7-4.
5. Judge each attack against the frozen criteria above.
6. Write EXP7_ADV_RESULT.md with verdict, evidence, and
   commit lineage. Commit prereg, fixtures, result, and raw
   evidence (only owned files).
