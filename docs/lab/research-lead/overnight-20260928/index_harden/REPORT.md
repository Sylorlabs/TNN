# REPORT.md -- Index Hardening Worker

## Verdict: INDEX-HARDEN-COMPLETE

The redteam's index-robustness BREAK is fixed with GENERAL invariants,
not a fixture patch. All four corruption types handled gracefully,
3/3 deterministic per type, zero regression on uncorrupted worlds.

## 1. The vulnerability (frozen, read-only)

`rebind_try_idx` in `../scaling_index/si_patch.zag` walked plen-bucket
linked lists with no validation:

```zag
let m:i32=ng(W,ix,idx_bfield(q));
while(m>=0 && nc<1024){
  hs(W,56,hg(W,56)+1);
  set32(cand,nc*8,m); set32(cand,nc*8+4,q);  // cand is 4096 bytes = 512 entries
  nc=nc+1;
  m=ng(W,m,12);                              // no bounds check on m
}
```

Three defects:
1. No bounds check: `ng(W,m,12)` with corrupt `m` reads past the workspace.
2. No cycle detection: a bucket cycle grows `nc` without bound.
3. Wrong buffer bound: `nc<1024` allows writes past the 512-entry buffer.
   (2)+(3) = the redteam's crash: cycle drives `nc` past 512,
   `set32` writes out of bounds, `panic: slice index out of bounds`.
4. No liveness/type check: evicted MAPs and non-MAP nodes enter as
   candidates blindly.

## 2. The fix (unfrozen): `idx_walk_bucket` in `ih_patch.zag`

Four GENERAL invariants, checked in dependency order (each check reads
only state that earlier checks proved safe to read):

- **I1 BOUNDS**: `m` in `[2, NN())`. A corrupt head or next pointer
  outside the node table would make `ng(W,m,*)` read past the workspace.
  Violation: stop this bucket. Nothing past a corrupt link is trusted.
- **I2 CYCLE**: `m` not already visited in this bucket traversal
  (per-bucket seen bitmap, `NN()*4` bytes, indexed by node id).
  Any cycle shape (self-loop, 2-cycle, n-cycle, lollipop, shared tail,
  dead-node cycle) revisits a node; the bitmap catches every one.
  Violation: stop; all distinct reachable nodes are already collected.
- **I3 LIVENESS**: `ng(W,m,36)==1` (the same field `alloc_node` /
  `evict_node` maintain). Evicted slots are dead; their field 12 may
  hold garbage from slot reuse. Violation: skip the entry but keep
  walking, so one stale entry does not hide live entries behind it.
- **I4 TYPE**: `ng(W,m,0)==T_MAP` (20). Only MAP nodes belong in MAP
  buckets. Violation: skip, keep walking (same reasoning as I3).
- **I5 BUFFER**: `nc<512` enforced by the walk condition. `cand` is
  4096 bytes at 8 bytes per entry; collection past capacity is
  statically impossible.

The index root is validated before any bucket head is read
(bounds + tag 40). The scan counter (header 56) still counts every
bucket visit, preserving the honest cost accounting. The candidate
sort and trial nest are untouched.

## 3. Invariant proofs

**Termination.** Each walk iteration either breaks (I1/I2/I5) or marks
one new node visited and advances. At most `NN()` distinct nodes exist,
so at most `NN()` iterations occur before I2 fires. The walk always
terminates, including on dead-node-only cycles (the trap that a
skip-without-visited-set design would loop on forever).

**Memory safety.** Every `ng(W,m,*)` is preceded by I1, so
`noff(m) = 64+m*40` stays inside the node region. Every
`set32(cand,nc*8,*)` has `nc<=511`, so the offset is `<=4095 < 4096`.
Every `seen[m*4]` access has `m<NN()`, so the offset is `< NN()*4`
(the allocated size). No out-of-bounds read or write is reachable.

**No legitimate candidate is lost.** On uncorrupted state: entries are
in-bounds node ids (I1 passes), the bucket is a linear list built by
prepend-only `idx_add` (I2 never fires), entries are live (I3 passes;
evicted entries are stale by definition), entries are tag-20 MAPs
(I4 passes; `idx_add` only indexes promoted MAPs). Verified empirically:
hardened output is byte-identical to the original on all uncorrupted
scaling worlds (section 5).

**Generality.** No invariant references a specific corruption value,
node id, or fixture layout. Bounds derive from `NN()`; liveness from
the allocator's own field; type from the node tag; cycles from the
mathematical definition (revisit). Any corruption of these four kinds,
in any bucket, any position, any shape, is handled.

## 4. Corruption tests: 4 types x 3 variants x 3 runs

Driver: `ih_driver.zag`. Each world builds 3 plen-5 chain MAPs, teaches
query facts, applies corruption to the plen-5 bucket, then queries.
Binary run 3x; all 3 outputs byte-identical (cmp clean).

| Type | Variant | Corruption | Result (3/3) |
|------|---------|-----------|--------------|
| T1 CYCLE | v0 | redteam exact break: head next -> head | ok=1, scan=1, no crash |
| T1 CYCLE | v1 | 2-cycle below head: H->A->B->A | ok=1, scan=3, no crash |
| T1 CYCLE | v2 | dead-node cycle: H->D1<->D2 (both evicted) | ok=1, scan=3, no crash, terminates |
| T2 NONMAP | v0 | redteam C1: live FACT prepended | ok=1, scan=4, no crash |
| T2 NONMAP | v1 | FACT spliced mid-list | ok=1, scan=4, no crash |
| T2 NONMAP | v2 | index node (tag 40) as bucket entry | ok=1, scan=2, no crash |
| T3 OOB | v0 | redteam C3: head next -> 9999 | ok=1, scan=1, no crash |
| T3 OOB | v1 | bucket head itself = 9999 | ok=1, scan=0, no crash, graceful fallback |
| T3 OOB | v2 | boundary: head next = 1024 | ok=1, scan=1, no crash |
| T4 STALE | v0 | head MAP evicted (dead, next intact) | ok=1, scan=3, no crash |
| T4 STALE | v1 | all 3 bucket MAPs evicted | ok=1, scan=3, no crash, fallback answers |
| T4 STALE | v2 | slot reused: dead MAP reborn as FACT, next=777 | ok=1, scan=2, no crash |

Clean baseline (no corruption): ok=1, scan=3, 3/3 identical.

Score: 12/12 variants x 3/3 runs = 36/36 worlds correct, zero crashes,
zero nondeterminism. Per corruption type: 3/3 deterministic.

## 5. Regression proof (no behavior change when uncorrupted)

- `ih_control_bin` (ORIGINAL vulnerable `rebind_try_idx` + same driver):
  clean worlds give `ans=6205 ok=1 scan=3`, identical to hardened;
  then T1v0 crashes with `panic: slice index out of bounds`,
  reproducing the redteam BREAK. This proves the test detects the bug
  and the fix is what removes it.
- `ih_scale_bin` (hardened patch + original `si_driver.zag`) output is
  BYTE-IDENTICAL to the original `si_bin` output across all scaling
  worlds (LIN10/50/100, IDX10/50/100): same answers, same tried/
  rejected verifies, same scan visits. The C193 verify-count invariant
  is preserved exactly.

## 6. Files

- `ih_patch.zag`: hardened index patch (replaces `si_patch.zag`;
  adds `idx_walk_bucket`, hardens `rebind_try_idx`).
- `ih_driver.zag`: 4-type corruption test driver.
- `build.sh`: assembly script (mirrors `../scaling_index/build.sh`).
- `ih_full.zag`: assembled test source.
- `ih_bin`: hardened test binary.
- `ih_control_bin`: vulnerable control binary (proves test sensitivity).
- `ih_scale_bin`: hardened patch on the original scaling driver.
- `ih_run_1/2/3.txt`: 3 deterministic hardened runs (byte-identical).
- `ih_control_run1.txt`: control run (clean OK, T1v0 panics).
- `ih_scale_run1.txt`: hardened scaling-driver output.
- `ih_compile.txt`: build log.

## 7. Notes and follow-ups

- The stale-pointer case (T4) is handled by graceful degradation:
  dead entries are skipped, live ones behind them are still found
  (skip-not-break), and fully-stale buckets fall through to the base
  miss path which still answers. The index never corrupts the answer.
- Buffer capacity (512 candidates) is a pre-existing mechanism limit,
  unchanged by this fix; the fix only makes the bound correct.
- The `seen` bitmap costs `NN()*4` bytes per walked bucket per query
  (4 KB at 1024 nodes); negligible against the scan work it guards.
- Toolchain guard: safebin active for all builds/runs;
  `which python3 python` returns nothing. Pure Zag throughout.
