# Preregistration: H-EXP2 (Experiment Invention)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any implementation
of exp_invent.zag. No Python at any stage.

## Hypothesis H-EXP2

A learner holding genuinely competing causal hypotheses can INVENT a
discriminating experiment by simulating predicted outcomes under each
hypothesis across the enumerated state space and selecting a state where
the predictions disagree. This is Level D (self-directed evidence): the
learner identifies which missing observation would resolve its own
uncertainty, without being told.

## Background

The causal learner (causal_learn.zag, H-CAUSAL SURVIVES, bounded L2)
represents competing hypotheses as AMBIGUOUS entries with a bitmask of
candidate split variables (en_amb). Its predict() already WITHHOLDs where
candidates disagree. What it cannot do is say WHICH unmade observation
would discriminate. H-EXP2 adds exactly that: counterfactual simulation
over the state space using the learner's own pred_under().

## Theoretical prediction (pre-registered)

If two single-variable split candidates both fully resolve their groups
(genuinely competing), then a discriminating state MUST exist in the
enumerated space. Proof sketch: let candidate s0 induce group effects
G0(t) and candidate s2 induce G2(l). If G0 and G2 agreed on every state,
their group effects would coincide everywhere, and the pooled episodes
would then resolve to a single unconditional effect, contradicting the
ambiguity. Hence some state has G0(t) != G2(l). Corollary: the only honest
nulls are (a) no ambiguity at all, and (b) ambiguity where no unobserved
state is fully predictive. An "ambiguity with agreeing predictions
everywhere" fixture is unconstructible, so the null control is abstention
on unambiguous input.

## Frozen fixtures

- S1 (scenario 1): causal/cum_B.txt (already frozen, commit 8ead2ca68).
  sha256 fedf3a6d767d535b85dc0377bafe79d328e6c5c4713f45a2b0bcc8e5920a441c.
  Phase A (valve intact, lamp always off) + Phase B (valve revealed:
  temp==hot blocks pressurize; lamp on as confounder). Verified with the
  committed causal_learn binary: action 2 AMBIGUOUS candidates={s0,s2}.
- S2 (mirror): causal/exp_obs2.txt (new, frozen here).
  sha256 180010ea3e152f4376cf9be5e3575f7780209d683e15cf7094ad48a125fbe165.
  Phase A (valve intact, temp always hot): (2,0,0)->(2,1,0),
  (2,1,1)->(2,1,1). Phase B (valve revealed: lamp==1 blocks pressurize;
  temp cold correlated): (0,0,1)->(0,0,1), (0,1,1)->(0,1,1). Verified:
  action 2 AMBIGUOUS candidates={s0,s2}. The true blocker is lamp here,
  temp is the confounder. The expected top pick differs from S1.
- S0 (null): causal/exp_null.txt (new, frozen here).
  sha256 ee62e30d082d1342e27385105ae1aef8fbc8f75d4a3fa47.
  Pressurize always works. Verified: action 2 ACTIVE (no ambiguity).

## Algorithm (frozen, generic)

exp_invent.zag is built by copying causal_learn.zag VERBATIM (generic
machinery, no task dynamics) and replacing main() with:

1. Load episodes from argv[1]; create entries for actions 0..3; run
   learn_episode over all episodes (identical to causal_learn main).
2. Scan entries for ST_AMBIG. If none: emit
   "NO AMBIGUITY: no competing hypotheses, nothing to invent." and stop.
   (Honest abstention.)
3. For each ambiguous entry with action a and candidate mask m:
   a. Enumerate states: t in 0..vmax(0), p in 0..vmax(1), l in 0..vmax(2)
      (12 states). State index = t*4+p*2+l.
   b. Skip the state if an exact episode (same 3 state values, EP_ACT)
      already exists in the entry: its outcome is known, it is not new
      evidence.
   c. For each candidate variable v in m: r_v = pred_under(W,i,v,t,p,l).
      If any r_v == 0 (unresolved): skip the state. An experiment whose
      outcome some hypothesis cannot predict is not discriminating.
   d. If all resolved predictions are identical: skip (no disagreement).
   e. Else record: state, per-candidate predicted next-states, and
      ndiff = number of output variables on which predictions differ.
4. Rank records by (ndiff DESC, state index ASC). Emit the full ranked
   list. The rank-0 record is the TOP PICK.
5. For the top pick, emit an inspectable trace: for each candidate,
   the variable, the episodes forming its prediction group
   (ep_s[v]==query value), and the predicted next-state; then the
   variables on which predictions differ.

No state literals from any fixture appear in the invention code. The
picks emerge from enumeration plus the learner's own predictions.

## Predictions (not bars)

- S1 top pick predicted: state (0,0,1) | action 2. Hand derivation:
  under s0, temp==0 group gives p:=1 so (0,1,1); under s2, lamp==1 group
  gives unchanged so (0,0,1). States (1,0,1) also discriminates (rank 1);
  (2,0,0) is unobserved and discriminating (rank 2). All differ on p only,
  so index order decides: 1 < 5 < 8.
- S2 top pick predicted: state (0,0,0) | action 2. Under s0, temp==0
  group gives unchanged so (0,0,0); under s2, lamp==0 group gives p:=1
  so (0,1,0). Second: (2,0,1) (index 9).
- S0: abstention, no pick.

## Kill bars (frozen)

- K-E1 (selects a discriminating experiment): On S1, the invention emits
  at least one ranked experiment; the TOP PICK's state has no exact
  episode in the action-2 entry; and the candidates' resolved predictions
  for it differ on at least one output variable. (Property bar; the
  predicted pick (0,0,1)|2 is confirmatory.)
- K-E2 (inspectable trace): The output contains, for the top pick, one
  line per candidate variable naming it (s0, s2) together with its
  predicted next-state, plus the list of output variables on which the
  predictions differ.
- K-E3 (not hardcoded, not heuristic):
  (a) Source audit: the invention code (new main plus helpers) contains
  no integer-literal triple encoding (0,0,1) or (0,0,0) as a picked
  state. Verified by grep.
  (b) On S0 the program emits the NO AMBIGUITY abstention and no pick.
  (c) On S2 the top pick is (0,0,0)|2: a different answer from the same
  binary, refuting hardcoding of the S1 answer.
- K-E4 (determinism): 3 consecutive runs per fixture are byte-identical
  (md5).

## Scope and honest limits (frozen)

- Setup planning is OUT OF SCOPE: the invention selects (state, action),
  not the action sequence to reach the state. Reachability-aware ranking
  is future work.
- One ambiguous entry per action is assumed; fixtures contain exactly
  one (action 2). Multiple ambiguous entries are each processed, but
  cross-entry ranking is not tested.
- The state space is the learner's own 3-variable enumeration; richer
  experiment spaces (multi-step, parametric) are not tested.
- This tests experiment SELECTION from enumerated candidates, not
  experiment CONSTRUCTION (inventing new actions or new variables).
- Not L3 evidence by itself: the hypothesis vocabulary and the
  enumeration space are authored. What is new is the learner using its
  own uncertainty to direct evidence gathering (Level D).

## Red-team notes for later

- Mirror-scenario variants with ambiguity on other variable pairs.
- Adversarial fixtures where the top pick is unreachable or unsafe.
- Whether ndiff-ranking can be gamed by degenerate predictions.
- Port into the unified learner (route + invent + revise loop).
