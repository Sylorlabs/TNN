# PREREG: H-GOALINF-1 Goal-Type Inference

Frozen: 2026-10-02 ~08:10 PDT. Worker: H-GOALINF-1 (Goal-Type Inference
Worker). Branch: tnn-native-lab, local only.

## Question

H-COMPVER-2 (prereg 6081afa94, results 0cfd4b0ba) resolved the ev_query
hookup by making RETRIEVE (ev_query) and CONSTRUCT (ev_cquery) distinct
query-goal operations, and recorded as open future work whether
CONSTRUCT-vs-RETRIEVE should be caller-specified or LEARNER-INFERRED.
H-GOALINF-1 tests the inference hypothesis: given a query (s,r), the
learner decides RETRIEVE vs CONSTRUCT from its own state, with no
researcher goal flag anywhere in the query path.

## Mechanism (unfrozen variant only)

- Base: gi_base.zag = byte-identical concatenation (cmp-verified) of
  H-COMPVER-2's lv2_base.zag + lv2_patch.zag. Copied, never edited.
  ev_query, compose_lv, ev_cquery untouched.
- Patch: gi_patch.zag (new code only):
  - gi_factscan(W,s,r): best live non-superseded FACT for (s,r) by
    (pred_score, bid), mirroring lv_predict's FACT scan. Returns node
    id; score and value via out params.
  - gi_probe(W,s,r): target-free greedy structural walk from s using
    un_candidates/un_satisfy (max 8 segments, no MAP reuse, same
    admission as lv_dfs). Returns the walked end value sp, segment
    count nseg, and MAP-execution count. Read-only: no promotion, no
    state writes, no FACT consultation.
  - gi_supersede(W,n): retires a FACT with the native type-3 self-edge,
    the same primitive lv_observe uses on contradiction.
  - gi_compose(W,s,r,pred,rel,masked,st): compose_lv's body with a
    caller-supplied (pred, rel) in place of lv_setup. The reliability
    gate (rel >= 3) is unchanged.
  - ev_iquery(W,s,r,masked,st): the inference entry. Route code in
    st[12]: 0=RETRIEVE, 1=CONSTRUCT, 2=CONSTRUCT-CONFLICT, 3=WITHHOLD.
    1. p = lv_setup(W,s,r). If p == -999999, route 3, return -3.
    2. F1 = gi_factscan(W,s,r). If F1.score < 3, route 1 and call
       ev_cquery (which withholds internally when unreliable).
    3. Else run gi_probe. If no chain walked, route 0 and call
       ev_query (RETRIEVE). The expected argument is -999999
       (researcher-absent sentinel); it is inert on the activate path,
       which returns before any other stage runs.
    4. If a chain walked and sp == F1.value, route 1 and call
       ev_cquery (compose_lv re-derives and verifies the answer).
    5. If a chain walked and sp != F1.value, CONFLICT: gi_supersede
       the contradicted FACT (learner-state revision, recorded), route
       2, and call gi_compose with (sp, nseg). Rationale, preregistered:
       a confident FACT contradicted by confident structure is retired
       in favor of the verifiable channel, because a constructed answer
       is independently re-verified by execution (lv_verify_chain)
       while a FACT is opaque recall. The structural reliability nseg
       (walked segments) is researcher scaffold, honestly labeled.
- Driver: gi_driver.zag. World builders (t1_train, t1_couse, t1_zfacts,
  t1_world, cmp_gap) and instrumentation copied verbatim from
  H-COMPVER-2's lv2_driver.zag. Confirm-cycle helper: N rounds of
  lv_predict + lv_pred_resolve (no lv_observe, so no new FACT is
  written; the taught FACT earns its own score).
- The inference reads only learner state: FACT pred_scores, MAP walk
  outcomes, lv_setup outputs. No goal flag, no researcher target, no
  new modes, bridges, or handlers.

Researcher scaffold (honest): PRED layout reuse, threshold value 3
reuse, srel = walked-segment count, the -999999 sentinel, world
builders, confirm-cycle counts, the conflict tiebreak rationale above.
Learner-owned: all scores, all walk outcomes, every routing decision,
the demotion event.

## Battery (5 tests, fresh workspace each)

1. T-RTRV (task arm a): T1 world; ev_teach_in(201,80,42) then 5 confirm
   cycles (o=42), so FACT(201,80) = (42, score 5); no MAPs touch
   relation 80. ev_iquery(201,80,0,st). Expect route=0 RETRIEVE,
   ans=42, cost=1, live MAPs unchanged, probe execs=0.
2. T-COMP (task arm b): T1 world; 5 lv_observe cycles (101,70) o=107,
   so FACT = (107, score 4); X/Y/W MAPs walk 101->103->105->107.
   ev_iquery(101,70,0,st). Expect route=1 CONSTRUCT, ans=107,
   tried>=1, live MAPs +1, LINK14 out of newest MAP = 3
   (ev_cquery/compose_lv genuinely ran, not recall).
3. T-STALE (task arm c, adversarial): T1 world; ev_teach_in(101,70,999)
   then 7 confirm cycles (o=999), so FACT = (999, score 6); X/Y/W MAPs
   walk 101->103->105->107, contradicting the FACT.
   ev_iquery(101,70,0,st). Expect route=2 CONSTRUCT-CONFLICT,
   ans=107, tried>=1, live MAPs +1, and the stale FACT superseded
   (is_superseded=1). ans=999 (stale recall) = FAIL; ans=-3 with no
   demotion = FAIL.
4. T-UNC (uncertainty arm): T1 world; 2 lv_observe cycles (101,70)
   o=107, so FACT = (107, score 1). ev_iquery(101,70,0,st). Expect
   route=1 CONSTRUCT, ans=-3 (compose_lv withholds: rel 1 < 3),
   tried=0, live MAPs unchanged. Uncertainty withholds; no gamble.
5. T-NE (no-basis arm): T1 world; no evidence at all.
   ev_iquery(101,70,0,st). Expect route=3 WITHHOLD, ans=-3.

## Cost model (preregistered)

- cost(RETRIEVE) = 1 (single activate recall).
- cost(CONSTRUCT) = probe MAP-execs + compose tried + compose rejected.
- cost(WITHHOLD) = 0.
- Report per-test cost and totals. Waste = T-COMP's CONSTRUCT cost
  despite FACT agreement (quantified, discussed, not hidden).
  Missed CONSTRUCT = a query needing construction routed elsewhere
  (expect 0; any miss = K6 FAIL).

## Kill bars

- K1: T-RTRV route=0, ans=42, cost=1, MAPs unchanged, probe execs=0.
- K2: T-COMP route=1, ans=107, tried>=1, +1 MAP, LINK14=3.
- K3: T-STALE route=2, ans=107, stale FACT superseded, tried>=1,
  +1 MAP.
- K4: T-UNC route=1, ans=-3, tried=0, MAPs unchanged.
- K5: T-NE route=3, ans=-3.
- K6: routing accuracy 5/5; 0 missed CONSTRUCTs; waste quantified.
- K7: 3/3 byte-identical runs, SHA-256 recorded.
- K8: 0 modes, 0 bridges, 0 handlers, 0 semantic cases; the token
  `expected` occurs 0 times in gi_patch.zag outside comments;
  ev_iquery takes no goal flag and no researcher target; gi_base.zag
  cmp-verified against lv2_base.zag + lv2_patch.zag.
- K9: cognition lines recorded (gi_patch.zag, gi_driver.zag).

## Verdict on completion

GOAL-INFERENCE-COMPLETE (with routing table) iff K1 through K9 pass.

## Constraints

Unfrozen variant only. Frozen sources read-only (copies). Pure Zag via
the pinned znc binary. Safebin toolchain guard active. Zero em/en dashes
in all documentation. Research paper untouched. Nothing pushed to GitHub.
Git add and git commit use EXPLICIT pathspecs only.
