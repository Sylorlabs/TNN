# ARM_SPEC.md — B-8: Fixed-size chunks (family CTRL)

**Arm:** B-8 · **Round:** r1 · **Scale:** 1x · **Status:** RETIRED (KILLED at size level) — see `RETIREMENT.md`
**Prereg:** `units/PREREG_FREEZE.md` commit `b0b9140c0eda` (branch `tnn-native-lab`), frozen 2026-09-21
**Design:** `units/ALPHABET_A-F.md` §Arm B · **Brief:** `units/arms/briefs/B-8.json`

## 1. Mechanism (prereg §3, verbatim)

> Aligned blocks of size 8; chunk ID = index (no table). Isolates "does boundary placement matter, or just existence?"

The stream is tiled into aligned 8-byte blocks: chunk `k` covers bytes
`[8k, 8(k+1))`. Chunk ID *is* the index (`id = start >> 3`); the mapping is a
pure arithmetic function, deterministic by construction. Unit ID =
`(corpus_id << 24) | chunk_index` (corpus IDs per ARM_INTERFACE §6:
1=prose, 2=code, 3=t1_prose, 4=t1_code, 5=t2_prose, 6=t2_code, 7=t3, 8=churn_fresh).

## 2. ID-layer classification (ARM_INTERFACE §9)

**B-8 is a NON-ID-layer arm** (confirming the provisional classification).
`recall` takes a unit ID and resolves it by pure arithmetic
(`id → (corpus, chunk index) → byte span`); no persistent ID→storage mapping
is maintained. Consequences:
- M1 swap probe: **N/A (no ID layer)** — there is no ID table to remap; the
  probe is vacuous, not failed.
- M7: **N/A (no ID layer)** + informational re-read-bytes footnote.
- A15's provisional remap schedule does not apply (no persistent ID layer).

## 3. Memory substrate

Adapted 1:1 from the harness's validated B-64 reference (`harness/b64/`):
- Slot arrays (per unit): `ids, offs, lens, corps, flags, shifts, pidx`
  (7 × cap × u32) + insertion-order queue (`ins_cap` × u32).
- Slot placement: multiplicative hash of the unit ID, linear probe;
  order-independent (A11: the M8 freelist perturbation is a verified no-op).
- Ops: `ingest` (deliberate add, `ADD_UNIT`), `recall` (re-read corpus buffer
  at the recorded span), `kill` (tombstone, `KILL_UNIT`), `pin`/`promote`
  (valuable marking), `weaken` (processed as audited annotation — documented
  policy), `revise` (clears recorded boundary shift / content patch after
  probing the unit — lineage preserved, same ID + `REVISE_UNIT` entry),
  `evict` (FIFO oldest-unpinned, `EVICT_UNIT`), loud `REFUSE` on overflow
  with no policy path.
- Trainer ops: `trainer_defect_boundary` (recorded shift),
  `trainer_defect_content` (recorded byte patch), `trainer_mark_valuable`
  (→ pin). All logged with trainer opcodes.
- Strength stays judgment-set: `use_count` is not even tracked (B-8 keeps no
  stats array — the design's "optional stats array" was omitted; it drives no
  decisions and M3 is reported from ledger + probes).

## 4. Audit ledger (sharded)

ARM_INTERFACE §6 opcodes and 16-word entry layout are implemented verbatim.
**B-8 deviation from the B-64 reference (build note, not a rule change):**
B-8's per-chunk ADD volume (≈1.93M entries in M8 ≈ 120MB) exceeds the 2^25
single-slice indexing limit, so the ledger is striped over
**524288-entry (32MB) shards** (8 max, allocated per-mode from the entry
budget — deterministic per mode, hence perturbation-identical). `b_led`
routes by `entry >> 19`. Consequences:
- `ledger.bin` (M5/M8) = concatenation of all shards' used bytes, written
  by `write_ledger` (single create-exclusive open, sequential ≤1MB writes).
- M8 `ledger_chain.txt` = `sha256(concat(sha256(shard_used_bytes) for each
  shard))` instead of `sha256(flat ledger)`. M8 compares each arm against
  itself only (C13), so the chain definition needs determinism, not
  cross-arm comparability. Documented here.
- M8 `store_hashes.txt`: the slot-region image (~73MB) also exceeds 2^25, so
  it is hashed as a **stream** — chunk `i` = bytes `[i·1MB, (i+1)·1MB)` of the
  concatenated region stream (ids, offs, lens, corps, flags, shifts, pidx,
  ins) — identical chunking to a materialized image, without materializing it.

## 5. Mode budgets (entry/slot caps)

| Mode | slot cap | ledger entries | ins cap |
|---|---|---|---|
| m1 | n+n/4+2048 | n+2048 | n+1024 |
| m2 | n+n/4+2048 | 64 (as the reference) | n+1024 |
| m3 | 4000 (C_M3, harness-fixed) | 140,000 | 60,000 |
| m4 | n+n/4+2048 | n+8192 | n+1024 |
| m5 | n+n/4+4096 | n+4096 | n+2048 |
| m6 | nt+ny+(nt+ny)/4+8192 | nt+ny+8192 | nt+ny+2048 |
| m8 | nun_p+nun_c+(…)/4+16384 | 2,000,000 (4 shards) | nun_p+nun_c+60000 |

(n = corpus chunk count; prose 677,841 / code 1,189,418.)

## 6. M3 reading (ambiguity A-B8-1)

The rig's M3 "fresh units" are 64B fixture spans of `churn_fresh.bin`. B-8's
native unit is the 8B chunk, so each fixture span is ingested as **8 chunk
units** (8 deliberate adds). C_M3 = 4000 slots therefore holds 4000 chunk
units: phase 1 (24,000 chunk ingests) and phase 3 (32,000) both overflow and
the arm's declared FIFO-oldest-unpinned eviction acts (V is pinned, never
targeted). Expected honest outcome: survival 100.0 (V pinned), fresh_recall
≈ 75.0 (last-500 spans = 4000 chunks, newest 3000 survive) →
**FROZEN-UNDER-PRESSURE fires mechanically** (survival ≥ 90 AND fresh < 80),
so the M3 cell scores 0. The flag's *intent* (detect undeclared freezing) does
not match B-8's situation (capacity-bound fine granularity, fully audited
eviction) — but the rule is applied literally. This is data about
granularity's capacity cost, logged as ambiguity A-B8-1.

## 7. Laws

- Pure Zag for all arm cognition. Zero RNG in any decision path.
- Byte-identical reruns (M8 gate: 5 perturbations × 2 reruns).
- No slice indexed above 2^25 (ledger shards, streamed store hashing).
- Never `==` on slices; spans identified by integer triples / chunk index.
- `_zag_arg` results never freed; `_zag_strcmp` = 1 on equality.
- Workdirs under `~/workspace` (never `/tmp`).

## 8. Kill criteria (prereg §3, verbatim)

> A size retires when another B size strictly dominates it on M1/M2/M3 both corpora. B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1. If it fires, the arm is KILLED — write the death certificate with evidence and commit it. Dead arms die in public.

B-8's 1x row feeds the family comparison; retirement/kill is decided by the
coordinator against the sibling B sizes and the smart arms.

**Adjudicated 2026-09-21 (follow-up crew): RETIRED.** B-16 strictly dominates
B-8 on M1/M2/M3 both corpora (M1/M2 tied at ceiling; M3 100.0/100.0 CLEAR vs
B-8's 67.6 FROZEN-UNDER-PRESSURE → cell 0 — the 67.6 confirmed real by
independent byte-identical reruns and an eviction-victim trace; the freeze is
genuine granularity/capacity pressure, not a metric defect). Death certificate:
`docs/RETIREMENT.md`; M3 adjudication evidence: `run/adjudication_m3.md`.
