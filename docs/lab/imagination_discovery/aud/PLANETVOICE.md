# D-AUD-3 — PLANETVOICE: the sound OF the alien planet

**"If it's for the planet, then cool."** The first two discoveries were not
the planet's sound — Vespera is a tidal glass organ that never existed,
Cryovolcano is a methane-moon eruption. This one is different: TNN was asked
to imagine what the alien planet from the D-IMG image series *sounds like* —
its voice, not music, not an instrument, not a song.

## The imagined world: KETHRA

Kethra is a ringed super-Earth — the world in the round-4–7 images (lavender
sawtooth range, rust basalt plains, the great ringed disc hanging in the
dusk sky). The microphone stands on Kethra's surface; the ringed disc
overhead is Kethra's own ring system seen tilted from the ground.

- **Gravity 1.7 g, atmosphere 0.35 bar of argon-nitrogen.** Argon is heavy:
  low frequencies carry for kilometers, high frequencies die fast. The
  planet sounds *deep* — a world heard through a subwoofer.
- **Tidally flexed by the shepherd moon Ilyra** (the small flat moon in the
  images). Ilyra's pull breathes the crust: slow pressure swells roll across
  the plains on a ~18-second period, and the crust creeps and groans.
- **A tectonic rift** runs along the foot of the lavender range, venting
  warm gas in deep exhalations.
- **Glass-sand dunes** (the rust foreground of the images) sizzle and shift
  in the wind; **cryo deposits** in shadowed craters crack as dusk cools them.
- **A strong magnetosphere** threads the ring plane. Charged ring particles
  excite **chorus emissions** — rising tones, the same physics as Earth's
  dawn chorus, transposed to an alien ring system. This is the planet's
  *voice proper*: not a creature calling, the magnetosphere itself singing.

## Where the microphone stands

On a basalt slab at the edge of the glass-sand dunes, at the foot of the
lavender range, at dusk. Behind it the rift vents; above it Ilyra climbs;
overhead the ring plane arcs. The mic does not move for 21 seconds. The
planet performs around it.

## Every sound, derived from the world

| # | What you hear | What it is on Kethra | How it's synthesized |
|---|---|---|---|
| 1 | Deep planetary hum, slow beating | Argon-atmosphere standing waves; two cavity modes 0.45 Hz apart beat against each other | Beating struck pair 33.0/33.45 Hz + 66.2 Hz octave, full-span swell |
| 2 | Slow pressure breathing, ~18 s period | Ilyra's tidal pull squeezing the thin atmosphere | LP noise beds (110/260 Hz) with 0.055 Hz LFO swell — "moon-breath" |
| 3 | Constant rushing band | Wind forced through the sawtooth ridgeline | Swept 2-pole resonator 280→950 Hz on noise, full span |
| 4 | Thin wandering whistle | Wind over the tall central spire | Narrow wandering resonator 1500→2350 Hz, low gain |
| 5 | Four rising gusts | Wind surging through the foothills | Broad swept-resonator whooshes (R=0.97, breathy not tonal) |
| 6 | Three deep exhalations | The tectonic rift venting gas | Deep swept vents 150→2400 Hz + low noise burst |
| 7 | Three seismic groans | Crust creeping under tidal flex | Slow-swell low struck partials 58/64/72 Hz |
| 8 | Eighteen ice cracks | Cryo deposits fracturing as dusk cools the craters | Noise bursts + high pings, sparse, golden-walk timing |
| 9 | Nine rising tones, mid-piece | **Magnetosphere/ring-particle chorus — the voice** | Exponential-rising chirps 1100→3400 Hz, sine + soft 2nd harmonic. Events, not notes: no melody, no rhythm |
| 10 | Air, shimmer, hiss bed | Argon wind on the mic diaphragm; glass-sand sizzle | HP noise 5600 Hz + white-noise bed |

## What it is NOT

Not music. Not an instrument — there is no `f3_tone` stack, no ADSR, no
12TET, no scale, no beat anywhere in the piece. The nine chorus tones are
*events*: they do not repeat, they do not form a phrase, they rise and die
like something in the sky clearing its throat. If it sounds "windy, like a
riser," that's honest — it *is* wind, on a world with 1.7 g and argon air.

## Can TNN imagine variations?

Yes — and this piece is the proof of the mechanism, not just one lucky
render. Every element is parameterized from the world description, not from
a preset: change the planet (thicker atmosphere → raise the LP cutoffs and
slow the moon-breath; no rings → delete the chorus; fiercer tectonics →
more groans, deeper vents) and the same generator speaks a different world.
The world comes first; the sound is derived. That is the whole method.

## Bars (2026-09-22, `bars.py`)

| Bar | Threshold | D-AUD-3 (PLANETVOICE) |
|---|---|---|
| A-DUR | ≥20 s, 44.1 kHz, mono, 16-bit | 21.000 s — PASS |
| A-EVOLVE | centroid std ≥400 Hz | 2755.6 Hz — PASS |
| A-SPEC | ≥2% energy above 8 kHz | 10.79% — PASS |
| A-NOHARM | ≥30% frames flatness >0.30 | 33.33% — PASS |
| A-DET | two clean reruns byte-identical | PASS (`7728fbee…0612c` ×2) |

Regression: `aud1` and `aud2` re-render byte-identical to the committed
deliverables after the `render_geyser` resonance-parameter refactor
(aud1 `0a07a35d…ffbbd6`, aud2 `29126cae…986d8bc` — both match README).

## Honest limitations

- A-NOHARM passed at 33.33% against a 30% bar — thin margin, honestly held.
  The piece is *supposed* to be tonal in places (the chorus is the voice);
  the bar and the art pull in opposite directions here, and the art won the
  close calls.
- The white-noise bed is prominent (it carries the flatness bar), same as
  the first two pieces — the mix is airy by construction.
- No blind listening by the builder. The lead's ears are the final judge.
- `synth3` is the build binary (kept out of the repo); `synth.zag` is the
  deliverable source. Rebuild: `znc synth.zag --no-zagd --no-analyze
  --no-foreground-cache -o synth3`, then `./synth3 aud3 d_aud3_planetvoice.wav`.

## Files

- `d_aud3_planetvoice.wav` — the deliverable (21 s, 44.1 kHz, mono, 16-bit)
- `synth.zag` — generator (adds `render_chorus` + `score_aud3`; `render_geyser`
  gained a resonance parameter, aud1/aud2 unaffected)
- `PLANETVOICE.md` — this file
