# UNPLAYABILITY_AUDIT.md — A-α (physical scene simulation)

Every component below is audited against the bright line: **no component may
accept arbitrary excitation and produce arbitrary tones.** If a component can
be "played" as an instrument (arbitrary in → musical out), the claim is dead.

## Audit method
For each component: (1) list every input it accepts; (2) show each input is a
committed scene/physiology quantity, not a musical parameter; (3) attempt the
"instrument test" — try to make it play a melody — and record the failure.

---

## 1. Vocal valve (suction-driven fold analog)

**What it is:** A single tissue mass on a spring (the fold body), driven by
lung pressure on its underside and closed by Bernoulli suction when glottal
flow is high (blow-open / suck-shut relaxation). Documented probe series
(probe1–probe19): the two-mass Ishizaka-Flanagan formulation proved too
delicate to voice reliably (settled to static flow in all 14 constant-pressure
trials); the suction valve self-oscillates robustly at its committed operating
point. The audit does not hide this substitution.

**Inputs accepted:**
| Input | Scene meaning | Musical? |
|---|---|---|
| `psg` (lung pressure, Pa) | Diaphragm/lung state; committed breath script | No — it is a pressure, not a pitch. Raising it changes loudness/roughness and (non-monotonically) the emergent f0, but there is no frequency input. |
| `ag0` (rest glottal half-gap, m) | Fold adduction (muscle) | No |
| tissue `mm`, `kk` | Fold mass/stiffness (anatomy, fixed per child) | No — fixed at build; not an input at render. |
| `a_push`, `a_suc` | Glottal geometry (anatomy, fixed) | No |

**It does NOT accept:** frequency, pitch, amplitude envelope, waveform, or
any audio-rate signal. There is no oscillator, no phase accumulator, no
wavetable, no FM/AM input.

**Instrument test:** Try to play "Mary Had a Little Lamb." There is no input
that selects pitch. Varying `psg` over 1300–1900 Pa moves the emergent f0
non-monotonically across two modes (621 → 380 → 255 Hz) with chaotic breaks;
it cannot be steered through a scale. **FAIL TO PLAY (as required).**

**Why not a synth in costume:** The periodicity is the valve's limit cycle,
not a clock. Perturb the anatomy and the pitch changes unpredictably or the
valve falls silent (documented: mass×2 → silent; Ps=1300 → silent). A synth
oscillator never falls silent when you change its "mass."

---

## 2. Vocal tract (digital waveguide, variable area)

**What it is:** A 1D acoustic tube (14–16 sections) with cross-areas from
committed articulatory postures (NEUTRAL/LAUGH/WHOOP/SQUEAL/EH in SCENE.md).
Propagation is the physical wave equation; there are no filter coefficients.

**Inputs accepted:** Section areas (m²), morphed between committed postures
by the gesture script. **It does NOT accept:** formant frequencies,
bandwidths, resonance gains, or filter Q.

**Instrument test:** The tract alone makes no sound (it is a filter, and an
honest one — it only shapes what the valve gives it). Driving it with an
arbitrary impulse train is not an offered input. **FAIL TO PLAY.**

**Anti-rename note:** This is not a "resonator bank." A resonator bank has
(frequency, bandwidth, gain) knobs; this has (tube areas) from a tongue/jaw
posture. Moving the tongue tip constriction forward raises F2 — because the
tube got shorter in front, not because a knob turned.

---

## 3. Diaphragm / lungs (breath script)

**What it is:** A pressure trajectory: baseline + raised-cosine pulses
(strengths committed in SCENE.md) × lung-volume sag. The pulses are the
diaphragm muscle; the sag is the lungs emptying (volume → pressure).

**Inputs accepted:** None at render. The script is committed data, not a
performance interface.

**Instrument test:** There is no real-time input. Rewriting the script is
rewriting the scene, not playing an instrument. **FAIL TO PLAY.**

**Anti-chirp-generator defense:** The 5 Hz is the diaphragm's contraction
rate (physiology), and the pulse SHAPE comes from muscle mechanics
(raised-cosine), not from a desire for a "nice envelope." The valve's
response (each pulse's waveform, whether it voices, the subharmonic breaks)
is emergent. If the pulses are removed, the valve still voices (it is not a
gated oscillator) — the pulses modulate, they do not generate.

---

## 4. Footfalls (body + surface)

**What it is:** A running body (mass, leg length → stride from ballistic
pendulum) produces foot-strike velocities; each strike drives a
mass-spring-damper contact chain (surface stiffness/damping/grain schedule
committed per surface: rubber, dirt, metal rungs).

**Inputs accepted:** Body state (position, velocity) from the locomotion
model. **It does NOT accept:** impact times, amplitudes, or "drum hits."

**Instrument test:** Try to play a rhythm. The footfalls occur when the body
model's feet hit the ground, which is determined by (speed, leg length,
terrain). You cannot place a hit arbitrarily without moving the body there,
and moving the body changes everything else (who is where, when). **FAIL TO
PLAY as a drum machine.**

---

## 5. Slide creak / swing creak (stick-slip)

**What it is:** Coulomb stick-slip: a mass on a surface with
velocity-weakening friction, driven at the (committed) sliding speed.
The tone is the stick-slip limit cycle, not an oscillator.

**Inputs accepted:** Sliding speed (from the scene: child mass descending
the slide; wind for the swings). **It does NOT accept:** pitch or amplitude.

**Instrument test:** The creak frequency is set by (mass, stiffness,
friction curve) — all committed. There is no pitch input. **FAIL TO PLAY.**

---

## 6. Wind / aeolian tones (vortex shedding)

**What it is:** Cylinders (slide poles, swing chains) shed vortices at
f = St·v/d (St=0.2, committed diameters, v from the committed gust schedule).
The sine LUT renders the (physically sinusoidal) lift force.

**Inputs accepted:** Wind speed (from the gust schedule, committed).
**It does NOT accept:** frequency or amplitude.

**Instrument test:** To "play" a tone you would have to command the wind,
which is a committed weather schedule. **FAIL TO PLAY.**

**Sine-LUT audit:** The LUT is used ONLY for (a) vortex-shedding lift
(physically sinusoidal) and (b) raised-cosine gesture windows (muscle
mechanics). It is never used as a voice source, never frequency-modulated
for pitch, never summed into a "pad." Each use is listed here.

---

## 7. Room / scene propagation (image sources)

**What it is:** Direct path + ground/slide/fence image sources, with 1/r
spread and per-path air absorption from the committed geometry. No late
reverb, no wet/dry, no decay time.

**Inputs accepted:** Source/mic positions (from the scene). **It does NOT
accept:** reverb time, room size, wet/dry, or any "space" knob.

**Instrument test:** It cannot generate sound, only propagate it. Moving the
mic is moving the mic (the scene changes). **FAIL TO PLAY.**

**Anti-reverb defense:** There is no feedback delay network, no comb/allpass
cascade, no exponential decay generator. The "reflections" are 3 image
sources with physical delays/gains. If it sounds "dry," that is because it
is outdoors.

---

## 8. Grains (dirt/sand impacts)

**What it is:** Discrete mass-spring impacts (committed schedules from the
locomotion/wind). Each grain is an event, not a bed.

**Inputs accepted:** Impact velocity (from the foot/wind model).
**It does NOT accept:** density, brightness, or "texture" knobs.

**Instrument test:** Grains occur when the physics says they do. **FAIL.**

---

## General anti-rename audit

| Banned thing | Costume it might wear | Verdict here |
|---|---|---|
| Oscillator | "valve limit cycle" | The valve's period is emergent and fragile (documented mode-hops); an oscillator is robust and tunable. This is not an oscillator. |
| Resonator | "waveguide tube" | The tube has no resonance knobs; its modes come from (length, areas). Moving a constriction moves formants for physical reasons. |
| Noise bed | "grain schedule" | Grains are discrete events with committed times; a bed is stationary. Autocorrelation of the grain track shows no periodicity. |
| Chirp | "5 Hz pulses" | The pulses are diaphragm muscle (physiology), not frequency sweeps. The valve's f0 is not swept by the pulses (documented: pulsing destabilizes; burst mode used). |
| ADSR | "raised-cosine bump" | The bump is muscle contraction shape; it gates lung pressure, not amplitude. There is no sustain/release. |
| Reverb | "image sources" | 3 specular paths, no recirculation, no decay knob. |

## Unplayability summary

No component accepts a musical input (pitch, note, rhythm, timbre knob).
Every input is a scene quantity (pressure, position, wind, anatomy). The
system as a whole cannot be played: there is no score input, no MIDI, no
"trigger." To change the sound you must rewrite the scene (move the children,
change the wind, alter the anatomy) — which is re-imagining, not performing.
