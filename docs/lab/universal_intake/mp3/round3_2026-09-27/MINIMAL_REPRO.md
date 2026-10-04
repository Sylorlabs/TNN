# MINIMAL_REPRO.md — 32 kHz `n_long_bands` investigation

**Date:** 2026-09-27
**Worker:** MP3-32kHz (Audio Round 3)
**Verdict: HONEST KILL — the "32 kHz discrepancy" does not exist.**

The RISK_REPORT (dangling commit `beb955732`) flagged as an open residual:
"the 32 kHz `n_long_bands` hardcoded-2 vs oracle shift discrepancy was not
addressed." This investigation proves the premise is wrong: **the oracle
does not shift at 32 kHz.** The hardcoded `2` in `mp3dec.zag` is correct
for every input the decoder supports. No code change to the value was made
(only a clarifying comment); the "fix" is the documentation of why.

---

## 1. The minimal reproducer

**File:** `clicks_32k_mx.mp3` (SHA-256 in `MANIFEST.sha256`)

A 32 kHz MPEG-1 Layer III file with **44 mixed-block granules**
(`block_type=2, mixed_block_flag=1`), built deterministically:

1. `clicks_32k.wav` — 3 s mono 32 kHz: periodic transient clicks
   (every 0.1 s) over a 220 Hz tone bed. Pure Python synthesis, zero RNG.
2. `ffmpeg -c:a libmp3lame -b:a 128k -ar 32000 clicks_32k.wav`
   → `clicks_32k.mp3` (86 frames, 44 short-block granules per oracle
   sideinfo; header `fffb98c0`, `sr_bits=2`, MPEG-1).
3. `flip_mixed.py` — parses each frame's side info at the bit level and
   sets `mixed_block_flag` 0→1 on every short-block granule
   (44 flipped; method mirrors the prior crew's mxflip fixtures, whose
   generator scripts were not preserved).

**Result — Zag vs oracle on the 32 kHz mixed-block fixture:**

| Metric | Value |
|---|---|
| Max abs PCM diff (LSB) | **1** |
| Mean abs diff (LSB) | 0.000212 |
| Samples compared | 99,072 |
| Zag×2 determinism | byte-identical |

**Non-vacuous:** oracle PCM on the flipped vs unflipped file differs by up
to **35,802 LSB**, so the ≤1 LSB agreement genuinely exercises the 32 kHz
mixed path (reorder + antialias + IMDCT with `n_long_bands=2`).

---

## 2. Root cause: `my_sr == 2` is MPEG-2.5 12 kHz, not MPEG-1 32 kHz

The oracle (`ref/mp3ref.py:768,774`):

```python
n_long_bands = (2 if gr['mixed_block_flag'] else 0) << (1 if my_sr == 2 else 0)
```

where (`mp3ref.py:121,765`):

```python
sr = (hdr[2] >> 2) & 0x03                                   # 0=44.1k, 1=48k, 2=32k (MPEG-1)
my_sr = sr + (((hdr[1] >> 3) & 1) + ((hdr[1] >> 4) & 1)) * 3  # += version*3
```

The two bits are the MPEG **version ID** (bits 19–20):
MPEG-1 (`11`) contributes 2, MPEG-2 (`10`) contributes 1, MPEG-2.5 (`00`)
contributes 0. Hence:

| Input | `sr` | version bits | `my_sr` | oracle shift fires? |
|---|---|---|---|---|
| MPEG-1 44.1 kHz | 0 | 2 | **6** | no |
| MPEG-1 48 kHz | 1 | 2 | **7** | no |
| MPEG-1 32 kHz | 2 | 2 | **8** | **no** |
| MPEG-2.5 12 kHz | 2 | 0 | **2** | **YES** |

The shift fires **only for MPEG-2.5 at sr index 2 (12 kHz)** — the
"32 kHz" in the risk report confused the *sr index* (2 = 32 kHz *within
MPEG-1*) with `my_sr` (which carries the version offset).

The Zag decoder (`mp3dec.zag:149-150`) computes `my_sr` with the identical
formula, but it is an **MPEG-1-only** decoder (MPEG-1 frame-length formula
`144·brate/sr`, MPEG-1 bitrate table, MPEG-1 scalefactor tables). For every
frame it can correctly parse, `my_sr ∈ {6,7,8}`, the oracle's shift never
fires, and the oracle uses `n_long_bands = 2` — exactly the hardcoded value.

### Why the 12 kHz row can't rescue the report's claim

Even if the decoder supported MPEG-2.5, the oracle's own 12 kHz mixed row
(`g_scf_mixed_rows[1]`, 40 entries) is **structurally incompatible** with
its reorder loop: tracing `reorder()` shows the short-band walk never hits
the 0-terminator (overruns the table) for `n_long_bands` 2 *or* 4, while
all MPEG-1 rows terminate exactly at 576 samples with `n_long_bands=2`.
The `my_sr==2` path is unreachable *and* untestable — no encoder produces
MPEG-2.5 mixed blocks, and the reference table would crash the oracle.
It is dead code on both sides.

### The "tables are the general mechanism" red herring

Deriving `n_long_bands` from the mixed table (sum of long widths ÷ 18)
gives 36÷18 = **2** for all three MPEG-1 rows — consistent with the
hardcoded value — but does **not** reproduce the oracle's 4 for the 12 kHz
row (its first 8 entries sum to 64, not 72; the row has a different
structure). The oracle's shift is an explicit rate-based special case, not
a table-derived value. Porting it would add dead code for a path neither
implementation can execute. The honest general statement is the comment
now in the source: `n_long_bands = 2` for all MPEG-1 mixed blocks.

---

## 3. Reproduction recipe

```sh
cd ~/workspace/audio_r3/mp3
# 1. build (pinned toolchain; run from the zag_full dir per BUILD.md)
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/zag_full
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 mp3dec.zag -o /tmp/mx/mp3dec
# 2. decode the 32 kHz mixed fixture
/tmp/mx/mp3dec ~/workspace/audio_r3/mp3/clicks_32k_mx.mp3 /tmp/mx/zag_32k_mx.pcm
# 3. oracle
cd ~/workspace/selfpam_run/tnn-lab/docs/lab/universal_intake/mp3/ref
python3 mp3ref.py ~/workspace/audio_r3/mp3/clicks_32k_mx.mp3 /tmp/mx/orc_32k_mx
# 4. compare (expect max 1 LSB)
python3 -c "
import numpy as np
z = np.fromfile('/tmp/mx/zag_32k_mx.pcm', dtype='<i2').astype(np.int64)
o = np.fromfile('/tmp/mx/orc_32k_mx/b4.s16', dtype='<i2').astype(np.int64)
d = np.abs(z - o); print('max LSB:', d.max(), 'mean:', d.mean())"
```

To regenerate the fixture from scratch: synthesize `clicks_32k.wav` as in
§1, encode with ffmpeg/libmp3lame at `-ar 32000`, then
`python3 flip_mixed.py clicks_32k.mp3 clicks_32k_mx.mp3`.
