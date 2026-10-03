# PREREG.md: XDOMAIN-CAUSAL -- Cross-Domain Causal to Intervention Composition

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.
This is the UNFROZEN variant: new driver code only; all mechanism cores
are ported verbatim (sha256-verified) and read-only.

## Hypothesis

H-XDC-1: None of the four existing composition mechanisms (A: plen
contract chaining via compose_try; B: co-use type-15 LINK edges with
chain assembly; C: constraint-driven assembly from MAP relation
sequences; XIO-general: typed pairing with per-class stage dispatch)
can compose a causal model with an intervention, because the do-operator
is a structure transformation (sever incoming edges of the intervened
variable, then recompute downstream), while all four mechanisms
implement composition as value chaining (f(g(x)) over single values).
Predicted outcome: all four mechanisms fail exactly the do-not-equal-see
queries (Z1, Z4) while the observational predictor transfers exactly the
do-equal-see queries (Z2, Z3) via rebind; a driver-level oracle
implementing the do-operator from learner state computes all four
answers, proving the world solvable and localizing the gap to
composition.

## World design: confounded causal world with a do-operator gap

Variables: A in {1,2} (confounder), C = A (cause), E = A + 2*C
(effect). Two observed units: 501 (A=1, C=1, E=3), 502 (A=2, C=2,
E=6). The confounding is structural: A drives both C and E, so the
observational mapping C -> E bakes in the backdoor path C <- A -> E.

X = observational causal predictor (chain MAPs, rel 81 facts, query
rel 91). Facts: (501,81,511), (511,81,515), (515,81,3) and
(502,81,512), (512,81,516), (516,81,6). Training queries: X1 =
(501,91) -> 3 (trial, plen 4), X2 = (502,91) -> 6 (rebind). X answers
what E was when the unit was observed; it cannot answer what E would
be under intervention.

Y = confounder-value reader (chain MAPs, rel 88 facts, query rel 92),
the MAP-representable half of what the do-operator needs. Facts:
(501,88,521), (521,88,1) and (502,88,522), (522,88,2). Training
queries: Y1 = (501,92) -> 1 (trial, plen 3), Y2 = (502,92) -> 2
(rebind of Y1). The do-operator itself (sever A->C, fix C, recompute
E) has no MAP form in any mechanism's ontology; that absence is the
gap under test, not an oversight.

World state (all arms): unit A-facts (501,86,1), (502,86,2);
declarative causal edges (801,71,802), (801,71,803), (802,71,803)
(A->C, A->E, C->E; inert, audit only); 30 interference facts
(5000+i, 60+(i%10), 6000+i). No comb node is installed, so the sum
template never fires in trial: the world tests causal to intervention
composition, and a coincidental sum of fact values must not
masquerade as an answer.

Intervention queries (the do-value is carried by the query relation,
the observed context by the subject unit):
- Z1 = (501,94) -> 5. do(C=2) on unit 501 (A_obs=1): sever A->C,
  E = 1 + 2*2 = 5. Observational predictor says 3. do != see.
- Z2 = (501,93) -> 3. do(C=1) on unit 501 (A_obs=1): E = 1 + 2*1
  = 3. Equals the observational answer. do == see.
- Z3 = (502,94) -> 6. do(C=2) on unit 502 (A_obs=2): E = 2 + 2*2
  = 6. do == see.
- Z4 = (502,93) -> 4. do(C=1) on unit 502 (A_obs=2): E = 2 + 2*1
  = 4. Observational predictor says 6. do != see.

Oracle (driver-level observability only, not a mechanism):
oracle_do(W, unit, c_do) = object of (unit,86) + 2*c_do, computed
from learner state. It implements the do-operator explicitly
(read parent value, inject do-value, recompute via the structural
equation) and doubles as the constructive specification of what the
gap requires. Expected: 5, 3, 6, 4.

## Mechanisms under test (all ported verbatim, sha256-verified)

- MECH-A: ../composition_A/cx_core.zag (dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6)
  + ../composition_A/cx_patch.zag + new driver. Contract chaining.
- MECH-B: head -1567 ../knowledge_composition/kc_core.zag
  + ../composition_B/cb_patch.zag + new driver. Co-use type-15 edges.
  TREAT runs one ev_cq co-use episode on fresh unit 503
  (503,81,513), (513,81,517), (517,81,3), (503,88,523), (523,88,1),
  (503,86,1): ev_cq(503,91,3) then ev_cq(503,92,1), giving B's
  history its best chance.
- MECH-C: ../composition_C/cc_base.zag + ../composition_C/cc_patch.zag
  + new driver. Constraint-driven assembly.
- MECH-XIO: ../composition_A/cx_core.zag (same hash as above)
  + ../xio_general/xio_core2.zag
  (5c0413af9a67583a36e22b3f333a36b11e5938f5ad0dbc8e9079e2da04e9ebe9)
  + new driver with the ev_query wrapper. Typed pairing, per-class
  stage dispatch.

Port fidelity: base/patch/core files are concatenated, never edited;
sha256 re-verified after assembly. Only the four drivers
(cd_driver_a/b/c/xio.zag) are new.

## Arms (per mechanism)

- TREAT: world facts; train X (81 facts + X1, X2); train Y (88 facts
  + Y1, Y2); gap; census; Z1..Z4. B additionally runs the 503
  co-use episode before Z. XIO uses xio_query with xio_on=1.
- ABL-X: train Y only (no 81 facts, no X queries); Z1..Z4.
- ABL-Y: train X only; Z1..Z4.
- FRESH: world facts only (no 81/88 facts, no training); Z1..Z4.
- ORACLE: world facts + 81/88 facts (no training needed); driver
  oracle reports Z1..Z4.
- AUDIT: train X+Y; mechanism-specific white-box probes (below).
- ABL-XIO (XIO only): TREAT with xio_on=0.

## Predicted mechanism behavior (frozen)

All pipelines run activate -> rebind -> composition -> trial ->
bootstrap. Rebind is relation-blind shape reuse, not composition.

- Z1 (do != see, answer 5): rebind fails everywhere (no path
  verifies to 5); every composition fails; trial fails (chain gives
  3/1/515/521, count gives 3/2/1, sum disabled, plen-2 gives
  non-answers). Predicted -2 on all four mechanisms.
- Z2 (do == see, answer 3): rebind of X1's plen-4 shape verifies
  3 == 3 on every mechanism. Predicted 3 via rebind (observational
  coincidence, disclosed; not composition).
- Z3 (do == see, answer 6): rebind of X verifies 6 == 6.
  Predicted 6 via rebind.
- Z4 (do != see, answer 4): rebind fails; composition fails;
  trial fails. Predicted -2 on all four mechanisms.
- No XIO-BUILD on any query (xio_has_typed = 0: the world has no
  NUMBER-typed MAP; XIO's typed-composition precondition never
  engages). No CX-STAT (A), no COMP-SEGS (C) anywhere. B emits
  COMPOSE pairs=1 on Z queries (the co-use edge passes the plen
  filter) but stages the intermediate value 3 through a plen-3 MAP
  with no len-3 path from 3, so no composite verifies.

## Kill bars (all must pass; verdict requires 9/9)

- K1 COMPETENCE: TREAT gives X1=3, X2=6, Y1=1, Y2=2 on all four
  mechanisms. X and Y are solidly learned; any Z failure is
  composition-specific.
- K2 SURGERY-CASES-FAIL: TREAT gives Z1=-2 and Z4=-2 on all four
  mechanisms. No XIO-BUILD lines and adapters=0 (XIO); no CX-STAT
  lines (A); no COMP-SEGS lines (C); no composite MAP promoted by
  any composition path on any Z query (B). The do != see cases,
  which require edge surgery, are unsolved by every mechanism.
- K3 ABLATION: ABL-X gives Z1=Z2=Z3=Z4=-2 on all mechanisms;
  ABL-Y gives Z1=-2, Z2=3, Z3=6, Z4=-2 (X alone suffices exactly
  for do == see); FRESH gives all -2 on all mechanisms.
- K4 ORACLE: the driver oracle reports 5, 3, 6, 4 on Z1..Z4. The
  world is solvable from learner state; the gap is in composition,
  not in the world.
- K5 XIO-DIAGNOSIS: AUDIT shows xio_has_typed=0 (typed composition
  never engages: the causal pair is node-typed throughout, so XIO's
  type axis is orthogonal to the gap); the sclass gate admits 0
  ordered pairs (every MAP is sclass 0; gate_rejected > 0), so even
  bypassing the precondition, XIO cannot pair the observational
  predictor with the confounder reader its own gate demands be
  structurally different; direct stage probes show
  xio_stage_exec(X,501)=3 (the confounded observational value),
  xio_stage_exec(Y,501)=515 (relation-blind re-derivation), and
  xio_stage_exec(Y,3)=xio_stage_exec(X,515)=-999999: no stage chain
  in the core's repertoire reaches 5.
- K6 A-DIAGNOSIS: census shows X MAPs with cx_contract=4 and Y
  MAPs with cx_contract=3 (both admitted; the failure is not
  admission, unlike the navigation/aggregation battery);
  compose_try runs and verifies 0 pairs; AUDIT shows t2_gather from
  each first-stage value (3 and 1) yields only the trivial 1-path,
  so the second stage has no plen-matching fact path: A's assembly
  is path concatenation, and the do-answer 5 is not at the end of
  any fact path.
- K7 B-DIAGNOSIS: the co-use episode writes >= 1 type-15 edge
  (cb_count15 >= 1; history crosses the gap); on Z1 B emits
  COMPOSE pairs=1 but no composite verifies (cb_stage of the
  second MAP on the intermediate value 3 returns -999999: the
  intermediate is a value with no outgoing facts); Z1=-2.
  History yes, assembly no.
- K8 C-DIAGNOSIS: census shows cc_relseq [81,81,81] for X MAPs and
  [88,88] for Y MAPs (non-empty; admitted as candidates); Z1 and
  Z4 emit COMP-FAIL; driver-called cc_dfs gives -1 for (501,5)
  and 1 segment for (501,3): C's search finds the observational
  predictor for the do == see goal and nothing for the surgery
  goal, proving C implements observational substitution, not
  intervention.
- K9 DETERMINISM: 3 full runs per mechanism are byte-identical
  (4 sha256 recorded in NAMECHECK.md).

## Verdict rule

XDOMAIN-CAUSAL-COMPLETE iff K1-K9 all PASS on the frozen design
above. Following the composition_xdomain precedent, COMPLETE marks
the battery as executed with exact-line gap diagnosis, not as
mechanism success: the predicted result is that all four mechanisms
fail the surgery cases. Any implementation existing at or before
this file's first commit voids the wave.

## Honest boundaries

- The do-value is carried by the query relation (93 = do(C=1),
  94 = do(C=2)). This is the query interface, not a hint: the
  mechanism still must combine the observed parent value with the
  do-value through the structural equation, which none can do.
- Y (confounder reader) is the MAP-representable half of the
  do-operator's needs; the operator itself (sever + recompute) has
  no MAP form. The composition under test is therefore X + Y_A +
  intervention -> Z, where the missing piece is named explicitly.
- Rebind is relation-blind shape reuse; its successes on Z2/Z3 are
  predicted observational coincidences, disclosed above, not
  composition and not counted as passes.
- B's co-use edge may link rebind-derived MAPs (rebind cross-serves
  in this all-chain world); the K7 claim is only that >= 1 type-15
  edge is written by the episode and that assembly fails on it.
- One causal structure (one confounder, linear equations). The
  generality claim is bounded to: the shared architectural reason
  (value chaining cannot express graph surgery), white-box evident
  in all four mechanisms' failure lines, not to sweeping the
  causal-structure space.
- Binary NODE/NUM kinds are syntactic, as in prior batteries.
- Expected answers are used for verification (same methodology as
  prior composition workers). Learner-owned verification of
  counterfactuals is future work.
