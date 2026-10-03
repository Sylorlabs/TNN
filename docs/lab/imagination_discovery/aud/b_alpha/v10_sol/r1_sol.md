### (a) Sound-production model

Use a continuously running, physically motivated mixture:

\[
y[n]=A_{\rm air}(n)+\sum_{i=1}^{4}V_i[n]+F[n]+P[n]+L[n]
\]

where all terms remain active, although their amplitudes vary smoothly.

**Air/ambience:** filtered deterministic noise, distant broadband play, and weak resonant playground reflections. Generate noise with a 32-bit hash counter, high-pass it, and pass it through several fixed biquads. Slowly varying gains represent wind and distance, but are bounded so the total never approaches silence.

**Children’s voices:** each child is a two-layer source. A voiced oscillator has continuously integrated phase,

\[
\phi[n+1]=\phi[n]+2\pi f_0[n]/44100
\]

with \(f_0\) typically 250–500 Hz, plus smooth vibrato and pitch glides. Excitation is a differentiated, rounded glottal pulse (a short polynomial pulse repeated by phase), mixed with aspiration noise. Pass this through three or four formant resonators (approximately 700, 1800, 2800, and 4000 Hz, with child-dependent bandwidths). Add irregular voiced/unvoiced balance modulation and weak subharmonic/inharmonic components for laughter. Laughter is modeled as repeated smooth pitch rises/falls and breath bursts, not samples.

**Footsteps:** each foot is a continuous damped contact oscillator:

\[
x''+2\zeta\omega x'+\omega^2x = a(t)u(t)
\]

where \(u(t)\) is a short, smooth half-sine force profile, exciting low resonances and filtered noise. Step times vary smoothly around 2–4 Hz and include running acceleration/deceleration. Impacts have no discontinuity.

**Playground mechanisms:** very low-level smooth resonances and occasional continuous squeaks/chimes, driven by slowly varying excitation rather than discrete samples.

### (b) Control structure

A deterministic scene script contains child trajectories, paths, play phases, and interaction relationships. It is evaluated every sample or control block using cubic Hermite splines. Each event is a parameter trajectory with at least 20–80 ms attack, continuous sustain, and 100–500 ms release. Use \(C^2\) bump functions such as

\[
b(t)=t^3(10-15t+6t^2),\quad 0\le t\le1
\]

for transitions. Event timing is generated from fixed-point phase accumulators and deterministic hash perturbations, never random calls. Voice activity, pitch, distance, formant shift, foot placement, and noise level all interpolate continuously. Maintain an always-present ambience floor.

### (c) Primitive DSP blocks

Implement:

- Q31 phase oscillators and sine LUT with linear interpolation;
- polynomial glottal pulse and differentiated waveforms;
- hash-based signed noise: `hash(seed, counter)` mapped to Q31;
- one-pole and biquad low/high/band-pass filters;
- state-variable resonators or biquad formants;
- second-order damped resonators for impacts;
- cubic/Hermite interpolation and \(C^2\) envelopes;
- DC blocker;
- fixed-point gain/mixer and final headroom limiter.

Use fixed-point arithmetic, specified rounding, integer coefficients, and saturating accumulators for byte-identical output. Keep mix peak below −3 dBFS; apply only a deterministic soft limiter as safety.

### (d) Why choppiness is impossible by construction

There are no buffers, atoms, sample replacement, or binary gates. Every generator owns persistent phase/filter/envelope state. All control changes are spline or \(C^2\)-smoothed trajectories, and every excitation has finite smooth rise and decay. Therefore no block boundary can introduce a waveform discontinuity or abrupt parameter jump.

### (e) Three largest realism risks

1. **Voices may sound like synthesizers:** mitigate with correlated aspiration, formant motion, pitch instability, and multiple independently controlled children.  
2. **Footsteps may sound like clicks:** use coupled contact force, surface resonances, and distance filtering rather than impulses.  
3. **Scene dynamics may feel artificial:** script plausible overlapping activities and constrain modulation rates, loudness ranges, spectral flux, crest factor, and minimum ambience using offline deterministic calibration.
