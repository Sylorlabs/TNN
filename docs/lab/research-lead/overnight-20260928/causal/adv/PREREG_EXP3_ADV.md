# Preregistration: H-EXP3 Red Team (X-E3-1..X-E3-4)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any attack
fixture is built or any attack is executed. No Python at any stage.
Assume the H-EXP3 claim is false. Builder: adv/exp_invent3.zag
(prereg 6a4bb29ba, result f8299c388). Attacks run the builder's
committed binary unmodified on adversarial fixtures, plus code audit.

## Target claims (from adv/EXP3_RESULT.md)

- T1: "picks are no longer silently recommended. Every pick carries an
  explicit reachability flag derived from the learner's own episode
  data." K-E3-1: the S1 top pick is flagged NEEDS-EXTERNAL-SETUP
  naming lamp with change count 0.
- T2: "the ranking is explicitly labeled as an unvalidated heuristic
  in all output, with the theoretical justification ... and a verified
  safety property replacing the unsupported optimality claim."
  "RANKING SAFETY: N/N emitted states verified discriminating
  (all candidates resolve and disagree)." "This is a real check, not a
  label: if any emitted state failed, it would be reported."

## Attack X-E3-1: controllability gaming (false "controllable" /
AGENT-SETUP-ABLE overclaim)

Background: compute_controllable marks v controllable iff some EP_ACT
episode has ns[v]!=s[v]. emit_reachability emits NEEDS-EXTERNAL-SETUP
if ANY variable is uncontrollable, else the bald label
"AGENT-SETUP-ABLE" with no values, no qualifications.

Two directions:

(a) False-uncontrollable (task-suggested): a variable controllable in
the true world but never changing in the episodes is marked
UNCONTROLLABLE, producing a spurious NEEDS-EXTERNAL-SETUP flag.
Empirical exhibit: S2 (exp_obs2.txt) itself — temp is flagged
UNCONTROLLABLE (0 changes in 4 episodes) though heat/cool change temp
in the true world. The builder's prereg explicitly predicts and
discloses this as "conservative and honest". Verdict if confirmed:
INFORMATIONAL (documented limitation), not a kill.

(b) False-controllable / positive-label overclaim (the sharp attack):
AGENT-SETUP-ABLE asserts the agent can set the pick up. Evidence used:
each variable changed at least once. NOT used: which action changes
which variable, whether the SPECIFIC required values are achievable,
whether the state combination is reachable. The learner has no
action-to-value mapping for setup and never verifies
value-achievability.

Fixture A1: S1 (cum_B.txt) episodes PLUS lamp-toggle episodes under a
non-interfering action so all three variables change at least once:
  T 0 0 0 | 3 | 0 0 1
  T 0 0 1 | 3 | 0 0 0
Action 3 already exists in the fixture; the added episodes must not
disturb the action-2 ambiguous entry (verify: action-2 top pick still
(0,0,1)|2 and the AMBIGUOUS action 2 entry still present).

Predicted mechanism behavior: CONTROLLABILITY shows temp/pressure/lamp
all controllable; every pick (including TOP PICK) labeled
"REACHABILITY: AGENT-SETUP-ABLE".

Kill criterion: If AGENT-SETUP-ABLE is emitted, the positive label is
demonstrated to rest on per-variable change counts alone, with no
check that the required values are achievable or that the learner
knows which actions produce them. This contradicts the prereg's own
conservative principle ("the learner only knows what it has seen"):
the learner has seen each variable change, but has NOT seen that it
can set up this specific state. Verdict: DOWNGRADE of the
reachability-flag claim — sound in the negative direction
(flagging uncontrollable), overclaiming in the positive direction.
Honest label would be "no uncontrollable variables detected (setup
not verified)".

I will additionally inspect whether the top pick on A1 requires any
variable value never observed in any episode; if so, that is a smoking
gun (label claims setup-ability for an unobserved value). If not, the
structural overclaim above still stands as the downgrade basis.

## Attack X-E3-2: safety-check tautology

Target: "verified safety property" / "a real check, not a label".

Code-analysis claim (to be verified by reading, then demonstrated):
the selection loop records a state only if ok==1 (all candidates
resolve via pred_under) and agree==0 (predictions disagree). The
safety loop re-runs the IDENTICAL deterministic pred_under
(pure function: reads W, writes only out; verified no RNG, no W
mutation) on the IDENTICAL inputs (same W, ii, cv, recorded state)
and re-checks disagreement against the SAME stored rpr values. W is
not modified between the loops (only emits and z_allocs). Therefore
nsafe==nrec on every valid execution; the VIOLATION branch is dead
code. The check verifies determinism/memory-integrity, not
discrimination; it cannot fail by construction.

Empirical component: run builder binary on S1, S2, A1; confirm
RANKING SAFETY is N/N in all runs. (Cannot empirically prove "for all
fixtures", the code analysis carries the universality.)

Kill criterion: if the analysis is confirmed, the "verified safety
property" overstates a tautological re-computation. Verdict:
DOWNGRADE of the X-A2 repair's safety sub-claim. The honest-labeling
half of the X-A2 repair (heuristic disclaimers in output) is real and
stands; the theoretical note (2-candidate information equivalence) is
correct and stands.

## Attack X-E3-3: flag ignoring (boundary)

Question: does the NEEDS-EXTERNAL-SETUP / AGENT-SETUP-ABLE flag have
any behavioral consequence (withhold, reorder, annotate downstream
decisions), or is it purely a label on emitted text?

The builder's prereg explicitly discloses: "reachability AWARENESS
(flagging), not reachability PLANNING" and "The ranked list is still
emitted (selection unchanged)". Method: code inspection of
emit_reachability call sites and any downstream consumer of ctrl[].

Kill criterion: none — if the flag is just a label, that matches the
disclosed design. Verdict: BOUNDARY confirmation (informational). The
flag does not prevent the learner from attempting unreachable picks;
it only annotates. Report so the parent can decide if awareness
without enforcement satisfies the research goal.

## Attack X-E3-4: source audit

Verify by reading (no execution needed):
(a) compute_controllable matches the prereg description (scans EP_ACT
episodes, ns[v]!=s[v] implies controllable; per-variable change
counts).
(b) No hardcoded state literals, variable-specific special-casing, or
fixture-specific branches in the new code (compute_controllable,
emit_varname, emit_controllability, emit_reachability, safety loop,
call sites). emit_varname mapping 0/1/2 to names is labeling, not
logic — acceptable.
(c) The selection mechanism is unchanged vs H-EXP2: diff
exp_invent3.zag against exp_invent.zag; new code must be additive
only (new functions + call sites + label strings).
(d) The safety loop matches its description (re-run pred_under per
emitted state per candidate; disagreement re-check on stored rpr).

Kill criterion: any hardcoding, special-casing, or undisclosed change
to selection → KILL or DOWNGRADE per severity. If clean → PASS.

## Fixtures (frozen)

- S1 = causal/cum_B.txt, S2 = causal/exp_obs2.txt, S0 =
  causal/exp_null.txt (builder's own).
- A1 = adv/x_e3_a1.txt (defined above; S1 + 2 lamp-toggle episodes
  under action 3). Built AFTER this prereg is committed.

## Determinism

3 runs per fixture for any empirical claim; byte-identical required
(md5). Pure Zag only. Only adversary-owned files committed
(adv/PREREG_EXP3_ADV.md, adv/x_e3_a1.txt, adv/EXP3_ADV_RESULT.md,
adv/evidence/*). Never modify the builder's exp_invent3.zag.

## Verdict mapping (frozen)

- Any X-E3-N kill criterion fires → H-EXP3 KILLED (if T1/T2 core
  claim falsified) or DOWNGRADED (if a sub-claim narrowed).
- X-E3-1(a) confirmed → INFORMATIONAL (already disclosed).
- X-E3-3 → BOUNDARY (informational) regardless.
- All attacks fail → H-EXP3 SURVIVES red team; report the survived
  attacks as negative evidence.
