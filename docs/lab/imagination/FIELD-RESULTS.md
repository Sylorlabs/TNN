# FIELD-TRACK RESULTS — 2026-09-22

Third substrate in the exposure-vs-mechanism test: v1 elements vs v2 rich
elements vs **fields** (continuous per-point visual values, per-time-frequency
audio energy+brightness, heightfield structure). Preregs:
`PREREG-amendment-2026-09-22-fields.md` and
`PREREG-amendment-2026-09-22-generative.md` (frozen before measurement).

## Implementation

`src/field.zag` → `src/field_bin` (separate binary; `imagine.zag` untouched).
Built with `toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
--no-foreground-cache`: **196,206 bytes** native main, **0 external tools**.
Pure Zag, zero RNG (texture = deterministic coordinate hash).

- VISUAL: 24×24 grid × (r,g,b,roughness). Strokes: fill, v/h-gradients,
  blotches, soft bands, soft rects, dither.
- AUDIO: 48 frames × 48 semitone bins (110·2^(b/12) Hz), energy + brightness
  cells. Strokes: tones (ADSR), sweeps, broadband noise, harmonic stacks.
- STRUCTURAL: 24×24 heightfield. Strokes: ground plane, boxes, domes.
- Modeless by design (one builder per brief). Max 64 strokes/scene.

## Pure-TNN generation mandate (Micah, 2026-09-22)

Every shipped image, WAV, and video byte is emitted by Zag itself:

- `f3_emit_bmp` — 14 BMPs (briefs 1–6, novels 11–18) via integer-bilinear
  visual / heat-ramp spectrogram / hillshaded relief rasterizers.
- `f3_emit_avi` — 2 audiovisual AVIs: RIFF headers, 24 keyframe-interpolated
  frames, interleaved PCM audio, idx1 index, all byte-written by Zag.
- `f3_emit_wav` — 8 WAVs (brief audio, novels 15/16, song, unheard, video
  soundtracks).
- Python renders are **harness-only** (independent byte-compare /
  reimplementation checks); they no longer ship. Old Python PNGs retired to
  `harness_png_superseded/`.

Independent verification: `crosscheck_raster.py` reimplements the integer
raster rules in Python and byte-compares all 14 BMPs + all 48 AVI video frames
against field dumps → **CROSSCHECK PASS** (two independent implementations,
byte-identical). An independent RIFF/AVI parser confirms both videos: valid
RIFF size, avih (24 frames, 2 streams, 240×240), 24 video + 24 audio chunks,
48 valid idx1 entries; embedded audio byte-identical to sibling WAV PCM
(52,800/52,800 bytes each). ffprobe (verifier only): rawvideo 240×240 8fps,
pcm_s16le, 3.000000 s.

## M1f — detail density (pooled, brightness counted where populated)

| Track | Scenes | Units | Populated attrs/unit | Units/scene |
|---|---|---|---|---|
| v1 elements | 12 | 46 el | 3.80 | 3.8 |
| v2 elements | 12 | 58 el | 5.86 | 4.8 |
| field strokes | 6 | 32 st | 5.38 | 5.3 |

Raw: v1 175/46, v2 340/58, f3 172/32. Field leads on units/scene, trails v2
on params/unit. H2 needs field ≥ v2 on both → **M1f does not cleanly support H2**.

## M2f — novel combinations: 32/32 (bar ≥24/32) PASS

8 novels × 4 concepts (generative prereg extends the original 6×4):

| Novel | Concepts (all pass) |
|---|---|
| N11 glass staircase underwater at dusk | dusk sky, ≥4 steps, underwater blue, glass highlights |
| N12 brass band in library, zero-G | ≥3 shelves, ≥3 figures, floating heights, brass colors |
| N13 thunderstorm in honey cathedral | dark storm wash, amber tones, lightning streaks, glow |
| N14 robot drinking tea on glacier at sunrise | sunrise, glacier ice, robot body, tea accent |
| N15 thunderstorm + distant church bell | thunder sweep, ≥2 bell tones, distant energy, decay |
| N16 music-box lullaby + rain | high register, ≥3 melody tones, ≥4 rain noise strokes, soft |
| N17 **entire short song** | melody contour 27→36 bins, bass line, kick+hat rhythm, pad harmony, full 40-frame span |
| N18 **unheard sound** | inharmonic partials {20,26,33}, crossing sweeps, noise wash, ×3 alien pulse |

Mechanically scored on stroke params + grid stats.

## GEN bars

| Bar | Score | Bar | Verdict |
|---|---|---|---|
| GEN-1f brief compliance | 12/12 | ≥10 | PASS |
| GEN-2f raw-continuous (no label vocab) | 12/12 | 12 | PASS |
| GEN-3f probes vs dump | 24/24 | ≥20 | PASS |
| Native artifacts (14 BMP + 2 AVI + 8 WAV parsed) | clean | 0 errors | PASS |

## Generative audio probes (N17, N18)

| File | Content |
|---|---|
| `f3song.wav` | Entire short song: melody (C5 E5 G5 A5 C6 A5 G5 E5 C5) + bass (C2 F2 G2 C2) + pad + kick ×5 + hats ×5, 3 s miniature |
| `f3unheard.wav` | Unheard sound: inharmonic partials (irrational-ish ratios), rising+falling sweeps crossing, noise wash, ×3 alien pulse |

**Honest caveat (unresolved):** synthesis maps field bins through a fixed
sine-LUT additive harmonic stack. Native Zag generates every sample, but this
may violate Micah's literal "no hardcoding sines" instruction. Do not claim
fully-generative-audio success until a non-fixed-waveform alternative is tested
head-to-head and Micah's ear judges both files. Mechanical bars pass; the ear
judgment is binding and still pending.

## Audiovisual scenes (native Zag AVI)

| File | Content |
|---|---|
| `f3vid1.avi` | Glacier sunrise: 4 native keyframes → 24 frames @ 8fps, wind + ice-chime soundtrack (4,201,484 bytes) |
| `f3vid2.avi` | City of bells at night: 4 native keyframes → 24 frames, bell + night-noise soundtrack (4,201,484 bytes) |

Both re-emitted byte-identical across runs. Location:
`~/workspace/your_files/imagination_video/`.

## Determinism + regression

- 5× `f3dump all` / `f3novel` byte-identical; 2× `f3wav`/`f3vidwav`/`f3bmp`/
  `f3avi` byte-identical (26/26 artifacts); raster crosscheck PASS. PASS
- M4: `q1 m/h all`, `q1v m/h all` via imagine_bin_v2 byte-identical to
  SHA256SUMS. PASS (field binary is separate; v1/v2 code untouched)

## M3f — blind ratings: PENDING

Three-way blind packet rebuilt: `~/workspace/your_files/imagination_fields/packet/`
(`blind_packet.html`, key in `blind_key.txt` — do not open before rating).
22 blind items with Zag-native field BMPs (v1/v2 images still Python-rendered,
pending their native re-render — noted in-packet), plus field-only sections:
8 novel probes (incl. song + unheard sound), 2 audiovisual scenes.
Needs Micah's ratings.

## H2 verdict (interim)

- M1f: field ≥ v2 on units/scene only → does NOT support H2.
- M2f: 32/32 (v2's measured M2 pending from the v2 track) → supports H2 if v2 < 24.
- M3f: pending blind ratings.
- **Interim: H2 UNDECIDED** — needs M3f and the v2 M2 number. Fields are not
  obviously the wrong substrate (composition is strong), but they do not
  dominate element lists on construction-unit density.

## Where fields still fall short of human imagination

1. 24×24 visual grid is coarse — no fine detail, no text legibility.
2. Audio: 62.5 ms frames, mono, fixed-oscillator timbres — the sine-LUT
   caveat above stands; transients and stereo are absent.
3. Construction is still a discrete stroke list — the field is continuous but
   its authoring is not. The substrate question is not fully escaped.
4. Heightfield is 2.5D: no overhangs, no occlusion, no interiors.
5. Queries exist but no deliberate imagine→query→revise loop was exercised.
6. All builders were authored with metric knowledge — shared caveat across tracks.
7. Cross-modal binding is now partially addressed (video = visual + audio in
   one native container), but sight and sound are still imagined separately
   and laid together, not jointly.
