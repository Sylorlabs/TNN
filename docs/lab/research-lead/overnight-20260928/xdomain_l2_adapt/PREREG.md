# PREREG: Cross-Domain L2 Adaptive Reuse (arithmetic to planning, renamed interface)

Frozen 2026-10-02. Committed alone before implementation.
Worker: XDomain L2 Adapt Worker. Branch: tnn-native-lab, local only,
nothing pushed.

## Objective

Demonstrate genuine L2 ADAPTIVE REUSE across domains with a real
interface mismatch. X (SUM over price facts, arithmetic domain) and Y
(ALLOC budget procedure, planning domain) are learned independently.
The Z world renames Y's allocation relation (82 -> 83, the Z planning
dialect's "disburse"). X transfers exactly; Y's trained interface no
longer matches. Exact composition provably fails. The learner must
REBIND Y's interface to the renamed relation, licensed by real Z
facts and execution-verified, without any domain-pair-specific
handler, without paired training examples, and without widening any
finite operator menu.

This is REBIND-family adaptation (one of the four mandated forms:
rebind, extend, truncate, specialize). The prior EXTEND-ONE worker
covered the extend family; this worker covers the rebind family for a
cross-domain pair, which is the composition reset's L2 top priority.

## Operator specification (frozen)

Name: adapt_relabel, the REBIND-RELABEL operator.

Trigger: fires exactly once per query, only after the standard
pipeline (activate, rebind_try, compose_try with compose_on) has
failed. It never fires when composition succeeds, so L1 exact-reuse
behavior is unreachable by it. adapt_on() gates the bracket; the
no-adapt control build differs by exactly one line (adapt_on 1 -> 0).

For each candidate first segment m1 satisfiable from the query start
s (enumerated by the unchanged cc_candidates, same ordering as the
DFS level 0), in order:

1. Satisfy m1 from s with cc_satisfy; let v1 be the endpoint value.
2. Read the frontier relation set F = distinct relations on live,
   non-superseded facts with subject v1 (learner state only; no
   relation is named in code).
3. For each live native MAP m2 (tag 20, no outgoing type-16 edge,
   m2 != m1), in node-id order: read its relation sequence R (length
   L, 1 <= L < 7) with cc_relseq (pure structural read).
4. For each distinct relation symbol d occurring in R, and each
   frontier relation f in F: build R' = R with every occurrence of d
   replaced by f (consistent single-symbol substitution; frozen
   scope, no multi-symbol substitution). Emit a RELABEL-TRY trace
   line naming m2, d -> f, and v1.
5. Dedup: skip R' if any live MAP already carries exactly R'.
6. Satisfiability license: R' must be fully satisfiable from v1 in
   the fact store (rl_satisfy_seq). Otherwise skip; no hallucinated
   interface.
7. Execution check: assemble the chain with t2_asm_chain and verify
   with t2_try_verify against its own terminal; a graph that does not
   execute to its terminal is never promoted.
8. Promote with rl_promote (MAP node layout identical to
   promote_graph but teaching NO fact: mid-query scaffolding is not a
   verified query answer, per the EXTEND-ONE invariant). Write a
   type-16 LINK from the adapted MAP to m2 ("adapted-from"). Type 16
   is free: base uses edge types 1-13, unified patch uses 14 and 15.
   Emit ADAPT-MK with the adapted id, source id, and length.

After the pass, if at least one adapted MAP was created, re-run the
UNCHANGED compose_try once over the augmented candidate set. The
final answer is verified against `expected` by t2_try_verify exactly
as before; a wrong relabeling cannot produce a false positive.

Generality (frozen claim): the operator names no relation, no MAP, no
length, and no query. Substitution candidates come from the fact
store at each reached frontier. Arm A2 (rename to a different
relation, 84 instead of 83) is the empirical proof that no target
relation is hardcoded.

Adapted marking (frozen): a MAP is ADAPTED iff it has an outgoing
type-16 edge; NATIVE MAPs have none. On success MAP_Z carries LINK14
to the adapted segment (and to MAP_X), never to native MAP_Y.
Provenance distinguishes adapted from native exactly as in the
EXTEND-ONE worker.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X
(ev_teach (201,81,231),(231,81,261),(261,81,291); ev_query
(201,91,291) -> MAP_X relseq [81,81,81]) and Y (ev_teach
(301,82,311),(311,82,321); ev_query (301,92,321) -> MAP_Y relseq
[82,82]), then 30 distractor teaches (subjects 5000+, relations
60-69), then Z facts, then exactly one query via ev_query_adapt (the
unified pipeline plus the relabel bracket; un_patch.zag used
verbatim).

- A1 L2-TREAT: Z facts (101,81,102),(102,81,103),(103,81,104),
  (104,83,105),(105,83,106). Query (101,70,106). Expect: ans=106;
  there exists an adapted MAP a with type-16 edge a->MAP_Y and relseq
  [83,83]; MAP_Z has LINK14 to a and to MAP_X; MAP_Z has no LINK14 to
  MAP_Y; exactly one adapted MAP created; trace shows RELABEL-TRY
  m2=MAP_Y 82->83 at v1=104.
- A2 L2-XDIALECT (different rename target): Z facts as A1 but with
  84 in place of 83: (104,84,105),(105,84,106). Query (101,70,106).
  Expect: ans=106; adapted MAP a with type-16 edge a->MAP_Y and
  relseq [84,84]; MAP_Z LINK14 to a and to MAP_X, none to MAP_Y.
- A3 L2-IMPOSSIBLE: Z facts (101,81,102),(102,81,103),(103,81,104)
  [dead end: 104 has no outgoing fact]. Query (101,70,106). Expect:
  ans=-2; zero type-16 edges workspace-wide (relabel fired, frontier
  relation set empty, created nothing; clean reject).
- A4 L1-REGRESSION: rename-free world: Z facts (101,81,102),
  (102,81,103),(103,81,104),(104,82,105),(105,82,106). Query
  (101,70,106) via ev_query_adapt. Expect: ans=106; zero type-16
  edges (operator never fires; exact composition succeeds);
  MAP_Z LINK14 to MAP_X and to MAP_Y.
- A5 NO-ADAPT CONTROL: A1 setup verbatim, run under the one-line
  no-adapt build (adapt_on()=0). Expect: ans=-2 and zero adapted
  MAPs. This proves the adaptation operator did the work: the exact
  pipeline (activate, rebind, compose, trial, bootstrap) cannot solve
  the mismatch task.
- A6 ABL-X: A1 setup, MAP_X killed before the Z query. Expect
  ans=-2 (Z causally depends on X; no first segment, no relabel).
- A7 ABL-Y: A1 setup, MAP_Y killed before the Z query. Expect
  ans=-2 (Z causally depends on Y; nothing to rebind).
- A8 FRESH: no X/Y training (distractors + A1 Z facts only). Query
  (101,70,106). Expect ans=-2 (fresh learner fails outright).
- A9 REUSE: A1 setup, query (101,70,106) twice. Expect: both
  ans=106; adapted MAP count stays 1 after the second query (Z
  persists via its taught fact; no spurious re-adaptation).

## Kill bars (frozen)

- K1: A1 all assertions pass.
- K2: A2 all assertions pass (no hardcoded rename target).
- K3: A3 ans=-2 and zero adapted MAPs created.
- K4: A4 passes with zero type-16 edges (no regression; operator
  inert on exact-reuse worlds).
- K5: A5 ans=-2 and zero adapted MAPs (exact-reuse control provably
  fails the mismatch task).
- K6: A6, A7, A8 all ans=-2 (causal dependence on X and Y; fresh
  learner fails).
- K7: A9 both queries ans=106, adapted count stable at 1.
- K8: 3/3 byte-identical runs for both binaries; sha256 recorded.
- K9: zero em/en dashes in all deliverables (byte-verified).
- K10: un_patch.zag sha256-identical to
  composition_unified/un_patch.zag
  (3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2);
  cc_base.zag never modified (read-only; used only via build
  concatenation).
- K11: 0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges, 0
  handlers, 0 semantic cases (operator uses only existing
  machinery: cc_relseq, cc_satisfy, cc_candidates, t2_lu_first,
  t2_asm_chain, t2_try_verify, alloc_node, link_edge; edge types 14
  and 16 only).

Verdict XDOMAIN-L2-ADAPT-PASS iff K1-K11 all pass.

## Implementation plan (after prereg commit)

1. cp ../composition_unified/un_patch.zag . ; sha256-verify.
2. Write relabel_patch.zag (operator + ev_query_adapt). No changes to
   the base or to un_patch. relabel_patch_noadapt.zag is a one-line
   diff (adapt_on 1 -> 0); verify the diff is exactly one line.
3. Write xd_driver.zag (arms A1-A4, A6-A9) and xd_driver_noadapt.zag
   (arm A5).
4. Build: cat ../composition_C/cc_base.zag un_patch.zag
   relabel_patch.zag xd_driver.zag > xd_full.zag; same with noadapt
   parts for xd_full_noadapt.zag.
5. Compile with pinned znc_linux_x86_64_abed8aa1; run 3x each;
   verify byte-identical; check kill bars.
6. Write REPORT.md. Commit with explicit pathspecs.

## Constraints

Unfrozen only (xdomain_l2_adapt/). Frozen read-only (cc_base.zag,
composition_unified/un_patch.zag). Pure Zag (safebin PATH, no
python). Zero em/en dashes. Paper untouched. Nothing pushed. No
domain-pair-specific composition handler: the operator is anchored
only at reached frontiers and reads substitution candidates from the
fact store. No paired training examples. No finite operator menu
widening: single consistent-symbol substitution, frozen scope.
