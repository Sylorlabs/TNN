# PREREG_R2 — Exhaustion-cap repair (ONE-BRAIN + SELF-PAM residual #2 of 4)

**Status: FROZEN on commit to tnn-native-lab (2026-09-24).** No edits without
a prereg amendment. This prereg freezes the repair design, the load-bearing
justification for every remaining bound, and the kill bars. Implementation
follows only after this commit lands.

## 0. Residual under repair

From `redteam/RESULTS.md` (residual #2), all in `sp_gate.zag`:

- **R1** — `SP_LEDGER_CAP=1024`: post-cap `SP_L_VERDICT` rows silently
  dropped (decision executes, notifies, but is never ledgered).
- **R2** — `SP_DSP_CAP=64`: 65th distinct claim → instant `SP_ESCALATE` on
  first withhold (escalation inflation, overseer-inbox flood).
- **R3** — `SP_QUAR_CAP=128`: ledgered `SP_L_QUARANTINE` while
  `sp_quarantined()==0` (phantom quarantine — ledger asserts what never
  happened).
- **R4** — `SP_INST_CAP=128`: post-cap installs dropped from the index;
  conflict check goes blind on unindexed entries (silent conflict miss).

In-scope adjacent defects of the same class (found while scoping the
repair): `SP_OVR_CAP=256` (overseer inbox silently drops entries when
full) and `SP_IPOOL_SZ=16384` (installed-claim text pool silently drops
atom text → textless entries are invisible to `sp_conflict_check`, the
same defect class as R4).

Frozen inputs: `~/workspace/onebrain_pam_integration/PREREG.md` (DO NOT
MODIFY), `redteam/RESULTS.md`, `redteam/ATTACK_LOG.md`. The three
`sp_gate.zag` copies (build/redteam/longhorizon `src/`) are byte-identical
(SHA-256 `d86262240338264df9544c84fe9becc71a0d2d7ed28efe5cc0ec90d8c66e24a2`)
and are repaired identically.

## 1. Repair design: chunked unbounded tables

Every capped table becomes a **chunked unbounded table**. Chunk capacity
is derived from the genuine load-bearing limit — the znc
2^25-bytes-per-slice toolchain ceiling (a single slice > 33,554,432 bytes
panics on ANY index; `~/AGENTS.md`). Logical capacity is unbounded
(chunks allocated on demand, chained); physical chunks are sized strictly
under the ceiling.

### Frozen parameters

- `SP_CHUNK_ROWS = 65536` rows per chunk, all five tables.
- Row layouts (little-endian i32 fields, `ob_s32`/`ob_g32` accessors —
  the ZNC-2026-09-21-007 `[]u8`-arena workaround, no `as []i32` casts):
  - ledger: 16 B `{ep,code,a1,a2}` → chunk **1,048,584 B**
  - dispute: 12 B `{org,key,count}` → chunk **786,440 B**
  - quarantine: 12 B `{org,key,line}` → chunk **786,440 B**
  - installed: 20 B `{org,weight,cseq,off,alen}` → chunk **1,310,728 B**
  - overseer inbox: 16 B `{ep,org,key,rson}` → chunk **1,048,584 B**
- Atom-text pool (replaces the fixed `G_IPOOL`): chunks of
  `SP_POOL_CHUNK = 1048576` B (2^20) + 8 B header; installed rows carry
  `(cseq, off, alen)` into the pool.
- Every chunk byte size is < 2^25 with ≥ 25x margin (largest: installed
  chunk 1,310,728 B vs 33,554,432 B ceiling).

### Mechanics (frozen)

- Gate state keeps per-table `(head_ptr:i64, row_count:i32)` plus pool
  `(head_ptr:i64, bytes_used:i32)` in the flat arena. Chunks are
  `ob_alloc`'d zeroed slices chained by an 8-byte header holding the
  next-chunk pointer (pointer round-trip `as i64` / `as *u8` proven on the
  pinned toolchain 2026-09-24). Row index → `(chunk_seq, row_in_chunk)`
  by division over `SP_CHUNK_ROWS`. Lazy allocation: chunk 0 is allocated
  on first append.
- `sp_ledger` **always appends** and returns the global row index (the
  `-1` drop path is deleted). "All ledgered" holds at any run length.
- `sp_dispute_bump` always inserts or finds the `(org,key)` row and
  returns the round count. Table exhaustion can no longer cause instant
  escalation: escalation happens **only** via the frozen
  bounded-deliberation law (`SP_MAX_ROUNDS = 3` consecutive withholds),
  which is ledgered (`SP_L_ESCALATE`) with an inbox entry — never silent.
- `sp_quarantine_add` always indexes the withheld claim. The gate ledgers
  `SP_L_QUARANTINE` **only when `sp_quarantined(org,key)==1` holds at
  ledger time, unconditionally** — the phantom-row defect is closed by
  construction, not by testing.
- `sp_installed_add` always indexes `(org,weight,cseq,off,alen)`;
  `sp_conflict_check` scans all chunks at every index position.
- Overseer inbox chunked: every escalation lands an inbox entry; the
  `SP_OVR_CAP` silent drop is gone.
- New ledger code `SP_L_STORE_FULL = 312` `{ep,org,key}`: when the
  testbed evidence store (§2, bound 3) cannot hold a quarantined claim's
  GEN text, the quarantine **index still records the claim** and the
  ledger records the truncation — fail-closed and ledgered, never silent.

### Accessor surface (frozen; raw `G_*` offsets are deleted)

`sp_ledger_n`, `sp_ledger_get(g,idx,field)`, `sp_ledger_count`,
`sp_ledger_count2`, `sp_dispute_n`, `sp_quarantine_n`,
`sp_quarantined` (unchanged semantics), `sp_installed_n`,
`sp_inst_get(g,idx,field)`, `sp_overseer_n`, `sp_overseer_get(g,idx,field)`,
`sp_chunk_max_bytes(g)` (walks every chunk chain incl. the pool; returns
the largest single-chunk byte size — the K6 machine check).

The smoke battery's three raw-offset reads and the red-team helpers'
raw-offset reads are rewritten onto these accessors with **unchanged
expected values**.

## 2. Load-bearing justification for every remaining bound

1. **Per-chunk byte sizes (§1).** The znc 2^25-bytes-per-slice ceiling is
   a genuine toolchain limit (`~/AGENTS.md`: a single slice > 33,554,432
   bytes panics on any index). Chunks are separate slices sized under it
   with large margin. This bound is physical/toolchain, not a design
   choice; logical capacity is unbounded.
2. **`SP_MAX_ROUNDS = 3` (bounded deliberation).** Approved composition
   law #4 (frozen integration PREREG §1.2; K3 there). A deliberation
   bound, not a storage cap; the escalation path is ledgered and
   notified. Unchanged.
3. **Evidence store `SP_MAX_LINES = 512` / `SP_STORE_SZ = 65536`.**
   Physical-memory-bounded testbed evidence partition. Overflow is now
   loud (`SP_L_STORE_FULL`, §1) instead of silent. The H6 write-once
   evidence partition carries its own sizing law when it lands (frozen
   PREREG §4 upgrade path).
4. **`SP_NORG = 8`, i32 nonces, message/queue constants in the organ
   layer.** Protocol constants outside this residual's scope; unchanged.
5. **Terminal hard stop: physical memory.** A chunk `ob_alloc` failure
   yields a zero-length chunk; the first write into it panics (loud
   halt — nothing proceeds unledgered). This is the ONLY remaining hard
   stop and it is physical, not arbitrary. Asserted unreachable in every
   battery (worst case §3 totals < 16 MB on a multi-GB VM).

## 3. Worst-case memory at 100x horizon

- Ledger: ≤ ~8 rows per gate decision
  (VERDICT + NOTIFY + QUARANTINE + ESCALATE + PROVTAGs + DEP edges).
  100x horizon of the s100 stream is O(thousands) of decisions → 1 chunk
  (1.0 MB).
- K1 battery (the heaviest run): 2000 REVOKE cycles → 4000 rows;
  600 withhold cycles → 1900 rows (incl. ≤100 `SP_L_STORE_FULL`); dispute
  table 600 rows → 1 chunk (0.75 MB); quarantine 600 rows → 1 chunk;
  pool < 100 KB.
- Installed index, adversarial worst case (1 install/cycle over a 100x
  128-episode curriculum): ~12,800 rows → 1 chunk (1.3 MB).
- **Total worst case across all tables at 100x: < 8 MB**, single-digit
  chunks per table, every chunk ≤ 1,310,728 B < 2^25. Memory is bounded
  per chunk by construction (§2.1); the total is bounded by physical
  memory — the load-bearing limit.

## 4. Kill bars

- **K1** — 2000-cycle ledger run → zero silently dropped rows. 2000
  `M_REVOKE` cycles (2 rows each: `SP_L_VERDICT` + `SP_L_REVOKE_PASS`) ⇒
  `sp_ledger_count(VERDICT)==2000` and `sp_ledger_n==4000`; plus 600
  ungrounded-withhold cycles ⇒ `VERDICT==600`, `NOTIFY==600`,
  `QUARANTINE==600`, ledger total `==1900` (600+600+600+≤100
  `SP_L_STORE_FULL`). Every executed decision has its `SP_L_VERDICT`
  row — exact counts, machine-checked.
- **K2** — no phantom quarantine rows: for **every** `SP_L_QUARANTINE`
  ledger row in the R3 run, `sp_quarantined(org,key)==1`
  (machine-checked loop over all rows); quarantine index holds all 600
  entries (`sp_quarantine_n==600`).
- **K3** — conflict detection correct at index positions >128: 200
  installs; contradict entries at positions 150 and 199 ⇒ `lose==1`;
  contradict an absent atom ⇒ `lose==0` (adversarial probe,
  machine-checked).
- **K4** — dispute overflow → fail-closed with ledgered reason, no
  silent escalation inflation: 200 distinct withholds ⇒ every
  `disp==SP_WITHHOLD` (none `SP_ESCALATE` on first withhold),
  `sp_dispute_n==200`, `sp_ledger_count(SP_L_ESCALATE)==0`,
  `sp_overseer_n==0`; then one claim re-emitted to 3 rounds ⇒
  `SP_ESCALATE` with ledgered `SP_L_ESCALATE` + inbox entry (bounded
  deliberation still works, and it is ledgered).
- **K5** — long-horizon T1–T5 verdicts unchanged vs frozen refs:
  long-horizon stdout **byte-identical** to
  `longhorizon/artifacts/` frozen refs (no regressions).
- **K6** — per-chunk memory ≤ 2^25 bytes: `sp_chunk_max_bytes(g) <=
  33554432` machine-checked after every battery in the R2 run.
- **K7** — zero RNG in any decision path: the `build/RNG_SCAN.md` grep
  method over the repaired tree; any hit in a decision path kills the
  run.

## 5. Test plan (frozen)

1. Rebuild all three batteries with the pinned znc
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
2. Re-run red-team R1–R4 with rewritten expectations: the old attacks
   must **FAIL to reproduce** (machine-checked by the K1–K4 assertions);
   all other red-team batteries (T3/T4/F) keep their frozen expectations.
3. Smoke battery: 3x byte-identical, `OB_FAILURES,0`.
4. Long-horizon T1–T5: 3x byte-identical per binary; stdout
   byte-identical to frozen refs (K5).
5. RNG scan (K7). No randomness anywhere in a decision path kills the
   run (frozen integration PREREG §3).

## 6. Deliverables

Repaired `sp_gate.zag` (3 identical copies), updated `ob_test_redteam.zag`
(R1–R4 rewritten; helpers onto accessors), updated
`ob_test_integration.zag` (3 raw-offset reads onto accessors),
`PREREG_R2.md` (this file), `VERDICT_R2.md` with kill-bar accounting —
committed to `tnn-native-lab` under
`onebrain/pam_integration/repairs/R2/` (prereg first, then
evidence+verdict). No binaries, no `.zagd` files.
