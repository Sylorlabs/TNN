# REPORT.md: XDOMAIN-CAUSAL -- Cross-Domain Causal to Intervention Composition

## Verdict: XDOMAIN-CAUSAL-COMPLETE (with gap diagnosis)

All 9 frozen kill bars (PREREG.md, commit 2dc11c883, committed before
any implementation existed) pass. All four composition mechanisms (A:
plen-contract chaining; B: co-use type-15 edges; C: constraint-driven
assembly; XIO-general: typed pairing with per-class stage dispatch)
were ported verbatim (sha256-verified) and tested against a confounded
causal world with a genuine do-operator semantic gap. The result is
clean and uniform: every mechanism fails exactly the two queries that
require intervention (do != see), while the observational predictor
transfers exactly the two queries where do == see. A driver-level
oracle implementing the do-operator from learner state computes all
four answers, proving the world solvable and localizing the gap to
composition itself. Runs are 3/3 byte-identical per mechanism.

## What was built

Four new drivers in xdomain_causal/ (unfrozen); every mechanism core
is referenced verbatim in assembly, never copied or edited:

1. cd_driver_a.zag: world + arms for MECH-A.
   cd_full_a.zag = ../composition_A/cx_core.zag
   (dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6)
   + ../composition_A/cx_patch.zag + driver.
2. cd_driver_b.zag: same world + one ev_cq co-use episode on fresh
   unit 503 for MECH-B.
   cd_full_b.zag = head -1567 ../knowledge_composition/kc_core.zag
   + ../composition_B/cb_patch.zag + driver.
3. cd_driver_c.zag: same world + cc_dfs white-box probes for MECH-C.
   cd_full_c.zag = ../composition_C/cc_base.zag (same hash as
   cx_core) + ../composition_C/cc_patch.zag + driver.
4. cd_driver_xio.zag: same world + sclass gate audit and stage
   probes for MECH-XIO, with the ev_query wrapper.
   cd_full_xio.zag = ../composition_A/cx_core.zag
   + ../xio_general/xio_core2.zag
   (5c0413af9a67583a36e22b3f333a36b11e5938f5ad0dbc8e9079e2da04e9ebe9)
   + driver.

Binaries cd_bin_a/b/c/xio (pinned znc, warnings only); run outputs
cd_run_{a,b,c,xio}{1,2,3}.txt; compile logs cd_compile_*.txt.

## The world (frozen design, executed as preregistered)

Structural equation E = A + 2*C with confounder A in {1,2}, C = A.
Unit 501: A=1, C=1, E=3. Unit 502: A=2, C=2, E=6. X (rel 81, 3-link
chains, query rel 91) learns the observational mapping: X1=(501,91)
-> 3 via trial, X2=(502,91) -> 6 via rebind. Y (rel 88, 2-link
chains, query rel 92) learns the confounder value: Y1=(501,92) -> 1
via trial, Y2=(502,92) -> 2 via rebind. Query rel 93 = do(C=1),
94 = do(C=2):

- Z1=(501,94)->5: do(C=2) on A_obs=1 gives 1+4=5; observational
  predictor says 3. Surgery required.
- Z2=(501,93)->3: do(C=1) on A_obs=1 gives 3; equals observational.
- Z3=(502,94)->6: do(C=2) on A_obs=2 gives 6; equals observational.
- Z4=(502,93)->4: do(C=1) on A_obs=2 gives 2+2=4; observational
  says 6. Surgery required.

No comb node was installed, so trial's sum template never fires; a
coincidental sum of fact values cannot masquerade as an answer.

## Kill-bar scorecard

- K1 COMPETENCE: TREAT X1=3 (trial 2 tried 1 rejected), X2=6
  (rebind), Y1=1 (trial 2 tried 1 rejected), Y2=2 (rebind) on all
  four mechanisms. Census: X MAPs contract/plen 4, relseq
  [81,81,81], sclass 0; Y MAPs contract/plen 3, relseq [88,88],
  sclass 0. The structures are solidly learned; every Z failure is
  composition-specific. PASS.
- K2 SURGERY-CASES-FAIL: TREAT Z1=-2 and Z4=-2 on all four
  mechanisms; Z2=3 and Z3=6 via rebind (predicted observational
  coincidence, disclosed in prereg). Zero XIO-BUILD, CX-STAT, or
  COMP-SEGS emissions across all 12 runs (grep count 0): no
  mechanism built any composite on any Z query. PASS.
- K3 ABLATION: ABL-X gives -2 on all four Z queries; ABL-Y gives
  Z1=-2, Z2=3, Z3=6, Z4=-2 (X alone suffices exactly for do==see);
  FRESH gives -2 throughout; on all four mechanisms. The adapters
  and composites are causally necessary where they are needed, and
  X alone is sufficient exactly where no surgery is needed. PASS.
- K4 ORACLE: driver oracle reports 5, 3, 6, 4 on Z1..Z4 in every
  ORACLE arm. The world is solvable from learner state; the gap is
  in composition, not in the world. PASS.
- K5 XIO-DIAGNOSIS: AUDIT has_typed=0, so xio_try's precondition
  never engages: the causal pair is node-typed throughout and XIO's
  type axis (node vs number) is orthogonal to the gap. The sclass
  gate admits 0 ordered pairs (gate_rejected=12; every MAP is
  sclass 0): XIO's mismatch gate demands the two stages be
  structurally different, but the do-operator needs the
  observational predictor and the confounder reader, which are
  both guard-only chains, to cooperate. Direct stage probes:
  stage(X,501)=3 (the confounded observational value: C=1 bakes in
  A=1 via the backdoor), stage(Y,501)=515 (relation-blind
  re-derivation: the class-0 stage rebuilds from the first
  plen-matching path regardless of the MAP's own relation),
  stage(X,515)=stage(Y,3)=-999999. No stage chain in the core's
  repertoire reaches 5: the confounding baked into X's output is
  irreversible by value chaining. PASS.
- K6 A-DIAGNOSIS: census contracts 4,4,3,3: both families are
  admitted, so unlike the navigation/aggregation battery the
  failure is not at admission. compose_try runs and verifies 0
  pairs (no CX-STAT). AUDIT npaths(3)=1, npaths(1)=1: from each
  first-stage value (3 and 1) t2_gather yields only the trivial
  path, so the second stage has no plen-matching fact path to
  continue on. A's assembly is path concatenation; the do-answer 5
  is not at the end of any fact path. PASS.
- K7 B-DIAGNOSIS: co-use episode EP1=3, EP2=1 writes couse15=1
  (a genuine type-15 edge from the episode; history crosses the
  gap). On Z1 B emits COMPOSE pairs=1 (the edge passes the plen
  filter) but no composite verifies: cb_stage of the second MAP on
  the intermediate value 3 returns -999999, because the
  intermediate is a value with no outgoing facts. History yes,
  assembly no. The co-use edge endpoints are rebind-derived MAPs
  (rebind cross-serves in this all-chain world; disclosed). PASS.
- K8 C-DIAGNOSIS: relseq [81,81,81] and [88,88] are non-empty, so
  both families are admitted as candidates; Z1 and Z4 emit
  COMP-FAIL (DFS from 501/502: X walks to 3/6, Y walks to 1/2, and
  from every reached value no candidate continues). Driver-called
  cc_dfs gives -1 for (501,5) and 1 segment (seg0=35, the X MAP)
  for (501,3); -1 for (502,4) and 1 segment for (502,6). C's search
  finds the observational predictor for the do==see goal and
  nothing for the surgery goal: C implements observational
  substitution, not intervention. PASS.
- K9 DETERMINISM: 3/3 byte-identical per mechanism. A:
  acf56c38678bfaaefefbaf61d60aa0e5459e1dd80dcd6e785bdc6f0c72e7712d.
  B: a30dfaf94552a376c1066c0e5c836cf7e424953b8064d3089e436c46d7739281.
  C: fdf4ff51c39179ae14e4b0244ba56a54342040fcb69980c8aef25cef55ff4bbb.
  XIO: ab690089c8f5bc5d516024775c32ba507e8b9b8748e59145a27f52af2bf2659c.
  PASS.

## Per-mechanism diagnosis: the exact failure line

All four mechanisms implement composition as value chaining over
single values: v1 = stage(m1, s), v2 = stage(m2, v1), verify. The
do-operator is not a value function of the observational
predictor's output. do(C=c) requires: (1) reading the causal graph
to find C's parents, (2) severing the incoming edges of C so that
C=c no longer licenses the backdoor inference A=c, (3) keeping
every other variable at its observed value, (4) recomputing
downstream through the structural equations. Step (2) is a graph
surgery; steps (1), (3), (4) need multi-source inputs (observed
context + intervention spec + equations). Value chaining provides
none of these:

- A fails inside compose_try's inner loop: the second stage needs
  a plen-matching fact path from the intermediate value, and
  intermediate values (3, 1) have no outgoing facts. Admission
  (contracts 4 and 3) passes; assembly is path concatenation and
  the answer is not on any path.
- B fails inside cb_stage on the second fragment: the co-use edge
  is real (type-15 written by the episode), the pair passes the
  plen filter (COMPOSE pairs=1), but staging the second MAP on the
  intermediate value 3 finds no len-3 path and returns -999999.
  History crosses the domain gap; assembly cannot.
- C fails in cc_dfs: from every value reachable by the first
  segment (3, 6 via X; 1, 2 via Y), cc_candidates finds no MAP
  whose relation sequence continues, because continuing would
  require walking from a value node that has no outgoing facts.
  The DFS exhausts and emits COMP-FAIL. C's search semantics are
  relation walks; surgery is not a walk.
- XIO fails twice before staging: xio_has_typed=0 (no NUMBER MAP
  exists, so typed composition never engages) and the sclass gate
  rejects every ordered pair (both families are class 0, and the
  gate demands difference). Even bypassing both, the stage probes
  show the confounded value 3 flowing out of X's stage with no
  downstream stage able to un-confound it: value chaining cannot
  undo the backdoor inference once X has baked it into its output.

The shared broken assumption, one level deeper than the
navigation/aggregation battery: all four mechanisms assume the
composed computation is a function of the first stage's OUTPUT
VALUE. Under confounding, the correct interventional answer is not
a function of the observational output: X(501)=3 discards A_obs=1
and the intervention C=2 is never an input to any stage. The
information needed for surgery (which edges to sever, which values
to hold fixed) is structural, and no mechanism reads or writes
structure at composition time.

## What the gap requires (constructive specification)

The driver oracle is the executable spec: oracle_do(unit, c_do) =
A_obs(unit) + 2*c_do, where A_obs is read from the (unit,86) fact
and c_do comes from the query. Generalizing from the oracle to a
mechanism, causal to intervention composition needs:

1. Causal edges as readable learner state (which variable depends
   on which). Planted here as inert (801,71,*) facts; a real
   mechanism must learn them, not be given them.
2. A graph-surgery operator: do(C=c) deletes the incoming edges of
   C in the learner's causal graph and fixes C=c. This is a
   structure transformation, not a value mapping; none of the four
   mechanisms has any operation of this kind.
3. Re-execution of the downstream computation on the modified
   graph with all other variables held at observed values
   (multi-source input: context + intervention + equations).
4. A composition operator that takes structures as arguments and
   returns a modified structure (X transformed by the
   intervention), rather than chaining values through fixed
   structures.

Whether this structure-transforming operator collapses into ONE
general composition operation with chain/count/sum composition
(the October 2 composition question) is now an experimentally
sharpened question: value chaining (A/B/C/XIO) demonstrably cannot
express do-semantics, so either the general operation is strictly
more powerful than value chaining, or causal to intervention
composition is a second, irreducibly structural composition kind.

## Honest boundaries

1. One causal structure (one confounder, E = A + 2*C). The
   generality claim rests on the shared architectural reason
   (value chaining cannot express graph surgery), white-box
   evident in all four mechanisms' failure lines, not on sweeping
   the causal-structure space.
2. The do-value rides the query relation (93/94). This is the
   query interface; the mechanism must still combine the observed
   parent value with the do-value through the structural equation,
   which none can do.
3. Y (confounder reader) is the MAP-representable half of what the
   do-operator needs; the operator itself (sever + recompute) has
   no MAP form in any mechanism's ontology. The tested composition
   is X + Y + intervention -> Z with the missing piece named.
4. Rebind is relation-blind shape reuse; its successes on Z2/Z3
   are predicted observational coincidences (do==see), disclosed
   in the prereg, not composition passes.
5. B's co-use edge links rebind-derived MAPs (rebind cross-serves
   in this all-chain world); the K7 claim is only that the episode
   writes >= 1 type-15 edge and assembly fails on it.
6. Expected answers are used for verification, as in all prior
   composition batteries. Learner-owned verification of
   counterfactuals is future work.
7. Binary NODE/NUM kinds are syntactic, as in prior batteries.

## Standing metrics

- Cognition lines added: 0 to mechanisms; ~330 new driver lines
  (4 drivers).
- Modes / bridges / handlers / new core semantic cases: 0/0/0/0.
- Researcher-owned: world design (structural equation, confounded
  units, do-relations), drivers, arm definitions, B episode
  queries, oracle ground-truth check.
- Learner-owned: all X/Y MAP graphs, rebind decisions, type-15
  edge endpoints, trial verifies, all stage values, all gate
  decisions.
- Capability-source delta: zero new capabilities; one new hard
  boundary with exact-line diagnoses for all four mechanisms.

## Deliverables (all in xdomain_causal/)

- PREREG.md (frozen 2dc11c883, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check,
  port hashes, build/run log, scorecard)
- REPORT.md (this file)
- cd_driver_a/b/c/xio.zag (new, unfrozen drivers)
- cd_full_a/b/c/xio.zag (assembled inputs, verbatim cores)
- cd_bin_a/b/c/xio (pinned znc builds), cd_compile_*.txt
- cd_run_{a,b,c,xio}{1,2,3}.txt (3/3 byte-identical per mechanism)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, frozen sources untouched,
committed locally with explicit pathspecs, nothing pushed.
