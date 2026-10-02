# REPORT.md -- Scaling/Indexing Worker

**Verdict: SCALING-INDEX-COMPLETE**

## What was built

A learner-maintained sublinear index for MAP retrieval in structural
rebinding, addressing Constitution Section 17 ("the current 1024-node /
full-scan limits are unacceptable") and the rebind-hardening finding that
15 MAPs cost 21 verifies vs 4 with no early termination for mismatched
MAPs (commit `0509fd116`).

**Mechanism** (`si_patch.zag`, ~150 lines, unfrozen variant only):

- **Plen-bucket index.** Four buckets in a dedicated index node (tag 40,
  unused by the base; node id in header 52). Fields 20/24/28/32 hold
  bucket heads for plen 2/3/4/5. Each bucket is an intrusive linked list
  of promoted MAP ids via MAP field 12 (next-pointer; -1/unused on
  tag-20 nodes in the base). Only plens 2..5 are indexed because
  `t2_gather` paths are at most length 5.
- **Learner-maintained.** `idx_add` fires inside the (mode-gated)
  `promote_graph`, so every promotion (trial-built, rebound, taught)
  updates the index. No researcher-authored MAP table exists. The
  plen walk happens once at promotion instead of once per query per MAP.
- **Identical trial order.** `rebind_try_idx` gathers paths, walks only
  buckets whose plen matches a gathered path length, collects candidate
  ids, insertion-sorts ascending, then runs the exact (MAP,path) trial
  nest of the linear scan. Verify counts must therefore match exactly;
  only scan work differs.
- **Why plen, not literals.** The task suggested (plen, first-literal).
  Literal keys do not transfer: rebinding deliberately discards the
  helper MAP's literals and re-instantiates the chain shape on the query
  subject's own literals (the trust boundary: B executes on B's data).
  The structural parameter plen is the correct and only transferable key.

A first version of this patch used header 32/36/40/44 for buckets and
collided with the base's context ring buffer (`ctx_push`); it panicked
on the first indexed run. Fixed by moving to the dedicated index node.
The collision is documented here as found, not hidden.

## Experiment

Six worlds, one binary, mode flag selects the arm:

- D non-chain decoy MAPs (plen-2 chain with the set cell retagged to
  INC, so `rb_chain_plen` returns -1) + 5 plen-5 chain MAPs.
- Decoys simulate accumulated knowledge of other structural forms:
  genuinely irrelevant to a chain query.
- 3 plen-5 queries on distinct subjects per world.
- Scales: D = 5, 45, 95 (total MAPs = 10, 50, 100).
- Metrics per query: answer, tried/rejected verifies, scan visits
  (header 56), plen-walk calls (header 60).

## Results (3/3 byte-identical, SHA-256 `c9d02824...3aeb`)

| World | Q | ans ok | tried | rejected | scan visits | plen walks (per query) |
|---|---|---|---|---|---|---|
| LIN10 | 0-2 | 1 | 1 | 0 | 69 | 6 |
| IDX10 | 0 | 1 | 1 | 0 | 5 | 0 (+1 rebound index) |
| IDX10 | 1 | 1 | 1 | 0 | 6 | 0 (+1) |
| IDX10 | 2 | 1 | 1 | 0 | 7 | 0 (+1) |
| LIN50 | 0-2 | 1 | 1 | 0 | 349 | 46 |
| IDX50 | 0-2 | 1 | 1 | 0 | 5/6/7 | 0 (+1) |
| LIN100 | 0-2 | 1 | 1 | 0 | 699 | 96 |
| IDX100 | 0-2 | 1 | 1 | 0 | 5/6/7 | 0 (+1) |

Build-phase plen walks (one-time index construction): IDX10=10,
IDX50=50, IDX100=100; LIN=0.

## Analysis

1. **Verifies identical everywhere.** tried=1, rejected=0 in all 18
   query runs, both arms, all scales. The index preserves mechanism
   semantics exactly (trial order is byte-identical by construction).
2. **Linear scan work grows O(D).** Slot visits 69 -> 349 -> 699;
   plen walks 6 -> 46 -> 96 per query. Every query re-examines every
   MAP's graph, including the 95 irrelevant decoys.
3. **Indexed scan work is O(1) in irrelevant knowledge.** 5 bucket
   visits at all scales (6, 7 on Q1/Q2 only because prior queries'
   rebounds accumulate in bucket 5). Zero plen walks at retrieval;
   the walk is amortized to promotion time (D+5 once, not per query).
4. **Sublinearity: YES, for irrelevant knowledge.** Indexed retrieval
   cost is constant as decoys grow 5 -> 95; linear retrieval cost
   grows ~10x. At 100 MAPs the indexed arm does 140x fewer scan visits
   per query (5 vs 699).
5. **Wall time.** Full 6-world binary runs in ~1s; query-time work is
   dominated by counters at this scale, so wall-clock differences are
   in the noise. The counters are the measurement. At lifetime scales
   (1000s of MAPs x 1000s of queries) the O(D)-per-query vs O(1)
   difference dominates.

## Honest limits

1. **Indexing cannot reduce verifies when decoys structurally match.**
   If decoy MAPs share the query's plen AND the subject has matching
   paths (the H1S case: plen-3 decoys on len-3 subpaths), both arms
   verify-and-reject them identically. Verification must arbitrate;
   the index only removes scan work, never candidate trials.
2. **`t2_gather` still scans O(1024) FACT slots per query** in both
   arms (constant, not compared). Fact indexing is separate future work.
3. **Revision staleness.** If a MAP's graph were revised after
   promotion, its bucket could go stale. No revision occurs in this
   experiment; invalidation-on-revision is future work.
4. **Amortization, not free.** The indexed arm pays D+5 plen walks at
   promotion. This wins when queries outnumber promotions, the normal
   lifetime regime. For a single query over freshly built knowledge,
   total work is comparable; query latency is still lower.
5. **Scale tested to 100 MAPs.** 1000+ MAPs exceed the 1024-node
   workspace (a separate architectural limit, Constitution 17); the
   scaling law measured here (O(1) vs O(D) in irrelevant knowledge)
   is what transfers, not the absolute fixture size.
6. **Chain family only.** The bucket key is the chain structural
   parameter. Other graph families need their own keys (same pattern).

## Standing metrics

- RESEARCHER-OWNED: bucket count (4), plen range (2..5), index node
  tag (40), field layout, intrusive-list discipline.
- LEARNER-OWNED: all bucket contents (which MAP id sits in which
  bucket), built entirely from promotion events.
- COGNITION LINES: ~150 (patch). MODES/BRIDGES/HANDLERS/SEMANTIC
  CASES: 0/0/0/0.
- One-System: the index reuses existing node/field/header machinery;
  no new node types, edge types, or scanners.

## Deliverables

- `si_patch.zag` (index mechanism), `si_driver.zag` (scale worlds),
  `build.sh` (assembly with function-count checks), `si_full.zag`
  (assembled, 1882 lines), `si_bin` (compiled), `si_run_1/2/3.txt`
  (3/3 byte-identical), `compile_err.txt` (warnings only),
  `NAMECHECK.md`, `REPORT.md`.
- Base provenance: `hard_base.zag` SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa8bd`
  (frozen TNN-2 base, read-only; rebind logic from `0509fd116`).
- Pure Zag via pinned znc. Safebin PATH throughout;
  `which python3 python` empty. Zero em/en dashes (byte-verified).
  Paper untouched. Nothing pushed.
