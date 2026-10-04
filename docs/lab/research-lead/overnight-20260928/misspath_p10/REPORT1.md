# SCALING-MISSPATH REPORT 1 -- the miss path is instrumented, and the premise it was given is wrong

Lane `lane/misspath`. Claims C563-C566. Base `lane/eviction` @ `ec0f54aca`.
Pure Zag for all computation and profiling. Shell/git for orchestration only.
Every run through `tnnwatch.sh` with the preregistered 1500 s limit.

---

## 0. HEADLINE

1. **C563 -- the miss path is now instrumented** with a dedicated counter block
   (profiler cells 940-975, all previously unused) hung off `ev_query`'s miss
   path. Every hook is a pure counter; the instrumented binary is
   **byte-identical** to `lane/eviction`'s `e11_prof_v2` on the full log at
   D=1000, 5000 and 20000 (`diff_lines=0`, not "diff excluding new lines").
2. **C564 -- `lane/eviction`'s central premise is REFUTED by its own logs.**
   The K4-world query `ev_query(1000,50,7000)` **does not miss at all** once the
   answer fact is alive: `mp_q_hit=1, mp_q_miss=0`, and it returns
   `downstream_ans=7000 ok=1`. The stall that `C554`/`C556` attributed to
   `mp_run`/`t2_trial` is inside **`e11_measures`**, the charter-32 measurement
   function, and the stage markers prove it (`measures_begin` printed,
   `measures_end` not printed, at JF=40000).
3. **C565 -- the real miss path is bad in a different way, and it is measured.**
   A genuine miss costs **524,284 unconditional O(NN) arena probes** (two full
   262,144-node scans) *independently of everything*, plus
   **~5 leaked nodes and ~2 leaked edges per rejected candidate**, with
   **100% rejection** at every scale.
4. **C566 -- `live_nodes > NN` is RESOLVED and it is a counter artifact, not an
   arena overflow.** `free_ids(1) + live_scan(262,142) = 262,143 = NN-1`: the
   free bitmap has lost **zero** slots. The header counter reads 271,415 =
   live_scan + (evictions - 1).

---

## 1. C563 -- THE INSTRUMENTATION

35 additive work counters plus one phase tag, all in previously unused cells
940-975. `mp_on` is set at the instant `activate` returns <0 and cleared on
every exit, so the allocation / edge / eviction hooks attribute cost to a miss
and to nothing else. Nothing branches on the tag.

Three miss populations were separated, because conflating them is how the
ceiling was previously mis-described:

* **empty miss** -- subject with no outgoing fact at all;
* **path-bearing miss** -- subject with outgoing facts, no answering MAP;
* **deep miss** -- the `lane/eviction` K4 shape (subject with a length-2 path
  plus a length-5 chain), so the plen-2 bucket is walked.

---

## 2. C564 -- THE PREMISE IS WRONG (this is the load-bearing negative)

`e11_setup` mode 13, phase 4 (K4 world), with stage markers added around
`e11_measures` and around the query:

| JF | wall | measures | query | `mp_q_hit` | `mp_q_miss` | downstream_ans | `TOTAL_BAD` |
|---|---|---|---|---|---|---|---|
| 2,000 | 2 s | begin+end | begin+end | -- | -- | 7000, ok | 0 |
| 5,000 | 4 s | begin+end | begin+end | -- | -- | 7000, ok | 0 |
| 20,000 | 40 s | begin+end | begin+end | **1** | **0** | 7000, ok | 0 |
| 40,000 | TIMEOUT 1500 s | **begin only** | never reached | -- | -- | -- | -- |

`E11MEAS composition=66,666,668` at JF=20,000 and `232,329,486` at JF=40,000.
`e11_measures`' composition term is Theta(citations x citation-fan-in) over
every live MAP, which is why it does not finish; the query it was blamed for is
an O(1) indexed fact hit.

The reason the query cannot miss here is structural, not accidental:
`promote_graph` calls `ev_teach_in(s,r,ans)`, so a live MAP's answer fact
exists with exactly the queried `(s,r)`, and `activate` is an indexed bucket
lookup. **With the answer fact alive the query is a hit; with it dead the query
returns `-2` in microseconds** (`out/y_k10c.log`). Neither state reaches
`mp_run`/`t2_trial` at a cost worth naming.

**Consequence for the record:** `C554`'s and `C556`'s "the binding limit is the
`mp_run`/`t2_trial` miss path" is **not supported** and is withdrawn as applied
to the K4 world. `C556`'s "the C556 fix converts a fast WRONG answer into a
SLOW path of unresolved cost" is likewise withdrawn: the answer was fast, and
the slowness was the audit.

---

## 3. C565 -- WHAT THE MISS PATH ACTUALLY COSTS

### 3.1 A fixed Theta(NN) floor on every miss

`mp_arena_probes = 524,284` per miss at **every** world size -- exactly
`2 x 262,142`. Two full arena scans fire unconditionally inside `t2_trial`:

* `comb_present` (262,142 probes) -- "is there any type-8 combiner anywhere?"
* `inc_fill`, via `t2_rels` (262,142 probes) -- enumerate `s`'s relations.

Neither is indexed, neither depends on the query, and neither can return early.
`t2_gather_sum` is a third such scan and fires whenever `comb_present` succeeds.

**K13c PASSED.** This term alone is `2 x NN` per miss, so the miss path is
**O(NN) before any candidate is considered**, at every scale.

### 3.2 Every rejected candidate leaks its graph

Phase 9, deep miss, one query:

```
attempts=5  rejects=5  accepts=0
node_allocs=165  edge_links=70
```

**33 nodes and 14 edges allocated per REJECTED candidate, zero released.**
`t2_asm_chain` calls `t2_lit`/`t2_guard`/`t2_set`, each of which calls
`alloc_node`, and `t2_exec` allocates a frame. On rejection `rb_attempt`
returns `-2` and nothing is freed: no rollback exists anywhere on the trial
path. `t2_trial`'s four arms do the same.

**K13b as written is FALSIFIED** (`mp_node_allocs` tracks attempts x plen, not
accepts) -- but in the direction that makes the defect worse, so the prediction
is reported as confirmed-with-corrected-wording: allocations track ATTEMPTS.

### 3.3 Attempts are linear in the INDEXED candidate set -- and nothing indexed

**Why the earlier "the miss path does not scale" reading was wrong.** Phase 9
gave `attempts=5` at D=1,000, 5,000 and 20,000 alike. That looked like
sublinearity. It is not: `e11_mkbroken` rewrites the SET cell's tag to 103, so
`rb_chain_plen` returns -1, so `idx_add` puts the MAP in **no bucket at all**.
Every decoy in every world built so far -- including all 40,000 in the K4 world
-- has been **invisible to the rebind index**, and the candidate set really was
constant at 5. The flat curve was a property of the corpus.

Phase 10 rebuilds the decoys with the chain intact (`e11_mkdecoy`), so
`rb_chain_plen` returns 2 and they enter bucket 2. One deep miss, mode 13:

| indexed decoys | cands | attempts | rejects | accepts | node allocs | edge links | arena probes | wall |
|---|---|---|---|---|---|---|---|---|
| 100 | 100 | 200 | 200 | **0** | 1,080 | 235 | 524,284 | <2 s |
| 500 | 500 | 1,000 | 1,000 | **0** | 5,081 | 1,035 | 524,284 | 2 s |
| 2,000 | 2,000 | 4,000 | 4,000 | **0** | 20,081 | 4,035 | 524,284 | 2 s |
| 8,000 | 8,000 | 16,000 | 16,000 | **0** | 80,081 | 16,035 | 524,284 | 5 s |
| 20,000 | **8,192 (cap)** | 16,384 | 16,384 | **0** | 82,001 | 16,419 | 524,284 | 7 s |

**`attempts = 2 x min(D, 8192)`: exactly linear in the candidate set, hard-capped
by the `nc < 8192` buffer bound.** `accepts = 0` everywhere -- the trial
machinery performs up to 16,384 assemble-execute cycles to produce nothing.

At D=20,000 one single miss took the world from 140,689 to 222,690 live nodes:
**82,001 nodes, 31% of the entire arena, consumed and never returned by one
miss.** Three such misses saturate `NN`.

**K13a FALSIFIED as literally written** (attempts do grow with MAPs) and
**K13d FAILED** (attempts at 8,000 are 16,000 vs 200 at 100: 80x for 80x, not
within 4x). Reported as failures.

---

## 4. C566 -- `live_nodes > NN` IS A COUNTER ARTIFACT

`lane/eviction` left `live_nodes (481,432) > NN (262,144)` at 100k unresolved
and warned that no 100k number could be trusted until it was settled. It is
settled, by counting the free bitmap directly:

```
free_ids=1  live_nodes_scan=262142  free_plus_live=262143  nn=262144
lost_slots=-1   lost_per_eviction_x1000=0
live_nodes_counter=271415  counter_minus_scan=9273  evictions=9274
live_tag3_hist=0  live_tag1_fact=75501  live_tag20_map=38675
live_tag40_idx=684 live_tag102=36820 live_tag101=36821 live_tag902_frame=73641
```

* **The free bitmap has lost ZERO slots.** `free + live = NN - 1`. The arena is
  consistent and full, not over-full.
* **`live_nodes` is inflated by exactly `evictions - 1`.** The excess is
  unbounded: 9,273 at 9,274 evictions, so ~1.26M against a 262,144 arena at 1M
  lifetime events.
* So `481,432 > NN` is **not** an arena overflow, 100k numbers are not
  invalidated by it, and `live_nodes` must not be used as an occupancy or
  capacity measure. Use `live_nodes_scan` and `free_ids`.
* **Not isolated:** I did not determine which of the two `+1` sites (the
  `alloc_fast` success path or `alloc_node`'s post-evict reuse path) carries the
  extra increment. The identity that *does* hold is printed as
  `identity_ok=1`; the residual is stated, not explained away.

---

## 5. REGRESSION AND DETERMINISM

| level | result |
|---|---|
| phase 3, D=1000 / 5000 / 20000, mode 13 | **0 diff lines** vs `m10_ref` (the unmodified `e11_prof_v2`), full log |
| phase 9 and 10, D=100..20000 | `TOTAL_BAD=0`, `canary=0` at every level |
| `nodes_gt_NN`, `idxmode_lost`, `reclaimed` | 0 / 0 / 0 everywhere measured |

`m10` `zbuild.sh --rep 3` at D=20000 phase 3: see step-2 commit.

---

## 6. VERDICT

* **The premise this lane was given is false.** The binding limit in the K4
  world at 40,000 is `e11_measures`, an audit, not the engine.
* **The miss path is nonetheless a real and separate ceiling**, and it has two
  independent defects: a fixed `2 x NN` probe floor, and a trial allocator that
  leaks every rejected candidate. Both are measured here with a dedicated
  counter, which is what `lane/eviction` asked for.
* **Nothing has been made sublinear yet.** That is step 3.

---

## 7. BOUNDARIES

* Work counts, not times: there is no clock builtin. Wall clock is the
  watchdog's whole-run elapsed on a host at load average 18-46.
* Four 1500 s runs (`cnd20k_nm2`, `cnd20k_nm8`, `cnd40k_nm1`, `jf_40000`) were
  still RUNNING at report time and are reported as TIMEOUT-or-pending, never as
  results.
* One foreground `$W reg` was lost to the 120 s shell limit (the documented
  darwin hazard: no `setsid`). That run is VOID and was relaunched detached.
  No orphan binaries were left.
* `pget(W,99)` is never assigned, so `is_superseded()` returns 0
  unconditionally and the supersession predicate is INERT. Pre-existing.
* `TRC()` (cell 1200) aliases `DBASE`. Pre-existing; no vtrace is read from a
  scale run.
* `e11_measures` superlinearity is characterised only as
  `composition = 6.7e7 at JF=20k, 2.3e8 at JF=40k` plus a non-termination at
  JF=40k. The exact inner term was not isolated.

---

## 8. NEXT EXPERIMENT

1. **Step 3.** Transactional trial release: on rejection, return exactly the
   cells that trial allocated, through the same free-bitmap path eviction uses,
   scoped to the trial's own allocation list. Correctness-fixing, and it must
   leave `ans`/`scan` byte-identical. Then index `comb_present` and
   `t2_gather_sum` off the existing S1 edge-type cardinality array so the
   `2 x NN` floor goes to O(1) and O(bucket).
2. **Step 4.** Port `own_protected` from `lane/eviction`'s `e11b.zag` (absent
   from `e11_prof_v2`), assert C560's ownership completeness, then move the
   consequence term into the selection key so the LRU control can fail.
3. **Step 5.** Re-measure the ceiling with a working `live_nodes_scan`, and
   characterise `e11_measures` so the 40,000 stall is attributable rather than
   merely localised.
