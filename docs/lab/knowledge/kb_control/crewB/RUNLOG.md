# KB-CONTROL CREW B — Run Log

## 2026-09-24: Implementation and debugging

### Build
- `kbctl.zag` + `kbcore.zag` + `kbcfg.zag` compiled on the pinned toolchain
  (`znc_linux_x86_64_abed8aa1`) on the first attempt. Two analyzer warnings
  (discarded `kb_find_prev` return values); no errors.

### Defects found and fixed during bring-up
1. **`kb_find_prev` not-found sentinel**: returned "not found" without setting
   `poff=-1`; caller's default `poff=0` caused a phantom predecessor check.
   Fixed by explicitly setting `poff=-1, plen=0, pid=0` on not-found.
2. **Journal reconstruction**: `kb_load` seeded `total` from `store.dat` then
   tried to replay intents staged against `tb=0`. Fixed: authoritative
   rebuild from zero; `store.dat` is informational only.
3. **Rollover adoption order**: `kb_apply_intent` validated `(nb,tb)` before
   adopting the trailer-backed chunks needed to reach `off`. Fixed: adopt
   chunks first, then validate.
4. **`k_rename` syscall**: used 38 (x86-64 `rename`), which returns EINVAL on
   this VM. Switched to `renameat(264)` with AT_FDCWD, which works.
   (Toolchain/environment quirk; also fixed a 6-vs-7 arg miscount.)
5. **Journal sequence restoration**: `kb_load` set `jseq=mc+1` (max committed
   intent seq + 1), colliding with the commit's own seq. Fixed: track
   `maxseq` over all entries, `jseq=maxseq+1`.
6. **History builder buffer overrun**: pass A read 13 bytes then `k_g64`
   at offset 9 (4 bytes past the buffer). Fixed to read the full 17.
7. **`k_pread_full` length semantics**: reads `buf.len`, not a passed length.
   Pass B checked `!=9` on a 17-byte buffer. Fixed the check.
8. **Fast-mode init**: `kb_init` didn't create `slotdir.dat`; `kb_load_fast`
   rejected the fresh store. Fixed: init writes an empty slotdir.
9. **`get` ignored `--mode`**: fixed to pass mode through to `kb_get`.
10. **DIRTY detection**: `kb_journal_scan` didn't flag intact uncommitted
    intents. Fixed: track max intent seq; `dirty=1` if `mi>mc`.
11. **Checkpoint atomicity**: `kb_store_save` now uses temp+fsync+rename+
    dir-fsync.

### T4 crash battery (2026-09-24)
- 20 trials × 3 crash points (after-journal, after-data, after-commit) ×
  put/revise = **120 trials, 120 pass, 0 fail**.
- Every trial: crash → verify (DIRTY for points 1-2) → recover → verify OK →
  data integrity confirmed (all facts readable, revised text correct).
- Fail-closed confirmed: no trial left the store corrupt or lost committed data.

### Rollover accounting bug (2026-09-24, found by T1)
- `kb_rollover` did `total = total + CHUNK`, but `total` already included
  `cur_used` bytes (invariant: `total == nchunks*CHUNK + cur_used`).
  After 37 puts (total=4012), rollover set total=8108 instead of 4096.
  The V1 tripwire (`off != nchunks*CHUNK+cur_used`) caught it fail-closed.
- Fixed: `total = (nchunks+1)*CHUNK` after increment (cur_used=0).
- **Second bug**: `kb_apply_intent` checked `nb==nchunks` BEFORE the rollover
  synthesis that adopts the chunk, making synthesis dead code. Moved the
  (nb,tb) check to after synthesis.
- **Third**: removed premature `kb_adopt_orphans` from `kb_load`; the journal
  replay adopts flushed chunks on demand via trailer-checked synthesis.
  A chunk file without a journal intent is uncommitted crash debris and is
  ignored (journal is the source of truth).
- **Fourth (trailer seq overlap)**: `kb_rollover` wrote the 4-byte chunk seq
  at `ch-12`, overlapping the 8-byte `used` field at `ch-16`. The trailer
  layout is `[used:8][seq:4][magic:4]`; seq belongs at `ch-8`, not `ch-12`.
  The overlap corrupted `used` (e.g. 3993 became 4294971289) and set seq=0
  for chunk 1, causing replay to reject the trailer. Fixed the offset.

## 2026-09-24: T1–T3, T5–T6 (in progress)

### T1: 20,000 deterministic conscious appends
- Batch file: `work/t1_batch.txt` (20k `put` ops, `gen:` lengths 20–199B,
  deterministic via SHA-256).
- **COMPLETE**: 20,000 ops in 48m41s (~6.85 ops/sec).
- Verify: `CENSUS mode=conscious slots=20000 live=20000 hist=0 chunks=560
  records=20000 data=2249032` → OK.
- Ledger: 20,000 entries, digest=
  `d6677da6e220e2e09be94254798d9f383fab5dfbb3892a221b88498f553b5e75`.
- Zero cross-slot clobbers (K1 holds for T1).

### T2: 1,000 revisions (500 near-boundary + 500 arbitrary)
- Batch file: `work/t2_batch.txt`.
- **BUG FOUND**: `kb_field_is` advances `fp` via `kb_next_field` even on
  mismatch. In `kb_batch`, after the "put" check fails, `fp` is already
  past the first field, so the "revise" check starts mid-line and fails.
  Fixed by resetting `fp=0` before each alternative ("revise", "delete").
- **COMPLETE**: 1,000 revises in 4m21s.
- Verify: `CENSUS mode=conscious slots=20000 live=20000 hist=1001 chunks=588
  records=21001 data=2361550` → OK.
  (hist=1001 includes one manual revise of id=1 done during debugging.)
- Ledger: 21,001 entries.
- Zero cross-slot clobbers (K1 holds for T2).

### T3: 200 deletes + 200 re-adds
- Batch file: `work/t3_batch.txt`.
- **BUG FOUND**: Re-add (put on tombstoned id) orphans the old record.
  The put intent did not include the old offset/len/hash, so
  `kb_hist_from_journal` could not account for the deleted version.
  Census failed with `unaccounted`.
- **FIX**: `kb_do_put` now includes the old triple (77..120) in the put
  intent when re-adding (payload 121+rl vs 77+rl). `kb_apply_intent` and
  `kb_hist_from_journal` handle the extended format.
- The earlier T1+T2+T3 store (work/t1) has the old-format journal and
  cannot verify. Redoing as three clean T5 runs with the fixed binary.

### T5: three byte-identical complete runs (T1+T2+T3)
- Runs: `work/t5a`, `work/t5b`, `work/t5c`.
- Each: 20k puts + 1k revises + 200 deletes + 200 re-adds, then verify.
- **ALL THREE COMPLETE**:
  - `CENSUS mode=conscious slots=20000 live=20000 hist=1200 chunks=594
    records=21200 data=2384940` → OK.
  - Ledger: 21,400 entries, digest=
    `0ad62e0a630aa966593a3a6686e4dfe8abb68655df134f97eb7ae4c2607dcf49`
    (identical across all three).
  - **BYTE-IDENTICAL**: SHA-256 of all 598 store files (content only):
    `69961a9da848bc54` for t5a, t5b, t5c.
- K3 SATISFIED.

### T5: three byte-identical runs
- Pending T1 completion.

### T6: conscious vs fast head-to-head
- Pending.
