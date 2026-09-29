# PREREG AMENDMENT X-A3: fixture replacement (transparent re-freeze)

Date: 2026-09-29. Amends PREREG_EXP2_ADV.md X-A3. Original kill bar is NOT
weakened. The frozen fixture was defective, not the bar.

## What happened

The frozen X-A3 fixture (adv/x3_pair.txt) was executed AFTER the prereg commit
0c6d62b9c and produced:

  NO AMBIGUITY: no competing hypotheses, nothing to invent.

Raw output saved at adv/evidence/x3_pair_raw.txt (byte-identical over 3 runs).

Root cause: the adversary's hand-derived prediction was wrong. The pooled
action-2 episodes (0,0,0)->(0,1,0); (1,0,0)->(1,1,0); (2,1,0)->(2,1,0) have
pressure outcomes 1,1,1, so the pooled effect resolves to FX_SET(p:=1) and
split_attempt is never reached. The fixture does not construct an ambiguity
at all, so the X-A3 kill criterion (which requires a VALID two-candidate
ambiguity) cannot fire on it. The fixture is VOID, not the attack.

## Why {s0,s1} is near-unconstructible (adversary analysis)

Attempting to repair the fixture revealed a structural fact worth recording.
For two variables to BOTH be split candidates, each must partition the
episodes into fully resolved groups. Because group resolution is permissive
(a group resolves if a single UNCH/SET/ADD description covers it, even when
member episodes have different raw transitions), two variables can only both
be candidates when they are CONFOUNDED in the episode set: the outcome must be
simultaneously describable as a function of either variable alone.

For pair {s0,s1} on the pressurize action this is near-impossible with
sensible dynamics, because pressure (s1) is the action's direct effect
variable: any episode pattern that makes s1's groups resolve also makes the
pooled pressure effect resolve (all groups must agree on pressure outcomes
per pressure value, and the pooled set then ends at a consistent value), so
no split is triggered. The only {s0,s1} constructions found require
degenerate perfect-correlation episode sets with bizarre dynamics
(pressurize decreasing pressure). This is a property of the domain's causal
structure, not a mechanism failure, but it means the {s0,s1} pair cannot
serve as a fair generality probe.

## Replacement fixture: X-A3v2

Pair {s1,s2} (pressure vs lamp) on action 0 (heat), with sensible confounded
dynamics: heat raises temp by 1 iff pressure is 0; lamp is a confounder
correlated with pressure in the observed episodes.

Frozen fixture adv/x3_pair_v2.txt:

  # X-A3v2: s1-vs-s2 ambiguity on heat (adversarial, frozen)
  T 0 0 0 | 0 | 1 0 0
  T 1 0 0 | 0 | 2 0 0
  T 0 1 1 | 0 | 0 1 1
  T 1 1 1 | 0 | 1 1 1

Frozen predictions:
- Learning: ep1,ep2 resolve (t+1). ep3 breaks pooled resolution (v0
  outcomes 1,2,0 are not UNCH/SET/ADD). split_attempt: s0 NOT a candidate
  (t==0 group mixes t+1 and unch). s1 IS a candidate (p==0 -> ADD(+1),
  p==1 -> UNCH). s2 IS a candidate (l==0 -> ADD(+1), l==1 -> UNCH).
  Entry becomes AMBIGUOUS action 0 candidates={s1,s2}.
- Invention: enumerates 12 states. Discriminating states are exactly the
  four where pressure and lamp disagree with their observed correlation:
  (0,0,1) idx1, (0,1,0) idx2, (1,0,1) idx5, (1,1,0) idx6. All differ on v0
  only (ndiff=1). Expected n=4.
- Expected TOP PICK: state (0 0 1) | 0 (lowest index among ndiff=1 ties).

Kill bar (unchanged in force, pair updated): if the invention, on this valid
two-candidate {s1,s2} ambiguity over a different action, crashes, emits zero
discriminating experiments, or emits a top pick whose candidate predictions
AGREE, the generic algorithm claim FAILS and H-EXP2 must be narrowed to the
tested {s0,s2} pair on the pressurize action. If it emits the predicted
discriminating set with top pick (0,0,1)|0, X-A3v2 PASSES and pair-generality
is confirmed for a second pair on a second action.

This amendment is committed BEFORE x3_pair_v2.txt is executed.
