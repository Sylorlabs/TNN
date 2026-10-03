# PREREG: L2-INTERFERENCE (clean restart)

Frozen 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: L2-INTERFERENCE clean-restart worker. Worktree at
~/workspace/lane-l2-interference (sparse), detached at tnn-native-lab tip
533706483 (branch tnn-native-lab itself is checked out by another
worker's locked worktree, so detached-at-tip is the closest compliant
checkout; exact tip hash recorded). Commits local only, never pushed.
Pure Zag for all scientific computation; shell only for znc invocation,
binary execution, git ops, and file movement. Pinned compiler
src/tools/toolchain/znc_linux_x86_64_abed8aa1.

## Objective

When a continuing learner holds several L2-adapted structures in one
shared memory and then learns a new structure that reuses some of the same
content keys with different values, does using or revising one structure
degrade another? Protocol: teach structure family A, pre-test A, teach
structure B, re-test A, measure retention. A conflict-relocation policy is
the mechanism under test: it is supposed to protect A under moderate
overlap and to saturate under total overlap.

## Substrate (frozen)

Single file l2_interference.zag, self-contained, no dependency on any
prior lane. All state in one []u8 workspace, i32 little-endian cells via
put32/ig helpers.

- Primary store: W = 128 slots. Slot layout (16 bytes): key i32, val i32,
  owners i32 bitmask (up to 8 structures), used i32 flag.
- Overflow: F = 8 slots, same layout, circular bump pointer. This is the
  conflict-relocation pool.
- Hash: h(key) = ((key as i64 * 2654435761) mod 2147483647) mod 128.
  Linear probe on collision.
- write(key, val, owner): probe from h(key) for matching key or an empty
  slot. Same key and same val: owners |= owner (no conflict). Same key
  and different val: CONFLICT. Empty slot: store (key, val, owner).
- On CONFLICT: copy the existing entry into overflow[ov_ptr],
  ov_ptr = (ov_ptr + 1) mod 8, conflicts += 1; if the overwritten overflow
  slot was in use, evictions += 1. Then store the new (key, val, owner)
  in the primary slot.
- read(key, owner): probe the primary chain for key; scan all 8 overflow
  slots for key. Among candidates whose key matches, return the val of the
  first candidate whose owners bitmask includes owner (primary candidate
  preferred). No owner match: MISS (-1). All stored vals are nonneg, so
  -1 is unambiguous.
- Output: all text formatted into one preallocated buffer with
  cursor-returning emit helpers (e1s/e1i), then a single
  _zag_raw_syscall(1, 1, ptr, len) write. No _zag_print for dynamic
  content. No `as *i32` slice construction in functions. if nesting at
  most 3. No `!(A && B)` in while conditions (De Morgan form instead).

## Learned structures (frozen)

Owner bits: A_BASE=1, A_EXT=2, A_SPEC=4, A_TRUNC=8, B=16.
Content keys for the A family: ka(i,hop) = 1000 + i*10 + hop,
i in 1..10, hop in 1..3. Values: va(i,hop) = i*100 + hop*7.

- A_BASE (2-hop chain, 10 examples, 20 entries):
  (ka(i,1), va(i,1)), (ka(i,2), va(i,2)) for i=1..10.
- A_EXT = EXTEND(A_BASE, third hop): shares A_BASE's 20 (key,val) pairs
  (owner bit A_EXT added, no conflict since vals equal) plus 10 new
  entries (ka(i,3), va(i,3)).
- A_SPEC = SPECIALIZE(A_BASE, examples 1..5, guard): the 10 (key,val)
  pairs of examples 1..5 (owner bit A_SPEC) plus 5 guard entries
  (2000+i, 9000+i) for i=1..5.
- A_TRUNC = TRUNCATE(A_BASE): hop-1 pairs only (owner bit A_TRUNC).
- B = interface-adapted generic 2-hop template, 10 examples x 2 hops.
  Interface map phi varies by condition:
  - NULL (0 percent overlap): kb(i,hop) = 3000 + i*10 + hop, disjoint.
  - PARTIAL (25 percent): 5 of B's keys reuse A's keys with different
    vals: (ka(1,1), ka(1,2), ka(2,1), ka(2,2), ka(3,1)) with
    val = 777000 + i*10 + hop; the other 15 keys are disjoint
    (3000 + i*10 + hop).
  - FULL (100 percent): all 20 of B's keys equal ka(i,hop) with
    val = 777000 + i*10 + hop.
  B's conflicting writes are value SUBSTITUTIONs on shared content keys.

Distinct (key,val) pairs held by the learner in the multi-structure
condition before B: 20 (base) + 10 (ext third hop) + 5 (spec guards) = 35.

## Queries (frozen)

- A_BASE query i: read(ka(i,1), A_BASE)==va(i,1) and
  read(ka(i,2), A_BASE)==va(i,2). 10 queries.
- A_EXT query i: 3 reads against va(i,1..3). 10 queries.
- A_SPEC query i (i=1..5): read(2000+i)==9000+i and the 2 base reads.
  5 queries.
- A_TRUNC query i: read(ka(i,1), A_TRUNC)==va(i,1). 10 queries.
- Total 35 queries multi-structure; 10 in the single-structure ablation
  (A_BASE only).
- B sanity queries (reported, not kill-barred): 20 reads with owner B.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace:
1. teach A family (multi: A_BASE, A_EXT, A_SPEC, A_TRUNC) or A_BASE only
   (ablation).
2. pre-test: count pre_ok.
3. teach B with the condition's interface map.
4. post-test: count post_ok; retention = 100 * post_ok / pre_ok.
5. record conflicts, evictions, B accuracy.

Conditions: multi+NULL, multi+PARTIAL, multi+FULL, single+PARTIAL.

## Frozen kill bars

- K1 baseline validity: pre_ok == total queries in every condition
  (35/35 multi, 10/10 single). Else BUILD-FAIL (substrate broken); no
  verdict on interference is drawn.
- K2 main: multi+PARTIAL retention >= 90 percent (post_ok >= 32/35).
- K3 null control: multi+NULL retention == 100 percent (35/35).
- K4 positive control (instrument sensitivity): multi+FULL retention
  <= 75 percent (post_ok <= 26/35). If FULL retention exceeds 75 percent,
  the instrument cannot demonstrate interference and the verdict is VOID.
- K5 determinism: 3/3 runs byte-identical (sha256 equal). Else VOID.
- K6 ablation: single+PARTIAL retention >= 90 percent (post_ok >= 9/10)
  AND |ret_multi_partial - ret_single_partial| <= 10 percentage points.

Verdict: PASS iff K1..K6 all hold. Any kill-bar miss names the bar and
yields FAIL. K4-sensitivity or K5 failure yields VOID. Thresholds are
frozen; they are not moved after results.

## Predicted (not bars)

PARTIAL: 5 conflicts, overflow holds 8, all relocated, retention 100
percent both multi and single. NULL: 0 conflicts, retention 100 percent.
FULL: 20 conflicts in B teaching order ka(1,1), ka(1,2), ..., ka(10,2);
circular overflow keeps the last 8 relocations, so A's entries for
ka(1..6, *) are lost: A_BASE 4/10, A_EXT 4/10, A_SPEC 0/5, A_TRUNC 4/10,
overall 12/35 = 34 percent, within the K4 bound.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(l2_interference.zag), build, runs, and REPORT.md only after.
