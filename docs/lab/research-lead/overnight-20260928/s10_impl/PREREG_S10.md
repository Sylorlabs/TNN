# PREREG: S10 String Pool Garbage Collection Implementation

Committed alone before any implementation file exists.
Design reference: commit fa9579074
(string_gc/STRING_GC_DESIGN.md, 205 lines).
S9 base: commit 83b78a781 (substrate_scale/s9.zag).

## Mechanism (from design, frozen)

`s9_strgc(W)` implements mark-compact with content dedup:

- Mark: collect the 3 offsets (e_off, a_off, v_off) of every live fact
  slot (0..factcount-1) into a root array.
- Compact+dedup: single in-place forward pass. Write pointer ncur starts
  at str_base; read pointer p scans str_base..str_cur. Unrooted strings
  dropped; rooted strings copied once per unique content (forward copy,
  overlap-safe since ncur <= p always). An (old,new) map table lives in
  a z_alloc buffer. Dedup by content comparison against bytes already
  copied to the new pool.
- Rewrite: every live slot's 3 offsets rewritten through the map; a
  missing map entry is fatal. Then str_cur = ncur, gc_count++.
- Header: offset 88 stores str_limit (u32 copy of wsize, set by
  sub_init9); offset 92 stores gc_count.
- Triggers: T1 overflow-triggered (sub_str computes need = p + 4 + s.len;
  if need > str_limit, run s9_strgc once and retry; retry failure returns
  -1, s9_fact_learn records learn_dropped++ and returns -2). T2 explicit
  s9_strgc(W) call.

## Frozen falsifiers (F1-F6)

- F1: 3/3 byte-identical stdout on a learn/query/pin workload run before
  and after an explicit s9_strgc. Query results, conflict counts, and
  evict/compact counters unchanged; gc_count increments by exactly 1.
- F2: content hash over all slot-referenced strings identical before
  and after GC (no live content lost).
- F3: str_cur after GC <= str_cur before GC on every run.
- F4: 500 learns of the same (e,a,v) triple followed by GC leaves at
  most 3 strings totaling exactly 12 + len(e) + len(a) + len(v) bytes
  in the pool.
- F5: 1000 queries (no learns) followed by GC leaves pool byte count
  equal to the pre-query count (all temp strings reclaimed).
- F6: a workload sized to overflow the pool completes without writing
  past str_limit (T1 fires; the pre-S10 code corrupted memory here).

## Kill bars

- K1: this prereg committed alone before implementation.
- K2: s9_strgc implemented per the frozen mechanism above.
- K3: F1-F6 all pass, 3/3 byte-identical runs.
- K4: pure Zag (znc + shell + git only), zero Python invocations, zero
  em/en-dash bytes in source and logs, deterministic.

## Predicted outcomes

- F1 PASS: stdout identical except gc_count line.
- F2 PASS: hash identical.
- F3 PASS: str_cur strictly decreases on duplicate-heavy workloads.
- F4 PASS: exactly 3 strings, 12 + le + la + lv bytes.
- F5 PASS: pool byte count returns to pre-query count.
- F6 PASS: overflow workload completes; learn_dropped may increment on
  retry failure; no write past str_limit.

Verdict rule: BUILD-PASS iff K1-K4 all hold and no falsifier fires.
Any falsifier firing yields BUILD-FAIL with the failing mechanism named.
