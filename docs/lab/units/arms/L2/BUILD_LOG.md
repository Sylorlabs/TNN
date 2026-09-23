# BUILD LOG — L2 (Epoch-Relative Position IDs)

Restart crew, 2026-09-21. All values below were independently verified by
this crew; the inherited build log was not trusted.

## Toolchain
- Frozen compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (md5 `0645ba22e9e61041be17e46eac81e8a0`).
- `znc check cl/arm.zag` — OK, all capability claims proven; analyzer
  reported 57 warnings (ignored-return warnings plus the file-writer
  dead-loop false positive also seen on L1; none affect semantics).
- Native build — succeeded 2026-09-21 ~07:47 UTC.
- Binary: `~/workspace/tnn-lab/work/l2b/l2_bin`
  (md5 `f39607c5c37d8d12b4563f66c38b80cc`, 255,010 bytes executable,
  243,641 bytes main). Build binaries are never committed.
- Memorizer (frozen harness control):
  `~/workspace/tnn-lab/work/l2b/memorizer_bin`
  (md5 `4be8ecbdede7497f94355f84b76d4a93`), built from
  `units/arms/harness/memorizer/cl/memorizer.zag` with the frozen compiler.
- Substrate: `substrate/R33_NATIVE_IO_V1.zag`
  (md5 `19bdcc5212998682ed733b43c09a23d0`),
  `substrate/R33_NATIVE_SHA256_V2.zag`
  (md5 `70e1be7d0c7caf2f9f037112ce3b2f03`) — byte-identical copies of the
  frozen substrate (verified by md5 against the frozen toolchain copies).

## Implementation notes
- `cl/arm.zag` (~2,030 lines): epoch-relative RID `(epoch<<24)|rel`,
  append-only write-once translation table (span→RID index + RID→location
  records), segment arena with 1 MiB segments / 64 KiB epoch-segments, touch
  bitmap + `touch_n*20 > seg_next*16` bump rule (the >5%-of-segments rule
  with the 16× sub-segment scaling folded in), bump ledger, revision map,
  ingest / recall / kill / pin / weaken / defect / revise / eviction paths,
  M1–M8 modes, A15 trainer swap probe, M8 artifact writers, exact
  shared-runner dispatch.
- `l2_id_changes` is a snapshot audit (RIDs snapshotted at mode start,
  re-derived at mode end; any mismatch counts), emitted by the
  store-mutating modes m1 and m4 — not a runtime counter in the shared
  recall path.
- `l2_xepoch_recalls` / `l2_xepoch_misses` are per-instance counters in the
  shared recall path; the M4 dedicated 200-unit translation audit runs
  through the same counter, so its recalls are a subset (no double count).
- Epoch overflow refused loudly (exit 2) before the 8-bit field wraps.
- No RNG in any decision path (verified by source review; the only
  nondeterminism-adjacent inputs are the M8 harness perturbations, which
  the gate proves do not change any artifact byte).
- The arm uses `[]u8` arenas with explicit little-endian accessors for all
  indexed tables — unaffected by ZNC-2026-09-21-007 (`as []i32` miscompile;
  the arm has zero such casts).

## Bugs found and fixed during this restart (before the evidence run)
1. **argc guard dropped m8 arguments (ZNC-2026-09-21-007).** `main()`
   gated `_zag_arg(3)`/`_zag_arg(4)` on `argc>=4`/`argc>=5`, but this znc
   build passes `argc=0` to `main` regardless of the real argument count
   (verified with a probe: 4 user args → argc=0; `_zag_arg(n)` itself is
   correct). The m8 outdir and perturbation selector were therefore
   silently empty: no M8 artifacts were written and every perturbation ran
   as the unperturbed case. Fixed to read `_zag_arg(3)`/`_zag_arg(4)`
   unconditionally (they return "" when absent; only m8-1x consumes them).
   Lesson recorded in `~/AGENTS.md`.
2. **m8 stdout carried the perturbation label.** The METRIC_JSON field
   `m8_perturbation` made `stdout.txt` differ across perturbations, which
   the frozen M8 gate (`m8_compare.py`, ARM_INTERFACE.md §7) counts as
   FAIL — stdout must be byte-identical across all five perturbations.
   The field was removed from stdout (the harness records the perturbation
   in the run directory layout `m8/<pert>/run<N>`). No mechanism semantics
   changed.
3. **Scorecard assembler double-counted the M4 audit.** The inherited
   `evidence/scorecard_assemble_l2.py` added the dedicated audit recalls to
   the cross-epoch denominator, but the audit already shares the
   instance's `l2_xepoch_recalls` counter. Fixed to use unique
   instrumented recalls across all metric modes, with audit fields kept as
   detail-only; per-mode breakdown added.

All evidence below comes from the fixed binary (md5
`f39607c5c37d8d12b4563f66c38b80cc`).

## Evidence runs
- Full frozen battery (`units/arms/harness/run_battery.sh`) with the final
  binary, workdir `~/workspace/tnn-lab/work/l2b/battery_r1`, canonical
  corpus root `units/arms/harness/corpora/r1`
  (prose 5,422,721 B; code 9,515,341 B; t1/t2/t3/churn_fresh + vocab files
  per MANIFEST.json). An earlier run against a stale `corpora/r1` copy
  (prose 5,638,480 B, missing `mem_vocab_sorted.txt`) was discarded.
- Every leg run ×2; stdout byte-identical across both runs for all 18 legs.
- M8 gate: `m8_gate.sh` (clean/frag/aslr/starve/freelist × 2 runs each),
  compared with frozen `m8_compare.py` over store_hashes.txt,
  store_chain.txt, ledger.bin, ledger_chain.txt, alloc_trace.txt,
  stdout.txt, stderr.txt → **M8GATE PASS** (`battery_r1/m8/GATE.txt`).
- Scorecard assembled evidence-side with
  `units/arms/L2/evidence/scorecard_assemble_l2.py` → `evidence/scorecard.json`.
  (The frozen `scorecard_assemble.py` is B-64-specific and crashes on L2's
  M7 fragment with `KeyError: 'm7_na_reason'`; it was not modified.)

## Results (from `evidence/scorecard.json`, battery end 2026-09-21T08:23:06Z)
- Legs: 18 passed, 0 failed; every leg stdout byte-identical ×2.
- M1: 100.0 recall / 100.0 boundary, prose (84,731 units) and code
  (148,678 units); A15 swap probe PASS (PROVISIONAL-PENDING-FREEZE).
- M2: ETC=1 (immediate) on t1/t2 prose+code; final recall/boundary 100.0.
- M3: survival 100.0, fresh recall 100.0, freeze CLEAR.
- M4: rev boundary/content 100.0; kill audit clean.
- M5: memory/source-byte 4.307 (generic 1.5x bar not met — slot-table
  figure is capacity-provisioned, see verdict), audit 16.2 entries/KB
  (generic 10/KB bar not met). Not L2 binding kill bars; reported honestly.
- M6: recall/boundary/revision 100.0, tax 0.0 both directions; memorizer
  validity gate PASS (drop 54.8 ≥ 15).
- M7: hit rate 100.0, cell PASS (PROVISIONAL-PENDING-FREEZE: C′/schedule).
- Kill bar (i): 0 within-epoch ID changes → CLEAR.
- Kill bar (ii): 4,334 cross-epoch recalls, 0 misses → CLEAR.
- Epoch bumps observed: 121 total (m4-prose 39, m4-code 35, m6-p2c 15,
  m6-c2p 12, m7 20) — the bump rule fires under revision/defect churn.
