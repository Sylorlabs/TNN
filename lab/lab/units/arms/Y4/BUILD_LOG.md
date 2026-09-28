# Y4 BUILD LOG

**Arm:** Y4 — Question-driven (lazy) cuts · **Date:** 2026-09-21
**Repo:** `sylorlabs/TNN`, branch `tnn-native-lab` (via `~/workspace/commit_to_branch.py`)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (frozen)
**Source:** `cl/arm.zag` (~1,580 lines, single file, pure Zag)
**Binary:** `build/y4_bin` (226,594 bytes; build/ is NOT committed)

## Resume state

The prior Y4 workdir contained only two substrate files and an empty `cl/`
— no usable prior mechanism existed. Implementation began anew against the
frozen brief `units/arms/briefs/Y4.json` and `units/ALPHABET_Y-Z.md` §Y4
(byte-compared; they match exactly).

## Detector sizing (measured with the final detector semantics)

| corpus | candidates | chunks | max chunk |
|---|---|---:|---:|
| prose | 79,303 | 79,304 | 1,346 B |
| code | 128,648 | 128,649 | 21,378 B |
| t1_prose | 6,648 | 6,649 | 837 B |
| t2_prose | 29,647 | 29,648 | 2,590 B |
| t2_code | 3,868 | 3,869 | 1,700 B |
| t3 | 14,860 | 14,861 | 853 B |
| churn_fresh | 5,272 | 5,273 | 5,344 B |

`Y4_PATCHB` = 32,768 (covers the 21,378 B max chunk); candidate cap 150,000
per corpus; M8 ledger cap 500,000 entries × 64 B = 32.0 MB — under the
2^25-per-slice znc limit (33,554,432) with ~1.5 MB headroom. M8 store image
≈ 15.9 MB, also under the limit.

## Bugs found and fixed (all caught before final evidence was taken)

1. **QUESTION logged after materialization.** `y_question` originally ran the
   materialization loop first and logged `QUESTION_ASKED` at the end, so the
   ledger read ADDs → QUESTION — violating the lazy mechanism's own ordering
   claim. Fixed: `QUESTION_ASKED` is now logged *before* any materialization
   (with a pre-scan counting already-live chunks so d2 = new
   materializations stays exact). `audit_ledger.py` confirms 0 ordering
   issues on the 438,510-entry M8 ledger: every corpus's CANDs precede its
   first QUESTION, which precedes its first ADD; no ADD-after-KILL for any ID.
2. **Slot-ID table not initialized to the EMPTY sentinel.** `y4_init` allocated
   the ID table but never filled it with −1; `slot_find`'s probe loop reads
   IDs until −1. It worked by allocator luck through all smoke tests (the
   exact L2 failure mode recorded in AGENTS.md the same day). Fixed with an
   explicit 0xFF fill. Because the binary changed, the in-flight battery was
   killed and restarted from scratch with the fixed binary — no battery
   evidence predates the fix.
3. **y4-cmp-1x key buffer overflow.** The comparison leg built JSON keys in a
   24-byte buffer; the longest key (`y4_cmp_materializations_prose`) needs
   29. Heap corruption → panic on first run. Fixed by using literal keys per
   corpus (no dynamic key building). This leg is not part of the shared
   battery; the final binary (`build/y4_bin`, sha256
   7a799d4b004b73125b367bbdacbd59e7f3e32ec09908efb816a0885c7ff76a0e) was
   verified byte-identical to the battery binary on all battery code paths
   (M1 prose stdout compared exactly).

## znc constraints hit (all from AGENTS.md's catalog)

- Slice fields are 16 bytes (ptr+len): `_zag_malloc` sized accordingly
  (ZNC-2026-09-21-003).
- No `slice as *u8` byte images: hashes built by word→byte decomposition
  (ZNC-2026-09-21-002).
- No slice `==` for array selection: integer selectors everywhere.
- `return;` in void fns; no user fn named `zalloc`; `_zag_arg` never freed;
  `_zag_strcmp` returns 1 on equality.
- 2^25 per-slice index limit respected for ledger (32.0 MB) and store image.

## Verification performed

- `audit_ledger.py` (committed): lazy-ordering + opcode-semantics audit of
  `ledger.bin`. Clean on the M5 ledger.
- Full battery via frozen `run_battery.sh` + `run_metric.sh` + `m8_gate.sh`
  (unmodified), workdir `~/workspace/y4runs/battery`.
- Extra legs `y4-lazy-1x` / `y4-cmp-1x` via `run_metric.sh`.
- Scorecard via `scorecard_assemble_y4.py` (mechanical Y4 adaptation of the
  frozen assembler; the frozen file is untouched and its `"arm":"b64"`
  hardcode is why the adaptation exists).

## Evidence committed (explicit file list)

- `cl/arm.zag`, `substrate/R33_NATIVE_IO_V1.zag`,
  `substrate/R33_NATIVE_SHA256_V2.zag`
- `ARM_SPEC.md`, `BUILD_LOG.md` (this file), `VERDICT.md`
- `audit_ledger.py`, `scorecard_assemble_y4.py`
- `scorecard_r1_1x.json`, `COMPARISON_D.json`
- `evidence/STATUS.txt` (per-leg rc/rss/determinism), `evidence/m8_GATE.txt`

NOT committed: `build/`, `.zagd*`, `.zag-cache/`, `ledger.bin` artifacts,
corpus files, battery workdirs.
