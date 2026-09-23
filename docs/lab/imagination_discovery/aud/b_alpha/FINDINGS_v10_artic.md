# FINDINGS — AUDIO V10 Fork A (ARTIC)

**Approach:** ARTIC — ARTiculatory-Inspired Continuous synthesis.
Phase-integrated glottal pulse trains (250–500 Hz child F0) through 3–4
parallel formant resonators per voice; laughter produced by driving the
*same* vocal model with syllabic amplitude/rate modulation (not a separate
laugh generator). Footsteps are smooth half-sine-driven damped contact
oscillators (thump + surface pair). Air is continuous filtered hash with
weak early reflections. All control trajectories are cubic/C²
(smootherstep bumps, smooth hash wander); no atoms, no splicing, no chunk
buffers, no binary gates, zero RNG in the render path (deterministic hash
streams only).

**Scene (one consistent playground, 30 s):** yard activity (singing,
distant calls, giggles, walking) → chase (running, shouts) → trip/yelp
→ shared laughter (4 voices, hopping) → wind-down (lullabies, slow steps).

**Renderer:** `src/render_v10_artic.zag` (single file, imports tracked
`src/common.zag`; compiled with pinned znc
`toolchain/bin/znc_linux_x86_64_abed8aa1`).
**Clip:** `clips/b_alpha_kids_1e_j_v10_artic.wav` — 30 s, mono,
44.1 kHz, 16-bit, globally peak-normalized, 30 ms end fades.
**Events:** `src/events_v10_artic.txt` — scripted footstep strikes,
laugh-syllable onsets, and accent timestamps written by the renderer.

## 1. Frozen consistency gate — nine bars (all PASS, no WARN)

| id | metric | value | bar | result |
|----|--------|-------|-----|--------|
| G-PER | max env autocorr, lags 0.5–25 s | 0.292 | ≤ 0.350 | PASS |
| G-STA | std of 1 s log-RMS | 1.064 dB | ≤ 3.0 dB | PASS |
| G-LURCH | std of 50 ms log-RMS | 1.591 dB | ≤ 5.0 dB | PASS |
| G-DRIFT | std of 1 s spectral centroid | 193 Hz | ≤ 800 Hz | PASS |
| G-FLUXm | max 1 s→1 s spectral flux (×1000) | 174 | ≤ 350 | PASS |
| G-SIL1 | fraction of 50 ms windows < −60 dBFS | 0.000 | ≤ 0.02 | PASS |
| G-SIL2 | longest < −60 dBFS run | 0 s | ≤ 0.5 s | PASS |
| G-CLIP | peak sample | 0.679 | ≤ 0.95 | PASS |
| G-CREST | crest factor | 5.12 | ≤ 14 | PASS |
| W-ENDS | head/tail vs mean | 0.33 / 1.76 dB | ok | ok |
| W-DENSE | max onsets per 2 s | 0 | ok | ok |
| W-DYN | 1 s RMS range | 4.31 dB | ok | ok |

GATE verdict: **PASS** (9/9, zero WARN). For reference, real anchors:
aporee G-PER 0.261 / G-STA 1.93 dB; garry 0.104 / 0.73 dB.

## 2. CHOP results

```
CHOP-1 hard discontinuities: 0 PASS
CHOP-2 silent gaps >=150ms: NONE PASS
CHOP-3 flux spikes: 5 total, 0 unexplained
```

All 5 flux spikes coincide with scripted events (trip/yelp onset,
laugh-burst onsets, chase entries) listed in `src/events_v10_artic.txt`.

## 3. Determinism proof (byte-identical reruns)

Two independent renders of the final single-file renderer:

- run 1 SHA-256: `57df7aa4015b3cde88615d34aa96ea1ac994845e0613bb96144ac990292ccd41`
- run 2 SHA-256: `57df7aa4015b3cde88615d34aa96ea1ac994845e0613bb96144ac990292ccd41`
- `cmp run1 run2`: identical (no differences)

The merged single-file renderer was additionally verified
byte-identical against the two-file (renderer + DSP support) build.

## 4. CHOP-4 — construction argument

CHOP-4 asks whether the clip could be cut/spliced/fused material rather
than one constructed performance. Construction evidence:

1. **Single continuous render.** The WAV is written by one 30 s forward
   pass of `render_v10_artic.zag`; every sample is a closed-form function
   of the sample index plus persistent continuous state (oscillator
   phases, resonator memories, filter states). There is no sample library,
   no concatenation point, no crossfade — nothing to splice.
2. **No atoms.** Voices never start/stop; four glottal oscillators run
   for the full 30 s with continuous frequency/gain trajectories.
   Footsteps are not placed hits but a continuously integrated oscillator
   pair driven by a smooth force profile that is exactly 0 outside the
   85 ms contact window (C¹ at both ends).
3. **No binary gates.** All "events" (laugh syllables, accents, steps)
   are smooth modulations of continuous carriers. The events file records
   *detections* (phase crossings), not edit points.
4. **Envelope forensics agree.** CHOP-1 finds zero hard discontinuities;
   the 50 ms envelope spectrum shows no energy at any plausible splice
   period; G-PER (0.292) sits inside the real-anchor envelope, i.e. the
   clip's slow dynamics look like a real playground, not a loop.

## 5. Design notes (what moved the needle)

- The G-PER failure mode was **not** footstep cadence: localizing the
  lag-0.5 s autocorrelation showed it came from the *air bed following
  the scripted scene arc* (section plateaus imposed via the scene-energy
  term on wind/distant-play gains). Decoupling the air into a constant
  bed with its own slow wander dropped G-PER 0.72 → 0.47 in one step.
- The remainder was clean 7 s voice plateaus; breaking them into
  irregular 1–3 s episodic swells (per-voice smooth hash wander, distinct
  seeds/knots) plus a concerned "you okay?" call filling the post-trip
  dip brought G-PER to 0.292.
- Voice spectrum check on an isolated-voice probe: call bands
  (0.3–5.2 kHz) −1.1/−9.8/−11.4/−17.2/−22.8 dB; laugh
  −2.0/−12.9/−7.2/−13.0/−16.9 dB — formant energy present through 5 kHz,
  F0 ≈ 410 Hz (child range).

## 6. Honest listening assessment

**I did not listen to this clip.** I am a text-only agent with no audio
playback; every claim above is measurement, not audition. What the
measurements say: the clip has the spectral and dynamic signature of a
busy playground (formant-rich voices 300–5000 Hz, footstep transients,
continuous air wash, no silence, no clipping, dynamics inside the
real-anchor envelope). What they cannot say: whether the voices read as
*children* rather than small adults or synth toys; whether the laughter
is joyful or mechanical; whether the scene feels like one consistent
place or four overlaid parts. The articulatory design (child F0
250–500 Hz, 3–4 raised formants, breathy aspiration, syllabic laugh
through the same tract) is *intended* to push toward "kids," but
formant synthesis is notorious for sounding synthetic on sustained
vowels, and no metric here penalizes that. **Micah's ears are the final
gate; this clip has earned the right to reach them, not a claim of
quality.**
