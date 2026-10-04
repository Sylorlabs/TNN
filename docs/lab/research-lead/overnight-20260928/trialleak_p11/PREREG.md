# SCALING-TRIALLEAK PREREG — C700-C7xx

Lane `lane/trialleak`. Base `lane/misspath` @ `eeefbc263` (merged).
Pure Zag for all computation and profiling. Shell/git for orchestration only.
Every run through `tnnwatch.sh` at a preregistered limit; detached via `wrun.sh`
(the darwin `setsid` hazard documented in `misspath_p10/wrun.sh`).

Engine under test: `misspath_p10/m10.zag` copied verbatim to
`trialleak_p11/t11_ctl.zag` (CONTROL, never edited) and to `trialleak_p11/t11.zag`
(FIX). Control and fix are built from the same tree on the same host.

---

## 0. THE INHERITED FINDING

`lane/misspath` C565/REPORT2 §3.2, verbatim:

> Every REJECTED candidate LEAKS its graph: 33 nodes and 14 edges, zero
> released. ... `t2_asm_chain` calls `t2_lit`/`t2_guard`/`t2_set`, each of
> which calls `alloc_node`, and `t2_exec` allocates a frame; on rejection
> `rb_attempt` returns -2 and **no rollback exists anywhere on the trial
> path**.

Their own scaling table gives `node_allocs 82001 / edge_links 16419` for
`attempts 16384`, i.e. **5.005 nodes and 1.002 edges per rejected candidate**,
not 33 and 14. So the two figures in their report are for two different worlds
and the headline figure was never shown to be a constant. **DETERMINING WHICH IS
THE TRUE CHARACTERISATION IS DELIVERABLE 1 AND IS FALSIFIABLE HERE.**

---

## 1. DELIVERABLE 1 — CHARACTERISE THE LEAK PRECISELY (K-LC)

Instrument `alloc_fast`, `alloc_node`'s evict path, `alloc_raw`'s success and
`link_edge` to append `(gen, kind, id)` to a transaction log, and additionally
classify each trial allocation by the node tag the assembler wrote
(902 literal, 101 MOVE/SETREG, 102 BEQ/guard, 103 INC, 1 FACT, 20 MAP, 40 IDX,
902 FRAME) and each trial edge by `eg(e,4)`.

Report, per rejected candidate, **separately for each of the 5 assembly sites**
(`t2_trial` k=2/3/4 chain, `t2_trial` sum, `t2_trial` count, `t2_trial` single-hop
fallback, `rb_attempt` chain):

| quantity | field |
|---|---|
| `plen` (candidates in the graph) | — |
| nodes by tag class | 7 counters |
| edges by type (1 DEP, 12 SEQ) | 2 counters |
| total nodes / total edges released | 2 counters |

### Falsifiable predictions (P1-P3)

* **P1.** The leak is **NOT a constant**. For a chain candidate of `plen` nodes
  assembled by `t2_asm_chain` and executed by `t2_exec`, the leak is exactly
  `4*(plen-1) + 1` nodes and `2*(plen-1) - 1` edges — 2 literals + 1 guard +
  1 set per link, plus the frame; 1 DEP edge per link plus 1 SEQ edge per
  subsequent link. P1 predicts `plen=2 -> 5 nodes / 1 edge`, `plen=3 -> 9/3`,
  `plen=4 -> 13/5`, `plen=5 -> 17/7`.
* **P2.** The published "33 nodes and 14 edges" is an **average over a mixed
  shape set**, not a per-candidate constant, and is therefore not the number a
  fix has to move. P2 predicts that no single candidate in any world leaks 33
  nodes, and that the ratio `nodes/edges` for a chain candidate is
  `(4(p-1)+1)/(2(p-1)-1)`, i.e. 5.0 at `p=2` falling to 2.43 at `p=5`, never
  33/14 = 2.357 for any integer `p >= 2`. **P2 predicts the 33/14 figure is
  unreproducible as a single candidate and is an artefact of summing several
  candidates of different `plen`.**
* **P3.** `t2_asm_count` (the `di` rebind arm) leaks **one extra INC cell and
  one extra MOVE cell and 2 extra SEQ edges** relative to `t2_asm_chain` at the
  same `plen`, because it adds `t2_inc` per link plus a `t2_mov` epilogue.
  P3 predicts `plen=2 -> 7 nodes / 3 edges`, `plen=5 -> 22/12`.
* **P4.** `t2_asm_sum` leaks exactly `total` INC nodes and `0` edges, and
  `total` is chosen by the assembler, not by the arena — so its leak is **not a
  function of the candidate's path length** and is the one place where the
  per-candidate cost is attacker/corpus-controlled.

Any of P1-P4 falsified ⇒ report the falsification, do not adjust the design to
fit.

### K-LC kill bar
The instrumented build must be **byte-identical to the control on the full log
at phase 3 D=1000 mode 13 and phase 3 D=5000 mode 13** (0 diff lines), and
3/3 deterministic. Instrumentation that changes an answer is not an
instrumentation.

---

## 2. DELIVERABLE 2 — TRANSACTIONAL TRIAL RELEASE (K-TX)

### 2.1 Ownership marker: a trial GENERATION LOG, not an address range

The arena node record is `noff(n)=64+n*40`, i.e. exactly 10 i32 fields
(0 tag, 4/8/12/16/20/24/28/32 payload, 36 liveness) — **there is no free node
field to stamp**, so a per-node generation stamp is not available without
changing the frozen record layout, which is forbidden. Ownership is therefore
recorded in a **transaction log** that the allocator itself appends to:

```
TX log region  E_TX()  (new, appended past the old arena end; the canary and
                        TOT() move with it, no existing region is aliased)
  +0   cur generation            (monotone, +1 per txn_open)
  +1   entry count               (grows within a txn, reset at open)
  +2   open depth                (nesting)
  +4..+35  savepoint stack       (entry count at each nested open)
  K[]   kind   (0 = node, 1 = edge)
  G[]   generation of the owning trial
  V[]   id
```

**Ownership is `G[i] == cur_generation`.** Release never inspects an address
range, never inspects a tag to guess, and never frees an id that is not in this
transaction's log under this transaction's generation. A stale entry from an
earlier, already-committed generation is therefore unreleasable by construction
— that is the property that makes "blanket free everything" impossible.

Hooks (pure appends, no branch on any engine decision):
* `alloc_fast` on success, `alloc_node` on its evict-path success,
  `alloc_raw` on success → `txn_mark(W,0,id)`
* `link_edge` on success → `txn_mark(W,1,id)`

An append is a no-op when `open depth == 0`, so **every allocation outside a
trial costs one load and one compare** and is bit-identical to the control.

### 2.2 Nested trials

`txn_open` pushes the current entry count onto the savepoint stack and
increments the generation. `txn_commit` pops (the log entries are kept, the
count is truncated to the savepoint so a later sibling transaction cannot
inherit them). `txn_roll` releases entries strictly above the savepoint whose
generation equals the current one, then truncates. Depth is capped at 32 and
overflow is counted, never silent.

### 2.3 Release, in LIFO order

1. **edges first**, in reverse creation order: `edge_del(W,e)` — the engine's
   own, existing, symmetrical release path. It performs `inset` decrement,
   `bid` un-adjustment, `il_del`, `ev_del`, `t9_del`/`mem_del`,
   `ev`-type cardinality decrement, live-edge decrement and the free-bitmap
   store. Nothing new is written.
2. **then nodes**, in reverse creation order: delete any residual incident edge
   (defensive; a well-formed trial has none), `vdrop` from the victim index,
   `ns(n,36,0)` (which is the only place the live-tag histogram is
   decremented), `hs(20, hg(20)-1)`, then `fb_set(NB0,NB1,NB2,n,1)`.
   `rec_evict` is deliberately **not** called: a trial cell that never became
   learner state has no history to record, and calling it would allocate inside
   the transaction it is rolling back.

### 2.4 Commit conditions — what must NOT be freed

A candidate's allocations are **committed, not released**, when `t2_try_verify`
returns anything other than -2. In that case `promote_graph(root,...)` has
already adopted the whole graph into a MAP, including the DEP provenance edges
and the licensing facts. `txn_commit` is called and nothing is touched.

`txn_open`/`commit`/`roll` are placed around **all five** assembly sites in
`t2_trial` **and** around `rb_attempt`, because `rb_attempt` is where 16384 of
the 16384 measured attempts occur.

**Pre-registered claim C701:** of everything a rejected trial allocates,
**exactly one thing is deliberately retained, and it is not inside the trial's
own allocation list** — the pre-existing licensing `FACT` node that the trial's
DEP edges point at. It is not allocated by the trial, it is not in the log, and
a blanket "free everything reachable from the candidate" would destroy it and
with it every promoted MAP that cites it. The trial's own list contains nothing
else that is retained, because nothing outside the transaction ever holds a
reference to it. **C701 is falsified** if the battery finds a released id that
some live promoted structure still references, or a promoted structure that
stops verifying after a rollback.

---

## 3. DELIVERABLE 3 — THE HARD CONSTRAINT (K-BYTE), PREREGISTERED AS A KILL BAR

> **The fix may not change any observable answer. `ans` and `scan` must be BYTE
> IDENTICAL between `t11_ctl` and `t11` at every preregistered configuration.**

* `scan` = `hg(W,56)`, the number of rebind candidate visits.
* `ans` = the value returned by `ev_query`, printed on every `E11DUMP` line.

Configurations (all mode 13 unless stated, all through the watchdog):

| id | phase | D | mode | note |
|---|---|---|---|---|
| C1 | 3 | 1000 | 13 | canonical small |
| C2 | 3 | 5000 | 13 | the 5000-MAP canonical, ans=6205/6405 scan=5/6 |
| C3 | 7 | – | – | selftest, raw query values |
| C4 | 9 | 1000 | 77 | deep miss, broken decoys |
| C5 | 9 | 20000 | 77 | deep miss, 20k broken decoys |
| C6 | 10 | 1000 | 77 | indexed decoys |
| C7 | 10 | 20000 | 77 | the 82001-node leak |
| C8 | 12 | 20000 | 77 | K4 discriminator world, `downstream_ans` |

**K-BYTE is scoped to `ans`, `scan`, `last_ans`, `downstream_ans`, `total_survived`,
`ansfact_live`, `junk_retention`, `TOTAL_BAD`, `canary`, `ns_viol`, `ns_dirty`,
`c560_ok` and every `ev_query` return value.** These are the observable answers
and the integrity counters.

**K-BYTE is NOT scoped to** `live_nodes`, `live_edges`, the live-tag
histogram, `evictions`, `reclaimed`, `sel_visits`, `mp_node_allocs`,
`mp_edge_links`, or any line whose entire content is "how much arena is
occupied". Those MUST change — that is the fix. A leak fix that does not move
them has not fixed the leak, and a run where they do not move is reported as
**FAIL-TO-IMPLEMENT**, not as a pass.

**K-COUNT (behavioural invariance), same table:** `attempts`, `rejects`,
`accepts`, `cands`, `max_cands`, `chain_calls`, `rels_calls`, `lu_calls`,
`gather_calls`, `gather_fact_visits`, `tried_tot`, `rejected_tot`, `comb_calls`
must be **bit identical**. The fix changes reclamation, never search.

**If any K-BYTE or K-COUNT value differs, the run is a FAIL and the difference
is REPORTED as a discovery about hidden state dependence. It is not tuned away
and the bar is not moved.**

### K3 — no new integrity violations
`TOTAL_BAD = 0`, `canary = 0`, `ns_viol` and `ns_dirty` equal to the control's
values, at every configuration. A reclamation fix that raises an integrity
counter is a FAIL.

### K5 — reclamation accounting, exact
At zero evictions:
`released_nodes_total + live_nodes_fix == live_nodes_control` and
`released_edges_total + live_edges_fix == live_edges_control`, exactly.
`lost_slots == 0` (the free bitmap loses no slot), `double_free == 0`,
`foreign_free == 0` (no id released that was not in the log under the current
generation), `stale_free == 0`.

### K8 — determinism
3/3 byte-identical stdout at C2 and C7.

---

## 4. DELIVERABLE 4 — THE STRESS BATTERY (K-STRESS), CHARTER 38

Charter 38: *reclamation must act on MEANINGFUL STRUCTURES and must not delete
shared structure because one owner disappeared.* Eight cases, each green only if
**0 answers change, 0 promoted structures stop verifying, 0 integrity
violations, and the released set is exactly the transaction's own allocation
list**:

| id | case | what it attacks |
|---|---|---|
| S1 | **shared subgraph** | two promoted MAPs whose graphs cite the SAME licensing facts; roll back many trials against them; the facts' `inset` counts, `bid`, incident lists and both MAPs' stored answers must be exactly as before |
| S2 | **cycles** | a trial whose graph is re-entered (self-loop SEQ) so `execute` walks a cycle; the rollback must terminate and release every node exactly once (`double_free==0`) |
| S3 | **version history** | the tag-3 `HISTORY` chain (`hg(W,12)`) built by `rec_evict`; rollback must not append to it, must not truncate it, and a graph whose history records an evicted node must still verify |
| S4 | **provenance** | `t2_revise_graph`'s DEP walk after rollbacks; a stale-step revision on a MAP must find exactly the same stale edge before and after rollback churn |
| S5 | **multi-owner** | `own_add` chains (`chm`/`chn`) — several MAPs owning one cell; rollback must not unlink a shared owner because one owner went away |
| S6 | **partial success** | a candidate list where candidate 1 rejects, candidate 2 rejects, candidate 3 ACCEPTS: exactly candidates 1+2 released, candidate 3's whole graph AND its MAP alive and re-verifying |
| S7 | **promote then later fail** | `t2_revise_graph` re-executes a restructured graph and REVERTS on verification failure; the revert path must leave no phantom nodes and the MAP must still answer its old value |
| S8 | **nested trials** | `txn_open` inside an open `txn` (forced synthetically, since no production path nests today); the inner roll must not release the outer transaction's nodes and the outer roll must release both |

**K-STRESS kill bar: 8/8 green.** Any red ⇒ report which case, which assertion,
and do not narrow the case.

---

## 5. DELIVERABLE 5 — THE CEILING, RE-MEASURED

Re-run the ceiling at genuinely evicting scales after the fix, at
**D = 20k, 50k, 100k** MAPs (indexed decoys, `e11_mkdecoy`), plus the
saturation arms `NM = 1, 2, 8`. Per level record: retrieval visits, CPU/wall,
peak memory, live nodes (`live_nodes_scan`, **not** `live_nodes`, which
`lane/misspath` C566 proved is inflated by exactly `evictions - 1`), live edges,
free-bitmap slots, index size, `TOTAL_BAD`, correctness, learning/composition/
revision latency, reclamation cost (release operations per miss), corruption,
forgetting (answer-fact survival 6/6).

**Preregistered prediction P5:** with the leak fixed, one miss at D=20,000 costs
**5 nodes and 1 edge of PERMANENT growth** (the promoted MAP and its facts, or
zero if rejected-and-released), against 82,001 today; therefore the 20k `NM=2`
and `NM=8` saturations and the 40k timeouts should clear. **P5 is falsified**
if `NM=2` at D=20,000 still times out at the preregistered limit.

Limits are fixed now and are NOT extended after a miss:
D=20k → 400 s. D=50k → 700 s. D=100k → 1400 s. All at load-average-independent
watchdog limits; a timeout is recorded as TIMEOUT.

---

## 6. DELIVERABLE 6 — RE-OPEN THE EVICTION DISCRIMINATOR

Precondition, re-verified before use and not inherited: `own_assert` must report
`c560_ok=1, ansfact_wrong_owner=0` at 20,006 MAPs, because `promote_graph`'s
ownership relation once omitted the MAP's own answer fact and any
ownership-keyed comparison would fail SILENTLY.

Arms, identical eligible set and identical kill path, differing ONLY in the key:
* **arm A** `sel_key` — `key(n) = bid(n) + LB_W*min(bid(owner(n)),CAP)`, `LB_W = 6*NE+1`
* **arm B** `evict_lru` — lowest eligible id, key ignored entirely

Charter-32 shape, **RECENT JUNK against OLD FOUNDATIONAL STRUCTURE**, scored on
foundational answer-fact survival, not on total survivors.

**Preregistered verdict rule, fixed now:** the discriminator is
**ESTABLISHED** only if arm A's foundational-answer survival **strictly
exceeds** arm B's at a level that evicts (`evictions > 0`). Equal scores ⇒
**INCONCLUSIVE**, reported as such. Arm B failing to be beaten ⇒ the consequence
term is not doing the work and that is reported, not re-tuned.

---

## 7. FROZEN KILL BARS, ALL OF THEM

| bar | statement |
|---|---|
| K-LC | instrumented build byte-identical to control at C1, C2; 3/3 deterministic |
| K-BYTE | `ans` and `scan` byte identical, C1-C8 |
| K-COUNT | search counters bit identical, C1-C8 |
| K3 | `TOTAL_BAD=0`, `canary=0`, `ns_viol`/`ns_dirty` equal to control |
| K5 | released + live == control live, exactly; `lost_slots=0`, `double_free=0`, `foreign_free=0` |
| K-STRESS | 8/8 |
| K8 | 3/3 byte-identical at C2 and C7 |
| P1-P4 | leak characterisation predictions |
| P5 | leak fix clears the D=20k saturation |
| K-DET | discriminator ESTABLISHED only on a strict arm-A win at `evictions>0` |

**VOID rule:** if a kill bar turns out to be ill-posed (e.g. it cannot be
evaluated because the instrument cannot be built), this prereg is marked **VOID**
in a follow-up document and a new prereg is written. A bar is never
reinterpreted after seeing the result, and a miss is never recorded as a pass.

---

## 8. BOUNDARIES CLAIMED IN ADVANCE

* Work counts, not times: there is no clock builtin. Wall is the watchdog's
  elapsed on a host observed at load average 36.
* One host, one compiler, one corpus.
* Node ids are expected to **diverge** between control and fix from the first
  rollback onward, because `fb_find` returns the lowest free id and the fix
  returns ids to the bitmap. That divergence is a PREDICTION, not a failure;
  what must not change is any answer.
* Under eviction pressure the fix is expected to change **which** nodes die,
  because leaked trial cells are currently the lowest-bid, lowest-id population
  and the policies select them preferentially. Any answer change at an
  evicting level is therefore reported as expected-and-explained or as an
  unexplained divergence; it is never tuned away.