# PREREG: XP-SELECT-5 (navigation to aggregation, PATH-COVERAGE mismatch, {TRUNCATE, REROUTE} selection)

Frozen 2026-10-02. Committed alone before implementation.
Worker: XP-SELECT-5 (replacement for completed XP-SELECT-4).
Branch: shared lane branch, local only, nothing pushed.

## Objective

Complete the XP-SELECT line's coverage of the four original L1 domain
pairs with mismatch. Priors: arithmetic to planning (length C322,
direction C331), causal to intervention (arity C339), grammar to
program (strictness C344), all PASS K1-K13. The remaining uncovered
pair is NAVIGATION to AGGREGATION. This probe adds a principled
MISMATCH that the exact pipeline cannot solve, and the learner must
SELECT the adaptation operation itself.

The L1 navigation x aggregation work (composition_xdomain) showed
mechanisms A/B/C all fail the pair because every one of them defines
composition as navigation concatenation: a count MAP (INC cells,
arithmetically computed output, no walkable output literal) is
invisible to their admission filters and unassemblable by t2_asm_chain.
H2 (xdomain_value) solved the exact pair with value-level function
composition: execute the chain as a function, feed the intermediate
VALUE to the count template. This probe builds its exact pipeline on
that value-level principle, but derives the function types from learner
state (chain MAP vs INC-cell MAP) rather than researcher-defined modes,
and adds the evidence-driven selector for the mismatch.

## Domain design (frozen)

- Relation 81 = "nav-step": (x,81,y) means y is the next node on the
  route from x. X's learned route is a chain of 81 facts.
- X = learned navigation structure (a route). Trained by ev_teach
  (11,81,12), (12,81,13), (13,81,14), then ev_query (11,91,14) ->
  MAP_X with relseq [81,81,81]. X's output is a node (the route
  endpoint). Relation 91 = X's query relation.
- Relation 82 = "item-link": (x,82,y) links the aggregation chain.
  Y counts the links of the 82-chain from its subject. The chain
  (not star) shape is load-bearing: t2_chain follows one chain per
  relation.
- Y = learned aggregation procedure (counting over visited nodes).
  Trained by ev_teach (50,82,51), (51,82,52), (52,82,53), then
  ev_query (50,92,3) -> MAP_Y, a count graph (guard/set links plus
  INC cells tag 103 and a MOV epilogue). Y's output is a NUMBER
  (the link count), not a node. Relation 92 = Y's query relation.
  Y's aggregation relation (82) is read by the learner from MAP_Y's
  type-1 provenance edges to its licensing facts, never hardcoded.
- Relation 84 = "detour": an alternative navigation step, never
  learned by X. Used only in BRANCH worlds as the store-read
  substitute hop.
- Query relation 93 = "navigate-then-aggregate": (site-query
  start,93,count) = "route to the aggregation site, then count".
- 30 distractor teaches (subjects 5000+, relations 60-69) separate
  training from Z in every arm. Distractor teaches induce no MAPs.

## Family selection rationale (frozen)

The task suggests PATH-COVERAGE (X's learned route covers a different
node set than Y's aggregation needs) or ORDER (X's route order does
not match Y's expected traversal). ORDER is untestable on this pair:
Y's aggregation (link count) is order-invariant, so no route
permutation defeats the exact pipeline; K5 could never pass. A pure
relabel of the route relation is untestable for the line's standard
reason (the XDOMAIN-L2-ADAPT amendment records the pilot: the unified
composition's contract fallback solves a pure relation rename with
zero adaptation fired); adapted here, a pure 81->81 rename changes
nothing observable.

The PATH-COVERAGE family is the operationalization that survives. X's
route is a node sequence; Y's aggregation applies to a SITE (a node
whose 82-chain is counted). Composition requires the route to END at
the site. The mismatch is a coverage mismatch: the set of nodes X's
route visits does not end at the site. Two sub-cases:

- OVERSHOOT (A1): the site IS on X's route, but the route continues
  past it. The route covers the site but ends elsewhere (at a node
  with no 82-chain). Fix: TRUNCATE the route to end at the site.
- BRANCH (A2): the site is NOT on X's route. X's route ends at a
  node with no 82-chain; the site sits on a detour branch (relation
  84, never learned by X). Fix: REROUTE, substituting the divergent
  hop with the store-read detour fact.

The two selectable operations, drawn from the mandated L2 set
(truncate, extend, specialize, substitute):

- TRUNCATE: hypothesis "the learned route overshoots the aggregation
  site"; adapt to the longest prefix of the learned relation sequence
  whose endpoint carries Y's aggregation chain (minimal adaptation).
- REROUTE: hypothesis "the learned route misses the site entirely";
  adapt by substituting exactly one hop with a store-read alternative
  relation (r_alt != the learned hop relation, so the adapted relseq
  stays relation-specific and deterministic under t2_lu_first),
  truncating after the substitute (minimal adaptation).

Both preserve the navigation domain of X; the adaptation is on X's
route coverage, licensed cross-domain by Y's native aggregation
interface (the count template over Y's provenance-derived relation)
executing successfully, expected-free, on the adapted endpoint.
Strictness mismatches on Y are out of scope; direction is out of scope
(XP-SELECT-2's family); length-as-such is out of scope (C322's family).
This probe adds only the evidence-driven selector on the new pair,
not a finite operator menu.

## Operator specification (frozen): XS5-SELECT

Fires exactly once per query, only after the standard pipeline
(activate, rebind_try, xs5_compose, trial, bootstrap) has failed. It
never fires when composition succeeds, so L1 exact-reuse behavior is
unreachable by it. adapt_on() gates the bracket; the no-adapt control
build differs by exactly one line (adapt_on 1 -> 0).

Value-level exact composition (xs5_compose, the pipeline's
composition step): function types derived from learner state, not
researcher modes. A MAP is NAV iff cc_relseq extracts a non-empty
relation sequence (pure chain structure). Aggregation capability iff a
live MAP's graph contains an INC cell (tag 103); its relation r_agg
comes from that MAP's type-1 provenance edges to licensing facts.
xs5_compose tries (NAV,AGG): for each live NAV MAP m in id order,
e = nav_exec(m,s) = cc_satisfy walk of m's relseq from s; then
v = agg_exec(e,r_agg) = count template over e's r_agg chain,
masked; if v==expected, promote MAP_Z (LINK14 to m and to the count
MAP) and return v. Then (AGG,NAV) symmetrically (fails in practice:
a count is not a walkable subject). Ordered pairs are tried, not
given (H2 precedent); the types themselves are structural.

Phase 1 (adaptation, expected-free). r_agg from the count MAP's
provenance; if none, the selector cannot fire. For each live native
NAV MAP m (tag 20, live, cc_relseq length L with 2 <= L < 7, no
outgoing type-16 edge), in node-id order, in frozen priority order
(TRUNCATE before REROUTE per m; both may fire):

1. TRUNCATE branch: for Lp = L-1 down to 1 (longest first):
   candidate prefix R[0..Lp-1]. Dedup: skip if any live MAP
   already carries exactly this relseq. Walkability: the prefix
   must fully walk from s via t2_lu_first. License: agg_exec(e,
   r_agg) != -2 on the endpoint e (Y's native interface applies,
   expected-free). Assemble with t2_asm_chain and promote with
   xs5_promote (MAP node layout identical to promote_graph but
   teaching NO fact: mid-query scaffolding is not a verified query
   answer). Write a type-16 LINK adapted -> m ("adapted-from").
   Emit ADAPT-MK op=TRUNCATE. At most one TRUNCATE per m
   (longest licensed prefix wins).
2. REROUTE branch: for i = 0..L-1: walk R[0..i-1] from s via
   t2_lu_first; if any hop fails, stop (no deeper reroute). Let
   u be the reached node. Find the lowest-id live fact (u, r_alt,
   w) with r_alt != R[i] (a genuinely different hop relation, so
   the adapted relseq is deterministic under t2_lu_first; the
   same-relation branch case is an honest boundary, not covered).
   Candidate relseq R[0..i-1] ++ [r_alt]. Dedup as above. The
   candidate walks by construction. License: agg_exec(w, r_agg)
   != -2. Assemble, promote, type-16 LINK adapted -> m. Emit
   ADAPT-MK op=REROUTE. At most one REROUTE per m (first
   licensed i wins).

Generality (frozen claim): the selector names no relation, no MAP,
no length, no query, and no site. Walk relations come from the
source relseq; the substitute relation comes from the fact store;
lengths come from satisfiability evidence only. Arm A1 proves no
hardcoded truncation point (longest licensed prefix wins); arm A2
proves no hardcoded detour relation (frontier fact read live; the
adapted relseq mixes relations 81 and 84).

Phase 2 (completion). The adapted routes are forward traversable,
so Phase 2 re-runs the UNCHANGED xs5_compose exactly once (frozen
L2-ADAPT precedent). If at least one adapted MAP was created and the
re-run verifies against expected, MAP_Z is promoted with the
standard value-level provenance (LINK14 to the NAV MAP used and to
the count MAP). A licensed-but-wrong adaptation cannot produce a
false positive: the verifier checks expected. Ambiguity (A10) is
resolved by the verifier, deterministically by candidate ordering
(id order, then verification).

Adapted marking (frozen): a MAP is ADAPTED iff it has an outgoing
type-16 edge; NATIVE MAPs have none. On success MAP_Z carries
LINK14 to the adapted NAV MAP used and to the count MAP, never to
an unused adapted MAP and never to the source m.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X and Y
as above, then 30 distractor teaches, then Z facts, then exactly
one query via ev_query_xs5 (the value-level pipeline plus the
XS5-SELECT bracket; cc_base.zag and un_patch.zag used verbatim).

- A1 SELECT-TRUNCATE (overshoot): Z facts (101,81,102),
  (102,81,103), (103,81,104), (103,82,201), (201,82,202).
  Query (101,93,2). Expect: ans=2; exactly one adapted MAP t;
  t has type-16 edge to MAP_X; relseq(t)==[81,81];
  start(t)==101; end(t)==103; MAP_Z has LINK14 to t and to
  MAP_Y; MAP_Z has no LINK14 to MAP_X; trace shows ADAPT-MK
  op=TRUNCATE and no ADAPT-MK op=REROUTE.
- A2 SELECT-REROUTE (branch): Z facts (101,81,102),
  (102,81,103), (102,84,105), (105,82,201), (201,82,202),
  (202,82,203). Query (101,93,3). Expected=3 (not 2) so the
  trial's route-link count (2) cannot coincide with it.
  Expect: ans=3; exactly one adapted MAP d; type-16 d->MAP_X;
  relseq(d)==[81,84]; start(d)==101; end(d)==105;
  MAP_Z LINK14 to d and to MAP_Y, none to MAP_X; trace shows
  ADAPT-MK op=REROUTE and no ADAPT-MK op=TRUNCATE.
- A3 REJECT: Z facts (101,81,102), (102,81,103), (103,81,104)
  [no 82-chain anywhere]. Query (101,93,2). Expect: ans=-2;
  zero type-16 edges workspace-wide (selector fired, nothing
  licensed; clean reject).
- A4 L1-REGRESSION: Z facts (101,81,102), (102,81,103),
  (103,81,104), (104,82,201), (201,82,202).
  Query (101,93,2). Expect: ans=2; zero type-16 edges (exact
  value-level composition succeeds; selector never fires);
  MAP_Z has LINK14 to MAP_X and to MAP_Y.
- A5 NO-ADAPT CONTROL: A1 setup verbatim, run under the one-line
  no-adapt build (adapt_on()=0). Expect: ans=-2 and zero adapted
  MAPs. This proves the selector did the work: the exact pipeline
  (activate, rebind, xs5_compose, trial, bootstrap) cannot solve
  the overshoot task.
- A6 ABL-X: A1 setup, MAP_X killed before the Z query. Expect
  ans=-2 (nothing to coverage-adapt).
- A7 ABL-Y: A1 setup, MAP_Y killed before the Z query. Expect
  ans=-2 (no native aggregation interface: r_agg underivable and
  the capability check fails, so nothing licenses).
- A8 FRESH: no X/Y training (distractors + A1 Z facts only).
  Query (101,93,2). Expect ans=-2 (fresh learner fails outright).
- A9 REUSE: A1 setup, query (101,93,2) twice. Expect: both
  ans=2; adapted MAP count stays 1 after the second query
  (dedup blocks re-adaptation; the unchanged xs5_compose reuses
  the adapted MAP as a NAV candidate; the selector never fires
  on the second query).
- A10 AMBIGUOUS-SELECT: Z facts (101,81,102), (102,81,103),
  (103,81,104), (102,84,105), (103,82,301), (105,82,401),
  (401,82,402). Query (101,93,2). Both branches licensed
  expected-free: TRUNCATE walks 101->103 (agg=1, licensed but
  wrong), REROUTE walks 101->102->105 (agg=2, licensed).
  Expect: ans=2; exactly two adapted MAPs, both with type-16
  edge to MAP_X; one with end==103 (call it t), one with
  end==105 (call it d); MAP_Z has LINK14 to d and to MAP_Y;
  MAP_Z has no LINK14 to t and none to MAP_X; two type-16 edges
  total. The verifier, not a world flag, picks the
  expected-consistent adaptation.

## K5 rationale: why the exact pipeline must fail (frozen)

Arm A1 (A2/A3 analogous with the noted differences):
- activate: no (101,93,2) fact exists.
- rebind_try: X's chain MAP rebinds via relation-blind gathered
  paths, but every assembled chain returns a node, never the
  number 2; Y's count MAP is not rebindable (trial-only shape).
- xs5_compose: (NAV,AGG): nav_exec(X,101) walks [81,81,81] to
  104; agg_exec(104,82) fails (104 has no 82-chain, t2_chain
  len<2). No other NAV MAP. (AGG,NAV): agg on 101 fails (no
  82-chain at 101); a count is not a walkable nav subject
  anyway. Result -2.
- trial: chain trial seeks a node path to the number 2 (none);
  count trial counts 101's 81-chain (3 links) != 2; single-hop
  fails. Result -2.
- bootstrap_miss: miss path, no answer. Result -2.
A2 note: nav_exec(X,101) fails outright ([81,81,81] not walkable:
102->103 exists but 103 has no 81 onward); trial counts 2 != 3.
A3 note: no 82-chain anywhere, so agg_exec fails on every
endpoint. Validated pre-freeze by the well-formedness prototype
(see NAMECHECK.md): exact pipeline gives -2 on the A1, A2, A3
shapes and 2 on the A4 shape, with X=[81]x3 and Y a 3-link
82-chain count intact.

## Kill bars (frozen)

- K1: A1 all assertions pass (selector chose TRUNCATE).
- K2: A2 all assertions pass (selector chose REROUTE with a
  store-read detour relation 84, mixed-relation relseq).
- K3: A3 ans=-2 and zero adapted MAPs created.
- K4: A4 passes with zero type-16 edges (no regression; selector
  inert on exact-reuse worlds).
- K5: A5 ans=-2 and zero adapted MAPs (exact value-level control
  provably fails the overshoot task).
- K6: A6, A7, A8 all ans=-2 (causal dependence on X and Y;
  fresh learner fails).
- K7: A9 both queries ans=2, adapted count stable at 1, second
  query fires no selector.
- K8: A10 all assertions pass (both operations licensed;
  verifier selected the expected-consistent one; unused
  adaptation not composed).
- K9: 3/3 byte-identical runs for both binaries; sha256 recorded.
- K10: zero em/en dashes in all deliverables (byte-verified).
- K11: cc_base.zag sha256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  and composition_unified/un_patch.zag sha256
  3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
  both used verbatim via build concatenation, never modified.
  (un_patch.zag is used only for cc_relseq/cc_satisfy; its
  unified compose_try/ev_query are not called by this lane.)
- K12: 0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 semantic cases (selector uses only existing
  machinery: cc_relseq, cc_satisfy, t2_lu_first, t2_chain,
  t2_asm_chain, t2_asm_count, t2_try_verify, alloc_node,
  link_edge, promote_graph layout via xs5_promote; edge types 1,
  2, 6, 13, 14, 16 only; 15 unused by this lane).
- K13 NO-REBUILD: every adapted MAP has exactly one outgoing
  type-16 edge to a live native MAP; for TRUNCATE the adapted
  relseq is a strict prefix of the source relseq; for REROUTE the
  adapted relseq shares a proper prefix with the source relseq,
  diverges at exactly one hop position with a store-read
  relation, and is no longer than the source; and the adapted
  MAP's licensing fact ids are disjoint from the source MAP's
  training fact ids. Driver asserts per arm. A from-scratch
  rebuild cannot satisfy parentage + provenance +
  fact-disjointness + dedup simultaneously.

Verdict XP-SELECT-5-PASS iff K1-K13 all pass.

## Implementation plan (after prereg commit)

1. Write xs5_patch.zag (xs5_agg_rel, xs5_nav_exec, xs5_agg_exec,
   xs5_compose, XS5-SELECT Phase 1, ev_query_xs5 with the
   unchanged xs5_compose re-run, adapt_on()=1) and
   xs5_patch_noadapt.zag (one-line diff: adapt_on 1 -> 0);
   verify the diff is exactly one line.
2. Write xs5_driver.zag (arms A1-A4, A6-A10 + assertions) and
   xs5_driver_noadapt.zag (arm A5).
3. Build: cat composition_C/cc_base.zag
   composition_unified/un_patch.zag xs5_patch.zag xs5_driver.zag
   > xs5_full.zag; same with noadapt parts for
   xs5_full_noadapt.zag.
4. Compile with the pinned znc_linux_x86_64_abed8aa1; run 3x
   each; verify byte-identical; check kill bars.
5. Write REPORT.md. Commit with explicit pathspecs.

## Constraints

Unfrozen only (xdomain_select5/). Frozen read-only
(cc_base.zag, composition_unified/un_patch.zag). Pure Zag
(safebin PATH, no python). Zero em/en dashes. Nothing pushed.
No domain-pair-specific composition handler: the selector is
anchored only at the query start and reads candidates from
source relseqs and the fact store. No paired X->Y training
examples. No finite operator menu widening: the PATH-COVERAGE
family {TRUNCATE, REROUTE} is the line's shared selector shape
on the fourth pair; this worker adds only the evidence-driven
selector. Phase 2 is the unchanged xs5_compose re-run (L2-ADAPT
precedent), not new completion code. Function types (NAV vs
aggregation) are structural over learner state (relse q
extractable vs INC cell present), not researcher modes.

## Battery well-formedness (disclosed pre-freeze work)

Before freezing, a throwaway prototype ran in
~/workspace/_scratch_xs5 (outside the repo, never committed,
deleted after): (1) the exact pipeline (cc_base.zag +
un_patch.zag plus a minimal exact value-level composition, NO
selector code) on the A1/A2/A3/A4 shapes, confirming ans=-2 for
the mismatch shapes and ans=2 for the exact shape, with
X=[81]x3 and Y a 3-link 82-chain count intact; (2) the
r_agg derivation (82 from MAP_Y type-1 provenance), the
cc_satisfy nav walk, and the count-template agg execution.
It caught two design bugs pre-freeze: Y must be taught as an
82-CHAIN (t2_chain follows one chain per relation) and A2's
expected (3) must not coincide with the trial's route-link
count (2). These validated only that the arms are well-formed
against the shared machinery, not experimental outcomes. No
selector/orchestration code was prototyped. The frozen bars were
not adjusted to fit any outcome.
