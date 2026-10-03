# TNN-2 Scaling Analysis

**Verdict: SCALING-COMPLETE.** Analysis only. All projections are
arithmetic on the measured cost table from `3eeb0d78e` under an explicit
event-mix model. No implementation, no new measurements.

## 1. Inputs

**Measured per-operation scan costs** (from COST_ACCOUNTING.md, 3/3
byte-identical):

| Operation | scan steps |
|---|---|
| teach | 4,097 |
| query hit | 37,888 |
| query, trial+promote | 21,988 |
| query miss, full path | 13,325 |
| observe confirm | 37,888 |
| observe contradict | 33,804 |
| act (guide select) | 61,445 |
| query hit (100 facts) | 443,398 |
| evict_node (1 victim) | 2,528,389 |
| revise (chain rewire) | 42,105 |

**Structural facts** (frozen source, read-only):
- Node table: 1,024 slots, edge table: 4,096 slots (source literals,
  `NN()`/`NE()`, ~40 scan sites use these constants).
- `decay` scans all 4,096 edge slots on EVERY event
  (`ev_teach`, `ev_query`, `ev_observe`, `ev_act`).
- `alloc_node`: linear scan for a free slot; when full, calls
  `evict_node` (min-bid victim over up to 1,024 nodes, then full edge
  cleanup). If no victim, returns -1.
- Per the eviction-corruption analysis, eviction silently corrupts
  surviving MAP roots (zombie MAPs). Per the white-box inventory, the
  workspace reached 1022/1024 live nodes after FW9.

**Event-mix model** (stated explicitly; a plausible lifetime stream):
- 30% teach, 25% query hit, 15% query miss, 10% trial+promote,
  5% observe confirm, 5% observe contradict, 10% act.

Weighted mean scan cost per event (pre-saturation):

```
0.30 x  4,097 =  1,229
0.25 x 37,888 =  9,472
0.15 x 13,325 =  1,999
0.10 x 21,988 =  2,199
0.05 x 37,888 =  1,894
0.05 x 33,804 =  1,690
0.10 x 61,445 =  6,145
-----------------------
mean          = 24,628 scan steps/event
```

Weighted mean node growth per event (from the node deltas):

```
0.30 x  1 = 0.30   (teach)
0.25 x  0 = 0      (hit)
0.15 x  3 = 0.45   (miss)
0.10 x 41 = 4.10   (trial+promote)
0.05 x  0 = 0      (confirm)
0.05 x  2 = 0.10   (contradict)
0.10 x  0 = 0      (act)
-----------------------
mean          = 4.95 nodes/event
```

The trial+promote term dominates node growth. A quieter mix (1% promote)
gives ~1.2 nodes/event. Both regimes are analyzed below.

## 2. Cost projections

### 10,000 events (pre-saturation, if it were reachable)

- Mean: 10,000 x 24,628 = **246M scan steps**.
- Decay tax alone: 10,000 x 4,096 = **41M** (17% of the mean-mix total).
- ISA execution across the same stream: on the order of hundreds of
  opcodes. The cognitive fraction (exec / (exec + scan)) is ~0.0006%
  in the measured sample and stays negligible at any scale.

### The node-budget wall (the binding constraint)

The 1,024-node table fills at:

- Busy mix (4.95 nodes/event): 1,024 / 4.95 = **~207 events**.
- Quiet mix (1.2 nodes/event): 1,024 / 1.2 = **~850 events**.

Empirical anchor: the white-box inventory found 1022/1024 live nodes
after FW9 (nine worlds), consistent with fill-in within the low hundreds
of events at observed promotion rates.

**The wall is at hundreds of events, not thousands.** Everything below
assumes the post-saturation regime, because no lifetime stream of
interest stays under ~1k events.

### Post-saturation regime

Once the table is full, every new node allocation triggers `evict_node`
(2,528,389 scan steps) before the operation itself runs. Per-event cost
becomes:

```
base (24,628) + nodes_per_event x 2,528,389
```

- Busy mix: 24,628 + 4.95 x 2,528,389 = **~12.5M scan steps/event**.
- Quiet mix: 24,628 + 1.2 x 2,528,389 = **~3.1M scan steps/event**.

### 100,000 events

The system is deep in eviction churn for ~99% of the stream.

- Quiet mix: 100,000 x 3.1M = **~310B scan steps**.
- Each of the ~120,000 evictions also risks silent MAP-root corruption
  (eviction-corruption analysis). Capability degrades while cost
  explodes: the anticorrelated margin from the cost accounting, now as
  the steady state rather than the exception.

For reference, the entire pre-saturation 10k-event stream costs 246M;
a single post-saturation event at the quiet mix costs 3.1M, i.e. one
event costs ~13x the entire per-event mean of the unsaturated regime.

### 1,000,000 events

- Quiet mix: ~3.1T scan steps, ~1.2M evictions.
- Not feasible under the current architecture. The system would spend
  effectively all compute on eviction bookkeeping while eviction
  destroys the procedural structures the stream is trying to build.
  This is not a performance problem; it is a regime in which the
  retention mechanism and the corruption mechanism are the same
  operation.

## 3. Bottleneck ranking

Ordered by contribution to lifetime cost in the post-saturation regime:

1. **Eviction churn** (2.5M/event/node): the dominant term by two orders
   of magnitude. Triggered by the fixed node budget, not by workload.
2. **Retrieval bookkeeping** (38k-443k per query): `bid`/`evcount`/
   `is_superseded` scans. Grows with resident facts (measured 4,352
   scan steps per fact at 100 facts; linear in occupancy against fixed
   tables).
3. **Decay tax** (4,096/event, 41M per 10k events): fixed, unconditional,
   17% of the pre-saturation budget. Small per event, inescapable in
   aggregate.
4. **Guide selection** (`act`, 61k): the most expensive single
   non-eviction operation that produces no persistent improvement.
5. **ISA execution** (~tens of opcodes per stream): negligible at every
   scale. The procedure-execution machinery is not the bottleneck and
   optimizing it changes nothing.

## 4. Fixed-table design: implementation choice, architectural consequence

The 1,024/4,096 sizes are implementation choices (constants, not
derived). But enlarging them does not fix the scaling problem; it moves
the wall:

- Every scan loop iterates over the full table size, not live
  occupancy. Doubling the tables roughly doubles per-query and
  per-event scan cost (Finding 5 of the cost accounting).
- A 10,240-node / 40,960-edge build would push saturation to ~2k-8k
  events while making every query hit cost ~380k-4.4M scans.
- Variable-size tables (grow on demand) have the same property: cost
  per operation grows with capacity, because there is no index. The
  architecture scans; it does not look up.

The fixed size is therefore not the root cause. The root cause is that
**retrieval and maintenance are linear scans over the whole workspace
with no indexing structure**, and the retention policy that rations the
fixed budget is both the most expensive operation and silently
destructive. A bigger table is a slower table that fills later.

What variable sizing would require (stated, not designed): dynamic
workspace growth, reallocation of the flat arrays, updating every
hardcoded bound (~40 sites), and it still leaves per-operation cost
linear in capacity. Indexing (per-(s,r) lookup, per-type freelists,
incremental bid maintenance) is the actual missing machinery, which is
a TNN-3 design problem.

## 5. Lifetime feasibility

The lifetime protocol (v2) envisions one continuing learner over long
experience streams with transfer, retention, and interference
measurement. Against the measured costs:

- **Maximum viable lifetime under current costs:** on the order of
  10^2 to 10^3 events before eviction churn dominates. Beyond that the
  stream is mostly paying for the privilege of forgetting destructively.
- **The decay tax alone** (41M/10k events) is affordable; it is not the
  binding constraint.
- **The binding constraints in order:** (a) node-budget saturation at
  hundreds of events; (b) eviction cost (2.5M) plus silent corruption per
  victim thereafter; (c) linear retrieval scaling against any enlarged
  table.
- **No measured operation gets cheaper with experience.** State
  dynamics found constant +1 node/+2 edge teach cost and repeated
  identical miss costs. There is no amortization: the 10,000th event
  costs at least as much as the 100th, and after saturation it costs
  ~100x more.

**Verdict on the lifetime vision under TNN-2:** the current
architecture cannot support it. The failure is not at 1M events; it is
at ~10^2-10^3, where the system enters a regime in which learning more
destroys more. This is consistent with the forgetting analysis (no
learner-owned retention), the eviction-corruption analysis (destructive
reclamation), and the state-dynamics finding (write-mostly, no
convergence). Scaling analysis adds the quantitative form: the cost
curve bends the wrong way at saturation, and saturation arrives early.

## 6. What would have to change (requirements, not design)

For a lifetime stream of 10^4+ events to be viable, the architecture
would need, at minimum:

1. **Sublinear retrieval:** per-query cost must not scan the full
   workspace. (Currently O(tablesize) per query, O(facts x edge-slots)
   for ranked retrieval.)
2. **Non-destructive, sublinear reclamation:** freeing a slot must cost
   far less than 2.5M scans and must not corrupt survivors. (Currently
   the most expensive operation is also the most destructive.)
3. **Amortization:** repeated operations must get cheaper with
   experience, or at minimum not more expensive. (Currently cost is
   constant pre-saturation and jumps ~100x at saturation.)
4. **A retention policy with a read path:** something must decide what
   is worth keeping, and that decision must be consulted. (Currently
   eight researcher-fixed criteria, zero learner-state input, per the
   forgetting analysis.)

Items 1-3 are quantitative; item 4 is the cognitive prerequisite the
other analyses establish. None is present in TNN-2.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
