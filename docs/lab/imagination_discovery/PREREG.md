# IMAGINATION DISCOVERY BATTERY — PREREG (frozen 2026-09-22)

Micah's bars (verbatim intent): images/video native HIGH RESOLUTION and SHARP —
no more 480×480 fuzzy era; composition is genuine generative control with detail
at every scale, NOT placed template primitives; audio has ZERO forced
instruments — full-spectrum control, more than a human with a DAW, not less;
trials are open-ended DISCOVERY ("I discovered some high-quality alien planet").
Judging is normal vision only — no horror prompting, no hardcoded horror
criteria (standing law). Micah's eyes/ears are the binding judge; blind judges
are the mechanical gate first.

## Battery subjects (5)

| ID | Modality | Subject |
|---|---|---|
| D-IMG-1 | image 1024²+ | Alien planet: surface vista of an extrasolar world, high detail at every scale |
| D-IMG-2 | image 1024²+ | Impossible architecture: a structure that could not exist, rendered coherently |
| D-AUD-1 | audio ≥20 s | Unheard instrument: a performance on an instrument that never existed |
| D-AUD-2 | audio ≥20 s | Impossible phenomenon: soundscape of an impossible natural event |
| D-VID-1 | video 1024², 48 fr | Alien ocean: moving liquid surface of an extrasolar sea |

## Kill bars — IMAGE (D-IMG-1, D-IMG-2)

- **D-RES**: output exactly ≥1024×1024 px, 24-bit. FAIL if smaller. (2048 allowed if the pipeline holds.)
- **D-SHARP** (self-calibrating, mechanical): let B = downscale(output,2×) then upscale(box,2×).
  Compute mean gradient magnitude on luma for output O and B. Require
  grad(O) ≥ 1.20 × grad(B). An upscaled-blurry render scores ≈1.0; genuine
  high-frequency detail scores above. FAIL below.
- **D-COMP** (anti-template, code audit): the discovery scene builders must
  contain ZERO axis-aligned filled-primitive placement calls
  (rect/band/blotch-as-object style composition). Verified by grep over the
  discovery generator source. FAIL if any found.
- **D-DET**: two clean-process reruns → SHA-256 identical. FAIL otherwise.
- **D-BLIND**: 5 fresh blind judges (know nothing of the pipeline), normal
  viewing criteria: ≥3 answer "would not guess AI" or "unsure", and none may
  name a template/blur tell unprompted.

## Kill bars — AUDIO (D-AUD-1, D-AUD-2)

- **A-DUR**: ≥20 s, 44.1 kHz, mono 16-bit. FAIL if shorter.
- **A-EVOLVE**: spectral centroid per 1-s window; require stddev ≥ 400 Hz
  across windows. A static sine-pad is near-constant; evolving timbre clears it.
- **A-SPEC**: ≥2% of total signal energy above 8 kHz. Proves full-spectrum use,
  no dull lowpass, no single-mellow-instrument.
- **A-NOHARM**: ≥30% of 1-s frames have spectral flatness > 0.30. A pure
  harmonic sine-stack sits near 0 — this bar kills the old failure mode
  mechanically.
- **A-DET**: two clean-process reruns → SHA-256 identical. FAIL otherwise.
- **A-BLIND**: 5 fresh blind listeners: ≥3 answer NO to "does this sound like a
  single instrument / keyboard preset?", and ≥3 describe ≥2 distinct timbral
  characters unprompted.

## Kill bars — VIDEO (D-VID-1)

- **V-RES**: 1024×1024, 48 frames. **V-SHARP**: D-SHARP applied to frames
  0/23/47. **V-TEMP**: mean abs consecutive-frame difference in [0.5%, 15%]
  of full scale — no frozen frames, no chaotic flicker. **V-DET**,
  **V-BLIND** as per image.

## Generation law

- 100% pure Zag in the deliverable path. External tools may VERIFY, never generate.
- Deterministic: identical input → byte-identical output. No RNG in any decision path.
- The 512×512 u4f field cap from the senses work does NOT apply: discovery
  renderers rasterize directly to pixel buffers (or tile fields) and document how.
- znc hard limits respected: no single slice > 2^25 bytes; sign-extending reads
  where sign matters; see ~/AGENTS.md.

## Verdict rule

Bars decide, not opinions. Any subject failing any bar is a FAIL — reported as
such, then iterated. A subject passing every mechanical bar goes to Micah's
eyes/ears as binding. Partial battery pass is reported per-subject, never
rounded up.
