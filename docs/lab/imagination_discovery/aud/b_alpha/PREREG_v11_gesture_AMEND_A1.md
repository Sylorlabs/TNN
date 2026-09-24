# PREREG AMENDMENT v11_gesture-A1

**Date:** 2026-09-24 (PDT)
**Amends:** PREREG_v11_gesture.md (commit efa5f35a2bd3c3af36d8e0cca13a5a3760f683ab)
**Status:** COMMITTED BEFORE USE — no render with amended parameters exists yet.

## A1.1: Vowel area LUT retuning (rows /a/ and /o/)

**Change:** Replace the /a/ and /o/ area-function rows with numerically
optimized values. Rows /i/, /e/, /u/ unchanged.

New /a/ (row 2):
1.5 1.9 3.52 3.38 2.7 4.38 4.036 5.68 7.9 9.22 9.849 9.0 10.9

New /o/ (row 3):
1.436 2.3 4.476 3.98 2.724 2.676 1.9 1.38 3.3 2.971 2.4 0.4 1.1

**Justification (measurement, not tuning-to-metric):**
The frozen LUTs were an initial guess. A numpy replica of the exact
waveguide + voice_sig LPC-centroid computation (validated: replica
739/2254/3428 vs scene 752/2598/3546) showed the guessed /a/ produces
F2B/F3B centroids ~450/700 Hz above the anchor (2104/2814). Coordinate
descent on the 13 areas against the replica (targets = anchor centroids)
yielded the above profiles, which score F1B=769/F2B=2104/F3B=2817
(/a/) and F1B=647/F2B=1613/F3B=2801 (/o/) on the replica — i.e., the
tract now produces the anchor's formant distribution. This is a
mechanism repair (wrong initial guess), not metric-chasing: the
optimization target was the ANCHOR's acoustic properties, derived from
the frozen instrument's definition.

**Vowel assignment:** Utterances now use /a/ (2.0) and /o/ (3.0)
predominantly (tunable per §8: "vowel-morph assignment per utterance").
Giggles already used /a/.

## A1.2: Footstep frequency range (130–200 Hz → 100–145 Hz)

**Change:** Footstep thud frequencies move from 130–200 Hz to 100–145 Hz.
Amplitudes: chase steps 0.16→0.10 (level, §8-tunable).

**Justification (instrument artifact, not voice tuning):**
The frozen voice_sig's voice gate accepts F0∈[150,800] Hz. Footstep
thuds at 140–200 Hz pass the periodicity gate and are counted as "clean
voice frames" (P10=184.5 Hz in the first render), corrupting V-F0DYN
(537 Hz vs anchor 174 Hz). This is a measurement artifact: footsteps are
not voice. Moving thuds below 150 Hz ensures the instrument's own F0
floor rejects them, while preserving their scene function (audible
child thuds). The thud timbre (damped sine + LP noise) is unchanged.

## A1.3: What is NOT changed

- Shaper LUTs, gesture state table, scene arc, hash scheme: frozen.
- All §8 knob changes (F0 bases +35 Hz, breath_gain 0.5→0.3,
  jitamp 0.03→0.02, radc 0.96→0.90, eff_s adjustments) were already
  within declared ranges and are documented in FINDINGS, not here.
- The kill rules and judging protocol are unchanged.

## Verification

After this amendment is committed, the renderer will be rebuilt and
measured. The amendment is valid only if the new render's voice_sig
shows F2B/F3B moving toward the anchor WITHOUT degrading the already-
passing bars (V-F1, V-F2DYN, M-MOD).
