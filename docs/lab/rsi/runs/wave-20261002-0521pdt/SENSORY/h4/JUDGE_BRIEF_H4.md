# JUDGE_BRIEF_H4.md - SEALED BLIND A/B

## Provenance header (machine-checkable)

- RENDER_SHA: [TO BE FILLED - sha256 of the sealed 1024 variant BMP]
- FIRST_RENDERED_WAVE: wave-20261002-0521pdt
- COMPONENT_LINEAGE:
  - H1 LIT CLOUD DECK: JUDGED-DISCARDED (KB3 -2.13 vs >= 6.0, wrong sign)
  - H1v2: BUILD-FAIL (KB3 +0.64 vs >=3.0; KB9 2.36x vs <=2.0x)
  - H2v1: QUEUED-UNJUDGED (frozen prereg, not implemented)
  - H3 SUN-ANCHORED SKY-DOME: QUEUED-UNJUDGED (smoke renders only, no verdict)
  - E3 FILM GRAIN: JUDGED-REJECTED (Micah: grain added visible static)
  - H4 CLOUD SHADOWS ON TERRAIN: THIS CANDIDATE (new mechanism, new prereg)
- NEW_KNOWLEDGE_CLAIM: Terrain lit only by its own occlusion shadow looks
  floaty under a cloudy sky; sampling the visible cirrus field along the
  sun ray and attenuating the direct-sun term grounds the terrain under
  its clouds at zero new texture cost.

## The pair

- Two 1024x1024 renders, one BASELINE (frozen r11) and one H4 VARIANT.
- Randomized as LEFT/RIGHT; the mapping is sealed below.
- Both renders are fresh from wave-20261002-0521pdt (not recycled).

## What changed (for the judge's context, not to bias)

The variant adds cloud shadows on the terrain: where the visible cirrus
clouds block the sun, the terrain's direct sunlight is attenuated (up to
45%). The sky, moon, and clouds themselves are untouched. The effect is
subtle by design (dusk scene, strong ambient).

## Sealed mapping

[TO BE FILLED: LEFT=X, RIGHT=Y, sealed until Micah judges]

## Status

[ ] DRAFT - awaiting sealed 1024 renders
[ ] READY-FOR-JUDGE - pair prepared, mapping sealed, awaiting Micah
[ ] JUDGED - verdict recorded

---
*Micah is the sole judge. This brief does not present a verdict.*
*The skeptic's provenance probe: Is this a recycled render? No. Both*
*images are fresh 1024 renders from this wave (see RENDER_SHA). The*
*baseline is the frozen r11 (rebuilt byte-identical). The variant*
*implements the new H4 mechanism (frozen PREREG_SENSORY_H4.md).*
