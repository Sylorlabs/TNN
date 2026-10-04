# IMPLEMENTATION.md - H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK
Wave: wave-20261001-2021pdt. Lane: SENSORY. Prereg: PREREG_SENSORY_H1V2.md,
frozen and committed alone at 48bd41494 before any implementation file
existed. Pure Zag, safebin toolchain, zero Python invocations.

## Build provenance

- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use).
- IO substrate: docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/g1/sub/
  R33_NATIVE_IO_V1.zag copied byte-identical to h1v2/sub/R33_NATIVE_IO_V1.zag,
  sha256 e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (matches frozen hash at copy time).
- Baseline h1v2/r11_baseline.zag: byte copy of
  docs/lab/imagination_discovery/img/r11_alien.zag
  (sha256 29ca7b0d79ca93aa7d2205e7195edae71af5f09971614cafaf62323dfe4e2e3b)
  with exactly one line changed: the @import repointed to
  ./sub/R33_NATIVE_IO_V1.zag (diff-verified, line 25 only).
- Variant h1v2/h1v2_clouds.zag: baseline + h1_dens/h1_alpha (seeds 601/602,
  same placement language as the discarded H1) + the frozen H1v2 block
  replacing the "thin cirrus, warm-lit on the sun side" block inside b_sky.
  The block is verbatim from the prereg modulo indentation (diff-verified
  after whitespace stripping). Output names h1v2_clouds_{256,1024,2048}.bmp.
- Verifier h1v2/h1v2_verify.zag: H1 verifier copied verbatim except:
  header/usage strings, the KB10 march-field conformance function and
  measurement, and the KB11 blowout counter. All point sets, formulas,
  and keep-count asserts frozen identical to H1 (diff-checked).
- Lane tools: h1v2/tools/bmp2png.zag (+ tools/sub IO copy) reused from H1.

## Baseline gate (prereg procedure)

- (a) One-line diff baseline vs in-tree source: PASS.
- (b) Two 1024 baseline renders byte-identical; both
  sha256 72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b,
  matching the 1721pdt baseline sha from the prereg: PASS.
- (c) Geometric validator on rebuilt baseline: VALIDATOR: PASS.
  SKYWIN_KEPT 48 (>=36), TERRAIN_KEPT 64 (>=56), MOON_KEPT 16 (>=12),
  FULLSKY_KEPT 144 (>=100), SUNHALF_N 25, ANTISUN_N 23 (each >=12).
- Baseline wall: base1 412 s, base2 483 s (evidence/render_base{1,2}.log).

## Kill-bar measurements (verifier output, evidence/killbars.log)

Variant render sha (KB1): 3/3 byte-identical,
9394fc6d34e35cf0976a883ddb9f826bf582ae825bcce7607724d4728b5607a5.

| Bar | Measured | Frozen bar | Verdict |
|---|---|---|---|
| KB1 determinism | 3/3 identical | 3/3 byte-identical | PASS |
| KB2 coverage | 0.2916 | [0.08, 0.60] | PASS |
| KB3 light logic | sun mean +0.64, anti mean -0.08, diff +0.72 | diff >= 6.0 AND sun mean >= 3.0 | FAIL |
| KB4 structure | dL variance 89.58 | >= 40.0 | PASS |
| KB5 terrain | mean |dL| 0.45 | <= 1.0 | PASS |
| KB6 moon | mean |dL| 0.00 | <= 1.0 | PASS |
| KB7 sky calm | |mean dL| 3.58, big frac 0.1944 | <= 5.0 and <= 0.35 | PASS |
| KB8 acutance | ratio 0.981 | <= 1.15 | PASS |
| KB9 cost | 974/412 = 2.36x (pair 1), 622/483 = 1.29x (pair 2) | <= 2.0x, matched-contention sequential pairing per H1 | FAIL |
| KB10 align | mean err ~0 (<5e-7), max err ~0, N=42, degen 6 | mean <= 0.02, max <= 0.15 | PASS |
| KB11 dropout | blowout fraction 0.0 | == 0.0 | PASS |

KB9 detail: variant walls h1v2a 974 s, h1v2b 622 s, h1v2c 623 s.
H1's pairing rule (sequential, max ratio, as executed for H1's 0.89x):
max(974/412, 622/483) = 2.36 > 2.0. Extra fbm octave-evals per sky
pixel: baseline cirrus 6 (2 fbm calls x 3 octaves); H1v2 block 32
(den 6 + th 2 + gx/gz 12 + s1/s2 12); extra = 26. Note: the prereg's
frozen prediction claimed "zero new fbm evals" and "~12 multiplies per
sky pixel"; that prediction was factually wrong about the frozen block,
which carries the gradient and march taps.

## KB3 failure analysis (the decisive kill)

The sign is fixed (sun side brighter, +0.64 vs H1's -2.13 diff), but
the magnitude is an order of magnitude short: diff +0.72 vs 6.0
required, sun mean +0.64 vs 3.0 required. KB10 proves the anchoring is
implemented correctly (mean alignment error under 5e-7 against the
analytic-Jacobian reference), so this is not an implementation bug.
The mechanism produces real per-blob contrast (KB4 variance 89.58,
std ~9.5 dL; visible warm tops and dark bases in the 1024 render), but
per-blob bright/dark flanks average to near zero within each screen
half. The frozen bar measures a systematic half-level shift; the only
half-level terms in the frozen block are the sunAmt-gated ones (silver
lining at cloud edges, warm-top color mix), which are weak against the
baseline's already-warm sun-side flat cirrus. The prereg's frozen
prediction ("full lit-to-dark swing on the order of 80 dL units, ample
against the 6.0 bar") confused per-blob swing with half-mean shift.
Correct anchoring alone does not move the half-means. Mechanism-level
negative result, honestly measured.

## KB9 failure analysis

Pairing 1 (h1v2a 974 s vs base1 412 s) gives 2.36x, over the frozen
2.0x. Pairing 2 (622 s vs 483 s) gives 1.29x. h1v2a is a 57% outlier
against its siblings h1v2b/c (622/623 s), run under visibly heavier
machine contention; the matched-contention pairing did not cancel the
load difference between the baseline phase and the variant phase. The
bar as executed fails. No re-runs were shopped to rescue it.

## Red-team investigation: knowledge vs architecture
(mandatory; documented before any verdict)

Scope: dropout, flicker, banding, weirdness in the H1v2 renders.

1. Dropout/blowout: KB11 machine bar = 0.0 fraction of kept FULLSKY
   with |dL| > 60. Eye pass on the 1024 pair (out/h1v2a/h1v2_1024.png,
   out/base1/base_1024.png): no dropout, no banding, no hard edges,
   no NaN-black regions. Finding: none. Knowledge, not architecture:
   the clamps (shade 0.05..1.35, sh 0.15..1.0, lit <= 1.2, lk 0..1,
   a <= 1.0) contain every new term.
2. Flicker: KB1 3/3 byte-identical 1024 renders exclude flicker.
   Zero RNG anywhere (pure functions of pixel coordinates). Finding: none.
3. KB10 degenerate pixels: 6 of 48 kept SKYWIN pixels excluded with
   |J*S| < 1e-6. The prereg predicted "none expected"; that prediction
   was wrong. Analytic derivation: |J*S| = 0 requires
   dx = -3.23*(dy+0.18) and dz = -4.00*(dy+0.18) simultaneously, which
   is satisfied by real normalized rays near the left frame edge, low
   in the sky band. At those rays the finite-difference transport
   magnitude collapses and the tmc = 1e-9 clamp yields an arbitrary
   march direction. The shade/sh/lining clamps bound its visual
   effect; KB11 shows no blowout and the eye pass shows no artifact at
   those locations. Finding: a genuine mechanism domain-of-validity
   limit (knowledge about the transport's degeneracy), not a substrate
   flaw. Any future revision of this mechanism family must handle the
   degenerate rays explicitly rather than rely on the clamp.
4. Weirdness: clouds read as structured lit/deck formations with warm
   sun-side tops; moon disc, terrain, and sky gradient untouched
   (KB5/KB6/KB7 pass). Acutance ratio 0.981: no grain added (E3 verdict
   honored). Finding: none.
5. Attribution summary: KB3 fail = mechanism knowledge finding (right
   anchoring, insufficient systematic half-level effect); KB9
   pairing-1 fail = measurement-environment finding (contention
   outlier) compounded by a real cost increase (+26 fbm octave-evals
   per sky pixel that the prereg prediction missed). No substrate
   defect found; KB10 confirms the implementation matches the frozen
   design to ~1e-6.

## Verdict: BUILD-FAIL

Killed by KB3-LIGHTLOGIC (diff +0.72 vs >= 6.0; sun mean +0.64 vs
>= 3.0) and KB9-COST (2.36x vs <= 2.0x on sequential pairing 1).
No blind pair prepared, no JUDGE_BRIEF.md, no SEALED_MAPPING.
This candidate is not READY-FOR-JUDGE. The renders, binaries, logs,
and verifier remain in h1v2/ as evidence.

Provenance honesty: H1v2 was a NEW candidate under a NEW frozen prereg
naming a NEW mechanism (derived anchoring). It failed two frozen bars
and is discarded on the merits, never adopted on metrics. Lineage for
the record: prior candidate wave-20261001-1721pdt H1 LIT CLOUD DECK,
status JUDGED-DISCARDED; this wave's H1v2, status BUILD-FAIL (KB3, KB9).

## Artifact inventory (all under SENSORY/h1v2/)

- r11_alien_src.zag, r11_baseline.zag, h1v2_clouds.zag (sources)
- h1v2_verify.zag (verifier source)
- bin/r11_baseline, bin/h1v2_clouds, bin/h1v2_verify, bin/bmp2png
- out/base1, out/base2 (baseline 1024 BMPs), out/smoke (baseline 256)
- out/h1v2a, out/h1v2b, out/h1v2c (variant 1024 BMPs), out/h1v2smoke
- out/h1v2a/h1v2_1024.png, out/base1/base_1024.png (viewing PNGs)
- evidence/: render logs with wall times, sha lists, validator.log,
  killbars.log
- run_h1v2.sh (pipeline script)
- tools/bmp2png.zag, tools/sub/R33_NATIVE_IO_V1.zag, sub/R33_NATIVE_IO_V1.zag
