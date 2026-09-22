# TEST_RESULTS.md — B-γ fork results

**Fork:** B-γ (the monster fork), position (b) study-then-invent, event-assembler.
**Ears:** Micah's (final oracle) + 5 fresh native critics (Test 1) — arranged by the parent.
**Status legend:** ⏳ not yet run · ✅ pass · ❌ fail · 🟡 partial/honest-smaller-claim

## K0 — determinism gate (must pass before anything ships)

| Subject | SHA-256 | 3/3 byte-identical |
|---|---|---|
| kids | `655978ec978a6ae5fd792f3c442b48bba601df307a067ecf0a21144c68464b95` | ✅ |
| planet | `71c5c7b0bcbe7b63cb03baa3336f3ae04bf79e97203b29031a43b768b5c50feb` | ✅ |
| ocean | `e8db1a18f47f1df21e0f63c8fa22a3914c14eb85201ebc94732423d5364278bb` | ✅ |
| monster | `6b0c9c576a0fa504490e79c2a6d36f73d8750917129d19a2d2d7775b2d844a9c` | ✅ |

Rendered by `gamma_bin` (pure Zag, zero RNG) from `study_out/gamma.grpk`
(1278 grains, 12 licensed sources). Rerun: `python3 render_verify.py`.

## K1 — the kids-playing-and-laughter bake-off (benchmark / TEST 1)

**Brief given to judges:** 30 seconds, children playing and laughing:
≥3 distinct child voices, overlapping play, running feet, one laugh tumbling
into another.

**Blind set:** three 30 s clips, hidden deterministic order (sorted by
sha256 of bytes — documented in `blind/ORDER_SEALED.md`):

| judge_A.wav | `blind/clip_synth.wav` | control (i): synth.zag paradigm's best attempt at the same brief |
| judge_B.wav | `blind/clip_real.wav` | control (ii): real playground recording (calibration only) |
| judge_C.wav | `blind/clip_method.wav` (= `render/b_gamma_kids.wav`) | B-γ method |

**Kill bars (from AUDIO_DEBATE.md):**
- Any one "sounds like a synth" from Micah → B-γ's kids claim dies.
- No-copy audit must clear (audit.py, bar 0.80).

| Check | Result |
|---|---|
| no-copy audit (max 2 s window xcorr vs any study source) | ✅ CLEAR — 57 windows, 0 trips, worst 0.361 (bar 0.80), 2026-09-22 |
| A-NATIVE (native_check.py) | ✅ PASS (see table below) |
| ≥3 distinct child voices (audit + critics) | ⏳ critics pending |
| overlapping play / running feet / tumbling laughs (critics) | ⏳ critics pending |
| 5 fresh native critics: method vs control | ⏳ parent to dispatch (brief: `blind/JUDGE_BRIEF.md`) |
| Micah's verdict | ⏳ |

**Control history (honest):** the synth control initially shipped with a
numerical bug — `tsin_small`'s 4-term Taylor series diverges for the
harmonic arguments (ph·2/3/4 up to 25 rad), producing million-scale samples
whose peak-normalization crushed the whole clip to near-silence (5 s digital
black tail, A-NATIVE FAIL). Fixed 2026-09-22: phase wrapped to [−π,π] inside
`tsin_small`, score extended to fill 30 s. Rebuilt control passes A-NATIVE
(peak 0.679, hiss CLEAN, clicks 0.39 < 1.20) — which is exactly why Micah's
ears, not the bar, decide the synth-smell question. Final blind mapping:
judge_A = synth control, judge_B = real playground, judge_C = B-γ method
(deterministic sha256 order, `blind/ORDER_SEALED.md`).

**Outcome:** ⏳

## K2 — anti-v2 rebuild (paradigm escape / TEST 2)

**Question:** does B-γ escape the v2 paradigm (oscillator/resonator/noise-bed
synth smell), or is it a synth in costume?

**Evidence:**
- TRANSFORMATION_LOG.md: closed mechanism list, exclusion list, per-piece use.
- Anti-rename audit: each mechanism defended against 1:1 mapping to synth.zag.
- `b_gamma_planet.wav`: the deliberate anti-v2 artifact — built from the
  debate's anti-v2 brief, no synth primitive anywhere in the chain.

**Judge:** Micah's ears + blind critics on planet.wav.

**Outcome:** ⏳

## K3a — alien ocean generalization (TEST 3a)

**Question:** does the studied vocabulary (Earth surf, thunder, ice) stretch
to an alien ocean without collapsing into Earth pastiche?

**Honest risks (pre-registered):** Earth-surf pastiche; reversed-crack tails
reading as synth-reverse cliché.

**Outcome:** ⏳

## K3b — the Raxith (imagination beyond experience / TEST 3b)

**Question:** can position (b) invent a movie-monster-class creature it never
heard — the Raxith, whose voice is controlled micro-fracture (MONSTER.md,
committed before rendering)?

**Honest risks (pre-registered):** ice-cubes-in-a-glass; Hollywood-boom
pastiche on the plate-breaks; "fracture percussion, not a voice."

**Smaller claim (ready if needed):** "real-event fracture percussion with
language-like phrasing" — reported honestly if the creature-voice claim
fails.

**Outcome:** ⏳

## A-NATIVE quality table (native_check.py, 2026-09-22)

| Clip | peak | DC offset | ZCR | noise-floor slope | exposed hiss | clicks | verdict |
|---|---|---|---|---|---|---|---|
| b_gamma_kids | 0.673 | 0.000072 | 0.063 | natural fall (20.8/6.9/1.7 dB) | 0.013 CLEAN | 0.34 < 1.20 | ✅ PASS |
| b_gamma_planet | 0.680 | 0.000036 | 0.076 | natural fall (8.8/−5.5/−8.2 dB) | 0.065 CLEAN | 0.63 < 1.20 | ✅ PASS |
| b_gamma_ocean | 0.679 | −0.000013 | — | natural fall | 0.006 CLEAN | 0.66 < 1.20 | ✅ PASS |
| b_gamma_monster | 0.679 | 0.000002 | — | natural fall | 0.000 CLEAN | 0.78 < 1.20 | ✅ PASS |

(Crest factors 7.8–28.8 — healthy dynamics, not squashed.)

## Grain inventory (from study_summary.json, 2026-09-22)

| Class | Grains | Voices | Notes |
|---|---|---|---|
| laugh | 144 | 0:27, 1:44, 2:73 | the benchmark's core vocabulary |
| squeal | 107 | 0:29, 1:59, 2:19 | youngest-voice events, trip scene |
| shout | 104 | 0:25, 1:30, 2:49 | calls, "you're it" |
| thump | 231 | — | footsteps, impacts |
| swell | 28 | — | lake-swell anchors (ocean) |
| wash | 19 | — | texture grains (ambience, never a bed) |
| creak | 57 | — | wood/swing creaks (seismic groans, Raxith plates) |
| crack | 442 | — | ice micro-fractures (chorus, Raxith syllables) |
| boom | 60 | — | thunder onsets (rift, plate-breaks) |
| rumble | 65 | — | thunder tails (planet hum, sky hum) |
| wind | 21 | — | Mars wind/dust-devil textures |
| **total** | **1278** | | 12 sources, pack 77.8 MB |

12 sources: 3 playground recordings (CC0 / CC BY-SA 4.0 / PD), gravel
footstep (CC BY 4.0), lake surf (CC BY-SA 4.0), 2 wood creaks (PD), swings
(CC BY 4.0), ice crackling + storm thunder + Mars wind + Mars dust devil
(PD, from aud/inspiration). Full table: STUDY_LOG.md.

## Commitments kept / broken

- [x] every transformation auditable against the grain map
- [x] no study material committed (study_src/, study_out/, binaries excluded)
- [x] synth control built and included blind
- [ ] honest verdicts reported per test, smaller claims where earned
