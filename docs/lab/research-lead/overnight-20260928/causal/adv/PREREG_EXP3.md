# Preregistration: H-EXP3 (Reachability-Aware Experiment Selection)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any implementation
of exp_invent3.zag. No Python at any stage.

## Mission

Address the two DOWNGRADED claims from the H-EXP2 adversary
(adv/EXP2_ADV_RESULT.md, verdict SURVIVES with downgrades):

1. X-A1: "experiment invention" -> "discriminating-state selection". The
   mechanism selects states but plans no way to reach them. S1's top pick
   (0,0,1)|2 requires lamp==1, but lamp never changes in any episode
   (demonstrator-controlled per causal_world.zag line 11).
2. X-A2: "top-ranked = most informative" -> "ranked by an unvalidated
   disagreement-count proxy". ndiff has no information-theoretic basis;
   the state-index tiebreak is pure enumeration order.

## Hypothesis H-EXP3

The downgrades can be addressed WITHOUT changing the selection mechanism:
(1) the learner can compute per-variable controllability from its own
episodes and explicitly flag picks requiring uncontrollable variables;
(2) the ranking can be explicitly scoped as a heuristic with a verified
safety property (every emitted state genuinely discriminates).

## Design (frozen)

exp_invent3.zag is built by copying exp_invent.zag VERBATIM and adding:

### A. Controllability computation (new helper)

fn compute_controllable(W): for v in 0..2, controllable[v] = 1 if there
exists an EP_ACT episode with ns[v] != s[v], else 0. This uses only the
learner's own episode data. No domain knowledge.

Predicted on S1 (cum_B.txt): temp controllable (heat/cool change it),
pressure controllable (pressurize/depressurize change it), lamp
UNCONTROLLABLE (0 changes in all episodes).

### B. Reachability annotation (per ranked pick)

For each ranked discriminating state, emit:
- "REACHABILITY:" followed by per-variable controllability.
- If any variable is uncontrollable: "FLAG: NEEDS-EXTERNAL-SETUP"
  with the required values of uncontrollable variables, e.g.
  "requires lamp==1; lamp: 0 changes in N episodes (not action-controllable)".
- If all variables controllable: "AGENT-SETUP-ABLE".

The ranked list is still emitted (selection unchanged), but no pick is
silently recommended as runnable. The top pick carries its flag.

### C. Ranking explicitly scoped as heuristic

- Output header changes from "RANKED EXPERIMENTS" to
  "RANKED EXPERIMENTS (heuristic: ndiff DESC, state-index ASC;
  informativeness NOT validated)".
- "TOP PICK" becomes "TOP PICK (by heuristic)".
- Add explicit safety verification: after ranking, re-verify each
  emitted state (all candidates resolve AND disagree). Emit
  "RANKING SAFETY: all N emitted states verified discriminating."
  This is a real check, not a label: if any emitted state failed,
  it would be reported.

### D. Theoretical note (documented, not a bar)

In the 2-candidate case, ANY discriminating state yields the same
information (1 bit: which candidate predicted correctly). ndiff cannot
correspond to "more informative" because the information gain is
identical regardless of how many output variables differ. This is WHY
the ranking is unvalidatable as informativeness, and why the safety
property (all emitted states discriminate) is the correct validated
claim.

## Frozen fixtures

Same as H-EXP2: S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt. No new fixtures. This ensures K-E3-3
(no regression) is meaningful.

## Kill bars (frozen)

- K-E3-1 (unreachable picks flagged): On S1, the output explicitly
  flags the top pick (0,0,1)|2 as NEEDS-EXTERNAL-SETUP, naming lamp
  as uncontrollable with its change count (0). The flag must appear
  in the raw output; a silently recommended pick fails this bar.
  Also: the controllability report must show temp=controllable,
  pressure=controllable, lamp=uncontrollable on S1.

- K-E3-2 (ranking scoped as heuristic): The output contains the
  explicit heuristic disclaimer on the ranked list header AND on the
  top pick line. The RANKING SAFETY line appears with N matching the
  number of emitted ranked states, all verified discriminating.

- K-E3-3 (no regression on H-EXP2 bars): All four original H-EXP2
  kill bars still PASS on the same fixtures:
  (a) K-E1: S1 top pick (by heuristic) is still (0,0,1)|2 with
  differing predictions; (b) K-E2: trace still names candidates and
  differing vars; (c) K-E3: S0 abstains, S2 picks (0,0,0)|2,
  no hardcoded state literals; (d) K-E4: determinism holds.

- K-E3-4 (determinism): 3 consecutive runs per fixture are
  byte-identical (md5).

## Scope and honest limits (frozen)

- This does NOT add setup planning (action sequences to reach states).
  That remains out of scope. H-EXP3 adds reachability AWARENESS
  (flagging), not reachability PLANNING.
- Controllability is computed from observed episodes only. A variable
  that is controllable but never happened to change in the episodes
  will be marked uncontrollable. This is conservative and honest:
  the learner only knows what it has seen.
- The ranking heuristic is unchanged (ndiff DESC, index ASC). H-EXP3
  does not claim to improve the ranking, only to scope it honestly
  and verify its safety.
- Not L3. Bounded L2 infrastructure repair addressing red-team
  downgrades.

## Predictions (not bars)

- S1: controllability = temp:1, pressure:1, lamp:0. Top pick
  (0,0,1)|2 flagged NEEDS-EXTERNAL-SETUP (requires lamp==1).
  All 3 ranked picks flagged (all require lamp at some value).
  RANKING SAFETY: 3/3 verified.
- S2: same controllability. Top pick (0,0,0)|2 flagged
  NEEDS-EXTERNAL-SETUP (requires lamp==0; lamp uncontrollable).
  RANKING SAFETY: 2/2 verified.
- S0: NO AMBIGUITY abstention (unchanged).
