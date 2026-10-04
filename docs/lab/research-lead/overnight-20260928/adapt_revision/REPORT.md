# REPORT.md -- ADAPT-REVISION: revising an L2 adaptation

Date: 2026-10-02. Worker: Adapted Structure Revision Worker.
Verdict: **ADAPT-REVISION-COMPLETE**.

## Mission

Prior work showed the learner can ADAPT a learned MAP (L2 EXTEND-ONE:
X becomes X' by adding a frontier link). Open question: when the
adapted MAP proves wrong under a world change, can the learner revise
the ADAPTATION itself (not just the underlying contract)?

## Design (preregistered, amended transparently)

- Train contract X = [1,1,1] (11->12->13->14). Phase-2 teaches
  (14,1,15); the frozen adapt_extend creates X' = [1,1,1,1]
  (type-16 edge X'->X), which answers (11,72,15)->15.
- Operator (`revise_patch.zag`, pure Zag, zero new opcodes/modes/
  edge types): `adapt_revise` scans live adapted MAPs. A MAP `a`
  (source `src`) is STALE iff the source contract is intact
  (`cc_satisfy(src,s)` full) while the adaptation is not
  (`cc_satisfy(a,s)` not full). On stale: re-extend `src` against
  the current world, link the new MAP's type-16 edge to `a`
  (chain new->a->src), then retire `a` (field 36 = 0; edges
  persist). Dead-end frontier: retraction (retire, create nothing).
  `ev_query_revise` runs `adapt_revise` before the frozen
  `adapt_extend` fallback.
- Amendment 1 (pre-implementation): per-episode query relations to
  dodge the exact-hit memory path.
- Amendment 2 (pre-implementation, from trial findings): (a)
  teach-then-kill world changes (alloc_node recycles dead ids;
  kill-then-teach silently rewrites the adaptation's licensing);
  (b) R2/R4 withdraw stale cached shortcuts so redundant
  chain/sum-trial paths do not confound the -2 signal; (c) retire
  after re-extension; "retired" observably means "not a live MAP".

## Results (3/3 byte-identical runs)

- **R1 PARAM-REVISE: PASS (8/8).** World change teaches (14,3,12)
  (cyclic: rebind cannot help), kills (14,1,15). REVISE-STALE fired;
  X'' = [1,1,1,3] created with type-16 X''->X'; X' retired; chain
  X''->X'->X; ans = 12; contract control (11,74,14) = 14.
- **R2 RETRACT-ON-DEAD-END: PASS (4/4).** Frontier killed, nothing
  taught. REVISE-STALE fired; X' retired; zero live adapted MAPs;
  type-16 X'->X persists; ans = -2. The learner revised the
  adaptation decision to nothing rather than hallucinating.
- **R3 NO-CHANGE-CONTROL: PASS (5/5).** No world change; ans = 15;
  X' live; exactly one live adapted MAP; no type-16 edge targets X';
  edge count unchanged. Revision is driven by the world change.
- **R4 CONTRACT-BREAK-CONTROL: PASS (4/4).** World change breaks
  the contract ((12,1,13)->(12,1,93)). ans = -2; X' still LIVE; one
  live adapted MAP; edge count unchanged. The learner does not
  touch the adaptation when the break is in the contract. Mirror
  discrimination holds: revision fires iff the adaptation broke.

## What this establishes

The learner revises the adaptation (different parameter via
re-extension, or retraction to nothing), keeps the provenance
chain readable (type-16 new->old->source), leaves the base
contract intact, and discriminates adaptation-break from
contract-break. The revision is computed from satisfiability
only; the operator names no relation, MAP, length, query, or
expected value.

## Files

- `PREREG.md`, `PREREG_AMENDMENT1.md`, `PREREG_AMENDMENT2.md`
- `revise_patch.zag` (operator), `rv_driver.zag` (battery)
- `build.sh`, `rv_full.zag`, `rv_bin`, `run1.txt`, `run2.txt`,
  `run3.txt`, `sha256sums.txt`, `compile.txt`, `NAMECHECK.md`
