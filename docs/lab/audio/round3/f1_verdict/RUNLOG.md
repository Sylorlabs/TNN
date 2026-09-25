#!/usr/bin/env python3
# F1 build log — epoch_graft (TD-PSOLA of real glottal cycles on donor clock)
# Prereg: ~/workspace/audio_round3/ROUND3_PREREG.md (frozen 2026-09-24). Section 3 = spec.

## 2026-09-24 18:15 PDT — setup
- Read ROUND3_PREREG.md in full. F1 spec = sec 3; secs 0/2/7/8 binding law.
- Verified source SHAs:
  - aud_v11/diag/vowel_real.wav = 8ba3b42708a8bab2... (matches prereg prefix 8ba3b42708a8bab2) ✓
  - v5work/kida.wav = b8ad8e1a1f4f70b0... (matches prereg prefix b8ad8e1a1f4f70b0) ✓
  - All 44.1 kHz mono 16-bit. vowel_real 2.0 s; kid* 30 s each.
- Analyzer gates read from audio_round2/shared/analyze.py (219 lines).
- Key reconnaissance:
  - vowel_real.wav alone: HNR 11.57 (FAIL box), HF -54.0 (FAIL), n_onsets 0 -> crest 0.0 (FAIL), prosody 1.35% PASS, frac_static 1.0 PASS.
  - fossil_VF1_raw.wav (fossil crew): HNR 8.01 (FAIL high), HF -39.6 (PASS), n_onsets 1 crest 6.35 (PASS) -> the render-attack onset theory confirmed: a render starting from silence triggers exactly the onset detector.
  - Donor search (prereg-spec tracker, quick prototype): NO run in kida..kide with F0 CV in [0.3%,3%]. Best = kide 0.52 s CV 7.5% @ ~484 Hz. Many runs pegged at 809 Hz detector ceiling (kids screaming). -> fallback "closest-to-anchor CV + documented gate conflict" likely; final call made by the Zag binary's deterministic rule.

## Design decisions (logged per G-prereg; all deterministic, zero RNG)
- D1 EPOCH DERIVATION: prereg pins frame-level F0 (40ms/5ms/Hann/autocorr lag[55,552]/r>=0.5/parabolic/snap) but not mark placement. Decision: marks by stepping the interpolated period contour: m_0 = first voiced frame center (integer), m_{k+1} = m_k + round(T_interp(m_k)), stop when m_{k+1} > last_center + round(T_last). Rationale: phase-consistent by construction (all grains share one arbitrary phase); "snap to sample" = round() of the refined lag. Logged as interpretation.
- D2 MAPPING: grok merged spec i(j) = clamp(round(j*(Ns-1)/(Nd-1)), 0, Ns-1). Monotonic; reuse<=2 enforced by truncating donor marks to 2*Ns when Nd > 2*Ns. Unique fraction = distinct(i)/Nd.
- D3 FOSSIL EXCERPT: vowel_real.wav longest voiced run (full ~1.97 s). >=400 ms ✓.
- D4 DONOR: deterministic rule in-binary: longest contiguous voiced run (frames) with frame-F0 CV in [0.003,0.03]; tie -> lowest file (a<b<c<d<e), lowest start frame. Fallback: min distance to the [0.003,0.03] interval; tie -> longest run, then lowest file/start. NO minimum length (letter of the rule).
- D5 RENDER SPAN: OLA coverage [d_0 - tau_{i(0)}, d_{J-1} + tau_{i(J-1)}). No margins -> the "unvoiced donor intervals" clause is vacuous by construction (donor is one contiguous voiced run); documented, not silently dropped.
- D6 GAIN: G = min(1, 10^(-1/20)/peak_norm), peak_norm = fossil-excerpt peak/32768. Computed and logged BEFORE render. (a)/(c): |y|<=G*peak<=-1dBFS by the W-division bound, no clip possible. (b): sinc overshoot measured; over-peak -> failed render -> replan with lower fixed G (one replan allowed).
- D7 VARIANTS: (a) grain = raw 2*tau_i samples x Hann, centered at d_j, OLA, /W. (b) same but grain first resampled by r=tau'_j/tau_i clamped to [0.75,1.33] via windowed-sinc (Hann-windowed sinc, half-width 8); clamp events logged. (c) butt-splice: cycle j = fossil[s_i .. s_i+min(tau_i,tau'_j]) placed at [d_j, d_j+tau'_j), zero-pad if short. No OLA, no window, no resample.
- D8 PROVENANCE: one source file (vowel_real.wav) for all variants. Per output sample: list of fossil offsets (a), grain+float-pos (b), offset or Z (c). Donor file = grid only.
- D9 F1.4 freeze: variant (a) pipeline with i(j)=i(0). D10 F1.5 LF control: Python (explicitly synthetic, control-only): LF-model pulses on donor grid, Hann-OLA like (a), same G rule from its own peak.
- D11 Parabolic clamp: |d|<=1. D12 hop = 220 samples (floor(220.5)); Hann = np.hanning formula 0.5-0.5cos(2pi n/(N-1)); Taylor cos in Zag matched to this.

## 2026-09-24 ~19:00 PDT — donor finalized (exact rule, all runs)
- Ran /tmp/proto_track.py: prereg-exact tracker (1764-sample frame, 220 hop, Hann,
  lag [55,552], normalized autocorr, r>=0.5, parabolic refine, ALL contiguous runs).
- Result: 1099 total runs across kida..kide; 363 runs with F0 CV in [0.3%, 3%].
  Longest in-box = kidb.wav frames 2573-2618 (nfr=46, 0.23 s), CV=1.2424%, fmed=493.7 Hz.
  (The earlier quick prototype missed it: it had an extra >=400 ms filter that the
  prereg rule does not contain. The prereg rule has NO minimum length. The exact
  rule therefore selects kidb 2573-2618 deterministically: longest, then lowest file.)
- Fossil: vowel_real.wav longest voiced run = frames 0-392 (393 frames, ~1.97 s),
  785 marks, mean tau 110.1 samples. Fossil excerpt peak 26213 -> G = min(1, 1.114) = 1.0.
- D10 CORRECTION (pure-Zag law): the LF negative control is implemented in Zag as a
  `control` mode of epochgraft.zag (control-only, never a candidate render). The old
  "Python" note above is superseded.
- LF CONTROL DESIGN (F1.5): triangle pulses on the donor mark grid. At each donor mark
  d_j, place p[n] = A*(1 - n/44) for n = 0..43 (A = round(fossil_peak * G), deterministic).
  Spectrum is LF-weighted (triangle ~ 1/f^2); no oscillator, no trig, no RNG. Same grid
  as the fork (timing/prosody preserved), none of the fossil's phonetic content. Expected
  outcome: HNR near the de-Krom clip (periodic pulse train, r~1) -> outside [0.7,6.7]
  and >3 dB from the real render -> gate keeps evidence status. If instead it lands in
  the box within 3 dB of real, gates lose evidence status per F1.5 (honest report).
  Control output is SYNTHETIC; its provenance file says so explicitly (G1 provenance
  applies to fork renders, not to the mandated synthetic control).

## 2026-09-24 ~19:05 PDT — epochgraft.zag complete, compiles clean (pinned toolchain)
- ~39 kB single-file Zag. Compiles with only warnings (false-positive dead-loop
  lints on the write loops; ignored-return-value notes). Binary: build_f1/epochgraft.
- Modes: `plan` (tracker + selection + mapping + gain + plan.bin/plan.txt),
  `render <a|b|c|freeze>` (variants + provenance), `control` (LF pulse train).
  `control` mode still to be written; plan binary running now (proc_ac0071ce0ca8).
- Cross-check plan: Zag plan's donor/run/marks MUST match proto_track.py
  (kidb 2573-2618, fossil 0-392/785 marks) before any render. Mismatches get
  investigated, not hand-waved.

## 2026-09-25 — plan completion, renderer fixes, audits, verdicts

### Plan (supersedes terminated slow attempts)
- Slow plan processes (proc_ac0071ce0ca8, proc_b72e76e5f9b9, proc_5b027894476e) terminated during tracker optimization.
- Optimized epochgraft.zag tracker (raw *i64 pointers, i64 autocorrelation numerators, x2^20 Hann table, pointer-cursor dot-product ~25x faster). Fossil tracking ~5s; full plan completed 2026-09-25 02:18.
- plan.bin (15,432 bytes) SHA: 1551226008b2f3ebd106926c34fd05a8ffade6ef8aa0d85313f66231f189de86
- plan.txt frozen values: fossil frames 0-392 (393 frames, 785 marks); donor kidb frames 2573-2618 (46 frames, CV 1.2424008155672617%, median F0 493.71903047640404 Hz); donor marks 113/113 used; mapping unique 1.0, max reuse 1; slice 773-87345 peak 23560; G=1.0.
- Cross-check vs exact Python prototype: kidb, 2573-2618, fossil 0-392, 785 marks all match.

### Renderer safety refactor
- render_main renders to internal i64 arena, computes peak BEFORE WAV write. If peak >= 29205 (0.891*32768), writes no WAV, returns rc 10. Optional arg 10 = one fixed gain override (x1e12).
- Provenance logs gain used and over-peak status. No output normalization/clipping on accepted renders.
- driver.sh: single lower fixed-gain retry at half plan gain on over-peak, logged to REPLAN.log.

### Variant (b) sinck blowup — diagnosed and fixed
- Symptom: b peak 18116224871 (rc 10, no WAV written). Debug showed vs ~ -6.9e9 for grain 0, m=89.
- Root cause: sinck(t) for tiny |t| (~1e-6) computed sinr(pt)/pt via Taylor cosr(pt-pi/2). The 5-term Taylor has ~3e-5 absolute error near pi/2, which dominates pt for pt<1e-4, giving s~10 instead of ~1.0.
- Fix: in sinck, for |t| <= 1e-4 use s=1.0 (limit); for 1e-12 < |t| <= 1e-4 use Taylor 1-pt^2/6. Local fix, does not affect global trig.
- After fix: b renders peak 23350, rc 0. G1b sinc spot check: 1200 spots, 0 bad, exact match.

### Duplicate G declaration removed
- render_main had `let G:f64` twice (lines 933 and 946). Removed duplicate; rebuilt binary produces byte-identical output (SHA 14c7f43f... verified).

### Audit.py fixes
- hum(): was comparing spectrum magnitude to time-domain peak (meaningless). Fixed to compare to spectral peak.
- verify_full: (a)/(freeze) now use z_hann_u16 (Taylor replication) for bit-exact match. (c) fixed x[i]->x[oi] bug and implemented last-writer-wins for overlapping grains.
- band816k(): added 1/N Parseval normalization (was reporting +29 dB impossible values).
- boundary_disc(): now reports click ratio (boundary slew / local slew, F2.3-style). G4a PASS if raw <= -40 dB OR ratio <= 4.0.
- grain_identity(): replaced flawed isolated test with true isolated region (grain 0, [1, p0_1)): byte-identical True, corr 1.0.

### Renders (all 3x byte-identical)
- f1_a.wav: 14c7f43f40b51ec8ab2f12f521798bc704314b0e2e95f9b5c4e46e037905008f, peak 22133
- f1_b.wav: 3bea9096bc24632d76319193e6eb3e68ffce137b251f57afc4a511fc5dddf630, peak 23350
- f1_c.wav: 32150962a1ea0f9fcffe7ed9211f371c74e048687260a0bcffda765aef702f36, peak 23389
- f1_freeze.wav: dfdce5d8e8ca985e824193b721f6286085009a9459fd1dff3543772fe30065d4, peak 21520
- f1_control.wav: 43ded64586e705085c675d0df32bb35607cc300df8fbeba4e57b6ecb24059fad, peak 23560

### Zero-source test
- All variants (a/b/c/freeze) render bit-exact zero from zero PCM source. PASS.

### G4 verdicts
- (a): G4a PASS (ratio 1.02x), G4b PASS (0 frames), G4c PASS (-73.46 dB), G4d PASS (grains 2*tf, not sub-period)
- (b): G4a PASS (1.02x), G4b PASS, G4c PASS (-53.93 dB), G4d PASS
- (c): G4a FAIL (ratio 30.43x, real clicks), G4b PASS, G4c FAIL (-1.27 dB), G4d FAIL (sub-period grains when dtj<tf)
- freeze: G4a PASS, G4b PASS, G4c PASS (-72.08 dB), G4d PASS

### F1 verdicts
- F1.1 (unique>=0.5, reuse<=2): (a) 1.0/1 PASS, (b) 1.0/1 PASS, (c) 1.0/1 PASS
- F1.2 (byte-identical, corr>=0.999): (a) PASS (True, 1.0), (b) N/A (resampled by design), (c) N/A (butt-splice)
- F1.3 (F0 within 3% of 493.719 Hz): (a) 491.1 Hz (0.53%) PASS, (b) 492.3 Hz (0.29%) PASS, (c) 494.4 Hz (0.14%) PASS
- F1.4 (not wavetable): freeze passes all G-bars. flux-std: freeze=0.89198, (a)=1.15644, (b)=0.65796. 
  - (a): 0.89198 >= 0.5*1.15644=0.57822 → TRUE → KILL as wavetable
  - (b): 0.89198 >= 0.5*0.65796=0.32898 → TRUE → KILL as wavetable
- F1.5 (LF control): control HNR 12.31 dB leaves HNR box [0.7,6.7] → PASS. Analyzer gates retain evidence status.

### Final verdict
- (a): Best-on-gates (passes G4 4/4, F1.1/F1.2/F1.3) but FAILS F1.4 → KILLED as wavetable.
- (b): Passes G4 4/4, F1.1/F1.3, but FAILS F1.4 → KILLED as wavetable.
- (c): Fails G4 (clicks, HF, sub-period) → KILLED. No repair possible (butt-splice design).
- Fork F1 (epoch_graft): KILLED per F1.4. The method does not produce sufficient spectral variation beyond a static wavetable.
- No variant staged for ears (per prereg, coordinator stages neutral CLIP_X; none qualified).
