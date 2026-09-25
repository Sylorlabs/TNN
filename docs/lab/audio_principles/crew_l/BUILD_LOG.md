# Crew L build log

## Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned per task).

## 2026-09-25 — initial build (pre-registration)
- Wrote `src/core.zag` (WAV io, tone renderer, input organ: 2048/Hann framing,
  integer RMS, direct normalized autocorr F0 lags 36..551 with parabolic
  interp, ZCR, naive-DFT N=512 band decomposition 0-2k/2-4k/4-8k/8-16k via
  Q30 twiddle tables, onset detector, thirds-ratio env classifier;
  semitone-grid planner) + 4 mains (organ/render/loop/hfloop).
- Build method: `build.sh` concatenates `core.zag` + `main_<m>.zag` (avoids
  `@import` cwd-vs-file ambiguity), compiles each with pinned znc.
- Numeric tables: `[]i64` via `(p[0..N*8]) as []i64` — verified non-aliasing
  on this toolchain with a dedicated probe (two consecutive 512-entry
  allocs, pattern write/read + clobber test, all clean). No `as []i32/u32/u16`
  anywhere. No slice > 2^25 B (largest: 2.4 MB sample buffer, 2×2 MB twiddle
  tables).
- Probes confirmed: `_zag_arg(n)` works with argc=0; `_zag_print` adds no
  newline (explicit `\n`); `[]u8 ==` is not content equality (manual `streq`).
- Analyzer warnings on build: benign (cosr range-reduction loops flagged
  A0107; one false-positive A0101 on the lag loop — indices verified
  0..515 into a 516-entry table).
- Smoke tests (dev renders 440 flat / 220 rise / 880 decay):
  - organ F0 vs frozen scorer F0 agree to 4th decimal (440352 vs 440.3516 mHz
    scale; 220705 vs 220.7050489; 880177 vs 880.1772306); env classes agree.
  - loop smoke (440 flat, on-grid): iter0 plan 440000 → organ meas 440352
    (estimator bias, same as scorer) → deadbeat correction → converged by
    iter2, stable at iter3. Loop is functional.
- Reference WAVs: 10 files, deterministic Python synthesis (closed-form +
  fixed-seed LCG noise), SHAs in `manifests/ref_manifest.json`.
- Intent list: 20 cases, integer-Hz targets in [90,1175] with
  semitone-quantization error in [1.0%, 2.9%], env cycling flat/rise/decay,
  sealed in `manifests/intent_manifest.json`. Disjoint from dev {440,220,880}.

## Deferred to post-commit
- Organ self-check (§3.5) on the 10 ref WAVs.
- L battery: 3× runs of the 20-case loop, frozen scoring, Wilcoxon, L-R1 curve.
- Dither spot check (§5.3), HF-reduction variant, SHA grep audit (§5.1).
