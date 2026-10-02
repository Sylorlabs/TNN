# H-EXP5 Result: Per-(action,variable,value) Achievability

Date: 2026-09-29. Pure Zag, no Python at any stage. Prereg
adv/PREREG_EXP5.md frozen in commit d638f7798 BEFORE any
implementation of exp_invent5.zag. Commit order: prereg strictly
precedes this implementation commit (verify with
git merge-base --is-ancestor).

## Verdict: H-EXP5 SURVIVES (6/6)

The exact gap the H-EXP4 legend admitted, "(which action sets which
value, and state-level reachability, are not computed)", is now
half-closed: per-(action,variable,value) observed-outcome
achievability IS computed and reported. State-as-combination
reachability remains uncomputed and documented.

## What was added

exp_invent5.zag = exp_invent4.zag verbatim plus four additions:

1. compute_achievability: achv[a][v][x] counts EP_ACT episodes
   where action a yielded value x for variable v as outcome.
   36 i32 cells, actions 0..3. Observed outcome only, not causal
   attribution.

2. emit_achv_table: full table once per run after CONTROLLABILITY.

3. emit_achievability: per ranked pick and top pick, for each
   required variable value, the demonstrating action set or
   "NEVER OBSERVED as outcome (undemonstrated)".

4. Legend replaced with the frozen text scoping "demonstrated" as
   observed-outcome (not caused, not guaranteed) and documenting
   the outcome-vs-change distinction.

The selection mechanism, ranking heuristic, reachability FLAG
logic, and CONTROLLABILITY are untouched (K-E5-4 verifies).

## Kill bar results

- K-E5-1 (positive achievability): PASS. A1 top pick (0,0,1):
  "lamp==1 demonstrated by action(s) {2,3} (2 eps)" and
  "temp==0 demonstrated by action(s) {1,2,3} (6 eps)". Matches the
  hand-verified frozen predictions exactly.

- K-E5-2 (outcome-without-change nuance): PASS. S1 top pick
  (0,0,1): "lamp==1 demonstrated by action(s) {2} (1 eps)" (the
  single ep11 outcome, never a change) AND the REACHABILITY line
  remains "FLAG: NEEDS-EXTERNAL-SETUP (requires lamp==1 [0
  changes in episodes; not action-controllable])". The
  conservative flag is preserved while achievability honestly
  reports the observed outcome. This is the sharpest honesty
  property of H-EXP5: demonstrated-as-outcome does not clear the
  change-based hazard flag.

- K-E5-3 (table present, zero row): PASS. S0 ACHV table contains
  "ACHV a0 temp[0:0,1:0,2:0] pressure[0:0,1:0] lamp[0:0,1:0]";
  S0 still emits "NO AMBIGUITY: no competing hypotheses, nothing
  to invent."

- K-E5-4 (no regression): PASS. On S1/S2/A1/S0, all RANKED
  EXPERIMENTS state lines, CONTROLLABILITY, SELECTION FILTER,
  TRACE, and REACHABILITY flag lines are byte-identical to the
  exp_invent4 outputs (verified by diff excluding the added
  ACHV/ACHIEVABILITY lines and the replaced legend).

- K-E5-5 (determinism): PASS. 3/3 byte-identical per fixture:
  A1 4c4e9954fe4fcbd64470e777f934515c,
  S1 ae8d42e417f38228de6aa707350bf5bd,
  S2 cd949065b4ad6ed4f33dbbd47bdacf2e,
  S0 64fc5fde5f36107e2889ccf2703bef42.

- K-E5-6 (legend honesty): PASS. Legend contains "not
  necessarily caused by them" and "state-as-combination
  reachability is not computed". The H-EXP4 parenthetical
  "(which action sets which value, and state-level reachability,
  are not computed)" appears 0 times in source and outputs.
  "AGENT-SETUP-ABLE" and "RANKING SAFETY" appear 0 times.

## Classification

Bounded L2 discriminating-state selection with honest
per-(action,variable,value) achievability reporting. Not L3: no
new representation invented; the (action, variable, value)
vocabulary is given by the episode format. The mechanism now
answers "which action was observed to yield which value" from
its own episodes; it still does not do setup planning and does
not assess state-as-combination reachability.

## Honest limits

- Achievability is observed-outcome, not causal attribution and
  not a capability guarantee.
- Demonstrated-as-outcome is weaker than demonstrated-as-change;
  change-to counts remain future work.
- No setup planning; no state-as-combination reachability.
- Actions outside 0..3 not represented.

## Artifacts (this commit)

- adv/exp_invent5.zag (implementation; binary excluded per
  convention)
- adv/EXP5_RESULT.md (this file)
- adv/evidence/exp5_a1_raw.txt (md5 above)
- adv/evidence/exp5_s1_raw.txt
- adv/evidence/exp5_s2_raw.txt
- adv/evidence/exp5_s0_raw.txt

Prereg: adv/PREREG_EXP5.md (commit d638f7798).
Toolchain: znc 2026.07.0-dev (edition 2026).
