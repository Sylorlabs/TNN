# ARM M — Counter IDs (IDENT family) — Arm Specification

Status: FROZEN. Authority: `units/arms/briefs/M.json`; verbatim frozen §3 row
(coordinator-verified byte-identical against frozen commit
`b0b9140c0eda` via the GitHub API).

> M — Counter IDs | IDENT | Mechanism: Monotonic nth-chunk issuance; identity
> is issuance order; store-local handle. M-dedup: optional dedup scan over
> last-W episodes. | Binding kill criterion: **Scoped:** KILL counter IDs as
> the cross-store/global identity if, in the two-TNN merge trial, remapping
> produces ≥1 dangling/misdirected pointer OR remap compute > 10% of total
> merge compute. (Survives unconditionally as the store-local handle.)
> Separately: the M-dedup claim dies (revert to pure issuance) if M7 dedup
> ratio < 0.4 on the repetition protocol.

Two coordinator corrections are acknowledged and applied:

1. **First correction:** the original dispatch text specified "Fixed-32B IDs"
   with a ≥90%/≥97%/99%-swap kill criterion. That mechanism was VOIDED by the
   coordinator; the dispatch text was wrong. The `cl/arm.zag` built on it
   (uncommitted) was discarded, not salvaged.
2. **Second correction:** the coordinator's own paraphrase of the frozen §3 row
   (from memory) was superseded by the verbatim row above, byte-verified
   against frozen commit `b0b9140c0eda`. The brief at
   `~/workspace/tnn-lab/units/arms/briefs/M.json` matches it exactly. Authority
   order: (1) brief file; (2) verbatim row; (3) nothing else written by the
   coordinator.

## 1. Mechanism (what was built)

Counter IDs. The ID of a chunk is its issuance index into the ID→span table.
Identity is issuance order; the handle is store-local (independently-issued
counters do not agree across stores, so cross-store use requires remapping).

Logged substrate state (`struct M`, `cl/arm.zag`):

- `seq` — `next_id: u64`. Add assigns `id = next_id++` atomically with the
  audited write. The ID rides in the add entry's slot/b-fields (op@0,
  slot@4 = ID); ID issuance costs zero marginal audit entries.
- Seven parallel `u32` arrays indexed by ID (`cap` × 4 bytes each): `offs`
  (byte offset of the span), `lens` (span length), `corps` (corpus ID),
  `flags` (LIVE/PIN/WEAK/SHIFT/PATCH bits), `shifts` (recorded boundary
  shift), `pidx` (defect-patch index or −1), `eps` (episode number at issuance,
  for the dedup window).
- `ep_start[64]` — first ID of each episode (dedup window bookkeeping).
- `evict_head` — FIFO eviction cursor. Issuance order == ID order, so the
  "insertion-order queue" is an implicit cursor, not a stored structure.
- Append-only audit ledger, frozen 16-word layout (op@0, slot@4, rc@8,
  b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60).

Rules (implemented literally):

- **Monotonic, never reused.** Kill clears LIVE but the row is retained as a
  tombstone: old pointers resolve to "killed", never dangle; the ID is never
  reissued. Gaps are permanent.
- **M-dedup (optional, required for M7).** Before issuing, an exact
  byte-equality scan (memcmp) over live chunks of the last-W episodes
  (W = 3, window includes the in-progress episode), scan order ID-ascending,
  first match wins. Equal bytes → reuse the existing ID + a lightweight reuse
  audit entry (`OP_ADD` with `d2 = ADD_REUSE`). Without dedup, identical
  re-ingest mints a fresh ID (pure issuance).
- **Recall** carries only the ID; resolution goes through the ID→span table
  live, end-to-end (no side channel).
- **Revision (M4):** per-unit deliberate repair through the revision API that
  clears SHIFT/PATCH and writes a REVISE entry with the SAME ID kept (per
  METRICS.md M4 scoring: REVISED requires same ID + revise/repair entry;
  kill+re-add does not count).
- **Eviction:** evict-oldest-unpinned, FIFO via the cursor.
- **Value marking (M3):** pin (the arm's own deliberate op), logged.
- **Weaken (documented policy):** processed as a management annotation — sets
  the WEAKENED flag, audited; never changes stored bytes, never blocks recall.
  Deliberate management, not silent freezing.

Segmentation: fixed 64-byte chunks (the tested variable is the identity
layer, not the chunker). Corpora: `harness/corpora/r1`
(prose 5,422,721 B / 84,731 units; code 9,515,341 B / 148,678 units).

## 2. What each trial exercises

| Mode | Trial | Mechanism under test |
|---|---|---|
| m1-1x-prose/code | M1 | ID-layer recall (content + boundary), plus the mandatory 64-swap probe |
| m2-1x-t1p/t1c/t2p/t2c/t3 | M2 | Episodes-to-criterion on novel tiers (T1 held-out last-10%, T2 third corpus, T3 synthetic) |
| m3-1x | M3 | Churn protocol + freeze-vs-retention distinguisher |
| m4-1x-prose/code | M4 | Deliberate revision (same-ID repair), kill-substitution guard |
| m5-1x | M5 | Slot-table bytes (itemized), ledger bytes |
| m6-1x-p2c/c2p | M6 | Transfer tax prose↔code |
| m7-1x | M7 | Repetition protocol; barred dedup ratio = 1 − seq_r2/(2n) (rounds 1–2 per M-32; round 3 reported separately), bar 0.4 |
| m8-clean/frag/aslr/starve/freelist | M8 | A17 combined instance (M1 prose+code + M3 ops, no capacity pressure); image = per-ID rows in ID order + ledger sha256 + evict cursor; artifacts (image sha256) + stdout/stderr byte-identical across all five perturbations |
| merge-1x | binding | Two-TNN merge: A=prose, B=code; remap table + 1,487 deterministic pointers rewritten; dangling/misdirected check + remap-compute fraction |

## 3. Determinism posture

Pure Zag cognition; zero RNG in any AI decision path (no randomness
anywhere in the implementation — no tie-breaks, no sampling; every schedule
is a fixed function of indices). Byte-identical reruns: one binary, argv
mode dispatch; all trial schedules are deterministic (e.g. M7 lookups use
`(l*37)%n`, M4 defects use the cyclic shift table, merge links are every
100th chunk).

## 4. A15 swap probe (PROVISIONAL-PENDING-FREEZE)

The prereg mandates an N=64 swap probe for ID arms but gives no schedule;
the harness-proposed deterministic schedule is implemented: after every
`n/64-1` recalls the ID table row of the next recall target is patched
to resolve to the next ID's span, `TRAINER_SWAP_PROBE` is logged, recall
runs through the ID path, the REMAPPED content is required back, then the
row is restored. Returning original content despite the remap = side channel
→ M1 scored 0. Marked `PROVISIONAL-PENDING-FREEZE` on the scorecard until
Micah freezes the procedure. Final 1x: 64/64 detected on both prose and code.

## 5. Merge-trial operationalization (binding)

- Two stores built by pure issuance (A: 84,731 prose IDs; B: 148,678 code
  IDs). B carries 1,487 pointers: every 100th chunk → `(i*37) % nB`.
- Merge into M: ingest A's chunks (IDs 0..nA−1), then B's (explicit remap
  table `remap[j]`, not an assumed offset); rewrite every pointer through the
  table, logging `OP_REMAP` per pointer.
- **Dangling:** remapped target ≥ M.seq or not LIVE. **Misdirected:**
  remapped target's bytes ≠ B's original bytes for that pointer.
- **Compute (deterministic op units):** remap_compute = nB (table entries) +
  nLinks (pointer rewrites); total_merge = nA + nB (ingests into M) +
  remap_compute. Kill fires iff bad-pointers ≥ 1 OR
  remap_compute/total_merge > 10%.
- Result 1x: dangling=0, misdirected=0, remap_compute/total = 39.14% > 10%
  → **SCOPED KILL FIRES**. Counter IDs die as cross-store/global identity;
  survive unconditionally as store-local handle.

## 6. M7 dedup — honest failure

The M7 dedup scan (exact byte-equality over last-W episodes, ID-ascending)
was implemented with an FNV-1a hash accelerator as a candidate filter
(exact equality remains authoritative). The accelerator triggered a znc
compiler bug (multi-parameter corruption, ZNC-2026-09-21-007 extended):
with a computed table index the binary panics "slice index out of bounds"
in round 2; with a constant index it runs (slowly). Inlining, struct-field
aliasing (per AGENTS.md), and 32-bit hashing did not resolve it.

For the 1x evidence run, the dedup path is disabled (`if(false && ...)`),
so M7 runs with pure issuance: dedup_barred = 0.00, dedup_r3 = 0.00.
The frozen bar (dedup ≥ 0.4) FAILS, triggering the separate M-dedup death:
**revert to pure issuance**. The arm itself is not killed by this; the
M-dedup claim is.

The linear-scan fallback (provably identical semantics) is too slow for the
full 84,731-unit corpus (timed out after 180s in testing). The mechanism
is correct; the performance optimization is blocked by the compiler.

## 7. Known honest limits

- M8 perturbations frag/aslr/starve/freelist: for counter IDs, placement is
  a pure function of issuance order (ID = index); there is no freelist, no
  hash table, no pointers. `frag` performs real heap churn before the build;
  the others are documented no-ops. The gate's force is that the logical
  image is invariant to all of them.
- T3 (synthetic) is a single 1 MiB file; reported per tier.
- M3 capacity models 4,000 live slots with a larger monotonic-ID space
  (corrected 2026-09-21).
- M6 capacity is `4*nt + ny + 1024` (corrected 2026-09-21).
