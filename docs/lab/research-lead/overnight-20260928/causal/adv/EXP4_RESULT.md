# H-EXP4 Result: Honest Reachability Labels, Tautology Removal

Date: 2026-09-29. Pure Zag, no Python at any stage. Prereg
adv/PREREG_EXP4.md frozen in commit de41396ae BEFORE any
implementation. Commit order verified: prereg strictly precedes this
implementation commit.

## Verdict: H-EXP4 SURVIVES (4/4)

Both H-EXP3 red-team downgrades are repaired by honest weakening.
The selection mechanism is untouched.

## The repairs

### X-E3-1(b): positive label weakened (not re-engineered)

The H-EXP3 label "AGENT-SETUP-ABLE" asserted the agent can set the
pick up. The learner only computed per-variable change counts; it
does not know which action changes which variable, whether the
specific required values are achievable, or whether the state as a
combination is reachable. The new positive label states exactly
what was computed:

  REACHABILITY: NO-UNCONTROLLABLE-VARS (setup NOT verified)

A legend line is emitted once per run documenting both labels:

  REACHABILITY LEGEND: NEEDS-EXTERNAL-SETUP is a conservative hazard
  flag; NO-UNCONTROLLABLE-VARS means no hazard detected but setup is
  NOT verified (which action sets which value, and state-level
  reachability, are not computed).

The negative direction (FLAG: NEEDS-EXTERNAL-SETUP with variable,
required value, change count) is byte-identical to H-EXP3; the red
team confirmed it sound. Per-(action,variable,value) achievability
remains future work (the prereg took the label-weakening direction,
which the red team listed as an acceptable honest repair).

### X-E3-2: tautological loop removed (not relabeled)

The H-EXP3 re-verification loop re-ran the identical deterministic
pred_under on identical inputs; the red team proved the VIOLATION
branch dead code. The loop, the branch, and the "RANKING SAFETY"
line are deleted. In their place:

  SELECTION FILTER: all N emitted states passed the discriminating
  filter at selection (unobserved; all candidates resolve;
  predictions disagree). No independent re-verification performed.

The real guarantee was always the selection filter itself, applied
once. H-EXP3 K-E3-2 (which required the RANKING SAFETY line) is
explicitly SUPERSEDED in the prereg with rationale: keeping a
proven-tautological check to pass a frozen bar would be dishonest.
The honest core of K-E3-2 (explicit heuristic disclaimers,
"informativeness NOT validated") is preserved.

## Kill bar results

- K-E4-1 (honest positive label): PASS. On A1 (lamp controllable,
  2 changes), the top pick (0,0,1)|2 is labeled
  "NO-UNCONTROLLABLE-VARS (setup NOT verified)". Byte search:
  "AGENT-SETUP-ABLE" appears 0 times across all four raw outputs.
  Legend line present once per run.

- K-E4-2 (tautology removed): PASS. Source inspection: no
  "RANKING SAFETY" string in exp_invent4.zag; the second pred_under
  pass is gone. Output: "SELECTION FILTER:" line present with N
  matching the emitted ranked count (3 on S1/A1, 2 on S2);
  "RANKING SAFETY" appears 0 times in all raw outputs.

- K-E4-3 (no regression): PASS.
  (a) S1: CONTROLLABILITY line byte-identical to exp_invent3
  (temp/pressure controllable, lamp UNCONTROLLABLE 0 changes);
  ranked state lines identical (diff clean); heuristic
  disclaimers present on header and top pick; top pick
  (0,0,1)|2 flagged NEEDS-EXTERNAL-SETUP naming lamp==1.
  (b) S2: ranked state lines identical; top pick (0,0,0)|2
  flagged NEEDS-EXTERNAL-SETUP.
  (c) S0: NO AMBIGUITY abstention, unchanged (output gains only
  the legend line).
  (d) A1: ranked state lines identical to the red-team recorded
  output; top pick (0,0,1)|2 with the new honest label.

- K-E4-4 (determinism): PASS. 3/3 byte-identical per fixture:
  S1 70e7838337714149eba11da778254042,
  S2 d0e5f41e8ba100f39cfc632cddda309f,
  S0 1856e624665cce73bcf6929fc998e2f5,
  A1 769165fbbe848c16c3e51d2ab9435653.

## Classification

Bounded L2 discriminating-state selection with honest reachability
flagging (reliable conservative hazard flag; positive direction
explicitly unverified) and honestly-scoped heuristic ranking (no
tautological re-verification claimed). Not L3. Both H-EXP2
downgrades remain addressed in their honest core.

## Honest limits

- No setup planning; no per-(action,variable,value) achievability.
- Controllability remains per-variable change counts (conservative,
  may over-flag on small episode sets).
- Ranking heuristic unchanged (ndiff DESC, index ASC);
  informativeness NOT validated.
- The SELECTION FILTER line documents single application of the
  filter; it is not an independent check.

## Artifacts (this commit)

- adv/exp_invent4.zag (implementation; binary excluded per
  convention)
- adv/EXP4_RESULT.md (this file)
- adv/evidence/exp4_s1_raw.txt (md5 above)
- adv/evidence/exp4_s2_raw.txt
- adv/evidence/exp4_s0_raw.txt
- adv/evidence/exp4_a1_raw.txt

Prereg: adv/PREREG_EXP4.md (commit de41396ae).
