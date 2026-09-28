# Seal — diverse held-out photo set

## How the seal was made (2026-09-27)

Nine real photographs were sourced from Wikimedia Commons by querying the
Commons API (`action=query`, `list=search`, `filetype:bitmap` photo filter,
then `prop=imageinfo` with `extmetadata` for author/license and a 768px
thumbnail URL). For each candidate the API-returned author name and license
short name were recorded verbatim into MANIFEST.tsv along with the Commons
file-page URL. Downloads were normalized to the sealed pipeline format —
exactly 768px wide, RGB JPEG, quality 90 (PIL, LANCZOS resize when the API
returned a non-768 thumbnail; the API returned 960px thumbnails for
`iiurlwidth=768` on 2026-09-27, so the resize step is part of the seal).
Every stored file was verified with PIL: JPEG format, 768px wide, RGB.
SHA-256 of the exact stored bytes is in MANIFEST.tsv, recomputable with
`sha256sum`.

## Non-training statement

These bytes are HELD OUT. They MUST NEVER enter `azteach` or any training /
atom-selection / teaching process. They are test fixtures only: the eval
harness reads them as ground truth, downscales them to an input, and scores
generation-vs-bicubic against them. Feeding them to any teach step voids the
seal and the honesty of every verdict that used this set.

## Anti-leakage verification (2026-09-27)

Grepped every training-side source under `docs/lab/image_upscale/` —
`generation/` (azteach.zag, azgen.zag, TEACH_TRACE.txt, vocab.bin),
`concept_probe/`, `src/` — excluding `diverse_set/` itself, for:

1. All 9 stored filenames (`fabric.jpg` … `market.jpg`) → **0 hits**
2. The 16-hex-char SHA-256 prefixes of all 9 stored bytes → **0 hits**
3. All 9 Commons source titles (e.g. "An example of waffle fabric",
   "Elderly Gambian", "Fishmonger smiling") → **0 hits**

The teach trace (`generation/teach_out/TEACH_TRACE.txt`) confirms the shared
vocabulary was built from exactly 4 training photos — brick_wall, lake_water,
foliage, stone_wall — none of which are in this set. **Result: 0 hits —
seal holds.**

## Re-verification procedure

Any future crew must re-run before use:
```
cd docs/lab/image_upscale
grep -rl "fabric.jpg\|woodgrain.jpg\|treebark.jpg\|calmwaters.jpg\|portrait.jpg\|car.jpg\|building.jpg\|cat.jpg\|market.jpg" generation/ concept_probe/ src/ | grep -v diverse_set
```
Any hit outside `diverse_set/` means the seal is broken.
