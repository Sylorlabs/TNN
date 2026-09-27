# P2 — lineage-vouched cascade (VOC3): implementation report

Round 4 arm P2, frozen prereg `../PREREG_R4.md`. Implementer read the R4
prereg, the R3 prereg, and `VERDICT_R3.md` (C2's VOID) before starting.
Pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Phase 1 — feasibility dry-run: PASS

Tool: `voc3_tool.py` (this dir). Command:

```
python3 voc3_tool.py --trace ~/workspace/upscale_gen/teach_out/TEACH_TRACE.txt \
    --voc2 ~/workspace/upscale_gen/teach_out/vocab.bin \
    --voc3 vocab_v3.bin
```

Result: **DRY-RUN PASS**, exit 0.

| check | result |
|---|---|
| VOC2 SHA-256 | `cbead2f7c13e455fb1598defc34182f7b2517dfaeb6f0fa95925e4f1f0d525b2` — matches frozen pin |
| VOC2 size | 1,958,448 bytes; header+body layout sums exactly, zero slop |
| TEACH_TRACE parse | 235 traced atoms, unambiguous: per-scale ids exactly 1..K−1 (S=64: 1..47, S=32: 1..47, S=16: 1..47, S=8: 1..31, S=4 thin: 1..63); no duplicates, no out-of-range ids, all src_img ∈ 0..3 |
| NULL atom | atom 0 all-zero **binary-verified** at all 5 scales (not just trace text) |
| src_img distribution | 0=brick_wall: 101, 1=lake_water: 132, 2=foliage: 2, 3=stone_wall: **0** |
| VOC3 layout | VOC2 bytes with magic → `VOC3`, + 240-byte appended u8 table (scale-major: si0 atoms 0..47, si1 0..47, si2 0..47, si3 0..31, si4 0..63); NULL atoms → sentinel 255 |
| VOC3 SHA-256 | `e43cfebfb0f4a8a4a38d685690a6ab6933de44cc170f1b89ad94dad9deb7ae8d` (1,958,688 bytes) |
| reload check | header identical mod magic; **every** atom/key payload byte identical to VOC2; table round-trips |

Notes: stone_wall (src 3) contributes zero atoms — psrc=3 can therefore
never occur (psrc always comes from a real winning atom's table entry),
and any hypothetical psrc=3 block would hit the empty-set → full-vocab
fallback. Foliage (src 2) has only 2 atoms in the whole vocab.

## Phase 2 — P2 binary

### Base

`azgen_p2.zag` is derived from **pristine** `azgen.zag`
(SHA-256 `060193d0ca8c948a24b953953ad0c49602dfa39dfd2cacafdf8cfdd7f7e59a7f`,
identical copies at `~/workspace/upscale_gen/src/azgen.zag` and
`~/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/generation/src/azgen.zag`)
— the ATOM-STAMP baseline, not C3's chooser. (C2's lesson: build on the
clean base.) `azgen_p2.zag` SHA-256:
`d1620a96e90f743dbaf4111b562be2964d6d8efd37895fc8fbca80e012861a8f`.

### Exact mechanism change (the ONLY behavioral change vs baseline)

1. **VOC3 loader** (`g_vocab_load`): requires magic `VOC3`
   (86,79,67,51); parses the header/body exactly as VOC2; reads the
   appended 240-byte lineage table into `vsrc` (+ `voff[5]` scale-major
   offsets); rejects truncated tables (rc 10). **VOC2 is rejected with
   rc 9 and the message** `vocab is VOC2 (no per-atom lineage table);
   P2 requires VOC3` — verified live (exit 1, clear message). No silent
   fallback.
2. **Lineage restriction** (`gshapes_fit`, new params
   `psrc, vsrc, voff, pln, st`): top scale (si=0, S=64) passes psrc=−1 →
   full vocabulary, byte-identical matching to baseline. At every finer
   scale the candidate loop keeps ascending `ai` order and **skips**
   atoms whose `vsrc` entry ≠ psrc. Children receive
   `bsrc` = winning atom's table src; `best==0` (NULL won — the parent
   block is NO-FIT, "no fit found") → psrc=−1 → full vocabulary.
   Empty restricted set → full vocabulary. Gain bar (≥9/value), split
   logic, take records, commit, ATOM-STAMP construction, and the entire
   LINES path (thin atoms have no parent block) are baseline-identical.
3. **Take records** stride 9→15 to carry match-time LS-plane numerators
   (analysis support, see below); commit/render read the same fields 0..8.
4. **Trace**: `GEN_TRACE.txt` gains `planemode=` and a
   `lineage: top=… restricted=… empty_fallback=… parent_nofit=…
   rcand_evals=… fullcand_evals=…` line.

### Analysis mode (preregistered, analysis-only)

`argv[3]=="plane"` renders atom-takes as **PLANE-FIT** instead of
ATOM-STAMP: same take geometry (identical takes — same G/N/take count),
least-squares plane evaluated at 2×, label 3. Plane helpers
(`g_csq`, `g_pterm`, `g_plane_fit`) and the render branch are verbatim
from committed `azgen_c3.zag` (SHA `cd5bab26…`, the post-fix plane code
per VERDICT_R3's honest build note). The plane is fit at **match time**
on the same block pixels the atom matched (stored in the take record),
so it is correct under both SHAPES-first and LINES-first cascade orders.
For the P2 vocab-abandonment bar; not a mechanism.

### Build

```bash
mkdir build && cd build
cp ../impl_p2/azgen_p2.zag .
cp ~/workspace/upscale_gen/src/{azlayers.zag,common_az.zag,R33_NATIVE_IO_V1.zag} .
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 azgen_p2.zag -o azgen_p2
```
Clean build, warnings only (pre-existing analyzer lints, also present
for the pristine baseline build). Run: `azgen_p2 <indir> <outdir>
[plane]`; indir holds `input.bmp`, `vocab.bin` (VOC3), `gt.bmp`.

### Determinism (bridge, VOC3)

| run | upscale_gen.bmp SHA-256 |
|---|---|
| 1 | `655afed606f66ffb50c5177bfcb83b23a10dd84973f3cd0aeea0cf7042f0b80c` |
| 2 (fresh outdir) | `655afed606f66ffb50c5177bfcb83b23a10dd84973f3cd0aeea0cf7042f0b80c` |
| 3 (`env -i`) | `655afed606f66ffb50c5177bfcb83b23a10dd84973f3cd0aeea0cf7042f0b80c` |

Byte-identical across reruns and allocator perturbation. Analysis mode
also deterministic (2 runs → `94e6090c…`, identical).

### Sanity: bridge/sky vs baseline

Baseline = pristine `azgen.zag` rebuilt with the same toolchain +
frozen VOC2. Both rebuilds reproduce the **committed baseline output
SHAs** (`2028ba1d…` bridge, `84255819…` sky) and PSNRs — build pipeline
valid. PSNR = mean of per-channel dB via frozen
`upscale_gen/src/metrics.py`, `upscale_gen.bmp` vs `gt.bmp`.

| image | baseline PSNR | P2 PSNR | Δ | P2 sse_gen | base sse_gen |
|---|---|---|---|---|---|
| bridge | 18.47 | 18.40 | −0.07 | 272350651 | 268467517 |
| sky | 22.75 | 22.75 | 0.00 | 409624167 | 409163171 |

P2 analysis-mode (plane render) on bridge, same takes: **19.20 dB**
(sse 225179077) vs P2-atom 18.40 dB — i.e. +0.80 dB for measured planes
over atom stamps on identical take geometry (bridge). For the battery
runner's abandonment-bar adjudication, not a finding.

### Restriction-binds check: the restriction genuinely binds

From `GEN_TRACE.txt` lineage counters:

| image | top (full) | restricted | empty_fallback | parent_nofit (full) | rcand_evals | fullcand_evals |
|---|---|---|---|---|---|---|
| bridge | 24 | 128 | 0 | 1376 | 1108 | 50184 |
| sky | 96 | 80 | 12 | 7972 | 1056 | 282288 |

- 128 bridge / 80 sky child blocks matched under restriction
  (evaluating only 1108/1056 same-src candidates instead of full K).
- Sky exercised the empty-set → full-vocab fallback 12 times (as designed).
- Output SHAs differ from the unrestricted baseline on **both** images
  (bridge `655afed6…` vs `2028ba1d…`; sky `2e2e323d…` vs `84255819…`),
  so the restriction changes matching at the output level — it is not
  decorative. (Sky's PSNR rounds identically at 2 dp despite different
  pixels: 22.75 vs 22.75.)

Reading: most fine blocks (1376/7972) have a NULL-winning parent and
correctly fall back to full vocabulary; where the parent did vouch a
source, the restriction cut the candidate field to same-src atoms only.

### What was NOT done (per task/prereg)

- No full battery (dev or sealed). Sealed dir never opened.
- No tuning of any kind; frozen bars/gains untouched.
- Binaries and build scratch deleted after scoring; `impl_p2/` holds
  source + fixture + tool + this doc only.

## Files in `impl_p2/`

- `azgen_p2.zag` — P2 source (pure Zag).
- `vocab_v3.bin` — frozen VOC3 fixture (1,958,688 bytes,
  SHA `e43cfebf…deb7ae8d`). The one file intended for later commit.
- `voc3_tool.py` — VOC2→VOC3 converter + dry-run gate
  (SHA `8d7a2828…98140167`).
- `IMPL_P2.md` — this file.

**P2 COMPLETE**
