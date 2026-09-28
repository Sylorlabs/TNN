# ARM J1 — Fixed-k Competing Tilings (STRUCT)

**Status:** PROVISIONAL implementation — A15 schedule PROVISIONAL-PENDING-FREEZE.
**Branch:** `tnn-native-lab` (frozen prereg commit `b0b9140c0eda`)
**Date:** 2026-09-21

## 1. Mechanism (§3 literal reading)

J1 implements **three fixed tilings** that compete to cover each query span via
deterministic arbitration. There is no learned segmentation; the tilings are
fixed functions of the byte stream.

### Tilings

- **T0** — Deterministic word/content-run cuts. Maximal non-whitespace runs,
  with following whitespace attached to the preceding run. Chunks capped at
  512 bytes (longer runs are split). This is the "word-like" tiling.
- **T1** — T0 phase-shifted by half the running mean chunk length
  (`shift = (buflen / n0) / 2`). Same cuts as T0, shifted forward; cuts outside
  `[0, seglen)` are dropped; `seglen` is appended as the final cut.
- **T2** — Fixed 64-byte grid (`0, 64, 128, …, seglen`).

All three tilings are computed once per corpus at ingest (seal) time and stored
in the chunk-list registry. They do not change thereafter.

### Persistent IDs

Each chunk receives a persistent 32-bit ID at seal time:

```
id = (corpus << 27) | (tiling << 24) | idx
```

- `corpus`: 1–8 (prose=1, code=2, t1_prose=3, t1_code=4, t2_prose=5, t2_code=6,
  t3=7, fresh=8)
- `tiling`: 0, 1, 2
- `idx`: chunk index within (corpus, tiling), 0-based, up to 2^24-1

The ID→slot table maps each ID to its current slot index (or -1 if dead).
IDs survive kills, weakens, and evictions; a re-ingested chunk revives its
original ID (dedup by ID, not by content hash).

### Records

Each chunk is stored as a 32-byte slot record:

| Word | Field | Description |
|------|-------|-------------|
| 0 | id | persistent chunk ID |
| 1 | off | byte offset in corpus |
| 2 | len | byte length |
| 3 | flags | F_OCC(1) F_LIVE(2) F_PIN(4) F_WEAK(8) F_SHIFT(16) F_PATCH(32) |
| 4 | shift | A15 remap displacement (if F_SHIFT) |
| 5 | seq | recency sequence number |
| 6 | patch | patch index (if F_PATCH), else -1 |
| 7 | reserved | 0 |

Slots live in a 6-chunk open-addressed hash table (6M slots max, 32B each,
192MB total). Hash = Knuth multiplicative (`id * 2654435761 & 0x7FFFFFFF`)
mod cap. Linear probing. Tombstones (F_OCC without F_LIVE) are reused.

### Arbitration (α/β/γ)

For a query span `[qoff, qoff+qlen)`:

1. **Byte-cover filter:** For each tiling, binary-search the chunk list for the
   last chunk with `start <= qoff`. If `start+len >= qoff+qlen`, it's a
   candidate. Non-covering tilings are excluded (kill criterion ii).
2. **Score:** `score = α·value(tiling) + β·recency − γ·overhang`
   - `value`: T0=20, T1=16, T2=8 (judgment-set; NOT prereg-frozen — see §7)
   - `recency`: `seq mod 64`
   - `overhang`: `(start+len) − (qoff+qlen)` (extra bytes beyond query)
   - `α=2, β=1, γ=1` (judgment-set; NOT prereg-frozen — see §7)
3. **Winner:** Highest score. Ties broken by lower tiling index (deterministic).

The winner's slot is returned. If no tiling covers, arbitration fails (-1).

**Kill criterion ii** is evaluated during M1/M2/M3: `cov_viol` counts
arbitration choices that did not byte-cover (must be 0); `subopt_viol` counts
choices where a higher-scoring-by->γ-margin tiling was available but a lower
one was chosen (must be ≤5% of choices).

### A15 N=64 ID-remapping probe (PROVISIONAL-PENDING-FREEZE)

Per the proposed A15 schedule (not yet frozen):

1. Select 64 probe targets: every `nunits/64`-th record in (tiling, idx) order.
2. For each target, remap its ID: `new_id = id ^ 0x4000000` (flip bit 26,
   within the tiling field's spare bit).
3. Update the ID→slot table to point `new_id` at the target's slot.
4. Recall via `new_id`; verify content matches.
5. **Loud failure:** If the target slot is empty or content mismatches, count
   as `ploud`.
6. **Side channel:** If recall succeeds via a path that bypasses the ID table
   (e.g., direct slot arithmetic), count as `pside` and FAIL the probe.

**Status:** PROVISIONAL-PENDING-FREEZE. The schedule above is implemented
literally as proposed. If the frozen A15 differs, this implementation must be
updated and re-run.

Current observation (tiny-file test): `ploud=10/12` — the remapped ID often
resolves to a sparse hash-table region. This is the literal behavior of the
proposed schedule on a sparse table; it is logged, not reinterpreted.

## 2. Birth/Death Turnover (kill criterion iii)

**Birth:** When a corpus is ingested, each tiling's chunks are "born" as
records. Birth is the ingest mechanism itself; `s.births` counts records
created via `j_ingest_one` with `is_new=1`.

**Death:** Records die via:
- `j_kill_id` (deliberate kill, audited OP_KILL)
- `j_evict_oldest_unpinned` (capacity eviction, audited OP_EVICT)
- `slot_kill` clears F_LIVE (tombstone)

`s.deaths` counts kill/evict operations.

**Settling:** Turnover "settles" when the birth rate and death rate converge
over a window and the live set stabilizes. Measured via:
- `J1_TILING` lines: per-tiling win shares over the mode's window
- `J1_KILL2` lines: `cov_viol`, `subopt_viol` (must be zero/≤5%)

**Kill criterion iii:** "Birth/death turnover fails to settle." If win shares
oscillate without convergence, or if `cov_viol>0`, the arm is killed.

## 3. Memory Layout

```
J1 struct (heap-allocated via struct literal):
  cap, nlive, npin, seq
  sl0..sl5: 6 × 32MB slot chunks (192MB total, only cap*32 zeroed)
  idt: ID→slot table (4 bytes/entry)
  chl: chunk-list (start offsets, 4 bytes/entry)
  reg_*: corpus registry (8 corpora × 3 tilings)
  led: 16MB audit buffer (262144 entries × 64B) + file spill
  ins: insertion-order FIFO queue (for eviction)
  patches: content patches (for M4 defects)
  wins0/1/2: arbitration win counters
  ... (see source for full layout)
```

**Constraints observed:**
- No single slice > 2^25 bytes (33,554,432) is indexed. All large structures
  are chunked (slots: 6×32MB; ledger: 16MB buffer + file spill).
- Slot table capacity capped at 5.9M (6M chunks × 1M minus margin).

## 4. Modes

One binary; `argv[1]` selects mode:

| Mode | Description |
|------|-------------|
| `m1-1x-prose`, `m1-1x-code` | M1 content+boundary recall, ID probe, adversarial |
| `m2-t1-prose`, `m2-t1-code` | M2 curriculum tier 1 (+M9 shape) |
| `m2-t2-prose`, `m2-t2-code` | M2 tier 2 |
| `m2-t3-1x` | M2 tier 3 (synthetic) |
| `m3-1x` | M3 strength/churn |
| `m4-1x-prose`, `m4-1x-code` | M4 revision |
| `m5-1x`, `m5-baseline` | M5 memory accounting |
| `m6-p2c-1x`, `m6-c2p-1x` | M6 transfer |
| `m7-1x` | M7 dedup/reuse |
| `m8-1x <corpus> <outdir> <pert>` | M8 determinism (5 perturbations) |
| `shatest` | SHA-256 self-test |
| `timtest`, `dbg1` | Debug (not for evidence) |

## 5. Determinism

- **Zero RNG** in all AI decision paths. No random exploration, no random
  tie-breaks, no stochastic policies.
- Tie-breaks: lower tiling index wins (arbitration); lower slot index wins
  (hash collisions, via linear probing order).
- All iteration orders are deterministic (tiling 0,1,2; idx ascending).
- Byte-identical reruns required; any differing M8 byte = DISQUALIFIED.

## 6. Evidence

Each mode emits:
- Human-readable lines to stdout (e.g., `M1,100.0,100.0,PASS ...`)
- `METRIC_JSON {...}` — single-line JSON with `schema`, `arm`, `round`,
  `scale`, `mode`, `fields` (frozen interface keys)
- `J1_TILING`, `J1_KILL2`, `J1_ADV*` diagnostic lines

M8 writes artifacts to `<outdir>`: `store_hashes.txt`, `store_chain.txt`,
`ledger.bin`, `ledger_chain.txt`, `alloc_trace.txt`, plus `GATE.txt`.

## 7. Ambiguities and Provisional Choices

| # | Ambiguity | Choice | Status |
|---|-----------|--------|--------|
| A-22 | α/β/γ integers not in prereg | α=2, β=1, γ=1 | JUDGMENT-SET, not frozen |
| A-22 | Tiling values not in prereg | T0=20, T1=16, T2=8 | JUDGMENT-SET, not frozen |
| A-22 | Recency formula not in prereg | `seq mod 64` | JUDGMENT-SET, not frozen |
| A-22 | Death share not in prereg | 5% | JUDGMENT-SET, not frozen |
| A15 | ID-remap schedule | As proposed (§1) | PROVISIONAL-PENDING-FREEZE |
| A7/A8 | M7 edit, lookup target, split | First-byte XOR 0xFF; `(l*37)%nunits`; 1666/1667/1667 | PLACEHOLDER (frozen doc unclear) |
| A17 | M8 scope | Full M1+M3 combined instance | Per B-64 precedent |

**"Implement the literal reading, log it, report it. Never reinterpret."**
All of the above are logged as implemented. If the frozen prereg specifies
different values, this arm must be updated and re-run.

## 8. Kill Criteria (binding)

Per the J1 assignment:

1. **Best-of-k ≤ best single tiling + 2 points** at equal total budget on the
   adversarial-cut corpus. Evaluated via `j1_adversarial`: compares best-of-3
   arbitration vs best single tiling at equal chunk budget.
2. **Any non-byte-covering arbitration choice**, or **>5% lower-scoring-by->γ-
   margin choices**. Evaluated via `cov_viol` (must be 0) and `subopt_viol`
   (must be ≤5%).
3. **Birth/death turnover fails to settle.** Evaluated via win-share stability
   and `J1_TILING`/`J1_KILL2` logs.

If any criterion fires, the arm is DEAD and a public death certificate is
written instead of a champion claim.
