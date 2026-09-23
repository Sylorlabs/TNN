# AUDIT VERDICT — 1GB Ingestion Store (sealed)

Branch: `tnn-native-lab` · Date: 2026-09-23 · Auditor: Muse (subagent)
Prereg: `knowledge/ingest_1gb/audit/PREREG_AUDIT.md`
Prereg commit: `7bab8109e2e9e6f2783bb9be5e29819470229111` (2026-09-23, committed BEFORE any new battery ran)
Report under audit: `knowledge/ingest_1gb/REPORT.md` @ `ebcb273b57e932354ae3b67cac4ebc897596bed6`
Frozen ingest source blob: `f46d340862bf4f68842d803971d87557acd91b27`
Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Verdict summary

| Check | Result |
|---|---|
| A1 facts census (C1–C3) | **PASS** — 3,707,990 records, 0 inversions, 539,418 adjacent dupes; source bins sum exactly |
| A2 pure-Zag gate replay | **PASS** — 57/57 lesson lines byte-identical to audit.log; g1=0/g2=462,263/g3=58,846; 2,597,057 installed |
| A3 events / audit cost / tombstones | **PASS** — 66 events (57×tag-7 + 9×tag-8), zero other tags; 0 tombstones in 2,597,057 slots |
| A4 seal-tail idempotency | **VIOLATION CONFIRMED** — ingest `sc_seal_tail` re-seals on second call (nsealed 635→636); canonical is idempotent. PORT_EQUIV.md's "trailing whitespace only" claim is **false** |
| A5 rebuilt byte-identical rerun | **PASS** — rebuilt binary → byte-identical store.dat, manifest, audit.log, 12 blob chunks, rebuilt sparse.idx; identical seal |
| A6 sparse-index integrity | **PASS** — 2,548/2,548 entries valid, strictly sorted, all 2,597,057 blob records reachable |
| E2 revisions (corrected, slot-based) | **FAIL — blocked by store defect** (see §E2/E3) |
| E3 deletions (corrected, slot-based) | **FAIL — blocked by store defect** (see §E2/E3) |
| Report §2 merge paragraph | **FALSE** — input was 3,707,990 (not 4,247,408); 539,418 dupes were counted but NOT removed |
| Determinism (zero randomness) | **PASS** — rebuilt binary byte-identical across builds; rerun artifacts byte-identical by SHA |
| store_full / facts.bin mutation | **NONE** — re-hashed after all batteries, unchanged |

**Headline:** the sealed 1GB store is **sound for reads**. Every mechanism the report claims (gate counts,
seal, lesson accounting, index coverage, deterministic rebuild) replays exactly in independent
pure-Zag code. **But the store has a critical defect**: the S5 slot→blob-offset values are wrong
for all records in blob chunks 1–11 (2,398,865 slots, 92% of the store), because `igb_append`
never counted inter-chunk zero-padding in `b.*.total`. This breaks `revise` and `delete`
(which use `sc_recall`) for those slots — E2/E3 **cannot pass** on the sealed store as specified.
The `query` path is unaffected (it uses the sparse index, which has correct offsets).

Two report defects: (1) the §2 merge/dedup paragraph is factually wrong — the
dedup was a counted no-op and the "4,247,408 input" number is phantom (it equals output + dupes);
(2) PORT_EQUIV.md mischaracterizes the `sc_seal_tail` divergence, which is a real missing
idempotency guard (demonstrated, not just diffed). The original E2/E3 ID-space blocker is
**diagnosed and the fix validated** (slot-based sampling works where offsets are correct);
the full 100+100 run fails only because of the blob-offset defect below.

---

## A1 — facts.bin census (C1, C2, C3)

Program: `audit/audit_census.zag` (pure Zag, independent record parser).

| File | records | inversions | adj. dupes |
|---|---|---|---|
| `run/facts.bin` | 3,707,990 | 0 | 539,418 |
| `run/wn.bin` | 117,789 | 1 | 0 |
| `run/wikt.bin` | 821,558 | 250,237 | 1,545 |
| `run/wiki.bin` | 2,768,643 | 154,305 | 0 |
| **source sum** | **3,707,990** | — | — |

- **C1 PASS**: source bins sum to exactly 3,707,990 = facts.bin count.
- **C2 PASS**: facts.bin has 0 sort inversions (merge output sorted).
- **C3 PASS**: 539,418 adjacent duplicate keys = `merge_stats.txt` `duplicate_keys=539,418`.
- Cross-check: independent Python census of `run/tiny.bin` agreed with the Zag binary
  (`n=706 inversions=0 dupes=0` both).
- The 1 inversion in `wn.bin` and unsorted `wikt.bin`/`wiki.bin` are pre-merge extraction
  order; the merge sorts. Not a defect.

## A2 — independent pure-Zag gate replay

Program: `audit/audit_replay.zag`. Gate functions (`ig_key_eq`, `ig_has_sub`, `ig_key_word`,
`ig_gate`, `ig_cal_bad`) copied **verbatim** from the frozen `build/ingest.zag`; the lesson
harness (peek-4 / CAL dry-run / drain-and-drop / prev_key staleness / counting) written
independently from `INGEST_DISK_FORMAT.md` + prereg.

Result:
```
REPLAY lessons=57 rejected=9 inst=2597057 g1=0 g2=462263 g3=58846
```
- All **57 per-lesson lines byte-identical** to `run/store_full/audit.log`
  (`diff`: 57/57 identical, including `inst=`/`g1=`/`g2=`/`g3=` counts per lesson).
- Rejected lessons + masks: `3:1, 14:1, 23:1, 28:1, 31:1, 39:1, 43:15, 48:8, 50:4` —
  exactly the nine masks recorded from audit.log before the prereg froze.
- Gate totals match REPORT: g1=0, g2=462,263, g3=58,846; installed=2,597,057.
- `slot2pos.bin` emitted: n=2,597,057, strictly increasing, all positions in
  `[0, 3707990)`. SHA `678f948fa30d2533a254c366f7f2712dc17966c0264b830e95d8e7d5b78a595f`
  (kept in `audit/`, not committed — build artifact).

## A3 — events, audit cost, tombstones

Program: `audit/audit_events.zag` (pure Zag, read-only).

```
EVENTS total=66
tag7=57 tag8=9 other=0 stages0..56_in_order=1 pos_nondecreasing=1
reject-lessons: 3:1 14:1 23:1 28:1 31:1 39:1 43:15 48:8 50:4
TOMBSTONES scanned=2597057 deleted_bit0=0
```
- Exactly the preregistered 66 events: 57 tag-7 episode events (stages 0..56 in order,
  slot positions non-decreasing) + 9 tag-8 lesson-rejects with the exact lesson/mask pairs
  from A2. **Zero** tag-1 (add-fail), tag-9 (revise), tag-10 (delete), tag-11 (cal-fail):
  no per-G2/G3 reject events, no audit-cost events beyond the episode/reject records.
- Tombstone scan over all 2,597,057 sealed slots: deleted-bit = 0 everywhere.
- `store.dat` SHA unchanged after the read (`e98f85c8…`).

## A4 — seal-tail idempotency (VIOLATION)

Program: `audit/audit_seal.zag` (pure Zag, in-memory only — `store_full/` never written).

```
BASELINE              n=2597057 nsealed=635 seal=3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87
ingest seal_tail rc=0
AFTER-INGEST-SEALTAIL n=2597057 nsealed=636 seal=3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87
canon seal_tail rc=0
AFTER-CANON-SEALTAIL  n=2597057 nsealed=635 seal=3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87
```

- The ingest `sc_seal_tail` (verbatim from frozen `build/ingest.zag`) is **not idempotent**:
  a second call on the sealed store appends a 636th chunk (`nsealed` 635→636). The canonical
  `adopt/s5_store.zag` version — which carries the `if(n/cs < nsealed) return 0;` guard
  (ported as commit `7303b6db`) — returns 0 with state untouched.
- Baseline seal `34867163…e87` matches REPORT's seal exactly.
- `store.dat` on disk untouched (`e98f85c8…` before and after).
- **PORT_EQUIV.md is wrong**: it claims `sc_seal_tail` differs "only in trailing whitespace".
  The missing idempotency guard is a behavioral divergence, demonstrated empirically here —
  a second seal call mutates the store (and would change the finalized seal: the chain
  gains a 636th entry, so the chain head moves).
- Note: the committed `adopt/s5_store.zag` already carries the fix; the ingest copy does not.
  Legacy `s4/s5_learner.zag` copies remain unguarded (superseded, unreferenced — see memory).

## A5 — rebuilt byte-identical rerun

- Rebuilt `audit/ingest_bin_audit` from the frozen source with the pinned toolchain.
  The pinned toolchain is deterministic: two consecutive rebuilds are byte-identical.
  (The rebuilt binary differs from the committed `build/ingest_bin` — different size and
  embedded addresses — so the committed binary was **not** produced by the pinned toolchain
  from the frozen source; recorded as a provenance gap, not a determinism failure.)
- Reran from `knowledge/ingest_1gb/` with identical relative argv:
  `ingest run/facts.bin run/bad.bin run/store_rerun 4078789` →
  `ingest done inst=2597057 seal=3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87`
  (seal matches REPORT).
- SHA comparison `run/store_rerun` vs `run/store_full`: **store.dat, manifest.txt,
  audit.log, all 12 blob_*.dat IDENTICAL**. Rebuilt `sparse.idx` in the rerun
  (`sindex done entries=2548`) → **IDENTICAL** to baseline.
- AK4 input hashes recorded in `audit/AK4_hashes.txt` before the rerun
  (facts.bin `0a566aa3…`, bad.bin `ffd2e69b…`, all store artifacts).

## A6 — sparse-index integrity (full scale)

Program: `audit/audit_index.zag` (pure Zag, read-only).

```
IDX entries=2548
IDX2 strictly_sorted=1
IDX1 expected_entries=2548 actual=2548 match=1
BLOB records=2597057 chunks=12
IDX3 entry_target_bad=0
IDX4 unreachable_records=0
```
- IDX1: entry count exactly equals #{records with id%1024==0 or first-in-chunk} (2,548).
- IDX2: entries strictly increasing by key.
- IDX3: all 2,548 entries point at real blob records with byte-matching keys.
- IDX4: **all 2,597,057 blob records reachable** — binary search for the greatest entry
  ≤ record key yields `goff ≤ record goff` for every record, so the fallback lookup's
  forward scan reaches each one.
- This is a strictly stronger check than E1's spot lookups: full coverage, not samples.

## E2/E3 — root cause, fix, results

**Root cause** (diagnosed 2026-09-23, confirmed in this audit): `extract/gen_eval.py`
generated fixture IDs as **positional indexes into facts.bin** (`(i*n)//100`, n=3,707,990),
but `revise`/`delete` accept **installed-slot IDs** (0..2,597,056). The two spaces diverge
because 9 lessons were CAL-rejected (589,824 records) and 521,109 records were gate-rejected
(1,110,933 dropped total). Concrete instance from `slot2pos.bin`:
- old E2 passed positional ID **37079** → `revise` treated it as slot 37079 → revised the
  fact at facts position **40,705** (wrong fact);
- the intended fact (facts position 37,079) lives at installed slot **33,760**;
- the old E2 then queried position-37079's key → hit unrevised slot 33,760 → "failure".

**Fix** (frozen in prereg): replay the gate in pure Zag to build `slot2pos.bin`
(installed slot → facts.bin position), then sample **directly in installed-slot space**.
Per prereg: E2 slots `s_i=(i·N)//100`, E3 slots `t_i=(i·N)//100+N//200` (N=2,597,057).

**New blocking defect found during the E2 run (CRITICAL):** the sealed store's S5
slot→blob-offset values are **incorrect for all records in blob chunks 1–11**.

Root cause: `igb_append` (build/ingest.zag) returns `b.*.total` as the record's global
blob offset, but `b.*.total` is only incremented by `reclen` per record — it never
accounts for the zero-padding at the end of each 33,488,896-byte blob chunk.
When a chunk fills, `igb_append` zero-pads the remainder and flushes, but `total`
stays short by the padding length. Every subsequent chunk's offsets are therefore
too low by the cumulative padding.

Measured (by walking all 12 blob chunks):
| chunk | padding (bytes) | cumulative offset error for later chunks |
|---|---|---|
| 0 | 40 | 40 |
| 1 | 125 | 165 |
| 2 | 81 | 246 |
| 3 | 148 | 394 |
| 4 | 27 | 421 |
| 5 | 19 | 440 |
| 6 | 120 | 560 |
| 7 | 203 | 763 |
| 8 | 467 | 1,230 |
| 9 | 24 | 1,254 |
| 10 | 43 | 1,297 |

Concrete: slot 207764's record is truly at blob offset 34,980,177, but `store.dat`
stores 34,980,137 (40 bytes low = chunk-0 padding). `revise` does `sc_recall` →
reads the wrong offset → `ig_blob_parse_hdr` yields garbage id → "revise: id mismatch
at offset" → refuses (fails closed, no corruption).

Scope: blob chunk 0 (198,192 slots) has correct offsets; chunks 1–11 (2,398,865 slots,
**92.4% of the store**) have wrong offsets. `revise`/`delete` (via `sc_recall`) fail
for all of them. `query`/`bquery` are **unaffected** — they resolve through `sparse.idx`,
which was built by scanning the blob and carries correct offsets (A6 verified).

**E2/E3 outcome per prereg bars:**
- E2 (100 slots `(i·N)//100`): only the 8 slots < 198,192 (blob chunk 0) revise
  successfully; the other 92 fail with "id mismatch at offset". **Bar 100/100: FAIL.**
- E3 was not run to completion once the defect was characterized (same `sc_recall`
  path; identical failure mode).
- Diagnostic (not the prereg battery): 7/7 revises on chunk-0 slots succeeded with
  exact text+ID verification via `query`, confirming the revise **mechanism** is sound
  where the stored offsets are correct. (An 8th was interrupted by premature cleanup
  of the diagnostic copy, not by the mechanism.) The failure is purely the stored-offset defect.

Per prereg AK3, this verdict is the written statement of what blocks E2/E3: **the
sealed store's S5 blob offsets are wrong for 92% of slots due to the `igb_append`
padding bug; E2/E3 cannot pass until the ingest is fixed and the store rebuilt.**
The original ID-space confusion is resolved; the mechanism is proven on correct offsets.

**Fix required (ingest source, not the sealed store):** in `igb_append`, when rolling
to a new chunk, add the padding length to `b.*.total` (or compute `off` as
`b.*.nchunk*IG_BLOB_CHUNK + used`). The sealed store cannot be repaired in place —
the offsets are baked into 635 sealed chunks.

## Violations found

0. **CRITICAL — S5 blob offsets wrong for 92% of slots (store defect)** — `igb_append`
   (build/ingest.zag) does not count inter-chunk zero-padding in `b.*.total`, so the
   blob offsets stored in `store.dat` are too low by the cumulative padding for all
   records in blob chunks 1–11 (2,398,865 slots). `revise`/`delete` via `sc_recall`
   fail for these slots ("id mismatch at offset", fails closed). `query` unaffected
   (sparse.idx has correct offsets). E2/E3 **cannot pass** on the sealed store.
   Fix: count padding in `b.*.total` in `igb_append`; store must be rebuilt.
   (Full characterization in §E2/E3 above.)
1. **REPORT §2 merge paragraph (factual)** — claims "4,247,408 input → 3,707,990 unique
   merged, 539,418 removed (12.7%)". Truth: merge input was 3,707,990 (source bins sum
   exactly); output was 3,707,990; `duplicate_keys=539,418` were **counted but not removed**
   (`extract/merge_sort.py` writes every record unconditionally; facts.bin contains all
   539,418 adjacent dupes, 0 inversions). 4,247,408 = 3,707,990 + 539,418 (phantom input);
   12.7% = 539,418/4,247,408. True dupe rate in the merge input: 14.55%.
   The report also carries a stale duplicated draft fragment after §7 (repeated §§3–7
   with "pending" markers) — editorial, not technical.
2. **PORT_EQUIV.md `sc_seal_tail` claim (factual)** — "differs only in trailing whitespace"
   is false; the ingest copy lacks the `nsealed` idempotency guard. Demonstrated: second
   call re-seals (nsealed 635→636). Canonical copy already fixed (commit `7303b6db`).
3. **Committed `build/ingest_bin` provenance gap** — not reproducible from the frozen
   source with the pinned toolchain (differs in size/embedded addresses; two pinned
   rebuilds are byte-identical to each other). The rebuild's *artifacts* are byte-identical
   to the original run's, so this does not affect store determinism.

## Determinism verdict

**PASS — zero randomness, byte-identical reruns proven by SHA.**
- Pinned-toolchain rebuilds are byte-identical to each other.
- Full ingest rerun from the same inputs produced byte-identical `store.dat`,
  `manifest.txt`, `audit.log`, all 12 blob chunks, and rebuilt `sparse.idx`
  (seal `34867163…e87` both runs).
- Independent pure-Zag replay of all 57 lessons reproduced `audit.log`'s lesson lines
  byte-for-byte (57/57).
- No RNG in any audit program; all sampling deterministic (`(i·N)//100` strides).

## Mutation check

`run/store_full/store.dat` SHA `e98f85c8600417e2…` — identical before the first battery
(AK4), after A3/A4 (read-only programs), and after all batteries. `run/facts.bin`
`0a566aa3…` unchanged. E2/E3 ran on the disposable copy `run/store_audit_e23/`.

## Artifacts committed with this verdict

- `knowledge/ingest_1gb/audit/AUDIT_VERDICT.md` (this file)
- `knowledge/ingest_1gb/audit/PREREG_AUDIT.md` (already committed @ `7bab8109e2…`)
- `knowledge/ingest_1gb/audit/audit_census.zag`
- `knowledge/ingest_1gb/audit/audit_replay.zag`
- `knowledge/ingest_1gb/audit/audit_seal.zag`
- `knowledge/ingest_1gb/audit/audit_events.zag`
- `knowledge/ingest_1gb/audit/audit_index.zag`
- `knowledge/ingest_1gb/audit/AK4_hashes.txt`
- `knowledge/ingest_1gb/audit/replay_full.log` (57 lesson lines + summary)
- `knowledge/ingest_1gb/audit/index_full.log`
- `knowledge/ingest_1gb/audit/e23_run.log`
- `knowledge/ingest_1gb/audit/gen_e23_fixtures.py`, `run_e23.py` (glue)
- `knowledge/ingest_1gb/audit/e2_targets.tsv`, `e3_targets.tsv`, `neighbors.tsv`,
  `neighbor_texts.tsv` (fixtures)

Not committed (per prereg): `slot2pos.bin`, `ingest_bin_audit`, `audit_*` binaries,
`run/store_rerun/`, `run/store_audit_e23/`, `e23` tmp files.
