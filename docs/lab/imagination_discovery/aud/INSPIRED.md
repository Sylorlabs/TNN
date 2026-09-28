# D-AUD-4 — INSPIRED: Kethra's voice, re-imagined through real alien sound

**The diagnosis.** The lead's verdict on the program so far: audio never
gets it right; maybe it needs inspiration. Human imagination is inspired
all the time — pure from-scratch invention may be the wrong starting point
for sound. So this piece was built differently: first listen to real alien
sound (Mars has wind; NASA recorded it), study it, then deliberately invent
Kethra's voice *from* that inspiration. Inspiration is a starting point, not
a sample pack — not one sample of the field recordings appears in the
piece. Every sound is still synthesized in pure Zag.

**Same planet, second imagining.** The world is Kethra from `PLANETVOICE.md`
(the D-IMG world: ringed super-Earth, argon atmosphere, shepherd moon
Ilyra, tectonic rift, glass-sand dunes, cryo deposits, magnetosphere
chorus). D-AUD-3 was the first imagining of its voice; this is the second,
with its ears opened by reality first.

## What was studied

Four public-domain field recordings (`SOURCES.md`; kept in
`aud/inspiration/`, never committed). Measured with numpy (spectrum,
envelope, transient analysis — `inspiration/study.py`, `study2.py`):

| # | Recording | Key measurement |
|---|---|---|
| 1 | Martian wind, Perseverance SuperCam (NASA) | **94.5% of energy below 120 Hz**, centroid ~50 Hz. Real alien wind is a deep buffet, not a hiss. |
| 2 | Martian dust devil, Perseverance SuperCam (NASA) | 81.9% below 120 Hz; the vortex passage = **fast attack, long asymmetric tail**, spectrum brightening at closest approach (centroid p95 1550 Hz). |
| 3 | Ice-crackle field | **425 transients/min**, median gap 75 ms, crack centroid med 1640 Hz (p5–p95: 34–4844 Hz), ~6 ms 1/e decay, crest 38. A dense, spiky, wide-brightness fracture language. |
| 4 | Storm thunderbolts | Rumble core **120–400 Hz holds 47% of energy**; sharp attack, multi-second low tail. |

Reference flatness (spectral flatness >0.30, the A-NOHARM metric): Mars
wind **0%**, ice crackling **0%**, dust devil 38%. Nature does not do 30%.

## Lineage trace: inspired element → what it became → what was invented

| # | Inspired element (source) | What it became on Kethra | What was invented (not from the source) |
|---|---|---|---|
| 1 | Mars wind's sub-120 Hz buffet (94.5% <120 Hz, centroid 50 Hz) | **Argon buffet**: very-low LP noise beds (55/140 Hz), the piece's foundation — deep, physical, breathing | The 18 s breathing period (Ilyra's tidal cycle), the argon atmosphere, the swell depth |
| 2 | Thunder's 120–400 Hz rumble core (47%) | **Thunder-core bed** (320 Hz LP) + **rift throat**: three deep booms (62/78/71 Hz), sharp attack, long tails | The tectonic rift as the cause; boom spacing on the tidal cycle |
| 3 | Dust devil's asymmetric envelope + spectral brightening | **Vortex passages** (`render_vortex`, new): 2-pole resonator whose center frequency *tracks* the envelope — dark-bright-dark, 250 ms attack, ~3 s tail | Charged glass-sand spirals that sing as they pass; the whistle is the vortex's own |
| 4 | Ice field's transient density/brightness/decay | **Fracture rain**: 144 micro-cracks in 4 cooling fronts (~410/min, the measured real rate), ~6 ms decays, 800–5000 Hz brightness spread, wide amplitude distribution (crest-like) | The cooling fronts (dusk shadows crossing crater fields); front timing and count |
| 5 | Dust devil's gesture (fast rise, bright peak, long tail) | **The voice** (`render_voice`, new): the magnetosphere chorus *reshaped* — rising chirps with asymmetric envelopes, 2nd-harmonic brightness tracking the envelope | The chorus identity itself (kept from the Kethra world: ring-particle/magnetosphere emissions) |
| 6 | Mars wind's missing hiss (0.000% energy >8 kHz) | **Deleted**: the white-noise bed and the 7 kHz HP shimmer bed. All HF in the piece comes from transient events, exactly as in the ice field (5.9% >8 kHz from transients alone) | — (a removal, per the A-NATIVE bar) |

## A-NATIVE: the new standing bar, and the honest bar table

Mid-build the lead set a new standing bar: **A-NATIVE** — no static, no
hiss bed, no lo-fi artifacts; clean native field-recording quality, the
way the inspiration recordings sound. This piece was reworked for it: the
white-noise bed and the HF shimmer bed were deleted outright, every burst
window was sized to let its decay complete (no mid-decay cutoff clicks),
and the result was verified by measurement (`native_check.py`):

- Noise-floor spectrum: 22.6 → −1.9 → −13.6 dB across 0.1–12 kHz — **natural fall**, not flat white
- Zero-crossing rate 0.054 (white noise ≈ 0.5; clean rumble < 0.15) — **no hiss**
- Crest 6.0, DC offset 0.00002, peak 0.679 (−3.4 dB headroom) — **healthy, no clipping, no DC**
- Loudest sample-to-sample jump 0.715 vs 1.198 in the real ice field recording — **within nature**

Final bars (2026-09-22):

| Bar | Threshold | D-AUD-4 (INSPIRED) |
|---|---|---|
| A-DUR | ≥20 s, 44.1 kHz, mono, 16-bit | 21.000 s — PASS |
| A-EVOLVE | centroid std ≥400 Hz | 1208.5 Hz — PASS |
| A-SPEC | ≥2% energy above 8 kHz | 2.70% — PASS (transient energy only, zero hiss) |
| A-NOHARM | ≥30% frames flatness >0.30 | **0.00% — FAIL, honestly held** |
| A-NATIVE | native field-recording quality (measured) | PASS |
| A-DET | two clean reruns byte-identical | PASS (`865b02ec…40416` ×2) |

**On the A-NOHARM failure.** This is the exact tension the lead named when
setting A-NATIVE: the old pieces passed A-NOHARM by gaming it with
white-noise hiss beds. Real Mars wind scores 0% on this bar. Real ice
crackling scores 0%. A piece that sounds like a clean native recording of
an alien world *should* score near 0% — tonal winds, booms, and transients
are not spectrally flat. Per the lead's ruling the bar is reported, not
gamed; ears outrank bars. If A-NOHARM is to stay, it needs redesigning
against real field recordings, not against hiss.

## What it is NOT

Not a remix — no sample of any inspiration recording is in the piece (all
synthesis is hash-noise + resonators + partials in pure Zag). Not music:
no 12TET, no ADSR, no beat, no melody. The seven voice tones are events
with the dust devil's gesture, not notes. If it sounds deep and physical
rather than airy, that is the Mars wind talking.

## Files

- `d_aud4_inspired.wav` — the deliverable (21 s, 44.1 kHz, mono, 16-bit)
- `synth.zag` — generator (adds `render_vortex`, `render_voice`, `score_aud4`; aud1–aud3 untouched, still byte-identical)
- `native_check.py` — A-NATIVE verifier (numpy; never generates audio)
- `INSPIRED.md` — this file; `SOURCES.md` — the inspiration set
- `aud/inspiration/` — the four PD recordings + study scripts (local working material, **never committed**)
