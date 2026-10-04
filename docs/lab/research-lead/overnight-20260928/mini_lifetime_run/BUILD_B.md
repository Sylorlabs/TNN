# Build B: Reuse-Path Variant

**Status:** BUILT. Acceptance gate PASSED. Hash-recorded pre-freeze.
**Date:** 2026-10-01. **Builder:** Mini-Lifetime Builder.

## Source

- Base: `ml_base.zag`, verbatim frozen TNN-2 (f4de7ff46), SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
- Build B: `ml_buildb.zag`, SHA-256
  `73b9b61ce5e16f140d1fb9659749d6321e98d176752407b57270e9b5c92c5d69`.
- Binary: `ml_buildb_bin`, SHA-256
  `228725e57fe78272fc5ca31d0f79245c778812ca67c6655621a10f8ff149034e`.
- Diff: 107 lines changed. Hashes in `BUILD_B_HASHES.txt`.

## The 5 minimal items (from REUSE_PATH_DESIGN.md Section 6.1)

1. **MAP-lookup branch in `ev_query` before `activate`.** New `map_lookup`
   function scans live tag-20 MAPs for field8==s, field4==r,
   is_superseded==0. On hit, `t2_exec(W, ng(W,m,20), s)`; if not
   -999999, same bookkeeping as activate branch (link_edge type 6,
   ref_prot, log_ev with MAP as source) and return. On -999999,
   fall through to activate.
2. **Shadow teach deleted.** `ev_teach_in(W,s,r,ans)` removed from
   `promote_graph`. The MAP is the promoted artifact.
3. **Liveness.** MAPs get a type-9 self-edge in `promote_graph`, so
   the `decay` sweep applies to them like facts. `is_superseded`
   filter in `map_lookup`. Live-MAP-wins via MAP-first ordering.
4. **Contradiction retargeted at MAP.** `ev_observe` checks
   `map_lookup` first: match confirms, mismatch supersedes the MAP
   (type-3 self-edge) and teaches the observation as fact.
   `t2_revise_graph`: fact-contradiction loop and `ev_teach_in`
   deleted; `ns(W,m,28,out)` kept; acceptance criterion UNCHANGED
   (out != -999999). `revise_on_contradict` now returns i32: on
   revision failure (0), the MAP is superseded via type-3 self-edge
   (honest failure mode); on success (1), `ev_observe` skips the
   shadow fact teach.
5. **MAP selection.** `map_lookup` selects the most-recent live MAP
   by field24. The selection call site is documented as the
   target-selection integration seam.

`t2_revise_graph` is otherwise UNCHANGED, including its acceptance
criterion.

## Acceptance gate

Micro-world: 2-hop chain (1,1,11), (11,1,12); query (1,50) expects 12.
Relation 50 has no direct facts, forcing trial and promotion.

- K-REUSE-1 (query-time MAP execution): PASS. After promotion,
  re-query returns 12 with zero facts present for (1,50); the answer
  can only come from MAP execution via the map_lookup branch.
- K-REUSE-2 (no shadow facts): PASS. Zero tag-1 facts for (1,50)
  after promotion and re-query.

Runs: 3/3 byte-identical, SHA-256
`6a42ba256524101f2694531307ac677f9beee80ca4187474e3a58f8e24a8937c`.
Transcripts: `accept_run1.txt`, `accept_run2.txt`, `accept_run3.txt`.
Driver: `ml_accept.zag` (diagnostic output kept for white-box evidence).

## Corruption-detector layout check

Tag-20 MAP layout unchanged by Build B, verified by inspection:

- `promote_graph`: `ns(W,m,0,20)`, `ns(W,m,4,r)`, `ns(W,m,8,s)`,
  `write_node(W,m,root,hg(W,24),ans,0)` gives field20=root,
  field24=promo index, field28=answer. Unchanged.
- `map_lookup`: reads tag 20, field8 (s), field4 (r), field24
  (promo). Consistent.
- `t2_revise_graph`: reads field20/field8/field4/field28, writes
  field28. Unchanged.
- Added: type-9 self-edge on MAP (decay participation). This is a
  new edge type on the MAP node, not a layout change; the detector's
  tag-20 classification is unaffected.

## Standing metrics (Build B)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the 5 reuse-path items.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (build only; counted at run).
- SOURCE-ENUMERABLE FORMS: 0 new (MAP layout reused as-is).
- SUF DECISIONS: MAP scan order (node id), most-recent tie-break.
- LEARNER-INTERNAL CRITERIA: 0.
- COGNITION LINES: ~60 added (map_lookup, ev_query branch,
  promote_graph edits, ev_observe edits, revise_on_contradict edits).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
