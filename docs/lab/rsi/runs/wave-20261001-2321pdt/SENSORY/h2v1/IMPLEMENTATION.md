# H2v1 IMPLEMENTATION (SENSORY, wave-20261001-2321pdt)

Prereg: PREREG_SENSORY_H2V1.md (committed alone, 58a1a0d7f).
This file documents the implementation, committed separately.

## Files

- r11_baseline.zag: byte copy of the frozen r11 substrate with only
  the @import line repointed at ./sub/R33_NATIVE_IO_V1.zag
  (diff-verified: exactly one line differs).
- sub/R33_NATIVE_IO_V1.zag: byte copy of the 20260924 IO substrate,
  sha256 e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (verified at copy time).
- h2v1_clouds.zag: r11_baseline.zag plus (a) h1_dens verbatim from
  H1v2 (seeds 601/602), and (b) the frozen H2v1 FORWARD-SCATTER DECK
  FIELD block verbatim from the prereg, replacing the baseline
  "thin cirrus" block. Nothing else changed.
- h2v1_verify.zag: H1v2 verifier with KB10 replaced by KB10-ANCFIELD
  (Clause A: argmax field x < 512; Clause B: field range >= 0.40).
  Point sets, keep-count asserts, KB2 (H1-family alpha), KB3-KB9,
  KB11 unchanged.
- tools/bmp2png.zag: H1v2's BMP to PNG converter, unchanged.
- run_h2v1.sh: H1v2's pipeline script with names swapped.

## Build

All compiled with src/tools/toolchain/znc_linux_x86_64_abed8aa1
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
--no-zagd --no-analyze. Pure Zag. Safebin PATH. No Python.

## Prereg compliance

The generator contains the frozen block verbatim (modulo comments).
The verifier implements the frozen bars. KB10-ANCFIELD is the
prereg's redefined KB10. Baseline gate (a)(b)(c) runs first in
run_h2v1.sh.
