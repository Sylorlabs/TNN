# PROVENANCE.md — image_nolayers

- Fixture: `~/workspace/your_files/image_repro/original_512.bmp`
  (512x187 24-bit BMP, SHA-256
  `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`),
  sealed entry in `~/workspace/your_files/image_exact_NEW/SHASUMS.txt`.
- Layered baselines (pre-existing, not rebuilt here):
  - v3 precursor: `~/workspace/image_exact_work/` @ `d64892bc3911`
    (30.33 dB / 0.9177 / 47.5%).
  - zoom fork: `~/workspace/image_zoom_fork/` @ `2384090e54cf`
    (30.80 dB / 0.9620 / 19.9%).
- This fork: `~/workspace/image_nolayers/` (pure Zag, zero RNG).
  Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- metrics.py: PSNR = mean of per-channel dB; SSIM = Gaussian-window
  per-channel mean (same script as layered forks).
- Evidence commit: branch `tnn-native-lab` (never main).
  Code + docs + verdict evidence only (no binaries, .zagd, BMP/PNG).
