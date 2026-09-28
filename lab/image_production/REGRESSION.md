# Phase-1 Regression — Adoption of Adaptive Layers + Adaptive Magnification

Adoption worker run, 2026-09-26 ~20:40 PDT. Rebuilt ONLY from the committed sources
(`docs/lab/image_adaptivelayers/src/`, SHA-verified byte-identical to the copy used),
built with the pinned toolchain `znc_linux_x86_64_abed8aa1`. Fixture SHA verified
`4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00` before each run.
No prebuilt binaries used. Two full ingest+emit runs.

## Bar (a) — numbers hold

| Metric | Expected | Run 1 | Run 2 | Verdict |
|---|---|---|---|---|
| Understanding PSNR | 46.35 dB | 46.35 dB | 46.35 dB | PASS |
| Understanding SSIM | 0.9955 | 0.9955 | — (byte-identical render) | PASS |
| Residual share | 2591/95744 = 2.7% | 2591/95744 = 27 per-mille | 2591/95744 | PASS |
| knowmap.bin size | 636,451 bytes | 636,451 bytes | 636,451 bytes | PASS |
| Layer order | SMOOTH→SHAPES-ZOOM→LINES (1 3 2) | 1 3 2 | 1 3 2 | PASS |
| SMOOTH | G=6,311,802,255, 46,228 B, 1,778 leaves | G=6311802255, B=46228 | identical | PASS |
| SHAPES-ZOOM | G=57,044,876, 571,565 B, 269 regions, 79 zoomed | G=57044876, B=571565 | identical | PASS |
| LINES | G=15,833, 378 B, 27 segs | G=15833, B=378 | identical | PASS |
| Knowmap magic | TNNKTLM3 | TNNKTLM3 (od-verified) | identical | PASS |
| @16 vocab quirk | — | trace: 32 built → PRUNE dropped 1 unfired → 31 kept (emit prints 31; inherited RUNLOG prose says 32 — the prose counted built, emit counts kept; both runs byte-identical) | — | noted, not a bar |

## Bar (b) — exact closure

| Check | Result |
|---|---|
| renderA.bmp SHA-256 | `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00` == sealed fixture SHA |
| renderB.bmp SHA-256 | `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00` |
| Path A == Path B | renderA.bmp and renderB.bmp byte-identical |
| render_understanding vs fixture | 46.35 dB / 0.9955 (mse_ch 2.31/1.46/1.02) |

## Bar (c) — pentagon artifact

Bridge-arch crop re-rendered at 4x from my run's `render_understanding.bmp` and
compared to the same crop of the sealed original: visually identical, smooth curves,
no faceting. The zoom fork's pentagon defect does not reappear.
**PASS.**

## Bar (d) — byte-identical reruns

Run 1 vs Run 2: knowmap.bin, renderA.bmp, renderB.bmp, render_understanding.bmp,
renderB_understanding.bmp, DELIBTRACE.txt, render_layermap.bmp, render_scalemap.bmp,
render_splitmap.bmp — all 9 byte-identical. **PASS.**
Bonus: my run-1 artifacts are byte-identical to the official `~/workspace/image_adaptivelayers/run/`
artifacts (knowmap, renderA, renderB, render_understanding, DELIBTRACE.txt all match).

DELIBTRACE.txt also matches the committed evidence SHA from the inherited
`SHASUMS.txt` (`b7d6d55045a4f1b6c9f6a3e740067a8ffa2ade1f52892b07b194132e57fe0455`).

## Phase-1 verdict: PASS — adoption shipped

All four regression bars hold. Ingest ≈15s, emit ≈2s on the adoption worker's VM
(inherited run log recorded ~60s/~7s on different hardware).
