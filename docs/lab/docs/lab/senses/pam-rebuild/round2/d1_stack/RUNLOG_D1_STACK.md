# RUNLOG — D1 Defense-Stack Battery (G1 + MG6 + H6)

**Date:** 2026-09-24. **Prereg:** `2b3a485fca5a1ce0953f8db243f976f398cd1cd9` (committed alone).
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
**Workdir:** `~/workspace/pam_round2/d1_stack/`.

## Build

- `gen_d1.py` (deterministic Python glue, zero RNG): builds trial tables from
  branch sources, a hand-verified Python mirror of the frozen stack rules,
  `EXPECT_D1.tsv` (758 trials), `EXPECT_D1_CELL.tsv`, `stack_records.zag`
  (generated trial/gatt init-functions), `gatt_leg3_*.txt` (frozen-key cell tags).
- `stack_main.zag`: pure-Zag battery. Gate = exact G1 port; guard = MG6
  three-arm rule; hardening = H6 R1–R4 + in-Zag attestation
  (`hex(sha256(KEY|seq|fixture|jG|confG))` vs sidecar).
- Substrates `R33_NATIVE_IO_V1.zag` (e6379ddb…) and
  `R33_NATIVE_SHA256_V2.zag` (9824f6db…) copied byte-identical from the
  pinned toolchain (IO matches the branch-pinned SHA).
- znc gotchas hit: array literals rejected for large tables → init-functions
  with `t_put64` (gen_guard.py pattern); gatt must be ASCII hex (not raw
  bytes); veto-arm attribution needs explicit flags (not a count).
- Compile: ~6 min for the 1.3 MB generated source; binary 9.0 MB.

## Runs (byte-identical ×3)

16 streams × 3 runs. SHA-256 over all 16 outputs per run:

- run1: `d38b3d8a3cf3756de36fb3018da65022f2dd8d4cd95cf7860701e5b47eb2a6bf`
- run2: `d38b3d8a3cf3756de36fb3018da65022f2dd8d4cd95cf7860701e5b47eb2a6bf`
- run3: `d38b3d8a3cf3756de36fb3018da65022f2dd8d4cd95cf7860701e5b47eb2a6bf`

Byte-identical: PASS. 758/758 trials match EXPECT_D1.tsv (0 mismatches).

## Per-leg results

| Leg | Trials | Installs | False installs |
|---|---|---:|---:|
| leg1 (43 V2-D candidates) | 43 | 0 | 0 |
| leg2 (12 TMB-5 wrongs) | 12 | 0 | 0 |
| leg3_C1 | 4 | 1 (correct) | 0 |
| leg3_C2/C3/R1/R2/H1/T1/W1 | 19 | 0 | 0 |
| leg3_CC1 | 4 | 0 (wrong pair vetoed) | 0 |
| leg3_CC2 | 4 | 1 (correct) | 0 |
| leg4_clean/withhold/install/decoy | 672 | 0 | 0 |

## Kill bars

- **KB-D1a (0 false installs):** PASS. 0 false installs across all 758 trials.
- **KB-D1b (≥26/34 true retained):** FAIL → KILL. 0/34 true candidates install.

## Honest F5-less report (8 TMB-5 false accepts)

Without F5, the 8 TMB-5 false accepts are refused by G1+MG6:
- 3 reach install proposals and are vetoed by MG6's temporal arm
  (`|Δseq|` 1–5 < 20): idx 19, 22, 25.
- 5 never form corroborated proposals (gate prov/reanchor): idx 16, 21, 24, 27, 29.
- The COL-4 false accept (idx 30) never forms a proposal.

## Why KB-D1b fails

The 4 true install proposals (idx 4, 18, 26, 37) are all vetoed by MG6's
temporal arm (`|Δseq|` 1–5). True corroborators on this geometry are as
temporally clustered as the wrong ones; the guard cannot distinguish them.
G1's sequential re-anchoring additionally misses true pairs with
`|Δseq| ≥ 20`. The conjunction is too costly: 0/34 retained vs the 26/34 bar.

## Verdict

**KILL** — per frozen KB-D1b. See `VERDICT_D1_STACK.md`.
