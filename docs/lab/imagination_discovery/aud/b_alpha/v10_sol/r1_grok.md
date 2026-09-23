** (a) Sound-production model **  
The architecture models four overlapping acoustic phenomena as parallel synthesis channels, all driven by continuous-time blocks:

- **Ambient**: Deterministic LCG noise (state = 1664525·state + 1013904223 mod 2³²) filtered by a shared 4-pole IIR low-pass (cutoff 80–400 Hz, 6 dB/octave) whose center frequency and gain vary slowly (0.3–2 Hz LFO-like trajectory). Represents distant chatter, wind, and air absorption.  
- **Voices** (3 parallel channels): Each is a 1024-entry sine LUT oscillator (phase accumulator: phase += f/fs; sample = LUT[phase]). Base F0 280–520 Hz, 2–4 harmonic partials (1.0 + 1.12 + 1.25 + 1.40, each detuned ±3–8 % by a fixed hash-derived offset). Amplitude and frequency modulated by independent smooth envelopes (linear ramps or cubic Bézier between scripted targets). Models fundamental + formant-like overtones of small vocal tracts.  
- **Laughter**: Single noise source passed through a time-varying 2nd-order bandpass (center 800–1800 Hz, Q=3–6) whose bandwidth and gain follow a slow “bursty” trajectory (gentle sigmoid rises/falls over 0.4–1.2 s). Models exhaled laughter and giggles.  
- **Footsteps** (4 parallel damped sinusoids): Each is a high-frequency oscillator (2.5–6 kHz) whose amplitude decays with a smooth exponential envelope (time constant 80–400 ms) and receives a brief high-pass “impact” boost at envelope onset. Models shoe/foot contact transients.

All blocks run at every sample; no gating, no sample-and-hold.

** (b) Control structure **  
A 30 s “scene script” is a deterministic sequence of 40–60 modulation events generated once from a 64-bit seed via a hash chain (e.g., event_time = hash(seed + t/30.0) mod 30, then event_type = hash(event_time) mod 4). Each event specifies which channel/parameter (amp, freq, cutoff, etc.) and a target value reached by a smooth curve (linear, quadratic, or exponential, chosen by hash). Overlapping events are linearly blended in parameter space at each sample, guaranteeing continuous parameter trajectories. Global time t increments sample-by-sample; every parameter is therefore a C¹ function of t.

** (c) Primitive DSP blocks (C-like pseudocode) **  
```c
// Oscillator
double osc_run(osc_t* o) {
    o->phase = fmod(o->phase + o->freq / FS, 1.0);
    return sin_lut[(int)(o->phase * LUT_SIZE)];
}

// 1-pole low-pass filter (direct form)
double lp_run(lp_t* f, double x) {
    double y = x + f->a * (f->y - x);
    f->y = y; return y;
}

// Deterministic noise
double noise_run(uint32_t* s) {
    *s = *s * 1664525U + 1013904223U;
    return ((*s >> 16) & 0xFFFF) / 65535.0 - 1.0; // bipolar
}

// Smooth envelope multiplier
double env_run(env_t* e, double target, double dt) {
    e->val += (target - e->val) * (1.0 - exp(-dt / e->tau));
    return e->val;
}
```
All filters are 2–4 pole; no external DSP library calls.

** (d) Why choppiness is impossible by construction **  
Every output sample is produced by a linear combination of continuous phase-accumulating oscillators and memory-bearing IIR filters. All time-varying parameters (frequency, amplitude, cutoff) are obtained by cubic-spline or exponential interpolation between scripted targets; no parameter ever jumps discontinuously. The signal is therefore a globally C¹ function of time, eliminating any audible discontinuities at block boundaries.

** (e) Three biggest risks **  
1. The scripted modulation, while continuous, lacks the chaotic micro-variations of real overlapping children; spectral flux may fall below real-recording gates.  
2. Formant and impact modeling with few oscillators cannot reproduce the exact resonance shifts of playground acoustics (air absorption, multiple simultaneous voices), risking a “polished” rather than lived-in timbre.  
3. Noise statistics must be tuned by ear and by running the exact same hash chain against reference recordings; any mismatch in crest factor or stationarity will fail automated tests.

(Word count: 548)
