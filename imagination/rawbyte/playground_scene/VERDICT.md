# VERDICT — PLAYGROUND SCENE (NEW, 2026-09-26)

TNN-native imagination, pure Zag, zero RNG. Ordered 2026-09-26 ~01:11 PDT for Micah's morning ear judgment.

## What TNN imagined, and why

TNN deliberated FIRST, in pure Zag (`deliberate.zag`), enumerating 1,296 scene
configurations over mood / ages / count / play-type / acoustic-space / duration
with seven explicit 0–2 criteria and deterministic argmax. Winner: index 820,
14/14. Full trace in `DELIBERATION_TRACE.txt`.

The scene: **lively midday, four children aged 3–6 in mixed free play, in a
small pocket park, 15 seconds.** TNN's recorded reasons:

- A small enclosed park keeps all voices in one consistent air (one world,
  one reverb, one distance law).
- Four children is the most distinct stable identities TNN can honestly make
  from two learned pitched voice models plus pitch scaling.
- Mixed free play (voices + ball bounces + metal clanks) gives simultaneous
  activity, not a sequence.
- Swings were REJECTED: there is no learned swing-creak fixture, and TNN will
  not fake one.
- 15 seconds allows overlap while limiting repetition from the small voice
  inventory.

## What was rendered

`scene.zag` (pure Zag, 44.1 kHz / 16-bit mono) renders the scene as ONE mix:

- **Four stable child identities**, constant for the whole scene:
  - child 0 — cry model @345 Hz, 3.5 m
  - child 1 — vowel model ×1.15 @365 Hz, 5.5 m
  - child 2 — cry model ×0.90 @310 Hz, 4.5 m
  - child 3 — vowel model ×1.25 @396 Hz, 7.0 m
  (Pitch scaling replays the learned harmonic waveform at a different phase
  rate — formants preserved, verified 344.5→445.5/293.0 Hz on the cry model.)
- **16 voice phrases, interleaved** (each child vocalizes across the whole
  15 s, ~1.7 voices active on average), deterministic fmix32 staging, never
  RNG. A polyphony repair nudges any phrase that would start inside another
  child's phrase (3 repairs this run) — no phrase is ever cut mid-cry.
- **Textures**: 3 ball-bounce trains (strike model), 3 metal clanks (clang
  model), 2 soft thuds.
- **One air**: shared distance gain + air low-pass, shared early reflections
  (11/29/53 ms), and one low non-tonal air bed (−33 dB rel mix).
- Voice loudness compensation: the learned cry voice is ~4× the RMS of the
  learned vowel voice; without a 4× staging gain on vowel events the two
  vowel children sit 12 dB under and the deliberated 4-child scene collapses
  to 2 audible voices. This is a placement gain, not a voice change.
- `playground_scene_nobed.wav` is the identical mix with the bed muted, for
  masking diagnosis (cf. the 2026-09-24 bed-fusion lesson).

## Measurements (analyzer-first)

Baselines for comparison: cry_3s (F0 344.5 Hz, HNR +2.7..+7.4 dB),
vowel_3s (F0 317.3 Hz, HNR +2.1..+5.9 dB), strike/clang (unvoiced, noisy HNR).

Scene (`playground_scene.wav`, bed version):

- 15.00 s, peak 10785/32768, RMS 1621 — no clipping, no normalization needed.
- Voiced F0 median 336.6 Hz; all four child pitch bands detected across the
  scene (windows dominant: 310 Hz ×245, 345 Hz ×166, 365 Hz ×75, 396 Hz ×112
  of 748 — the tracker credits one F0 per window during overlaps, so shared
  windows undercount).
- HNR alternates voiced-positive / unvoiced-negative blocks, as a mixed
  scene should (not one static harmonic stack).
- Spectral centroid drifts 1720–3716 Hz across blocks (moving voices and
  textures, not a frozen spectrum).
- Hum/tonal audit: 50/60/100/120/150/180 Hz all ≤0.03% — no mains hum, no
  tonal bed. The bed is non-tonal filtered noise.
- Continuity: 94.7% of 100 ms windows above −40 dBFS — one unbroken world,
  no dead gaps between "clips".
- Loop/regularity: envelope autocorrelation max 0.26 at 0.5 s lag; onset
  intervals median 0.06 s, min 0.02 s — no machine grid, no loop.
- Onset-boundary diagnostic: median spectral-centroid jump at the 16 voice
  onsets is 0.13 vs 0.04 at random points (real vocal onsets are noticeable),
  max 0.52 — inside the range of ordinary polyphonic moments (random max
  0.71). No hard-cut signature.
- Bed vs no-bed: bed-only RMS 34.9 (−33.3 dB rel mix); mix RMS differs by
  0.4 — the bed glues, it does not mask.

## Verdict: ONE SCENE, with a disclosed white-box gap

This is a single simultaneous scene, not fused clips: continuous energy,
overlapping voices throughout, one shared air (reflections + distance law +
bed), no silence gaps, no periodic loop, no tonal drone fusing the spectrum.

**Honest gap (white-box):** TNN owns only TWO learned pitched timbres (cry,
vowel). Children 0 & 2 share identical LPC formants (one at 345 Hz, one at
310 Hz); children 1 & 3 share the other's (365 Hz, 396 Hz). A careful ear may
hear "the same voice at two pitches" when a pair overlaps. This is a
knowledge ceiling — the voice inventory — not a staging trick, and it is why
TNN capped the scene at four children and fifteen seconds: more children or
more time would repeat the two timbres until the repetition itself became
the percept. The fix is a real one: learn more voice fixtures, not a
mixing trick.

Also note: the first staging pass grouped each child's phrases into a
sequential block (caught by the staging-report audit, fixed to interleaved
k×4+c before rendering the delivered files), and the first mix buried the
vowel children 12 dB down (fixed by the documented 4× staging gain). Both
are recorded here so the evidence trail is complete.

## Determinism (zero RNG)

- Renderer and deliberator are pure Zag; `grep` for rand/time/rdtsc/pid in
  `scene.zag` and `deliberate.zag` is clean (one comment mention only).
- `playground_scene.wav` rendered twice independently → byte-identical
  SHA-256: `8d7a0d923353220bb9d5e8376ab1648b81e8328d6651fda1121a470c4743317c`
- Deliberation rerun → identical winner (index 820, 14/14), byte-identical
  `DELIBERATION_TRACE.txt`.

## Files

- `playground_scene.wav` — the scene (bed version), 15 s
- `playground_scene_nobed.wav` — identical mix, bed muted (judgment variant)
- `VERDICT.md` — this file
- `DELIBERATION_TRACE.txt` — TNN's deliberation, byte-identical across reruns
- `STAGING_REPORT.txt` — deterministic event staging (36 events, 3 repairs)
- `SHA256SUMS` — hashes
- `index.html` — NEW-badged self-contained gallery (all WAVs as data URIs,
  zero external loads)

## Reproduction

Sources committed to branch `tnn-native-lab` under
`imagination/rawbyte/playground_scene/` (code + docs + evidence only; no
binaries, no WAVs, no model bins). Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
`deliberate.zag` regenerates the spec; `scene.zag` renders
(`./scene <models-dir> <out.wav> <bed 1|0>`).
