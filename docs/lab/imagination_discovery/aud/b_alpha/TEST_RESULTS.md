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

## Battery 1b: Kids / playground — v2 natural ending (2026-09-22)

**Artifact:** `clips/b_alpha_kids_v2.wav` — re-render of the flagship kids clip
addressing Micah's ear verdict: v1 was the most realistic of all five clips,
but all five "cut off weirdly" (v1's last-2s envelope stayed loud to the
final sample, then exact zeros — a hard digital cut mid-sound at ~-10 dB).

**What changed in the score** (`src/render.zag`, `score_kids`, same seed 6101,
same `catalog.bin`):
- Grammar-fill loop bound `29.5` → `26.0` (both the `while` and the placement
  guard).
- The explicit 27.0 s and 28.6 s events and the 4th footstep (~27.1 s) are
  REMOVED — last placed event now starts at ~26.42 s, so its natural decay
  completes by ~28.4 s and the last ~1.5 s is quiet room tone resolving to
  the bed's natural floor. No synthetic fade added anywhere (compositional
  fix only; the common writer's 30 ms de-click edge fade applies as in v1).
- New `reserve()` helper replicates `ev()`'s atom selection (hash pick,
  3 s lastuse guard, `usedcl` marking) without placing audio, so the
  hash-walk state (`stm`, `lastuse`) entering the grammar fill is
  byte-identical to v1 for every event before the cutoff. All other content
  (seed, catalog, grammar, bed) unchanged.

| Check | Result |
|---|---|
| Format/duration | 30.00 s mono 44.1 kHz PCM16 ✓ |
| Voice clusters used | 0, 1, 2 (unchanged) |
| A-NATIVE | PASS — dc=-0.000001, peak=0.679 (3.4 dB headroom), maxjump=0.2425 (field-range), zcr=0.0516, no hiss (quietest-100ms HF frac=0.001) |
| Determinism | 3/3 byte-identical: `c6be7e1fb9b135f10236f2b86b1afa2b0b22e8f12724d669a3468af0a48caf89` |
| Tail envelope (last 2 s, per-100 ms max) | v1: [3910…14647…8971] loud to the last sample → v2: [46,53,84,1327,1478,1265,1177,1409,1013,926,1484,2231,1279,616,265,336,650,471,2000,452] — genuine decay to the floor |
| Final 100 ms max | 452 (≤1000 bar) ✓ |
| v2 last-1 s rms | 218 (-43.5 dBFS) vs v1's 2622 (-21.9 dBFS) |

**Rest-of-piece unchanged (diff summary vs v1):** the writer's global
DC-subtract + peak-normalize means raw byte-identity isn't achievable, but
the global peak is at the identical sample in both files (22259 @ 5.764 s →
normalization unchanged) and the sample-wise difference `v1−v2` is a 0.15 LSB
DC-shift floor (rms 0.36 LSB, max 6.1 LSB — inaudible) over the entire first
27.0 s. First sample exceeding that floor is at exactly 27.000 s — the
removed explicit event. In other words: v1 had no fill events in
[26.0, 27.0), and everything before 27.0 s is the same audio in both files;
the only content difference is the removed late events (their energy accounts
for essentially all of v1's tail: rms 2610 of the 2622).

**Micah ear oracle:** AWAITING (v1 verdict was binding-most-realistic; v2
keeps v1's content with the cut fixed).

---

## Battery 1c: Kids / playground — v3 cutout fix (2026-09-22)

**Artifact:** `clips/b_alpha_kids_v3.wav` — re-render addressing Micah's ear
verdict on v2: it STILL "cuts out weirdly." The v2 fix (removing the late
composed events) did not resolve what he hears — because the cutout was
never in the composed score. It was in the ambience bed.

**Diagnosis (measured, then traced — not guessed):**
- Full-clip envelope scan of v2 found the two dominant defects at
  **27.35 s** (hard cut: −21.5 dBFS → −58 dBFS, then ~1 s of dead air) and
  **28.35 s** (hard attack: −51 dBFS → −24.5 dBFS out of the floor).
- An instrumented build (event map: every `place_event` start/end + every
  bed chunk onset; verified byte-identical to shipped v2,
  `c6be7e1f…`) showed **zero composed events** start or end at either
  timestamp. Both align to the sample with **bed texture-chunk onsets**
  (27.35 s: delta −10 ms; 28.35 s: delta 0 ms).
- **Root cause:** `bed()` chained texture chunks at full level with no edge
  fades and no crossfades — its own comment claimed "1 s crossfades" but the
  code just summed full-level chunks. 21 hard chunk boundaries in 30 s: short
  chunks butt-jointed with hard cuts on both ends; long 1 s-overlap chunks
  still ended with a hard drop of the old layer. Secondary: `place_event()`
  used symmetric 8 ms edges, leaving fast fades on loud atom endings
  (28–33 dB drops inside 60 ms at 25.40/25.72/26.08 s).
- v2's composed-event removal could never fix this: the bed runs the whole
  clip. This also explains the v1 verdict that all five clips "cut off
  weirdly" — the bed is shared by every score.

**Fix in the source** (`src/render.zag`, pure Zag, zero RNG — all fades
analytic, fully deterministic):
- `bed()`: every texture chunk now gets 1 s smoothstep crossfades — fade-in
  over its first 1 s (except the clip-opening chunk, whose onset is the clip
  onset), fade-out over its last 1 s (computed on the clip-truncated written
  length, so the final chunk still fades). Overlapping chunks crossfade at
  constant amplitude (smoothstep(u)+smoothstep(1−u)=1); butt-jointed chunks
  meet at zero. No clicks possible by construction.
- `place_event()`: split edges — 8 ms attack (transient crispness kept),
  60 ms release (no audible chop on loud atom endings).
- Also repaired two stale comments the work exposed (the aspirational
  "crossfades, breathing gain" note; the TEST 2 header sitting above
  `score_kids` instead of `score_planet`).

**What changed vs v2:** same seed 6101, same `catalog.bin`, same score —
no composition change. v3↔v2 correlation 0.99; the difference is the bed
crossfades + release fades only.

| Check | Result |
|---|---|
| Format/duration | 30.00 s mono 44.1 kHz PCM16 ✓ |
| Voice clusters used | 0, 1, 2 (unchanged) |
| A-NATIVE | PASS — dc=−0.0000052, peak=0.679, maxjump=0.3572 (verified natural zero-crossing transient at 19.419 s, byte-identical transient in v2 — not a click), zcr=0.0461, quietest-100ms −73.1 dBFS zcr=0.0002 (no hiss) |
| Determinism | 2/2 byte-identical: `3f1f36a9c755a280eca64395c9740a14d8cbc516f2b8f87f5b189d2b05440b50` |
| Hard digital cuts (exact-zero runs ≥64 from audible) | 0 |
| Fast envelope drops >12 dB/60 ms | 12 remain — all traced: scored event onsets (8 ms de-clicked attacks: footsteps/laughs at their scored times) or smooth 30–60 ms release fades on event endings; zero cliffs, zero un-scored pops |
| The 27.35 s cut / 28.35 s attack / 1 s dead gap | GONE — tail now decays smoothly to the bed floor, no gap, no pop |
| v2→v3 tail (per-100 ms max, 27–30 s) | v2: […1869, 29×8 (dead), 1327…] → v3: [741, 519, 207, 32, 13…21 (floor), 101…1228 (natural bed swell), …363] — continuous |

**Micah ear oracle:** AWAITING — the measurements show no audible chops;
his ears are final.

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
