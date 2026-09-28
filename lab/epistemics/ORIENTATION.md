# TNN Investigator Orientation

**For:** an outside investigator bot seeing TNN for the first time.
**Date:** 2026-09-26. **Live branch:** `tnn-native-lab` (all program work commits here; `main` is kept clean).
**Repo:** `sylorlabs/TNN`. Evidence lives under `docs/lab/<area>/` — each mature area has
`VERDICT.md` (the claim), `RUNLOG.md` (how it was run), and `evidence/` (measurements).

## What TNN is

TNN is a native AI program: pure Zag (a low-level systems language), zero randomness
anywhere in decision paths, byte-identical reruns. No LLMs in the loop, no tokenizer —
raw bytes in, raw bytes out. Standing laws: no arbitrary hard limits, deliberation over
memorization, human senses (Micah's eyes/ears) outrank metrics, exact replication gates
imagination.

## What is STALE — do not start here

- `R33_NATIVE_*` substrate files and anything "R33"-era: old crypto/IO substrate, superseded.
- Table machinery, HDE v1, prediction-advisory: dead, documented as dead.
- `docs/lab/wave*`, `htd-1`, `FINDINGS_2026-09-21.md`: historical batteries, not the live program.
- Pre-2026-09-24 design docs: check the date; the program moves fast and old docs are marked OLD.

## The five flagship lines (keep all alive) and where they stand

| Line | State 2026-09-26 | Look at |
|---|---|---|
| Image | ADOPTED production pipeline: adaptive-layers + adaptive-magnification, 46.35 dB / 0.9955 SSIM, exact closure, byte-identical | `docs/lab/image_production/` (live), `docs/lab/image_adaptivelayers/` (evidence), `docs/lab/image_upscale/` (honest negative: loses to bicubic 21.96 vs 25.89 dB — forced-take diagnosis, reject option in progress) |
| Audio | 359/359 sealed WAVs byte-identical; planner/vocabulary loop PARTIAL PASS (mean error −29%/−44%, per-case bars fail — red team in progress); untrained-analysis repair ADOPTED (0 hallucinations, binding confirmatory PASS) | `docs/lab/audio_longhorizon/`, `docs/lab/untrained/`, `docs/lab/exact_audio_replication/` |
| Text | Learned adaptive chunker in production (26/26 wall, 57/57 production, 41-case degenerate battery, zero panics) | `docs/lab/mg_chunking_batteryfix/`, `docs/lab/mg_chunking_promote/` |
| Video | AMBIG clip program; fusion fork B (H1d) perception PERFECTED 24/24 both series; re-render fix path is the current wall | `docs/lab/fusion-forkb/`, `docs/lab/ambig_clips/` |
| Memory/governance | Immediate-121 adopted into strength core (cite on tombstoned episodes returns 121; precedence 121>111>122) | `docs/lab/strength/`, `docs/lab/strength-destruction-pricing-adoption/` |

## Recently adopted (settled, don't re-litigate without new evidence)

- Immediate-121 Variant A (commit `45f655a5a226`)
- Adaptive image pipeline to production (commit `e6f805ed4ca3`)
- Untrained-analysis repair + binding PASS (commits `022b8c53a8`, seal `66749134f1`, verdict `f5288bc6c9`)
- Fork B perception: saturation material gate (commit `01794343ed54`)
- Chunking battery fix + panic hardening (commits `d496120c9db7`, `7cc8bbe175aa`)

## Open walls (live work, 2026-09-26)

1. **Upscale rectangles** — TNN's 2x upscale shows block/rectangle artifacts; forced-take at the top
   level is the diagnosed cause; a reject/split option ("no atom fits") is being implemented.
2. **H1 re-render** — perception sees the sticker 24/24 but the re-render loop never fixes it
   (`face_removed=0` every round); the fix path is being white-boxed.
3. **Pig-front teach-and-rerun** — TNN honestly marked an unseen pig face UNKNOWN; now being taught
   real front-view knowledge to test whether learning alone fills it in (Micah's hypothesis).
4. **Decoders** — FLAC stereo ✅ closed, progressive JPEG ✅ closed; MP3 partial (oracle validated,
   Zag incomplete); H.264 blocked at the slice parser.
5. **Audio semantic frontier** — past codec-style exact closure toward imagination-grade understanding.

## Falsified — do not revive without new evidence

- Edge/interior texture ratio and boundary step-direction consistency as graft discriminators
  (measured: no separation).
- Luma-only gate for graft detection (background foliage matches donor brightness).
- "TNN invents architecture from knowledge alone" (Task 1 rerun: 8/58 both arms; composition is
  the broken link, deliberation is real).

## Conventions for reading evidence

- Numbers in VERDICT.md are measured by the committed binaries, rerun byte-identically (×2).
- Sealed fixtures: SHA-256 committed before the run; check the seal timestamp precedes first output.
- "HONESTY DELIBERATION" prose in older verdicts may be crew-authored fixed wording — newer work
  discloses this; treat eloquent explanations as suspect unless the trace shows computed values.
- Galleries for Micah's eyes are self-contained (data URIs, zero external loads) under
  `~/workspace/your_files/` (not in the repo).
