# BUILD_LOG.md — Crew P organ

## Toolchain
- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Pure Zag, zero external tools (compiler reports "0 external tools").

## Source
- `organ.zag` (745 lines), SHA-256:
  `eadfc83027b2c469d0f2f8534029ba2ecb3413a78f0908d4a25731aa00d33bfb`
- Frozen design: `FROZEN_ORGAN.md` (2026-09-25).

## Binary
- `organ`, SHA-256:
  `1ed4bfba250336ad1da3fdbc66e865fe09cb6913854894c2faf0b119b53a5128`
- Built 2026-09-25. Regenerable from source; NOT committed (no binaries in repo).

## Algorithm notes (see FROZEN_ORGAN.md)
- F0: normalized autocorrelation (lags 1..551) with YIN cumulative-mean
  period selection. The plain argmax provably fails 80–112 Hz under the
  2048-sample Hann window (verified 2026-09-25); YIN recovers 80–1200 Hz.
- Fixed-point/i64 in `[]u8` arenas (no indexed `[]f64`, per 2026-09-25 probe).

## Validation (dev renders, not test material)
- pitchabs: 48/48 (24 classes x 2 pools)
- env: 6/6 (3 classes x 2 pools)
- rhy: 2/2, hf: 2/2 (dev)
- Organ and frozen scorer agree on all dev renders.
