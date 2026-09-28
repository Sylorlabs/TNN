# Round 8A report — Fork A: one sun, deliberated (D-IMG-1)

Date: 2026-09-22. Base: `r6_alien.zag` (Micah judged R6 more realistic
than R7, so Fork A starts from R6, not R7). Method: explicit sun
deliberation first, then one-sun enforcement plus qualitative craft
fixes BY EYE against the converged tell list. No blind judging in this
crew — that is the separate crew's gate.

## Deliverables

- `img/r8a_alien.zag` — pure-Zag canonical generator (no RNG anywhere)
- `img/r8a_alien_1024.bmp` — 1024×1024 24-bit canonical artifact
- `img/r8a_alien_1024.png` — lossless Python re-encode, preview only
- `img/ROUND8A_REPORT.md` — this file

## The sun deliberation (committed in-source, not fitted)

Micah's note: shadows point in strange, unrealistic directions. The
header of `r8a_alien.zag` records the deliberation that replaced three
private suns with one:

- The old generator claimed one sun but used three incompatible
  vectors: moon `(-560,+720,+430)`, planet/rocks `(-880,-260,+390)`,
  and separately hand-tuned cast-shadow geometry `(94,34)`. That is the
  "faces weirdly" defect, diagnosed, not guessed.
- High noon rejected (flat, moodless); a visible sun disc rejected
  (competes with the giant planet); chosen: a low sun just past the
  LEFT horizon at 9° elevation — dusk mood, long dramatic shadows.
- One shared vector `(sunx,suny,sunz) = (-970,-160,230)`, |S| ≈ 1010,
  exposed as `r8a_sunx()/r8a_suny()/r8a_sunz()` so no element can
  drift. Direct light amber `(255,190,130)`; shadows filled by cool
  skylight `(96,124,168)`; ambient floor 300 in the mountain diffuse.
- Ground-shadow azimuth `(shdx,shdy) = (97,16)` = −S_horizontal;
  boulder shadow length 4.9 radii = height/tan(9°) for a dome ~0.78
  radii tall. Pebble shadow length 5 radii likewise.

## What changed and why (per converged tell)

**1. Inconsistent lighting — root-caused.** Every element now derives
from the deliberated vector: moon phase/terminator, planet terminator
and storm relief, mountain diffuse (true normal·sun, see 2), boulder
dome shading, rock/pebble cast shadows, bank highlight on the
riverbed's sunward side. No per-element light constants remain
(grep-verified; the only integer sun literals live in the three
accessor functions).

**2. Pinstripe mountains — root-caused to the integer, not the
baseline.** Round 4 blamed the ±6px baseline; round 6 widened it to
±24px and the bands survived, softer. A numeric port of the lighting
showed the deeper defect: the gradient was truncated to an INTEGER
slope, and each integer step swung the sun-dot by the full 970
x-component — the bands were quantization cliffs, not creases. Fix:
fractional slope (raw heightfield difference, in 48ths) dotted as a
true diffuse `(g·Sx − Sy)/(|N|·|S|)` with cool-sky ambient floor. The
spire now falls off smoothly, lit flank facing the deliberated sun.
While there, a sign error was caught by eye (lit/dark flanks swapped)
and corrected against the normal derivation in the comments. Mid hills:
the 1D ridge was additionally removed from the *lighting* profile
(silhouette keeps the crags) — lighting x-columns had printed a
"picket fence"; the 2D gully field carries erosion detail instead.

**3. Contour-map strata.** Strata are now broken lenses: heavy warp,
irregular spacing, and a patch mask, so no stratum runs continuously —
plus a 2D mottle that is the primary wear texture. The topographic-map
rings on the spire are gone.

**4. Pasted planet glow-blob.** The storm is now weather, not a lamp:
it samples the same zonal flow field as its surroundings and tints
warm, with a wide soft rim dissolving into the flow and only a faint
parting where the flow bends (the dark moat was thinned to a whisper).
Terminator and storm relief use the deliberated sun; the night side
keeps limb glow instead of going featureless black.

**5. Flat-disc moon.** Broad maria, a crater field with sunlit rims
tied to the same phase/light, and a foreground cirrus veil drawn AFTER
the moon and planet — atmosphere between viewer and sky, so the moon
is no longer a disc pasted on a backdrop.

**6. Sticker rocks / halo rims.** Contact darkening now fires only on
the shadow side (dot with the shadow azimuth), tighter and softer —
no halo ring all the way around. Cast shadows use the derived
`(97,16)` azimuth and 4.9-radii length, replacing the hand-tuned
`(94,34)` geometry.

**7. Stamped pebble dashes.** Two grids at different scales, density
falling toward the horizon (perspective), elliptical stones (no two
share an outline), some half-buried with only the crown showing, dust-
covered pale variants — shadows along the deliberated azimuth.

**8. Diorama composition / detail-poor foreground.** A ghost ridge
behind the far range (one more hazed depth plane); a dry riverbed
winding from the foreground toward the hills, widening with
perspective, smooth dark bed, sunward bank highlight — compositional
intent, not decoration. Foreground grit settles out inside the channel.

## Frozen bars (PREREG.md)

| Bar | Result |
|---|---|
| D-RES 1024×1024 24-bit | PASS |
| D-SHARP ≥ 1.20 | PASS — grad(O)=3.510, grad(B)=1.366, ratio=**2.570** |
| D-DET clean reruns byte-identical | PASS — 3 independent runs, sha256 `ebdb7eb9…b26861e54` ×3 |
| D-COMP anti-template audit | PASS for this file — zero banned tokens in executable code (4 comment mentions only); the directory-wide grep flags `var1_terminus.zag`, another fork's file, not this one |
| Pure Zag canonical path | PASS — Python only re-encodes/verifies |
| Zero randomness | PASS — integer hash noise, no RNG |
| No znc slice > 2^25 B | PASS — one ~3.15 MB RGB buffer |

SHA-256:
- `r8a_alien_1024.bmp`: `ebdb7eb98fe83c69c91cbb1dd20ddc0dfb50b70dcf5d37e92686321b26861e54`
- `r8a_alien_1024.png`: `de5de832e49699fec459b7d28db07eaa6d38e8c7fb8e49468952568cbe06d653`
- `r8a_alien.zag`: `fbf82eabc302c6e9736841d190b066bd34bd0971755a00371b0175dab402f98f`

Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`--no-zagd --no-analyze`); render ~7–29 s at 1024² (scene got heavier:
veil, ghost ridge, second pebble grid, riverbed). Binary emitted to
`/tmp` only; no binaries, `.zagd`, or `.zag-cache` committed.

## Iteration log (honest)

- Pass 1 (sun unification + storm/moon/shadow/pebble/riverbed/veil/
  ghost-ridge work): built clean first try; 3/3 identical. Eye check
  showed the spire still banded with HARD-edged stripes — worse-looking
  than r6's soft ones.
- Pass 2 (diagnosis): a Python port of the integer lighting math proved
  the bands were integer-slope quantization cliffs (each step swung the
  sun-dot by 970), not heightfield steps — an earlier wrong port had
  briefly blamed a nonexistent peak discontinuity, caught by reading
  the actual source. Fractional-slope true diffuse fixed the spire;
  sign error (flanks swapped) caught by eye and corrected.
- Pass 3 (mid-hill picket fence): the 1D ridge removed from the
  lighting profile; fence gone, 2D gullies carry the detail.
- Stopped here by eye — the remaining verticality reads as erosion,
  and further work risked the R5 over-working trap.

## Honest limitations

- D-BLIND is the separate judge crew's gate; nothing here claims
  aesthetic success, only that the converged tells were addressed and
  the sun is now one, deliberated, and enforced.
- Rock crack patterns remain ridge-noise, not stress-fracture
  geometry (inherited).
- The riverbed and veil are deliberately subtle; a judge may miss
  them entirely.
- 2048² untested (prereg minimum is 1024²).

## Reproduce

```
cd imagination_discovery/img
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 r8a_alien.zag --no-zagd --no-analyze -o /tmp/r8a_alien
/tmp/r8a_alien /tmp/r8aout 1024
python3 verify_bars.py /tmp/r8aout/r8a_alien_1024.bmp
```
