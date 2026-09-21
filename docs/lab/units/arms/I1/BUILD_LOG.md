# ARM I1 — Build Log

**Date:** 2026-09-21
**Source:** `cl/arm.zag` (pure Zag)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Substrate:** `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` (byte-verified copies)

## Defects found and fixed (2026-09-21)

1. **Co-recall overcounting.** Was counted once per child; fixed to exactly
   once per fixed 8-block per rehearsal episode.
2. **Formation freeze (`fdone`) set after episode 1.** Counters below `T_co`
   were treated as "no future candidate". Fixed: a level stays active while
   any parentless block could become a future candidate.
3. **`fdone` set on empty levels.** `scan_formations` with `ins_n==0`
   (level not yet formed) permanently disabled that level's formation.
   Fixed: early return without touching `fdone`. (This was blocking L2+.)
4. **Parent spans never set.** `form_super` left `off=0,len=0`. Fixed:
   parent span = min child offset .. max child end (deterministic).
5. **M2 JSON malformed.** Human-readable M9 line printed inside the JSON
   object. Fixed: `j_end()` before the M9 line.
6. **ID packing collision.** `(level<<27)|(corpus<<24)|serial` with
   `I1_C_FRESH=8` overlapped the level field. Fixed: corpus slots sized
   `9*5` (`I1_CSLOT=9`); all `8*5` index math updated.
7. **M3 slice OOB.** `ser`/`blk`/`fdone` arrays sized for corpus 0..7 but
   corpus 8 used. Fixed by (6).
8. **M3 stale `insn`.** Insertion count captured before second fresh wave;
   survival/recall loops missed new units. Fixed: re-read after ingest.
9. **M4 leaf staled by revision.** `cascade_stale` marked the revised leaf
   itself stale, so verification always failed (0% repaired). Fixed:
   revision marks **ancestors** only; leaf stays live.
10. **M4 re-revise spam.** Clean units re-emitted REVISE every episode.
    Fixed: only revise units still carrying defect markers.
11. **M8 ledger > 2^25.** 600000×64 = 38.4MB single slice panics on index.
    Fixed: capped at 500000 entries (32MB). M8 uses 283989 — no truncation.
12. **M8 missing JSON.** Added `m8-1x` METRIC_JSON emission.

## Verification

- Recompiled clean after each fix; final binary builds with 0 errors.
- Formation: L1 at episode 7, L2 at 14, L3 at 21, L4 at 28 (M5: 13048 /
  1696 / L3 / L4 — see scorecard).
- M4: 100.0% boundary + 100.0% content revised, 0.0% killed (both corpora).
- M3: 100.0% valuable survival, 100.0% fresh recall, 50/50 weaken handled.
- M8 determinism: base / frag / aslr perturbations → byte-identical
  `ledger.bin`, `ledger_chain.txt`, `store_chain.txt`, `store_hashes.txt`.
- M5 determinism: two runs byte-identical.
- Full 1x battery: 14/14 modes rc=0.

## Known limitations (nonblocking)

- `hier_recall` counts L0 recalls with live L2+ ancestry; not a true
  equal-store-cost flat comparator (kill-(i) caveat in VERDICT.md).
- `killii_frac` scans the whole instance; kill-(ii) is per-corpus in the
  freeze — reported per mode corpus as the closest available.
- Natural-break metric uses the provisional whitespace interpretation.
- `E=3` demotion threshold is provisional pending freeze.
- 10x scale legs not run: no 10x corpora in harness; 10x modes not
  implemented in this build.
