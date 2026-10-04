# PREREG: CAUSAL-WORLD (C500)

Lane: `causal_world/`. Branch `lane/causal`. Claim block **C500+**.
Frozen BEFORE any implementation exists. Pure Zag. Pinned compiler.

## 0. Frozen separation finding (verified by reading frozen source, pre-implementation)

Read of `compression_exec/tnn2_frozen_ref.zag` (1591 lines) at
`compression_exec/tnn2_frozen_ref.zag`:

- `ev_observe(W,s,r,o)` (line 836) is the ONLY world ingress. It creates a
  fact node via `ev_teach_in`.
- `ev_act(W)` (line 859) takes **no arguments**. It performs no operation on
  the world. It does `ctx_push(W,-3)`, reads `POLICY_ROOT`, walks edges,
  scores candidates by `bid`, and returns an integer. It is a *retrieval over
  policy nodes*, not an intervention.
- `t2_trial(W,s,r,expected,masked,dc,di)` (line 586) is named "trial" but
  assembles candidate *derivation graphs* over already-stored facts and
  verifies them against a post-hoc `expected` scalar passed in by the caller
  (`t2_try_verify`, line 497). No world is stepped. No trial is run.
- Grep for `do`, `interven`, `counterfact`, `cf_` over the file: **zero
  hits.** There is no do-operator, no incoming-edge cut, no mutilated graph,
  no counterfactual evaluator anywhere in TNN-2.

**Conclusion frozen now:** the observation/intervention entry-point split in
TNN-2 is COSMETIC. Two differently named doors open onto the same fact store.
The distinguishing content of an intervention (sever the incoming causes of
the target, hold it fixed, let the rest re-derive) does not exist in TNN-2 and
must be built. This finding is reported independently of the experiment
outcome.

## 1. Scope and honesty frame

This is NOT an L3 claim (charter 9 / brief section 9). The learner does not
invent an open form. What is tested is narrower and stated up front:

- The **representation** of the learned model (a versioned, lag-indexed sparse
  conditional table over learner-selected parent sets, with edge evidence
  split across three acquisition channels) is researcher scaffolding.
- The **content** of the model (which variables are causes of which, which
  direction, which parent sets, which lag, which variables are causally
  IRRELEVANT despite perfect predictive correlation, which law version is
  current) is created by the learner from experience. No variable id, no edge,
  no direction, no lag, no parent set appears as a literal in learner source.
- **If the true dynamics are coded by the researcher, it is not a world-model
  claim.** They are. They live in a separate file, and section 3 makes the
  learner's inability to read them a runtime-checked property, not a promise.

## 2. World (researcher-authored ground truth, learner-invisible)

12 variables, integer values in 0..3. Variable ids and their roles are
recorded here and NOWHERE in learner source.

```
0 TR (treatment input)      6 GF (goal flag)
1 MD (hidden intermediate)  7 A1 (action 1)
2 OU (outcome)              8 A2 (action 2)
3 CN (confounder)           9 A3 (action 3)
4 SN (sensor / lamp)        10 RG (regime observable)
5 PL (policy)               11 LT (latent regime, NOT readable by learner)
```

Ground truth generative law, per tick, in regime `q = LT`:

- `TR = f(CN)` : CN is a confounder of TR and OU.
- `TR -> MD` : a real causal edge, lag 0.
- `MD -> OU` at **lag 1** : a real causal edge with delay.
- `OU = g(MD_prev, TR, CN)` : a **conjunction and interaction**. Specifically
  OU=1 iff `(MD_prev==1 AND CN==3)` OR `(MD_prev==2 AND TR==1)`. The parent set
  of OU is therefore `{MD, TR, CN}` and is not pairwise recoverable.
- `SN` is a noisy deterministic readout of `TR` (a sensor). `SN` predicts OU
  perfectly through `TR`. **`SN` has no causal path to OU.** This is the
  deceptive correlation (charter 192).
- `PL, A1, A2, A3 -> GF` : `GF=1` iff all four equal 1. A three-component
  conjunctive goal (charters 190, 191).
- Regime schedule over ticks: `q=0` for ticks 0..149, `q=1` for 150..299,
  `q=2` for 300..449. In `q=1` the `MD -> OU` mechanism is **inverted**. In
  `q=2` it **reverts** to the `q=0` mechanism. Three distinct laws in one
  lifetime (CHANGING LAWS + law reversion + multiple causal systems).

`do(v, val)`: the world writes `val` into `v`, **skips v's generative rule**,
and holds the clamp across ticks until `release(v)`. This is the do-operator,
implemented in world code, and the learner has no way to see the skip.

Interface available to the agent: exactly three calls.
`w_step()`, `w_set(v,val)` (= do), `w_rel(v)` (= release), `w_get(v)` (= obs).
That is the whole world. `w_get` returns the current value including any clamp.

## 3. PRIVILEGE ISOLATION, RUNTIME CHECKED

`src/w_world.zag` holds all dynamics. `src/agent.zag` holds the learner.
`src/main.zag` holds the driver.

Kill bar **K0**: `main` reads `src/agent.zag` with `_zag_read_file`, counts
byte occurrences of the substrings `w_rule`, `W_RULE`, `W_TRUE`, `qtrue`,
and of the literal variable ids used as world roles. **Any hit is a FAIL and
the program prints `K0 FAIL`.** The build also greps. This is a checked
property, not a discipline claim.

Second isolation check **K0b**: the driver in `main.zag` is forbidden from
naming any world-internal symbol; the driver may only call `w_step`, `w_set`,
`w_rel`, `w_get`, and must obtain every action from the agent.

## 4. AGENT (learner), pure, generic, zero world literals

Agent state `A` (one flat arena):

1. **Tape.** Every episode appends a 64-byte record:
   `[mode, nforced, fv0, fv1, fv2, fv3, prev[12], cur[12], t]`.
   `mode` = 0 passive, else `1 + v` when variable `v` was forced.
   Forced variables have their `cur` value equal to the clamp.
2. **Channel counters**, derived by rescanning the tape. Three channels, and
   the split between them IS the causal evidence:
   - `PAS[v][a][w][b]` : passive episodes, v=a and w=b.
   - `INT[v][a][w][b]` : episodes where v was FORCED to a and w was free,
     observed b.
   - `HOL[v][a][w]` : episodes where v forced to a and w also forced, so w is
     unobserved. Required for correct handling of multi-variable designs.
3. **Lag.** The same conditional table is keyed by lag. Not a second stack:
   `A_int` is one array with a lag dimension; lag 0 and lag 1 share code.
4. **Versions.** Each ordered pair `(v,w)` carries a current law version and a
   small list of versions, each with `hit`, `miss`, `onset`. A version is
   created by the agent when its own probes contradict the retained one. **No
   regime variable exists anywhere in agent state or code.** Prediction picks
   the version whose evidence window covers the query, else the newest.

Agent procedures, all generic:

- `a_scan`   : rebuild channel counters from the tape.
- `a_effect(v,w)` : integer total-variation distance between
  `INT[do(v=a)][w]` and `PAS[v=a][w]`, computed by exact cross-multiplication
  per brief section 2. This is the causal-effect score. It is *zero* for a
  predictive-but-irrelevant variable (SN) and *positive* for a cause.
- `a_order`  : orient edges. `v -> w` is admitted only if
  `a_effect(v,w) > 0` and `a_effect(w,v) == 0`. Both directions admitted only
  if both effects positive, in which case neither is recorded as a bare edge
  and the pair is flagged cyclic.
- `a_parents(target)` : greedy set growth over the *interventional* tape.
  Start empty. Repeatedly add the `(candidate variable, value)` pair whose
  addition most reduces misclassification of the target, scanning the tape.
  Ties broken by lowest variable id then lowest value. Runs at most 4 rounds
  and at most 3 parents. Handles conjunctions and interactions because it
  scores on joint interventional rows, not pairwise marginals.
- `a_mediators(v,w)` : scan all `z` for `v->z`, `z->w`, and mediatedness
  (effect of `v` on `w` present in the tape but absent when `z` is clamped).
  This is how the hidden intermediate MD is found. No schema names MD.
- `a_predict(state, target)` : apply the learned parent set and version table
  to a supplied state vector. Used for unseen-outcome prediction, for
  counterfactuals, and for the agent's own experiment predictions.
- `a_choose_action` : ACTIVE EXPERIMENT CONSTRUCTION. The agent maintains its
  own hypothesis set (its top `H=4` candidate structures by `a_order` score).
  For each candidate it can predict the outcome vector under an action
  sequence. It enumerates all action sequences of length 1, 2 and 3 over its
  primitive set `{SET(v,a)}` restricted to variables that appear in its
  hypothesis set, computes its OWN predicted outcome vector under each
  hypothesis for each sequence, and selects the sequence maximising
  `(number of hypotheses discriminated) / (1 + sequence length)`, subject to a
  budget of at most `maxforce=2` simultaneous clamps. The chosen sequence is
  returned to the driver, which executes it and only then observes.
- `a_counterfactual(state, forked_at, do_var, do_val)` : re-derive the whole
  state vector from the fork using `a_predict`, with the intervened variable
  overwritten. Depends on parent sets and versions by construction.

**No prewritten experiment scripts exist.** The action space is enumerated at
runtime from the two-element primitive set by the agent's own code.

## 5. BASELINES (charter 79)

- **B-STUPID-RECENCY**: always repeat the most recent action sequence.
- **B-STUPID-CORR**: a passive-only correlation learner. Same tape, same
  counters, same budget. It has access to the identical episode count as the
  causal agent (see the confound control in section 6) but only the `PAS`
  channel. Its parent sets are grown on the passive tape. It cannot order
  edges, cannot find mediators, cannot detect law change.
- **B-MEMORISE**: replay the recorded successor state of the nearest matching
  context. Handles nothing unseen.

The causal agent is reported only as a win if it beats all three on the
frozen metrics. If it ties any baseline on any kill bar, that bar FAILS.

## 6. ABLATIONS, WITH WHAT IS HELD CONSTANT

- **A1 NO-INT (passive-only agent).** Held constant: episode count, tape
  length, counter array sizes, all scan iteration counts, all thresholds.
  Varied: only whether `INT`/`HOL` counters are read by `a_order`,
  `a_parents`, `a_mediators`, `a_choose_action`. Episode counts are matched
  exactly: the passive arm is given passive episodes equal in number to the
  causal arm's total episodes, so no arm wins by having seen more.
- **A2 PRIVILEGED (agent may read world rules).** Held constant: identical
  agent code path, identical counters, identical episode budget. Varied: only
  whether `a_order` and `a_parents` are seeded from the true rule table.
  Purpose: establish how much of the result is attributable to the learning
  process rather than to being handed the answer. **If PRIVILEGED is not
  meaningfully better than the honest agent, the learner is doing the work.**
  If PRIVILEGED is much better, that is reported as a shortfall.
- **A3 DESTROY-STRUCTURE (ablation destroys the advantage, charter 79).**
  Held constant: tape, all counters, all versions, all iteration counts.
  Varied: `a_predict` replaces the learned parent set with a single-variable
  (marginal) model, keeping the same number of array reads. Kill bar K7
  requires unseen-outcome accuracy to fall by at least 20 percentage points
  versus the intact agent. This is the ablation that must destroy the
  advantage, proving the advantage lives in the structure.
- **A4 NO-CAUSAL-IN-CF (counterfactual ablation).** Held constant: tape,
  versions, parent sets, counterfactual query set. Varied: only whether
  `a_counterfactual` routes through `a_predict` or returns the associative
  modal successor. Kill bar K8.

## 7. FROZEN PREDICTIONS AND KILL BARS

All bars are frozen now. `3/3` byte-identical stdout is a bar for everything.

- **K0 / K0b privilege isolation.** See section 3.
- **K1 CONFOUNDING.** Agent reports edge `TR->OU`? Predicted: agent's
  oriented set contains `TR -> OU` (true cause) and does **not** report
  `CN -> OU` as absent. Kill: `TR->OU` present AND `CN->OU` present (the
  agent merely inherited the confounder association is not a kill; the kill is
  the agent claiming the confounder is a cause of OU *by association alone*).
  Concretely: for every variable the agent records a direction, it must
  satisfy `effect(fwd) > 0 AND effect(rev) == 0`. Zero violations.
- **K2 DECEPTIVE CORRELATION (192).** The agent must record `SN` as having
  **zero** causal effect on `OU` despite `PAS`-level prediction. Frozen bar:
  agent's `a_effect(SN,OU) == 0` AND agent's `a_effect(OU,SN) == 0` AND the
  passive predictor `P(OU | SN)` differs from `P(OU | not SN)`. If the agent
  claims SN causes OU, FAIL.
- **K3 INTERVENTION vs OBSERVATION.** The essential distinction. Frozen bar:
  there exists a variable pair where the agent's passive marginal table and its
  interventional table **disagree**, and the agent's prediction of the
  interventional outcome is correct while the passive-table prediction is
  wrong. Reported as `SEPARATION REAL/FAKE`. This bar must pass with the
  TNN-2-style cosmetic split as the explicit contrast.
- **K4 UNSEEN OUTCOMES (charter 31).** The agent is given 12 held-out states
  it never observed (drawn after learning completes, from states not in the
  tape) and must predict `OU`. Its learned parent set has 3 parents; a
  single-parent model cannot. Frozen bar: intact agent correct on at least
  9/12, and A3 marginal model correct on at most 8/12, and the two must
  differ by at least 2 cases.
- **K5 REVISION UNDER COUNTEREXAMPLE (charter 31).** After regime change,
  the agent's retained version must be contradicted by its OWN subsequent
  probes, a new version must be created, and the agent's OU accuracy in the
  new regime must recover to at least its pre-change accuracy minus 5 points.
  On regime reversion the agent must **re-use the older version**, not
  mint a fresh one. Frozen bar: `versions_created >= 2` and
  `versions_reused >= 1`.
- **K6 ACTIVE EXPERIMENT CONSTRUCTION (charter 29).** Frozen bars:
  (a) the agent's chosen action sequence is chosen **before** the outcome
  (driver records the sequence index before `w_step`);
  (b) the sequence is **constructed**, not selected from a researcher list:
  the driver contains zero experiment scripts and the agent's enumeration
  covers length-1, 2 and 3 sequences;
  (c) the agent's **own** model correctly predicted the discriminating
  outcome vector under at least the winning hypothesis;
  (d) an `H` where **no passive observation can separate the hypotheses** is
  shown to be separated by the constructed sequence. Frozen bar for (d): the
  constructed sequence separates at least 2 hypotheses that the agent's
  passive tables score identically (same predicted marginal vector).
  (e) multi-step is used at least once, and reachability is respected: the
  agent never forces a variable that appears in no hypothesis, and never
  exceeds `maxforce=2` simultaneous clamps.
- **K7 ABLATION DESTROYS (79).** Per A3, at least 20 points.
- **K8 COUNTERFACTUAL vs ASSOCIATIVE (charter 123).** Frozen bars:
  (a) the agent's counterfactual answer **differs** from the associative
  baseline on at least 3 of 8 forked queries;
  (b) the counterfactual answer changes when the causal model is ablated
  (A4) on at least 3 of 8, i.e. it genuinely depends on the causal model;
  (c) on the queries where they differ, the causal answer matches the world
  (verified by re-running the true world from the fork with the counterfactual
  do applied) on at least 75 percent. **No `COUNTERFACTUAL_MODE` constant
  anywhere.** Grep-enforced, checked at runtime by the same `_zag_read_file`
  trick.
- **K9 DELAYED CREDIT (190) and COMPOSITION (191).** Goal `GF` needs all four
  of PL, A1, A2, A3. Ablate each in turn. Frozen bars: all four ablations
  drop `GF`, and the agent's credit shares satisfy
  `credit(A3) < 0.60` AND all four shares `> 0.15`. The recency baseline
  gives `credit(A3) = 1.00` and must be reported as such. Contribution is
  established by ablation, not by recency.
- **K10 CHANGING LAWS / REVERSION / MULTIPLE SYSTEMS.** See K5. Additionally
  frozen: the agent never reads `LT` or `RG`-as-regime. `RG` is an observable
  *state* variable with its own law, not the regime. Grep-enforced: zero
  occurrences of regime ids `150`, `299`, `300`, `449` in agent source.
- **K11 PLAN vs MEMORISED (charter 68).** Two plans computed before the
  environment change: a memorised sequence copied from the successful trace,
  and a model-based plan from `a_predict`. After the law change the memorised
  plan's success must fall to 0 while the model-based plan, replanned with
  `a_predict`, must succeed. Frozen bar: memorised success `<= 1/5` trials,
  replanned success `>= 4/5`.
- **K12 TRANSFER (charter 31).** The agent's learned edge set and parent sets
  are applied to a **second world** with different variable ids, different
  value ranges and a different regime schedule, with the learner code
  unchanged. Frozen bar: at least 60 percent of edges recovered and at least
  2 of 3 parent sets recovered. Transfer uses the *learned structure as data*,
  which is the honest reading of "transfers".
- **K13 3/3 DETERMINISM.** Byte-identical stdout over 3 runs.
- **K14 NO DYNAMICS IN LEARNER.** K0 plus: the assembled learner region
  contains zero of the world rule expressions. Enforced at runtime and by grep.

## 8. FROZEN FAILED-BAR DIRECTIVE

If any of K0..K14 fails, **report the failure**. Do not move a bar, do not
re-run with a different seed, do not widen a threshold, do not re-prereg. The
one permitted action is to add an `ERRATA.md` that documents a transcription
error in a *frozen number*, with proof, and to leave every criterion intact.

## 9. TERMINAL VERDICT FORMS

`CAUSAL-STRUCTURE-LEARNED` requires K0, K1, K2, K3, K4, K5, K7, K10, K13,
K14, and at least one of K6, K8, K11.
`CAUSAL-PARTIAL` if the above hold but some of K6, K8, K11, K12 fail.
`NOT-CAUSAL` if K3 fails, since that is the load-bearing distinction.

## 10. Explicit non-claims

- Not L3. The representation is researcher scaffolding (stated above).
- The world is researcher-authored. A world-model claim requires that the
  dynamics be absent from the learner, which K0 checks; it does NOT require
  that the dynamics be unknown to the researcher.
- The primitive action set `{SET, RELEASE}` is researcher-authored. What the
  agent creates is the *sequence*, its length, its order, and its content.
- `H=4` hypotheses and a `maxforce=2` budget are researcher-set resource
  constants, not learned.

No em dashes appear in this document.
