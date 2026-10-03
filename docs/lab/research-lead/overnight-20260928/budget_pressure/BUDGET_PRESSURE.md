# Budget Pressure Experiment: Eviction Behavior and Post-Pressure Capability

Verdict: BUDGET-PRESSURE-COMPLETE. 3/3 byte-identical runs.

## Method

One learner (`W`, 1024 nodes / 4096 edges), no reset. Driver built on a
verbatim copy of frozen `tnn2.zag` (SHA-256 verified identical before and
after; cognition code untouched; test main removed, measurement driver
appended). Pinned `znc_linux_x86_64_abed8aa1`. Unsealed synthetic subjects
only. No sealed worlds opened.

Phases:
- **P1**: Build a chain MAP via masked query (reproduce the P4 setup from
  `tnn2_transfer/TRANSFER_ANALYSIS.md` section 4).
- **P2**: 1050 teaches to the 1024-node cap. Verify the P4 eviction
  signature (order of death, fossil MAP, catastrophic forgetting).
- **P3a**: New learning at cap: 20 teaches + immediate query-back.
- **P3b**: Hit-fact retention: one fact hit 30x, one fact unhit, 60
  teaches of pressure, then liveness + queryability check.
- **P3c**: Trial (masked query) at cap on a fresh chain: does construction
  still work under eviction pressure?
- **P3d**: Re-teach the P2-forgotten answer: measure re-learning cost
  (tests R5, revisable forgetting).
- **P3e**: 120 mixed events (teach / query / observe / masked-miss) at cap:
  stability of live count + probe recall rate.

Scale note: P3b pressure was reduced from 200 to 60 teaches and P3e from
300 to 120 events after discovering that `evict_node` is O(nodes x edges)
(~30M ops per victim: `bid` scans edges 6x per node across ~1022 nodes).
This computational cost of cap operation is itself a finding (section 5).

## 1. P4 prediction test: CONFIRMED

P2 reproduced the transfer-analysis P4 signature exactly (3/3 identical):

| Metric | P4 (transfer) | P2 (this run) |
|---|---|---|
| live_nodes | 1022 (at cap) | 1022 (at cap) |
| MAP node live | 1 | 1 (node 15) |
| FACTs live | 1021 | 1021 |
| op cells live (101-104) | 0 | 0 |
| MAP re-executable | no (-999999) | no (0 live cells on graph walk) |
| requery learned answer | -2 | -2 |

Eviction order confirmed: executable structure (bid 0, unprotected) dies
first; the MAP (constant bid 2) outlives its graph as a fossil; the
promoted fact and licensing facts are evicted after their 12-event PRO
clocks expire; the learned answer is catastrophically forgotten
(requery = -2) and cannot be rebuilt (licensing facts gone).

Fossil anatomy (white box): MAP node 15 live, its root node (8) live, but
the graph walk from root finds 0 live cells. The header survives; the
body and provenance are gone. Inert, unrevisable, reclaimed last.

Additional observation: the P2 requery (a miss) triggered the trial path,
which allocated 13 op cells + 13 literals + 1 uncertainty, evicting 28
facts (T1 1021 -> 993) to make room. A single forgotten-query miss costs
28 facts under cap pressure. Forgetting is not free: the miss path is
more expensive than the teach path at cap.

## 2. Post-pressure capability

### P3a: new learning at cap WORKS

- 20/20 teaches succeeded (0 failures; eviction made room each time).
- 20/20 immediate query-backs hit.
- The learner is not jammed at cap. `alloc_node` -> `evict_node` ->
  lowest-bid unprotected victim functions as a working pressure valve.

### P3b: hit retention (underpowered, honest limitation)

- 30x-hit fact: node 97, live, queryable (9001). Survived.
- 0x-hit fact (taught at the same time): node 98, live, queryable (9003).
  Survived.
- Both survived because 60 evictions only reclaimed the 60 oldest nodes
  (the 7000-series from P2); the 9000-series facts were too young in the
  age ordering to be reached. The test did NOT discriminate the USE-edge
  bid bonus. Reported as a limitation, not a result about hit protection.

### P3c: trial (construction) at cap WORKS

- Fresh chain (9100->9101->9102->9103) taught at cap.
- Masked query (9100,40): trial succeeded, answer 9102, new MAP promoted
  (node 171).
- Post-trial snapshot: T20=2 (two MAPs), Top=17, T902=18. The new trial's
  graph cells are live.
- Construction is NOT jammed by a full workspace. The trial loop
  allocates through the same eviction valve and succeeds.

### P3d: re-learning cost (R5)

- Re-taught the P2-forgotten answer (6000,40,6002): node 173 allocated,
  nalloc delta 0 (evict -1 then alloc +1 nets to zero at cap).
- Requery returns 6002. The answer is restored.
- Cost: one eviction + one alloc, identical to first learning. The
  `rec_evict` records are never consulted; nothing about the prior
  learning accelerates re-learning. R5 (revisable forgetting) is
  confirmed absent: forgetting is not cheaper to reverse than to incur.

### P3e: sustained mixed pressure

- 120 mixed events at cap: live count stable at 1022 throughout.
- Probe recall: 10/10 of the 10 probe facts taught during P3e
  queryable at end.
- Final state: T1=935, T20=2, Top=17, T902=18, T30=49 (uncertainty nodes
  accumulate from masked misses; +1 per miss, never deduped).
- No deadlock, no allocation failure, no jam across teach / query /
  observe / masked-miss event types.
- Nuance: the probes survived by recency (eviction is oldest-first;
  120 events = ~360 evictions did not reach the young 9800-series
  cohort). Moderate pressure preserves recent memories; only severe
  pressure (~1000+ events, full workspace turnover) causes catastrophic
  forgetting of specific old answers. Degradation is graded, not a cliff.

## 3. What gets evicted first (answer)

Strictly by (bid, age): bid-0 unprotected nodes oldest-first. In practice:
trial cells and literals (bid 0, never protected) > unhit facts past
their 12-event PRO window (bid 0) > contradicted facts (bid negative
from type-3 edges) > MAPs (bid 2, reclaimed last) > recently-hit facts
(bid grows with USE edges, never decayed).

## 4. Answers to the tasked questions

1. **What gets evicted first?** Bid-0 unprotected nodes, oldest first.
   Matches the P4 profile exactly.
2. **Do MAPs fossilize?** Yes. Node 15: header live, 0 live graph cells,
   provenance gone. Inert and unrevisable.
3. **Are answers catastrophically forgotten?** Yes. Requery = -2 after
   cap pressure; licensing facts co-evicted so rebuild is impossible.
4. **Does trial garbage consume budget?** Yes. Rejected-trial cells are
   never freed; they are the first eviction victims, meaning the system
   spends its eviction budget discarding its own scratch. The P2-requery
   trial allocated 26 nodes to answer one forgotten query.
5. **Capability AFTER pressure?** Surprisingly intact at the interface
   level: new learning works (P3a 20/20), construction works (P3c MAP
   promoted), re-learning works (P3d), sustained operation is stable
   (P3e). What is lost is SPECIFIC: the particular learned answers and
   executable structures that were evicted. The machinery survives; the
   memories do not.

## 5. Computational cost of cap operation (incidental finding)

`evict_node` scans all 1024 nodes; for each live unprotected node it calls
`is_prot` (4096-edge scan) and `bid` (5 x 4096-edge `evcount` scans plus
a 4096-edge type-10 scan, ~25K edge visits). Per eviction: ~1022 x ~30K
~ 30M operations. Every teach at cap, every trial cell at cap, every
miss-path allocation at cap pays this. A continuing learner operating at
cap indefinitely pays O(NxE) per allocation. This is a scalability
ceiling on the current fixed eviction machinery, independent of the
cognitive questions.

## 6. Standing architectural metric (this experiment)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (experiment only, no mechanism)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 observed (all eviction and
  re-learning followed fixed source paths)
- SOURCE-ENUMERABLE FORMS: all observed behavior
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 exercised
- REUSE EVENTS: 0
- REVISION EVENTS: 0 in this run
- COGNITION LINES: 0 added
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0

## 7. Limitations

- P3b did not discriminate hit-based protection (both facts too young
  for the eviction cursor). A proper test needs pressure deep enough to
  reach the cohort, which is computationally expensive under O(NxE)
  eviction.
- Single MAP / single chain tested for the fossil anatomy. The P4 profile
  is the general claim; this run confirms one instance.
- P3e probe recall was 10/10 with graded degradation: moderate pressure
  preserves recent memories by recency; only severe pressure (full
  workspace turnover) causes catastrophic forgetting.

## Files

- `NAMECHECK.md`: Step 0 guard, provenance, constraints.
- `bp_driver.zag`: measurement driver (new main only).
- `bp_base.zag`: verbatim frozen copy (SHA-256 identical).
- `bp_nodriver.zag`: base with test main removed.
- `bp_full.zag`: nodriver + driver; compiled with pinned znc.
- `bp_bin`: compiled driver binary.
- `bp_run1.txt`, `bp_run2.txt`, `bp_run3.txt`: 3/3 byte-identical.
