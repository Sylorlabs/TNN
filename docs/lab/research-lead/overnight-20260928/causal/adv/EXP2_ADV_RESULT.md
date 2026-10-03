# H-EXP2 ADVERSARY VERDICT (X-A1..X-A4)

Date: 2026-09-29. Adversary: independent H-EXP2 red team.
Prereg: adv/PREREG_EXP2_ADV.md (commit 0c6d62b9c).
Amendment: adv/PREREG_EXP2_ADV_AMEND_XA3.md (commit 5b0d3cf36).
Status of H-EXP2: SURVIVES all frozen bars, with two DOWNGRADED claims.

## Dispositions

### X-A1: unreachable pick — CONFIRMED BOUNDARY (not a kill)

S1's top pick (0,0,1)|2 requires lamp==1. Audit of all 18 episodes across
cum_B.txt, exp_obs2.txt, exp_null.txt: lamp NEVER changes (0->0 or 1->1 in
every episode; zero lamp-changing transitions). causal_world.zag line 11
documents: "lamp: never changed by actions (demonstrator-controlled)."

The mechanism selects a discriminating STATE but provides no action sequence
to REACH it. Reachability and setup planning were explicitly out of the
frozen H-EXP2 scope before results, so this does not trip any frozen bar.
DOWNGRADE: the honest description is "discriminating-state selection", not
"experiment invention" in the full planning sense. An experiment one cannot
set up is a prediction, not a procedure.

### X-A2: ranking game — PASSED (mechanism behaved as predicted)

Fixture adv/x2_game.txt produced AMBIGUOUS action 2 {s0,s2}, n=5 ranked
experiments, top pick (0,0,1)|2 with ndiff=2, exactly as frozen-predicted.
Byte-identical over 3 runs (adv/evidence/x2_game_raw.txt).

The attack did not kill: every one of the 5 emitted states genuinely
discriminates. But it confirms the interpretation downgrade: ndiff has no
validated information-theoretic basis, the state-index tie-break is pure
enumeration order, and rank [1] (2,0,0)|2 also scores ndiff=2. DOWNGRADE:
"top-ranked = most informative experiment" is an UNSUPPORTED interpretation.
The defensible claim is "ranked by a crude disagreement-count proxy".

### X-A3: different variable pair — ATTACK FAILED (honest negative evidence)

The frozen x3_pair.txt fixture was DEFECTIVE: executed post-prereg it
produced NO AMBIGUITY (pooled pressure outcomes 1,1,1 resolve to FX_SET(p:=1),
so split_attempt never fires). Raw output at adv/evidence/x3_pair_raw.txt,
byte-identical over 3 runs. Fixture declared VOID; transparent amendment
re-froze X-A3v2 before execution (amendment commit strictly precedes v2 run).

Adversary analysis during repair found a structural fact: {s0,s1} ambiguity
is near-UNCONSTRUCTIBLE with sensible dynamics, because two variables can
only both be split candidates when CONFOUNDED in the episode set, and
pressure (the pressurize action's direct effect variable) resists sensible
confounding with temp. Only degenerate perfect-correlation episode sets with
bizarre dynamics (pressurize decreasing pressure) produce it. This is a
domain-structure property, not a mechanism failure.

X-A3v2 ({s1,s2} on action 0/heat, sensible confounded dynamics) PASSED:
AMBIGUOUS action 0 candidates={s1,s2}, n=4 discriminating experiments,
top pick (0,0,1)|0, exactly as frozen-predicted. Byte-identical over 3 runs
(adv/evidence/x3_pair_v2_raw.txt). The invention algorithm is generic over
variable pairs AND actions by construction (bitmask-indexed candidates).
The kill criterion did not fire. Pair-generality holds for a second pair on
a second action.

### X-A4: source audit — PASSED (no hardcoding)

- No literal encoding of S1/S2 selected states (0,0,1), (0,0,0) anywhere in
  exp_invent.zag. No action-2 special casing (the cands==2 hits are
  single-candidate bitmask checks, not action checks).
- Ranking comparator is exactly (ndiff DESC, state index ASC); no hidden
  tie-breakers.
- Fixed assumptions confirmed as DISCLOSED scope, not kills: vmax()
  hardcodes 3x2x2; record arrays allocate 12 states / 108 prediction bytes;
  state index is t*4+p*2+l. No K-E3 violation.

## Final verdict

H-EXP2 SURVIVES. All four adversarial attacks either confirmed disclosed
boundaries (X-A1, X-A4), behaved exactly as predicted without killing
(X-A2), or failed honestly against a generic mechanism (X-A3v2).

DOWNGRADED claims (the adversary's yield):
1. "Experiment invention" -> "discriminating-state selection". The mechanism
   does not plan how to reach the selected state; its S1 top pick requires
   lamp control that no action provides.
2. "Top-ranked = most informative" -> "ranked by an unvalidated
   disagreement-count proxy with arbitrary enumeration-order tie-breaking".
   Every emitted state discriminates; the ranking itself is not validated.

What the adversary could NOT break: determinism (all runs byte-identical),
the ambiguity-formation logic, the generic pair/action handling, and the
absence of hardcoded answers. The S2 mirror is confirmed as a genuine
second run of the same pair, and X-A3v2 extends generality to {s1,s2} on
heat. The remaining honest limitation is that {s0,s1} ambiguity appears
unconstructible in this domain, which bounds the generality claim without
refuting it.

Evidence: adv/evidence/x2_game_raw.txt, adv/evidence/x3_pair_raw.txt,
adv/evidence/x3_pair_v2_raw.txt. Fixtures: adv/x2_game.txt, adv/x3_pair.txt
(VOID), adv/x3_pair_v2.txt.
