# SEALED_EVAL - SA1 (measured transient channel on imagination render path)

Wave: wave-20261002-0521pdt. Lane: SENSORY (audio).
Frozen prereg: PREREG_SA1.md, committed ALONE at 5305d9195
(wave-20261002-0221pdt). Commit-order self-check: 5305d9195 is an
ancestor of db3cc7086 (wave start tip); all SA1 implementation commits
in this lane are descendants. Prereg strictly precedes implementation.
CHECK PASSED.

Toolchain: pure Zag, safebin (/home/hatch/safebin, 36 tools, no
python3), pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
Three programs built: src/sa1_isolate.zag, src/sa1_render.zag (byte-
for-byte the committed desynth_render.zag render path plus the EVT1
channel; the atom's stored NIMP block stays skipped), src/sa1_meter.zag,
plus src/sa1_check.zag (B2/R2 validity checker). Baseline renderer:
the committed docs/lab/audio_longhorizon/desynth/src/desynth_render.zag
built UNMODIFIED.

Battery (frozen section 6): atoms atom0_child.bin (f0 393176, mode 0)
and atom1_speech.bin (f0 466296, mode 0); sources
child-fsd50k-171101.wav and speech-e22-000.wav (n_source = 220500,
5.0 s, confirmed); amp_scale_pm = 1000000. Isolator 1x + 2 determinism
reruns per atom; baseline render 3x per atom; variant render 3x per
atom. SHA-256 recorded for every output. Full logs in evidence/.

## Isolator white-box output

child:  n=220500 T0=116.000000 NBINS=116 rrms=1926.414680 P=16423.000000
        candidates=0 M=441 kept=0 med_contrast=0.000000
        frac_contrast_ge10=0.000000 maxamp_over_P=0.000000
speech: n=220500 T0=362.000000 NBINS=362 rrms=3121.286193 P=20107.000000
        candidates=0 M=441 kept=0 med_contrast=0.000000
        frac_contrast_ge10=0.000000 maxamp_over_P=0.000000

Residual RMS ~= signal RMS on both atoms (child 1926.41 vs 1928.28;
speech 3121.29 vs 3125.98). The global phase-locked harmonic mean
captures essentially nothing. Diagnostic (short-time): per-1s-chunk
T0s are child {157, 59, 113, 117, 48} and speech
{448, 185, 459, 358, 353}; no global NBINS in 108..120 lowers rrms
below signal rms on either atom. The 5 s sources are too
nonstationary for one global period. The 6x local-contrast gate then
correctly finds zero impulsive events. EVT1 files are 24-byte headers
(magic EVT1, version 1, n_source 220500, NEVT 0), byte-identical
across reruns.

## Meter table (frozen section 5c detector)

label       n       peak    rms       dc        clip  H         onset_rate  f0_mhz
src_child   220500  16423   1928.281  0.014     0     0.021893  3.200000    380172
src_speech  220500  20107   3125.981  0.456     0     0.006259  5.800000    121823
base_child  88200   1850    667.407   -0.203    0     0.006671  2.500000    393750
base_speech 88200   790     145.668   -0.480    0     0.009828  4.500000    464211
var_child   88200   1850    667.407   -0.203    0     0.006671  2.500000    393750
var_speech  88200   790     145.668   -0.480    0     0.009828  4.500000    464211

Variant renders are byte-identical to baseline renders (0 events
applied; "sa1_render: events applied = 0" in all 6 variant logs).

SHA-256:
- child.evt / child_r2.evt / child_r3.evt:
  49c90f8be07a8e329397e995b2c92c75c7ab38a780809f23898dff35a0c8b445 (3/3)
- speech.evt / speech_r2.evt / speech_r3.evt:
  49c90f8be07a8e329397e995b2c92c75c7ab38a780809f23898dff35a0c8b445 (3/3)
  (identical to child: both are the same 24-byte empty header)
- base_child_1/2/3.wav:
  be7f706308177077fd90e03b83629a9045e4e45b9009ca759fb6d75b8f5d1787 (3/3)
- base_speech_1/2/3.wav:
  c0816e9f9e14cbbaefb9ac89ca58d94cd7ef5c05dec6f20840cfa17d0eec68b2 (3/3)
- var_child_1/2/3.wav: be7f706308177077fd90e03b83629a9045e4e45b9009ca759fb6d75b8f5d1787 (3/3)
- var_speech_1/2/3.wav: c0816e9f9e14cbbaefb9ac89ca58d94cd7ef5c05dec6f20840cfa17d0eec68b2 (3/3)

## Kill bars B1-B8

- B1 realism: gap_base(child) = |2.5 - 3.2| = 0.70/s;
  gap_var(child) = 0.70/s. NOT strictly less. gap_base(speech) =
  |4.5 - 5.8| = 1.30/s; gap_var(speech) = 1.30/s. NOT strictly less.
  Mean gap shrink 0% (< 40% required). Neither atom vacuous
  (0.70, 1.30 >= 0.25). FAIL.
- B2 validity: (i) vacuous PASS (NEVT = 0; nothing exceeds P).
  (ii) UNDEFINED (zero event train; Pearson undefined; cannot satisfy
  < 0.30). FAIL. (iii) 0.000000 with contrast >= 10 (< 0.50). FAIL.
  Checker output: "NEVT=0 ... B2ii: UNDEFINED (zero event train),
  B2iii: 0.000000 (< 0.50 FAIL), R2: vacuous" on both atoms.
- B3 no static: child H(var)/H(src) = 0.006671/0.021893 = 0.305
  (outside [0.5, 2.0]). FAIL. speech 0.009828/0.006259 = 1.570 PASS.
  Bar needs both atoms. FAIL. (Note: variant added zero events, so
  this is a baseline property, not an SA1 regression; reported as
  frozen, attribution in REDTEAM_SELF.md.)
- B4 no voicing break: child |393750-393176|/393176 = 0.00146 <= 0.02
  PASS. speech |464211-466296|/466296 = 0.00447 <= 0.02 PASS.
- B5: zero clip samples in all renders PASS; |DC| 0.203/0.480 <= 5.0
  PASS; RMS(var)/RMS(base) = 1.0 PASS.
- B6 determinism: 3/3 byte-identical in all 6 groups PASS.
- B7 cost: child var median 77 ms <= 1.05 x base median 103 ms PASS;
  speech var median 64 ms <= 1.05 x base median 106 ms PASS; event
  files 24 bytes <= 16384 PASS; atom fixtures read-only, unmodified
  PASS. Isolator wall (one-time, amortized): child 618 ms, speech
  1461 ms.
- B8 human-ear gate: NOT REACHED (B1, B2, B3 fail). No judge pair
  prepared. The worker makes no claim about how anything sounds.

## Verdict: BUILD-FAIL

Killed by B1 (no onset gap closure: 0 events, variant == baseline),
B2(ii) (undefined correlation), B2(iii) (0% valid), and B3 on child.
The frozen SA1 design's core assumption, that one global period
captures 5 s of speech harmonics well enough to leave an impulsive
residual, is false on both battery atoms (residual RMS ~= signal RMS;
per-chunk T0s vary 3x). This is a design-level negative, not an
implementation bug: the isolator, renderer, and meter all executed as
frozen. The informative next mechanism is short-time (chunked)
pitch tracking, which is a different mechanism (SA1b), not a patch
to SA1. Queued next per prereg section 10: SA2/SA3/SA4 remain queued;
SA1b (short-time harmonic modeling) is the honest follow-up.

No image judge pair arises from this audio lane. No ear claims made.
