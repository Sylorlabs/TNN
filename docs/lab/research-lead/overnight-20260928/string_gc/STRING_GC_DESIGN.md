# S10 Design: String Pool Garbage Collection

Design only. No implementation. Addresses the gap noted in
SUBSTRATE_SCALE_RESULT.md: S9 reclaims fact slots, not string bytes; the
string pool grows monotonically.

## 1. Problem

The substrate string pool is a bump allocator. `sub_str(W, s)` writes a u32
length followed by the bytes at `h_strcur(W)` and advances the cursor. There
is no dedup, no free list, and no overflow check.

Measured leak behavior in s9.zag:

- Every `s9_fact_learn` interns 3 fresh copies (e, a, v), even for byte
  identical content learned before.
- Every `s9_query` and `s9_pin` interns 2 throwaway copies (e, a) used only
  for comparison, then abandoned.
- S9 compaction and eviction remove fact slots, but the strings those slots
  referenced remain in the pool permanently.
- `sub_str` never checks the workspace bound. A long enough run writes past
  `wsize` into unowned memory. This is a latent memory safety bug, not just
  a capacity issue.

Consequence: pool bytes grow roughly linearly with total learn plus query
count, while live unique content stays small. On the K2 workload (500
learns, hundreds of queries), the pool holds thousands of duplicate and
abandoned strings after S9 has reclaimed every dead slot.

## 2. Root analysis

Liveness roots for the string pool are exactly the three u32 offsets stored
in each live fact slot (slots 0 through factcount minus 1). Evidence:

- Facts store (e_off, a_off, v_off) as raw pool offsets in the fact region.
- `s9_query` copies value bytes out to a caller buffer; it retains no
  offsets.
- Conflict checks use `sub_streq` (content comparison); they retain no
  offsets.
- Episode and entity regions are reserved in the layout but hold no string
  offsets in any current build (counts stay 0).
- Meta region holds pin/tick/use in a u32, not string references.

Semantics preservation lemma: every consumer of a pool string goes through
`sub_streq` (content equality) or a byte copy of the value. No consumer
compares offsets for identity. Therefore replacing an offset with another
offset whose content is byte identical preserves all observable behavior.

## 3. Mechanism: mark-compact with content dedup (S10)

### 3.1 State additions (header, backward compatible)

- Offset 88: `str_limit` (u32). Stored copy of `wsize`, set once by
  `sub_init9`. Previously `wsize` was a parameter that was never retained.
- Offset 92: `gc_count` (u32). Number of string GC cycles run. Diagnostic,
  same family as `evict_count` and `compact_count`.

### 3.2 Mark phase

Walk slots 0..factcount-1. For each slot read its three offsets
(e_off, a_off, v_off). Collect them into a root set. Duplicates in the root
set are expected and harmless; the set is small (3 * factcount entries max,
4096 slots max, so at most 12288 roots).

Implementation note for the future builder: a linear array of u32 roots is
sufficient. No hash table is required.

### 3.3 Compact and dedup phase (single in-place forward pass)

Maintain a write pointer `ncur` starting at `str_base`, and a read pointer
`p` scanning from `str_base` to `str_cur`. Maintain a map table of
(old_offset, new_offset) u32 pairs in a `z_alloc` buffer (outside the
workspace, same as existing test helpers).

For each string at `p` with length `l`:

1. If `p` is not in the root set: drop it. Advance `p` by 4 + l.
2. If `p` is in the root set: check whether identical content has already
   been copied to the new pool (compare against the bytes between
   `str_base` and `ncur`, or keep a parallel list of copied contents).
   - If yes at new offset `q`: append (p, q) to the map. Advance `p`.
   - If no: copy the 4 + l bytes from `p` to `ncur`. The copy is forward
     (destination at or below source) with ascending index, so unread
     source bytes are never overwritten. Append (p, ncur) to the map.
     Advance `ncur` by 4 + l, advance `p` by 4 + l.

In-place safety: `ncur <= p` holds at every step because the new pool only
shrinks relative to the old scan position (we copy at most what we scan,
and drops make `ncur` lag further behind). The read of length at `p`
happens before any write near `p`.

### 3.4 Rewrite phase

For each live slot, look up its three offsets in the map table and write
back the new offsets. Every live slot offset must appear in the map; a
missing entry is a fatal internal error (fail loudly, do not proceed).

Then set `str_cur = ncur` and increment `gc_count`.

### 3.5 Trigger conditions (frozen)

- T1 (overflow-triggered): `sub_str` computes `need = p + 4 + s.len`. If
  `need > str_limit`, run `s9_strgc` once and retry. If the retry still
  exceeds the limit, return -1 to the caller; `s9_fact_learn` then records
  `learn_dropped++` and returns -2, matching the existing full-store
  behavior. This also fixes the latent out-of-bounds write.
- T2 (explicit): `s9_strgc(W)` is callable directly, e.g. after a bulk
  eviction burst or before a checkpoint.

No background timer, no periodic trigger. GC runs only on demand or on
overflow pressure.

### 3.6 Cost bound (structural)

Mark is O(slots). The scan is O(pool_bytes). Root membership per string is
O(roots) with the linear array; content dedup comparison is O(new_pool)
per string. Total is quadratic in the worst case but with small constants
(4096 slots, pool bounded by workspace size). GC is amortized: it runs at
most once per overflow event, and each run reclaims a positive number of
bytes, so total GC work over a run is bounded by O(total_bytes_interned
* workspace_size), acceptable for a design-stage bound. The future
implementer may add an intern cache to make dedup O(1) amortized; the
frozen falsifiers do not depend on it.

## 4. Safety argument (K2)

Claim: no live string content is lost or altered by `s9_strgc`.

1. A string is live iff its offset is referenced by a live fact slot
   (section 2 root analysis; episodes and entities hold no string
   references in current builds).
2. Every live offset enters the root set (mark phase visits every live
   slot).
3. Every rooted string is either copied to the new pool (first occurrence
   of its content) or mapped to an existing copy of byte identical content
   (dedup branch). In both cases the map holds a valid new offset whose
   content equals the old content.
4. Every live slot has all three offsets rewritten through the map
   (rewrite phase visits every live slot; missing map entries are fatal).
5. All consumers are content based (semantics preservation lemma), so the
   substitution is unobservable.

Therefore post-GC query results, conflict counts, and pin behavior are
identical to pre-GC.

## 5. Effectiveness bound (K3)

After `s9_strgc` completes:

- `str_cur - str_base` equals the sum of (4 + len) over the unique live
  strings. All duplicate copies and all unreferenced strings are gone.
- `str_cur` never increases across a GC (monotonic non-increase).
- On the S9 K2 workload shape (500 learns of heavily repeated content
  plus query temps), the pool collapses to at most one copy per unique
  live string. Repeated learns of the same triple converge to exactly 3
  pooled strings regardless of learn count.
- Query-temp strings are always reclaimed: a query-only workload leaves
  the pool unchanged after GC.

What S10 does not do: it does not reduce the number of `sub_str` calls
(the hot path still interns then collects). Intern-time dedup would cut
allocation traffic but touches the hot path; it is rejected for S10 and
noted as optional future work.

## 6. Frozen falsifiers for the future implementer

- F1: 3/3 byte identical stdout on a learn/query/pin workload run before
  and after an explicit `s9_strgc` (query results, conflict counts,
  evict/compact counters unchanged except `gc_count` incrementing by 1).
- F2: content hash over all slot-referenced strings is identical before
  and after GC (no live content lost).
- F3: `str_cur` after GC <= `str_cur` before GC on every run.
- F4: 500 learns of the same (e,a,v) triple followed by GC leaves at most
  3 strings totaling 12 + len(e) + len(a) + len(v) bytes in the pool.
- F5: 1000 queries (no learns) followed by GC leaves pool byte count
  unchanged from the pre-query count (all temps reclaimed).
- F6: a workload sized to overflow the pool completes without writing
  past `str_limit` (T1 fires; previously this corrupted memory).

## 7. Alternatives rejected

- Reference counting: would require inc/dec on every learn, query, pin,
  evict, and compact path, including the query-temp interning that
  currently has no free site. Invasive across the hot path; rejected.
- Intern-time dedup (hash-consing in `sub_str`): cuts allocation traffic
  and is the better long term answer, but changes the hottest function in
  the substrate and needs a resident index structure. Rejected for S10;
  kept as named future work (S11 candidate).
- Larger pool / bigger workspace: raises the ceiling without changing the
  growth curve. Rejected as treadmill.
- GC on a timer or every N learns: steady state cost with no pressure
  signal. Rejected; triggers are demand driven (T1) or explicit (T2).

## 8. Honest scope

- The trigger conditions, header layout, and dedup policy are
  researcher authored. S10 is infrastructure, like S9 and the verification
  subsystem: it satisfies no part of Criterion 0 and is not an L3 claim.
- S10 does not compact the meta region or the fact slots themselves; slot
  level GC remains S9's job. The two compose: S9 frees slots, S10 frees
  the bytes those slots referenced.
- Episodes and entities are assumed to hold no string offsets. If a future
  build stores offsets there, the root set must be extended and F2
  re-verified; this assumption is stated here so the breakage is loud.
- Design only. No implementation, no measurements, no verdicts claimed.
