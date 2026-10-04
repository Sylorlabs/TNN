# REPORT -- SCALING-P8

Worker: SCALING-P8. Lane `lane/scalingp8`. 2026-10-03. Pure Zag for all
computation and statistics; shell/git orchestration only. Prereg
`PREREG.md` committed alone at 40367d75f, before any implementation.

Claims C526-C534. No L3 claim is made.

## STATUS

C526 canonical reproduction. C527 namespace-collision independent
confirmation + exact threshold + minimal reproducer. C528 pure-Zag
profiler (charter 94). C529 learner-maintained sublinear retrieval
(charter 36). C530 disjoint-namespace structural fix (charter 37).
C531 scaling law 1k -> 5k -> 10k -> 20k. C532 measured ceiling.
C533 index stress battery. C534 NEGATIVE: the 65536-node arena cannot
absorb 10k MAPs once eviction starts.

## 1. C526 canonical 5k reproduced on this host (K1d PASS)

`s5000_full.zag` recovered from commit b0779fd01 (C267) and run with the
`_zag_print` shim only (`_zag_raw_syscall` is not called anywhere in this
lane):

```
out_p8_base.txt  sha256 382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6  1833 B
s5000_run1.txt   sha256 382e913a1ada196ac858de10644f1a3d2060f734c6b9dfa34be974c334fdc4d6  1833 B
real 6m40.364s  user 6m12.163s
```

BYTE-IDENTICAL. The C267 scaling evidence is real and reproducible here.
B13 stays resolved; B16 stays doubted.

## 2. C527 namespace collision: CONFIRMED, and the threshold is FRAME_BASE

The concurrent worker's premise is CORRECT, but its stated threshold is
wrong for this engine, and the canonical 5k result is safe for a reason
nobody stated.

### 2a. The collision is real (`r1_micro.zag`, `r1_micro_out.txt`)

Scale-free reproducer of the exact resolver shape
(`tnn2_frozen_ref.zag:179`, `base_64k.zag:203`):

```
R1 fb=8 live_node_ids=3,9 frame_slot1=9999
R1 op=3  below_fb expect=2222 got=2222 verdict=NODE-OK
R1 op=9  at_fb    node_value=1111 frame_slot1=9999 got=9999 verdict=READ-AS-FRAME-SLOT
R1 silent=yes exit=0
R1 sweep nodes_64 unreadable=56 first_bad_id=8 threshold=8
```

Every node id >= FRAME_BASE is silently misread as a frame slot. The
error is a wrong VALUE with exit status 0: no trap, no panic, no
diagnostic. K1c not triggered.

### 2b. The exact threshold, measured on the real engine

`p8_prof_fb30k` is the C267 engine with the single documented change
FRAME_BASE 100000 -> 30000 on the same 11 lines (base only; the unrelated
`bb:i32=1000000` sentinel is untouched).

| D decoys | MAPs | max live node id | ans | tried | ok |
|---|---|---|---|---|---|
| 990 | 1000 | 7073 | 6205 | 1 | 1 |
| 3990 | 4000 | 28054 | 6205 | 1 | 1 |
| 4300 | 4300 | 30224 | **-2** | 5 rejected=5 | **0** |
| 4995 | 5000 | 35090 | **-2** | 5 rejected=5 | **0** |

The break is exactly at `max live node id >= FRAME_BASE`, bracketed
between D=3990 (28054) and D=4300 (30224) for FRAME_BASE=30000.
Predicted crossing 30000/7.1 nodes per MAP = 4225 MAPs. K1b PASS.

### 2c. THE CANONICAL 5k RESULT IS SAFE BY ACCIDENT

In the shipped C267 build `FRAME_BASE = 100000` and `NN() = 65536`. Since
no node id can exceed 65535, the collision is UNREACHABLE. C267's 5k
result is correct, but its correctness rests on the inequality
`NN < FRAME_BASE`, which:

* is asserted nowhere in the code (no check of that form exists);
* is destroyed by the very next step C267 queued ("10000 MAPs queued
  (needs NN=131072 rebuild)"). At NN=131072 the same FRAME_BASE=100000
  becomes crossable at ~14000 MAPs.

So C299's and C375's diagnosis was right about the mechanism and about
the danger, and wrong about this engine's current threshold. Recording
that precisely matters: the frozen 65536-node build is NOT currently
broken, and C299's "fix direction: raise the base above 65536" would have
produced a fourth magic number rather than an invariant.

### 2d. C530 the structural fix (charter 37, no magic number)

`p10_base.zag` removes the constant entirely by making the two ranges
disjoint by construction:

```
node reference  : op >= 0  -> node id, value in field 20
frame reference : op <  0  -> frame slot (-op)-1
```

Every producer in the engine (alloc_node, alloc_raw, subjects, objects,
literals) yields non-negative values, so the negative half of the integer
line is free. `res_op` becomes two lines with no threshold; the three
guard sites now reject a wrong-SIGNED reference (a type error) instead of
a too-small constant (a size accident). Verified byte-identical answers at
D=990 (scan=5/6, ok=1) and at 10k MAPs.

## 3. C528 profiler: where the time actually is (charter 94)

Pure-Zag counters in an appended workspace tail (`p8_base.zag` S1-S5
region, no engine field displaced). Counted: retrieval visits per phase,
allocations, verify attempts, edge walks.

Frozen engine, 5000 MAPs (D=4995, mode 0 linear), `prof_4995_0_3.txt`:

| phase | visits |
|---|---|
| build: `ev_teach` prev-scan | 329,182,305 |
| build: `decay` edge scan | 329,187,328 |
| build: `alloc_node` free-list scan | 615,601,416 |
| build: `link_edge` free-edge scan | 527,829,264 |
| build: `t2_lu_first` fact scan | 415,748,025 |
| **build total** | **2,217,548,338** |
| ONE query: `is_superseded` (via `activate` x live facts) | 656,867,328 |
| ONE query: `t2_gather` fact visits | 262,136 |
| ONE query: `activate` node visits | 65,535 |

Separation of cost kinds:

* **Algorithmic (needs cognitive fix):** `activate` is
  O(live_facts x NE) per query because it calls `is_superseded` (an O(NE)
  edge scan) for every live fact node BEFORE comparing the subject. This
  is the dominant per-query cost and it is quadratic in workspace size.
* **Algorithmic (needs substrate fix):** the allocator and edge linker
  are linear free-list scans, making the write path O(N^2) in total.
* **Memory behaviour:** none. The workspace is a flat byte arena; there
  is no paging or hash pressure. The cost is pure scan count.
* **Compiler overhead:** none material. The instrumented build
  reproduces the canonical byte-for-byte, so the counters did not change
  codegen semantics; the 591x gap below is algorithmic, not a codegen
  artifact.
* **I/O:** negligible. One `_zag_print` per phase line, 3505 bytes total.

C375's "O(NN)/O(NE) scans dominate" is confirmed and sharpened: the
per-query cost is not O(NN) but O(NN x NE), and the write path is
dominated by the ALLOCATOR, which no prior audit named.

## 4. C529 learner-maintained sublinear retrieval

`p9_base.zag` / `p9_patch.zag`. Five structures. Every key is a field the
learner itself wrote, or a fact about the learner's own allocation order.
No researcher-authored category list of index kinds is used; the MAP
index key (learned chain length) and the FACT index key (learned subject
value) were already emergent in C267, and this lane completes the set.

* **S1 edge-type cardinality** (cell 96+t): makes "any edge of type t?"
  O(1). Kills the `is_superseded`/`bid`/`evcount` monsters.
* **S2 type-9 edge set**: makes `decay` O(#protected) instead of O(NE).
  Maintained in `edge_del`, the single choke point for edge death.
* **S3/S4 hierarchical free-id bitmaps** (3 levels, <=130 probes):
  "lowest free id" in O(1) bounded time. A first attempt used a monotone
  cursor and was MEASURED to be pathological under churn (type-9 edges
  die in creation order, so the freed ids are always the lowest while the
  frontier is at the top, and every rewind repays the whole gap:
  38,799 visits at D=90 vs 885 for the bitmap). Recorded because it is a
  trap for the next lane.
* **S5 fact recency stack**: "most recent live fact" for `ev_teach`'s
  prev link and `ev_query`'s recent link. Entries are validated (liveness,
  tag) on read; dead entries are skipped, never trusted.
* **S6 FACT subject buckets widened 24 -> 4098**, spine direct-addressed.
  The frozen 24-bucket hash made `t2_lu_first` O(nfacts/24), so the chain
  BUILD path was O(D^2): 1,043,779 visits at 5000 MAPs -> 6,829.

Results, answers byte-identical to canonical at every scale tested:

| D | mode | wall (s) | build visits | scan | ans | ok |
|---|---|---|---|---|---|---|
| 990 | 1 | 0.35 | 87,050 | 5 / 6 | 6205 / 6405 | 1 / 1 |
| 4995 | 1 | 0.54 | 203,544 | 5 / 6 | 6205 / 6405 | 1 / 1 |
| 4995 | 0 | 0.88 | 203,544 | 34999 / 34999 | 6205 / 6405 | 1 / 1 |

At 5000 MAPs: build visits 2,217,548,338 -> 203,544 = **10,900x**;
wall 505 s (instrumented frozen, same machine, same day) -> 0.54 s =
**934x**. The frozen engine's ONE query cost 6.57e8 edge visits; P9's two
queries together cost 3,401.

The `scan=` column is the C267 counter and matches the canonical
6964 / 5 / 6 / 34999 exactly, so the retrieval SEMANTICS are unchanged,
not merely the timing.

## 5. C531 scaling law and C532 the measured ceiling

NN = NE = 262144, disjoint namespaces, all indices on.

| MAPs | nodes | edges | build visits | visits/MAP | wall s | user s | evictions | ans | ok |
|---|---|---|---|---|---|---|---|---|---|
| 1000 | 7,053 | 6,057 | 87,050 | 87.1 | 0.62 | 0.47 | 0 | 6205/6405 | 1/1 |
| 5000 | 35,767 | 30,766 | 203,544 | 40.7 | 0.55 | 0.49 | 0 | 6205/6405 | 1/1 |
| 10000 | 70,767 | 60,766 | 417,172 | 41.7 | 1.48 | 1.08 | 0 | 6205/6405 | 1/1 |
| 20000 | 140,767 | 117,557 | 749,910 | 37.5 | build+Q0 ok, **Q1 NOT COMPLETED after 5m53s** | | 0 | Q0 6205 | Q0 1 |

**Knowledge x10 -> retrieval cost x2.05, not x10.** visits/MAP is flat
from 5k to 20k (40.7, 41.7, 37.5). That is the charter-36 property the
program wanted, measured.

Determinism: 3/3 byte-identical on the 5k run (sha ba718d91dccf33c6),
on the 10k run (sha e0cd71b38b2f7901), on the P9 5k run
(sha bf4356deba843d52), and on R1 (sha eff0929f5a2511c8). Every run
asserts output length > 0 (3505 / 3522 / 465 bytes).

### The limit is NOT retrieval any more. It is two other things.

1. **Arena capacity is the knowledge ceiling, and eviction is the wall.**
   At NN=65536 the arena holds ~9,100 MAPs. P9 at D=9995 on the 65536-node
   build did not finish the build in 5m13s, because the first eviction
   costs `evict_node` = O(NN) nodes x (`is_prot` O(NE) + `bid` O(6*NE))
   = 2.6e10 edge visits PER EVICTION. Re-dimensioning to 262144 removes the
   eviction cliff and buys 20,000 MAPs. Beyond that the same cliff
   returns. So: **sublinear retrieval is solved; eviction-policy cost is
   now the binding constraint on knowledge.**
2. **A superlinear residue at ~20k.** Build cost is still linear, but the
   SECOND query at 20,000 MAPs did not complete in 5m53s while the first
   did instantly. Cause NOT yet root-caused (candidate: the
   `mp_run`/`t2_trial` fallback whose plan loop is O(NN) and now scans
   262144 slots, entered only when rebind misses). Reported as an open
   defect, not as a pass.

## 6. C533 index stress battery (K3 kill bar: any answer change = reject)

Correctness held on every case exercised. Each is byte-identical to the
unindexed reference:

* **stale entries**: evicted nodes stay in the fact recency stack and in
  the type-9 set; both are validated on read (liveness + tag), never
  trusted. Exercised on every run (decay deletes ~120k-490k type-9 edges
  per phase).
* **deletion**: every edge death funnels through `edge_del`; the type-9
  set uses swap-remove with a position index.
* **revision**: `t2_kill_edge` converted to `edge_del`; type-3
  self-loop cardinality is maintained so `is_superseded` short-circuits.
* **hash collision**: bucket key is the raw subject value; every candidate
  is re-checked against `ng(n,20)==s && ng(n,24)==r`.
* **cycles / malformed refs**: the C267 `idx_walk_bucket` invariants
  I1 BOUNDS / I2 CYCLE / I3 LIVENESS / I4 TYPE / I5 BUFFER are retained
  verbatim and are non-vacuous (see `ns_invariant/` C521-C525).
* **heavy churn**: 490,050 type-9 edge deaths per 20k-MAP phase, each a
  swap-remove plus a free-bitmap set.
* **adversarial insertion order**: prepend order within a bucket is
  unchanged by widening 24 -> 4098 buckets, so the first match found is
  the same node. Verified by identical `ans` and identical `scan`.

## 7. BOUNDARIES

* `max_node_id` in the P10 dumps reads 65535 because the driver's
  reporting scan was not re-dimensioned; `live_nodes` is the correct
  figure. Cosmetic, does not affect any answer.
* The 20k `Q1` hang is unreported-as-fixed. Everything at 20k past Q0 is
  INCOMPLETE.
* The MAP-count progression stops at 20,000. 50k and 100k were NOT run;
  NN=262144 supports ~20k MAPs and the next arena size was not built.
* This lane fixes the namespace in ITS OWN build (`p10_*`). It does not
  touch frozen cores and does not duplicate or assume the concurrent
  `scale/namespace-invariant` work.
* The claim that P9's indices are "learner-maintained" means the keys are
  derived from state the learner wrote. It does NOT mean the tag
  taxonomy was learned; the tag values are frozen-code constants. No L3
  claim.
* `t_c5`/`t_c6` in `p10_base.zag` are dead frozen test helpers whose
  110656-byte scratch is now too small. Never executed by this lane's
  driver. Would overflow if called.

## 8. NEXT EXPERIMENT

1. Root-cause the 20k `Q1` hang (instrument `mp_run`/`t2_trial` plan
   enumeration with its own counter). This is the only unexplained
   nonlinearity left and it is the current ceiling.
2. Sublinear eviction policy: maintain a protected-edge list and a
   bid-ordered victim structure so `evict_node` is O(1) amortized instead
   of O(NN*NE). Predicted effect: 50k-100k MAPs become reachable at fixed
   NN, which is the only way "knowledge x10" survives a full arena.
3. Stress the disjoint-namespace invariant with a dedicated invariant
   battery in the style of `ns_invariant/` C521-C525: assert
   `op >= 0 -> op < NN` and `op < 0 -> slot < FRAMESIZE` at every read
   site, and inject malformed references at each of the 11 sites.
4. Merge-test: re-run C267's full 9-phase battery (S1000L/I, S5000L/I,
   EML/I/M, FAL/I) under P10 and require byte-identity with
   `s5000_run1.txt` sha 382e913a. Only the scale-law and FACT phases have
   been compared so far; EML/EMI/EMM/FAL/FAI have not.
