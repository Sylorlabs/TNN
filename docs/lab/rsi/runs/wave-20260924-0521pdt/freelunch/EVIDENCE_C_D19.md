# EVIDENCE C-D19 - raw wave artifacts index

Wave wave-20260924-0521pdt, Worker C. All files under
docs/lab/rsi/runs/wave-20260924-0521pdt/freelunch/evidence/.

## Renders (1024x1024 24-bit BMP, 3145782 bytes each)

- base.bmp: baseline rebuild, sha256
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d
  (byte-identical to the committed r8c baseline, S14 record).
- var1.bmp, var2.bmp, var3.bmp: D19 variant, three runs, sha256
  30a9cd5c404c4b14393660cfc305064c56e6e19745e093b0b146feb013a
  (all three identical: KB1-DET PASS).
- Full list with hashes: evidence/SHA256SUMS.

## Traces

- base_trace.md: baseline elaboration trace (no D19 section).
- var_trace1/2/3.md: variant traces, each containing "D19 dabs: 208"
  (KB6 budget gate).

## Logs

- evidence_compile_baseline.txt, evidence_compile_variant.txt,
  evidence_compile_verify.txt: znc build logs (pinned toolchain
  498abcb5...; all three compiled clean).
- evidence_base_run.txt, evidence_var_run1/2/3.txt: program stdout
  per render.
- evidence_verify.txt: s19_verify.zag output; the kill-bar numbers:
  KB2_FOCUS_BP 11804 (bar 13000, FAIL), KB3_STONE_BP 19027 (bar 12000,
  PASS), KB4_SKY_BP 10000 (bar <= 11000, PASS), KB5_MEANABS_X100 5
  (bar <= 800, PASS).
- evidence_walltime.txt: baseline 979 ms, variant avg 934 ms
  (KB6 cost PASS, 0.95x).

## Sources (all pure Zag, zero RNG, no Python)

- s19_focus.zag: r8c copy plus the D19 mechanism (frozen in
  PREREG_C_D19_0521.md, commit 35f81a256).
- r8c_baseline.zag: import-rewritten r8c copy, no D19.
- s19_verify.zag: kill-bar checker.
- sub/R33_NATIVE_IO_V1.zag: vendored Linux IO substrate, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (blob from wave commit 72ef158fc).
- run_d19.sh: the full harness (static checks, pins, builds,
  renders, gates).

Build binaries lived in freelunch/bin/ during the wave and are not
committed; they rebuild byte-identically from the sources above with
the pinned toolchain.
