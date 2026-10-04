# PREREG: Composition L2 Adaptation Operator (EXTEND-ONE)

Frozen 2026-10-02. Committed alone before implementation.
Worker: L2 Adaptation Operator Worker. Branch: tnn-native-lab, local
only, nothing pushed.

## Objective

Build a genuine L2 adaptation operator for composition: EXTEND-ONE.
Given a MAP whose relation sequence fully covers a prefix of what a
query needs but falls one link short, the learner EXTENDS the MAP by
one link (licensed by a real fact at the frontier) instead of the DFS
rejecting it. This closes the L2 adaptation gap documented in
COMPOSITION-LEVELS-COMPLETE (L2 FAIL: "no extension operator; clean
decline on extension demand"), without touching L3 (no invention
claim is made or tested here).

## Operator specification (frozen)

Name: adapt_extend, the EXTEND-ONE operator.

Trigger: fires exactly once per query, only after the standard
pipeline (activate, rebind_try, compose_try) has failed. It never
fires when composition succeeds, so L1 exact-reuse behavior is
unreachable by it.

For each live native MAP m (tag 20, live, no outgoing type-16 edge),
in node-id order:

1. Read its relation sequence R (length L) with cc_relseq (pure
   structural read, no semantics).
2. Satisfy the FULL sequence from the query start s with cc_satisfy.
   If unsatisfiable, skip m. Partial-prefix extension is out of scope;
   it belongs to the T4 decomposable-MAP frontier, not this operator.
3. Let v_L be the frontier value. Scan the fact store for every live
   non-superseded fact (v_L, r_new, v_next), any relation, in
   node-id order.
4. Candidate extended sequence R' = R ++ [r_new]. Dedup: skip if any
   live MAP already carries exactly R'.
5. Assemble the extended guard/set chain from the L+1 values and L+1
   licensing facts with t2_asm_chain.
6. Execution check: t2_try_verify(root, s, v_next) must succeed; a
   graph that does not execute to its own terminal is never promoted.
7. Promote with promote_graph(root, s, r_src, v_next, facts, L+1),
   where r_src is the source MAP's own training relation (field 4).
   Write a type-16 LINK from the adapted MAP to the source MAP
   ("adapted-from"). Type 16 is unused by the base (types 1-13) and
   the unified patch (14 provenance, 15 co-use).

After the pass, if at least one adapted MAP was created, re-run the
UNCHANGED compose_try (verified DFS) once over the augmented
candidate set. The final answer is verified against `expected` by
t2_try_verify exactly as before; a wrong extension cannot produce a
false positive.

Generality (frozen claim): the operator names no relation, no MAP, no
length, and no query. The extension relation is read from the fact
store at the frontier. Arm A2 (cross-relation extension) is the
empirical proof that it is not a hardcoded "add r1" rule.

Adapted marking (frozen): a MAP is ADAPTED iff it has an outgoing
type-16 edge; NATIVE MAPs have none. On success MAP_Z carries LINK14
to the adapted segment (and to the other native segment), never
directly to the native source of the adapted segment. Provenance
distinguishes adapted from native.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X
([1,1,1]: ev_teach (11,1,12),(12,1,13),(13,1,14), query (11,71,14))
and Y ([2,2,2]: ev_teach (21,2,22),(22,2,23),(23,2,24), query
(21,72,24)), then 30 distractor teaches (subjects 5000+, relations
60-69), then Z facts, then exactly one query via ev_query_adapt (the
unified pipeline plus the adapt bracket; un_patch.zag used verbatim).

Note on expectations: the task brief says "ans=107 or appropriate".
The frozen amended L2 battery queries (101,70,108), so the
appropriate expectation is ans=108. L1 arms reuse the amended levels
battery verbatim (query (101,70,107), ans=107).

- A1 L2-TREAT: Z facts (101,1,102),(102,1,103),(103,1,104),
  (104,1,105),(105,2,106),(106,2,107),(107,2,108). Query
  (101,70,108). Expect: ans=108; COMP-SEGS n=2; there exists an
  adapted MAP a with type-16 edge a->MAP_X; MAP_Z has LINK14 to a;
  MAP_Z has LINK14 to MAP_Y; MAP_Z has no LINK14 to MAP_X; a has
  relseq [1,1,1,1].
- A2 L2-XREL (cross-relation): Z facts (101,1,102),(102,1,103),
  (103,1,104),(104,2,105),(105,2,106),(106,2,107),(107,2,108).
  Query (101,70,108). Expect: ans=108; adapted MAP a with type-16
  edge a->MAP_X and relseq [1,1,1,2]; MAP_Z LINK14 to a and to
  MAP_Y.
- A3 L2-IMPOSSIBLE: Z facts (101,1,102),(102,1,103),(103,1,104)
  [dead end: 104 has no outgoing fact],(105,2,106),(106,2,107),
  (107,2,108). Query (101,70,108). Expect: ans=-2; zero type-16
  edges workspace-wide (adapt fired, found no frontier fact,
  created nothing; clean reject, no hallucinated extension).
- A4 L1-REGRESSION: the six amended L1 arms verbatim (TREAT ans=107
  n=2; ABL-X -2; ABL-Y -2; FRESH -2; REUSE 107; PROV LINK14
  MAP_Z->MAP_X and MAP_Z->MAP_Y), all via ev_query_adapt.

## Kill bars (frozen)

- K1: A1 all assertions pass.
- K2: A2 all assertions pass (relation-agnostic extension proven).
- K3: A3 ans=-2 and zero adapted MAPs created.
- K4: A4 all six L1 arms pass (no regression from the adapt bracket).
- K5: 3/3 byte-identical runs; sha256 recorded.
- K6: zero em/en dashes in all deliverables (byte-verified).
- K7: un_patch.zag sha256-identical to
  composition_unified/un_patch.zag
  (3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2);
  cc_base.zag never modified (read-only; used only via build
  concatenation).

Verdict COMPOSITION-ADAPT-COMPLETE iff K1-K7 all pass.

## Implementation plan (after prereg commit)

1. cp ../composition_levels/un_patch.zag . ; sha256-verify against
   ../composition_unified/un_patch.zag.
2. Write adapt_patch.zag (operator + ev_query_adapt). No changes to
   the base or to un_patch.
3. Write ad_driver.zag (arms A1-A4).
4. Build: cat ../composition_C/cc_base.zag un_patch.zag
   adapt_patch.zag ad_driver.zag > ad_full.zag.
5. Compile with pinned znc_linux_x86_64_abed8aa1; run 3x; verify
   byte-identical; check kill bars.
6. Write NAMECHECK.md (Step 0 guard, commit-order self-check, build
   records) and REPORT.md. Commit with explicit pathspecs.

## Constraints

Unfrozen only (composition_adapt/). Frozen read-only (cc_base.zag,
composition_unified/, composition_levels/ sources). Pure Zag
(safebin PATH, no python). Zero em/en dashes. Paper untouched.
Nothing pushed. 0 modes, 0 bridges, 0 handlers, 0 new semantic
cases. No COMPOSE_MODE or similar.
