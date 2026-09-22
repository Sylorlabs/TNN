# SCENE.md — A-α (physical scene simulation)

**STATUS (2026-09-22):** This document was revised to reflect EVIDENCE, not
aspiration. The original draft contained forward-looking claims (two-mass
folds, f0 targets 430/350/290 Hz, "emergent" waveforms) that the probes did
NOT validate. What follows is what was actually built and measured.

## What was built

**Voice source:** Single-mass suction valve (blow-open / suck-shut), NOT the
two-mass Ishizaka-Flanagan model. The two-mass proved too delicate to voice
reliably (14 constant-pressure trials, all settled to static flow). The
suction valve self-oscillates but is FRAGILE (narrow regime, mode-hops,
intermittent startup).

**Measured f0s (not targets):**
- Child A/B: ~1050-1076 Hz (Ps=1700-1800 Pa)
- Child C: ~1102 Hz (Ps=1900 Pa)

These are HIGHER than the intended 290-430 Hz. The valve does not track
anatomical targets reliably. The "three distinct voices" are distinguished
by rhythm/burst pattern and (for C) f0, NOT by three controlled pitches.

**Vocal tract:** 14-section uniform waveguide (scalar, NOT area-varying).
The committed articulatory postures (LAUGH/NEUTRAL/etc.) were NOT implemented.
The tract is uniform; formants are at 788/2364/3940 Hz (for 14 sections).

**Breath:** Burst-mode gating (diaphragm pulses), NOT continuous pressure.
The 5 Hz "ha-ha" comes from the burst rate (0.19s on, 0.06s off).

## PIECE 1 — "Tag at the playground" (kids benchmark, 30 s)

### The place
Playground, late afternoon. Mic at (0,1.5,0). Slide, fence, ground as
reflectors (image sources). Air: 20°C, c=343 m/s (used 343, not 353).

**NOTE:** The image-source room was NOT implemented in the final render.
The output is direct sound only (no reflections). This is a gap.

### The children (as built)

| Child | Bout times | Bursts | Ps (Pa) | Measured f0 | Distinction |
|---|---|---|---|---|---|
| B (6yr) | 3.6-5.6s, 14-18.5s | 8×(0.19+0.06)s, 10×(0.19+0.06)s | 1800, 1700 | 1076, 1050 Hz | Rhythm |
| A (4yr) | 4.0-5.2s, 12.5-19s | 5×(0.15+0.05)s, 14×(0.20+0.07)s | 1800, 1700 | 1050 Hz | Faster giggle |
| C (8yr) | 16.0-17.5s | 6×(0.17+0.06)s | 1900 | 1102 Hz | Higher f0 |

**Honest assessment:** A and B are NOT distinct in f0 (both ~1050 Hz). They
are distinguished by burst duration (A: 0.15s, B: 0.19s) and timing. C is
distinct (1102 Hz). This WEAKLY satisfies "three distinct voices."

### Footsteps
Implemented: mass-spring-damper contact (foot mass 2kg, surface stiffness
per material). Surfaces: rubber (k=30k), dirt (k=60k + grains), metal
(k=200k + 720Hz ring). Stride from committed leg lengths.

**NOTE:** Footstep timing is from a simple loop (t += 0.42s), NOT from a
full body dynamics simulation. The "body locomotion" is kinematic, not
dynamic. This is a gap.

### Ambient
**NOT IMPLEMENTED.** The wind, swing creaks, and slide aeolian tones from
the original SCENE were not built. The render has voices + footsteps only.

## What was NOT built (gaps)

1. **Kethra (Test 2):** Not started. The valve source is unsuitable for
   planetary-scale phenomena (tidal flex, rift, dunes). A different physical
   model is needed.
2. **Alien ocean (Test 3):** Not started. Requires surf (breaking waves) and
   "sky hum" (magnetospheric?) models. Not attempted.
3. **Monster (objection):** See MONSTER.md (thought experiment, not a build).
4. **Room reflections:** Planned but not implemented.
5. **Moving vocal tract:** Planned but not implemented (uniform tube).
6. **Two-mass folds:** Attempted, failed (documented in TEST_RESULTS.md).

## Physical commitments (honest)

**What IS physical:**
- Valve: mass-spring-damper with aerodynamic forces (Bernoulli suction).
  Fragile, but physical.
- Waveguide: 1D wave equation (Kelly-Lochbaum). Physical.
- Footsteps: mass-spring contact. Physical.
- Breath pulses: diaphragm muscle (raised-cosine). Physical.

**What is WEAK:**
- f0 control: The valve mode-hops; f0 is not reliably set by anatomy.
- Voice distinctness: A/B share f0; distinction is rhythmic, not anatomical.
- Tract: Uniform, not articulatory. Formants are not from tongue/jaw.
- Startup: Valve needs Ps=1800 to start reliably (not physical; it's a
  numerical kick).

**What is MISSING:**
- See gaps above.
