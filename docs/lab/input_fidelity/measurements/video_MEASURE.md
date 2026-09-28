# MEASURE.md — Video modality, input-fidelity battery (overnight)

**Date:** 2026-09-27 · **Worker:** video measurement · **Prereg:** `docs/lab/input_fidelity/PREREG.md` (frozen, 5b661730)
**Bar:** B5 — NO BAR. Capability gap reported honestly.
**Toolchain:** pinned `znc_linux_x86_64_abed8aa1`, pure Zag, zero RNG.
**Sources:** committed only, extracted via `git archive origin/tnn-native-lab` (dirty worktree NOT used).

## Fixture integrity

| Fixture | Sealed SHA-256 | Measured SHA-256 | Match |
|---|---|---|---|
| `fixtures/t.mp4` (61,004 bytes) | `424f5cc71018a007…` | `424f5cc71018a007bb23c4441e9b9e2cf82089a1a8066ee881bd51f8e023cfb9` | ✅ |

## 1. MP4 container parse — PASS (reproduced exactly)

Rebuilt committed `src/mp4.zag` (SHA `69870756…` per manifest) with the pinned toolchain, ran on the sealed fixture:

```
moov found / stbl found / stsz count 8 / total sample bytes 60112 / extracted 8 samples / ok
```

- Output: 60,112 bytes of sample payload, SHA-256 `486056756ba17b8653279b6f14053fe3eed8d9ffebce395486e703f4606e94d5`
- Two independent runs: byte-identical SHA → deterministic ✅
- **Committed claim verified:** 8 samples extracted ✅

NAL-unit enumeration of the 60,112 output bytes (4-byte BE length prefixes):

| NAL type | Count | Sizes (bytes) | Meaning |
|---|---|---|---|
| 6 | 1 | 621 | SEI |
| 1 | 1 | 7,082 | non-IDR (P) slice |
| 5 | 7 | 7,369 / 7,458 / 7,807 / 7,434 / 7,538 / 7,258 / 7,509 | IDR slices |

9 NAL units total, all length fields well-formed, all type bytes sane. ⚠️ Honest caveat:
the committed `mp4.zag` itself does **not** validate NAL structure — it copies sample
byte ranges wholesale. The enumeration above was done with an external script; the
"NAL units validated" part of the committed claim is crew analysis, not parser output.
SPS/PPS do **not** appear in the sample stream — they live in the `avcC` box in `stsd`,
which `mp4.zag` locates (`avcc_off`/`avcc_len`) but never emits.

## 2. H.264 SPS parse — PASS (reproduced exactly)

SPS extracted from `avcC` (byte 0 of avcC content: `01`, profile `0x42` = 66,
level `0x0b` = 11; SPS NAL = 23 bytes starting `67 42 c0 0b d9 01 41 fa …`).
Fed to rebuilt committed `src/sps.zag`:

```
profile 66 level 11 seq_id 0
width 320 height 240
BLOCKER: CAVLC/intra/inter/deblocking not implemented
```

- **Committed claim verified:** 320×240 Baseline (profile 66) ✅
- Note: `sps.zag` does not strip emulation-prevention bytes (documented in-source);
  on this fixture the parse lands identically with and without unescaping — verified
  both ways above. A hostile SPS with `00 00 03` in a sensitive field position could
  misparse; out of scope, flagged for the record.

## 3. Where slice decode stops — the precise blockage

The committed binary's own last line names it. Stage-by-stage audit of the
**committed Zag** sources:

| Stage | Exists in committed Zag? | State |
|---|---|---|
| MP4 box parse → sample extraction | YES (`mp4.zag`, 225 lines) | ✅ working, measured |
| NAL length demux | NO (byte copy only) | ⚠️ done externally |
| avcC SPS/PPS emission | NO (located, not emitted) | ⚠️ done externally |
| SPS Exp-Golomb parse | YES (`sps.zag`, 134 lines) | ✅ working, measured |
| PPS parse | NO | absent |
| Slice header decode | NO | absent |
| **CAVLC residual decode** | NO | **absent — the blocker** |
| Dequant + inverse 4×4 transform | NO | absent |
| Intra 4×4/16×16 + chroma prediction | NO | absent |
| Inter P-frame motion compensation | NO | absent |
| Deblocking filter | NO | absent |

What exists beyond SPS is a **Python prototype**, not TNN machinery:
`h264/ref/h264ref.py` (839 lines) + `recon.py` (427 lines) — SPS/PPS parse,
slice-header parse, CAVLC with nC neighbor derivation, MB-layer parse incl.
P-skip-run and median MV prediction, dequant+itrans, intra 4×4/16×16/chroma
prediction. Verified **only on MB0–MB4 of the first IDR** (0/256 pixel diffs vs
ffmpeg no-deblock decode, SHA `5ce87b07…`). Its known limits: 81/300 MBs of the
full first IDR differ from ffmpeg due to intra-prediction edge-case bugs;
the fixture's one P-slice NAL (type 1, 7,082 bytes) is **parsed at the MB layer
but never reconstructed to pixels**; deblocking exists nowhere (the ffmpeg
ground truth was deliberately no-deblock). The Python line is analysis tooling,
not intake.

## 4. End-to-end verdict: .mp4 → frames?

**No. TNN cannot currently get from a real video file to faithful frames.**

| Leg | Status |
|---|---|
| Container: MP4 → sample byte ranges | ✅ measured working, deterministic |
| Codec metadata: SPS → 320×240 Baseline | ✅ measured working |
| Bitstream: samples → NAL units | ⚠️ external script only |
| Pixels: NALs → decoded frames | ❌ blocked — no slice decoder in Zag |

The video path gets exactly as far as the committed VERDICT.md says: container
parsed, SPS params only, slice decode blocked.

## 5. The current working video input: raw PPM frames

Committed `docs/lab/video-fusion-v4/src/composer_base.zag` contains a general
PPM P6 reader (`read_ppm_gen`, any W/H) + PPM writer — this is the ingest path
the fusion line actually uses (`composer ingest <label> <srcdir> <workdir>`:
24× 320×240 PPM → store.bin; `stillrecall` → output PPMs). Raw frames only,
no codec. The referenced fixtures exist externally and are intact:

- `~/workspace/video-combine/source/frames/frame_00–23.ppm` (pig, 320×240, 5.4 MB)
- `~/workspace/video-repro/source/frames/frame_00–23.ppm` (bunny, 320×240, 5.4 MB)

So: **TNN's working video input today is uncompressed raw frames via PPM
ingest; the coded-video path (any real .mp4) stops at the container/SPS.**

## 6. What stands between here and faithful frames (honest estimate)

The committed VERDICT.md estimates ~2,000 lines for baseline slice decode. From
this measurement, the actual gap decomposes as:

1. **Port slice-header + CAVLC to pure Zag** — the load-bearing missing piece.
   The Python prototype proves the algorithm (MB0–MB4 exact); the Zag port must
   handle the full 300-MB IDR, not 5 MBs.
2. **Fix the 81/300-MB intra-prediction edge bugs** in the prototype first
   (e.g. I_4x4 Horizontal-Up `zHU>5` fallback, left-edge mode constraints) —
   known-broken today, would ship as wrong pixels.
3. **Inter decode for P-frames** — MB-layer parse exists in the prototype but
   pixel reconstruction (reference-frame management, sub-pixel interpolation)
   does not; the fixture's only non-IDR slice is exactly this.
4. **Deblocking filter** — boundary-strength computation, absent everywhere;
   needed for byte-exactness vs a real decoder.

No guessing beyond this: items 1–4 are named from the actual prototype gaps and
the committed blocker list. Nothing here is a small patch.

## Assets (all NEW, created 2026-09-27 for this battery)

- `assets/pipeline_stages.png` — stage diagram: 6 stages with PASS/PARTIAL/BLOCKED
- `assets/frame_ref_pig_00.png` — reference input frame (pig frame_00, 320×240, from
  `~/workspace/video-combine/source/frames/` — external workdir, previously used by
  the fusion line; the PNG rendering is new)

## Could not measure

- Byte-identical "held frames" for H.264 — there is no decoder to hold frames; that
  IS the finding, not a measurement failure.
- PPS parse fidelity in Zag — no PPS parser exists to measure.
- Whether the Python prototype's 81/300 differing MBs are fixable without redesign —
  out of scope (diagnosis only, no repair).
