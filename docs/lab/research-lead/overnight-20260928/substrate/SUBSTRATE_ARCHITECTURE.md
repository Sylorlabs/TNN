# S9+S10 Memory Substrate: Unified Architecture Document

Document only. No implementation. Status: SUBSTRATE-DOCUMENTED.

This document specifies the unified memory substrate formed by the S9
fact eviction mechanism (slot level) and the S10 string pool garbage
collector (byte level). Together they close the append-only growth of
the shared substrate: S9 reclaims dead fact slots, S10 reclaims the
string bytes those dead slots referenced.

## 1. Lineage

| Phase | Prereg | Result | Verdict | Commit |
|---|---|---|---|---|
| S9 fact eviction / GC | 18f3d2a5e | SCALE-TESTED | all K1-K4 pass | 83b78a781 |
| S10 string GC design | (design) | DESIGN-COMPLETE | all K1-K3 pass | fa9579074 |
| S10 implementation | d23ca466a | BUILD-PASS (F1-F6) | all K1-K4 pass | 54851fd3f |

Prereg strictly precedes implementation in both phases (verified with
`git merge-base --is-ancestor`). All builds pure Zag (znc/shell/grep/git
only, zero Python). Determinism: 3/3 byte-identical runs in each phase.

Problem both phases address: the shared substrate fact store was
append-only. Learning (e,a,v2) after (e,a,v1) appended a new triple; the
old triple was unreachable (query scans from the end and returns the
latest match) but still occupied a slot. Once the 256-slot cap was hit,
every further learn was dropped, including important facts learned late.
S9 fixes the slot waste. The string pool (bump allocator, no dedup, no
free list) kept every interned copy forever: 3 fresh copies per learn,
2 throwaway temp copies per query/pin, plus bytes referenced only by
evicted slots. S10 fixes the byte waste.

## 2. Workspace layout

The S9+S10 workspace carries one fact triple store and one string pool.
Relevant header fields (u32 offsets, backward compatible additions):

| Offset | Field | Introduced |
|---|---|---|
| 60 | max_fact (live slot cap, default 256) | S9 (was constant, now parameter) |
| 72 | evict_count | S9 |
| 76 | compact_count | S9 |
| 80 | learn_ok | S9 |
| 84 | learn_dropped | S9 |
| 88 | str_limit (stored copy of wsize, set once by sub_init9) | S10 |
| 92 | gc_count | S10 |

Region order: header, fact triples, meta region (S9), string pool (S10).

The S9 meta region holds one u32 per fact slot:

- bit 31: pin (1 = never evict)
- bits 16..30: last-hit tick (15 bits, logical clock = header seq,
  bumped on every learn and every query)
- bits 0..15: query-hit count, saturating at 65535

Fact triples store (e_off, a_off, v_off) as raw string pool offsets.

## 3. S9: slot-level eviction

Frozen spec (18f3d2a5e). API:

- `s9_learn(W,e,a,v,pin)`: learn with pin flag 0/1. Returns slot index
  on success, -2 if the store cannot make room.
- `s9_query(W,e,a,out)`: latest-match query; on hit bumps use and tick.
- `s9_pin(W,e,a)`: pins the latest matching triple.
- `s9_compact(W)`: returns triples removed.
- `s9_evict_one(W)`: evicts one victim, returns slot or -1.

Two phases, run in order on a full store:

**Phase 1: compaction (semantics-preserving).** Keep only the last
triple per (e,a) key in slot order; remove earlier same-key triples and
exact duplicates. This changes no query result, because the query path
returns the latest matching triple, so removed triples were
unreachable. Survivors shift down preserving order; metadata shifts with
them. A pinned-but-superseded triple is still removed: pin protects
against eviction, not against being superseded.

**Phase 2: scored eviction.** If the store is still full after
compaction, evict exactly one victim: among unpinned slots, the victim
minimizes (use, tick) lexicographically (lowest query-hit count; ties
broken by oldest last-hit tick, i.e. LRU). Pinned slots are never
victims. If every slot is pinned, the learn fails with -2 and
learn_dropped increments.

Measured results (md5 9d9254db0c6fda04d1c022845d3df8e5):

- K2 world (cap 256, 500 mixed learns): learn_ok=500,
  learn_dropped=0, compact_count=100, evict_count=144,
  factcount=256, conflicts=100. Important accuracy 150/150 (50 imp +
  100 sup-new). Pinned survival 15/15 (10 imp + 5 junk). Victim order as
  predicted: junk{0..143} evicted, junk{144..249} present (including
  pinned junk{249}).
- Control (plain append-only store, same 500 learns): ok=256,
  dropped=244, 156 distinct live keys (100 slots wasted on dead
  superseded triples).
- S9 comparison: 500/500 learns accepted vs 256/500; 256/256 live keys
  retained vs 156.
- K3 world (cap 1024, 1200 learns): learn_ok=1200, dropped=0,
  compact=0, evict=176, factcount=1024. Important accuracy 300/300.
- Wall time: 28.9 s real (13.3 s user) for the full K2 + control + K3
  program, dominated by string-pool interning on thousands of queries.
  Engineering datum, not a threshold.

## 4. S10: byte-level string GC

Frozen spec (design fa9579074, prereg d23ca466a). `s10.zag` carries the
S9 substrate over verbatim (layout, eviction/compaction, query
semantics) and adds:

**Root analysis.** Liveness roots for the string pool are exactly the
three u32 offsets stored in each live fact slot (slots 0 through
factcount-1). Evidence: facts store offsets; `s9_query` copies value
bytes out and retains no offsets; conflict checks use `sub_streq`
(content comparison) and retain no offsets; episodes and entities hold
no string offsets in current builds; the meta region holds pin/tick/use
in a u32, not string references.

**Semantics preservation lemma.** Every consumer of a pool string goes
through `sub_streq` (content equality) or a byte copy of the value. No
consumer compares offsets for identity. Therefore replacing an offset
with another offset whose content is byte identical preserves all
observable behavior.

**Mechanism: `s9_strgc(W)`, mark-compact with content dedup.**

1. Mark: walk slots 0..factcount-1, collect the three offsets of each
   live slot into a root array (linear u32 array, at most 3*4096
   entries).
2. Compact+dedup: single in-place forward pass. Write pointer `ncur`
   starts at `str_base`; read pointer `p` scans to `str_cur`. Unrooted
   strings are dropped. Rooted strings are copied once per unique
   content (forward copy with ascending index; `ncur <= p` holds at
   every step, so unread source bytes are never overwritten);
   duplicates map to the existing copy. An (old,new) map table lives in
   a `z_alloc` buffer.
3. Rewrite: every live slot's three offsets are rewritten through the
   map; a missing map entry is a fatal internal error. Then
   `str_cur = ncur`, `gc_count++`.

**Triggers (frozen).**

- T1 (overflow-triggered): `sub_str` computes `need = p + 4 + s.len`.
  If `need > str_limit`, run `s9_strgc` once and retry; retry failure
  returns -1, which `s9_learn` converts to `learn_dropped++` / return
  -2 (existing full-store behavior). `s9_query`/`s9_pin` degrade to
  miss/fail on -1. This fixes the latent out-of-bounds write past
  `wsize` found in the S10 root analysis (the pool previously had no
  overflow check at all).
- T2 (explicit): `s9_strgc(W)` is callable directly, e.g. after a bulk
  eviction burst or before a checkpoint.

No background timer, no periodic trigger. GC runs only on demand or on
overflow pressure.

Measured results (md5 b94cbdcdbea4cb22010c9c7053ba35a1, exit 0,
zero stderr, 3/3 byte-identical):

- F1 PASS: query results byte-identical pre/post GC (20 hits + 5
  misses); conflict/evict/compact counters unchanged; gc_count 0 -> 1.
- F2 PASS: FNV-1a content hash over all slot-referenced strings
  identical pre/post (7232251642060297911). No live content lost.
- F3 PASS: str_cur 11383 -> 10621 (strictly decreased).
- F4 PASS: 500 learns of the identical ("eee","aaa","vvv") triple
  followed by GC collapse the pool to exactly 3 strings totaling 21
  bytes.
- F5 PASS: 1000 queries (no learns) followed by GC leave the pool byte
  count unchanged from pre-query count (all 2000 temp strings
  reclaimed).
- F6 PASS: a workload sized to overflow the pool completes; T1 fired
  (gc_count=2); final str_cur=10134 <= str_limit=16384;
  learn_dropped=0. No write past the limit.

## 5. S9/S10 interaction (K2)

The two mechanisms compose as slot-level and byte-level GC over the
same store. S9 does not compact the string pool; S10 does not compact
the meta region or the fact slots. Interaction contract:

1. **Ordering.** S10's mark phase reads roots from the live fact slots
   as left by S9 (post-compaction, post-eviction). The valid run order
   is S9 eviction/compaction first, S10 GC after; a GC rewrite between
   a compaction decision and its slot shift would invalidate offsets.
   In `s10.zag` the S9 code path runs to completion before any explicit
   or overflow-triggered `s9_strgc`.
2. **Root-set freshness.** Compaction shifts survivors down and drops
   superseded triples; eviction removes victim slots. Slots removed by
   S9 are simply absent from the S10 root set, so their referenced
   strings become unrooted and are reclaimed by the compact pass. No
   cross-notification is needed: liveness is re-derived from scratch on
   every GC.
3. **Shared header.** Offsets 72/76/80/84 (S9 counters) and 88/92 (S10
   fields) are distinct; both mechanisms update only their own fields.
   `gc_count` increments on every completed GC; `evict_count` and
   `compact_count` are untouched by S10 (F1 verified counters unchanged
   across GC).
4. **Semantics preservation, stacked.** S9 compaction is
   semantics-preserving because removed triples were unreachable under
   query-latest. S10 offset substitution is unobservable because all
   consumers are content-based (lemma, section 4). The stack is therefore
   behavior-preserving end to end, as F1/F2 verified.
5. **Byte accounting.** After an S9 eviction burst, the pool still holds
   the victim's strings until the next GC. After an S10 GC, the pool
   holds exactly the unique live strings. The two together bound both
   dimensions of growth: slots by max_fact and (use,tick) eviction,
   bytes by str_limit and dedup.
6. **Failure-mode sharing.** The T1 retry-failure path (`-1` from
   `sub_str`) funnels into the existing S9 full-store behavior
   (`learn_dropped++`, return -2). One drop counter covers both
   dimensions of pressure.
7. **Assumption both rely on.** Episodes and entities hold no string
   offsets. If a future build stores offsets there, S10's root set must
   be extended and F2 re-verified; S9 is unaffected (it reads triples,
   not pool content).

## 6. Performance characteristics

- S9 scale measured: 256-slot cap with 500 learns (all accepted, 144
  evictions) and 1024-slot cap with 1200 learns (all accepted, 176
  evictions). Wall time for the combined K2 + control + K3 program:
  28.9 s real (13.3 s user), dominated by string-pool interning on
  thousands of queries, not by eviction scoring.
- S10 cost bound (design-stage): mark is O(slots); the scan is
  O(pool_bytes) with per-string root membership O(roots) and content
  dedup comparison O(new_pool) in the linear-array implementation.
  Worst case quadratic with small constants (4096 slots max, pool
  bounded by workspace). GC is amortized: it runs at most once per
  overflow event, and each run reclaims a positive number of bytes, so
  total GC work over a run is bounded by
  O(total_bytes_interned * workspace_size).
- S10 measured: explicit GC on a 60-learn + 25-query workload collapsed
  str_cur 11383 -> 10621; 500 duplicate learns converged to 3 pooled
  strings / 21 bytes; 1000 query temps fully reclaimed (0 -> 0 bytes);
  overflow workload completed with str_limit=16384, str_cur=10134,
  zero drops.
- znc analyzer note (S10 build): 3 A0107 dead-loop warnings are
  heuristic false positives (pool scans advance by 4+l with l >= 0 on
  well-formed data); runtime verified by the passing falsifiers.

## 7. Limits and honest scope (K3)

1. **Researcher-authored policy, not learned.** The (use,tick) eviction
   score, the pin flag, the T1/T2 GC triggers, and the dedup policy are
   all researcher-authored. The claim is that the mechanism preserves
   what the learner marks important and discards the rest, not that the
   learner chose the policy. S9+S10 satisfy no part of Criterion 0 and
   are not an L3 claim. They are bounded engineering infrastructure.
2. **No intern-time dedup.** The hot path (`sub_str`) still interns
   every copy and collects the garbage later. Hash-consing at intern
   time would cut allocation traffic but changes the hottest function
   and needs a resident index; it is the named S11 candidate, rejected
   for S10 with reasons.
3. **No meta-region or slot compaction in S10.** Fact-slot layout and
   per-slot metadata are S9's job; S10 leaves them untouched.
4. **Tick field is 15 bits.** Bits 16..30 of the slot metadata hold the
   last-hit tick from the header logical clock (bumped on every learn
   and query). Hit counts saturate at 65535 by design. Long-run tick
   wraparound behavior is not specified or tested; runs to date stay
   far below 32767 clock ticks.
5. **Pin is coarse.** Pin protects a slot against eviction, not against
   being superseded by a later learn of the same key (a pinned-but-old
   triple is removed by compaction). Pin is also binary; there is no
   graded importance beyond use/tick.
6. **Query temps are GC-only reclamation.** The 2 throwaway interned
   copies per query/pin accumulate between GCs; only S10 reclaims them.
   Workloads with heavy querying between GCs carry transient pool
   bloat (measured: thousands of temps on the K2 workload shape, all
   reclaimed by one explicit GC).
7. **Episode/entity offset assumption.** Both the S9 design and the S10
   root analysis assume episodes and entities hold no string offsets.
   This is stated so the breakage is loud if a future build changes it.
8. **No cross-run persistence claim in this document.** S9+S10 manage
   live workspace memory. Checkpoint/restore of the substrate (including
   the new header fields) is a separate concern and was not tested in
   either phase.

## 8. What is closed, what is next

Closed: append-only slot growth (S9), monotonic string-pool growth
(S10), latent pool overflow write (S10 T1). The substrate now accepts
unbounded learns at fixed slot cap with (use,tick)-scored eviction and
reclaims both slots and bytes.

Next gaps, in order: (a) S11 intern-time dedup to cut hot-path
allocation traffic; (b) tick/hit-count policy review for very long runs
(limit 4); (c) graded importance beyond binary pin (limit 5);
(d) wiring the substrate into the continuing-learner integration track
(usage signals from real learner workloads rather than synthetic
junk/imp phases).

Kill bars: K1 PASS (architecture specified, sections 2-4). K2 PASS
(interaction documented, section 5). K3 PASS (limits and honest scope,
sections 7-8). Zero Python at every stage. Zero em/en-dash bytes
(byte-verified before commit).

Builder label: SUBSTRATE-DOCUMENTED.
