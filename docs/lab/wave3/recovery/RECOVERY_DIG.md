# Recovery dig — R15–R27 pre-git sources and codex_restore_v62

Date: 2026-09-19. Objective: exhaust every remaining lead for the R27 training
sources (`r15_master_training.py`, `r23_experiments.py`, `r25_release.py`,
`r26_experiments.py`, `r27_experiments.py`) and the `codex_restore_v62` transfer,
per the RECOVERY_SPEC.md leads in `wave3/perceptual-origins/` and
`wave3/trace-op-semantics/`. Verdict: **repo-side recovery is exhausted.**

## Leads checked

1. **This VM's filesystem** — `find /` for all five filenames and any
   `*codex_restore*`: zero hits.
2. **`archive/transfer-staging/codex_restore_v62/v62.tar.xz.b64`** — the file is
   **0 bytes** (empty blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`). Dead lead.
3. **`archive/transfer-staging/codex_restore_v67/`** — contains only
   `R33_N17_V65_V66_V67_COMBINED.tar.xz` (0 bytes) and `combined.b64.part00`
   (18,001 bytes). The part decodes to an xz stream listing R33 checkpoint
   adapter material (V65/V66 Zag adapters, `r27_native_state_semantics_v4.zag`).
   No R15–R27 training sources, no opcode implementations, no perceptual code.
4. **`archive/transfer-staging/r46_transfer/r46.tar.xz.b64`** — R46
   factorized-predictive-latent experiment bundle (prereg, dev jobs, results).
   Grepped: no training-source references, no opcode defs, no perceptual code.
5. **`archive/transfer-staging/recovery/`** — `TNN_R36_R42_RECOVERY_20260917`
   (R36 context-identification jobs) and `_V2_` (R41 strategy-reliability).
   Grepped: no hits for any of the five filenames, `SELF_VERIFIED`, opcodes,
   or perceptual/torch code. These are later-generation experiment bundles.
6. **GitHub code search** — `r27_experiments` in `sylorlabs/tnn`: 0 hits
   (confirms the wave-3 census).

## Conclusion

Nothing in the repo, the VM, or any transfer bundle contains the R15–R27
training sources, the 19 trace-opcode implementations, or the perceptual
training code that produced the 76 torch parameters. The **only remaining
lead is Micah's own pre-git environment** (the machine where the R15–R27
sessions ran, pre-2026-08-25).

## Intake protocol (if the files surface)

If the five files are found, extract in this order before anything else:
1. The 19 trace-opcode implementations (validate against the stored 435 traces —
   an implementation is only accepted if it reproduces stored op behavior).
2. The perceptual training code (loss, data, optimizer config, seeds — the full
   provenance the 76 parameters are missing).
3. The structural-revision decision code (to cross-check the native NSR loop).
4. Anything that explains how the 76 perceptual parameters were learned.

Record full provenance this time. Do not re-run training without a prereg.
