# Revision Substrate Experiment: Copy-and-Commit + MAP Retargeting

**Verdict: REVISION-SUBSTRATE-COMPLETE.**
**Status:** UNFROZEN VARIANT ONLY. Correctness experiment, not a capability claim.
**Date:** 2026-10-01 (UTC).

## 1. What was tested

Per Micah's 2026-10-01 approval: copy-and-commit + MAP retargeting as a
correctness architecture experiment. No in-place mutation/revert. Candidate
repairs are built in fresh cells, verified, then atomically committed. This
prevents the demonstrated allocator-alias corruption (bug `8b58c4104`).

This is correctness infrastructure. It does NOT make repair form
learner-authored. It does NOT establish SUF. It does NOT establish L3.

## 2. Implementation (unfrozen variant)

Base: `reuse_experiment/tnn2_reuse_variant.zag`
(SHA-256 `0bd8156fb249f07778fbe6929f1e46ea0fe085448e25cd7d4826493df0f321d8`).
Variant: `tnn2_revision_variant.zag` in this directory. Frozen TNN-2
(`tnn2.zag`, `tnn2_bin`, build `f4de7ff46`) untouched.

### 2.1 Copy-and-commit (`t2_revise_cc`)

Replaces the in-place `t2_revise_graph`:

1. **Find (read-only):** locate the stale SETREG via provenance edges,
   (s,r)-based (matches any fact with the same subject/relation, so
   post-fork contradictions work). No tombstoning, no mutation.
2. **Copy:** `t2_copy_graph` walks the graph from the MAP root, allocates
   fresh cells for every 101/102/103/104 cell, and applies the
   single-schema repair (fresh literal holding the observed value) to the
   stale SETREG's copy. Literals (902) are shared, not copied. Seq edges
   (type 12) are replicated between copies; provenance edges (type 1) are
   replicated to the same facts. The original graph is not modified.
3. **Verify:** `t2_exec` runs the COPY. The frame allocator cannot alias a
   graph node the commit depends on, because no graph node is tombstoned
   during verification. Bug `8b58c4104` is closed by construction: there
   is no revert path to be corrupt.
4. **Commit (atomic):** on verification success, `ns(W,m,20,croot)` retargets
   the MAP root and `ns(W,m,28,out)` updates the answer. Two field writes
   on the MAP node. Then the superseded original cells are tombstoned
   (after commit, outside verification). Shared literals survive.
5. **Fail honestly:** on verification failure, the copy is freed
   (cells tombstoned, edges removed) and the original is untouched.
   The candidate MAP is superseded via type-3 self-edge (`contradict_map`),
   and `ev_observe` teaches the observation as a fact. Queries fall back
   to the fact path.

### 2.2 MAP retargeting (`revise_on_contradict`)

The contradiction dispatch is now (s,r)-based, not exact-fact-node-based.
It finds MAPs with a DEP edge to ANY fact sharing the contradicted
fact's (s,r). After the first revision forks the fact lineage (new fact
taught), the second contradiction on the same (s,r) still reaches the
same MAP. This fixes the one-shot limit (boundary map Surprise 2).

The MAP node persists across revisions: its identity is the MAP node,
its current procedure is whatever its root field points to.

### 2.3 What was NOT changed

- The repair operator is the same single-schema topology (tombstone-free
  version of the frozen operator): replace the stale SETREG's literal.
  The researcher still chooses the repair form. SUF still FAILs for
  revision, as expected. This is deliberate per the revision advice:
  Constraints A (corruption) and B (one-shot) are fixed without widening
  the repair space.
- No new ISA operations, modes, bridges, handlers, or semantic cases.
  The repair machinery uses only ALLOC, field WRITE, LINK, and tombstone,
  all of which the frozen TNN-2 already performs inside revision.

## 3. Results (3/3 byte-identical runs)

### V1: Failed interior revision is a byte-identical no-op (advice test 1)

Setup: facts (101,11,102), (102,12,201); 2-hop chain (101,40)->201
(MAP node 13, root cell 6). Contradict interior fact: observe (101,11,777).

- Graph cell dump before and after: IDENTICAL (cells 6,7,10,11;
  all fields match).
- MAP root unchanged (6 -> 6). No commit on failure.
- `t2_exec` on the original root still returns 201.
- The MAP is superseded (fail-honest path); the observation fact answers.
- **V1 PASS.** The frozen bug's corruption mode cannot occur: the
  verification ran against a copy, the original was never tombstoned,
  and there is no revert path.

### V2: Successful revision produces a working MAP

Setup: fact (102,12,201); 1-hop chain (102,40)->201 (MAP node 15,
root cell 12, answer 201). Contradict: observe (102,12,999).

- MAP root retargeted (12 -> 16). Answer updated (201 -> 999).
- `t2_exec` on the new root returns 999.
- `ev_query(102,40)` returns 999 via the MAP path.
- Same MAP node (15) persists; only its fields changed.
- **V2 PASS.** Atomic commit works: two field writes, verified copy live.

### V3: Repeated contradiction reaches the same logical MAP (advice test 2)

Setup: as V2. Contradict (102,12,999), then contradict (102,12,888).

- After first: MAP node 15, root 12->16, answer 999.
- After second: MAP node still 15, root 16->20, answer 888.
- `t2_exec` on the final root returns 888.
- The fact lineage forked (102,12,999 taught after first revision), but
  the (s,r)-based lookup found the same MAP the second time.
- **V3 PASS.** The one-shot limit is fixed at the MAP level.

## 4. Honest scope and non-claims

- This experiment fixes revision SAFETY (no corruption) and
  REPEATABILITY (second contradiction reaches the MAP). It does not
  change WHAT repairs are proposed: the single-schema operator is
  researcher-authored, and the SUF decision list for revision is still
  empty. Presenting this as "the revision fix" for R3's structural
  ceiling would be failure-mode preservation.
- Cross-subject transfer of repaired graphs was not tested and is not
  claimed. The value-trace limitation (reuse experiment R4) is orthogonal.
- The 2-hop interior repair cannot succeed with the single-schema
  operator (the downstream guard still expects the old intermediate
  value). V1 confirms it fails SAFE, not that it succeeds. Multi-topology
  repair is future H1/H3 work on this substrate.
- GC note: failed copies are freed immediately (cells tombstoned, edges
  removed). Superseded originals are tombstoned after commit. The fresh
  literal allocated for a FAILED repair's SETREG copy is orphaned (one
  cell per failed revision); shared literals survive correctly. A
  production design needs a GC policy for orphans; this experiment does
  not implement one.

## 5. Standing architectural metric (variant delta vs frozen TNN-2)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 3 (copy-before-verify ordering;
  (s,r)-based MAP lookup; supersede-on-failure policy)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (single repair schema unchanged)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0 (not measured here)
- REVISION EVENTS: observed (V2: 1 commit; V3: 2 commits, same MAP)
- COGNITION LINES: +~180 added (cc_walk, cc_remap, t2_copy_graph,
  cc_free_graph, t2_revise_cc, rewritten revise_on_contradict),
  ~50 removed (in-place t2_revise_graph)
- MODES / BRIDGES / HANDLERS / SEMANTIC CASES: 0 / 0 / 0 / 0

## 6. Relation to the four regression tests (advice section 5)

1. Failed interior revision is a no-op: TESTED (V1 PASS).
2. Second contradiction revises again: TESTED (V3 PASS).
3. Revision failure supersedes, then facts answer: TESTED
   (V1: MAP superseded, observation fact taught; query path verified
   via MAP-first skip).
4. Floor preservation (FW4 12/12): NOT TESTED. This variant was not run
   against the frozen battery. The MAP-level changes must not regress
   fact-level law-change/revert; that check belongs to a future
   preregistered evaluation, not this experiment.

## 7. Deliverables

In this directory:
- `NAMECHECK.md` (Step 0 toolchain guard + UNFROZEN VARIANT declaration)
- `REVISION_SUBSTRATE.md` (this report)
- `tnn2_revision_variant.zag` (variant source, 1238 lines)
- `revision_probes.zag` (probe driver source)
- `tnn2_revision_variant_bin` (compiled binary)
- `probe_run1.txt`, `probe_run2.txt`, `probe_run3.txt` (3/3 byte-identical)

Paper untouched. Nothing pushed. Frozen TNN-2 untouched (verified:
no modifications under frozen source paths; variant lives in its own
directory).

## 8. Recommendation

Copy-and-commit + MAP retargeting is a sound correctness substrate for
TNN-3 revision. It closes the corruption bug class by construction and
makes multi-step revision architecturally possible. The next steps,
per the revision advice ordering, are: (a) preregister K-T3-REV-1/2/3
against this substrate, (b) widen the repair-proposal generator (H1),
(c) add the H3-lite repair-dispatcher policy node for the SUF-relevant
learner-state write path. None of (a)-(c) are implemented here.
