# ROOTCAUSE_A — KB-Control Crew A: root-cause audit + write-path map

**Date:** 2026-09-23. **Crew:** KB-Control Crew A. **Prereg:** `PREREG_KBCONTROL_CREWA.md`
(frozen, commit `667ddc63b52a2e13efe430c112e535b2b4f505b5`, before any results).
**Scope:** the two 1GB-ingest blob defects (D1 padding miscount, D2 RT-G3 silent
cross-fact destruction) in `knowledge/ingest_1gb/build/ingest.zag`. No fixes land
in this crew's commits.

## 0. Root cause in one paragraph

Both defects are the same accounting error in two places: the blob writer's
`total` counter counts **record bytes only** and never the **inter-chunk
zero-padding**. In `igb_append` (`build/ingest.zag:822,833`) the returned/stored
global offset is `off = b.*.total` advanced by `reclen`, while the chunk-rollover
branch zero-pads `IG_BLOB_CHUNK - used` bytes and flushes *without adding the
padding to `total`* — so after the first rollover every recorded slot offset is
short by the accumulated padding (100% of post-boundary slots wrong), and
`revise`/`delete` via `sc_recall` fail closed on them. In `ig_revise`
(`build/ingest.zag:1807`) the blob tail is reconstructed arithmetically as
`bb.used = btotal % IG_BLOB_CHUNK`; because `btotal` excludes all padding, this
undercounts the true tail usage of the final chunk by `(accumulated padding mod
CHUNK)` — 126 bytes in the red-team run — so the "successful" revise writes the
new record 126 bytes too early, silently overwriting the last 126 real data
bytes of the final chunk and destroying an unrelated fact. The store then
persists the still-wrong `total`, so the corruption compounds on every revise.

## 1. Reproducer

`kb_repro.zag` — minimal, self-contained, pure-Zag. It implements the
blob-writer formulas **verbatim** from `build/ingest.zag` (the `igb_append`
rollover/total logic, `ig_revise`'s `bb.used` reconstruction, the
`[1B kind][4B id LE][2B klen BE][4B tlen BE][key][text]` record layout),
parameterized to `CHUNK=4096` so two boundaries are crossed with 100 records.
Chunk size changes only padding magnitudes, never the formulas. Zero RNG.

Geometry: key=8B, text=90B → `RECLEN=109`; 37 records/chunk; 63B padding per
rollover. Chunk 0 = ids 0–36, chunk 1 = ids 37–73, chunk 2 = ids 74–99
(2834 B). `btotal` after ingest = 10900; buggy `bb.used` = 10900 % 4096 = 2708;
true tail usage = 2834; undercount = **126** — the same number as the red team's
RT-G3 run (their 1,499,994 vs 1,500,120).

Protocol (pre-committed in the prereg): (1) append 100 records, recording each
returned offset; (2) offset census — parse the header at each recorded offset;
(3) geometric walk at true `chunk*CHUNK+in` offsets (sindex-style), proving the
bytes are fine and only the accounting is wrong; (4) revise pre-boundary id=5
via the buggy tail reconstruction; (5) post-revise verification + byte-diff of
the final chunk over the real-data region; (6) two runs from clean outdirs,
byte-identical, hash-chained.

Results (both runs byte-identical; evidence SHA
`e335718a0074ca8797651689eaa0525ca7c0a5119fdb2985af76e7192663e753`,
chain in `RUNLOG.md`):

```
census wrong_pre=0/37 wrong_post=63/63          # D1: 100% post-boundary wrong
walk_true_geometry parsed=100/100 bad=0         # bytes fine; accounting wrong
revise id=5 rc=0 rused_buggy=2708 rused_true=2834 undercount=126
revise id=50 via recorded offset: REFUSED id_mismatch (fail closed)   # H3/G2
verify id=5 new text at true_off=10900 OK       # revise "succeeds"
verify id=99 at true_off=10917 MISSING (header destroyed)              # D2
clobber first=2708 last=2833 count=125
verify id=98 tail damaged: yes (17 text bytes)
verdict D1=REPRODUCED D2=REPRODUCED
```

Prereg-deviation note (honest): A4's sub-prediction said "exactly 126 bytes
changed". The clobber **span** is exactly the predicted 126 bytes
`[2708,2834)`; the differing-byte **count** is 125 because position 2719
coincidentally holds `0x6B` ('k') in both old and new content. H2 is confirmed
on the span and the destruction, not the byte count. Second deviation: the
126-early write also eats the last **17 text bytes of record 98** (any write
starting at 2708 necessarily does — the damage is not confined to the single
tail record). Both deviations strengthen, not weaken, the finding.

Hypothesis verdicts: **H1 CONFIRMED** (0/37 pre-boundary wrong, 63/63
post-boundary wrong; geometric walk 100/100 intact). **H2 CONFIRMED** (revise
rc=0; unrelated fact id=99 destroyed; clobber span exactly the predicted 126
bytes). **H3 CONFIRMED** (post-boundary revise via recorded offset fails
closed; pre-boundary revise succeeds-but-destroys; delete never reads a blob
offset — structural, from source; query unaffected — structural, sparse.idx is
geometric).

## 2. The exact arithmetic error

**D1 — `igb_append`, `build/ingest.zag:808-836`.** The counter is `b.*.total`,
documented as "total record bytes appended (= next global offset)". Two lines:

- `:822` `let off:i64=b.*.total;` — the returned/stored global offset.
- `:833` `b.*.total=off+(reclen as i64);` — advanced by the record length only.

The rollover branch (`:815-821`) zero-pads `IG_BLOB_CHUNK - used` bytes and
flushes, but never adds the padding to `total`. Invariant violated:
`total` should equal `nchunk*IG_BLOB_CHUNK + used` (the true on-disk end); it
instead equals the sum of record bytes. After `k` rollovers every offset is
short by `Σ pad_i`. Red-team numbers check out exactly: one rollover with
126 B padding → `btotal % CHUNK` = 1,499,994 vs true 1,500,120.

**D2 — `ig_revise`, `build/ingest.zag:1807`.** `bb.used=(btotal%(IG_BLOB_CHUNK))
as i32;` reconstructs the final chunk's tail usage from the padding-blind
`btotal` instead of measuring the chunk. `btotal % CHUNK = (true_used -
accumulated_padding) mod CHUNK`, which undercounts by
`(accumulated_padding mod CHUNK)` whenever that doesn't exceed `true_used`
(the normal case; if it wrapped, `used` would overshoot into the padding region
instead). `igb_append` then writes at the too-small `used`. Note the same
undercount also corrupts the rollover branch's zero-pad loop if a revise
triggers a second rollover (`while(p<cur.len){cur[p]=0;...}` would zero real
tail data), and the recorded `new_off = btotal` plus the re-persisted `total`
carry the error forward into `store.dat` and `overrides.dat`.

## 3. Full write-path map

Paths in `build/ingest.zag`. "Padding?" = does offset/length accounting include
inter-chunk padding. "Bounds?" = is there a guard. "Mode" = fail-closed vs
silent on violation.

| # | Path | Padding? | Bounds? | Mode |
|---|---|---|---|---|
| 1 | `igb_append` — record append (ingest `ig_process_lesson` + `ig_revise` share it) | **NO (D1)** — `:822`/`:833` | rollover check yes; **no oversize-record guard**: `reclen > IG_BLOB_CHUNK` would write past `cur` (heap overflow). Latent: max real `reclen` = 11+160+4096 = 4267 ≪ 33,488,896 | **silent** — wrong offsets stored, no error |
| 2 | Rollover branch inside `igb_append` (`:815-821`) | pads but **doesn't count** (the D1 line) | — | silent |
| 3 | `igb_flush_full` — chunk file write | n/a (doesn't touch `total`) | write rc → `-1` | fail-closed on IO error |
| 4 | `igb_finish` — final pad + flush | pads final chunk; doesn't touch `total` (correct iff `total` were right) | — | — |
| 5 | `ig_revise` tail reconstruction (`:1802-1809`) | **NO (D2)** — `:1807` | none on the reconstructed `used` | **SILENT DESTRUCTION** of other facts' bytes |
| 6 | `ig_revise` append + chunk rewrite | inherits D1+D2 | none | silent; compounds (wrong `total` re-persisted) |
| 7 | `ig_revise` override update (`ig_ovr_save`) | stores wrong `new_off` (downstream) | `ocnt>=4096` → "too many overrides" | fail-closed on count; **silent** on wrong offset; file is read-modify-write with no locking (concurrent-revise race, latent — CLI is single-threaded) |
| 8 | `ig_delete` | n/a — **never reads a blob offset** (flags + rechain + reseal only) | id range, already-deleted guards | fail-closed; **SAFE w.r.t. padding** (G4) |
| 9 | `ig_ovr_load` — overrides reader | n/a | `cnt>maxn` → `-1`; short file → 0 | fail-closed |
| 10 | `ig_store_save` — persists `blob_total`/`blob_nchunk`/`blob_recs` | persists the wrong `total` (downstream of D1/D2) | write rc checked | **silent propagation** |
| 11 | `ig_store_load` — restores tail | trusts persisted `total` | magic + read-length checks | fail-closed on corrupt header; **silently trusts** a wrong-but-well-formed `total` |
| 12 | `sc_add` — slot table store | stores the wrong `off` (downstream of D1) | `id>=ncap` → `-1` (in `ig_process_lesson`) | silent |
| 13 | `sc_compact_and_seal` — slot-chunk compaction + chain | n/a — slot bytes only, **never touches blob bytes** | alloc checked | fail-closed; SAFE w.r.t. blob bytes |
| 14 | `sc_seal_tail` | n/a | **NO idempotency guard** — 2nd call: `nsealed` 1→2, chain[0] rewritten | **silent state corruption** → sets up #15 (RT-H) |
| 15 | `sc_seal_final` | n/a | none — reads `chain[(nsealed-1)*32..]` OOB after a double seal | **LOUD panic** (`slice index out of bounds`) in checked builds; would hash heap garbage into the seal in an unchecked build (RT-H) |
| 16 | `ig_sindex` — sparse.idx writer | **YES — geometric `ci*CHUNK+off`, correct** | entry-overflow + key-order guards | fail-closed; **CORRECT, unaffected** (why query works) |
| 17 | `ig_open_write` | n/a | O_WRONLY\|O_CREAT\|O_TRUNC (577), **no O_EXCL** — rewrites land (AGENTS.md silent-failure lesson already applied) | — |
| 18 | checkpoint/resume | **ABSENT in the port** (grep-confirmed; the stale-checkpoint incident was Wiktionary extraction, not this binary) | — | n/a |
| 19 | `ig_lookup` / `ig_query` / `ig_bquery` (read paths) | use sparse.idx (correct) + linear scan; overrides applied last | parse-fail → error/NOTFOUND | fail-closed; **blast radius**: D2-destroyed bytes can break the linear scan (`rl<0` → "lookup error") |

Unsafe for cross-fact byte damage: **#1, #2, #5, #6** (padding accounting),
**#14/#15** (seal, different bug), **#1** (missing oversize guard),
**#7** (no locking). Downstream propagators (wrong but not themselves
damaging): #10, #11, #12. Safe: #3, #4, #8, #9, #13, #16, #17.

## 4. What "count padding in total" fixes vs what needs more

**Fixed by counting padding in `total`** (add `IG_BLOB_CHUNK - used` on
rollover, or compute the offset as `nchunk*CHUNK + used`):

- #1/#2 (D1): all future slot offsets correct; `revise`/`delete` via
  `sc_recall` unblocked for post-boundary slots.
- #5 (D2): **but only for stores built with the fix.** With a correct
  `btotal`, `btotal % CHUNK` equals the true tail usage, so `bb.used` becomes
  right. On an *old* store the persisted `btotal` is still wrong, so a revise
  would still destroy — **rebuild is required** (as the FINDINGS already state);
  a fix without a rebuild leaves a live data-destruction path.
- #6, #7, #10, #11, #12 transitively (they propagate the corrected counter).

**NOT fixed by counting padding — needs more:**

- #1's missing oversize-record guard: needs an explicit
  `reclen <= IG_BLOB_CHUNK` fail-closed check (padding counting doesn't add it).
- #14/#15 (seal): needs an idempotency guard in `sc_seal_tail` and/or a bounds
  check in `sc_seal_final` — unrelated to padding (RT-H).
- #7's read-modify-write race on `overrides.dat`: needs locking/atomic rename.
- `ig_blob_name`'s 6-digit chunk index: silently collides past 999,999 chunks
  (latent, unrelated to padding).
- **Structural (Micah's "conscious control" bar):** even with padding counted,
  `ig_revise` *trusts* `btotal` from `store.dat` and derives `used`
  arithmetically instead of *measuring* the chunk (parse the tail / verify the
  zero-padding region). Defense in depth: verify `bb.used` against the actual
  chunk bytes before writing. Further gaps: no pre-write snapshot of the chunk
  being rewritten; blob chunk file is rewritten **before** `store.dat` is
  saved (crash in between = disagreeing blob and index, no write-ahead
  discipline); no post-revise verification that untouched records still parse.
  The write path never checks its own work — that is the construction-level
  hole behind "silent cross-fact destruction", and padding arithmetic alone
  does not close it.

## 5. Files

- `PREREG_KBCONTROL_CREWA.md` — frozen prereg (commit `667ddc63`, pre-results)
- `kb_repro.zag` — reproducer source (the binary `kb_repro` is NOT committed)
- `RUNLOG.md` — hash-chained run log (binary SHA, evidence SHAs, chunk SHAs)
- `run1/`, `run2/` — evidence logs + chunk images (byte-identical across runs)
- `ROOTCAUSE_A.md` — this file

All under `docs/lab/knowledge/kb_control/crewA/`.
