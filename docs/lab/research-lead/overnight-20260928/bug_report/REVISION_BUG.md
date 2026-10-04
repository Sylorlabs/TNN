# Revision-Corruption Bug Report

**Status:** DOCUMENTED, NOT FIXED. TNN-2 is frozen; this bug is recorded so TNN-3 avoids it.
**Source:** Boundary mapper, commit `8d763d766`, Surprise 1 (probe pE E4).
**Severity:** Silent state/answer divergence. White-box graph is permanently broken while
query answers keep flowing from a stale fact.

## 1. What happens

A failed interior revision permanently corrupts the promoted graph.

Sequence (probe pE E4, boundary map lines 124-132):

1. Facts `(101,11,102)` and `(102,12,201)` are taught. A 2-hop chain `(101,40)->201`
   is promoted as a graph.
2. A contradiction is observed on the INTERIOR fact: `(101,11,777)`.
3. `t2_revise_graph` fires: it patches the interior SETREG, re-executes the graph,
   and correctly computes -999999 (the patched chain is broken: 777 has no
   outgoing relation-11 fact).
4. The REVERT path runs, intending to restore the graph to its pre-revision state.
5. The revert is corrupt (Section 2). The graph is permanently broken: `t2_exec`
   now returns -999999 forever.
6. Yet `ev_query` still answers 201, because queries hit the promoted FACT directly
   via `activate` and never re-execute the graph.

End state: the system answers 201 with a broken justification it cannot detect.
White-box state and query answers diverge silently. Verified by direct field dumps
before/after (boundary mapper probes `pY`, `pZ` diagnostics).

## 2. Why it happens

The revert is broken by a frame-allocation alias (boundary map lines 299-309):

- `t2_revise_graph` tombstones the stale node (marks it free, bid flag 0).
- The verification re-execution calls `t2_exec`, which allocates its execution
  frame via `alloc_node`.
- `alloc_node` returns the just-tombstoned stale node as free memory.
- `fr_set` overwrites the stale node's fields: f4=0, f8=0, f20=frame garbage
  (in probe E4, f20=777).
- The revert path restores only the node TYPE and the LIVE-FLAG. It does NOT
  restore field 4, field 8, or field 20.
- Result: the node that was supposed to be reverted now has f4=0, f8=0, f20=777.
  The SETREG's slot field (0) is below 1000, which fails the execute guard, so
  `t2_exec` returns -999999 on every future execution.

In short: the revert assumes the tombstoned node is untouched during verification,
but the verifier itself reallocates and clobbers that exact node. The revert then
restores an incomplete subset of fields, leaving the graph in a state that no
legitimate revision would have produced.

## 3. Impact

- **Irreversible corruption.** There is no second revision, no repair path, and no
  revert-to-original for the broken graph. (See also Surprise 2: revision is
  one-shot per fact lineage, so the graph is frozen at its first revision anyway;
  the bug makes even the first revision a potential permanent break.)
- **Silent divergence.** The stale promoted fact keeps answering (201) while the
  graph that supposedly justifies it fails (-999999). No signal flags the
  inconsistency. `standing` is 1 before and after: it tracks the DEP/CON edge
  balance, not correctness, so it does not catch this.
- **Masks the failure it was meant to handle.** The whole point of the revert path
  is to make failed revisions safe. The bug makes a failed revision worse than no
  revision: an un-revised graph at least executed correctly to its stale answer.
- **Blocks multi-step belief correction.** Any TNN-3 design that relies on
  revising graphs in place inherits this failure mode unless the allocator and
  the revert path are fixed together.

## 4. Required fix (TNN-3, not TNN-2)

Do NOT fix this in TNN-2. The binary is frozen; the bug is part of the evaluated
artifact. TNN-3 must avoid it. Any of the following closes the hole:

1. **Atomic revision (recommended).** Reserve the execution frame BEFORE
   tombstoning any graph node, so the verifier cannot alias a node the revert
   needs intact. Alternatively, run verification against a snapshot copy and swap
   only on success.
2. **Full field snapshot/restore.** If the revert path must reuse nodes, snapshot
   ALL node fields (type, live-flag, f4, f8, f20, and any other mutable fields)
   before patching, and restore the full set on revert. The current revert's
   type-plus-live-flag-only restore is the direct cause.
3. **Separate the free pools.** Do not let `alloc_node` hand out nodes that are
   part of an in-progress revision's revert set. A revision-epoch tag on
   tombstoned nodes, respected by the allocator, would prevent the alias.

Whichever is chosen, add a regression test: contradict an interior fact, force a
failed verification, and assert (a) the graph re-executes to its pre-revision
answer and (b) a white-box field dump matches the pre-revision snapshot
byte-for-byte. The boundary mapper's pY/pZ diagnostics are the model for the
field-dump check.

## 5. Related findings (not this bug, but compounding)

- **Surprise 2 (one-shot revision):** E2/E3 show the second contradiction on the
  same (s,r) never reaches the graph, because the first revision forked the fact
  lineage (the new fact has no graph provenance edges). Revision follows the
  ORIGINAL fact's provenance exactly once. This is architectural, not a memory
  bug, but it means the corruption bug's damage can never be repaired through the
  revision path.
- **Shadowed facts:** E5 shows observing a contradiction on the promoted fact
  itself teaches a new fact that shadows the old one by recency, without revising
  any graph. The map still claims ans=201 while queries answer 777. Silent
  divergence again, via a different route.

## 6. Provenance

- Boundary map: `docs/lab/research-lead/overnight-20260928/tnn2_boundary/BOUNDARY_MAP.md`
  (commit `8d763d766`), Surprise 1, probe pE E4 (lines 124-132, 299-309).
- Field dumps: `tnn2_boundary/probes/pY`, `pZ` diagnostics (same commit).
- Frozen TNN-2 binary: `tnn2_build/tnn2_bin` (commit `f4de7ff46`), untouched.
- This report: documentation only. No source, binary, shim, or sealed asset was
  modified, executed, or inspected in producing it.
