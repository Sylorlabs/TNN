# PREREG -- EVICTION-P9 (sublinear structural reclamation + namespace battery)

Worker: SCALING-EVICT. Lane `lane/eviction`. 2026-10-03.
Base: `lane/scalingp8` @ 310a8a2d6 (claims C526-C534). Built ON, not rebuilt.
Pure Zag for ALL computation, statistics and profiling; shell/git orchestration
only. New claim IDs C535+.

Frozen BEFORE implementation. No bar is moved after seeing a result.

## 0. INHERITED STATE THAT IS ASSUMED, NOT RE-ARGUED

From C526-C534: the engine is `p10_base.zag + p10_patch.zag + p10_driver.zag`
concatenated to `p10_prof.zag` (verified byte-identical to the concatenation).
NN = NE = 262144. Namespaces are DISJOINT BY SIGN (`op>=0` node, `op<0` frame).
Five learner-maintained indices (edge-type cardinality, type-9 set, 3-level
free-id bitmaps, fact recency stack, 4098-bucket FACT subject index).

## 1. K0 -- ARENA ALLOCATION IS UNDERSIZED (falsification of the inherited harness)

**Observation made while reading the inherited code, before any experiment.**
`p8_big()` allocates `z_alloc(3674176+P9X())` = 7,556,800 bytes.
3674176 = 64 + 65536*40 + 65536*16 + 128*32, i.e. the workspace size for the
ORIGINAL NN=NE=65536 arena. The re-dimensioned engine addresses
`noff(n)` up to 10,485,824, `eoff(e)` from 10,485,824 to 14,680,128,
`loff(l)` to 14,684,224, and the whole P9 index tail `PB()..` from 14,684,224
to 18,566,848. `tnn2_init` then zeroes 14,684,224 bytes into the 7,556,800-byte
buffer. **~11 MB of engine state -- every edge record, every profiler cell,
the type-9 set, the fact stack and BOTH free-id bitmaps -- lives outside the
allocation.**

Prediction K0a: with the allocation corrected to `WSZ()+P9X()` the ANSWERS are
unchanged at every scale (they survived by luck below the corruption
threshold), but the profiler counters in the `PB()` region change, because
those cells were reading and writing foreign heap.

Prediction K0b: the inherited "Q1 INCOMPLETE after 5m53s at 20000 MAPs" is an
artifact of that corruption and DISAPPEARS under the corrected allocation.

KILL BAR K0: if either answer changes at D<=10000, C529-C534's numbers are
declared artifacts and every inherited visits/wall figure is retracted.

## 2. K1 -- EXACT SUBLINEAR PREDICATES (replaces the O(NN*NE) scan)

Frozen `evict_node` is `O(NN * (is_prot + 6*evcount)) = O(NN*6*NE)` PER
EVICTION, i.e. 4.1e11 edge visits at NN=NE=262144. Two exact O(1)-amortized
replacements are built in the tail region, maintained only at the three places
where the underlying state changes (`link_edge`, `edge_del`, `ref_prot`):

* `inT[t][n]` = live count of edges with `to==n` and `type==t`, for
  t in {1,2,3,6,7,12}. Makes `evcount(n,t)` O(1).
* `prot[n]` = live type-9 edges into n with clk>0. Makes `is_prot(n)` O(1).
* `bidv[n] = contrib(n) + SUM over live type-10 edges e with to(e)==n of
  contrib(from(e))`, where `contrib(n) = in1+in2+in6+in7-in3`. Delta-propagated
  through a per-node intrusive list of live type-10 OUT-edges, so a change to
  `contrib(g)` reaches `bid[to]` in O(#type-10 out-edges of g).

KILL BAR K1: at every checkpoint, for EVERY live node n,
`fast_is_prot(n) == scan_is_prot(n)` and `fast_bid(n) == scan_bid(n)`.
Any mismatch is a FAIL, not a rounding. The scan versions are retained in the
binary for the comparison; the comparison itself is O(NN*NE) and therefore only
run in the small-arena correctness mode, never in the scale mode.

## 3. K2 -- NO GLOBAL SCAN IN VICTIM SELECTION

Frozen selection: scan every node slot from the allocator cursor, take min
`bid` over live unprotected tag-1 nodes, ties broken by lowest id in cyclic
order from the cursor.

Replacement: live tag-1 nodes are held in per-`bid` buckets (`bid` shifted by a
bias so the common negative-to-small range is direct-addressed; a single
overflow list holds `bid` above the table). `vmin` is the lowest non-empty
bucket and only ever moves DOWN on insertion, so total upward advance is
amortized O(1) per insertion. The current `vmin` bucket additionally carries a
32 KiB membership bitmap (ids 0..262143, 1 bit each) built once when the bucket
becomes current and updated incrementally per removal, so the cyclic-id
tie-break is resolved by bitmap scan instead of a list walk. Two bitmaps exist
(current + one being built) so a bucket change never loses work.

Cost model (preregistered, to be checked not assumed): total victim-selection
cost over a whole run is O(total nodes ever inserted) = LINEAR in the run, and
per-eviction cost is amortized O(1).

KILL BAR K2: (a) the node selected by the fast policy is EXACTLY the node the
frozen scan selects, on every eviction, in every test world; (b) the fast
policy's total selection visits over a run are within 2x of the number of
evictions plus the number of nodes.

## 4. K3 -- STRUCTURAL RECLAMATION (charter 38)

Frozen `evict_node` kills the chosen tag-1 node and then deletes every edge
touching it. Anything it owned structurally is left behind as a fossil, and
`rec_evict` writes a bare tombstone.

P9 adds an ownership record in the tail (`own[n]`, plus a per-MAP child list)
populated at `promote_graph`, and reclaims structurally:

* **Atomic**: the graph cells owned by a MAP are reclaimed in the SAME
  reclamation as the MAP, not left as fossils.
* **Shared**: a node is reclaimed only when its live reference count
  (`in1+in2+in3+in6+in7+in12`) is 0 at the moment of consideration. Facts are
  shared by many MAPs via type-1 edges, so they are NOT deleted when one owner
  disappears. Shared-node survival is asserted directly, not assumed.
* **Cycles**: reclamation uses a worklist plus a visited bitmap, so a cyclic
  ownership/edge shape terminates and visits each node once.
* **Version history**: `rec_evict` history nodes are marked non-reclaimable and
  now carry the evicted MAP's root graph id and its (subject, relation) so
  provenance survives the eviction. Asserted: no history node is ever reclaimed.
* **Provenance**: the surviving evidence a victim supported is counted before
  reclamation (`ev_teach` facts referenced by the victim) and asserted to
  remain live afterwards.

KILL BAR K3: zero dangling references after every reclamation, measured by a
full-arena audit (`live edge with to!=sender and to not live` == 0, and
`own[c]==m` with `c` not live == 0). Any nonzero count is a FAIL.

## 5. K4 -- THE POLICY MUST NOT BE ONLY RECENCY/FREQUENCY/AGE (charter 32)

The selection score stays the frozen structural `bid` (a bidirectional edge
count). Three measures are RECORDED per surviving node at the audit, not used
as the key: downstream dependents, reconstruction cost (graph length),
predictive usefulness (verified hits), composition usefulness (graphs that
consumed it), uniqueness of evidence (is this the only support for its answer),
revision relevance (revisions that touched it).

Test world W-JUNK-FOUND: old FOUNDATIONAL MAPs with long graphs that later MAPs
depend on through shared facts, plus recent JUNK MAPs with short broken graphs
that depend on nothing.

KILL BAR K4: under the fast policy, >=90% of evicted nodes in W-JUNK-FOUND are
junk and 100% of foundational MAPs survive; under an LRU-by-id control policy
that evicts the oldest ids, foundational MAPs are destroyed and downstream
answers are lost. The control MUST fail, otherwise the test does not
discriminate and K4 is reported as INCONCLUSIVE, not as a pass.

## 6. K5 -- NAMESPACE INVARIANT BATTERY (charter 37)

Because the 5k result was correct only by accident of two unrelated constants,
correctness must be invariant-backed. The disjoint-sign resolver has 11 operand
dereference sites:

  S1 `res_op` node branch            S7 `exec_val` operand
  S2 `execute` MOVE src              S8 `execute` MOVE dst
  S3 `execute` BEQ lhs               S9 `t2_exec` result operand
  S4 `execute` BEQ rhs              S10 `fr_get` frame-chain walk
  S5 `execute` INC dst              S11 `fr_set` frame-chain walk
  S6 `execute` DEC dst

At each site assert `op >= 0 -> op < NN` and `op < 0 -> (-op)-1 >= 0`, count
violations, and on violation return the engine's existing failure sentinel
(`-999999`) instead of dereferencing.

INJECTION: at each of the 11 sites a malformed operand is written into a live
cell and the query re-run. Required of every injection:
  (i) the site guard fires and the violation counter increments;
  (ii) the run returns a DEFINED failure, never a wrong answer;
  (iii) no read outside the arena occurs (checked by a canary region: the last
       4 KiB of the allocation is filled with a known pattern and re-read);
  (iv) engine state is not corrupted -- a subsequent well-formed query on the
       same workspace still returns the correct answer.

KILL BAR K5: 11/11 sites guarded, 11/11 injections detected, 11/11 post-injection
queries correct, canary intact at every site. Any miss is a FAIL.

## 7. K6 -- SCALE PROGRESSION AND LIFETIME EVENTS

Retired scale modes, run under the corrected allocation with all structures on:
1000 / 5000 / 10000 / 20000 / 50000 / 100000 MAPs, plus forced-eviction runs at
a small NN so that reclamation is actually exercised (K7), plus a
100k-lifetime-event run (charter 35) where feasible.

Measure at each level: retrieval visits, CPU, wall, nodes, edges, index bytes,
correctness, learning latency, composition latency, revision latency,
reclamation cost, corruption, forgetting.

FORGETTING (charter 35): after eviction pressure, re-query the pre-eviction
question set and report the fraction still answered. A policy that reclaims
junk must not lose answers that were previously correct.

## 8. K7 -- FORCED-EVICTION COMPARISON

Run the same MAP count twice at NN=65536: once with the frozen scan policy and
once with the fast structural policy. Report per-eviction selection visits and
wall. Prediction: >=100x fewer selection visits.

## 9. K8 -- MERGE / BYTE-IDENTITY

Re-run the C267 canonical 9-phase battery and compare byte-for-byte against the
checked-in canonical outputs (`s5000_run1.txt` sha 382e913a for the 5000-MAP
case, and `p10_*.txt` for the P10 layout). Correctness always beats speed: any
answer difference in the NO-EVICTION regime is a hard FAIL, because in that
regime reclamation never runs and every change is a pure index change.

Determinism: 3/3 byte-identical on every reported run. Every run asserts
non-empty output.

## 10. PRE-EXISTING BOUNDARIES CARRIED FORWARD

* `max_node_id` in the dumps is scanned to 65536 only (cosmetic; `live_nodes`
  is the correct figure). Not fixed here.
* `t_c5`/`t_c6` are dead frozen test helpers whose 110656-byte scratch is now
  too small. Never executed by this lane. Would overflow if called.
* "Learner-maintained" means the keys derive from state the learner wrote. It
  does NOT mean the tag taxonomy was learned. No L3 claim is made here.