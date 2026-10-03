# EVIDENCE.md — MP3 32 kHz / mixed-block verification (Audio Round 3)

**Date:** 2026-09-27
**Decoder:** pure-Zag `mp3dec`, built with pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
from `docs/lab/universal_intake/mp3/zag_full/` (working tree incl. the
uncommitted beb955732 mixed-block stride fix + a comment-only
`n_long_bands` clarification; build OK, 4 pre-existing analyzer warnings).
**Oracle:** `docs/lab/universal_intake/mp3/ref/mp3ref.py`
**Gate:** Zag-vs-oracle PCM max diff ≤ 1 LSB. PCM-bit-exactness is the metric.

Delivered sources (`~/workspace/audio_r3/mp3/`):
`mp3dec.zag`, `mp3tab64.zag`, `common.zag` (= working tree, verified below).

---

## 1. Pre-existing mixed-block fix — VERIFIED (task step 1)

The working tree carries the beb955732 fix (table re-padded to 40-byte
stride, `mixed_row_get` uses `row*40+i`, copy loop `k<40`). Rebuilt from
scratch and re-ran the sealed mixed fixtures from the dangling commit:

| Fixture (44.1 kHz, mixed-flag-flipped) | Zag×2 | Zag vs oracle max LSB | mean LSB | samples |
|---|---|---|---|---|
| `fx_mxflip_drums_all.mp3` | IDENTICAL | **1** | 0.000106 | 359,424 |
| `fx_mxflip_drums_alt.mp3` | IDENTICAL | **1** | 0.000095 | 359,424 |
| `fx_mxflip_rapid_all.mp3` | IDENTICAL | **1** | 0.000256 | 359,424 |
| `fx_mxflip_rapid_alt.mp3` | IDENTICAL | **1** | 0.000134 | 359,424 |

Confirms the RISK_REPORT "After" column (all 1 LSB). The "already fixed"
claim holds. (Pre-fix behavior per the report: 65,535 LSB max error.)

## 2. Standard-fixture regression — NO CHANGE

| Fixture | PCM SHA-256 | matches committed ref | Zag×2 |
|---|---|---|---|
| `t_128cbr.mp3` | `f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467` | YES (EVIDENCE.md) | IDENTICAL |
| `t_128js.mp3` | `711f0f067397f1439f62f18275b88e0e25df86875936e11f27be0d65318209b0` | YES (BUILD.md) | IDENTICAL |
| `t_vbr.mp3` | `7abcd3cb239f530cbc583ff9427738f2a2276bb47a14ae885551d7be63e4c6d5` | YES (BUILD.md) | IDENTICAL |

44.1 kHz fixture SHAs unchanged; 48 kHz shares the same `n_long_bands=2`
code path (oracle `my_sr=7`, no shift) and the same mixed-row table family
as 44.1 kHz (rows 5/6 verified structurally identical: reorder terminates
at exactly 576 samples for both).

## 3. 32 kHz mixed-block — the "discrepancy" that wasn't (task step 2)

New fixture `clicks_32k_mx.mp3` (see MINIMAL_REPRO.md): 32 kHz MPEG-1,
86 frames, **44 mixed-block granules**.

| Check | Result |
|---|---|
| Zag vs oracle max LSB | **1** (mean 0.000212, n=99,072) |
| Zag×2 | byte-identical |
| Oracle mixed vs unflipped (path-activity) | max 35,802 LSB — path genuinely exercised |
| Oracle `my_sr` on this file | **8** (MPEG-1 32 kHz) → no shift → `n_long_bands=2` |

Zag's hardcoded 2 and the oracle agree bit-for-bit on the formula for
every MPEG-1 rate. **No divergence at 32 kHz. Honest kill.**

## 4. Why the oracle's shift is out of scope

`n_long_bands = (2 if mixed else 0) << (1 if my_sr == 2 else 0)` fires only
at `my_sr == 2` = MPEG-2.5 version ID (`00`) + sr index 2 (12 kHz):

- The Zag decoder is MPEG-1-only (MPEG-1 frame-length `144·brate/sr` and
  bitrate table); `my_sr ∈ {6,7,8}` on all parseable input.
- The oracle's 12 kHz mixed row (`g_scf_mixed_rows[1]`) overruns its own
  `reorder()` loop (never reaches the 0-terminator) for `n_long_bands` 2
  or 4 — the path is untestable even in the reference.
- Table-derivation (long-widths sum ÷ 18) yields 2 for all MPEG-1 mixed
  rows and does *not* reproduce the oracle's 4 for the 12 kHz row, so the
  shift is an explicit rate special-case in the oracle, not a table
  property. Porting it would be dead code on an unreachable path.

## 5. Huffman / pow coverage (task step 4)

No decoder logic changed (comment-only edit; rebuilt binary produces
byte-identical PCM on all fixtures above). Huffman and `pow_43_z` paths
are exercised by every fixture here (mixed fixtures use Huffman tables
across all 16 linbits tables via the flipped short blocks; standard
fixtures cover long-block Huffman). The Risk-3 `pow_43_z` full-domain
sweep (8,207 outputs, max rel err 1.32e-6, pre-existing) is unaffected —
the function is untouched.

## 6. Disk discipline

`df -h ~` before work: 99% / 1.4 GB free. All scratch kept in `/tmp/mx`
(tmpfs, 498 MB free) and `~/workspace/audio_r3/mp3/work/` (~2 MB).
Deliverables total < 200 KB. No battery exceeded available space.

## 7. Change summary for the coordinator (no commit made by worker)

Working-tree diff in `docs/lab/universal_intake/mp3/zag_full/`:
- `mp3tab64.zag` + `mp3dec.zag`: the beb955732 mixed-block stride fix
  (pre-existing, verified §1).
- `mp3dec.zag`: +9-line comment at the `n_long_bands` site documenting the
  32 kHz finding (comment-only; rebuilt binary byte-identical output on
  `t_128cbr` and the 32 kHz mixed fixture).

Delivered to `~/workspace/audio_r3/mp3/`: `mp3dec.zag`, `mp3tab64.zag`,
`common.zag`, `clicks_32k.mp3`, `clicks_32k_mx.mp3`, `flip_mixed.py`,
`MINIMAL_REPRO.md`, `EVIDENCE.md` (this file), `MANIFEST.sha256`.
