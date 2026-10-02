# REPORT.md: STRUCT-COMPOSITION -- Structure-Transforming Composition for Causal Intervention

## Verdict: STRUCT-COMPOSITION-COMPLETE

All 8 frozen kill bars (PREREG.md, commit dfa75105, committed before
any implementation existed) pass. A prototype sever+recompute
operator solves both do-surgery cases the four value-chaining
mechanisms failed (Z1=5, Z4=4), preserves the do==see controls
(Z2=3, Z3=6), generalizes unmodified to a second causal structure
with a different intervention target, and is shown experimentally to
be inexpressible as value chaining over values. Runs are 3/3
byte-identical.

## What was built

One new driver, sc_driver.zag (497 lines, 46 comment), assembled as
sc_full.zag = composition_A/cx_core.zag (dc0e86d44..., verbatim) +
composition_A/cx_patch.zag (c7074c5928..., verbatim, used ONLY for
ev_query, the learner's own trial/rebind engine, in the K1 census)
+ sc_driver.zag. The bases were never copied or edited; the
assembly is concatenation with recorded hashes. Binary sc_bin
(pinned znc 2026.07.0-dev, warnings only, exit 0); run outputs
sc_run1/2/3.txt (3/3 byte-identical,
f0374f3dc73c9393a958b5620b5b4f14158d9a7f0a8d79a606c3b430d779096c);
compile log sc_compile.txt.

The prototype mechanism is sc_do (sc_do_inner): given a unit and a
query relation, it reads the causal graph (rel-71 edge facts),
structural equations (rel-72 term facts, packed parent*10+coeff),
observation mapping (rel-70), and intervention spec (rel-69, packed
do_var*10+do_val) from learner state, then: (1) copies the edge list,
(2) severs incoming edges of the intervened variable on the working
copy, (3) fixes the intervened variable to the do-value,
(4) recomputes every other variable in topological order (Kahn) from
the surviving equations, with exogenous variables held at observed
values. Nothing about any particular variable is hardcoded; variable
enumeration is a generic scan of fact state (ids 800..920, a
disclosed working-memory bound). Surgery acts on the operator's
working copy; workspace facts are not mutated.

## Kill-bar scorecard

- K1 COMPETENCE: X1=3 (trial, tried=2 rejected=1), X2=6 (rebind),
  Y1=1 (trial, tried=2 rejected=1), Y2=2 (rebind). Trial statistics
  are identical to xdomain K1, confirming the frozen world was
  reproduced exactly. PASS.
- K2 SURGERY: TREAT answers exactly (5,3,6,4) on Z1..Z4, all PASS.
  The two queries every mechanism failed (Z1, Z4) are solved by the
  operator. PASS.
- K3 ABLATION: ABL-NOEDGE, ABL-NOEQ, ABL-NOOBS, FRESH all give -2 on
  every Z query with STRUCT-MISSING emitted. The operator reads
  structure; it has no hardcoded answers. (The X/Y MAPs are not
  inputs to the operator at all.) PASS.
- K4 GENERALITY: GEN arm gives exactly (3,0): do(Q=1) on unit 512
  (P_obs=2) severs P->Q and yields R=2+1=3 (observational R would be
  6); do(P=0) on unit 511 hits the root, where surgery is a no-op,
  and yields R=0. Same operator code, zero edits, new variables
  (811/812/813), new coefficients (Q=2*P, R=P+Q), new intervention
  target (middle variable Q), new topological role (root). PASS.
- K5 IRREDUCIBILITY: IRRED arm gives exactly (4,2) on Z1,Z4 with
  value facts identical to TREAT: same X/Y facts, same unit facts,
  same gap facts, same trial statistics (X1 tried=2 rejected=1 in
  both arms). The only change is structural: edge (801,71,803) and
  equation term (803,72,8011) deleted, so the structure now says
  E = 2*C. The answers move 5->4 and 4->2 with zero change to any
  value fact. PASS.
- K6 DEGENERATE: DEGEN arm gives exactly 7: with no intervention on
  a single-edge graph (OUT = 1*IN), the operator reduces to
  structure-respecting value propagation, which is what a single
  chain stage computes. PASS.
- K7 AUDIT: the surgery record for Z1 shows SEVER 801->802,
  topological order [802,801,803], recompute trace 802=2, 801=1,
  803=5, answer 5. The graph surgery is white-box visible. PASS.
- K8 DETERMINISM: 3/3 byte-identical. PASS.

## Generality analysis: generalization, not reduction

The preregistered question was whether sever+recompute can be
expressed as a generalization of value chaining, or is irreducibly
different. The experiments support a two-level answer:

1. Value chaining is the no-surgery degenerate case of the
   operator (K6). When the intervention set is empty and the graph
   is a single edge, sever+recompute is value propagation through
   fixed structure, exactly what a chain stage computes. So the
   operator strictly contains value chaining as a special case.

2. The surgery step itself has no value-chaining expression over
   values (K5). Any composition of the form m2(m1(s)) over the same
   value facts must emit identical outputs on identical inputs; the
   IRRED arm shows the operator emitting different outputs
   (5->4, 4->2) on identical value facts. The difference between
   the runs is structure, and the composition step is what rewrites
   structure. No choice of single-value intermediate stages can
   express edge deletion.

So: relative to the four mechanisms' ontology, where composition
means value chaining, causal-to-intervention composition is a
second, irreducibly structural composition kind (this is what
xdomain's uniform failure established, now with a constructive
positive). As a candidate for the ONE general composition
operation, sever+recompute strictly generalizes value chaining: it
adds a structure-rewriting dimension (sever on a graph copy, then
recompute over multi-source inputs: context + intervention +
equations) and recovers value chaining at the empty-surgery limit.
The architectural consequence is that the general operation must
take structures as arguments and return modified structures; an
operation confined to chaining single values through fixed
structures cannot express it.

## What the prototype does not do (honest boundaries)

1. Structural equations are declarative facts in this prototype
   (planted, like xdomain's edges). The operator reads them from
   learner state and nothing about A/C/E is hardcoded in it, but
   learning the equations from data is future work.
2. Two causal structures were tested (one confounder, one
   two-level chain). The generality claim rests on the operator's
   genericity (no world-specific code paths: enumeration,
   surgery, topo sort, and recompute are all structure-driven) and
   on the shared architectural reason, not on sweeping the
   causal-structure space.
3. Surgery operates on the operator's working copy of the edge
   list; workspace facts are not mutated, so repeated queries see
   the intact graph. A continuing-learner version would need a
   learner-owned scratch structure.
4. The do-value rides the query relation (93/94/95/96), the same
   interface as xdomain (disclosed).
5. Expected answers are used for verification, as in all prior
   composition batteries. Learner-owned verification of
   counterfactuals is future work.
6. ev_query (trial/rebind via the verbatim cx_patch) is used only
   for the K1 competence census. The prototype mechanism sc_do
   never calls compose_try, rebind_try, or any composition
   function; its Z answers come from the operator alone.

## Standing metrics

- Cognition lines added: 497 new driver lines (451 non-comment),
  of which the operator and its fact-state helpers are ~300; 0
  lines added to any mechanism or core.
- Modes / bridges / handlers / new core semantic cases: 0/0/0/0.
- Researcher-owned: world designs (variables, equations, units,
  do-relations), drivers, arm definitions, expected answers,
  equation/edge/observation-mapping facts (planted declarative
  structure, as in xdomain).
- Learner-owned: all X/Y MAP graphs, trial verifies, rebind
  decisions, trial statistics; every operator input (edges,
  equations, observations, intervention spec) is read from
  workspace fact state at composition time.
- Capability-source delta: one new prototype capability (do-query
  answering via explicit graph surgery) with a full generality and
  irreducibility analysis; zero new subsystems, modes, or core
  operations.

## Deliverables (all in struct_composition/)

- PREREG.md (frozen dfa75105, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check,
  port hashes, build/run log, scorecard)
- REPORT.md (this file)
- sc_driver.zag (new prototype mechanism + worlds + arms)
- sc_full.zag (assembled input: verbatim bases + driver)
- sc_bin (pinned znc build), sc_compile.txt
- sc_run1.txt, sc_run2.txt, sc_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, frozen sources untouched,
committed locally with explicit pathspecs, nothing pushed.
