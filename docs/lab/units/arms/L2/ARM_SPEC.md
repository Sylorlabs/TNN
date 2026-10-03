# ARM SPEC — L2: Epoch-Relative Position IDs

Family: IDENT. Round r1, scale 1x. Pure Zag, Linux lab VM, `sylorlabs/TNN`
branch `tnn-native-lab`. Deterministic: zero randomness in all decision paths;
double runs byte-identical (M8 gate: 10 runs across 5 perturbations).

## 1. Mechanism (frozen brief §2, implemented verbatim)

Compact position IDs relative to an epoch; epochs bump on >5% of segments
touched; fixed translation table across epochs.

- **RID layout.** A unit's position ID (RID) is `(epoch << 24) | rel`, where
  `rel` is the unit's index *within its epoch*. Epoch occupies the high 8 bits
  (epochs 0–127 usable in signed 32-bit storage); the low 24 bits hold the
  within-epoch index. Overflow past epoch 127 is refused loudly
  (`EPOCH-OVERFLOW`, exit 2) — the epoch counter never wraps.
- **Epoch-relative compaction.** When an epoch bump occurs, the new epoch's
  RIDs restart at `rel=0` for newly ingested units. Old-epoch units keep their
  old RIDs forever (they are never rewritten).
- **Bump rule.** The store's segment arena is divided into 64 KiB
  *epoch-segments* (16 per 1 MiB storage segment). Each epoch tracks a
  touch bitmap over epoch-segments: a mutation op (boundary defect, content
  defect, revision — *not* plain ingestion) marks the epoch-segment its
  bytes land in. When
  `touched_epoch_segments × 20 > allocated_epoch_segments × 16`
  (strictly more than 5% of allocated epoch-segments touched), the epoch
  bumps: `epoch += 1`, `epoch_base = rel_next`, the touch bitmap clears,
  and a bump record is appended to the on-disk bump ledger. The 5%
  denominator is the count of *allocated* epoch-segments
  (`seg_next × 16`), which includes sealed old-epoch segments —
  conservative (bumps rarer) relative to a live-only denominator.
- **Fixed translation table across epochs.** A single append-only translation
  table maps every RID ever issued → its physical location
  (segment, offset, length, corpus tag, corpus offset). The table is
  write-once: entries are never mutated, never reused, never compacted.
  A RID always resolves to the same location no matter how many epochs have
  passed. Killing a unit tombstones its live slot but does NOT free or reuse
  its translation entry — the mapping RID→location survives the unit's death.
- **Within-epoch stability.** A unit's RID never changes within its epoch:
  re-ingesting the same span returns the existing RID; revision patches the
  bytes in place (new segment on patch overflow, recorded in the revision
  map) without touching the RID; kill/pin/weaken/defect affect flags only.
  A dedicated counter (`l2_id_changes`) increments if any observed RID ever
  differs from the first RID issued for its span — it must stay 0.

## 2. Design decisions (disclosed, arm-level — brief was silent)

- **D-EPOCH-SEG.** "Segment" in the bump rule is interpreted as a 64 KiB
  epoch-segment (16 per 1 MiB storage segment), not the 1 MiB storage
  segment. Rationale: with 1 MiB segments a few hundred KB of writes would
  touch >5% of segments and bump constantly; 64 KiB gives the rule teeth
  without making bumps either impossible or continuous.
- **D-LEDGER-CHUNK.** znc cannot index a single slice above 2²⁵ bytes.
  Ledger allocations are sized per-mode under 32 MB; overflow follows the
  documented LEDGER-BOUND policy (stop recording, keep running, count it).
- **D-M6.** "Train on prose" is implemented as the prose.bin corpus with the
  M2 episode loop to the M2 mastery criterion (frozen-policy, real corpus).
- **D-EPOCH-OVERFLOW.** Epoch overflow is refused (exit 2) rather than
  wrapping — wrapping would silently alias RIDs across epochs and break the
  fixed translation table's core promise.

## 3. Binding death (frozen brief §4)

KILLED if **any** within-epoch ID change (same bar as L1), **or** translation
misses exceed **1% of cross-epoch recalls**. Rationale (frozen): kept L1's
costs while breaking L1's promise.

## 4. Provisional flags (carried from frozen ambiguities)

- **A15 trainer swap probe.** Every `ceil(nunits/64)` recalls the trainer
  remaps the target to `(slot+1) % nslots`; `TRAINER_SWAP_PROBE` is logged and
  the mapping restored afterward. Results marked PROVISIONAL-PENDING-FREEZE.
- **M7.** Uses the frozen provisional C′ (single-lookup) schedule and the
  frozen provisional edit for the revision arm. Marked
  PROVISIONAL-PENDING-FREEZE.
