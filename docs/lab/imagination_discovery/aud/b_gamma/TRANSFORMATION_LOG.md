# TRANSFORMATION_LOG.md — mechanism inventory + anti-rename audit

Every transformation B-γ applies to studied grains, with the justification
and the explicit defense against the "renamed synth primitive" charge.
If a mechanism maps 1:1 onto a `synth.zag` primitive, it is banned here.

## The allowed mechanism set (closed list)

| # | Mechanism | What it does | Why it is not a synth primitive |
|---|---|---|---|
| T1 | **GRAIN-CUT** | Segment event grains from study recordings by onset/envelope detection (Python, deterministic). | Editing operation. No waveform is generated; the source is a real recording. |
| T2 | **GRAIN-PLACE** | Put a grain at a new time with a static gain. | Arrangement. A synth *generates*; this *positions* captured events. |
| T3 | **GRAIN-OVERLAP** | Sum two or more grains at the same time. | Mixing — what air does when two real sounds coincide. No partials, no additive resynthesis of spectra: the inputs are whole recorded events. |
| T4 | **GRAIN-REVERSE** | Play a grain backwards. | Editorial transform (samplers do it). Produces "blooming" transients with no natural referent — genuinely new event shapes, still 100% captured samples. Not a filter, not a pitch effect. |
| T5 | **GRAIN-MORPH** | Crossfade grain A → grain B sample-wise over min(lenA,lenB): one real event *becoming* another (e.g. a crack deepening into a plate-break). | Both endpoints are real captured events; the path between them is bounded by their spectra. This is a *transition*, like a branch snapping then the hollow trunk resonating — a natural acoustic phenomenon. It contains no oscillator, no filter sweep, no pitch shift. The closest synth cousin would be wavetable morphing, but wavetables are synthetic cycles; these are recorded events. |
| T6 | **DENSITY-GRAMMAR** | Change *when* events happen per the imagined creature/scene (a 9 m animal fractures at its own rate; an alien sea surfs 3× slower). | A *decision* about the imagined world, not a signal processor. Time is composed; samples are untouched. |
| T7 | **EDGE-GLUE** | ≤2 ms smoothstep fades at grain boundaries only. | Minimum click-prevention edit required by the A-NATIVE law (no digital clicks). Grain bodies are never enveloped. |
| T8 | **BRIGHTNESS-ORDER** | Sort candidate grains by measured centroid and place ascending (the planet-chorus "rising" gesture). | Selection + arrangement of real events. No pitch is shifted; nothing is resampled. |

## Explicitly EXCLUDED (with the reason)

| Excluded | Reason |
|---|---|
| Pitch-shift / resampling | The classic synth-in-costume; changes formants unnaturally. |
| Ring modulation / AM | Synth primitive, full stop. |
| Oscillators, 2-pole resonators, filtered-noise generators | The banned set, under any name. |
| Chirp / boom generators | The banned set (v2's conviction). |
| Stationary noise beds | The banned texture; ambience here is overlapping *real* texture grains (T2+T3), which breathe because the recordings breathed. |
| Time-stretch | Formant/time decoupling is a synth effect; excluded. Slowness is composed via T6 (fewer, longer grains), never by stretching. |
| Synthetic envelopes on grain bodies | sol's event-assembler line: no imposed ADSR. Only T7 edge glue. |
| Reverb / convolution | Would smuggle a resonator network in costume. Space is composed by grain choice and timing, not simulated. |

## Per-piece mechanism use

- **kids** (benchmark/T1): T1, T2, T3, T6, T7. No T4/T5 — the scene is Earth-real; invention is in the composition (a tag game that never happened).
- **planet** (T2): T1–T4, T6–T8. T4: reversed booms as rift exhalations (slow bloom, not a boom hit). T8: the chorus.
- **ocean** (T3a): T1–T4, T6, T7. T4: reversed cracks as fracture-recession tails.
- **monster** (T3b): T1–T3, T5–T7. T5: crack→rumble morphs as plate-breaks deepening. No T4 (the Raxith's cracks are forward — fracture has a direction).

## The audit principle

Every placed grain is traceable: (grain idx → source recording → source
time → class → voice). `study_out/grains.csv` is the map; the scores are
deterministic functions of the pack. If any mechanism above is judged a
renamed synth primitive on listening, that piece's claim dies — the log
is written so the judgment can target the mechanism, not the vibe.
