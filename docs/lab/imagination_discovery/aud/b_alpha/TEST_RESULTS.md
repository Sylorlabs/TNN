# Fork B-α — Test Results

**Date:** 2026-09-22
**Position:** (b) study-then-invent, pure
**Rule:** Tests determine outcomes. Document everything.

---

## Battery 1: Kids / playground (flagship)

**Artifact:** `clips/b_alpha_kids_v1.wav`
- 30.00 s, mono, 44.1 kHz, PCM16
- Scene: three children (clusters 0/1/2 as voice roles) — chasing game, overlapping play,
  running feet, laugh cascade at ~16 s (trip-and-tumble), grammar fill between beats.

| Check | Result |
|---|---|
| Format/duration | 30.00 s mono 44.1 kHz ✓ |
| Voice clusters used | 0, 1, 2 (three roles) |
| A-NATIVE | PASS — dc=-0.000002, peak=0.679 (3.4 dB headroom), maxjump=0.2425 (field-range), zcr=0.0508, quietest-100ms rms=0.00135 zcr=0.0406 (no hiss) |
| Determinism | 3/3 byte-identical: `47cb7f04a106a42be95311ceb4cc2750bb5981f848ca4ed71885380531c31e84` |
| No-copy (correlation) | d=0.896 ≥ 0.450, closest window 4/57 vs 367 study windows — PASS |
| Blind test (5 critics) | NOT YET RUN — requires browser delegation for critic recruitment |
| Real-playground calibration | NOT YET PACKAGED |
| Micah ear oracle | AWAITING |

**Caveat:** "Three distinct children" = three descriptor clusters used as roles. No
listening-based identity audit has confirmed perceptual distinctness. The blind test
will adjudicate.

---

## Test 2: Kethra's planet voice (rebuild from scratch)

**Artifact:** `clips/b_alpha_planet_v1.wav`
- 21.00 s (matches `d_aud3_planetvoice_v2.wav` duration for A/B)
- Scene: deep argon/nitrogen world — tidal pressure swells (Mars wind, slowed),
  rift-vent exhales, cryo-crack field (ice, sparse), thunder rolls, call-and-response
  "voice" phrases between vent fields.

| Check | Result |
|---|---|
| A-NATIVE | PASS — dc=0.000001, peak=0.679, maxjump=0.3723 (verified natural transients, not clicks), zcr=0.0310 |
| Determinism | 3/3 byte-identical: `0c15ea56f9295c1818cd1b6162f0ec08af4938205d9abd1e0f398f4ec514c544` |
| No-copy | d=0.708 ≥ 0.450, window 4 — PASS |
| Blind A/B vs `d_aud3_planetvoice_v2.wav` | NOT YET RUN — requires the v2 file and blinded presentation |
| "Meaningful but unrecognizable as same paradigm" | UNJUDGED — needs Micah's ears |
| Micah ear oracle | AWAITING |

---

## Test 3: Alien ocean's surf at dawn, sky hums (NO direct study referent)

**Valid artifact:** `clips/b_alpha_alien_ocean_v1.wav`
- 30.00 s, built ONLY from catalog2 (Mars wind, dust devil, storm, ice).
- Surf = wind atoms arranged as dawn wave-sets (3, pause, 4 building, climax, settle).
- Sky hum = wind atoms slowed (0.55–0.62×), long overlaps, dawn swell arc.
- Deep alien ones = storm atoms. Ice glints sparse.
- **Zero ocean/wave/throat-singing/whale material.** No direct referent for any scene element.

| Check | Result |
|---|---|
| A-NATIVE | PASS — dc=-0.000044, peak=0.679, maxjump=0.2101, zcr=0.0299 |
| Determinism | 3/3 byte-identical: `bfcc78f8b33922087034c9c8198fe9de1d8e9c613e242838f801afd81345f8fd` |
| No-copy (vs planet study) | d=0.674 ≥ 0.450, window 56 — PASS |
| "Alien ocean's surf at dawn, sky hums" | UNJUDGED — needs Micah's ears |
| Rename trigger | If Tests 1–2 pass but this fails his ear test → claim renames to **"study per scene"** |

**Invalid path (documented, not claimed):** `clips/b_alpha_ocean_v1.wav` (score_ocean,
catalog3) uses tropical-ocean and sea-wave recordings as direct surf referents. It passes
all technical gates (determinism 3/3: `96cb8d468fccda5d1984ebbfad315908ff2492b5f46928c0f3a79ba44ebb93d7`,
no-copy d=0.905, A-NATIVE clean) but is **disqualified as Test 3 evidence** by the
no-direct-referent rule. Retained as a negative control.

---

## No-copy gate: limitations

The current auditor implements **one** distance measure (normalized zero-lag
cross-correlation, downsampled ×8). The assignment requested multiple independent
distances. Additional measures (e.g., spectral-flux distance, MFCC-free timbral distance)
are NOT yet implemented. The single-metric gate is frozen at d≥0.450 and reported honestly
as a partial gate.

**Minimum-variation:** Not yet formally gated. All outputs use ≥3 distinct atoms per
2 s window by construction (event density), but no automated minimum-variation metric
has been run. Flagged as open.

---

## Synth control

**Artifact:** `clips/control_synth_kids.wav` — deliberately convicted synthesis paradigm
(sine LUT, inharmonic partials, filtered-noise bed, chirp giggles, decaying-sine steps).
For blind-test contrast only. Current SHA must be re-verified after the common-writer
DC-subtraction change (was `a4f20cc4...` pre-change).

---

## Open items (require Micah or browser delegation)

1. Five fresh blind critics (B-α kids vs synth control vs real playground) — needs delegation.
2. Planet blind A/B vs `d_aud3_planetvoice_v2.wav` — needs the file and blinding.
3. Micah's ear oracle on all three — the final kill/confirm for every claim.
4. Multi-distance no-copy gate — implement ≥2 independent measures.
5. Minimum-variation gate — formalize and run.
