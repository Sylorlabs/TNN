# UNPHONY LOOP — Round-1 falsification meter recipes (R1)

Script: `~/workspace/unphony_loop_work/meters_R1.py` (Python 3, numpy only, no RNG).
Final output: `meter_summary_R4.json` — SHA-256 `6f0c933db50336f3a9f8a56a98cb037750e9aa677b78bffdf257baff0ddb2a18`,
byte-identical across two consecutive runs (verified with `cmp`).

All clips: mono PCM16, 44100 Hz, exactly 4.0 s, in
`~/workspace/tnn-lab/bytegen/excerpts/{ar_motif,ar_motif_recur,par_motif,par_motif_recur}.wav`.

## 0. Common primitives (exact)

- `load`: PCM16 → float64 / 32768.
- `stft_mag(x, fs, win_ms=46.0, overlap=0.75)`: Hann window, N = round(0.046*fs),
  hop = round(N*0.25); returns magnitude spectra, bin freqs, frame centers (samples),
  bin width df, N, hop.
- `centroid_of(mag, freqs, fmin, fmax)`: Σ f·m / Σ m over the band; NaN if Σ m = 0.
- `f0_acf(frame, fs, fmin, fmax)`: mean-removed frame; autocorrelation via
  `rfft` zero-padded to 2n (`irfft(|RFFT|²)`); lag search in
  [fs/fmax, fs/fmin]; parabolic interpolation of the argmax lag (clamped ±1 bin);
  returns f0 = fs/lag and peak height pk = ac[lag]/ac[0].
- `fest_note` (per-note estimated f0): frame = note[t0+60 ms, t0+dur−30 ms],
  middle 4096 samples, `f0_acf` with fmin = 0.85*f0nom, fmax = 1.15*f0nom.
  (Constrained search: robust to the wideband-PM sideband cluster the renderer
  produces — 15-cent 5.5 Hz PM has modulation index 4.37 rad, smearing partial
  energy over ±4.3%.)
- `peak_amp_freq(mag, df, fc, tol=0.06, min_db=6)`: argmax in [fc(1−tol), fc(1+tol)],
  parabolic interpolation; rejected unless peak ≥ 6 dB above local median.

## 1. Note segmentation

- **PAR**: plan-anchored. 8 notes, t0 = 0.5 + 0.4k s, dur = 0.35 s,
  f0nom = [440.00, 554.37, 659.25, 554.37, 440.00, 369.99, 329.63, 440.00] Hz
  (from `tnn-lab/bytegen/fixture/plan_v1.txt`; excerpt = render[1.5, 5.5] s).
- **AR**: onset detector. 10 ms frames, log-energy flux
  `max(0, diff(10*log10(E+1e-12)))`; threshold = median + 6*MAD; local-maximum
  picking with 200 ms minimum separation. Note = [onset, min(next_onset−5 ms, +450 ms)];
  per-note f0 = median of `f0_acf` (pk > 0.4, 60–1200 Hz) over 2048-sample frames
  stepped 512, ≥3 valid frames, then one constrained re-estimate.

## 2. H2 — attack/sustain regime split

Per note:
- **Centroid drop**: mean centroid over frames in A = [t0, t0+30 ms] minus mean
  over B = [t0+120 ms, min(t0+400 ms, t0+dur)]. PRIMARY: high band 1000–12000 Hz
  (rejects the always-on 110 Hz bed that dominates the full-band 0–30 ms window).
  SECONDARY: full band 0–12000 Hz (reported; bed-confounded, see results).
- **Inharmonicity B**: per window (A, B), mean magnitude spectrum; for harmonics
  n = 1..8 with n*fest ≤ 11000 Hz, `peak_amp_freq` (tol 6%); least-squares fit of
  `(f_n/n)² = f0²(1 + B n²)` i.e. regress y=(f_n/n)² on [1, n²]; B = slope/intercept;
  needs ≥3 found partials else NaN. Report median B_attack, B_sustain.
- Kill/confirm per `native_hyp_A.txt` §H2: predicted real anchor drop ≥ +800 Hz;
  render prediction: drop ≈ 0 (no transient regime) and B_attack ≈ B_sustain ≈ 0.

## 3. H1 — partial-envelope correlation

Per note, per harmonic n = 1..max_harm (PAR: 6 = plan timbre; AR: 8):
- Cluster energy: Σ mag² over [0.94, 1.06]×n×fest per STFT frame
  (integrates the PM sideband cluster; fixed-bin/peak tracking was shown to
  measure off-peak amplitudes on this material).
- Bed subtraction (PAR only): subtract Σ G over the same bins, where G = mean
  power spectrum of the 7 inter-note gap spectra (bed-only), scaled by (N/gap_len)².
- Floor at 1% of the track's positive median before 10·log10 (late-release
  near-zero would otherwise collapse to −150 dB spikes and dominate r).
- Keep partials with median cluster energy ≥ 10 dB above the local bed floor.
- Smooth with 300 ms boxcar (macro envelope; rejects the 5.5 Hz PM micro-dance
  that decorrelates 100 ms tracks — verified: synthetic exact-model render scores
  0.996 with this meter).
- Region [t0, t0+dur]; Pearson r over all kept-partial pairs; r_bar = mean.
- Report median/min/max r_bar over notes.
- Calibration: float synthetic of the exact renderer model (shared raised-cosine
  env, shared 15c/5.5 Hz PM, 1/h stack, 110 Hz bed) scores r_bar = 0.996.

## 4. H3 — room probes

- **End tail**: after last note end + 50 ms, RMS in 50 ms blocks (dBFS);
  floor = median of last 4 blocks; time-to-floor = first block ≤ floor+3 dB.
- **Inter-note gaps** (PAR): RMS dBFS of each [note_end, next_note_start]
  (room would accumulate across notes).
- **Cepstrum**: per note, first 200 ms, Hann, log|rfft|, `irfft` → real cepstrum;
  band 5–40 ms vs reference 45–120 ms (median + MAD); EXCLUDE all pitch rahmonics:
  for f in {fest, 110 Hz}, all k with quefrency 1000k/f ≤ 45 ms, ±25% bands
  (v2 excluded only k≤6 and faked 8/8 detections from pitch rahmonics at k=7..17);
  detection = peak > median + 6·MAD. Report detection count and quefrencies.
- Result on these clips: the 5–40 ms band is fully tiled by note+bed rahmonics
  (PAR: 0 usable windows) → cepstral arm INCONCLUSIVE by masking, not by absence.

## 5. H4 — recurrence

- PAR: plan-anchored 8 notes in motif vs recur; per-note features = RMS over
  [t0+10 ms, t0+80 ms] and mean full-band centroid over the same span;
  CV(a,b) = |a−b|/(√2·mean); report mean/max CV over the 8 pairs + bit-identity.
- AR: detector notes; whole-waveform Pearson r motif vs recur; first-N paired
  CV with the same features (approximate pairing — detector counts differ).

## 6. H6 — sustained-note / vibrato probe

- Repertoire: max note dur; count ≥ 600 ms. (All clips: none → INAPPLICABLE.)
- Bonus (attempted): Hilbert instantaneous-frequency demodulation of the
  fundamental cluster — ruled INCONCLUSIVE on these clips (notes ≤ 445 ms,
  bed beating, wideband PM). Vibrato presence instead confirmed by source
  inspection: `parse_plan` stores vibhz/vibc with vbeta≠0, vinc≠0;
  `voice_q16` applies `ph += (vbeta·vs)/32768` (15-cent 5.5 Hz PM per plan).

## 7. HNR (auxiliary)

- (a) Wide-sieve on note regions: 8192-sample Hann frames, ±5% bands around
  n×fest (captures PM sidebands), 10·log10(E_harm/(E_tot−E_harm)) to 12 kHz.
- (b) Autocorrelation periodicity: gated frames (RMS ≥ −40 dBFS), `f0_acf`
  50–1200 Hz, keep 0.30 ≤ pk < 1, HNR = 10·log10(pk/(1−pk)) (PM-robust).
- Report median/p10/p90.

## 8. Determinism

numpy only, no RNG, no wall-clock, no dict-ordering dependence. Two consecutive
full runs → byte-identical `meter_summary_R4.json` (verified `cmp` 2026-09-24).

## 9. Known confounds (do not "fix" by tuning)

- The 110 Hz bed drone is mixed under everything (−16.8 dBFS floor); it biases
  full-band attack centroids, low-partial tracks, and narrow HNR sieves.
- The renderer's 15-cent 5.5 Hz PM is modulation index 4.37 rad (wideband):
  partials are sideband clusters ±4.3%, not lines. Narrowband estimators
  under-read on this material.
- Measured fundamentals read sharp of plan by tens of cents (estimator-dependent:
  peak-pick ≈ +68c, autocorr ≈ +55c, phase-fit ≈ +48c on the 440 Hz note; the bed
  is in tune at 110.01 Hz). Not root-caused; reported as an open side finding.
