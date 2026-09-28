# VERDICT — B-T5 literal same-material split→remerge round-trip (MARATHON CREW 5)

**Date:** 2026-09-21 (UTC) · **Track:** R0 · **Battery:** B-T5 · **Verdict: FAIL**

This document **supersedes** the B-T5 PASS claimed in `VERDICT_B5_DYNAMICS.md`
(B-DYNSG battery). That battery's split fired on chunk `"splitchk"` (id 0)
while its merge fired on *different* material (`"AAAA"+"BBBB"`, ids 1+2), and
then claimed the bar. The coordinator rejected that reading. The frozen bar is
literal:

## Frozen requirement (programmatic extract — `BT5_FROZEN_SPEC_EXTRACT.md`)

From `units/PREREG_FREEZE.md` §2 (B-table, R-9), extracted verbatim
(`sed -n "371,451p"`, source SHA-256
`0e07ad031a808782cd41e711ccee90995cd36584ade4c303b4a3364d35063863`):

> **Split/merge dynamics** — recovered Zag dynamics: split fires iff
> `use_count ≥ 3 AND conflict ≥ learned_conflict AND utility ≤ learned_utility_floor`;
> merge fires iff `pair_seen ≥ learned_pair_seen AND joint_gain − separate_regret ≥ learned_gain`.
> Bar: dynamics occur, are ledger-auditable, boundaries shown mutable
> (**a recruited chunk split then re-merged on the record**).

Interpretation used (no stretching): **the same recruited chunk** must be
split and then its halves re-merged, and the restored chunk must be
byte-identical to the original. Verdict rule: PASS iff a merged chunk is
minted whose bytes byte-compare equal to the pre-split snapshot. Anything else
is FAIL — a re-promoted whole-span dup is a new recruitment, not a re-merge,
and does not satisfy "re-merged on the record".

## Harness

`units/r0/impl/dynamics/bt5_roundtrip.zag` — pure Zag, zero RNG in AI decision
paths. Tests the **actual B-T5 mechanism** (`r0_maybe_split` /
`r0_maybe_merge` in `units/r0/impl/core/r0_core.zag`), not a reimplementation.

- Per leg (0 = conflict≥400/pair_seen≥3/gain≥0; leg 1 = conflict≥500/
  pair_seen≥4/gain≥500; utility floor 0 both):
  - **Arena RT-1 (the round-trip):** recruit `"splitchk"` (8 bytes) → snapshot
    original bytes → drive `use_count=3`, `conflict=500`, utility to ≤0 →
    `r0_maybe_split` → observe the split's own (parent, child) pair ×6 →
    `r0_maybe_merge` in both orders → byte-compare any merged chunk vs snapshot.
  - **Arena RT-2 (prefix-shadow control):** after the split, re-observe only the
    4-byte prefix and promote — measures *why* the re-merge has no live halves.
  - **Arena RT-3 (merge-alone control):** two live halves `"spli"+"tchk"` merged
    directly — proves the merge op is sound and the gain conjunct is
    satisfiable at `pair_seen=6`, isolating the FAIL to split→merge composition.
- Byte-identical reruns: N=5 deterministic heap-perturbation modes per leg;
  all 59 output lines identical across modes (only the two self-labeling
  `RT_BATTERY,pert=` / `M8_PERTURB,` lines differ).
- Build: `znc 2026.07.0-dev (edition 2026)`,
  `znc bt5_roundtrip.zag -o <out> --no-zagd --no-analyze --no-foreground-cache`;
  binary built to `~/workspace/scratch_bt5/` (never committed).
- Store-image (SHA-256 over arena header+bank), ledger hash, alloc trace
  captured per leg (M8 armor idiom).

## Measured results — Arena RT-1 (both legs; identical except RT_UTIL_BEFORE)

| # | Measurement | leg 0 | leg 1 |
|---|-------------|-------|-------|
| 1 | Chunk recruited (`RT_PROMOTED`) | 1 (id 0) | 1 (id 0) |
| 2 | Original material length (`RT_ORIG_LEN`) | **8** | **8** |
| 3 | Original bytes verified `"splitchk"` | yes | yes |
| 4 | `conflict` at split | 500 | 500 |
| 5 | `use_count` at split | 3 | 3 |
| 6 | Utility before → after regret drive | 5283 → −717 | 5163 → −717 |
| 7 | Parent regret driven (3 iters × 2000) | 6000 | 6000 |
| 8 | Split fired; child id (`RT_SPLIT_CHILD`) | 1 | 1 |
| 9 | Parent state after split | **2 (tombstoned)** | 2 (tombstoned) |
| 10 | Child state / prefix len / suffix len | live / 4 / 4 | live / 4 / 4 |
| 11 | `pair_seen(parent, child)` | 6 (≥ 3/4 bar) | 6 |
| 12 | `r0_maybe_merge(parent, child)` rc | **−1** | **−1** |
| 13 | `r0_maybe_merge(child, parent)` rc | **−1** | **−1** |
| 14 | Merged chunk id (`RT_MERGED_ID`) | −1 (none) | −1 (none) |
| 15 | Merged length vs required 8 | 0 vs 8 | 0 vs 8 |
| 16 | Merged bytes byte-compare vs original | n/a (no chunk) | n/a (no chunk) |
| 17 | Halves' bytes concatenated vs original | 8/8 preserved | 8/8 preserved |
| 18 | Ledger: SPLIT ops (196) / MERGE ops (197) | **1 / 0** | **1 / 0** |

**Byte divergence:** original material 8 bytes → merged output 0 bytes.
**Missing output relative to the required byte-compare: 8 bytes.** The
round-trip does not restore the material at all.

## Why the merge refuses (measured, not assumed)

1. **Tombstoning (primary, measured):** `r0_split_at` rewrites the parent's
   record to the 4-byte prefix and tombstones it (state 2). `r0_maybe_merge`
   requires *both* input IDs live (`r0_chunk_state==R0_ST_LIVE`); the
   tombstoned parent fails the gate in both argument orders (rc −1). Measured
   rows 9/12/13.
2. **Prefix shadow (control RT-2, measured):** after the split, re-observing
   the 4-byte prefix 6× and promoting recruits the stale 8-span proposal as a
   **new live dup** (`RT2_DUP_ID=2`, 8/8 bytes `"splitchk"`, state live) while
   the prefix proposal is dedup-skipped against the tombstoned record —
   `RT2_FIND_LIVE_SPLI=−1`. The prefix half can *never* be recruited live
   again; the re-merge has no live halves in either order. (The 8-span dup is a
   fresh recruitment, not a merge — it proves the composition gap, not the bar.)
3. **Regret arithmetic (secondary):** driving the parent's utility to ≤0 added
   6000 separate-regret to the parent record. Even if the parent were live, the
   merge gate reads `joint_gain − separate_regret ≥ learned_gain`; the split's
   own regret drive poisons the merge's arithmetic on the same IDs.

## Controls

- **RT-3 merge-alone:** `RT3_MERGED_ID=2`, `RT3_MERGED_LEN=8`,
  `RT3_MERGED_BYTES_OK=1` on both legs — the merge op is sound; the FAIL is
  composition, not a broken merge.
- **Data preservation:** `RT_HALVES_CONCAT_OK=1` — the bytes survive the split
  (4+4=8/8); the FAIL is mechanism refusal, not data loss.
- **Ledger auditability:** exactly one SPLIT op (196) and zero MERGE ops (197)
  in the RT-1 arena ledger; the split entry is dumped in the log (`RTLED,…`).

## Determinism manifest

| Run | Exit | Log MD5 |
|-----|------|---------|
| leg 0, pert 0 (canonical `rt_leg0.log`) | 4 | `fc67fccf9fb59cc7b9f6137d54590054` |
| leg 1, pert 0 (canonical `rt_leg1.log`) | 4 | `6c1099926b124fbd642349b4d3581b3b` |
| leg 0/1, pert 1..4 | 4 | all 59 measurement lines byte-identical to pert 0 |

Store images: leg 0 `7008d19c…0cc1eb22`, leg 1 `2698a3b7…20080bb3fb21`.
Ledger hashes: leg 0 `1547986639`, leg 1 `952025763`.
R0 probe gate: `R0_PROBE,total_fails=0` (store-sequence readback clean all runs).

## Verdict

**FAIL.** The same-material split→remerge round-trip does not occur: the
merge fires on the split's own halves in 0/2 orders on both legs, no merged
chunk exists, and the byte-compare cannot run (0 of 8 required bytes
produced). The split side meets its recovered conditions and is
ledger-audited; the merge side is sound in isolation (RT-3). The composition
fails because the split tombstones the parent and shadows the prefix, leaving
no live halves for the merge gate — a genuine dynamics gap in the recovered
B-T5 mechanism, not a harness artifact.

## Evidence map

- `units/r0/evidence/dynamics/VERDICT_BT5_ROUNDTRIP.md` (this file)
- `units/r0/evidence/dynamics/BT5_FROZEN_SPEC_EXTRACT.md` — verbatim §2 extract + extraction command + source SHA-256
- `units/r0/evidence/dynamics/rt_leg0.log`, `rt_leg1.log` — canonical logs (pert 0)
- `units/r0/impl/dynamics/bt5_roundtrip.zag` — harness source
