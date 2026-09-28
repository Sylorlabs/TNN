# SOL_IDEAS_V11 — Sol inspiration round for V11 synthesis forks

**Date:** 2026-09-23 (session continued past midnight UTC; local PDT still 23rd)
**Coordinator:** audio V11 Crew B
**Work dir:** `~/workspace/aud_v11/sol/` (prompts + raw replies + error logs)
**Context:** V10 built ARTIC (glottal pulses → formant resonators), PARADD
(additive voices), SPECSTAT (band-energy noise resynthesis). All passed 9/9
technical bars with zero choppiness. Micah's ears: none sound like little
children; the two finalists sound similar. Machinery converged on the wrong
target. This round asks Sol models for DIVERGENT paradigms — not variations
on formant synthesis.

## Provider availability (all 5 models attempted)

| Model | Result |
|---|---|
| step-3.7-flash:free | **ANSWERED** (6.8 KB) — physical waveguide vocal tract |
| swe-1-6-slow:free | **ANSWERED** (4.7 KB) — phonation-state waveshaping |
| gpt-5.6-sol | FAILED ×4 — provider returns `choices: null`, 0 completion tokens (same failure mode as V10 round 2; backend generating nothing, not a prompt problem; verified via raw-response dump) |
| grok-4.6 | FAILED ×4 — two socket-read timeouts at 120 s, one timeout with `max_tokens=2500`, one HTTP 524 gateway timeout at 300 s (upstream provider down/overloaded) |
| glm-5.3-flash-search:free | FAILED ×2 — HTTP 503 Service Unavailable (matches V10's 403s on this model) |

Two strong, genuinely different paradigms were obtained. A third architecture
(the data-anchored parametric-atom design assigned to glm) is sketched by the
coordinator in §4 as an analyst-derived fallback, clearly marked as such —
fork builders should know it is NOT Sol-sourced.

---

## Diagnosis consensus: why ARTIC did not sound like children

Both responding models independently converge on the same ranked errors:

1. **Adult-sized formant positions (the dominant error — perceived speaker
   size).** ARTIC's ~700/1800/2800/4000 Hz resonator set matches an adult
   male 17 cm tract. A 4–7-year-old 8–10.5 cm tract puts /a/-vowel formants
   at roughly **F1 800–1100, F2 2200–3000, F3 3500–4500, F4 5500–7000 Hz**
   (about 1.6–2× adult-male values). ARTIC got F0 right (~410 Hz measured,
   child range) but the resonator body reads as a small adult, not a child.
   Speaker-size perception is driven by formant positions, so this alone
   plausibly explains "doesn't sound like children."
2. **Formant bandwidths too narrow.** Child tract walls are softer and the
   tract shorter → higher damping → **1.5–2× wider bandwidths**
   (B1 150–250, B2 250–400, B3 350–500, B4 500–700 Hz) than adult
   (50–150 Hz). Narrow adult Q-factors make unnaturally sharp, peaky
   resonances.
3. **Glottal source too adult: spectral tilt too steep, HNR too high.**
   Adult LF-model pulses roll off at −12 dB/octave with modal HNR >15–20 dB.
   Child vocal folds (6–8 mm long, ~3× lighter) give incomplete closure →
   flatter tilt **−6 to −9 dB/octave** and lower modal HNR **8–12 dB**,
   breathy speech/giggles 0–5 dB. ARTIC sounded too buzzy and clean.
4. **Missing high formants and radiation.** Children have audible formants
   F5/F6 up to 8–10 kHz (the bright child timbre); ARTIC's 4-formant
   ceiling at 4 kHz plus no lip-radiation high-pass (~6 dB/octave) darkened
   the spectrum.
5. **Excessive pitch stability.** Deterministic pulse trains lack child
   motor immaturity: real child jitter (cycle-to-cycle F0 variation) >1.5%
   vs adult <1.0%, plus shimmer. Without micro-instability the voice reads
   robotic/adult.
6. **Laughter underspecified.** Syllabic AM of the vocal model was the right
   instinct, but real giggles need abductory (fold-separating) damping
   pulses and breath-burst coupling, not just amplitude modulation.

Note: this diagnosis implies V10's 9-bar suite measured the wrong things —
all bars passed while perceived speaker size was off by ~1.8×. Any V11
verification battery must include formant/HNR/jitter checks (§5), not just
dynamics/flux gates.

---

## Paradigm 1 — CS-DWGVT: child-scale digital-waveguide vocal tract
### (step-3.7-flash:free)

**Core idea:** replace source/filter separation with one physical system —
a 1D digital waveguide mesh vocal tract coupled to a child two-mass vocal
fold oscillator, so child-likeness falls out of *anatomy* (9 cm tract, light
folds) rather than hand-tuned formant numbers. Source-filter coupling
(tract back-pressure modulating the folds) produces natural HNR/F0 variation
during shouting/giggles for free.

**Source model:**
- Two-mass vocal fold driver, child tissue parameters:
  lower mass m1 = 0.02 g, upper mass m2 = 0.01 g;
  stiffness k1 = 2 N/m, k2 = 4 N/m, coupling kc = 1 N/m;
  damping d1 = 0.005 Ns/m, d2 = 0.003 Ns/m;
  subglottal pressure 0.5–2 kPa (Q15 fixed-point).
- 2-section subglottal waveguide (1.4 cm total) filters glottal noise.
- Driver outputs glottal area → directly modulates airflow into tract
  section 1 (no separate source/filter split).
- Breathy noise: 12-bit deterministic LFSR (fixed polynomial, seeded once
  at boot — NOT runtime RNG), scaled by glottal leakage area, shaped by the
  subglottal waveguide (high-pass character) to hit child HNR ranges.

**Tract model:**
- Digital waveguide mesh, 13 sections, Δx = 0.714 cm, Δt = 21 µs at
  48 kHz → 9 cm total tract (average 5-year-old).
- Per-section cross-sectional areas from precomputed LUTs of 5 playground
  vowel area functions scaled to child anatomy:
  /a/ max 10 cm², /i/ min 0.5 cm², /u/ 2 cm², /e/ 3 cm², /o/ 4 cm².
- Distributed series resistance R = 0.1 (Q15 Pa·s/m³) and shunt
  conductance G = 0.01 (Q15 S) model child tissue damping → 1.5–2× wider
  formant bandwidths emerge automatically.
- 1-zero FIR high-pass at output models child lip radiation.
- Result for mid vowels: F1 ≈ 950 Hz, F4 ≈ 6000 Hz, F0 220–450 Hz.

**What makes it childlike:** the tract length and propagation physics fix
formant scaling and bandwidths structurally (no adult numbers to mis-tune);
light low-mass folds give larger natural pitch excursions and unstable
harmonic structure; coupled physics gives natural F0/HNR co-variation
under effort (shouts vs whispers) that a decoupled source/filter cannot.

**Laughter:** modulate subglottal pressure with 4 Hz AM (syllable rate) +
12 Hz FM on fold stiffness (pitch wobble); 10 ms abductory damping pulses
create "ha" glottal bursts; +3 dB LFSR noise during open phases for the
breathy giggle quality.

**Footsteps:** repurpose the same waveguide core as a 20-section mechanical
impact model (Δx = 0.75 cm, 15 cm total — child rubber sole + soft ground).
Each step: deterministic 1 ms impulse scaled to a child's ~20 kg, low-passed
at 200 Hz for sole compliance; waveguide yields 80–250 Hz resonant modes =
the light, high-pitched thud of child footsteps. Step timing jitter from a
17-bit LFSR, CV ≈ 0.3.

**Build notes (fixed-point):** all Q15; tract updates are multiply-adds of
neighboring junction pressures — no transcendental functions; area-function
LUTs frozen at build time. Deterministic: LFSR seeded once.

---

## Paradigm 2 — Phonation-state waveshaping machine
### (swe-1-6-slow:free)

**Core idea:** abandon source→filter. Treat voice as a sequence of
physiological *gestures* (effort, tension, airflow) driving a time-varying
nonlinear waveshaper. Child-likeness comes from micro-prosody and phonation
instability, not from getting the spectrum's shape exactly right.

**Source model:**
- Carrier: fixed-point phase accumulator → naive sawtooth.
- **Glottal Shaper:** 256-entry LUT implementing y = f(x), a nonlinear
  transfer function set by the current phonation state:
  *Pressed* = hard-clip knee (rich harmonics, shouts/onsets),
  *Modal* = soft-clip (steady voice),
  *Breathy* = sigmoid (rounded, air leak).
- Jitter engine: LFSR noise added to the phase increment, 2–4% of period
  (targets >1.5% relative jitter).
- Effort dynamics: the waveshaper LUT index is modulated by a vocal-effort
  signal — high effort sharpens knees, low effort rounds them.

**Tract model:** only 3 parallel 2nd-order biquads (F1, F2, F3) with WIDE
bandwidths (Q = 2–3), F1/F2 slowly drifted by a 0.5 Hz LFO to simulate tract
movement. Aspiration: LFSR-driven bandpass noise, mixed by state.

**State machine (the "child" logic):** an event sequencer steps through
utterance gestures; each state carries duration, pitch target, effort,
tension:

| State   | Duration   | Dynamics                    | Shaper curve   | Child feature          |
|---------|------------|-----------------------------|----------------|------------------------|
| Inhale  | 50–100 ms  | noise ramp                  | null (pass noise) | audible breath intake |
| Attack  | 20–50 ms   | pitch +20% overshoot        | Pressed        | abrupt energetic onset |
| Sustain | variable   | 5–7 Hz vibrato + jitter     | Modal          | wobbly unsteady tone   |
| Release | 40–80 ms   | pitch drop −10%             | Breathy        | air leak before silence|

**What makes it childlike:** the phonation-mode switching IS the child
model — children live at the boundaries of modal/breathy/pressed; attacks
overshoot pitch by ~20% and releases leak air before going silent; audible
inhales; sustained tones wobble. No stable "vowel organ" anywhere.

**Laughter:** rapid Attack→Release state looping at 4–8 Hz, aspiration
noise triggered on every Release.

**Footsteps:** separate percussive engine — Karplus-Strong delay line tuned
60–80 Hz (low, for body) + filtered noise burst (contact). No melodic
content.

**Build notes:** the LUT, biquads, and state machine are all fixed-point
friendly; determinism via seeded LFSRs; the state machine is a small
table-driven loop, easy to unit-test per utterance type.

---

## §4. Paradigm 3 — data-anchored parametric atom inventory
### (COORDINATOR-DERIVED FALLBACK — NOT Sol-sourced; included because glm,
gpt-5.6-sol, and grok-4.6 all failed to answer)

**Core idea:** learn child-likeness from real child recordings by analysis,
but store *parameters, not audio*. A self-grown inventory of syllable-scale
vocal atoms (giggle-syllables, chant fragments, shriek onsets, call
contours) encoded as time-aligned parameter trajectories, recombined with
continuous coarticulation smoothing and resynthesized through a child-scale
tract.

**Inventory design:** record/obtain real child playground audio (ages 4–7).
Analysis pass (offline): pitch track (YIN), formant track (LPC order 12–14,
5 ms hop), HNR envelope, energy envelope, spectral tilt per frame. Segment
into atoms at syllable-ish boundaries (energy-dip + pitch-reset detection).
Each atom = a parameter bundle: F0 trajectory, F1–F4 trajectories +
bandwidths, HNR trajectory, RMS envelope, tilt, duration, utterance-type
tag (chant/shout/giggle-syllable/call/whimper). Store ~200–500 atoms; this
is a text/number file, not audio.

**Recombination:** a scene script selects atoms by utterance type and
concatenates parameter trajectories with 50–150 ms coarticulation
crossfades (smoothstep on F0/formant tracks; overlap-add on envelopes).
Prosody is composed from REAL child prosody shapes, not hand-drawn curves.

**Resynthesis:** parameter trajectories drive either (a) a child-scale
waveguide tract (§1-style) or (b) a time-varying all-pole LPC filter from
the stored formants + an LF-model glottal pulse with child tilt (−8 dB/oct)
+ breathy noise at the stored HNR. Because the parameters come from real
children, formant scaling, bandwidths, jitter, and prosody are correct by
construction.

**What makes it childlike:** nothing is invented — pitch excursions, giggle
rhythms, shriek onsets, breathiness are measured from real kids. The
"understanding" is in the atom taxonomy and the scene grammar; the
"synthesis" is parametric recombination, so no recorded audio ever plays.

**Laughter/footsteps:** laughter atoms (giggle syllables) are the highest-
value inventory entries; footsteps remain physically modeled (§1 or §2
engines) since they are not vocal.

**Build notes:** analysis is offline (any language); the renderer only reads
the atom parameter file. Deterministic atom selection via hashed scene
script. This is the most buildable path to guaranteed child-scale acoustics,
at the cost of needing real child recordings for the analysis pass — the
one input the other two paradigms avoid.

---

## §5. Objective child-likeness measurement battery (agreed by both models)

All measurable with fixed-point DSP, no human oracle, reference values for
ages 4–7:

| # | Quantity | Method | Child target (4–7y) | Adult-male contrast |
|---|----------|--------|---------------------|---------------------|
| M1 | Mean F0, speech/singing | YIN | 250–350 Hz (5y: 300±20) | ~120 Hz |
| M2 | Peak F0, shouts | YIN on shout segments | 400–500 Hz | ~250 Hz |
| M3 | F0 variability | std of F0 over 30 s speech | ≥ 30 Hz (2× adult) | ~15 Hz |
| M4 | Formant positions | 12th-order LPC on /a/ vowels | F1 800–1100, F2 2200–3000, F3 3500–4500, F4 5500–7000 Hz | ~500/1500/2500/3500 |
| M5 | Formant bandwidths | LPC 3 dB bandwidths | B1 150–250, B2 250–400, B3 350–500, B4 500–700 Hz | 50–150 Hz |
| M6 | HNR, modal phonation | inter-harmonic noise energy on sustained vowels | 8–12 dB (5y: 10±2) | 15–20 dB |
| M7 | HNR, breathy/giggle | same, giggle segments | 0–5 dB | n/a |
| M8 | Glottal spectral tilt | linear fit 100 Hz–4 kHz of inverse-filtered glottal flow | −7 to −9 dB/oct (5y: −8±1) | −11 to −13 |
| M9 | Jitter (RAP) | cycle-to-cycle F0 perturbation | > 1.5% | < 1.0% |
| M10 | Radiated spectral centroid | 0–8 kHz FFT, speech segments | 2500–3500 Hz (5y: 3000±200) | ~2000 Hz |
| M11 | Utterance duration stats | VAD-based | mean 0.8–1.5 s, CV ≥ 0.4 (5y: mean 1.1 s, CV 0.42) | CV ~0.2 |
| M12 | Giggle syllable stats | onset detection | 150–250 ms/syllable, CV ≥ 0.3 | n/a |

Kill-bar proposal for V11 forks: **M4 (formant positions) and M6 (HNR) must
land inside child ranges** — these two discriminate child from small-adult
timbre and are exactly what V10's bars failed to check. M5 and M8 as
secondary gates. M1–M3/M10–M12 as watch metrics.

---

## §6. Synthesis: where the models agree and disagree

**Agree:**
- The #1 error is adult-sized formant positions/bandwidths (perceived
  speaker size), not F0 — ARTIC's ~410 Hz F0 was already child-range.
- Glottal tilt too steep and HNR too high (too buzzy, too clean).
- Micro-instability (jitter/shimmer) is load-bearing for child-likeness.
- The M1–M12 battery above (HNR 8–12 dB, jitter >1.5%, tilt −6..−9
  dB/oct, formants per M4/M5) is the objective replacement for ears.
- Laughter must be more than AM — abductory pulses / state looping.

**Disagree:**
- *Where child-likeness lives:* step says **anatomy** (9 cm waveguide
  tract + light folds ⇒ correct formants/bandwidths/HNR emerge from
  physics, including source-filter coupling). swe says **behavior**
  (phonation-mode switching, overshoot attacks, breathy releases, audible
  inhales — child-likeness is gestural, spectrum can be approximate).
- *Tract modeling depth:* step's 13-section physical mesh with
  area-function LUTs vs swe's 3 wide biquads with LFO drift. These are
  opposite bets on how much tract physics is audible.
- *Footsteps:* step reuses the waveguide as a mechanical impact model;
  swe uses Karplus-Strong + noise. Both are buildable; a fork could A/B
  them directly.
- *Parameter richness:* step gives a full physical parameter table;
  swe gives a compact state-machine framing that is easier to unit-test
  per utterance type.

**Coordinator's read for fork builders:** the two paradigms are not
mutually exclusive. The highest-expected-value V11 fork may be a hybrid:
step's waveguide tract (fixes the #1 and #2 errors structurally) driven by
swe's phonation-state gesture sequencer (fixes micro-prosody/instability)
instead of a smooth control script. The diagnosis consensus (M4/M6 kill
bars) should apply to ALL V11 forks regardless of paradigm — V10 proved
that dynamics/flux bars alone pass adult-timbered audio.
