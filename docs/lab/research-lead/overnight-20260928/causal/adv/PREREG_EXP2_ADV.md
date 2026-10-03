# Preregistration: H-EXP2 Adversary (X-A1..X-A4)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any adversarial
fixture is created or executed. No Python at any stage.

## Mission

Independently attack H-EXP2 (experiment invention, EXP2_RESULT.md,
verdict SURVIVES bounded). Assume the claim is false. Find the strongest
alternative explanation or the narrowest true scope.

## Baseline (reproduced before writing this prereg)

Rebuilt exp_invent from committed exp_invent.zag with pinned znc
2026.07.0-dev. Outputs on cum_B.txt, exp_obs2.txt, exp_null.txt are
byte-identical to evidence/exp2_s1.txt, exp2_s2.txt, exp2_s0.txt.
The reported S1/S2/S0 behavior is confirmed: top picks (0,0,1)|2,
(0,0,0)|2, and honest abstention on S0.

## Attack X-A1: Unreachable pick (boundary probe)

Construction: No new fixture. Audit the S1 top pick (0,0,1)|2 against
the domain's action repertoire. The pick requires lamp==1 (s2==1).
There is no lamp-toggle action in the domain (actions 0..3; lamp is
demonstrator-controlled per EXP2_RESULT.md). The learner therefore
cannot set up its own top pick.

Kill criterion: NONE. The frozen H-EXP2 prereg explicitly places setup
planning out of scope ("the invention selects (state, action), not the
action sequence to reach the state. Reachability-aware ranking is future
work"). Killing on an explicitly excluded dimension would be post-hoc
bar strengthening, which is forbidden. This attack is a boundary probe.

Predicted outcome: CONFIRMED BOUNDARY. The invention ranks hypothetical
states by prediction disagreement; it cannot distinguish a runnable
experiment from a hypothetical one. The "experiment invention" label
overstates "discriminating-state selection". Document, do not kill.

## Attack X-A2: Ranking game (downgrade probe)

Construction: (a) Cite the frozen S1 output: 3 ranked experiments, all
ndiff=1, top pick = index-minimal (0,0,1), index 1. The frozen prereg
itself admits "ndiff never exceeded 1 in these fixtures, so index order
decided." (b) Construct fixture x2_game.txt (frozen below) with
ambiguity {s0,s2} where discriminating states have varying ndiff, to
exercise the ndiff-DESC leg.

Frozen x2_game.txt:
```
# X-A2: ndiff varies; probe the ranking proxy
T 0 0 0 | 2 | 0 1 0
T 1 0 0 | 2 | 1 1 0
T 2 0 1 | 2 | 1 0 1
```
Predicted: action 2 AMBIGUOUS {s0,s2} (s0 groups: t==0 p:=1, t==1 p:=1,
t==2 t:=1; s2 groups: l==0 p:=1, l==1 t:=1; s1 groups mixed).
Discriminating states include (0,0,1) [s0->(0,1,1), s2->(1,0,1),
differ v0,v1, ndiff=2] and (1,0,1) [s0->(1,1,1), s2->(1,0,1),
differ v1, ndiff=1]. Predicted top pick: (0,0,1)|2 by ndiff DESC.

Kill criterion: NONE on the frozen bars. Every ranked record
discriminates by construction (the code skips agreeing states), so K-E1
cannot be violated through ranking. This attack targets the
interpretation of "TOP PICK", not a frozen bar.

Predicted outcome: DOWNGRADE of "top pick" optimality. The ranking
(ndiff DESC, index ASC) is an unvalidated informativeness proxy:
ndiff counts differing variables with no information-theoretic
justification, and the index-ASC tiebreak is pure enumeration order
(t,p,l lexicographic), which has no epistemic basis. The mechanism
enumerates discriminating states correctly, but "top" is not principled.
Document with the x2_game trace.

## Attack X-A3: Variable pair s0 vs s1 (generality kill attempt)

Construction: fixture x3_pair.txt (frozen below). Designed so action 2
becomes AMBIGUOUS with candidates {s0,s1} (not the tested {s0,s2} pair).

Frozen x3_pair.txt:
```
# X-A3: s0-vs-s1 ambiguity (adversarial, frozen)
T 0 0 0 | 2 | 0 1 0
T 1 0 0 | 2 | 1 1 0
T 2 1 0 | 2 | 2 1 0
```
Predicted: s0 groups resolve (t==0 p:=1, t==1 p:=1, t==2 unch);
s1 groups resolve (p==0 p:=1, p==1 unch); s2 has one value (not a
candidate). Action 2 AMBIGUOUS {s0,s1}. Predicted discriminating
states: (2,0,0) [s0->(2,0,0), s1->(2,1,0), differ v1] index 8, and
(2,0,1) [s0->(2,0,1), s1->(2,1,1), differ v1] index 9.
Predicted top pick: (2,0,0)|2.

Kill criterion: If the invention, on a valid two-candidate ambiguity
over a different variable pair, emits NO DISCRIMINATING EXPERIMENT,
crashes, or emits a top pick whose candidates do NOT actually differ
(i.e., violates the K-E1 property on this fixture), then the
"Algorithm (frozen, generic)" claim is false and the mechanism is
pair-specific. Verdict: H-EXP2 DOWNGRADED to "discriminating-state
selection for the s0/s2 pair only"; the S2 mirror does not establish
pair-generality (S2 is also {s0,s2}). K-E3's "not heuristic" is
undercut because the selection would be effectively tuned to one pair.

Predicted outcome: The mechanism is generic by construction
(candidates from bitmask, pred_under indexed by v), so X-A3 is
predicted to CONFIRM pair-generality with top pick (2,0,0)|2.
A kill here would be surprising and significant.

## Attack X-A4: Source audit (kill attempt)

Construction: independent grep audit of exp_invent.zag, plus code
inspection of the enumeration/ranking for hardcoded assumptions.

Checks:
(a) No integer-literal triple encoding (0,0,1) or (0,0,0) as a picked
    state in the invention code (lines 1002+). Redo of K-E3(a).
(b) No subtler answer literals: the S1/S2 picks in any spacing,
    e64(0)/e64(1) sequences that assemble a pick.
(c) Document hardcoded enumeration assumptions: vmax() returns
    2/1/1 (fixed 3x2x2 space, 12 states); z_alloc(12)/z_alloc(108)
    record buffers; sort index t*4+p*2+l (bijective only for this
    fixed space). The "generic" enumeration is fixed to 12 states.

Kill criterion: If check (a) or (b) finds a literal encoding of a
picked state in the invention code, K-E3(a) is violated: H-EXP2 KILLED.
Check (c) is a boundary probe: the fixed 12-state space is consistent
with the frozen fixtures and the disclosed 3-variable scope, so no
bar violation is predicted; document as a generality boundary.

Predicted outcome: (a)(b) clean (the researcher already grep-verified);
(c) confirmed as documented boundary. No kill predicted.

## Verdict rules

- KILL: only on a frozen-bar violation (X-A3 property fail, X-A4
  literal found). Name the exact bar.
- DOWNGRADE: X-A2 ranking proxy; X-A1/X-A4(c) boundaries. Narrow the
  claim; do not overturn the S1/S2/S0 verdicts.
- CONFIRM: X-A3 predicted to confirm pair-generality.

## Scope

Pure Zag only. No Python. New fixtures x2_game.txt, x3_pair.txt are
adversarial and frozen here; they are not part of H-EXP2's claim.
Raw outputs go to adv/evidence/. This prereg commit must strictly
precede all attack execution commits.
