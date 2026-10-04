# PREREG -- SCALING-MISSPATH: the `mp_run`/`t2_trial` MISS PATH

Lane `lane/misspath`. Base `lane/eviction` @ `ec0f54aca`. Claims C563-C572.
Pure Zag for all computation and profiling. Shell/git for orchestration only.
Every run through `tnnwatch.sh` with a limit fixed HERE, before implementation.

## 0. WHY THIS LANE EXISTS

`lane/eviction` (C555-C562) established that nodes, edges and reclamation are no
longer the binding limit and named the successor:

> "the binding limit is now the `mp_run`/`t2_trial` MISS PATH, not
> nodes/edges/reclamation."

Its next experiment, which is this lane's step 1, was: *"dedicated counter on
`ev_query -> mp_run -> t2_trial` - now the ceiling and cheapest."*

It also left two named defects that this lane must not inherit silently:

* K9a failed, so **K4 has no policy discriminator**. The consequence term sits
  in the ELIGIBILITY predicate, so the age-based control scores the same.
  `lane/eviction`'s suggested fix -- move the consequence term into the
  selection KEY so a policy that ignores the key can fail -- is step 4.
* `promote_graph`'s ownership relation omitted the MAP's own answer fact, so an
  ownership-keyed policy would have failed SILENTLY. C560 claims it is fixed;
  step 4 must VERIFY that rather than inherit it.

## 1. WHAT IS BEING MEASURED (step 1 + 2)

The miss path of `ev_query(s,r,expected,flags)` is, in source order:

```
ev_query
  activate(s,r)            -> hit? return.  MISS continues:
  rebind_try_idx | _lin    -> candidates x paths -> rb_attempt -> t2_asm_chain + t2_try_verify
  fact_top / recent link
  mp_run -> t2_trial
       t2_gather                      (paths from s, depth<=4, cap 96)
       arm A: chain k=2..4 over paths (t2_asm_chain + t2_try_verify each)
       arm B: comb_present            O(NN) arena probe
               t2_gather_sum          O(NN) arena probe, m<=12 values
               subset mask loop       for sz=m..1, for mask=(1<<m)-1..1
       arm C: t2_rels -> inc_fill     O(NN*nr) arena probe
               t2_chain per relation  -> t2_lu_first per link (indexed)
       arm D: single hop (len==2 paths)
  bootstrap_miss
  miss_inquire
```

**Dedicated counter block.** New profiler cells, all previously unused
(verified: no `padd`/`pset` anywhere in 940..1003), all additive
(`paddv`, never assigned), all reset by one function `mp_reset`:

| cell | name | incremented at |
|---|---|---|
| 940 | `mp_q_total` | entry to `ev_query` |
| 941 | `mp_q_miss` | entry to `ev_query` when `activate` returned < 0 |
| 942 | `mp_q_hit` | entry to `ev_query` when `activate` returned >= 0 |
| 943 | `mp_rebind_calls` | entry to `rebind_try_idx` / `rebind_try_lin` |
| 944 | `mp_rebind_bkt_visits` | per node visited in `idx_walk_bucket` |
| 945 | `mp_rebind_cands` | per candidate collected |
| 946 | `mp_rebind_attempts` | per `rb_attempt` call |
| 947 | `mp_rebind_accept` | `rb_attempt` returned != -2 |
| 948 | `mp_rebind_reject` | `rb_attempt` returned -2 |
| 949 | `mp_asm_chain_calls` | per `t2_asm_chain` call |
| 950 | `mp_trial_calls` | per `t2_trial` call |
| 951 | `mp_gather_calls` | per `t2_gather` call |
| 952 | `mp_gather_fact_visits` | per fact-index chain probe |
| 953 | `mp_armA_attempts` | chain k=2..4 arm, per candidate path |
| 954 | `mp_armA_accept` | ditto, accepted |
| 955 | `mp_comb_calls` / 956 `mp_comb_probes` | `comb_present` call / its O(NN) probe count |
| 957 | `mp_gsum_calls` / 958 `mp_gsum_probes` | `t2_gather_sum` call / its O(NN) probe count |
| 959 | `mp_mask_iters` | per subset-mask iteration |
| 960 | `mp_subset_asm` | per subset assembly actually attempted |
| 961 | `mp_rels_calls` | `t2_rels` call |
| 962 | `mp_chain_calls` | `t2_chain` call |
| 963 | `mp_lu_calls` | `t2_lu_first` call |
| 964 | `mp_armD_attempts` | single-hop arm candidate paths |
| 965 | `mp_boot_calls` | `bootstrap_miss` call |
| 966 | `mp_inquire_calls` | `miss_inquire` call |
| 967 | `mp_node_allocs` | **`alloc_node`/`alloc_fast` while `mp_on==1`** |
| 968 | `mp_edge_links` | **`link_edge` while `mp_on==1`** |
| 969 | `mp_evictions` | **`evict_node` while `mp_on==1`** |
| 970 | `mp_zalloc_bytes` | `z_alloc` bytes requested while `mp_on==1` |
| 971 | `mp_arena_probes` | every explicit O(NN) probe on the miss path (956+958+`inc_fill`) |
| 972 | `mp_max_cands` | max single-query candidate count (assign, reset each query) |
| 973 | `mp_alloc_fast_hits` | allocs served from the free bitmap (no eviction) |
| 974 | `mp_alloc_evict_path` | allocs that had to evict |

`mp_on` is a profiler cell (975), set to 1 at the top of the miss path of
`ev_query` and to 0 on every return out of it. It is the ONLY behavioural hook
and it changes no decision.

**Predictions, preregistered before any run.**

* **M1.** On a miss, `mp_rebind_attempts` >> 1. A single miss attempts at least
  tens of candidate graphs, and the count GROWS with the number of live MAPs.
* **M2.** `mp_node_allocs` per miss is O(attempts x plen), not O(1): the trial
  machinery allocates graph cells **before** verification and never releases
  them on rejection, so a rejected attempt LEAKS its cells. `mp_rebind_reject`
  >> `mp_rebind_accept` in every miss-heavy world.
* **M3.** `mp_arena_probes` per miss >= 2*262142 (comb_present + t2_gather_sum
  each charge a full O(NN) probe once per `t2_trial`), i.e. the miss path is at
  best O(NN) per miss regardless of how good the indices are.
* **M4.** Because of M2, `mp_evictions` per miss > 0 once the arena is
  saturated, so the miss path **feeds reclamation**, and cost per miss grows
  with the world size: a miss is O(live MAPs x paths), not O(log n).

**Kill bars / falsification.**

* **K13a FALSIFIED IF** `mp_rebind_attempts <= 4` and
  `mp_rebind_reject == 0` on the K4-world miss. Then the miss path is not
  candidate-enumeration-bound and M1/M2 are wrong.
* **K13b FALSIFIED IF** `mp_node_allocs == mp_rebind_accept * O(plen)` on a
  miss, i.e. allocations track ACCEPTED graphs. Then there is no leak and M2
  is wrong.
* **K13c FALSIFIED IF** `mp_arena_probes == 0` on a miss reaching `t2_trial`.
  Then M3 is wrong.
* **K13d (the ceiling measurement)** the miss path is **SUBLINEAR-IN-SENSITIVE**
  iff `mp_rebind_attempts` at 40000 junk MAPs is within 4x of its value at
  5000 junk MAPs. `rebind_try_idx` already walks an index, so this may pass;
  it is measured, not assumed.
* **PROCESS FAIL** if any run reports `mp_q_total == 0`, `status=EMPTY`, or a
  canary/`TOTAL_BAD` change against the pre-instrumentation binary.

## 2. CORRECTNESS BAR (charter: CORRECTNESS ALWAYS BEATS SPEED)

The instrumented binary must be **byte-identical** to the pre-instrumentation
binary on every canonical level except the new `mp_*` lines. Any change to
`scan`, `ans`, `ok`, `fails`, `live_nodes`, `live_edges`, `evictions`, or any
audit counter is a FAIL, not a finding.

## 3. RUN PLAN (all limits preregistered here, not extended later)

Build: `tools/zbuild.sh` (removes the stale binary first).

| run | what | limit |
|---|---|---|
| `mp_base_1k` | reference binary, D=1000 mode 13 phase 3 | 1500 s |
| `mp_base_20k` | reference binary, D=20000 mode 13 phase 3 | 1500 s |
| `mp_i_1k` .. `mp_i_20k` | instrumented, same args | 1500 s each |
| `mp_miss_small` | NEW phase 9: isolated miss micro-world, MISS=1, at D in {200,1000,5000} | 1500 s each |
| `mp_miss_sweep` | phase 9 at D in {10000,20000,40000}, MISS=1 | 1500 s each |
| `mp_miss_big` | phase 9 at D=100000, MISS=1 (the ceiling probe) | 1500 s |
| `mp_jf_5k` / `mp_jf_20k` | phase 4 K4 world, FAST policy, JF=5000 / 20000 | 1500 s each |

A TIMEOUT is recorded as FAIL/TIMEOUT exactly as specified and is never
re-run with a larger limit. Determinism: 3/3 byte-identical via `--rep 3`.

## 4. STEP 3 -- MAKING IT SUBLINEAR (conditional on M1/M2/M4)

If the cause is candidate enumeration with a leaking allocator, the fix is a
**transactional trial**: assemble the candidate graph, verify, and on rejection
release exactly the cells that trial allocated, through the same free-bitmap
path eviction uses. That is a CORRECTNESS-FIXING change (it stops the miss path
from destroying the world), not a speed trick, and it must leave `ans`/`scan`
byte-identical.

The brief forbids hardcoding a human ontology of index categories (charter 36).
The release predicate is therefore derived from the learner's own state only:
a cell is releasable iff it is not reachable from any live MAP root, not
licensed by any live type-1 edge, not owned by a live MAP (`own_get`), and not
in the victim index with a nonzero eligibility. Cells the trial created carry
no owner and no in-edge, so the predicate is exact for them **provided** the
trial is the only writer -- which is why the release is scoped to the trial's
own allocation list, not to a scan.

Stress battery (all mandatory, all must hold): stale entries, deletion,
revision, hash collisions, cycles in the assembled graph, malformed references,
heavy churn, adversarial insertion order. Kill bar: **0 answer changes and 0
audit regressions at every stress level**, verified against the frozen
reference answers captured in the same run.

## 5. STEP 4 -- RE-OPENING THE EVICTION DISCRIMINATOR (K9a/K4)

Move the consequence term from the eligibility predicate into the selection
KEY: `key(n) = bid(n) + LB_W * min(bid(owner(n)), CAP)`, with `LB_W` large
enough that the structural term dominates `bid`. Both arms keep the identical
eligibility set, so the ONLY difference is the key. Then:

* arm A = consequence-aware key (sel_key),
* arm B = age control (sel_lru, lowest eligible id) -- **which IGNORES the key**.

Predictions, preregistered:

* **K14a.** Under arm B at JF>=20000, `ansfact_live < 6`. This is what the
  K4 world was built to produce and the K9a run failed to produce.
* **K14b.** Under arm A, `ansfact_live == 6` and `E11FOUND total_survived == 6`.
* **K14c.** Therefore arm A beats arm B on charter 32 (RECENT-JUNK vs
  OLD-FOUNDATIONAL) and **K4 is a PASS, not INCONCLUSIVE**.
* **K14d (ownership completeness).** `promote_graph` must register the MAP's own
  answer fact under `own_add` (C560). Verified by an explicit assertion run
  BEFORE the comparison: for every live MAP with `bid(owner)>=3`, its answer
  fact has `own_get(answerfact) == map`. If that assertion fails, the K4
  comparison is reported VOID, because an ownership-keyed policy would fail
  silently -- which is the exact defect C560 was raised for.
* **K14e FALSIFIED / K4 STAYS INCONCLUSIVE IF** `ansfact_live == 6` under arm B
  as well. Reported as a failure, not reframed.

## 6. STEP 5 -- THE CEILING

50k, 100k MAPs and lifetime events (charter 35). At each level: retrieval
visits, CPU, wall, memory, nodes, edges, index size, correctness,
learning/composition/revision latency, reclamation cost, corruption, forgetting.
Before trusting any 100k number, resolve `lane/eviction`'s unresolved
`live_nodes (481432) > NN (262144)`: `e11_scan_maxnode` walks for the maximum
LIVE id while `hg(W,20)` is the live COUNT. If the two disagree the counter is
wrong, not the arena.

## 7. STEP 6 -- C267 9-phase merge test

Byte-identity against `s5000_run1.txt` sha `382e913a` under the NN=131072
rebuild, only if steps 1-5 land and time remains.

## 8. BOUNDARIES DECLARED NOW

* One host, one compiler, one corpus. The host is SHARED and heavily loaded
  (load average 5.95-46.14 observed at prereg time); all elapsed times are wall
  clock on a contended machine and are not comparable across lanes.
* Every `mp_*` number is a WORK COUNT, not a time. There is no clock builtin;
  cost is inferred from work counts plus the shell's whole-run wall clock.
* Profiler cells 940-975 are new. `TRC()` at cell 1200 aliases `DBASE`
  (offset overlap) -- a pre-existing latent defect, not introduced here, noted
  so no one reads a vtrace from a scale run as sound.
* `pget(W,99)` is never assigned anywhere in the source, so
  `is_superseded()` returns 0 unconditionally and the supersession predicate
  is currently INERT. Noted as a boundary, not fixed here.
