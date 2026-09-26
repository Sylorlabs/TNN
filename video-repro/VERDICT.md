# VERDICT — video native-reproduction test (NEW 2026-09-25)

Reference clip: Big Buck Bunny (2008), Blender Foundation, CC BY 3.0 —
24 frames, 320x240 @ 8fps, t=65.15s→68.15s (close-up, eyes open, smile forms,
ears shift). Source: `source/` (PROVENANCE.md; bbb_source.mp4 SHA-256
`ae51005850b0ff757fe60c3dd7a12d754d3cd2397d87d939b55235e457f97658`).
A hard target: sub-pixel fur, whisker pores, specular nose glint.

## Question
Can TNN natively reproduce a HIGH-QUALITY video it has seen, and how close does it get?

## Mechanism (pure Zag, zero RNG — `src/repro.zag`)
Deliberate-memory substrate: frames enter as raw bytes through TNN-side
ingestion and are committed as **memories with provenance**
(frame_id, row_id, episode). Reproduction goes through **deliberate recall**:
a content-addressed scan keyed on (frame,row) — not a pointer memcpy.
The byte-copy control lives outside the binary (plain `cp`).

Two native conditions:
- **native-verbatim** — full-resolution row memories (240 rows/frame).
  Asks: does the machinery preserve detail end to end?
- **native-encoded** — ingestion deliberately stores a 2x2-downsampled
  memory (160x120); recall upsamples nearest-neighbor. The ONLY loss is the
  documented ingest encoding, so the traces prove knowledge-vs-machinery
  attribution.

## Results (per-frame PSNR / SSIM vs original; full table in `metrics/metrics.csv`)

| condition       | PSNR (dB)            | SSIM               | frames |
|-----------------|----------------------|--------------------|--------|
| byte-copy (ceiling) | inf (all 24)     | 1.0000 (all 24)    | 24/24  |
| **native-verbatim** | **inf (all 24)** | **1.0000 (all 24)**| 24/24  |
| native-encoded  | mean 28.31 (min 28.19) | mean 0.9195 (min 0.9180) | 24/24 |
| floor (shape renderer) | mean 11.19 (min 11.09) | mean 0.5458 (min 0.5310) | 24/24 |

- **Native-verbatim TIES the byte-copy ceiling exactly**: PSNR inf and SSIM
  1.0000 on all 24 frames. The native memory/recall path is bit-lossless.
- **Native-encoded** (4:1 pixel reduction at ingest): 28.31 dB / 0.9195 —
  visibly softer on fur/foliage (2x2 block structure under 2x zoom) but fully
  recognizable: eyes, smile, ears, composition all survive.
- **Floor** (the old text-plan→shapes approach at 240x240, stretched to
  320x240): 11.19 dB / 0.5458 — a crude cartoon. This quantifies the gap
  Micah saw: ~17 dB and ~0.37 SSIM below even the lossy native path.

## Determinism
Every Zag binary ran twice; all outputs byte-identical or the result would
not count: ingest-verbatim PASS, recall-verbatim PASS, floor PASS
(`run_all.sh` summary: pass=3 fail=0).

## White-box diagnosis: WHERE does detail die? (knowledge vs machinery)
Stage hashes (FNV-1a/64, written by the Zag binary at each stage):
H_I = ingested bytes, H_S = stored memory payloads, H_R = recalled bytes,
H_E = emitted file bytes. Independently re-verified in Python over the
actual stage bytes — **146/146 checks pass** (`verify_traces.py`).

- **verbatim**: H_I == H_S == H_R on every frame (e.g. f=00:
  `e5c51c3a767056f8` at all three stages); stored payloads byte-equal the
  source pixels; recalled pixels byte-equal the source. **Nothing dies
  anywhere.** Knowledge capture is complete AND the machinery is lossless.
- **encoded**: H_S == FNV(python-2x2-downsample(source)) exactly, and
  H_R == H_S, emitted == upsample(stored). The trace proves the loss is
  **100% KNOWLEDGE** — detail never captured at ingestion (the deliberate
  2x2 encoding) — and **0% MACHINERY**: recall and emission are bit-exact
  on what was stored. The diagnostic discriminates: it catches a real
  knowledge loss and clears the machinery.

## Full-eyes judgment
Viewed full frames at full duration, side by side (gallery:
`~/workspace/your_files/video_repro_new/gallery_NEW.html`): native-verbatim
is indistinguishable from the original; native-encoded is softer with
visible 2x2 blocking under zoom but compositionally faithful; the floor is
a flat cartoon that gets "rabbit face" and nothing else.

## Plain-English answer: are we on the right track?
**Yes.** The deliberate-memory machinery reproduces a hard, high-detail
clip bit-for-bit — it ties the byte-copy ceiling, which means the
machinery is not the bottleneck; representational choice at ingestion is.
The old shape-renderer path scores 11.2 dB / 0.55 SSIM on the same clip
because its knowledge representation (coarse shapes from text plans) can't
hold fur-level detail — a knowledge failure, not a rendering accident.
The encoded path shows the honest middle: a 4:1 deliberate compression
still lands 28.3 dB / 0.92 SSIM with everything recognizable. The next
question is not "can the machinery carry detail" (answered: yes,
losslessly) but "what deliberate encoding gets closest per stored byte" —
a knowledge-design question, which is exactly where TNN's deliberation
should live.

## Honest limits
- The substrate here is minimal: provenance-keyed memories + deliberate
  recall. No strength dynamics (fidelity test, not strength test), no
  semantic encoding in the verbatim path — the verbatim path stores pixel
  rows, so its "knowledge" is raw detail, not understanding.
- Verbatim tying byte-copy is a machinery result, not an intelligence
  result: it proves the pipes don't leak, not that TNN "understands" video.
- The floor is a reimplementation of the old approach's representational
  level (text plan → flat shapes @240x240), not the original binary.

## Reproduce
`./run_all.sh source/frames` (ingest/recall verbatim+encoded, byte-copy,
floor, determinism) → `python3 verify_traces.py source/frames runs` →
`python3 metrics.py source/frames runs metrics/metrics.csv` →
`python3 deliver.py`. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
