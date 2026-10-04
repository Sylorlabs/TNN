# F3 Design: Causal Learner Beyond Enumerate-Then-Select

Date: 2026-09-30. Worker: F3 Designer.
Status: DESIGN ONLY. No implementation. No Python. No em dashes.

## 1. What F2 is and where it breaks

F2 (frozen `1eb66765d`, md5 `de95a49350f42122da5fb0a8dd445eba`) is
enumerate-then-select over a fixed vocabulary:

- Hypothesis per effect variable: exactly one rule `(src -> dst, delay)`,
  single positive literal, delay d in 1..DMAX with DMAX=4
  (`L_DMAX()` at line 41 of `learner_frozen.zag`).
- Candidates come only from passive correlations. Cartesian product of
  candidates forms hypotheses. Disagreement-driven experiments
  (`L_find`) eliminate hypotheses. Planning under the survivor.
- Action codes have hardcoded effects shared by researcher convention
  between learner and world.

Empirically mapped boundaries (all 3/3 byte-identical, pure Zag):

| Probe | Commit | Finding |
|---|---|---|
| ABL1/ABL2/ABL3 | `1f3a9511c` | Experiment loop load-bearing (World B); disagreement targeting essential (random kills 0); context machinery load-bearing |
| ADV1 conjunctive truth | `1f3a9511c` | FOOLED=1. Confident planning on wrong model, GOAL_REAL=0 |
| ADV2 silent cause | `1f3a9511c` | MISSED=1. No cause proposal beyond passive data |
| W1 hysteresis | OOD-TESTED | Confident false model (shortest delay), goal by luck |
| W2 inhibition | OOD-TESTED | ne=0, declares impossible what oracle achieves |
| W3 delay 5 | OOD-TESTED | Blind beyond DMAX; cannot separate "no cause" from "too deep" |
| W4 disjunction | OOD-TESTED | Kills a TRUE sufficient cause; exclusive-alternative framing |

F3 keeps what works (disagreement-driven elimination, context machinery,
deterministic byte-identical execution) and replaces the five structural
commitments below. F3 is a stronger bounded L2 design, not an L3 claim.
The literal alphabet, the operator set, and the doubt threshold remain
researcher-authored; that is disclosed in section 8.

## 2. Representation change: DNF rule sets

F2 hypothesis for effect variable V: one rule, one positive literal.

F3 hypothesis for V: a SET of rules `H_V = {R1, ..., Rk}` (k may be 0,
meaning "no model yet", which is a legal state, not a failure).
Each rule is a CONJUNCTION of literals.
Each literal is `(src, polarity, delay)` with polarity in {+, -}
and delay d >= 1.

Prediction semantics (frozen): V(t)=1 iff there EXISTS a rule R in H_V
such that EVERY literal of R holds at t. Literal `(s,+,d)` holds iff
s(t-d)=1; `(s,-,d)` holds iff s(t-d)=0.

F2 is the special case: k=1, one literal, polarity +, d <= 4.
This one change uniformly subsumes gaps 3 (disjunction = several
singleton rules) and 5 (inhibition = negative literals; conjunction =
multi-literal rules).

Refutation semantics (frozen, replaces F2's hypothesis killing):

- A RULE R is refuted by an observation at time t iff all literals of
  R hold at t and V(t)=0 (false positive). Refuted rules are removed
  from H_V, and may trigger GROW (section 4).
- H_V is INCOMPLETE at t iff V(t)=1 and no rule fires. Incompleteness
  triggers PROPOSE (section 4).
- A hypothesis (rule set) is eliminated only when a refutation leaves
  it with no rule covering a positive observation AND no proposal
  operator can cover it. Elimination is per-rule, never per-hypothesis
  while any rule survives. This directly fixes W4: the experiment that
  killed (Z->Y,d2) in F2 now removes only the overclaiming reading of
  that rule, and because (X->Y,d1) still covers the positives, the
  set survives with both true causes retained.

## 3. Persistent learner state (C0-A direction)

All of the following live in learner-created persistent state and are
read by every downstream component. Nothing below is a hardcoded
researcher constant at decision time:

1. `rules[V]`: the DNF rule set per effect variable (section 2).
2. `effects[a]`: the learned action-effect table. For each action code
   a: one of {SETS(v), ADVANCES_TIME, OBSERVES(v), NULL}. Built only
   by the LEARN-EFFECT probing operator (section 6). Planning,
   simulation, and experiment construction read this table; no
   component may branch on a literal action code.
3. `verify_buf`: ring buffer of the last N reserved observations used
   only to check the converged model, never to fit it. N=16 (frozen
   design parameter, disclosed).
4. `history`: superseded rule sets with their refuting observation
   ids (provenance). Enables re-adoption under nonstationarity.
5. `doubt[V]`: 1 - (verify hits / verify total) over the buffer.
   Planning is gated on doubt (section 7).
6. `varied[v]`: whether manipulable variable v has ever been varied
   in the observation history (drives PROPOSE-VARIATION).
7. `Dcur`: the current adaptive delay horizon (section 5).

## 4. Growth operators (de-novo proposal; attacks ADV2, ADV1, W4)

F2's boundary is passive-only enumeration. F3 adds four operators.
All operators are deterministic functions of (rules, history,
observation log); all are logged to the construction trace.

- OP-PROP (passive proposal): from passive data, enumerate singleton
  literals over the adaptive horizon (section 5), both polarities.
  Fit criterion: literal true on at least one positive observation
  (ok > 0) and never refuted (no observation where the literal holds
  and V=0 for polarity +; dual for polarity -). This is F2's
  candidate generation, generalized.
- OP-VAR (variation proposal; attacks ADV2): if H_V is empty or
  incomplete and some manipulable variable v has `varied[v]=0`,
  emit a minimal variation experiment: drive v to 1 via the learned
  effect table, wait, observe V. If a correlation appears, promote
  the corresponding literals via OP-PROP and set `varied[v]=1`.
  F2 could never do this: its experiments only discriminate
  enumerated hypotheses. OP-VAR proposes NEW causes.
- OP-GROW (attacks ADV1): when rule R is refuted at observation t
  (all literals held, V(t)=0), search for a literal L that is FALSE
  at t (excludes the refutation) and TRUE on every observation where
  R fired correctly (keeps all true positives). If found, R := R + L.
  If no such literal exists, drop R and run OP-PROP on the positives
  R used to cover. This is residual-driven repair: the refuting
  observation names the residual, the added literal fixes exactly it.
- OP-SPLIT (attacks W1-style conflation): when one rule's true
  positives split into two groups separable by a literal (group A has
  L true, group B has L false, and no single literal separates a
  refutation), replace R with (R + L) and (R + not L). Logged as a
  split event with the separating literal.

Bounds (disclosed researcher parameters): at most 4 rules per
variable, at most 3 literals per rule. Growth is data-driven inside
the caps; hitting a cap with remaining incompleteness is reported as
CAP_REACHED, an honest signal F2 lacks.

## 5. Adaptive delay horizon (attacks W3)

`L_DMAX()=4` is replaced by `Dcur`, initially 4. Two rules, both
data-relative (no researcher constant):

- EXTEND: when OP-PROP finds no literal at any d <= Dcur and H_V is
  empty or incomplete, set Dcur := 2*Dcur and re-scan.
- STOP: after an extension, compare the best new literal's fit count
  against the worst kept literal's fit count. If best-new <
  worst-kept, revert Dcur and record HORIZON_SUFFICIENT. The stopping
  test is relative to the learner's own data, not a frozen cap.

Effect on W3 (truth Y(t)=X(t-5)): first scan at Dcur=4 finds nothing,
EXTEND to 8, literal (X,+,5) proposed with fit count above the
bar, HORIZON_SUFFICIENT recorded at the next doubling. The learner
can now distinguish "no cause" (extensions keep failing AND all
variables varied) from "cause beyond old depth" (extension succeeds).

## 6. Learned action effects (attacks gap 1; C0-A)

F2's action semantics live in a shared researcher convention. F3:

- OP-PROBE runs once at start (and on demand if an action's observed
  effect contradicts the table): for each action code a in the
  world's declared code range, execute a in a controlled context
  (all manipulable variables held at fixed values), record
  (pre-state, post-state) deltas over the full variable vector.
- Classification (frozen decision procedure): if exactly one variable
  v changes deterministically across 3 probes, `effects[a]=SETS(v)`;
  else if only timestamps advance, `ADVANCES_TIME`; else if a return
  value equals v's pre-state across probes, `OBSERVES(v)`; else NULL.
- All planning, simulation (`L_sim` successor), and experiment
  construction read `effects[a]`. A source audit must show no
  `a==0`/`a==1` style branches in learner decision code; the only
  legal reader is the table.

Test implication: a world may permute the codes (e.g., code 0 waits,
code 1 sets X). F3 must report the learned table matching the
permutation and still reach the goal; the frozen F2 learner fails
this world by construction.

## 7. Provisional convergence and calibrated doubt (attacks W1)

F2 stops at nalive==1 and plans with full confidence. F3:

- Convergence is PROVISIONAL. After the rule sets stabilize (no
  operator fires for a full pass), the learner keeps a verification
  stream: every 4th observation is routed to `verify_buf`, never to
  fitting.
- If a verification observation refutes or incompletes the converged
  model, REVISE fires: the refuting observation re-enters fitting,
  OP-PROP/OP-GROW/OP-SPLIT run, Dcur may EXTEND, and the superseded
  model goes to `history` with provenance. At least one REVISE event
  is expected on W1 (the hysteresis world), where the shortest-delay
  rule will eventually face a verification observation it mispredicts.
- `doubt[V]` gates planning (frozen threshold 0.2, disclosed):
  doubt >= 0.2 means plan INFORMATION-GATHERING actions (OP-VAR or
  disagreement experiments); doubt < 0.2 means plan for the goal.
  "No model" (empty H_V with all variables varied and horizon
  sufficient) is a legal terminal verdict with doubt reported,
  replacing F2's silent "PLAN none found".
- Nonstationarity: if a verification stream starts matching a model
  in `history` better than the current one, re-adopt it (doubt
  reset, event logged). F2 has no such path.

## 8. Honest scope: what F3 is not

F3 as designed is a stronger bounded L2 system, not an L3 claim:

- The literal alphabet (polarity, delay, conjunction), the six
  operators, the caps (4 rules, 3 literals), N=16, and the 0.2 doubt
  threshold are researcher-authored. C0-A is advanced (action
  semantics and rule content now live in learner state) but not met:
  the operator semantics themselves are still source code.
- C0-B is advanced (rule sets grow incrementally via logged
  operators) but the growth vocabulary is fixed.
- C0-C is untested by this design; the battery below uses
  researcher-designed worlds, and an independent post-freeze
  adversary family is required before any L3-adjacent claim.
- C0-D (reuse) is out of scope for F3; rule-library transfer across
  worlds is future work.
- The named next frontier is F4: latent-variable invention, i.e.,
  proposing an unobserved variable to explain structured residuals.
  F3's honest failure mode there ("CAP_REACHED with structured
  residual") is specified as F4's input signal.

## 9. Test battery (frozen design; each world 3/3 byte-identical)

Regression (must still solve; cost bounded):

- R-A: F2 World A (confounded chain). Bar: GOAL achieved, experiment
  count <= F2 count + 2.
- R-B: F2 World B (contextual delay). Bar: GOAL achieved, experiment
  count <= F2 count + 2. (The context machinery is retained verbatim;
  rules gain an optional context guard literal.)

Gap worlds (each targets one gap; frozen F2 behavior noted as control):

- T-EFF (gap 1): permuted action codes. Bar: learned `effects`
  table matches the permutation exactly; GOAL achieved. Control:
  frozen F2 fails (hardcoded codes).
- T-DELAY (gap 2): W3 truth Y(t)=X(t-5). Bar: GOAL achieved;
  trace shows at least one EXTEND event and HORIZON_SUFFICIENT.
  Control: frozen F2 ne=0 (already observed).
- T-DISJ (gap 3): W4 truth Y=X(t-1)|Z(t-2). Bar: at convergence
  both true rules present; no experiment log shows a true rule
  removed without replacement. Control: frozen F2 kills (Z->Y,d2).
- T-REV (gap 4): W1 hysteresis truth. Bar: at least one REVISE
  event fires on the verification stream; terminal state is NOT
  confident-false (either the 3-delay OR is learned or doubt >= 0.2
  with "model incomplete" verdict). Control: frozen F2 converges
  confident-false.
- T-NEG (gap 5): W2 truth Y=X(t-1)&!Z(t-1). Bar: conjunctive rule
  {(X,+,1),(Z,-,1)} learned; GOAL achieved. Control: frozen F2 ne=0.
- T-SILENT (ADV2 redux): silent cause Z. Bar: OP-VAR fires (log shows
  a variation experiment on Z); Z literal proposed; GOAL achieved.
  Control: frozen F2 MISSED=1.
- T-CONJ (ADV1 redux): Y=X(t-2)&Z(t-1). Bar: OP-GROW produces the
  two-literal rule; GOAL achieved. Control: frozen F2 FOOLED=1.

Global bars per world: pure Zag, zero Python, zero em dash bytes,
3/3 byte-identical runs, exit 0, zero stderr bytes.

Falsifiers for the design (what would kill F3's claims at build):

- F-EFF: learned table mismatches the permutation on any code.
- F-DELAY: EXTEND never fires on T-DELAY, or fires but the d=5
  literal is not proposed.
- F-DISJ: any true rule removed without replacement on T-DISJ.
- F-REV: zero REVISE events on T-REV, or terminal confident-false.
- F-NEG/F-CONJ: goal failed on T-NEG/T-CONJ.
- F-SILENT: zero variation experiments on T-SILENT.
- F-COST: R-A or R-B exceeds F2 experiment count + 2.

## 10. Kill-bar self-check

- K1 (5 gaps with concrete mechanisms): gap 1 section 6 (OP-PROBE +
  effect table); gap 2 section 5 (EXTEND/STOP, data-relative); gap 3
  section 2 (per-rule refutation, DNF sets); gap 4 section 7
  (provisional convergence, REVISE, doubt gating, history); gap 5
  sections 2 and 4 (polarity literals, OP-GROW conjunctions).
- K2 (architecture specified, not a wish list): representation
  (section 2), persistent state layout (section 3), six operators
  with trigger conditions (sections 4-6), planning rule (section 7),
  bounds disclosed (section 8).
- K3 (test battery designed): 2 regression + 7 gap worlds with
  frozen bars, controls, and falsifiers (section 9).

## 11. Recommended build order

1. Representation + persistent state (sections 2-3) with R-A/R-B.
2. OP-PROP + per-rule refutation; T-DISJ.
3. OP-GROW + OP-SPLIT; T-CONJ, T-NEG.
4. OP-VAR + varied tracking; T-SILENT.
5. EXTEND/STOP; T-DELAY.
6. OP-PROBE + table-only action reads; T-EFF.
7. Verification stream + REVISE + doubt gating + history; T-REV.
8. Independent red team and governance audit before any SURVIVES
   discussion (promotion steps 10-11 still apply).
