# SCALING-MISSPATH REPORT 2 -- the probe floor is gone, the leak is not, and the eviction discriminator has a fixture defect nobody had noticed

Lane `lane/misspath`. Claims C563-C568. Base `lane/eviction` @ `ec0f54aca`.
Pure Zag for all computation and profiling. Shell/git for orchestration only.
Every run through `tnnwatch.sh` at the preregistered 1500 s limit; no orphan
binaries left at report time (`pgrep -fl m10` shows only the two registered
watchdogs and their own children).

---

## 0. HEADLINE

1. **C564 -- `lane/eviction`'s central premise is REFUTED, by its own logs.**
   The K4 query `ev_query(1000,50,7000)` **does not miss** once the answer fact
   is alive: `mp_q_hit=1, mp_q_miss=0`, `downstream_ans=7000 ok=1`. The stall
   attributed to `mp_run`/`t2_trial` is inside **`e11_measures`**, the charter-32
   audit. Stage markers prove it.
2. **C565 -- the real miss path, profiled with a dedicated counter:** a genuine
   miss pays **524,284 unconditional O(NN) arena probes** plus **~5 leaked nodes
   per rejected candidate**, with **100% rejection** at every scale, and
   `attempts = 2 x min(D, 8192)` -- linear in the candidate set.
3. **C567 -- the probe floor is now SUBLINEAR: `arena_probes` 524,284 -> 1**, a
   524,284x reduction, with every answer, counter and audit **bit-identical**,
   `TOTAL_BAD=0`, 3/3 byte-identical determinism, and byte-identity against
   the pre-instrumentation binary on the full log at D=1000 and D=20000.
4. **C566 -- `live_nodes > NN` is RESOLVED: a counter artifact, not an arena
   overflow.** `free_ids(1) + live_scan(262,142) = 262,143 = NN-1`. The free
   bitmap has lost **zero** slots.
5. **C568 -- the K4 discriminator, run for real with the consequence term in the
   KEY. C560's ownership completeness VERIFIED (`c560_ok=1`, 0 wrong owners at
   20,006 MAPs).** Two fixture defects are found that make C553-C562's K4
   unscoreable as written; see section 5.

---

## 1. C563 -- THE INSTRUMENTATION (deliverable 1)

35 additive work counters plus one phase tag, in profiler cells 940-975, all
previously unused. `mp_on` is set the instant `activate` returns <0 and cleared
on every exit, so the allocation / edge / eviction hooks attribute cost to a
miss and to nothing else. Nothing branches on the tag.

**Byte-identity against `lane/eviction`'s unmodified `e11_prof_v2` (built as
`m10_ref`) on the FULL log, not "excluding the new lines":**

| level | diff lines |
|---|---|
| phase 3, D=1000, mode 13 | **0** |
| phase 3, D=5000, mode 13 | **0** |
| phase 3, D=20000, mode 13 | **0** |
| phase 4, JF=2000, mode 13 | **0** |

Three miss populations were separated, because conflating them is how the
ceiling was previously mis-described: **empty** (no outgoing fact), **path-
bearing** (outgoing facts, no answering MAP), **deep** (the K4 shape: a length-2
path plus a length-5 chain, so the plen-2 bucket is walked).

---

## 2. C564 -- THE PREMISE IS WRONG (deliverable 2, part 1)

Mode 13, phase 4 (K4 world), stage markers around `e11_measures` and the query:

| JF | wall | measures | query | `mp_q_hit` | `mp_q_miss` | downstream_ans | `TOTAL_BAD` |
|---|---|---|---|---|---|---|---|
| 2,000 | 2 s | begin+end | begin+end | -- | -- | 7000 ok | 0 |
| 5,000 | 4 s | begin+end | begin+end | -- | -- | 7000 ok | 0 |
| 20,000 | 40 s | begin+end | begin+end | **1** | **0** | 7000 ok | 0 |
| 40,000 | TIMEOUT 1500 s | **begin only** | never reached | -- | -- | -- | -- |
| 40,000 (rerun) | TIMEOUT 1500 s | begin+end | begin+end | 0 | **1** | -- | -- |

`E11MEAS composition=66,666,668` at JF=20,000; `232,329,486` at JF=40,000.
`e11_measures`' composition term is Theta(citations x citation-fan-in) over every
live MAP. The query it was blamed for is an O(1) indexed fact hit.

**The second JF=40,000 row is the decisive one.** There the query *did* run, as
a genuine full miss (`mp_q_miss=1`, the answer fact having been evicted), and
the whole miss path cost:

```
mp_arena_probes 524284   mp_node_allocs 5   mp_edge_links 3   mp_evictions 2
mp_rebind_attempts 0     mp_trial_calls 1    mp_lu_calls 16   mp_max_cands 0
```

**524,284 probes and 5 allocations.** That is not a 100-second stall. And
`mp_rebind_attempts=0` because the plen-2 bucket is empty -- see section 5.

Structural reason the K4 query cannot miss: `promote_graph` calls
`ev_teach_in(s,r,ans)`, so a live MAP's answer fact exists with exactly the
queried `(s,r)` and `activate` is an indexed bucket lookup. With the answer fact
alive the query is a hit; with it dead the query returns `-2` in microseconds
(`out/y_k10c.log`). **Neither state reaches a `mp_run`/`t2_trial` cost worth
naming.**

**C554's and C556's "the binding limit is the `mp_run`/`t2_trial` miss path" is
NOT SUPPORTED and is withdrawn as applied to the K4 world.** C556's "the fix
converts a fast WRONG answer into a SLOW path of unresolved cost" is likewise
withdrawn: the answer was fast and the slowness was the audit. The 1500 s
timeout at JF=40,000 is localised to *after* `query_end` (the junk-retention
loop and/or `e11_report`) and **not** localised further.

---

## 3. C565 -- WHAT THE MISS PATH ACTUALLY COSTS (deliverable 2, part 2)

### 3.1 A fixed Theta(NN) floor, independent of everything

`mp_arena_probes = 524,284` per miss at **every** world size -- exactly
`2 x 262,142`. Two full arena scans fire unconditionally inside `t2_trial`:
`comb_present` (262,142 probes: "is there ANY live tag-8 node?") and `inc_fill`
via `t2_rels` (262,142 probes: enumerate `s`'s relations). Neither is indexed,
neither depends on the query, neither can return early. `t2_gather_sum` is a
third and fires whenever `comb_present` succeeds. **K13c PASSED.**

### 3.2 Every rejected candidate leaks its graph

Phase 9, deep miss, one query: `attempts=5 rejects=5 accepts=0
node_allocs=165 edge_links=70` -- **33 nodes and 14 edges per REJECTED
candidate, zero released.** `t2_asm_chain` calls `t2_lit`/`t2_guard`/`t2_set`,
each of which calls `alloc_node`, and `t2_exec` allocates a frame; on rejection
`rb_attempt` returns -2 and **no rollback exists anywhere on the trial path**.

### 3.3 Attempts are linear in the INDEXED candidate set -- and nothing indexed

Phase 9 gave `attempts=5` at D=1,000, 5,000 and 20,000 alike. That looked like
sublinearity and it is an artifact: `e11_mkbroken` rewrites the SET cell's tag
to 103, so `rb_chain_plen` returns -1, so `idx_add` puts the MAP in **no
bucket**. Every decoy in every world built so far -- including all 40,000 in the
K4 world -- has been **invisible to the rebind index**, and the candidate set
really was constant at 5.

Phase 10 (`e11_mkdecoy`, chain intact) exposes the real curve. One deep miss:

| indexed decoys | cands | attempts | rejects | accepts | node allocs | edge links | arena probes | wall |
|---|---|---|---|---|---|---|---|---|
| 100 | 100 | 200 | 200 | **0** | 1,080 | 235 | 524,284 | <2 s |
| 500 | 500 | 1,000 | 1,000 | **0** | 5,081 | 1,035 | 524,284 | 2 s |
| 2,000 | 2,000 | 4,000 | 4,000 | **0** | 20,081 | 4,035 | 524,284 | 2 s |
| 8,000 | 8,000 | 16,000 | 16,000 | **0** | 80,081 | 16,035 | 524,284 | 5 s |
| 20,000 | **8,192 (cap)** | 16,384 | 16,384 | **0** | 82,001 | 16,419 | 524,284 | 7 s |

`attempts = 2 x min(D, 8192)`: **exactly linear, hard-capped by the `nc < 8192`
buffer bound.** `accepts = 0` everywhere. At D=20,000 one miss took the world
from 140,689 to 222,690 live nodes: **82,001 nodes, 31% of the arena, consumed
and never returned by one miss.**

**K13a FALSIFIED as literally written; K13d FAILED** (16,000 attempts at 8,000
decoys vs 200 at 100 -- 80x for 80x, not within 4x). Reported as failures.

**Saturation reproduced.** D=20,000 with NM=1 completes in 7 s; NM=2 and NM=8
both **TIMEOUT at the 1500 s limit**, and D=40,000 with NM=1 also **TIMEOUT**.
Once the arena is full, every one of the ~82,000 leaked allocations per miss
triggers an eviction. This is the ceiling, and it is the leak.

---

## 4. C567 -- MADE SUBLINEAR (deliverable 3, first half)

Three O(NN) scans on the miss path became O(1) and O(bucket):

* **`comb_present`** reads a **live-tag histogram** in O(1).
* **`t2_gather_sum`** walks the learner-maintained FACT subject bucket.
* **`inc_fill` / `t2_rels`** walks the same bucket.

### 4.1 The histogram has no ontology in it (charter 36)

The histogram is indexed by the node's **own tag field**, and it is maintained
inside `ns`, the single choke point that all 56 `ns(W,x,0,...)` call sites
funnel through. No call site is edited, and a tag nobody has ever written simply
has count 0. Every entry is a tag value the learner itself wrote.

The hook needs the allocator to publish liveness **after** the tag, because on
entry to a recycled slot the stale tag from the slot's previous life is still in
field 0 and must not be decremented. `alloc_fast` and `alloc_node` therefore
write field 0 before field 36 -- a reordering of two adjacent plain stores with
no call between them. **Verified by byte-identity on the full log, not asserted.**

### 4.2 Order is semantics, so the indexed versions reproduce it exactly

The trial promotes the FIRST candidate that verifies, so candidate-list ORDER is
semantics, not presentation. `t2_gather_sum_idx` and `inc_fill_idx` therefore
reproduce the linear versions' **ascending node id** order exactly, by
repeatedly taking the minimum qualifying id above the last one taken
(`fidx_minid`), not by walking the bucket in its natural newest-first order.

### 4.3 Result

| mode | arena probes / miss | attempts | rejects | accepts | node allocs | edge links | TOTAL_BAD | wall |
|---|---|---|---|---|---|---|---|---|
| 13 (linear) | **524,284** | 16,384 | 16,384 | 0 | 82,001 | 16,419 | 0 | 7 s |
| 77 (indexed) | **1** | 16,384 | 16,384 | 0 | 82,001 | 16,419 | 0 | 7 s |

**524,284x reduction, every behavioural counter bit-identical.** The probe tax
is gone; the linear-in-candidates leak is now the sole dominant term, which is
exactly what makes the transactional release the unambiguous next step.
`gather_fact_visits` rises 110 -> 146, the sublinear price of the bucket walks.

### 4.4 Two defects the kill bars caught, both recorded not hidden

* **C567b -- an offset collision, the same class as C555's own first bug.** The
  histogram was first placed at 43775440, chosen by arithmetic on the printed
  `E_*` constants as "the gap between `E_BCE` and `E_BMC`". That offset is
  **exactly `VBH()`**, the victim-index bucket-head array (8192 i32). The
  histogram was aliased by the bucket heads and read back as `(true count - 1)`
  in **every one** of its 1024 slots. The region actually used is
  18366656..18566848: past `EB2` (18366592+64) and before `E_INT`, which the
  source addresses as a 7 x 262144 array occupying 18566848..25906848. Verified
  by grepping every `18xxxxx`/`19xxxxx` literal in the source.
* **C567d -- a flag placed in a learner node field, rejected.** The fifth index
  bit was first added to `idx_mode`, which is a field of the tag-40 index node.
  Mode bit 3 already selects the FAST eviction policy in the driver, so this
  changed the stored value and the log printed `idxmode=13` instead of
  `idxmode=5`. The flag moved to header cell 930. This is C551's lesson applied
  to myself: state the engine reads back belongs in the arena only if the
  learner wrote it.

### 4.5 Determinism and equivalence

* **3/3 byte-identical**, sha `7264db5e1b283b8920e0a30a389c96ad00e61f2f591f3bf0bb7345b758f793d0`,
  at D=20,000 mode 77 phase 10.
* Equivalence kill bar (phase 11, 2,030 keys): `comb` boolean agrees,
  `gsum_bad=0`, `rels_bad=0`, `rels_max=2`, `rels_over16=0`.
* **UNRESOLVED, reported as a failure of the bar:** `tag_ok=0`. The histogram
  **total** is exact (`tag_sum=7801 = live_scan=7801`) and every tag with a
  population >= 20 matches its from-scratch count exactly, but one tag is short
  by 1 and tag 900 carries a phantom +1 -- the two `tnn2_init` sentinel nodes
  (ids 0, 1, tags 900/901) created by raw `ns()` calls that bypass the
  allocator. I fixed the sentinel order (tag before liveness) and the residual
  persisted, so I did not isolate it further. It does **not** affect the
  kill-barred predicate (`comb_present` vs the linear scan, which agrees), but
  `tag_ok` is the bar and it is not green.

---

## 5. C568 -- THE EVICTION DISCRIMINATOR (deliverable 4)

`lane/eviction` suggested moving the consequence term from eligibility into the
selection key. Done:

* **arm A** = `sel_key`: `key(n) = bid(n) + LB_W * min(bid(owner(n)),CAP)`,
  selecting ownerless-eligible first. **arm B** = `evict_lru`: lowest eligible
  id, **ignoring the key entirely**. Identical eligible set, identical kill path.
  `vre` is **not** modified: the term is in the key only, never in eligibility.
* `LB_W` is derived (the `bid >= 3` threshold is derived too: `promote_graph`
  gives every MAP type-2 and type-6 self-edges, so an uncited MAP's bid is
  exactly 2 and ">= 3" IS "cited at least once").

### 5.1 K14d -- C560's ownership completeness: VERIFIED, not inherited

The mission asked whether C560's fix landed, because if it did not, every
ownership-keyed comparison fails silently. `own_assert` checks, for **every**
live MAP, whether the fact holding its answer is owned by it -- run BEFORE any
junk exists and again after:

```
E11OWNASSERT maps=6      ansfact_wrong_owner=0 first_bad_map=-1 c560_ok=1
E11OWNASSERT maps=5006   ansfact_wrong_owner=0 first_bad_map=-1 c560_ok=1
E11OWNASSERT maps=20006  ansfact_wrong_owner=0 first_bad_map=-1 c560_ok=1
```

**C560 is real and complete.** The precondition for scoring K4 holds.

### 5.2 TWO FIXTURE DEFECTS that make C553-C562's K4 unscoreable as written

**(a) The decoys were never in the index.** `e11_mkbroken` sets the SET cell's
tag to 103, so `rb_chain_plen` returns -1 and `idx_add` files the MAP in no
bucket. The victim population the K4 policy chooses between was therefore the
**6 foundational MAPs**, not 40,000. C553 built broken decoys and C554/C556
measured policies over 6 nodes and reported it as a policy comparison. This is
the same finding as section 3.3, reached independently from the K4 side.

**(b) No eviction pressure at the scales tested.** Rebuilding the decoys
unbroken (`e11_mkdecoy`) raises node cost to ~7/MAP, so at JF=20,000 only
140,816 of 262,144 nodes are live: **`evictions=0`**, and the two arms are
bit-identical (both `ansfact_live 6/6`, `total_survived 6/6`,
`downstream_ans=7000 ok=1`, `junk_retention=32/32`, at JF=5,000 and JF=20,000).
A test with zero evictions cannot discriminate a policy. The old broken decoys
reached eviction pressure at JF=20,000 only because they were 3 nodes cheaper
each AND invisible to the index -- two errors partly cancelling.

### 5.3 The arms at real pressure

JF=40,000 unbroken (281k live nodes > NN) with arm A and arm B: **see section 7
-- both runs TIMEOUT at the preregistered 1500 s limit under host load average
59.5, so K14a/K14b/K14c are NOT ESTABLISHED.** Reported as not established. The
runs were left registered, not extended, and no orphan survived them.

### 5.4 A defect in my own key derivation, found and FIXED (C568e)

`LB_W` was `bid_max()+1`, but `bid_max()` reads `VBH()+32776`, which `bidx()`
maintains as the largest bid **bucketed so far** -- 2 at setup -- so `LB_W` came
out as **3**, while the foundational MAPs reach bid 6,224. "LB_W dominates bid"
was therefore **false as built**, and the printed `LB_W=3` said so.

Fixed to `6*NE+1 = 1,572,865`, which dominates any bid reachable (`bid_ref`
sums five edge-type in-degrees, each at most NE); verified in the log as
`LB_W=1572865`. `sel_key` does not read the weight -- it walks ownerless-first
regardless -- so **no measurement in this report is affected**; only the
derivation is now true. Byte-identity re-verified after the change.

---

## 6. C566 -- `live_nodes > NN` RESOLVED

`lane/eviction` left `live_nodes (481,432) > NN (262,144)` unresolved and
warned that no 100k number could be trusted until it was settled. Settled by
counting the free bitmap directly:

```
free_ids=1  live_nodes_scan=262142  free_plus_live=262143  nn=262144
lost_slots=-1  lost_per_eviction_x1000=0
live_nodes_counter=271415  counter_minus_scan=9273  evictions=9274
live_tag3_hist=0  live_tag1_fact=75501  live_tag20_map=38675  live_tag40_idx=684
live_tag102=36820  live_tag101=36821  live_tag902_frame=73641
c_alloc_fast=271415  c_alloc_evictpath=9274  c_evkill=9274  c_evscan_kill=0
```

* **The free bitmap has lost ZERO slots.** `free + live = NN - 1`. The arena is
  consistent and full, not over-full.
* **`live_nodes` is inflated by exactly `evictions - 1`,** and the drift is
  unbounded: 9,273 at 9,274 evictions, so ~1.26M against a 262,144 arena at 1M
  lifetime events.
* So `481,432 > NN` is **not** an arena overflow, 100k numbers are not
  invalidated by it, and `live_nodes` must not be used as an occupancy or
  capacity measure. Use `live_nodes_scan` and `free_ids`.
* **Not isolated:** I did not determine which of the two `+1` sites carries the
  extra increment. The identity that does hold is printed as `identity_ok=1`;
  the residual is stated, not explained away.

---

## 7. VERDICT

* **Deliverable 1 (instrument): DONE.** Dedicated `ev_query -> mp_run ->
  t2_trial` counters, byte-identical to the pre-instrumentation binary.
* **Deliverable 2 (characterise): DONE, and the premise refuted.** A miss costs
  `2 x NN` probes plus ~5 leaked nodes per rejected candidate, `2 x min(D,8192)`
  attempts, 0% acceptance.
* **Deliverable 3 (sublinear): HALF DONE.** The `2 x NN` probe floor is
  **sublinear: 524,284 -> 1**, kill-barred and bit-identical. The
  `Theta(candidates x plen)` **leak is NOT fixed** and is now the sole binding
  term. This is reported as a partial pass, not a pass.
* **Deliverable 4 (K4 discriminator): PRECONDITION MET, VERDICT NOT
  ESTABLISHED.** C560 verified. Two fixture defects found that make the
  historical K4 unscoreable as written. The decisive runs timed out at the
  preregistered limit under load average 59.5.
* **Deliverable 5 (ceiling): NOT REACHED.** The ceiling is now named and
  measured -- it is the trial leak, not nodes, edges, reclamation, or the miss
  path's probes -- but 50k/100k were not run.
* **Deliverable 6 (C267 9-phase merge test): NOT ATTEMPTED.**

## 8. BOUNDARIES

* Work counts, not times: there is no clock builtin. Wall clock is the
  watchdog's whole-run elapsed on a host at load average 5.9-59.5.
* Four runs TIMEOUT at 1500 s and are reported as TIMEOUT, never as results:
  `cnd20k_nm2`, `cnd20k_nm8`, `cnd40k_nm1` (phase 10 saturation), and
  `jf_40000` / `k4b_40000_a3` / `k4b_40000_a2` (40,000 levels).
* One foreground `$W reg` was lost to the 120 s shell limit (the documented
  darwin hazard: no `setsid`). That run is VOID and was relaunched detached.
* Two earlier placements of the C568 helper block were rejected by the compiler
  for being defined after their caller: Zag is concatenated with no forward
  declarations, so a forward reference is a COMPILE FAILURE. A third was
  rejected because `LB_W()` used `W` without taking it as a parameter.
* `pget(W,99)` is never assigned, so `is_superseded()` returns 0
  unconditionally and the supersession predicate is INERT. Pre-existing.
* `TRC()` (cell 1200) aliases `DBASE`. Pre-existing.
* `e11_measures` superlinearity is characterised only as
  `composition = 6.7e7 at JF=20k, 2.3e8 at JF=40k` plus a non-termination; the
  exact inner term was not isolated.
* `tag_ok=0` (section 4.5). One tag short by 1, one phantom +1, total exact.
* One host, one compiler, one corpus.

## 9. NEXT EXPERIMENT

1. **Transactional trial release.** On rejection, return exactly the cells that
   trial allocated, through the same free-bitmap path eviction uses, scoped to
   the trial's own allocation list. This is the binding term and the fix is
   correctness-fixing (it stops a miss from destroying the world), not a speed
   trick. It must leave `ans`/`scan` byte-identical, and it carries the whole
   stress battery: stale entries, deletion, revision, collisions, cycles,
   malformed references, heavy churn, adversarial insertion order, with 0 answer
   changes and 0 audit regressions at every level.
2. **Re-run K14a/b/c at a scale that actually evicts** (`LB_W` is fixed to
   `6*NE+1` in C568e, so the key's dominance argument now holds). `e11_mkdecoy` costs ~7
   nodes/MAP, so the first evicting level is JF ~ 37,000; the historical
   `e11_mkbroken` fixture reached pressure only because it was simultaneously
   invisible to the index.
3. **Characterise `e11_measures`** so the 40,000 stall is attributable rather
   than merely localised to "after `query_end`".
4. **Re-measure the ceiling** with `live_nodes_scan`, then 50k and 100k.
5. The **C267 9-phase merge test** was not done here.
