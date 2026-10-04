# PREREG H2R: learner-authored inversion on the construction-service substrate

Lane: H2R, wave wave-20261001-2321pdt. Status: FROZEN by this commit.
This prereg is committed alone, before any implementation. Kill bars do not
move after this freeze. Documentation rule observed: no em-dashes.

## 1. Lineage

- TNN3H2 PREREG_H2.md (wave-20261001-2021pdt): SUBSTRATE-ABSENT, never
  frozen. Finding, section 2: the frozen TNN-2 had no learner-reachable
  construction path (link_edge direction-neutral; the assemblers were the
  only graph construction, forward-only by schema; deletion would remove the
  only construction). No bars were frozen.
- TNN3-SUBSTRATE (this wave): DESIGN-COMPLETE. A 197-line generic
  construction-service package (prereg be112b78f, prototype a11dde4b9) plus
  contradiction trigger plus learner-writable standing, with frozen kill
  bars KB-H2R/H4R/H6R/H7R in its section 8. Adoption into the TNN-2 lineage
  is Micah's pending governance decision; this re-attempt runs against the
  prototype (the adoption candidate), not the frozen tnn2.zag.
- This document: the H2 re-attempt (H2R). It does not amend, re-score, or
  rehabilitate the 2021pdt finding, which stands as a negative result.

## 2. Hypothesis H2R (fresh, for this substrate)

On the construction-service substrate, a generic learner-side trial process
with no inverse schema and no hardcoded nonzero slot authors BUILD tickets
from experienced fact paths. On sealed worlds whose queries require
inverse-direction derivations, the trial discovers the inverse orientation
by execution feedback, builds the tickets through the generic service, and
answers hidden queries by executing the built graphs on the frozen ISA.

Inversion, frozen meaning for this prereg: a derivation graph in which a
BRANCHEQ (tag 102) cell guards slot 1, a slot the researcher-written
assemblers never guard (they guard only slot 0), while SET (tag 101) cells
write slot 0. This is the substrate V1's inversion shape; the H2R claim is
that the learner trial authors it from experience, where V1's dev check
hand-authored it as an explicitly labeled stand-in.

What H2R does NOT claim: it does not claim the learner invented the ticket
format or the construction service (those are the substrate's); it does not
claim forward diagnostic queries (out of scope; the frozen trial owns that
direction); it does not claim a continuing learner (fresh workspace per
query, section 6); it does not claim the orientation space itself is
learner-invented (the space {guard slot 0, guard slot 1} is
researcher-defined generic machinery; the selection within it is the
learner's, by trial).

## 3. Substrate re-verification (G1, completed before this freeze)

Per KB general precondition G1, this worker re-verified the package against
the committed prototype source (a11dde4b9) before freezing:

- PKG block: lines 1594-1790 of substrate_proto.zag, 197 lines, byte-identical
  to pkg_extract.zag from the same commit (mechanical extraction, no retyping).
- Hooks (committed-source grep): lb_run(W) at all three ev_observe tails
  (lines 843, 856, 858, marked SUBSTRATE-HOOK A); lt_fire(W,n,nn) plus
  ls_bump(W,n,-1) in the contradiction branch (line 855, HOOK B C2);
  ls_bump(W,n,1) in the confirm branch (line 842, HOOK C1); lbid(W,.) at the
  four cognition-path call sites (lines 145, 259, 874, 886; 874/886 marked
  HOOK C3). Zero protected-core changes: execute(), the 4-op ISA tags
  101-104, alloc_node, link_edge, ng/ns/eg/es all byte-identical to the
  frozen tnn2.zag regions.
- White-box run: the extracted prototype source compiled with the pinned znc
  (binary 260821 bytes, same size as the lane binary) and run: R0 46/46
  frozen self-tests pass; V1-PASS (guard-slot-1 ticket builds, cell0 tag 102
  field4 1001, executes true-branch and fail-closed); V2-PASS; V3-PASS;
  SUBSTRATE-VERIFY ALL-PASS. Log kept at /tmp/h2r_g1 during verification;
  the rerun is reproduced in the implementation commit's build log.

G1 verdict: the package is present as specified on the exact bits H2R builds
on. The construction service can express the inversion the hypothesis needs
(V1 proves guard slot 1 plus back-reference true-targets build and execute),
so the re-attempt proceeds; SUBSTRATE-INSUFFICIENT is not triggered.

## 4. The H2R learner: h2_trial (frozen spec)

h2_trial is learner-side cognition code (appended to a verbatim copy of the
prototype; the PKG block and hooks are not modified). It is the re-attempt's
miss policy, standing in for the ev_query wiring the substrate deferred.
Signature: h2_trial(W, s_q, expected, fr) -> i32 answer or -2.

### 4.1 Reverse gather (h2_rgather)

Generic reverse-direction BFS over type-1 fact nodes, mirroring t2_gather's
structure with the traversal direction reversed:

- Start: one path (len 1, v0 = s_q).
- Extend: for the path head's last value lastv, scan nodes n = 2..1023; for
  each live tag-1 node with field28 == lastv (lastv as object) and
  field24 != -999 (the existing t2_gather exclusion, inherited not new),
  extend the path with field20 (the subject). Skip extensions that repeat a
  value already in the path (cycle guard).
- Bounds: path length at most 5, at most 96 paths. Deterministic order: node
  scan order, BFS layers.

No domain content: no condition on relation values (other than the inherited
-999 exclusion), node values, or query identity.

### 4.2 Ticket authoring (h2_author)

For one path (vals[0..n-1], n >= 2) and one guard orientation g in {0,1}:

- t = lb_ticket_new(W, ctx, -41), ctx = 9000 + a per-candidate sequence
  number (opaque label only).
- step0 = lb_step_add(W, t, 102, 1000+g, vals[0], -2): BRANCHEQ cell, guard
  operand = frame-slot code for slot g, literal = vals[0] (the given), true
  target = back-reference -2 (the first built cell after this one, i.e. the
  step1 cell; the V1 convention).
- step_j (1 <= j <= n-1) = lb_step_add(W, t, 101, 1000, vals[j], 0): SET
  cell writing slot 0 (the protocol answer slot; each overwrites the last,
  so no scratch slot is hardcoded anywhere).
- Return t, or -1 on allocation failure.

The literal 1001 never appears in this worker's source: the guard slot code
is always the computed value 1000+g with g the trial loop variable. The
literal 1000 is the ISA frame-slot base (res_op interprets op >= 1000 as a
frame slot), generic machinery. No inverse-direction schema exists: the code
expresses "try guard slot g" for g in {0,1}, never "guard slot 1".

### 4.3 Trial loop

- Order candidates by descending path length (longer derivations first, the
  t2_trial convention), ties in BFS order; for each path, g = 0 then g = 1.
- For each (path, g): author the ticket; lb_run(W) (the package service
  entry); if the ticket is not built (field28 != 1) count rejected and
  continue; reset the frame (slot0 = 0, slot1 = s_q, slot2 = 0); execute the
  built root; tried++.
- Verify (post-hoc feedback only, the frozen E-ruling): accept iff
  execute returns 1 and fr_get(fr,0) == expected and the answer is neither
  -2 nor -999999. On accept, record the verifying ticket id driver-side and
  return the answer.
- Record trial stats exactly as t2_trial does: hs(W,16,tried*1024+rejected).
  TRIAL_ENTERED for the query = tried.
- Return -2 if nothing verifies.

`expected` is read only in the verify comparison. The authoring code
(h2_author) and the gather (h2_rgather) never read `expected`; the K-C0A
audit (section 7) verifies this textually.

### 4.4 Observation protocol (frozen apparatus, not learner cognition)

Hidden queries are posed to h2_trial with the frame pre-loaded: slot1 =
the given value s_q (the environment's observation slot), slot0 = 0,
slot2 = 0; the answer is read from slot0 after execution. This frame
convention is experimental apparatus frozen here, like ev_query's own
interface; it does not encode the derivation. The learner still has to
discover that guarding slot 1 (not slot 0) is what verifies, author the
right literals in the right order with the right back-reference, and select
the verifying candidate among distractors.

## 5. Sealed worlds (schema frozen here; values generated post-freeze)

### 5.1 Families (materially different structures)

- Family A (2-hop causal chains): per rule i, values k_i (cause), m_i
  (mid), a_i (effect), all distinct within the world. Facts, taught in this
  order via ev_observe: (k_i,R,m_i), (m_i,R,a_i). Query i: given a_i,
  expected k_i (effect-to-cause, the inverse diagnostic).
- Family B (3-hop chains): values k_i, m1_i, m2_i, a_i distinct. Facts:
  (k_i,R,m1_i), (m1_i,R,m2_i), (m2_i,R,a_i). Query i: given a_i,
  expected k_i. Tests multi-step tickets and back-reference wiring.
- Family C (2-hop plus distractor chain): family A facts plus, per rule i,
  distractor values d_i, e_i (distinct from all rule values and each other)
  with facts (d_i,R,a_i), (e_i,R,d_i) taught after the rule facts. The
  reverse gather then finds two length-3 paths from a_i; only the true one
  verifies. Tests trial selection among competing candidates.

Counts: 3 worlds per family, 4 rules per world: 9 worlds, 36 hidden queries.

### 5.2 Value and relation scheme

Rule/distractor values: integers 1..999 (the ticket literal spec range),
pairwise distinct within a world, drawn by the frozen generator (section
5.3). Relation R per world: 701 + world_index (701..709); never -999.
Query relation R_q = R + 5000 (no facts are ever taught with R_q).

### 5.3 Generator (frozen algorithm; seed chosen post-freeze)

gen_worlds.zag (pure Zag): LCG state = (state*1103515245 + 12345) &
0x7fffffff; draw(lo,hi) = lo + next() % (hi-lo+1); values drawn with
rejection sampling for within-world distinctness, in a fixed order (family
A worlds, then B, then C; within a world, rules 1..4; within a rule,
k, m, a then distractors d, e). The seed is chosen after this freeze and
recorded in the sealed-worlds commit; one seed, one generation (if the seed
is ever changed, the reason is recorded and the earlier generation kept).

The generator emits worlds_sealed.zag: per world, a fact-teaching function
(explicit ev_observe calls in the frozen order) and a query-accessor
function (per query: given, expected). The eval driver includes this file;
the H2R learner implementation never sees it at authoring time (commit
order, section 8).

### 5.4 No direct-query facts (argument, frozen)

A hidden query (given a_i, expected k_i) is not directly answered by any
fact: no fact has subject a_i at all (a_i appears only as an object), so
activate(a_i, R_q) misses; no fact is (a_i, *, k_i); no forward fact path
from a_i reaches k_i (the only paths touching a_i end at a_i). The
derivation is licensed only by the reverse chain a_i <- m_i <- k_i, which
no forward-only construction can traverse. The frozen baseline (section 7,
B4) measures this: ev_query(a_i, R_q, k_i, 0) must miss.

### 5.5 Practice worlds

During implementation the worker may use tiny hand-made practice worlds for
debugging, clearly labeled PRACTICE in the implementation commit. Practice
worlds are never scored and never enter the sealed eval.

## 6. Eval procedure (frozen)

Per hidden query, in order:
1. Fresh workspace W (z_alloc(110656)); tnn2_init(W).
2. Teach the world's facts via ev_observe in the generated order.
3. Allocate frame fr (tag 902 node); load slot1 = given, slot0 = slot2 = 0.
4. ans = h2_trial(W, given, expected, fr). TRIAL_ENTERED = hg(W,16)/1024.
5. correct = (ans == expected). Emit one line per query.

Fresh workspace per query: no cross-query transfer is claimed or measured.

## 7. Kill bars (frozen)

KB-H2R, adopted verbatim from SUBSTRATE_PREREG.md section 8 (unweakened):

- B1 substrate: this prototype's V1 re-run on the adopted build (ticket with
  guard slot != 0 builds; cell field4 equals ticket spec; executes
  correctly). Operationalized: the eval driver calls the prototype's dv_v1()
  and requires return 1. (Adoption is pending; "the adopted build" here is
  the prototype a11dde4b9, the adoption candidate.)
- B2 sealed: on the section-5 worlds, at least 80 percent of the 36 hidden
  queries answered correctly via ticket-built graphs executed by the frozen
  ISA. Operationalized: score >= 29/36.
- B3 source novelty: grep of the adopted source shows no constructor or
  assembler with a hardcoded slot != 0 and no inverse-direction schema;
  inverse content appears only in tickets. Operationalized audit on
  h2r_impl.zag (the H2R learner): (i) grep for the literals 1001 and 1002
  prints nothing; (ii) the only guard-slot expression is 1000+g with g the
  trial loop variable; (iii) white-box dump of a verifying ticket shows
  field4 = 1001 while the source contains no such literal; (iv) manual
  review finds no inverse-direction schema. Scope note: the substrate's own
  dev check dv_v1 hand-authors a 1001 ticket as an explicitly labeled
  stand-in (SUBSTRATE_PREREG.md section 5); it is substrate verification
  scaffolding, not the H2R learner, and is outside this audit's scope.
- B4 ablation: tombstoning the ticket-built cells destroys the sealed
  advantage (falls to at most the no-construction baseline).
  Operationalized: after each correct query, h2_tombstone walks the
  verifying ticket's built graph from its root (BRANCHEQ true-target via
  field12, other cells via SEQ; asserts walked count equals ticket step
  count) and sets every cell tag to 0; re-executing the dead root on the
  query frame must fail for every query (ablated score S_ablated expected
  0/36, measured not assumed). Baseline: fresh workspace per query, same
  experience, ev_query(given, R_q, expected, 0) (the frozen path, no tickets
  authored): score S_base (measured). Require S_ablated <= S_base: the bar
  kills if tombstoning leaves any advantage above baseline, i.e. if the
  sealed score did not come from the ticket-built cells.
- KILL: B2 below 80 percent, or B3 fails (inverse schema found in source).

Additional frozen bars for this re-attempt:

- G-TRIAL (anti-triviality gate): TRIAL_ENTERED > 0 on every sealed query.
  Any sealed query with TRIAL_ENTERED == 0 VOIDs the sealed run (the run is
  preserved as a negative finding, investigated, and re-run as a fresh
  eval; it is not scored).
- G-DET: the sealed eval binary is run 3 times; stdout must be
  byte-identical across all 3 runs (hashes recorded).
- K-C0A (zero new semantic cases): audit of h2r_impl.zag: (i) list every
  numeric literal and justify it as structural (tags 101-104, bounds,
  status codes, the ISA frame-slot base 1000) rather than domain content;
  (ii) grep confirms none of the sealed world values or relation ids
  appears in h2r_impl.zag (holds by commit order, verified textually);
  (iii) grep confirms `expected` is read only in h2_trial's verify
  comparison, never in h2_author or h2_rgather; (iv) the inherited -999
  relation exclusion in h2_rgather is labeled as inherited from t2_gather,
  not new. Any unjustified domain-conditional branch fails K-C0A.

## 8. Commit order and anti-contamination (frozen)

1. This prereg, committed alone (this commit).
2. Implementation: h2r_impl.zag (h2_rgather, h2_author, h2_trial,
   h2_tombstone, driver), gen_worlds.zag, build script; tested on practice
   worlds only. Committed before any sealed value exists.
3. Sealed worlds: run gen_worlds with the post-freeze seed; commit
   worlds_sealed.zag and the seed.
4. Sealed eval: build the full harness, run 3x, run B4 and the audits;
   commit results and JUDGE_BRIEF.md.

Because the implementation commit strictly precedes the sealed values, the
learner code cannot contain them; the K-C0A grep verifies this. The solo
worker stands in for the independent adversary (KB precondition G2) via:
schema frozen before values exist, PRNG-determined values, implementation
predating values, textual novelty audits, and the B4 causal ablation.

## 9. Amendment rule

If any bar proves unexecutable as written, this worker amends transparently
and re-freezes; bars are never moved silently to force a pass. A VOID
verdict is terminal for the voided run: correction proceeds as a fresh
prereg plus fresh sealed worlds, never salvage.
