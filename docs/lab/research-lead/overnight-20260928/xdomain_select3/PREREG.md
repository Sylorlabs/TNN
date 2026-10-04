# PREREG: XP-SELECT-3 (causal to intervention, INTERFACE-ARITY mismatch, {TRUNCATE, EXTEND} selection)

Frozen 2026-10-02. Committed alone before implementation.
Worker: XP-SELECT-3 (replacement for completed XP-SELECT-2).
Branch: lane-compinteg2-20261002, local only, nothing pushed.

## Objective

Break the domain-pair boundary of the XP-SELECT line. XP-SELECT
(C322) and XP-SELECT-2 (C331) both used arithmetic to planning.
This probe uses CAUSAL MODEL to INTERVENTION, the pair Micah's
high-value list names explicitly ("causal model to intervention
requiring adaptation"). The earlier XDOMAIN-CAUSAL-INTERV work
demonstrated this pair with EXACT reuse; this probe adds a
principled MISMATCH that the exact pipeline cannot solve, and the
learner must SELECT the adaptation operation itself.

## Family selection rationale (frozen)

The task suggests an interface mismatch such as X's output arity
or keying differing from Y's input expectations, or X's causal
variables needing re-keying to match Y's action space. A pure
relabel or re-keying at EQUAL arity is untestable in this
substrate: the XDOMAIN-L2-ADAPT amendment (PREREG_AMENDMENT1,
2026-10-02) records a pilot proving the unified composition's
contract fallback (mechanism A: relation-blind plen matching over
t2_gather paths) solves a pure relation rename directly with zero
adaptation fired. Any equal-arity re-keying is therefore solved by
the exact pipeline, so K5 (no-adapt control must fail) could never
pass. This is the same load-bearing lesson XP-SELECT-2 applied
when it rejected the suggested value-range relabel.

The INTERFACE-ARITY family is the operationalization that
survives: X's learned causal-step interface (a 4-hop causal walk)
differs in arity from the Z world's causal depth (3 hops in A1,
5 hops in A2). X therefore cannot produce the outcome key that Y's
intervention action space expects, and every exact mechanism fails
for a structural reason (see K5 rationale). The two selectable
operations, drawn from the mandated L2 set:

- TRUNCATE: hypothesis "the learned interface is too long";
  adapt to the longest frontier-licensed proper prefix of the
  learned relation sequence (minimal adaptation).
- EXTEND: hypothesis "the learned interface is too short";
  adapt to the learned relation sequence plus exactly one real
  frontier fact read from the fact store.

Both preserve the causal domain of X; the adaptation is on X's
interface arity, licensed cross-domain by Y's native intervention
interface strictly satisfying forward from the adapted endpoint
(the adapted endpoint is the causal variable re-keyed to Y's
action space). Length mismatches on Y are out of scope
(XP-SELECT's family); direction is out of scope (XP-SELECT-2's
family). This probe adds only the evidence-driven selector on the
new pair, not a finite operator menu.

## Learned structures (frozen)

- X: causal model. Trained by ev_teach (201,91,211), (211,91,221),
  (221,91,231), (231,91,241), then ev_query (201,93,241) ->
  MAP_X with relseq [91,91,91,91] (4 causal hops).
- Y: intervention procedure. Trained by ev_teach (241,92,251),
  (251,92,261), then ev_query (241,94,261) -> MAP_Y with relseq
  [92,92] (2 intervention hops).
- 30 distractor teaches (subjects 5000+, relations 60-69) separate
  training from Z in every arm. Distractor teaches induce no MAPs.

## Operator specification (frozen): XS3-SELECT

Fires exactly once per query, only after the standard pipeline
(activate, rebind_try, compose_try with compose_on) has failed. It
never fires when composition succeeds, so L1 exact-reuse behavior
is unreachable by it. adapt_on() gates the bracket; the no-adapt
control build differs by exactly one line (adapt_on 1 -> 0).

Phase 1 (adaptation, expected-free). For each live native MAP m
(tag 20, live, no outgoing type-16 edge), in node-id order, read
its relseq R (length L, 2 <= L < 7 via cc_relseq). In frozen
priority order (TRUNCATE before EXTEND per m; both may fire):

1. TRUNCATE branch: for Lp = L-1 down to 1 (longest first):
   candidate prefix R[0..Lp-1]. Dedup: skip if any live MAP
   already carries exactly this relseq (adaptation changes the
   relseq, so relseq-level dedup is sound here, unlike the
   direction family). Satisfiability: the prefix must fully walk
   forward from s via t2_lu_first (rl_satisfy_seq pattern).
   License: some native MAP m2 (tag 20, live, no outgoing
   type-16 edge, m2 != m) strictly satisfies its own relseq
   forward from the endpoint e (cc_satisfy >= 1, no contract
   fallback; expected-free). Assemble with t2_asm_chain and
   execution-verify with t2_try_verify against e. On success
   promote with xs3_promote (MAP node layout identical to
   promote_graph but teaching NO fact: mid-query scaffolding is
   not a verified query answer) and write a type-16 LINK
   adapted -> m ("adapted-from"). Emit ADAPT-MK op=TRUNCATE.
   At most one TRUNCATE per m (longest licensed prefix wins).
2. EXTEND branch: walk the full R forward from s via
   t2_lu_first; if any hop fails there is no candidate. Let eL
   be the endpoint. Find the lowest-id live non-superseded fact
   with subject = eL, excluding facts used in the walk; its
   relation r_new comes from the fact store (never hardcoded).
   Candidate relseq R' = R ++ [r_new]. Same dedup, license
   (native m2 != m, cc_satisfy from the new endpoint),
   assemble, verify, promote, type-16 LINK adapted -> m.
   Emit ADAPT-MK op=EXTEND. At most one EXTEND per m.

Generality (frozen claim): the selector names no relation, no
MAP, no length, no query. Walk relations come from the source
relseq; the extension relation comes from the fact store; depths
come from satisfiability evidence only. Arm A1 proves no
hardcoded truncation depth (longest licensed prefix wins); arm
A2 proves no hardcoded extension (frontier fact read live).

Phase 2 (completion). The adapted segments are forward
traversable (unlike the direction family), so Phase 2 re-runs the
UNCHANGED compose_try exactly once (frozen L2-ADAPT precedent).
If at least one adapted MAP was created and the re-run verifies
against expected, MAP_Z is promoted with the standard compose
provenance (LINK14 to each segment used, type-15 co-use between
consecutive segments). A licensed-but-wrong adaptation cannot
produce a false positive: the verifier checks expected. Ambiguity
(A10) is resolved by the verifier, deterministically by candidate
ordering (co-use, then decreasing length, ties by MAP id).

Adapted marking (frozen): a MAP is ADAPTED iff it has an outgoing
type-16 edge; NATIVE MAPs have none. On success MAP_Z carries
LINK14 to the adapted segment used and to the native second
segment, never to an unused adapted MAP and never to the source m.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X and Y
as above, then 30 distractor teaches, then Z facts, then exactly
one query via ev_query_adapt (the unified pipeline plus the
XS3-SELECT bracket; cc_base.zag and un_patch.zag used verbatim).

- A1 SELECT-TRUNCATE: Z facts (101,91,102), (102,91,103),
  (103,91,104), (104,92,105), (105,92,106).
  Query (101,70,106). Expect: ans=106; exactly one adapted MAP a;
  a has type-16 edge to MAP_X; relseq(a)==[91,91,91];
  start(a)==101; end(a)==104; MAP_Z has LINK14 to a and to
  MAP_Y; MAP_Z has no LINK14 to MAP_X; trace shows ADAPT-MK
  op=TRUNCATE and no ADAPT-MK op=EXTEND.
- A2 SELECT-EXTEND: Z facts (101,91,102), (102,91,103),
  (103,91,104), (104,91,105), (105,91,106), (106,92,107),
  (107,92,108). Query (101,70,108). Expect: ans=108; exactly one
  adapted MAP a; type-16 a->MAP_X; relseq(a)==[91,91,91,91,91];
  start(a)==101; end(a)==106; MAP_Z LINK14 to a and to MAP_Y,
  none to MAP_X; trace shows ADAPT-MK op=EXTEND and no ADAPT-MK
  op=TRUNCATE.
- A3 REJECT: Z facts (101,91,102), (102,91,103), (103,91,104),
  (104,83,105), (105,83,106) [relation 83 has no learned
  interface]. Query (101,70,107). Expect: ans=-2; zero type-16
  edges workspace-wide (selector fired, nothing licensed; clean
  reject).
- A4 L1-REGRESSION: Z facts (101,91,102), (102,91,103),
  (103,91,104), (104,91,105), (105,92,106), (106,92,107).
  Query (101,70,107). Expect: ans=107; zero type-16 edges (exact
  composition succeeds; selector never fires); MAP_Z has LINK14
  to MAP_X and to MAP_Y.
- A5 NO-ADAPT CONTROL: A1 setup verbatim, run under the one-line
  no-adapt build (adapt_on()=0). Expect: ans=-2 and zero adapted
  MAPs. This proves the selector did the work: the exact pipeline
  (activate, rebind, compose, trial, bootstrap) cannot solve the
  interface-arity mismatch task.
- A6 ABL-X: A1 setup, MAP_X killed before the Z query. Expect
  ans=-2 (nothing to arity-adapt).
- A7 ABL-Y: A1 setup, MAP_Y killed before the Z query. Expect
  ans=-2 (no native interface to license the adaptation).
- A8 FRESH: no X/Y training (distractors + A1 Z facts only).
  Query (101,70,107). Expect ans=-2 (fresh learner fails
  outright).
- A9 REUSE: A1 setup, query (101,70,106) twice. Expect: both
  ans=106; adapted MAP count stays 1 after the second query
  (dedup blocks re-adaptation; the unchanged compose_try reuses
  the adapted MAP as a level-0 candidate; no spurious
  re-adaptation).
- A10 AMBIGUOUS-SELECT: Z facts (101,91,102), (102,91,103),
  (103,91,104), (104,92,105), (105,92,106), (104,91,107),
  (107,91,108), (108,92,109), (109,92,110).
  Query (101,70,110). Both branches licensed: TRUNCATE walks
  101->104 (Y reaches 106, wrong but licensed expected-free),
  EXTEND walks 101->107 plus frontier fact (107,91,108) to 108
  (Y reaches 110). Expect: ans=110; exactly two adapted MAPs,
  both with type-16 edge to MAP_X; one with end==104 (call it
  t), one with end==108 (call it p); MAP_Z has LINK14 to p and
  to MAP_Y; MAP_Z has no LINK14 to t and none to MAP_X; two
  type-16 edges total. The verifier, not a world flag, picks the
  expected-consistent adaptation.

## K5 rationale: why the exact pipeline must fail (frozen)

Arm A1 (A2 analogous with longer counts):
- activate: no (101,70,106) fact exists.
- rebind_try: X's relseq [91,91,91,91] is unsatisfiable from 101
  (only three r91 hops); Y's [92,92] is unsatisfiable from 101.
- compose_try: level-0 candidates admitted by un_satisfy. X via
  the contract fallback (plen 5) walks the relation-blind path
  101,102,103,104,105 to endpoint 105 (wrong value); no level-1
  candidate continues from 105 to expected. Y via the fallback
  (plen 3) reaches 103; nothing continues to expected. DFS
  exhausts: COMP-FAIL.
- trial: the full s-to-expected path needs 5 links (plen 6) in
  A1 and 7 links (plen 8) in A2; the trial chain pass caps at
  plen 5.
- bootstrap_miss: miss path, no answer.
Result -2. Validated pre-freeze by the well-formedness prototype
(see disclosure below): exact pipeline gives -2 on the A1, A2,
A3, A10 shapes and 107 on the A4 shape.

## Kill bars (frozen)

- K1: A1 all assertions pass (selector chose TRUNCATE).
- K2: A2 all assertions pass (selector chose EXTEND).
- K3: A3 ans=-2 and zero adapted MAPs created.
- K4: A4 passes with zero type-16 edges (no regression; selector
  inert on exact-reuse worlds).
- K5: A5 ans=-2 and zero adapted MAPs (exact-reuse control
  provably fails the interface-arity mismatch task).
- K6: A6, A7, A8 all ans=-2 (causal dependence on X and Y;
  fresh learner fails).
- K7: A9 both queries ans=106, adapted count stable at 1.
- K8: A10 all assertions pass (both operations licensed;
  verifier selected the expected-consistent one; unused
  adaptation not composed).
- K9: 3/3 byte-identical runs for both binaries; sha256 recorded.
- K10: zero em/en dashes in all deliverables (byte-verified).
- K11: cc_base.zag sha256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  and composition_unified/un_patch.zag sha256
  3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2,
  both used verbatim via build concatenation, never modified.
- K12: 0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 semantic cases (selector uses only existing
  machinery: cc_relseq, cc_satisfy, t2_lu_first, t2_asm_chain,
  t2_try_verify, alloc_node, link_edge, promote_graph via the
  unchanged compose_try re-run; edge types 14, 15, 16 only).
- K13 NO-REBUILD: every adapted MAP has exactly one outgoing
  type-16 edge to a live native MAP; the source relseq is a
  strict prefix of the adapted relseq (EXTEND) or the adapted
  relseq is a strict prefix of the source relseq (TRUNCATE); and
  the adapted MAP's licensing fact ids are disjoint from the
  source MAP's training fact ids. Driver asserts per arm. A
  from-scratch rebuild cannot satisfy parentage + provenance +
  fact-disjointness + dedup simultaneously.

Verdict XP-SELECT-3-PASS iff K1-K13 all pass.

## Implementation plan (after prereg commit)

1. Write xs3_patch.zag (XS3-SELECT Phase 1 + ev_query_adapt with
   the unchanged compose_try re-run) and xs3_patch_noadapt.zag
   (one-line diff: adapt_on 1 -> 0); verify the diff is exactly
   one line.
2. Write xs3_driver.zag (arms A1-A4, A6-A10 + assertions) and
   xs3_driver_noadapt.zag (arm A5).
3. Build: cat composition_C/cc_base.zag
   composition_unified/un_patch.zag xs3_patch.zag xs3_driver.zag
   > xs3_full.zag; same with noadapt parts for
   xs3_full_noadapt.zag.
4. Compile with the pinned znc_linux_x86_64_abed8aa1; run 3x
   each; verify byte-identical; check kill bars.
5. Write REPORT.md. Commit with explicit pathspecs.

## Constraints

Unfrozen only (xdomain_select3/). Frozen read-only
(cc_base.zag, composition_unified/un_patch.zag). Pure Zag
(safebin PATH, no python). Zero em/en dashes. Nothing pushed.
No domain-pair-specific composition handler: the selector is
anchored only at the query start and reads candidates from
source relseqs and the fact store. No paired X->Y training
examples. No finite operator menu widening: the arity family
{TRUNCATE, EXTEND} is new, and this worker adds only the
evidence-driven selector. Phase 2 is the unchanged compose_try
re-run (L2-ADAPT precedent), not new completion code.

## Battery well-formedness (disclosed pre-freeze work)

Before freezing, a throwaway prototype ran in
~/workspace/_scratch_xs3 (outside the repo, never committed,
deleted after; /tmp was full): (1) the exact pipeline
(cc_base.zag + un_patch.zag, ev_query) on all five Z fact sets,
confirming ans=-2 for the A1/A2/A3/A10 shapes and ans=107 for
the A4 shape, with X=[91]x4 and Y=[92]x2 training intact;
(2) the walk primitives (t2_lu_first prefix walks, the frontier
fact lookup, cc_satisfy Y-license checks from 104/106/108),
confirming a 3-hop walk 101->104, a 4-hop walk 101->105 plus
frontier fact to 106, and Y licensing from each adapted
endpoint. These validated only that the arms are well-formed
against the shared machinery, not experimental outcomes. No
selector/orchestration code was prototyped. The frozen bars were
not adjusted to fit any outcome.
