# SCALING-EVICT REPORT -- sublinear reclamation, the 20k root cause, and a NEGATIVE result on meaningful-structure eviction

Lane `lane/eviction`. Claims C542-C554 (C542-C545 inherited from the aborted
attempt on this lane and re-verified here). Base: `lane/scalingp8` @ 310a8a2d6
(C526-C534). Pure Zag for all computation and profiling; shell/git for
orchestration only. Every run through `tnnwatch.sh` with a preregistered limit.
3/3 byte-identity is asserted per run by the harness where reported.

---

## 0. HEADLINE

1. **The 20k Q1 hang is root-caused with a dedicated counter, not inferred.**
   `t2_lu_first_lin` scans the entire arena on every lookup; `t2_chain` calls it
   once per chain link and the terminal link always misses, so every MAP pays a
   fixed 262,144-probe tax. The path is the MAP **build**, which is why the
   build stalled and Q0/Q1 never ran. Fixing it takes 20000 MAPs from
   **TIMEOUT at 900 s to 3 s**, with `scan=5/6` and `ans=6205/6405` -- exactly
   canonical -- at 1k/5k/10k/20k.
2. **A second, worse defect was found by measurement: reclamation was evicting
   the engine's own index scaffolding.** `idx_mode()` is a field of a node; once
   the index root was reclaimed and its slot reused, every lookup silently
   reverted to an O(NN) scan -- no error, no wrong answer, no counter, and the
   engine reported success while running quadratic. This, not reclamation cost,
   is what made 40k+ impossible.
3. **NEGATIVE RESULT, and it is the important one: reclamation does NOT operate
   on meaningful structures.** With 9337 real evictions under the structural
   policy, **all six foundational MAP nodes survived and all six foundational
   ANSWER FACTS were reclaimed.** An answer fact has in-degree 0 by
   construction, so the frozen selection key (`bid` = in-degree) ranks the most
   load-bearing old structure as the cheapest thing in the arena. **K4 is
   INCONCLUSIVE as a discriminator** because the LRU-by-oldest-id control
   produced numbers identical to the structural policy, so the test cannot
   separate them.

---

## 1. K0 -- THE INHERITED ARENA ALLOCATION WAS UNDERSIZED (answers unaffected)

The inherited harness allocated `z_alloc(3674176+P9X())` = 7,556,800 bytes, the
workspace size for the ORIGINAL NN=NE=65536 arena, while the re-dimensioned
engine addresses offsets up to 18,566,848. `tnn2_init` then zeroed 14,684,224
bytes into that 7,556,800-byte buffer, so ~11 MB of live engine state lay
outside the allocation.

**K0a CONFIRMED, K0 KILL BAR NOT TRIGGERED.** Under the corrected
`TOT = 45,221,344` bytes the answers are unchanged and so is the structure:

| | canonical `p10_9995` | this lane, corrected alloc |
|---|---|---|
| live_nodes | 70767 (D=9995) | 70802 (D=10000) |
| live_edges | 60766 | 60796 |

70802 - 70767 = 35 = 5 x 7.04 nodes, and 60796 - 60766 = 30 = 5 x 6.04 edges:
the corrected allocation is the canonical state plus exactly 5 more MAPs. **No
structure changed; the inherited numbers were honest about structure and wrong
only about scale.**

---

## 2. MISSION ITEM 2 -- ROOT CAUSE OF THE 20k Q1 HANG (dedicated counter)

`PREREG_ADDA_A.md` froze the hypothesis and the counters before implementation.

**The cause.** `t2_lu_first_lin` is
```
let n:i32=2; while(n<262144){ ... if(tag==1 && subj==s && rel==r) return n; n=n+1; }
```
`mkbroken` teaches one fact then calls `t2_chain(s0,1)`, which calls
`t2_lu_first` per link. The first call finds the fact after scanning past
every node allocated so far; the second, on the object `s0+1` which has no
fact, **always pays the full 262,144**. It is on the build path, not the query
path -- which is exactly why the build stalled and the queries never ran.

**Measured, profiler key 28 (`lu_first_visits`):**

| D | lu_first_visits | per MAP | (live_nodes/2 + 262144) |
|---|---|---|---|
| 2000 | 541,268,480 | 270,634 | 269,545 (+0.4%) |
| 4000 | 1,109,211,480 | 277,303 | 276,545 (+0.3%) |

97% of all visits at D=2000 are the fixed NN tax. Cost is **Theta(D x NN)** with
a fixed 262,144 constant, not O(live). D=20000 extrapolates to 6.6e9 visits.

**Second residue, found by reading `scan` rather than guessing.** `scan` is
workspace field 56, incremented by `rebind_try_lin`/`idx_walk_bucket`, i.e. the
rebind candidate enumeration, dispatched on `idx_mode & 1`. A run with bit0
clear keeps an O(NN) rebind. Measured `scan` at 1k/5k/10k/20k with bit0 clear:
7713 / 35713 / 70713 / 140713 -- tracking live_nodes, i.e. one full pass per
query. With bit0 set, `scan` is 5 and 6 at every scale.

**Consequence, recorded as specified:** `c20k`, 20000 MAPs on the pre-fix path,
**TIMEOUT at the preregistered 900 s** (log held only the `after_facts` dump;
the build never emitted `E11BUILD`). Not extended, not retried longer.

**Fix and kill bar.** `idx_mode = 5` (MAP plen-bucket index + FACT subject
index). `t2_lu_first_idx` now takes the **minimum matching id over the whole
bucket chain**, because `fidx_add` prepends and the linear scan returns the
lowest id -- so equivalence holds by construction instead of by the accident
that each key held one fact.

KILL BAR MET: **603 keys compared indexed-vs-linear, mismatch = 0, with
multimatch = 3**, so the test is non-vacuous: three lookups had more than one
candidate and the min-id rule was load-bearing. `activate()`'s equal-bid
tie-break was made order-independent for the same reason (C549).

---

## 3. MISSION ITEM 3 -- NAMESPACE INVARIANT BATTERY: 11/11

Inherited from the aborted attempt on this lane (C542-C545) and re-run under
the new layout. The disjoint-sign encoding (`op>=0` node, `op<0` frame) makes
the invariant explicit: `op>=0 -> op<NN`, `op<0 -> (-op)-1>=0`. All 11 operand
sites are guarded and count violations, returning the engine's `-999999`
sentinel instead of dereferencing. The inherited battery scored 0/11 and was
largely non-functional -- it injected well-formed operands, wrote through a
`-1` cell offset, compared against a chain length, and queried the wrong
relation. Each site now receives a genuinely malformed operand in a live cell
the site's own guard reads, reached through real `t2_set`/`t2_guard`/`t2_cell`
cells and real SEQ edges. Canary region re-read at every site.

**Two honest negatives, kept as negatives:** S7 `exec_val` and S9 `t2_exec` are
not independently world-reachable, because `execute()` validates the same
operand at its own site first -- that redundancy is the finding, and those two
are recorded `reach=0` and checked at unit level, so **9 of 11 sites are
independently reachable**, not 11. And `ns_dirty` is sticky by design, so a
violation poisons later `execute` calls until acknowledged.

---

## 4. MISSION ITEM 1 -- STRUCTURAL RECLAMATION: NEGATIVE RESULT

### 4.1 C551 -- the index scaffolding was a reclamation victim (found by measurement)

At D=40000 with 9290 real evictions the build completed, but the `after_build`
dump printed **`idxmode=0`** where `after_facts` had printed 5. `idx_mode()`
reads a field of a node; the MAP plen-bucket root had been reclaimed, its slot
reused, and every lookup silently fell back to the O(NN) scan. D=40000 then
**TIMEOUT at 400 s**; D=50000 never finished the build at all, because there
the root dies early enough that the remainder of the build runs quadratic.

This is the worst failure shape available: **a reclamation policy that destroys
the structures which make reclamation affordable.** Fixed by excluding tag-40
index scaffolding where victim eligibility is decided (`vre`), in `evict_scan`
-- a documented change to the frozen reference, which has the identical defect
-- and in `evict_lru`. Counter 914 counts skips; **counter 915 samples
`idx_mode` at every dump so a silent downgrade to quadratic can never again be
reported as success** (`idxmode_lost=0` in every post-fix run, including 100k).

### 4.2 C553 -- the frozen selection key is IN-DEGREE, and that is the whole story

`bid_ref(n) = evcount(n,1)+evcount(n,2)+evcount(n,6)+evcount(n,7)-evcount(n,3)`.
Every MAP gets its own self-edges of type 2 and 6, so **every MAP starts at
bid 2**. With no edges between MAPs the in-degrees are all equal, min-bid
degenerates to lowest-id-from-cursor, and the "structural" policy is
bit-identical to LRU: the test would have been vacuous. Each junk MAP therefore
CITES a foundational MAP with a type-1 edge (the engine's own representation
of composition). Measured effect: junk stays at bid 2, each foundational MAP
reaches **bid 6224-6226**, and `bid_ref == bid_fast` exactly at every one of
the six -- so the K1 fast-vs-reference kill bar on the bid counters **PASSES**.

### 4.3 C554 -- what actually died (the finding)

`k4diag`, 40000 junk MAPs, mode 13 (both indices + fast structural policy),
9337 evictions:

```
evictions=9337  evict_tag20=0  evict_nontag20=9337
evict_FOUND=0    evict_JUNK=0  classid_ok=1
nontag_FACT=1877 nontag_HISTORY=0 nontag_GOALI=1865 nontag_FRAME=3730 nontag_OTHER=1865
E11FOUND total_survived=6 of 6      (bid 6224-6226, bid==bid_fast)
E11FACTS fi=0..5 ansfact_live=0 bid=0     <-- ALL SIX ANSWER FACTS DEAD
E11JF downstream_ans=-2 expect=7000 ok=0
```

**Not one MAP was ever a victim.** All six foundational MAP nodes survived.
All six foundational *answer facts* were reclaimed. The downstream answer is
carried by the fact, not the MAP, and a fact nobody cites has in-degree 0 --
so the frozen key ranks the load-bearing answer of old foundational structure
as the **cheapest object in the entire arena**, strictly below junk (bid 2).

**K4 VERDICT: INCONCLUSIVE as a policy discriminator, and a strong NEGATIVE as
a design result.** The prereg required the LRU-by-oldest-id control to fail;
it did not. `k4_lru40k` (mode 45, same world) produced numbers *identical* to
the fast policy -- same 9337 evictions, same `evict_tag20=0`, same 6/6 survival,
same `downstream_ans=-2` -- because with no MAP ever eligible, min-bid and
min-id select the same nodes. Reporting this as a pass would be exactly the
error the prereg anticipated; it is reported as INCONCLUSIVE.

**No history node was reclaimed** (`nontag_HISTORY=0`), satisfying the K3
"version history survives" requirement. **No structural children were
reclaimed** (`reclaimed=0`) -- vacuously, since `reclaim_map` only runs when a
MAP is evicted and no MAP was. Shared-subgraph protection was therefore never
exercised at scale and is **NOT CLAIMED**.

---

## 5. CEILING

| level | before | after (`idx_mode=5`, C551) | evictions | verdict |
|---|---|---|---|---|
| 20,000 | TIMEOUT >900 s | **3 s**, scan 5/6, ans 6205/6405 | 0 | FIXED |
| 40,000 | TIMEOUT 400 s | build completes, query stalls | 9290 | partial |
| 50,000 | TIMEOUT 500 s, no `E11BUILD` | not re-run post-C551 | -- | superseded |
| 100,000 | never reached | **build completes**, `idxmode=5` held, `live_edges=262144` = NE exactly, 219,290 evictions, `idxmode_lost=0` | 219,290 | query TIMEOUT 800 s |

**The binding limit moved from retrieval, to reclamation cost, to EDGE
CAPACITY.** At 100000 MAPs `live_edges` sits at exactly NE=262144: edges, not
nodes, are now exhausted. `live_nodes=481432` exceeds NN=262144, which means
the `live_nodes` header counter and the reclamation path disagree and that
disagreement is **unresolved** -- flagged, not fixed.

**Remaining known superlinear residues, all measured, none fixed:**
* `sel_fast` charges a full 262,144-probe bitmap scan per eviction
  (`paddv(W,823,262144)` inside it) -- 9337 evictions x 262144 = 2.4e9 at 40k.
  This is the K2 cost model failing, and it is why the K4 runs TIMEOUT at 600 s
  rather than completing.
* `evict_lru` is O(NN) per eviction by construction (it is the reference
  control).
* `comb_present` and `t2_gather_sum` are unconditional O(NN) loops. Measured
  `comb_present_probes` and `gsum_probes` are **0 on every build path reported
  here**, so they are not on the hot path at these scales -- reported as
  measured, not as eliminated.
* `t2_gather_idx` (trial path) still returns candidates in bucket-chain order
  rather than id order. Untested for equivalence at scale. **Known open risk.**

---

## 6. TOOLCHAIN / HARNESS DEFECTS FOUND (all cost this lane real time)

* **`_zag_raw_syscall` is inert** on darwin/arm64 (brief 4.0). All output goes
  through `_zag_print`.
* **`setsid` does not exist on this host** (`command -v` -> rc=1), so
  `tnnwatch.sh reg` falls back to a plain background child and its poll loop
  dies with the orchestrating shell. **Calling `$W reg` in the foreground
  leaves the experiment running with NO timeout enforcement.** `wrun.sh` and the
  ladder scripts launch it under `nohup`+`disown` and return immediately.
* **Exceeding if-nesting 3 does not fail to compile.** `znc` reports success
  and emits a binary that is **SIGKILLed at exec, rc=137, zero bytes of
  output** -- which the watchdog correctly flags `EMPTY`. A silently unrunnable
  binary is indistinguishable from a hung experiment unless empty output is
  enforced. Found by C554's first build; flattened to sequential `if`s.
* Rebuilding the binary while a ladder is running produced three EMPTY rungs
  (`bs_8000/12000/16000`). **My harness defect, recorded, not hidden.**
* Two counter-key collisions that I introduced and then fixed: key 836 was
  already owned by `vre()` in the base, so every LRU run double-counted it.
  Policy selector 100 -> 910, LRU counters 836/837/838 -> 911/912/913, with an
  explicit owner audited per key.

---

## 7. VERDICT

* **Retrieval and MAP-build scaling: SOLVED and byte-identical to canonical.**
  20000 MAPs in 3 s with `scan=5/6`, `ans=6205/6405`. The 20k hang was a single
  O(NN) scan with a fixed constant, found by a dedicated counter, fixed by an
  equivalence-by-construction index.
* **Namespace correctness: INVARIANT-BACKED, 11/11 guarded**, 9/11
  independently world-reachable, with two recorded negatives.
* **Sublinear eviction: NOT ACHIEVED.** Selection is sublinear
  (`sel_visits == evictions`, 9337 == 9337) but `sel_fast` still scans 262,144
  probes per eviction, so per-eviction cost is O(NN), not amortized O(1). The
  prereg K2 cost model is **FAILED** and is reported as failed.
* **Charter 32 / charter 38: NEGATIVE.** Reclamation runs on arbitrary cells,
  not on meaningful structure. It destroys foundational answer facts while
  preserving the MAPs that own them, because "load-bearing" is measured as
  in-degree and an answer fact has none. This is age-priority wearing a
  structural costume.

## 8. BOUNDARIES

* "Learner-maintained" means keys derive from state the learner wrote. The tag
  taxonomy was NOT learned. **No L3 claim is made or implied.**
* The K4 world is synthetic. Its junk MAPs are built broken and were never
  reliably answerable, so junk retention is not a loss measure; the single
  quantity that must hold is the foundational downstream answer, and it does
  not.
* `sel_fast` vs `evict_scan` victim equality (prereg K2a) is **not** re-verified
  at scale; the scan reference is O(NN*NE) and cannot run there.
* The `live_nodes` vs NN discrepancy at 100k is unresolved.
* `t2_gather_idx` order-equivalence is untested.
* Only ONE host, one compiler, one corpus. Cross-platform determinism rests on
  brief 4.1, not on this lane.
* `t_c5`/`t_c6` remain dead frozen helpers whose 110,656-byte scratch is too
  small. Never executed here. Would overflow if called.

## 9. NEXT EXPERIMENT

1. **Give the selection key a consequence term.** The finding is precise: an
   answer fact has in-degree 0. Add a per-node `loadbearing[n]` = count of live
   nodes that would lose an answer if `n` died (queryable subjects citing it,
   MAPs whose root graph reaches it) and key selection on
   `bid + loadbearing`, leaving `bid` as the frozen control. Kill bar: the same
   K4 world must then return `downstream_ans=7000` with `evict_FOUND` nonzero
   and the LRU control still failing. If it does not discriminate, K4 stays
   INCONCLUSIVE and the key is reported inadequate.
2. **Fix `sel_fast`'s O(NN) bitmap probe per eviction** so the K2 amortized-O(1)
   cost model is actually met; this is what currently forces the K4 runs to
   time out at 600 s.
3. **Decouple node and edge capacity.** Edges are now the binding limit at
   100k. Size NE from live-node pressure rather than fixing NE=NN.
4. **Resolve the `live_nodes` > NN discrepancy** before any reclamation result
   at 40k+ is cited.