# PREREG SA1 - measured transient channel on the imagination render path

**Status:** FROZEN. Committed alone before any implementation.
**Lane:** SENSORY-AUDIO, wave-20261002-0221pdt. **Worker:** this lane.
**Toolchain:** pure Zag only, pinned znc (`/home/hatch/safebin/znc`,
znc 2026.07.0-dev), zero RNG, zero Python, zero em/en dashes in loop docs.
**Branch:** tnn-native-lab. **Working copy:** ~/workspace/tnn-rsi.

## 1. Hypothesis

A valid measured-transient isolator (true residual from a
pitch-synchronous harmonic prediction, plus a local-contrast
impulsiveness test, plus hard anti-leakage gates) produces transient
events that, rendered as measured single-sample impulses on the de-synth
imagination path, close the measured onset-realism gap between renders
and real audio at negligible marginal cost, without static, clipping,
DC shift, or voicing break.

One sentence: the transient channel that phase 3 proved dominant in
analysis (91-94% residual shrinkage) can be made valid for imagination,
and the current renders' missing onset structure is the measurable
consequence of its absence.

## 2. Why this is a big lever (prior evidence)

- Phase-3 H1 (audio_longhorizon/phase3/VERDICT.md): the transient-event
  channel (top M deterministic impulses) shrank residual RMS 91-94% per
  class and improved semantic RMS 26-40% per class, no clip regressed.
  It is the largest measured fidelity effect in the audio line.
- It exists ONLY in the hear/re-emit path. The imagination renderer
  (desynth_render.zag) has it at ZERO: transients honestly disabled.
- Measured symptom (closure evidence/waveform_battery_final.tsv, t1):
  reference 21 onsets / 5 s vs render 1 onset / 2 s. Every imagination
  render is nearly onset-free while real audio is onset-rich.

## 3. Why this is NOT the killed path

The legacy transient table in the v2 atoms was killed (P2 #8 and the
desynth_render.zag source comment): its peaks came from the
period-synchronous residual, which does not isolate valid transients
(residual RMS exceeded the source via harmonic leakage; speech peaks
~170x harmonic RMS); rendering them broke voicing detection. SA1 does
NOT re-enable those peaks. The same source comment prescribes the
unblocking work: "Transient rendering needs a fixed residual isolator
(future work); do NOT re-enable without a separate valid extraction
mechanism." SA1 is that separate valid extraction mechanism, built new
in pure Zag: true residual (source minus pitch-synchronous harmonic
prediction), local-contrast impulsiveness test, amplitude bounded by the
source peak. The atom's stored NIMP block stays skipped; the variant
renderer reads a new sidecar event file.

## 4. No-synth law compliance

Every output sample traces to a recorded sample: harmonic stack
(measured), texture (measured), amplitude trajectory (measured),
transient impulses (measured residual values at measured positions).
Adding measured values at measured positions is a documented transform.
No oscillators, no parametric excitation, no synthetic noise, no RNG.
Interpolation is unchanged from the committed baseline renderer.

## 5. Frozen design

### 5a. sa1_isolate.zag (WAV -> event table)

1. Chunk-aware RIFF parse; require PCM16/mono/44100; i64 samples -> f64.
2. T0: autocorrelation on every 4th sample, lags 44..500, max normalized
   autocorr. NBINS = round(T0).
3. Phase-locked harmonic mean: plm[b] = mean of x[i] with i mod NBINS = b.
   Harmonic prediction h[i] = plm[i mod NBINS]. Residual r[i] = x[i]-h[i].
4. Source peak P = max |x|.
5. Candidates: i is a local maximum of |r| over +-2, and
   |r[i]| > 6.0 * local_rms(i) where local_rms is over [i-64, i+64]
   excluding [i-8, i+8], and |r[i]| >= amp_floor with
   amp_floor = max(32.0, 0.002 * P), and |r[i]| <= P (hard anti-leakage).
6. Keep top M = max(16, nr/500) by |amp|; deterministic: larger |amp|
   wins, ties broken by smaller position. Fixed-size array, no RNG.
7. Write EVT1: magic 'EVT1', u32 version=1, u64 n_source, u64 NEVT,
   then NEVT records of (i64 pos, f64 amp).
8. Print white-box stats: T0, NBINS, residual RMS, candidate count, M,
   top-10 |amp|, median contrast, max|amp|/P.

### 5b. sa1_render.zag (variant renderer)

Byte-for-byte the committed desynth_render.zag render path, plus:

- Parse the atom identically (v2; the stored NIMP block is skipped as in
  baseline: those peaks are the invalid legacy extraction).
- argv 7 = EVT1 event file. After the main render loop, before WAV
  write: for each event, op = floor(pos * 88200 / n_source); if
  0 <= op < 88200, out[op] = out[op] + amp * amp_scale. WAV write
  clamps as in baseline.
- Print NEVT applied.

### 5c. sa1_meter.zag (WAV -> metrics)

Per file: n, peak, RMS, DC (mean), clipping count (|x| >= 32760),
HF proxy H = sum((x[n]-x[n-1])^2)/sum(x[n]^2),
onset rate (10 ms RMS frames; flux = positive frame-to-frame RMS
difference; threshold = 3.0 * median positive flux; 50 ms refractory;
rate = onsets / seconds), autocorr f0 (lags 44..500, every 4th sample).
One TSV line per file. All parameters above are frozen.

### 5d. Baseline

The committed docs/lab/audio_longhorizon/desynth/src/desynth_render.zag,
unmodified, built with the pinned znc. The variant differs ONLY by the
transient channel (5b).

## 6. Frozen battery

| atom | source WAV | f0_mhz (frozen) | mode | amp_scale_pm |
|---|---|---|---|---|
| child | audio_longhorizon/corpus/child/child-fsd50k-171101.wav | 393176 | 0 flat | 1000000 |
| speech | audio_longhorizon/corpus/speech/speech-e22-000.wav | 466296 | 0 flat | 1000000 |

f0_mhz = round(44100000 / T0_atom); child T0 = 112.163570, speech
T0 = 94.575072 (read from the committed atoms with od, 2026-10-02).
n_source = 220500 for both (5.0 s). Renders are 2.0 s (88200 samples).

Runs per atom: isolator 1x (plus 2 determinism reruns); baseline render
3x; variant render 3x. SHA-256 recorded for every output.

## 7. Frozen kill bars (ALL must pass; any fail = BUILD-FAIL, no judge pair)

- B1 realism (primary): gap_base(a) = |rate(baseline_a) - rate(source_a)|,
  gap_var(a) = |rate(variant_a) - rate(source_a)| with the frozen onset
  detector. PASS iff gap_var(a) < gap_base(a) for BOTH atoms AND the mean
  gap shrinks by >= 40%. (If gap_base(a) < 0.25/s on an atom, that atom
  is vacuous-pass but then gap_var(a) <= 1.0/s is required.)
- B2 validity / anti-leakage: (i) max|event_amp| <= source_peak, both
  atoms; (ii) Pearson correlation between the event train (amp at event
  positions, 0 elsewhere) and the harmonic prediction h[i] is < 0.30,
  both atoms; (iii) at least 50% of kept events have local contrast
  >= 10.0, both atoms.
- B3 no static: H(variant) within [0.5x, 2.0x] of H(source), both atoms.
  H(baseline) and H(variant) reported as the measured delta.
- B4 no voicing break: |f0(variant) - f0_commanded| / f0_commanded
  <= 0.02, both atoms (explicit anti-regression for the legacy failure).
- B5 no clipping / DC / level blowup: zero samples with |x| >= 32760 in
  any render; |DC| <= 5.0 samples; RMS(variant) within [0.5x, 2.0x] of
  RMS(baseline), both atoms.
- B6 determinism: 3/3 byte-identical SHA-256 within each group
  (isolator outputs per atom, baseline renders per atom, variant renders
  per atom).
- B7 cost / free lunch: variant render wall time <= 1.05x baseline
  render wall time (median of 3, same machine); event file <= 16384
  bytes per atom; zero bytes added to the committed atom fixture.
  Isolator wall time reported separately (one-time per atom, amortized).
- B8 human-ear readiness gate: ONLY if B1-B7 all pass, prepare the
  sealed blind A/B (section 9). If any of B1-B7 fails: NO judge pair,
  verdict BUILD-FAIL with the killing evidence. The worker makes no
  claim about how anything sounds.

## 8. Red-team plan (knowledge vs architecture)

- R1 harmonic-leakage hypothesis: if B2(ii) fails, the events are leaked
  harmonics, not transients. Kill, publish the contrast and correlation
  distributions as the killing evidence.
- R2 old-failure signature: any event with |amp| > 10x the render
  harmonic RMS is a kill even if B2(i) passes (the ~170x signature must
  be absent, not merely bounded).
- R3 hash audit: if B3 fails, ablate with top-32 events only
  (informational; does not rescue the verdict).
- R4 dropout / weirdness: any meter anomaly (NaN, f0 = 0, onset
  explosion, DC jump) gets a knowledge-vs-architecture writeup in
  REDTEAM_ARTIFACTS.md, never silently dropped.

## 9. Sealed listening-pair protocol (B8 only)

Per atom: two files, baseline vs variant, presented as A/B in an order
fixed by sorting their SHA-256 hex (deterministic, auditable, blind).
Mapping recorded in SEALED_MAPPING.md, which the judge must not open
before judging. JUDGE_BRIEF.md carries the full provenance header
(RENDER_SHA, FIRST_RENDERED_WAVE, COMPONENT_LINEAGE with
JUDGED/QUEUED-UNJUDGED status, NEW_KNOWLEDGE_CLAIM one sentence),
artifact labels NEW, what changed, and what the meters say. No ear
claims by the worker. WAV masters stay in the lane dir; M4A per the
predelivery gate if an encoder is available, else WAV with the deviation
documented.

## 10. Queued next (not this wave)

- SA2: if B3 kills on tail hash, a sparser event cap (informational
  ablation becomes the candidate).
- SA3: onset-conditioned placement for novel targets (conditioning
  regime change), after SA1 validates the isolator.
- SA4: extend to the 4 closure atoms once their source WAVs are
  provenance-documented.
- The planner's envelope/F0 tradeoff and renderer D2 (0.59x) remain open
  walls; SA1 does not touch them.

## 11. Amendments

None. Any change to sections 5-9 after this commit invalidates the
freeze; the experiment would be re-preregistered as SA1b, never amended
in place.
