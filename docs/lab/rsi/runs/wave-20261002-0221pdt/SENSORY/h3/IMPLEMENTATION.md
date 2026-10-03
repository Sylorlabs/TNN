# IMPLEMENTATION.md - H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT (SDLGRAD)

Wave: wave-20261002-0221pdt. Lane: SENSORY.
Frozen prereg: PREREG_SENSORY_H3.md (commit 012f390c3, prereg-only;
commit-order self-check PASS: no H3 implementation artifact existed
before that commit).
Toolchain: safebin only, znc pinned
(src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Pure Zag, zero Python invocations (NAMECHECK Step 0).

## Frozen block conformance

The implementation contains the frozen H3 block verbatim (modulo
whitespace) inside b_skydome, inserted after the three horizon/zenith
mix lines and before the `if (dy < 0.0)` branch. Machine checks:

1. b_skydome body (h3_dome.zag lines 300-381, 82 lines) minus the
   14-line frozen H3 block is byte-identical to the b_sky body
   (lines 231-298, 68 lines): diff clean.
2. Full-file diff r11_baseline.zag vs h3_dome.zag: exactly two hunks:
   `299a300,382` (pure addition of the b_skydome function) and
   `796,798c879,881` (the three direct-sky call sites switch
   b_sky -> b_skydome). No other delta. The b_tshade ambient calls
   (lines 742-744) still call the original b_sky; the moon path is
   untouched.
3. r11_baseline.zag vs r11_alien.zag: exactly one differing line
   (the @import repoint to ./sub/R33_NATIVE_IO_V1.zag). Baseline
   gate (a) PASS.
4. IO substrate sub/R33_NATIVE_IO_V1.zag sha256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
   matches the frozen vendored hash.

## Verifier

h3_verify.zag: adapted from the prior wave's frozen h2v1_verify.zag
(world-model copies of camera basis, b_trace, b_moonhit; fixture
point sets; BMP reading; bar computations all carried over
verbatim). Changed for H3 only:

- KB2 alpha: v_alpha now recomputes the VERBATIM r11 cirrus alpha
  (h3_base_alpha: b_fbm2 seeds 601/602 with baseline offsets,
  m = ss((cm-0.56)/0.16) * ss((dy-0.02)/0.15) * 0.55). H3 does not
  change clouds.
- KB10: v_field replaced by v_dgfield, the frozen H3 dome field
  (dg = clamp(1 + 0.15*ss((samt-0.62)/0.12) - 0.20*ss((0.68-samt)/0.12),
  0.60, 1.40)); bar is argmax-x < 512 AND range >= 0.20.
- Comment header updated (H2v1 -> H3); usage string updated.

Build note: two self-inflicted splice errors during adaptation
(dropped fn-main header lines; dropped v_dgfield's closing brace;
an rl/rll typo) were caught by the compiler and repaired before any
render; no prereg content changed. The 40 em-dash bytes flagged by
check_no_dash.sh in h3_verify.zag are all inside verbatim-copied
frozen-substrate deliberation comments (T0/T1/T3), kept byte-identical
to preserve the "verbatim copy" claim; every line authored by this
lane is dash-clean per the standing style rule.

## Build evidence

- bin/r11_baseline (79178 bytes), bin/h3_dome (87370 bytes),
  bin/h3_verify (105337 bytes): all compiled with the frozen
  toolchain, --no-analyze (analyzer warnings only, same L0012 string
  pattern the prior lanes' tools carry).
- 256 smoke renders: out/smoke_base/r11_alien_256.bmp and
  out/smoke_h3/r11_alien_256.bmp both completed ("done", 196662
  bytes each). Pipeline is functional.
- Full 1024 pipeline (run_h3.sh): launched 2026-10-02 ~02:44 PDT in
  background (proc_65e1974e3806): baseline gate (2x 1024, sha match
  against 72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b),
  geometric validator on the rebuilt baseline, 3x 1024 H3 renders
  (KB1), then h3_verify kill bars KB2-KB11.

## Frozen predictions (design_calc.zag, cited by the prereg)

At (GW, GC) = (0.15, 0.20): KB3 sunmean 9.87, antimean -6.12, diff
15.99; KB4 variance 86.10; KB7 fsmean +0.18, bigfrac 0.2777; KB11
max|dL| 15.91; KB2 0.1250; KB10 range 0.349, argmax x = 320; KB5/KB6
0.00 by construction; KB8 smooth-field pass; KB9 0 new fbm evals;
KB1 deterministic pass. The bars decide on real renders.

## Verdict section (filled when the pipeline completes)

Per-bar results:

| Bar | Frozen bar | Measured | PASS/FAIL |
|-----|-----------|----------|-----------|
| KB1-DET | 3/3 renders sha256-identical | | |
| KB2-COVERAGE | [0.08, 0.60] (exp 0.1250) | | |
| KB3-LIGHTLOGIC | sunmean >= 3.0 AND diff >= 6.0 (pred 9.87 / 15.99) | | |
| KB4-STRUCTURE | var >= 40.0 (pred 86.10) | | |
| KB5-NONREG-TERRAIN | mean |dL| <= 1.0 (exp 0.00 by construction) | | |
| KB6-NONREG-MOON | mean |dL| <= 1.0 (exp 0.00 by construction) | | |
| KB7-SKYCALM | |fsmean| <= 5.0 AND bigfrac <= 0.35 (pred 0.18 / 0.2777) | | |
| KB8-ANTIGRAIN | acutance ratio <= 1.15 | | |
| KB9-COST | wall <= 2.0x baseline (exp 0 new fbm evals) | | |
| KB10-ANCDOME | argmax-x < 512 AND range >= 0.20 (pred 320 / 0.349) | | |
| KB11-DROPOUT | frac(|dL|>60) == 0.0 | | |

- Red-team investigation documented (REDTEAM_ARTIFACTS.md): pending
- Baseline gate evidence: (a) one-line diff PASS; (b) pending;
  (c) pending
- Verdict: PENDING (pipeline in flight)
- Verdict line: ________________________________________
