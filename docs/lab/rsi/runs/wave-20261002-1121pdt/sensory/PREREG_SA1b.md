# PREREG SA1b - short-time adaptive harmonic rejection (STAHR)

**Status:** FROZEN. Committed alone before any SA1b implementation.
**Lane:** SENSORY-AUDIO, wave-20261002-1121pdt. **Worker:** this lane.
**Toolchain:** pure Zag only, pinned znc (`/home/hatch/safebin/znc`),
zero RNG, zero Python, no em/en dashes in loop docs.
**Branch:** lane-sensory-20261002-1121pdt. **Working copy:**
~/workspace/tnn-rsi-work/wave-20261002-1121pdt/sensory/.
**Lane dir:** docs/lab/rsi/runs/wave-20261002-1121pdt/sensory/.

## 1. Hypothesis

SA1 failed because its harmonic model assumed one global pitch period
for 5 s of speech (BUILD-FAIL: REDTEAM_SA1.md; harmonic prediction
washed out, residual = signal, NEVT = 0). Speech is non-stationary:
per-chunk T0s on the speech source measured (448, 185, 459, 358, 353).

SA1b replaces the global model with SHORT-TIME ADAPTIVE HARMONIC
REJECTION (STAHR): the signal is partitioned into quasi-stationary
frames; each frame gets its own pitch estimate and its own
phase-locked harmonic prediction; the residual is frame-local. This
is a DIFFERENT mechanism from SA1 (the red team prescribed it as such:
"per-chunk T0, overlap blend, or pitch-tracked phase lock"), not a
parameter change: it changes what the isolator computes (frame-local
harmonic models vs one global), the event semantics (frame-adaptive
floors), and the cost model (per-frame autocorr).

One sentence: speech transients can be isolated by rejecting harmonics
frame-locally, because a pitch period is only valid inside a short
quasi-stationary window.

## 2. Why this is a new mechanism, not a re-tune

SA1: one T0 for the whole file, one phase-locked mean, one global
contrast floor. SA1b: per-frame T0_f, per-frame phase-locked mean
plm_f, per-frame amplitude floor amp_floor_f, and overlap handling by
nearest-frame-center assignment. No SA1 frozen constant changes value;
the global stationarity ASSUMPTION is removed. The mechanism is named
for what it does about the failure (adaptation to non-stationarity),
not for a knob value.

## 3. No-synth law compliance (inherited from SA1, unchanged)

Every output sample traces to a recorded sample: harmonic stacks
(measured), texture (measured), amplitude trajectory (measured),
transient impulses (measured residual values at measured positions).
Adding measured values at measured positions is a documented transform.
No oscillators, no parametric excitation, no synthetic noise, no RNG.
Interpolation unchanged from the committed baseline renderer.

## 4. Frozen design

### 4a. sa1b_isolate.zag (WAV -> EVT1)

1. Chunk-aware RIFF parse; require PCM16/mono/44100; i64 samples ->
   f64 via the 2-byte getter (pinned-znc rule).
2. Frame partition (frozen): FW = 11025 samples (0.25 s), OV = 2205
   (0.05 s), HOP = 8820. Frame f covers
   [f*8820, min(f*8820 + 11025, n)).
3. Per frame f: T0_f by autocorrelation on frame samples, every 4th
   sample, lags 44..500, i >= fstart + 500 (the SA1 procedure, applied
   per frame). NBINS_f = best lag, or 0 if no lag qualifies.
   If NBINS_f == 0 the frame's harmonic prediction is 0 everywhere
   (unvoiced/silence fallback; residual = signal, honest).
4. Phase-locked harmonic mean per frame: plm_f[b] = mean of x[j] with
   (j - fstart) mod NBINS_f == b, j in the frame.
5. Prediction assignment: sample j gets the prediction of the frame
   containing j; inside an overlap region between frame f and f+1
   ([(f+1)*8820, f*8820 + 11025)) the sample is assigned to the frame
   whose center (fstart + 5512) is nearer (ties: smaller f). This is
   the frozen overlap handling: nearest-center assignment, no
   incoherent waveform mixing.
6. Residual r[j] = x[j] - h[j]. Prefix sums of r^2 (as SA1).
7. Per-frame peak P_f = max |x| in the frame; global peak P.
   Frame-adaptive floor: amp_floor_f = max(32.0, 0.002 * P_f).
8. Candidates: j is a local maximum of |r| over +-2, and
   |r[j]| > 6.0 * local_rms(j) (window [j-64, j+64] excluding
   [j-8, j+8]), and |r[j]| >= amp_floor_f(j), and |r[j]| <= P
   (hard anti-leakage against the GLOBAL peak, same as SA1's
   B2(i)), and j is not within +-2 of an overlap switch point
   (midpoint of an overlap region; conservative against
   switch artifacts).
9. Keep top M = max(16, n/500) by |amp|, ties by smaller position.
   Deterministic, fixed-size arrays, no RNG.
10. Write EVT1 (format identical to SA1: magic 'EVT1', u32 version=1,
    u64 n_source, u64 NEVT, then NEVT records of (i64 pos, f64 amp)).
11. Print white-box stats: n, frame count, per-frame T0_f list,
    defined-T0 fraction, P, residual RMS, candidates, M, kept,
    median contrast, frac contrast>=10, max|amp|/P.

### 4b. sa1b_check.zag (validity, WAV + EVT1 -> bars)

Rebuilds the SHORT-TIME harmonic prediction h (sections 2-5 above,
verbatim) and reports: NEVT; KB0 stats (defined-T0 fraction,
max/min defined T0_f on speech); KB2(i) max|amp| vs P; KB2(ii)
Pearson correlation between the event train (amp at event positions,
0 elsewhere) and the short-time h; KB2(iii) fraction of kept events
with local contrast >= 10 (frame-local residual windows);
R2 max|amp| / hrms_shorttime (RMS of the short-time h over all n).

### 4c. sa1b_render.zag (variant renderer)

Byte-identical copy of the SA1 sa1_render.zag render path plus the
measured transient channel (argv 7 = EVT1 sidecar; op =
floor(pos * 88200 / n_source); out[op] += amp * amp_scale; WAV write
clamps as in baseline). The atom's stored NIMP block stays SKIPPED.
Machine-checked diff vs sa1_render.zag: binary name in prints only.

### 4d. sa1b_meter.zag (frozen metric)

Byte-identical copy of the SA1 sa1_meter.zag (onset detector, HF
proxy, f0, clip/DC/RMS). The meter is measurement, not mechanism.

### 4e. Baseline

The committed docs/lab/audio_longhorizon/desynth/src/desynth_render.zag,
unmodified, built with the pinned znc (desynth_render_base). The
variant differs ONLY by the transient channel (4c).

## 5. Frozen battery

| atom | source WAV | f0_mhz (frozen) | mode | amp_scale_pm |
|---|---|---|---|---|
| child | audio_longhorizon/corpus/child/child-fsd50k-171101.wav | 393176 | 0 flat | 1000000 |
| speech | audio_longhorizon/corpus/speech/speech-e22-000.wav | 466296 | 0 flat | 1000000 |

f0_mhz and n_source = 220500 inherited from the SA1 prereg (frozen).
Runs per atom: isolator 1x (plus 2 determinism reruns); baseline
render 3x; variant render 3x. SHA-256 recorded for every output.

## 6. Frozen kill bars (ALL must pass; any fail = BUILD-FAIL)

- KB0-ADAPT (mechanism-specific): (a) on BOTH atoms, >= 50% of frames
  have defined T0_f; (b) on SPEECH, max(T0_f)/min(T0_f) over defined
  frames > 1.15: the mechanism must demonstrate it tracked pitch
  drift, otherwise it degenerated to SA1's global model.
- KB1 realism (primary): gap_base(a) = |rate(baseline_a) -
  rate(source_a)|, gap_var(a) = |rate(variant_a) - rate(source_a)|
  with the frozen onset detector. PASS iff gap_var(a) < gap_base(a)
  for BOTH atoms AND the mean gap shrinks by >= 40%. AND NEVT >= 16
  on both atoms (the mechanism must fire; SA1's 0 is not repeated).
  (If gap_base(a) < 0.25/s on an atom, that atom is vacuous-pass but
  then gap_var(a) <= 1.0/s is required.)
- KB2 validity / anti-leakage: (i) max|event_amp| <= source peak P,
  both atoms; (ii) Pearson correlation between the event train and
  the SHORT-TIME harmonic prediction h is < 0.30, both atoms;
  (iii) at least 50% of kept events have local contrast >= 10.0,
  both atoms.
- KB3 no static: H(variant) within [0.5x, 2.0x] of H(source), both
  atoms. H(baseline) and H(variant) reported as the measured delta.
- KB4 no voicing break: |f0(variant) - f0_commanded| / f0_commanded
  <= 0.02, both atoms.
- KB5 no clipping / DC / level blowup: zero samples with |x| >= 32760
  in any render; |DC| <= 5.0 samples; RMS(variant) within [0.5x, 2.0x]
  of RMS(baseline), both atoms.
- KB6 determinism: 3/3 byte-identical SHA-256 within each group
  (isolator outputs per atom, baseline renders per atom, variant
  renders per atom).
- KB7 cost / free lunch: variant render wall time <= 1.05x baseline
  render wall time (median of 3, same machine); event file <= 16384
  bytes per atom; isolator wall time <= 300 s per atom; zero bytes
  added to the committed atom fixture.
- KB8 human-ear readiness gate: ONLY if KB0-KB7 all pass, prepare the
  sealed blind A/B (section 8). If any of KB0-KB7 fails: NO judge
  pair, verdict BUILD-FAIL with the killing evidence. The worker
  makes no claim about how anything sounds.

## 7. Red-team plan (knowledge vs architecture)

- R1 harmonic-leakage hypothesis: if KB2(ii) fails, the events are
  leaked harmonics, not transients. Kill; publish the contrast and
  correlation distributions as the killing evidence.
- R2 old-failure signature: any event with |amp| > 10x the
  short-time harmonic RMS is a kill even if KB2(i) passes (the ~170x
  signature must be absent, not merely bounded).
- R3 hash ablation: if KB3 fails, ablate with top-32 events only
  (informational; does not rescue the verdict).
- R4 dropout / weirdness: any meter anomaly (NaN, f0 = 0, onset
  explosion, DC jump) gets a knowledge-vs-architecture writeup, never
  silently dropped. NEW check: event positions vs overlap switch
  points; clustering at switch points is an architecture artifact
  and kills.
- R5 mechanism-degeneracy: if KB0(b) fails on speech, verdict is
  "re-tune, not a new mechanism": the frame adaptation did not
  engage, and SA1b is not promoted even if KB1 passes.

## 8. Sealed listening-pair protocol (KB8 only)

Per atom: two files, baseline vs variant, presented as A/B in an
order fixed by sorting their SHA-256 hex (deterministic, auditable,
blind). Mapping recorded in SEALED_MAPPING.md, which the judge must
not open before judging. JUDGE_BRIEF.md carries the full provenance
header (RENDER_SHA, FIRST_RENDERED_WAVE, COMPONENT_LINEAGE with
JUDGED/QUEUED-UNJUDGED status, NEW_KNOWLEDGE_CLAIM one sentence),
artifact labels NEW, what changed, and what the meters say. No ear
claims by the worker. WAV masters stay in the lane dir; M4A per the
predelivery gate if an encoder is available, else WAV with the
deviation documented.

## 9. Queued next (not this wave)

- If KB3 kills on tail hash: SA2 (sparser event cap) from the frozen
  top-32 ablation as the candidate.
- If KB0-KB2 pass but KB1 fails: the transient channel is valid but
  does not close the onset gap; SA3 (onset-conditioned placement)
  becomes the next mechanism question.
- The planner's envelope/F0 tradeoff and renderer D2 (0.59x) remain
  open walls; SA1b does not touch them.

## 10. Amendments

None. Any change to sections 4-8 after this commit invalidates the
freeze; the experiment would be re-preregistered, never amended in
place.
