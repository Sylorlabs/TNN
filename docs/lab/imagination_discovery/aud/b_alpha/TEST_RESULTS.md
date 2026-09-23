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

---

## Battery 1d: Kids / playground — v4 bed rewrite (2026-09-23)

**Artifact:** `clips/b_alpha_kids_v4.wav` — re-render addressing Micah's ear
verdict on v3: "still cuts out, has weird random cut outs and has weird
noises in between like i thought i heard static and also heard mouse squeaks
at the same time." His ears overruled v3's passing A-NATIVE metrics.

**Diagnosis (traced to source, not guessed):** built an instrumented
renderer logging every `place_event` (exact sample start, atom, cls, ratio,
gain) and every bed chunk onset — verified byte-identical to shipped v3
(`3f1f36a9c755a280eca64395c9740a14d8cbc516f2b8f87f5b189d2b05440b50`).
A Python replica of the bed + events correlated 0.9999+ with v3 in test
windows, enabling component-wise attribution of every symptom:

- **"Random cutouts":** v3's 1 s edge fades didn't save short chunks. For
  chunks < 2 s, `ff=wlen/2`; when `ln-44100 < 4410`, `step=ln`
  (butt-jointed). Short chunks faded to ZERO at their midpoint boundary,
  then the next started from zero. 20 ms RMS scan: 8+ dips 18–31 dB
  (3.59 s −18.7 dB/900 ms; 10.80 s −28.6 dB; 14.97 s −26.6 dB; 20.19 s;
  21.63 s; 25.40/25.72/26.09 s). Secondary: texture RMS varied 129..1006
  with no loudness matching — ambience audibly pumped between chunks.
- **"Static":** no sustained static (spectral-flatness scan clean). The
  percept is brief broadband transient grains in bed textures + the level
  pumping above.
- **"Mouse squeaks":** 9–16 kHz transient scan + per-component HF
  attribution. Bed: tx3 @ 28.73 s, tx6/tx7 @ 29.32 s in v3's tail
  (bed-schedule correlation 0.99999 — definitively bed, not score).
  Events: ai=4 (w1 call) @ 23.16 s — broadband click 1.326 s into the atom
  (strongest, +31.7 dB); ai=23 (w1 call) @ 1.22 s; ai=103 (w3 laugh) @
  19.50 s — harsh loud onset; ai=105 (w3 laugh) @ 16.32 s — tonal;
  ai=108 (w3 footstep) @ 26.52 s. Raw-atom HF ≡ placed HF for all: they are
  real recorded sounds in w1–w5, not renderer artifacts. Preserved and
  identified explicitly here, not silently removed.

**Fix in the source** (`src/render.zag`, pure Zag, zero RNG):
- `bed()` rewritten: (1) deterministic waveform-quality qualification —
  each texture's RMS and crest factor computed in-Zag; accepted only if
  rms<600 (quiet) and crest<7.0 (stable). 3 of 13 qualify (tx0, tx1, tx2);
  the click/squeak carriers (tx3, tx5–tx10) are rejected by criterion, not
  by hardcoded index. (2) Per-chunk RMS normalization to a common target —
  no level pumping. (3) Guaranteed crossfade overlap at every boundary
  (`step = wlen - xf`, 0.5 s crossfade clamped to wlen/2) — never
  butt-jointed, never fades to zero alone. 26 chunks (v3: 41).
- Events: unchanged — same 56 scored events, seed 6101, catalog.

| Check | Result |
|---|---|
| Format/duration | 30.00 s mono 44.1 kHz PCM16 ✓ |
| Determinism | 2/2 byte-identical: `5a1b1f7b1f359f4fa6fff40580e72be5c34f33f300dc4b2f9a6140c78eb4ab44` |
| Bed continuity (tail 27–30 s, 20 ms RMS) | max dip −4.6 dB (v3: −16.5 dB) — dropouts gone |
| Bed level | −50.0 dBFS RMS, consistent (v3: −47.8 dBFS with pumping) |
| Bed HF spikes (v3's 27.18/28.80/29.75 s) | GONE — zero bed squeaks |
| Event HF transients | 14 remain, all traced to legitimate scored atoms (listed above) |
| Clipping / DC | peak 0.679, dc −0.000015 ✓ |
| Near-silence runs | max 2.9 ms — no digital gaps |

**Micah ear oracle:** AWAITING.

---

## Battery 1c companions: planet / ocean / alien-ocean v2 re-renders (2026-09-22)

**Renderer provenance:** all three re-rendered with a binary built from the
committed fixed `src/render.zag` (bed 1 s smoothstep crossfades +
`place_event` 8 ms attack / 60 ms release). The binary reproduces
`clips/b_alpha_kids_v3.wav` byte-identically
(`3f1f36a9c755a280eca64395c9740a14d8cbc516f2b8f87f5b189d2b05440b50`),
proving it is the fixed renderer. Same seed 6101, same catalogs, same
scores as the v1s — the only delta is the bed crossfades + release fades
(same relationship as kids v3→v2). No scored-event changes: every fast
envelope drop/rise in each v2 matches a v1 drop/rise within ~30 ms, so all
remaining transients are content-driven (scored events + bed texture
motion), none are new render artifacts.

### Planet v2 — `clips/b_alpha_planet_v2.wav` (21.00 s, catalog2, score_planet)

| Check | Result |
|---|---|
| Determinism | 2/2 byte-identical: `7e561a5aa97661594fa9a5f51789a6c74439ea55bc0557ce90b747f8feaa043a` |
| Hard digital cuts (exact-zero runs ≥64 from audible) | v1: 1 (20.997 s tail chop, 131 zeros, pre −56.1 dBFS) → **v2: 0** |
| Fast envelope drops >12 dB/60 ms | 20 → 19; rises 25 → 25; all times match v1 (scored event onsets/ends, zero cliffs) |
| A-NATIVE | PASS — dc=−0.0000008, peak=0.679, maxjump=0.3723@19.509 s (smooth swing ctx [−0.2944,−0.1019,0.2705,0.3876,0.2625] — natural transient, not a click), zcr=0.0314, quietest-100 ms −62.7 dBFS@8.20 s zcr=0.0934 (no hiss) |
| v1↔v2 correlation | 0.9945 — composition unchanged |

**Micah ear oracle:** AWAITING-EARS.

### Ocean v2 — `clips/b_alpha_ocean_v2.wav` (30.00 s, catalog3, score_ocean)

Retains its negative-control status (direct ocean referents — disqualified
as Test 3 evidence, kept as the invalid-path control). Re-rendered for the
same bed defect, nothing else.

| Check | Result |
|---|---|
| Determinism | 2/2 byte-identical: `fda70d5548484ce7dd0cb78a0de3eacb8e51d1076ef0fbe686efb15958c9cbca` |
| Hard digital cuts (exact-zero runs ≥64 from audible) | v1: 0 → v2: **3 flags, all traced benign** (smooth fades through the quantization floor — zero discontinuities): 23.732 s (185 zeros): butt-jointed chunk boundary at 23.760 s, smooth V dip −17.8→−73.4→−41.7 dBFS over ~1.5 s (the fix's by-design crossfade through zero; v1 had a hard cliff −13.8→−37.6→−26.6 at the same boundary), max single-sample jump −29.8 dBFS in region; 29.532 s (185 zeros): sub-floor dip at the 29.560 s overlap boundary, envelope −55.8→−78.3→−36.6 smooth, max jump −49.7 dBFS; 29.988 s (551 zeros): intended final-chunk fade-out reaching digital zero 12.5 ms before clip end, max jump −55.0 dBFS |
| Fast envelope drops >12 dB/60 ms | 15 → 17; rises 14 → 14; all times match v1 (content-driven) |
| A-NATIVE | PASS — dc=−0.0000104, peak=0.679, maxjump=0.1281@22.415 s (natural), zcr=0.0403, quietest-100 ms −84.3 dBFS@11.90 s zcr=0.0005 (no hiss) |
| v1↔v2 correlation | 0.9938 — composition unchanged |

**Micah ear oracle:** AWAITING-EARS. Note for his brief: the 23.7 s region
now breathes through a ~1.5 s quiet dip instead of v1's hard cliff — smooth
by construction, but the dip reaches the digital floor, so his ears decide
whether it reads as a natural swell or a dropout.

### Alien-ocean v2 — `clips/b_alpha_alien_ocean_v2.wav` (30.00 s, catalog2, score_alien)

| Check | Result |
|---|---|
| Determinism | 2/2 byte-identical: `1173dabd1cfc157de2a3bf335320696a52b5cc51ef2ef411aaa355a39c1e27c7` |
| Hard digital cuts (exact-zero runs ≥64 from audible) | v1: 0 → v2: **1 flag, traced benign**: 29.997 s (152 zeros) = final-chunk fade-out tail; tail envelope −47.5→−19.8 (event swell)→−49.6→0 continuous |
| Fast envelope drops >12 dB/60 ms | 34 → 29; rises 36 → 38; all times match v1 (surf wave-sets, storm rolls, whale-call passes — content-driven) |
| A-NATIVE | PASS — dc=−0.0000588, peak=0.679, maxjump=0.1821@20.985 s (smooth swing, natural), zcr=0.0282, quietest-100 ms −67.6 dBFS@9.60 s zcr=0.0587 (no hiss) |
| v1↔v2 correlation | 0.9871 — composition unchanged |

**Micah ear oracle:** AWAITING-EARS.

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

## Battery 1e: component-isolation renders (2026-09-23)

**Trigger:** Micah's ear verdict on v4 — "nothing improved, same damn result."
v4 fixed the bed; all 56 events were unchanged. Five isolation renders so he
can point at the bad component. Full analysis in `FINDINGS_1e.md`.

| Clip | Content |
|---|---|
| `b_alpha_kids_1e_a_bedonly.wav` | bed only, true mix level (−48.4 dBFS RMS) |
| `b_alpha_kids_1e_b_eventsonly.wav` | 56 events only, true mix level (−20.2 dBFS RMS) |
| `b_alpha_kids_1e_c_mix_v4replica.wav` | full mix, byte-identical to v4 (`5a1b1f7b…`) |
| `b_alpha_kids_1e_d_mix_noharsh.wav` | mix minus the 6 harsh-atom placements |
| `b_alpha_kids_1e_e_mix_replaced.wav` | mix with harsh atoms swapped for lowest-crest same-class atoms |

Key measurements: the 5 harsh atoms carry 11% of event energy (ai=4 ranks
#49/56 by placed RMS); no digital defects in any of them; events cover 75%
of the timeline (sparse-scheduling hypothesis rejected); the systemic fact
is peak-normalization of every atom to 0.55–0.75 FS over a −48.4 dBFS bed
(~31 dB contrast, unchanged since v1). Recommendation: v5 changes gain
staging, not atoms.

**Micah ear oracle:** AWAITING.
