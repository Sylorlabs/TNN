# Evidence inputs for the phase-2 155-count reporter

These two logs are the INDEPENDENT VERIFIER's reproductions (2026-09-20),
not the modality workers' own logs.

- `audio_run_a.txt` — built from the committed audio sources
  (`se2a_ingress.zag`, `se2a_memif.zag`, `se2a_main.zag` at remote commit
  `766a51c12d9a`, which includes the per-pair save-dir fix) with the pinned
  toolchain `znc_linux_x86_64_abed8aa1`, run `harness` from clean state.
  Binary SHA256: `7e6ca60f447ebf16164d5dae082da565a2224a565b9906d1a63c6c080302ec76`
  (identical to the audio worker's reported hash). rc=0.
- `vision_run_a.txt` — built from the committed vision sources with the
  pinned toolchain, run `harness` from clean state. Binary SHA256:
  `90b49b4b4ac2449a01e45efbf5e49128b14582a1182a7ebd91e8673f1ebc2610`
  (identical to the vision worker's reported hash). This file is
  BYTE-IDENTICAL to the vision worker's committed `logs/run_harness_a.txt`.
  rc=0.

The reporter (`count_phase2.sh`) reads these plus the cross-cutting harness
log produced by `run_phase2_harness.sh` and counts the 155 preregistered
checks: A32/B18/C20/D48/E24 (manifest-driven) + F2/G2/H4/I5 (cross-cutting).
