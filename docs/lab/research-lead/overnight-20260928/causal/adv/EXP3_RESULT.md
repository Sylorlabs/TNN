# Experiment Invention v3 Results: H-EXP3 (Reachability-Aware)

Date: 2026-09-29. Pure Zag. Prereg frozen in commit 6a4bb29ba BEFORE
implementation. No Python at any stage.

## Verdict: H-EXP3 SURVIVES (4/4)

H-EXP3 addresses both DOWNGRADED claims from the H-EXP2 adversary
(adv/EXP2_ADV_RESULT.md) without changing the selection mechanism:

1. X-A1 (reachability): The learner now computes per-variable
   controllability from its own episodes and explicitly flags every
   ranked pick that requires uncontrollable variables. No pick is
   silently recommended as runnable.
2. X-A2 (ranking): The ranking is explicitly scoped as an unvalidated
   heuristic in all output, with a verified safety property: every
   emitted state is re-checked to genuinely discriminate.

## Bar-by-bar

**K-E3-1 (unreachable picks flagged): PASS.**
On S1, the output contains:
```
CONTROLLABILITY (from 11 episodes): temp=controllable (4 changes);
pressure=controllable (3 changes); lamp=UNCONTROLLABLE (0 changes)
```
The top pick (0,0,1)|2 carries:
```
REACHABILITY: FLAG: NEEDS-EXTERNAL-SETUP (requires lamp==1
[0 changes in episodes; not action-controllable])
```
All 3 ranked picks are flagged. The flag names the uncontrollable
variable, its required value, and its change count. Nothing is silently
recommended.

On S2 (4 episodes), temp is also flagged UNCONTROLLABLE (0 changes in
the 4-episode fixture). This is honest and conservative: the learner
only knows what it has seen. The prereg explicitly predicted this
behavior for small episode sets.

**K-E3-2 (ranking scoped as heuristic): PASS.**
The ranked list header reads:
```
RANKED EXPERIMENTS (heuristic: ndiff DESC, state-index ASC;
informativeness NOT validated)
```
The top pick line reads "TOP PICK (by heuristic)". The safety
verification emits:
```
RANKING SAFETY: 3/3 emitted states verified discriminating
(all candidates resolve and disagree).
```
on S1, 2/2 on S2. This is a real re-check (pred_under re-run per
emitted state), not a label.

**K-E3-3 (no regression on H-EXP2 bars): PASS.**
(a) K-E1: S1 top pick (by heuristic) is still (0,0,1)|2; predictions
differ on v1; no exact episode in the action-2 entry.
(b) K-E2: trace names s0/s2 with predicted next-states and differing
variables (v1).
(c) K-E3: S0 emits NO AMBIGUITY abstention; S2 picks (0,0,0)|2
(different from S1, refuting hardcoding); source audit confirms no
state literals in new code (states flow through rt/rp/rl record
arrays populated by enumeration).
(d) K-E4: determinism holds (see K-E3-4).

**K-E3-4 (determinism): PASS.** 3 consecutive runs per fixture are
byte-identical:
- S1: 3eef51b231247c9e975c41df0de8fcd9
- S2: 429573a776e0f5dc721cd089118c5b2b
- S0: b51bdf8cc3713935f347928e124cd6da

## Theoretical note (from prereg, confirmed)

In the 2-candidate case, ANY discriminating state yields identical
information (1 bit: which candidate predicted correctly). ndiff counts
differing output variables, but the information gain does not scale
with ndiff. This is WHY the ranking is unvalidatable as
"more informative", and WHY the safety property (all emitted states
discriminate) is the correct validated claim. The ranking orders by a
heuristic; it cannot promote a non-discriminating state (verified).

## What changed vs H-EXP2

Added (in adv/exp_invent3.zag, copied from exp_invent.zag):
- compute_controllable(): per-variable change detection over EP_ACT
  episodes. No domain knowledge.
- emit_controllability(): one-line report after learning.
- emit_reachability(): per-pick flag naming uncontrollable variables,
  required values, and change counts.
- Ranking safety re-verification loop over emitted states.
- Output labels: heuristic disclaimers on ranked header and top pick.

Unchanged: the selection mechanism (enumeration, pred_under simulation,
disagreement filter, ndiff/index ranking), the trace format, the
abstention behavior.

## Scope and honest limits

- Setup PLANNING (action sequences to reach states) remains out of
  scope. H-EXP3 adds reachability AWARENESS (flagging), not planning.
- Controllability is conservative: a variable that never changed in the
  observed episodes is marked uncontrollable even if actions could
  change it in principle. The learner only knows what it has seen.
- The ranking heuristic itself is unchanged. H-EXP3 does not improve
  the ranking; it scopes it honestly and verifies its safety.
- Not L3. Bounded L2 infrastructure addressing red-team downgrades.

## Artifacts

- causal/adv/exp_invent3.zag: implementation (H-EXP2 code + reachability).
- causal/adv/PREREG_EXP3.md: frozen prereg (commit 6a4bb29ba).
- causal/adv/evidence/exp3_s1_raw.txt, exp3_s2_raw.txt, exp3_s0_raw.txt:
  raw outputs (md5s above).
- causal/adv/EXP3_RESULT.md: this file.

## Downgrade status update

- X-A1 DOWNGRADE ADDRESSED: picks are no longer silently recommended.
  Every pick carries an explicit reachability flag derived from the
  learner's own episode data. The honest description is now
  "discriminating-state selection with reachability flags" rather than
  unlabeled "experiment invention".
- X-A2 DOWNGRADE ADDRESSED: the ranking is explicitly labeled as an
  unvalidated heuristic in all output, with the theoretical justification
  for WHY it cannot be validated as informativeness (2-candidate
  information equivalence), and a verified safety property replacing
  the unsupported optimality claim.
