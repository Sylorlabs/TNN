# TNN-2 Cost Accounting

**Verdict: COST-ACCOUNTING-COMPLETE.** Unfrozen variant only. 3/3
byte-identical runs (SHA-256 `8a738e5d...b785`). All behavior assertions
passed; instrumentation is behavior-preserving.

## Method

Four cost dimensions, measured as before/after deltas per operation on
an instrumented unfrozen variant (see NAMECHECK.md):

- **nodes**: delta live nodes (`hg(W,20)`).
- **edges**: delta live edges (`hg(W,24)`).
- **exec**: delta ISA opcodes executed (`execute` loop counter, header 56).
- **scan**: delta workspace scan-loop iterations (header 60; covers
  `activate`, `decay`, `is_superseded`, `is_prot`, `evcount`, `bid`,
  `evict_node`, `ref_prot`, `t2_lu_first`, `link_edge` alloc scans).

"Steps" (latency) = exec + scan. All runs deterministic.

## Cost table

| Operation | nodes | edges | exec | scan | steps |
|---|---|---|---|---|---|
| teach (fresh W) | 1 | 1 | 0 | 4,097 | 4,097 |
| query hit (fresh W) | 0 | 1 | 0 | 37,888 | 37,888 |
| query, trial+promote | 41 | 24 | 18 | 21,970 | 21,988 |
| query miss, full path | 3 | 3 | 0 | 13,325 | 13,325 |
| observe confirm | 0 | 1 | 0 | 37,888 | 37,888 |
| observe contradict | 2 | 4 | 0 | 33,804 | 33,804 |
| act (guide select) | 0 | 1 | 0 | 61,445 | 61,445 |
| activate (100 facts) | 0 | 0 | 0 | 435,198 | 435,198 |
| query hit (100 facts) | 0 | 0 | 0 | 443,398 | 443,398 |
| evict_node (1 victim) | 0 | -1 | 0 | 2,528,389 | 2,528,389 |
| revise (chain rewire) | 6 | 7 | 4 | 42,101 | 42,105 |

Raw transcripts: `run1.txt`, `run2.txt`, `run3.txt` (identical).

## Findings

**1. Scan dominates everything; execution is negligible.**
The most ISA-intensive operation measured (trial+promote) executes 18
opcodes against 21,970 scan steps, a ratio of roughly 1220:1. Across all
11 measurements, total exec is 22 against total scan over 3.6M. TNN-2
spends its compute on linear workspace scans for bookkeeping, not on
running procedures. The "cognitive" work (ISA execution) is lost in the
noise of retrieval and maintenance scans.

**2. Every event pays a fixed decay tax of 4,096 scan steps.**
`decay` scans all 4,096 edge slots on every `ev_teach`, `ev_query`,
`ev_observe`, and `ev_act`, regardless of workspace occupancy. Teaching
a single fact on a fresh workspace costs 4,097 scan steps, of which 4,096
are decay and 1 is the edge-alloc scan. The marginal structural cost of
a teach is 1 node + 1 edge; the marginal scan cost is ~0.

**3. A query hit costs ~38k scan steps, almost entirely bid bookkeeping.**
Decomposition of M-query-hit (37,888): decay 4,096 + `activate` node
scan 1,024 + `is_superseded` 4,096 + `bid` (5x `evcount` at 4,096 each
plus MEM scan 4,096 = 24,576) + `ref_prot` 4,096. The fact is found by a
direct field comparison; the other ~37k steps exist to maintain the
evidence-meter (`bid`) that the white-box analyses show is a birth
certificate for MAPs and is never read by any learner decision for
FACTs either (no production consumer distinguishes high-bid from
low-bid facts at query time beyond ranking).

**4. A successful trial is cheaper than a hit.**
Trial+promote costs 21,970 scan steps versus 37,888 for a hit, because
the trial path skips the per-candidate `bid` computation (`activate`
finds no direct fact, so no candidate is ever ranked). Building,
verifying, and promoting a 4-link procedure (41 nodes, 24 edges, 18 ISA
steps) is scan-cheaper than looking up one stored fact. This is not an
efficiency win; it is evidence that hit cost is dominated by
bookkeeping unrelated to answering.

**5. Retrieval scales as O(facts x edge-slots).**
`activate` over 100 facts costs 435,198 scan steps (~4,352 per resident
fact), driven by `is_superseded` (4,096 edge iterations) evaluated for
each live node plus `bid`/`evcount` scans per candidate. Doubling the
workspace roughly doubles per-query latency even though the edge table
is mostly empty; the scans are over fixed-size tables (1,024 nodes,
4,096 edges), not over live occupancy.

**6. A single eviction costs 2.5M scan steps and destroys structure.**
`evict_node` computes `bid` (5 edge scans + MEM scan, ~25k steps) for
each of up to 1,024 nodes to find the minimum, then scans all edges to
clean up. Measured: 2,528,389 scan steps for one victim, roughly 617x
the scan cost of teaching a fact. Per the eviction-corruption analysis,
this expensive operation silently corrupts surviving MAPs (zombie
roots), so the system pays its highest per-operation cost for an
operation that damages its own procedural memory.

**7. The miss path is cheap because its products are never read.**
Full miss (trial fails, bootstrap fails, UNCERTAINTY + guide created):
3 nodes, 3 edges, 13,325 scan steps. The theater audit and T30 ablation
show these nodes are write-only. The system spends 13k steps per miss
manufacturing structures no decision will ever consult.

**8. Revision is the cheapest structural change per unit of effect.**
Revising a contradicted chain link: 6 nodes, 7 edges, 4 exec steps,
42,101 scan steps, and the corrected answer (999) is queryable
afterward. It is the only measured operation whose structural cost
purchases a persistent, behaviorally visible improvement.

## What each unit of cost buys (descriptive, not a claim)

- 1 node + 1 edge + ~0 scan (teach net of decay tax): one stored fact,
  retrievable later at ~38k scan per lookup.
- ~38k scan (query hit): one retrieved value. ~99% is bid/decay/protection
  bookkeeping.
- 41 nodes + 24 edges + 18 exec (trial+promote): one verified procedure
  plus its shadow fact. The procedure is never executed at query time
  (closed replay; shadow answers first).
- 3 nodes + 3 edges (miss): one UNCERTAINTY node and one guide, both
  write-only.
- 2.5M scan (eviction): one freed node slot, plus silent corruption of
  surviving MAP roots.
- 6 nodes + 7 edges + 4 exec (revision): one corrected procedure whose
  new answer is actually returned.

## Implications for the capability/cost question

1. Any future capability/cost comparison against LLM baselines must use
   amortized scan steps as the cost unit, not node counts. Node counts
   understate true cost by 3-4 orders of magnitude for retrieval-heavy
   workloads.
2. The fixed 4,096-step decay tax per event and the O(NxE) retrieval
   scans are architectural, not incidental: they come from fixed-size
   table scans in `decay`, `activate`, `bid`/`evcount`, and
   `evict_node`. A lifetime stream of 10k events pays ~41M scan steps in
   decay alone before doing anything cognitive.
3. Cost and capability are currently anticorrelated at the margin: the
   most expensive operation (eviction) destroys capability; the
   cheapest structural path to improved answers (revision) is gated
   behind contradiction rather than available as a general policy.

## Limitations

- SCAN is a lower bound: `alloc_node` free-slot scans, frame walks, and
  trial assembler loops are not instrumented (small, bounded).
- Abstract steps, not wall-clock; no claim about hardware performance.
- Single-workspace, single-threaded; no interference or contention costs.
- Costs measured on small workspaces (except the 100-fact regime);
  scaling beyond 1,024 nodes / 4,096 edges is unmeasured (tables are
  fixed-size, so costs saturate rather than grow).

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 1 (M-revise, researcher-contradicted)
- COGNITION LINES: 0 added (12 instrumentation lines in variant only)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
