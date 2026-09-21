# Z3 Build Log

**Arm:** Z3 — Budgeted chunks (ECON family)
**Date:** 2026-09-21
**Compiler (frozen):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Source:** `units/arms/Z3/cl/arm.zag` (pure Zag, one binary, `argv[1]` selects mode)
**Substrate (required):** `units/arms/Z3/substrate/R33_NATIVE_SHA256_V2.zag`,
  `units/arms/Z3/substrate/R33_NATIVE_IO_V1.zag`

## Authority and corrections

1. The Track A coordinator's original dispatch ("Token→chunk/XFER") was wrong
   for Z3 and was discarded in full.
2. The coordinator's first corrected §3 quotation was still a paraphrase; the
   second correction (2026-09-21) supplied the byte-verified verbatim frozen
   row, which was programmatically compared against `units/arms/briefs/Z3.json`
   (ID, name, family, mechanism, kill wording all match exactly). The verbatim
   row governs.

## Build commands

```bash
cd ~/workspace/tnn-lab/units/arms/Z3
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  cl/arm.zag -o ~/workspace/z3scratch/build/z3
```

Output binary: `~/workspace/z3scratch/build/z3` (234,460 bytes, x86-64 ELF,
statically linked). Warnings only (discarded `nio_close` results; one
apparent false-positive A0107 in `write_file`). No errors.

## Implementation defects fixed (mechanism parameters unchanged)

All fixes correct the implementation to match the frozen ARM_SPEC.md; no
economic parameter (B, prices, spans, predicates) was altered.

1. **Patched-content recalls now pay budget and count access.** `b_recall` on
   a `F_PATCH` slot previously returned without debiting `c_recall + read`
   and without incrementing `accs` (broke consolidation accounting).
2. **`b_ingest` revive path.** Re-ingesting a live ID now returns 0 without
   debiting `c_create` (was double-charging on every M2/M7 repeat ingest;
   caused M7 `budget-exhausted-r1`).
3. **Half-B double division.** `t_m1` set `s.budget_b = Z3_B/bdiv` and
   `b_epoch_open` divided by `bdiv` again (B/4, not B/2). Now
   `s.budget_b = Z3_B` always; the epoch budget is `Z3_B / bdiv`.
4. **M2 op-ledger oversize.** `16*nspans_max` entries × 64B exceeded the
   2^25-byte slice limit on t2-prose (35.7MB). Reduced to `2*nspans_max`
   (re-ingests revive and do not log). Also made `t_m2` set
   `s.budget_b = Z3_B` for consistency.
5. **M8 insertion-queue oversize.** `ins_cap=20000` overflowed on ~46k
   inserts (prose+code+fresh+phase3). Now `np+nc+10000`.
6. **17-arg `b_led` calls** corrected to the 16-arg layout (2 instances).
7. **Slice-field aliases routed through pointers** per ZNC-2026-09-21-004
   (local-struct slice-field alias rejected by native codegen).
8. **Economic ledger** fixed at 200,000 × 32B = 6.4MB per epoch (under the
   2^25 indexed-slice limit); `b_epoch_open` resets the per-epoch ledger
   (documented in ARM_SPEC.md §5/§9).

## Pre-battery freeze

`docs/lab/units/arms/Z3/ARM_SPEC.md` was written and committed
(`9fb54b981dda` on `tnn-native-lab`) **before** the scored 1× battery.
Mechanism parameters frozen; only the implementation defects above were
fixed afterward (all are bug fixes toward the frozen spec, not parameter
changes).

## Test record

- Targeted smoke tests per mode (2026-09-21, pre-freeze implementation
  validation; not scored).
- Scored 1× battery: `run_battery.sh` (17 legs × 2 runs, stdout diffed;
  M8 gate 5 perturbations × 2 reruns, byte-identical artifacts).
  - First scored run: 17/18 legs pass; `m2-t2-prose` failed (ledger
    oversize, defect #4 above); M8 gate PASS.
  - Second scored run (fixed binary): see VERDICT.md.
- Half-B diagnostic (`m1h-1x-prose`, `m1h-1x-code`): 100.0% recall on both
  corpora at B/2 (spans 512/1024 vs 256/512 at full B). 0% accuracy drop;
  the >15% cliff kill criterion is NOT triggered.

## Reproducibility

All modes are pure Zag with no randomness. Slot placement is a pure function
of unit ID. Every battery leg runs twice with stdout diffed (byte-identical
rule); the M8 gate byte-compares all artifacts across perturbations and
reruns.
