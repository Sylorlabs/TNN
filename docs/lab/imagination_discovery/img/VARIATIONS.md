# VARIATIONS — can TNN imagine variations at all?

**Experiment:** one prompt, "alien planet". Three generators built from three
deliberately different world models. Not palette swaps: different physics,
different light logic, different composition, different subject.

**Frozen bars (from imagination_discovery/PREREG.md):** D-RES (1024x1024,
24-bit), D-SHARP (byte-identical reruns), D-COMP (pure Zag, zero RNG, zero
axis-aligned filled-primitive placement calls), D-DET, and D-BLIND (5 fresh
judges per image, "would you have guessed AI").

---

## Variation 1 — TERMINUS (`var1_terminus.zag`)

**The imagined world:** the surface of a tidally locked planet, standing on
the permanent terminator line. One side of the planet always faces its star
(scorched amber day), the other always faces away (frozen indigo night). The
terminator is a permanent storm wall.

**Deliberate world-model decisions:**
1. A huge dim red star sits permanently half-sunk on the western horizon —
   tidally locked means the sun never rises or sets.
2. The sky is a gradient between day-amber (west) and night-indigo (east),
   with the terminator line wobbling like weather, not a straight cut.
3. A permanent storm wall is pinned to the terminator: tall dark clouds with
   internal lightning and a lit rim.
4. Ground is scorched rock on the day side, frost on the night side, with
   frost sparkle where it is coldest.
5. **One western light source.** Every mesa, rock and ridge shadow is cast
   deliberately eastward. Long raking shadows. (Micah's critique of the old
   family was inconsistent shadow directions; this world has exactly one sun
   and the geometry is computed from it.)
6. Foreground mesas with warped strata, midground plain, background storm.

**Palette:** amber / rust / indigo. **Subject:** the terminator line itself.

---

## Variation 2 — SHEPHERD (`var2_shepherd.zag`)

**The imagined world:** standing on a small icy shepherd moon, looking up at
the ringed giant it orbits. The giant fills half the sky in crescent phase,
backlit by a pale sun. Geysers vent through the ice at your feet.

**Deliberate world-model decisions:**
1. **Composition is inverted from Variation 1:** the sky is the subject, the
   ground is the stage. (V1: horizon band world. V2: sky-dominant world.)
2. The giant is a crescent — backlit, because the sun is behind it from the
   viewer's position. Its night side is barely visible, lit only by
   moonshine. This is a phase computed from geometry, not a full disc pasted
   in the sky.
3. The ring is drawn as a real 3D annulus: the far half passes BEHIND the
   planet (occluded), the near half passes IN FRONT (occluding), with
   fine striations and the planet's own shadow cast across the ring.
4. One pale sun, off-frame upper-right. Ground shadows fall down-left.
   Ice ridges are lit from the right.
5. Foreground: cracked blue ice with pressure ridges, three geyser plumes,
   one tilted glowing ice slab with a soft shadow falling away from the sun.
6. Distant ice cliffs on the horizon — a different depth cue than V1's mesas.

**Palette:** cold blue / cream / rust. **Subject:** the giant and its ring.

---

## Variation 3 — EMBERFALL (`var3_emberfall.zag`)

**The imagined world:** a volcanic night world. There is NO sun. The ground
is black basalt split by a winding river of molten lava; glowing cracks vein
the plain; basalt boulders catch orange rim-light from the flows; embers rise
on the heat. Above it all the sky burns cold: three huge auroral curtains.

**Deliberate world-model decisions:**
1. **INVERTED LIGHT LOGIC vs both V1 and V2:** no sun at all. Light comes
   from BELOW (lava: warm, distance-falloff) and ABOVE (aurora: faint cool
   wash). Shadows are soft, short, and point AWAY from the nearest lava —
   every boulder's dark side faces away from the river.
2. The lava river is the compositional spine: it winds from the foreground
   to the horizon, leading the eye. Floating dark crust plates drift on the
   flow; the channel glows onto nearby basalt.
3. The aurorae are the sky subject: tall curtained draperies with vertical
   ray structure, green feet / teal mid / violet crowns, over a starfield.
4. The air is part of the world: rising embers with short trails, low ash
   haze, a smoldering red horizon of distant lava fields.

**Palette:** black-violet night, molten orange, aurora green/teal/violet.
**Subject:** the river of fire under curtains of cold light.

---

## Why these are variations, not palette swaps

| Axis | V1 Terminus | V2 Shepherd | V3 Emberfall |
|---|---|---|---|
| Light source | one low red sun, west | one pale sun, upper-right, off-frame | NO sun; lava below + aurora above |
| Sky subject | terminator storm wall | ringed giant in crescent | auroral curtains |
| Ground | scorched/frosted plain, mesas | cracked blue ice, ridges, geysers | black basalt, lava river, glowing cracks |
| Shadow logic | long, all east | short, down-left | soft, away from nearest lava |
| Composition | horizon-band landscape | sky-dominant, ground as stage | river-spine leading to horizon |
| Palette | amber/rust/indigo | ice-blue/cream/rust | black-violet/molten-orange/aurora-green |
| Depth cues | mesas -> plain -> storm | slab -> cliffs -> giant | boulders -> river -> glowing horizon |

## Technical notes (shared)

- Pure Zag, integer-hash value noise, fixed seeds, zero RNG.
- One shared lesson across all three, caught during the build: color channels
  must be CLAMPED after every additive step — unclamped adds wrap mod 256
  and print saturated artifacts. In V1 this produced a cyan disc (star-glow
  red channel wrapping 290->34), a yellow flame (frost-sparkle blue channel
  wrapping), and a green streak (storm-rim red channel wrapping 273->17).
  A `vN_addc`/`vN_clamp` discipline is now used after EVERY additive step in
  all three generators. Audit method: grep for unclamped `r = r +` patterns.
- 1024x1024, 24-bit BMP rendered natively, converted losslessly to PNG.
- D-COMP: no axis-aligned filled-primitive placement calls anywhere; all
  coverage is per-pixel analytic tests (distance-to-centerline,
  distance-to-curve, noise masks). No function or variable is named
  rect/band/blotch/fill/stroke/circle/ellipse.
- Determinism: each generator rerun byte-identically (SHA-256 recorded below).

## Rerun hashes (D-SHARP)

| Generator | Run 1 SHA-256 | Run 2 SHA-256 | Run 3 SHA-256 | Match |
|---|---|---|---|---|
| var1_terminus | 01b314f9dd191cf96f5665619e4c830045b5ff10e1a515d35db217539df77a0c | 01b314f9dd191cf96f5665619e4c830045b5ff10e1a515d35db217539df77a0c | 01b314f9dd191cf96f5665619e4c830045b5ff10e1a515d35db217539df77a0c | YES |
| var2_shepherd | 11942d9ef97368e7bb59d5116b4cb6f7eeea46459695500b24b3ff263aed7d54 | 11942d9ef97368e7bb59d5116b4cb6f7eeea46459695500b24b3ff263aed7d54 | 11942d9ef97368e7bb59d5116b4cb6f7eeea46459695500b24b3ff263aed7d54 | YES |
| var3_emberfall | 18bd75a57d04526cc16a74407e37966c52ff8f96ada6655e5b622df6f6d3b71e | 18bd75a57d04526cc16a74407e37966c52ff8f96ada6655e5b622df6f6d3b71e | 18bd75a57d04526cc16a74407e37966c52ff8f96ada6655e5b622df6f6d3b71e | YES |

All three generators rerun byte-identically across three clean processes.
D-SHARP: PASS. D-RES: PASS (1024x1024, 24-bit). D-COMP: PASS (pure Zag,
zero RNG, zero axis-aligned filled-primitive placement calls — the forbidden
names appear only in comments).

## D-BLIND results

Five fresh blind judges per image, normal vision. Question: "If someone
told you this was a real photograph of an alien planet, would you
believe them?"

| Image | J1 | J2 | J3 | J4 | J5 | Pass |
|---|---|---|---|---|---|---|
| var1_terminus | NO | NO | NO | NO | NO | 0/5 |
| var2_shepherd | NO | NO | NO | NO | NO | 0/5 |
| var3_emberfall | NO | NO | NO | NO | NO | 0/5 |

D-BLIND: FAIL for all three. Common tells cited: uniform noise-dot stars
with no brightness variation; procedural textures (sine bands, contour
lines, flat gradients); hard compositing seams; featureless gradient
spheres; no photographic texture, lens character, or coherent light
transport. The three world models ARE genuinely different (tidal
terminator vs ringed-giant moon vs volcanic aurora world), but all read
as synthetic renders.
