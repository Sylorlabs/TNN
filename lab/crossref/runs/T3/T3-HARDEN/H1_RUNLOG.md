# H1 — CERT Plant Artifact Boundary: RUNLOG

2026-09-23. Tier-3 hardening probe H1 (prereg `PREREG_TIER3_WAVE2.md`).
All work in `~/workspace/scratch-crossref/T3/HARDEN/h1/`.

## (a) Artifact boundary documentation

- Located `dirty1_variation.zag` (`plant_urandom()`, lines 102-113).
- Verified against pinned `znc_linux_x86_64_abed8aa1`:
  - `nio_open_readonly` (line 104): absent from `R33_NATIVE_IO_V1.zag`
    (defines only `nio_open_root`, `nio_open_child`); zero substrate hits.
  - `_zag_rand` (line 110): absent; pinned znc rejects with
    "call to unknown function '_zag_rand'" (reproduced on 1-line probe).
- Binary unreproducible from source with pinned toolchain, as Tier-2 reported.

## (b) 0-flip independence

- Rebuilt `flipcount.zag` (pure Zag) with pinned znc.
- Full `results_source.tsv`: 35 rows, 0 flips (34 confirmed, 1 inconclusive).
- Minus 2 `dirty1_urandom` rows: 33 rows, 0 flips (32 confirmed, 1 inconclusive).
- The unreproducible plant is not load-bearing for any flip/no-flip decision.

## (c) Clean-room plant

- Wrote `plant_cleanroom.zag`: same RNG-in-decision-path trap using only
  known raw syscalls (`_zag_raw_syscall` with 7 args, NUL-terminated paths
  via `z_cstr`, word→byte decomposition per ZNC-2026-09-21-002).
- Builds: "wrote native binary plant_cleanroom (18732 bytes main, 0 external tools)".
- Rebuilt committed `rngscan_v3_rb.zag`; scan: `hits=11 verdict=FAIL` (exit 1).
  Substantive: 3× raw-syscall-on-variation-path, 3× `_zag_slice_ptr` banned
  token, 2× uninitialized-use (scanner false positives on `nio_alloc`'d
  arrays, recorded honestly). 2 hits are probe-harness artifacts.
- The byte-wise path construction evades the `urandom` token check and
  binary-bytes check, but the plant still FAILS via the defense-in-depth
  raw-syscall ban. The certifier catches the mechanism class.

## Result

Verdict **ARTIFACT-BOUND** (see `H1_VERDICT.md`). No Tier-2 claim breaks.

## Commit

`plant_cleanroom.zag` source + `attest.json` under
`crossref/runs/T3/T3-HARDEN/evidence/cert-cleanroom/`. No binaries committed.
