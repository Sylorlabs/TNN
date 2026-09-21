# Arm E — Ephemeral Chunks (`STORE` family): Arm Specification

Round 1, Track A representation bake-off. Author: Arm E crew (subagent of the
Track A coordinator). Date: 2026-09-21.

## 1. Mechanism (frozen §3: "E — Ephemeral chunks")

- **Segmentation is transient, per episode, held in scratch memory, discarded.**
  Every ingest tiles the incoming corpus into fixed 64-byte windows in a
  64-byte stack scratch buffer (or an episode-local scratch array). The window
  boundaries are never persisted: no chunk table, no chunk IDs.
- **Persistent memory stores owned byte copies, not references.** Each
  accepted unit's bytes are `memcpy`'d into a persistent bump arena; the slot
  records `(corpus, offset, length, arena_offset)`. Recall serves the arena
  copy, never the corpus buffer.
- **No content deduplication, no `CUT_*` operations.** Two ingests of
  byte-identical content at different keys produce two independent arena
  copies (verified: M5 ledger shows distinct arena offsets for identical
  windows). Adding dedup would turn E into a D-like arm and is forbidden.
- **Deliberate operations** (all audit-logged with fixed opcodes): `ADD`,
  `KILL`, `PIN`, `WEAKEN`, `REVISE`, `EVICT`, `REFUSE`, `SNAPSHOT_MARK`.
- **Arithmetic unit key** `(corpus << 24) | index`, identical to B-64, because
  E is provisionally a non-ID arm (chunking is transient, not identity).
  M1 swap probe N/A; A15 does not apply.

## 2. Laws obeyed

Pure Zag cognition, zero RNG in any decision path (verified: no RNG
constructs in source; byte-identical reruns on every leg). No slice above
`2^25` is ever indexed (large buffers are sharded: corpus reads, arena, and
audit ledger). `_zag_arg` results are never freed; `_zag_strcmp` equality is
`1`; no slice `==`; large struct array fields are aliased to locals before
indexing.

## 3. Store layout (M5)

Per AMBIGUITIES.md A16, the measured store region is:

- 8 slot arrays (`ids, offs, lens, corps, flags, shifts, pidx, apos`):
  `cap × 4 bytes` each → `cap*32`
- insertion queue: `ins_cap × 4 bytes`
- arena bytes actually stored (the owned copies): `ar_used`

`m5_slot_table_bytes = cap*32 + ins_cap*4 + ar_used`.
Capacity formulas (same headroom policy as B-64): M1 `cap = n+n/4+2048`,
M5 `cap = n+n/4+4096, ins_cap = n+2048`. Arena capacity `(n+500)*64+1024`
bytes (sharded ≤ 2^25 per shard).

## 4. Binding verdict rule

> Stored-bytes-per-recall ≥ 2× B-64's at equal M1 on either corpus at 10x
> (copies-only strictly dominated by the dumbest persistent segmentation)
> ⟹ **KILLED**, with the public death certificate:
> "references matter, transient segmentation does not."

Stored-bytes-per-recall is read from the M5 metric `m5_slot_table_bytes`
(the persistent store region per A16). The comparison is run at 10x on the
prose corpus (both corpora for M1).

## 5. Ambiguities resolved (arm-local, documented)

1. **Repeated ingest of the exact same arithmetic key** revives the existing
   slot without allocating a second arena copy (same memory entry /
   provenance, same key — not cross-entry dedup). Tiled 10x ingests use
   distinct keys per tile and remain independent copies.
2. **FRESH-corpus units in M5** are real episodes (fresh keys), killed after
   the pressure phase; their ledger entries persist per the append-only rule.
3. **M5 baseline** allocates the same empty store the M5 trial uses (slot
   arrays + insertion queue + full arena capacity + ledger), fully touches it,
   then spins so the harness RSS sampler observes the peak.

## 6. Source layout

- `~/workspace/tnn-lab/units/arms/E/cl/arm.zag` — the arm (single file).
- `~/workspace/tnn-lab/units/arms/E/substrate/` — the two required R33
  substrate files, copied verbatim from B-64 (MD5-verified equal).
- `~/workspace/tnn-lab/units/arms/E/work/` — build + run scratch (binaries,
  corpora r10, battery workdirs). Not committed.
- `~/workspace/docs/lab/units/arms/E/` — this spec, `BUILD_LOG.md`,
  scorecard JSON, raw logs, `VERDICT.md`.

## 7. Scale scope

Full 1x battery (M1–M9) per the frozen harness. 10x evidence is scoped to
the kill criterion: M1 on both corpora (equal-M1 check) + M5
(stored-bytes-per-recall) + M5 baseline, on the 10x corpus built by the
frozen `build_10x.py` (tile SHAs verified against `CORPORA.md`). The M8
adversarial gate runs at 1x per the frozen battery.
