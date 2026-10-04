# Preregistration: H-EXP4 (Honest Reachability Labels, Tautology Removal)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any implementation
of exp_invent4.zag. No Python at any stage.

## Mission

Repair the two H-EXP3 red-team downgrades (adv/EXP3_ADV_RESULT.md,
verdict DOWNGRADED, not killed):

1. X-E3-1(b): the positive reachability label "AGENT-SETUP-ABLE"
   overclaims. The learner computes per-variable change counts only;
   it does not know which action changes which variable, whether the
   specific required values are achievable, or whether the state as a
   combination is reachable. The label is reliable as a hazard flag
   but unverified as a clearance.

2. X-E3-2: the ranking "safety verification" loop is tautological.
   It re-runs the identical deterministic pred_under on identical
   inputs, so the VIOLATION branch is dead code. It verifies
   determinism/memory-integrity, not discrimination.

## Hypothesis H-EXP4

Both downgrades are repaired by honest weakening, without changing
the selection mechanism:

1. Replace "AGENT-SETUP-ABLE" with a label that states exactly what
   was computed: no uncontrollable variable detected, setup NOT
   verified. Add a one-time legend line documenting both labels.
   The negative direction (NEEDS-EXTERNAL-SETUP) is untouched; the
   red team confirmed it is sound.

2. Remove the tautological re-verification loop and its dead
   VIOLATION branch. Emit an honest line stating the discriminating
   filter is applied once at selection time and no independent
   re-verification is performed.

## Design (frozen)

exp_invent4.zag is built by copying exp_invent3.zag VERBATIM and
making exactly two changes:

### Change 1: honest positive reachability label (addresses X-E3-1(b))

In emit_reachability, the positive branch currently emits
"AGENT-SETUP-ABLE". It will emit instead:

  NO-UNCONTROLLABLE-VARS (setup NOT verified)

The negative branch (FLAG: NEEDS-EXTERNAL-SETUP with variable,
required value, change count) is UNCHANGED.

A legend line is emitted once after the CONTROLLABILITY report:

  REACHABILITY LEGEND: NEEDS-EXTERNAL-SETUP is a conservative hazard
  flag; NO-UNCONTROLLABLE-VARS means no hazard detected but setup is
  NOT verified (which action sets which value, and state-level
  reachability, are not computed).

No other output changes. Selection, ordering, withholding are
untouched (reachability remains awareness/flagging, not planning,
per the H-EXP3 scope which the red team confirmed as a boundary,
not a kill).

### Change 2: remove tautological safety loop (addresses X-E3-2)

The re-verification loop (the second pred_under pass over emitted
states, the RANKING SAFETY VIOLATION branch, and the
"RANKING SAFETY: N/N ... verified discriminating" line) is DELETED.
In its place, one honest line is emitted:

  SELECTION FILTER: all N emitted states passed the discriminating
  filter at selection (unobserved; all candidates resolve;
  predictions disagree). No independent re-verification performed.

where N is nrec. Rationale, stated in a code comment: the H-EXP3
red team proved the loop tautological (identical deterministic
function on identical inputs; VIOLATION branch dead code). Keeping
it would mislead. The real guarantee is the selection filter
itself, applied once.

## Frozen fixtures

S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt,
S0 = causal/exp_null.txt (same as H-EXP2/H-EXP3), plus
A1 = adv/x_e3_a1.txt (the red-team attack fixture: 11 S1 episodes
plus two lamp-toggle episodes under action 3, making lamp
controllable with 2 changes). A1 exercises the positive label path
that S1/S2 cannot.

## Kill bars (frozen)

- K-E4-1 (honest positive label): On A1, the top pick
  (0,0,1)|2 carries the new positive label
  "NO-UNCONTROLLABLE-VARS (setup NOT verified)". The string
  "AGENT-SETUP-ABLE" appears NOWHERE in the A1 raw output
  (checked by byte search). The legend line appears once in the
  output.

- K-E4-2 (tautology removed): Source inspection of exp_invent4.zag
  confirms the second pred_under re-verification loop is gone:
  no "RANKING SAFETY VIOLATION" string and no "RANKING SAFETY:"
  line in the source. The raw output contains the
  "SELECTION FILTER:" line with N matching the emitted ranked
  count, and contains no "RANKING SAFETY" string.

- K-E4-3 (no regression):
  (a) S1: CONTROLLABILITY report byte-identical to exp_invent3
  (temp/pressure controllable, lamp UNCONTROLLABLE 0 changes);
  ranked states and order identical; heuristic disclaimers
  present on header and top pick; top pick (0,0,1)|2 flagged
  NEEDS-EXTERNAL-SETUP naming lamp==1.
  (b) S2: top pick (0,0,0)|2 flagged NEEDS-EXTERNAL-SETUP;
  ranked states and order identical to exp_invent3.
  (c) S0: NO AMBIGUITY abstention, unchanged.
  (d) A1: ranked states and order identical to the red-team
  recorded output (md5 96cbbd331a5c1af5d32085b6e1f91273 for the
  ranked section is NOT expected to match byte-for-byte because
  the labels changed; instead the state lines [N] state (...)
  and their order must match, verified by diff ignoring the
  REACHABILITY/RANKING lines).

- K-E4-4 (determinism): 3 consecutive runs per fixture
  (S1, S2, S0, A1) are byte-identical (md5).

## Explicit supersession (frozen)

H-EXP3 K-E3-2 required the "RANKING SAFETY: N/N" line with all
states verified discriminating. That bar is SUPERSEDED, not
evaded: the red team proved the loop that produced the line
tautological, so the line certified nothing beyond determinism.
Keeping it to pass a frozen bar would be dishonest. The honest
core of K-E3-2 (explicit heuristic disclaimers,
"informativeness NOT validated") is preserved and re-verified
under K-E4-3(a). This supersession is declared here, before
implementation, with rationale.

## Scope and honest limits (frozen)

- No setup planning. No per-(action,variable,value) achievability
  computation. Those remain future work (the red team listed the
  achievability computation as an alternative honest direction;
  this prereg takes the label-weakening direction, which is
  sufficient to close the overclaim).
- Controllability remains per-variable change counts from observed
  episodes (conservative, may over-flag). Unchanged from H-EXP3.
- The ranking heuristic is unchanged (ndiff DESC, index ASC).
- Not L3. Bounded L2 infrastructure repair addressing red-team
  downgrades.

## Predictions (not bars)

- S1: identical to exp_invent3 except the RANKING SAFETY block is
  replaced by the SELECTION FILTER line; all 3 picks still flagged
  NEEDS-EXTERNAL-SETUP.
- S2: same pattern; 2 picks flagged NEEDS-EXTERNAL-SETUP.
- S0: NO AMBIGUITY; output gains only the legend line.
- A1: top pick (0,0,1)|2 now labeled
  NO-UNCONTROLLABLE-VARS (setup NOT verified); legend present;
  no AGENT-SETUP-ABLE anywhere.
