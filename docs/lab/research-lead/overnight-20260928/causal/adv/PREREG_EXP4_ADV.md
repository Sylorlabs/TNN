# Preregistration: H-EXP4 Red Team (X-E4-1..X-E4-4)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any attack
execution. No Python at any stage.

## Mission

Independently attack the H-EXP4 repair claim (adv/EXP4_RESULT.md,
verdict SURVIVES 4/4). Assume it is false. H-EXP4 repaired two
H-EXP3 red-team downgrades by honest weakening:
- X-E3-1(b): "AGENT-SETUP-ABLE" replaced with "NO-UNCONTROLLABLE-VARS
  (setup NOT verified)" + legend line.
- X-E3-2: tautological safety loop deleted, replaced with honest
  "SELECTION FILTER:" line. H-EXP3 K-E3-2 explicitly SUPERSEDED.

## Attacks (frozen)

### X-E4-1 (Label honesty): KILL if the new positive label still overclaims

The H-EXP3 X-E3-1(b) attack established three things the learner
does not compute: (1) which action changes which variable, (2)
whether specific required values are achievable, (3) whether the
state as a combination is reachable. The new label says
"NO-UNCONTROLLABLE-VARS (setup NOT verified)" with a legend
documenting (1) and (3).

KILL CRITERION: I construct a concrete fixture where the positive
label is applied AND the pick is not set-up-able in a way that the
label+legend+parenthetical, read together, would lead a reasonable
consumer to miss. Specifically: a fixture where a variable is marked
"controllable" (changed >=1) but the specific required value for the
pick was never observed as an action outcome, AND the label does not
disclaim per-value achievability. If the legend's omissions create a
materially misleading impression beyond what "(setup NOT verified)"
covers, the label still overclaims.

If no such fixture can be constructed, or if the parenthetical
covers the gap, X-E4-1 FAILS (attack fails, mechanism passes).

### X-E4-2 (Filter): KILL if an emitted state bypassed the filter

The SELECTION FILTER line claims "all N emitted states passed the
discriminating filter at selection (unobserved; all candidates
resolve; predictions disagree)."

KILL CRITERION: By source inspection of exp_invent4.zag, I find a
code path where a state is emitted in the RANKED EXPERIMENTS section
or as TOP PICK without having passed all four filter conditions
(unobserved, ok==1, ncv>=2, agree==0) at selection time. This
includes: emission loops that iterate beyond nrec, ord[] indices
that don't correspond to recorded states, or rpr[] reads at
uninitialized indices.

If all emission paths draw exclusively from filter-passing recorded
states, X-E4-2 FAILS.

### X-E4-3 (Regression): KILL if any H-EXP3 behavior silently changed

The prereg claims exp_invent4.zag is exp_invent3.zag "copied VERBATIM"
with "exactly two changes."

KILL CRITERION: `diff exp_invent3.zag exp_invent4.zag` shows any
functional change beyond: (a) the reachability label string +
legend, (b) the safety-loop deletion + SELECTION FILTER line, plus
associated comments. Any change to selection logic, ordering,
controllability computation, prediction, or output formatting
beyond these two is a silent change. Additionally, ranked state
lines ([N] state ...) and CONTROLLABILITY lines must be
byte-identical between exp3 and exp4 outputs on S1/S2.

If the diff shows only the two preregistered changes and outputs
match, X-E4-3 FAILS.

### X-E4-4 (Source audit): KILL if repair is incomplete or hardcoded

KILL CRITERION (any one suffices):
(a) The string "AGENT-SETUP-ABLE" appears in any exp4 raw output
    (byte search across all four fixtures).
(b) The string "RANKING SAFETY" appears in exp_invent4.zag source
    or any exp4 raw output.
(c) The SELECTION FILTER line's N does not match the actual emitted
    ranked count on any fixture.
(d) Any test-fixture literal (state coordinates, variable names as
    logic) in the changed code paths.
(e) The legend line is missing on any fixture that emits
    reachability labels.

If all checks pass, X-E4-4 FAILS.

## Fixtures

S1, S2, S0 from adv/evidence/exp3_*.txt lineage; A1 =
adv/x_e3_a1.txt (the H-EXP3 red-team fixture). I will also attempt
to construct an X-E4-1 adversarial fixture if the analysis warrants.

## Determinism

All attack reproductions run 3x; byte-identical required.

## Verdict rule

H-EXP4 is DOWNGRADED if any attack meets its kill criterion (the
4/4 frozen bars are not retroactively altered). H-EXP4 is KILLED
only if an attack shows the repair does not address the downgrade
it claims to fix (i.e., the overclaim or tautology persists in
substance). Otherwise H-EXP4 SURVIVES the red team.
