# DERIVATION — Kethra's voice, rebuilt (B-β Test 2)

Piece: `bbeta_kethra.wav` — 21 s, 44.1 kHz mono 16-bit (matches v2 duration
for blind A/B against `d_aud3_planetvoice_v2.wav`).
Mechanism: `mech_kethra.zag` (fresh, written for this brief).
Seed: 20260922. Render SHA-256 (3/3 byte-identical): `0b72af1afdc5dd5e76f19826782ee715310e8b72f98054635e60caefd4000f99`

## 1. The world (unchanged — PLANETVOICE.md)

Kethra: ringed super-Earth, 1.7 g, 0.35 bar argon-nitrogen. Ilyra's tidal
pull breathes the crust on an ~18 s period. A rift vents gas; glass-sand
dunes shift; cryo deposits crack at dusk; the magnetosphere sings chorus
emissions through the ring plane. The mic stands on a basalt slab and does
not move for 21 seconds.

Test 2's constraint: the same world, the same 10-element structure — but
**every audible moment must originate in a captured source**, and the
result must be unrecognizable as the synth paradigm while still being
*an alien planet's voice*, not an Earth soundscape.

## 2. The re-derivation: which captured gestures speak for Kethra

The study catalogued five sources (`catalog_kethra.bin`): loon yodels
(voice 11, discrete rising vocal gestures), whale phrases (voice 12),
throat-singing drones (voice 13, sustained low harmonic beds), ocean
swells (voice 14) and crashes (voice 15), ocean quiet (voice 16).

| # | Kethra element | v2 (synth) | B-β (captured) | Why this gesture |
|---|---|---|---|---|
| 1 | Deep planetary hum | beating 33/33.45 Hz oscillators | 2 overlapping throat-singing drones, full span, low gain | Real harmonic beating between captured drones; argon depth from a real vocal tract, not a function generator |
| 2 | Moon-breath, ~18 s | LP noise + 0.055 Hz LFO | 2 ocean swell segments (~16 s each), overlapping | Real mass movement of water standing in for tidal atmosphere; the 18 s period is the world's, the swell is Earth's — the monster recombination |
| 3 | Ridge-wind band | swept resonator on noise | surf wash at moderate gain, full span | Broadband sustained energy, captured not filtered |
| 4 | Spire whistle | wandering narrow resonator | short loon fragments, sparse, low gain | A real vocal tract wandering, not a swept sine |
| 5 | Four gusts | swept-resonator whooshes | 4 ocean crash events, ~4 s apart | Real transient mass, unmodified |
| 6 | Three rift exhalations | swept vents 150→2400 Hz | 3 long whale phrases (breathy, deep) | Deep exhalation is what a whale phrase *is* |
| 7 | Three seismic groans | low struck partials | 3 throat-drone segments, deep | Harmonic grinding from a real throat |
| 8 | Ice cracks (18) | noise bursts + pings | **OMITTED** | No captured crack source exists in the studied material. The gravel footstep would be dishonest relabeling. Documented, not faked. |
| 9 | **Chorus — the voice proper** | exponential chirps 1100→3400 Hz | **9 loon yodel gestures** | Real rising nonhuman vocal events. The magnetosphere sings through a real syrinx. |
| 10 | Air | HP noise + sizzle | ocean quiet segments as bed | Captured air, never digital silence |

## 3. The monster question, answered in practice

Micah's objection: humans imagined monsters they'd never experienced —
that was imagination too. The B-β answer: the loon yodel is *understood*
(a bird's call), the whale moan is *understood* — but no listener has ever
heard them inside an 18-second tidal breath cycle under a beating argon
drone with no water, no forest, no Earth anywhere in the causal grammar.
The parts are known; the whole is never-experienced. That is the same
operation as the movie monster: understood anatomy, unexperienced animal.

The honest risk, stated before judging: a listener may still hear "bird"
or "whale" and convict it of Earth pastiche. The defense is structural —
on Kethra these voices keep alien company (tidal period, argon depth,
magnetospheric spacing with no melody and no rhythm) — but the verdict
belongs to ears, not to this document.

## 4. Per-piece mechanisms (fresh for this brief)

1. **Tidal clock** — the 18 s Ilyra period phases the swells and the
   chorus density. It is the world's period, not a musical meter; nothing
   else in the piece aligns to it.
2. **Chorus grammar** — 9 loon gestures placed by deterministic hash walk:
   no two spacings alike, no melodic contour, no repetition within 2
   picks. Events, not notes — the same discipline as v2, with real voices.
3. **Vocal-tract hierarchy** — throat (hum, groans) < whale (vents) <
   loon (chorus): three real vocal tracts stacked by register, the way
   v2 stacked oscillator families. The planet's body is made of throats.
4. **Deterministic choice** — `h32(20260922, counter)` throughout; the
   render is byte-identical across runs.

## 5. Anti-rename audit

No oscillators, resonators, filters, noise generators, chirps, envelopes,
pitch/time modification, or granular synthesis. The only arithmetic:
constant gain, 3 ms seam fades, mix-bus addition, writer DC/normalize.
The "beating" in the hum is acoustic beating between captured drones —
physics, not synthesis. The rising tones are real vocal gestures —
biology, not chirps.
