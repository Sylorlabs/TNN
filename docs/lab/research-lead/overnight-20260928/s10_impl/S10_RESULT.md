# S10 Result: String Pool Garbage Collection (mark-compact with dedup)

Verdict: BUILD-PASS. All four kill bars hold. No falsifier fires.

## Commits

- Prereg: d23ca466a (PREREG_S10.md, committed alone before any
  implementation file existed)
- Implementation + results: this commit (s10.zag, S10_RESULT.md,
  S10_RAW_1/2/3.txt, S10_ERR_1/2/3.txt, s10_build.err)
- Order: prereg strictly precedes implementation (verify with
  git merge-base --is-ancestor d23ca466a <this>)

## What was built (s10.zag, pure Zag, znc 2026.07.0-dev)

S9 substrate carried over verbatim (layout, S9 eviction/compaction,
query semantics). S10 adds:

- Header: offset 88 str_limit (stored wsize, set by sub_init9),
  offset 92 gc_count.
- s9_strgc(W): mark (root offsets from live fact slots), compact+dedup
  (single in-place forward pass, ncur <= p invariant, (old,new) map in
  z_alloc buffer), rewrite (slot offsets through map; missing entry is
  fatal). str_cur = ncur, gc_count++.
- sub_str overflow check (T1): need = p + 4 + s.len; if need > str_limit,
  run s9_strgc once and retry; retry failure returns -1, which
  s9_learn converts to learn_dropped++ / return -2 (existing full-store
  behavior). s9_query/s9_pin degrade to miss/fail on -1. This fixes the
  latent out-of-bounds write past wsize found in the S10 root analysis.
- T2: explicit s9_strgc(W) call.

## Results (3/3 byte-identical, md5 b94cbdcdbea4cb22010c9c7053ba35a1,
exit 0, zero stderr on all runs)

F123 world (60 learns + 20 conflicting dup learns + 25-query suite,
explicit GC between BEFORE and AFTER):

- F1 PASS: query results byte-identical pre/post (20 hits + 5 misses);
  conflicts/evict/compact counters unchanged; gc_count 0 -> 1.
- F2 PASS: FNV-1a content hash over all slot-referenced strings
  identical pre/post (7232251642060297911).
- F3 PASS: str_cur 11383 -> 10621 (strictly decreased).

F4 world (500 learns of identical ("eee","aaa","vvv") triple, then GC):

- F4 PASS: pool collapses to exactly 3 strings totaling 21 bytes
  (12 + 3 + 3 + 3), as predicted.

F5 world (1000 queries, zero learns, then GC):

- F5 PASS: pool byte count 0 -> 0 (all 2000 temp strings reclaimed).

F6 world (500 learns, 64-slot store, 16384-byte workspace sized to
force pool overflow):

- F6 PASS: T1 fired (gc_count=2), run completed, final str_cur=10134
  <= str_limit=16384, learn_dropped=0. No write past the limit.

## Kill bars

- K1 PASS: prereg d23ca466a committed alone before implementation.
- K2 PASS: s9_strgc implemented per the frozen mechanism.
- K3 PASS: F1-F6 all pass, 3/3 deterministic.
- K4 PASS: pure Zag (znc + shell + git + grep only); zero Python
  invocations at every stage; zero non-ASCII/em-dash bytes in source
  and logs (shell byte-verified); exit 0; empty stderr.

## Notes

- znc analyzer emits 3 A0107 dead-loop warnings (heuristic false
  positives: pool-scan loops advance by 4+l with l >= 0 from
  well-formed pool data). Build succeeds; runtime behavior verified
  by the passing falsifiers.
- s10_bin left untracked (not committed), matching the S9 convention.
- Honest scope: triggers, header layout, and dedup policy are
  researcher-authored infrastructure. S10 satisfies no part of
  Criterion 0 and is not an L3 claim. Composes with S9 (S9 frees
  slots, S10 frees the bytes they referenced).

Builder label: BUILD-PASS.
