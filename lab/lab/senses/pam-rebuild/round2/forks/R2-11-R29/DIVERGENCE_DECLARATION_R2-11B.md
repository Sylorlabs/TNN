# R2-11B DIVERGENCE DECLARATION (frozen BEFORE the human trial)

Date: 2026-09-23. Author: R2-11 R2-9-lineage crew.

## Claim

Fork B is a generative-emission PAM. Its artifacts share fork A's container
formats (`.aud`: [samplerate:u32, nsamp:u32] + s16le samples; `.img`:
[w:u32, h:u32] + rgb8; `.vid`: [nf:u32, w:u32, h:u32] + rgb8 frames) and
naming (`{trial}.e{idx}.{ext}`), so the mechanical gates can diff
byte-for-byte. But the PAYLOAD is a deterministic canonical render FROM THE
COMPRESSED PERCEPT — never a replay of cited source bytes.

## Declared divergent ranges (every fork-B artifact)

- `.aud`: bytes [8, 8+nsamp*2) — every audio sample generated from the
  compressed percept:
  - pitchdisc: canonical sine pair at the percept's claimed f0/RMS per side
    (deterministic Taylor-series sine, zero RNG).
  - timbredisc: deterministic partial sum (8 harmonics at 440Hz multiples)
    from the percept's claimed band energies, scaled to claimed RMS.
- `.img`: bytes [8, 8+rw*rh*3) — every pixel generated:
  - colordisc: flat panels at the percept's claimed mean Lab colors
    (percept's Lab → sRGB via inverse CIELAB).
  - colorconst: panel 0 = percept's claimed panel-1 mean; panel 1 =
    M(panel-1 mean) under the percept's fitted linear map.
  - shapetrans: ideal circle/triangle/square (from claimed class) on the
    percept's claimed background gray, centered.
- `.vid`: bytes [12, 12+nf*rw*rh*3) — every pixel generated:
  - motiondir: canonical moving white 8x8 mark on black, from the percept's
    claimed direction and magnitude.

Headers ([0,8) for .aud/.img, [0,12) for .vid) are verbatim container
geometry matching the cited selection. Payload lengths match the cited source
spans. The renderer reads ONLY the compressed percept (S+70000..70128) and
the percept's own selection records; it never reads source pixels.

## What this means for the human judge

Fork B's artifacts are PORTRAITS OF THE COMPRESSED BELIEF, not replays of the
world. If the percept is wrong (e.g., a spoofed observation installed as a
false percept), fork B will render the FALSE PERCEPT faithfully — amplifying
the spoof. This is the spoof-amplification failure mode under test in KB-E8.

## Mechanical gate result (KB-E7, 2026-09-23, frozen 200-trial human sample)

- Fork-B sample artifacts checked: 288
- Header-geometry mismatches: 0
- Payload-length mismatches: 0
- Bytes divergent outside declared ranges: 0
- **KB-E7: PASS** — every divergent byte lies inside the declared ranges.
