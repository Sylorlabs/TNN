# REPAIR — Audio intake 64-sample head bug (L1) + plm phase (L2)

**Date:** 2026-09-26. **Worker:** A (senses bug-repair program, Micah order ~09:56 PDT).
**Verdict baseline:** `docs/lab/audio_intake/VERDICT_INTAKE.md` (commit `c33b623f2ce3`).

## 1. The bugs

### L1 (assigned): fabricated 64-sample head — INTAKE machinery bug
- **Location:** `imagination/rawbyte/v5/proto5g.py`, `hear()` (intake) and
  `reemit()` (Python read-back); `imagination/rawbyte/v5/rb_longmem.zag`,
  mode 9 (pure-Zag read-back).
- **Mechanism:** `hear()` computes LPC residuals only for samples `P..n-1`
  (`P=64`). The first 64 PCM samples were never quantized, never stored.
  Re-emit filled samples `0..63` with `proto[q[0..63]]` — prototype indices
  fit to samples `64..127`, a different signal region (attack transient vs
  settled tone for the cry). The cry's LPC(64) is highly resonant (impulse
  peak gain 8.93); the wrong initial filter state rang into a transient
  peaking at **23834 vs the 12442 fixture peak (1.92×, +11,392)**.
- **Why the fabrication existed:** the model stored only the residual score
  `q` (length `n-P`); re-emit needed *something* for the first P samples to
  seed the synthesis filter, and the cheapest something was reusing the
  first P score indices. It was never a deliberate design choice — the
  `q` array simply had no head, and both re-emit paths papered over it the
  same way (the Zag mode 9 mirrors the Python line exactly).
- **Fix:** `hear()` now stores the first P **real PCM samples**
  (`head = x[0:P]`, int16-exact) in the model. Re-emit plays them verbatim
  for samples `0..P-1` and seeds the LPC filter memory with them, so the
  synthesis from sample P onward starts from the true state. The
  fabrication branch (`proto[q[i]]` for `i<P`) is **deleted** in both
  paths — no code path invents the head anymore.

### L2 (required by the repair criterion): plm half-period phase mismatch
- **Location:** same two re-emit functions (`reemit()` in `proto5g.py`,
  mode 9 in `rb_longmem.zag`).
- **Mechanism:** `hear()` bins the residual **relative to the residual
  frame** (`arange(nr)/T0`), but re-emit binned by **absolute sample index**
  (`arange(n)/T0`) — a 0.502-period shift for cry (P=64, T0=127.49),
  phase-error RMS 19.7 vs quantization-error RMS 5.1 (3.9×).
- **Why fixed here:** the brief's repair criterion is the ablation result
  (cry peak 12406, corr 0.99827), which the verdict's ablation table
  defines as **phase fixed + true head** (row C). The head fix alone gives
  corr 0.906 (measured §3) — the 0.998 bar is unreachable without the
  phase fix. The fix is mechanical (one phase convention everywhere):
  re-emit now bins `((i-P)/T0)`, matching `hear()`'s convention, which is
  the reference (it defines what `plm[b]` means). Models are unchanged
  by L2 (re-emit-side only).

## 2. Model format change: RBLMEMv5 → RBLMEMv6
- `imagination/rawbyte/v5/npz_to_bin.py` now writes magic `RBLMEMv6` and a
  new section after `boost`, before `q`: **`head[P]` int16 LE** (the true
  first-64 PCM samples). `q` (length `n-P`) follows unchanged.
- `rb_longmem.zag` mode 9: `head_off = PMF_off + 144`,
  `q_off = head_off + 2*P`; new `rb_get16` (LE i16 with sign extension).
- **Safety:** the binary checks the magic and **refuses v5 models**
  (verified: old `m5g_cry.bin` → no output, no crash) instead of
  silently misparsing. No `.bin` models are committed to the repo —
  they are regenerable via `hear()` → `npz_to_bin.py`.

## 3. Verification (all measured 2026-09-26, pinned toolchain `znc_linux_x86_64_abed8aa1`)

Build recipe (validated by reproducing the verdict's byte-identical binary
`7206eae3…` from the pre-fix source first):
`znc rb_longmem.zag -o rb_longmem_v6` with cwd containing `rb_longmem.zag`
and `toolchain/R33_NATIVE_IO_V1.zag` (import `../../toolchain/…` resolves
against cwd). Fixed binary SHA-256:
`7fce0152189c15f57dcbbd634ae0ff06a95b24789af121ef24bf1c4346b67a9c`.

| clip | fixture peak | re-emit peak BEFORE | re-emit peak AFTER | corr BEFORE | corr AFTER | errRMS AFTER |
|---|---|---|---|---|---|---|
| strike | 3305 | 3126 | 3126 | 0.99836 | 0.99842 | 40.5 |
| **cry** | **12442** | **23834** | **12406** | 0.89618 | **0.99827** | 136.0 |
| clang | 14220 | 15245 | 15245 | 0.99596 | 0.99651 | 109.8 |
| vowel | 4463 | 4317 | 4317 | 0.98985 | 0.98986 | 97.9 |

Cry matches the ablation row C **exactly** (peak 12406, corr 0.99827,
err 136). The peak doubling is gone (+11,392 → −36 vs fixture).

Determinism / exactness:
- `hear()` re-run → byte-identical `.npz`; `npz_to_bin.py` re-run →
  byte-identical `.bin` (zero RNG throughout).
- Zag mode-9 re-emit ×2 per clip → **byte-identical** (`cmp` clean, 4/4).
- Fixed Python `reemit()` vs fixed Zag binary → **sample-identical**
  (max|diff| = 0.0) on all 4 clips.
- Head samples 0..63 of every re-emit **bit-equal** the fixture's
  (verified per clip).
- Parse level unchanged and still lossless (untouched `read_wav` path).
- Zag imagine path (mode 0) smoke-tested on a v6 model — works (magic +
  offset parse OK).

Head-fix-only ablation (for the record): peak 23834 → 11104, corr
0.89618 → 0.90645. The remaining peak/corr gap to the C numbers is the
L2 phase error — now fixed.

## 4. Regression check: image / video intake
No shared code was touched. Diff is exactly 3 files, all under
`imagination/rawbyte/v5/` (`proto5g.py`, `npz_to_bin.py`,
`rb_longmem.zag`). Untouched: `R33_NATIVE_IO_V1.zag` (imported only),
the crew-P organ (`audio_principles/crew_p/organ.zag`), image intake
(`docs/lab/image_intake_verdict/`), video intake
(`docs/lab/imagination/video-intake-fidelity/`). Image/video stay
bit-exact by construction.

## 5. Handoff for the exact-replication audio crew
- **Branch:** `tnn-native-lab` (this repair committed on
  `audio-intake-headfix`; merge to `tnn-native-lab`).
- **Entry point:** `imagination/rawbyte/v5/proto5g.py`
  (`hear()` → `save()`), `imagination/rawbyte/v5/npz_to_bin.py`
  (`.npz` → `RBLMEMv6` `.bin`),
  `imagination/rawbyte/v5/rb_longmem.zag` mode 9 (read-back).
- **Rebuild:** `python3 proto5g.py hear <fixture.wav> <model.npz>` →
  `python3 npz_to_bin.py <model.npz> <model.bin>` →
  `znc rb_longmem.zag -o rb_longmem` (pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, cwd with
  `toolchain/R33_NATIVE_IO_V1.zag` beside the source) →
  `./rb_longmem <model.bin> 12 9 <out.wav>`.
- **What changed for you:** models now carry the true head; re-emit is
  sample-identical between the Python replication and the Zag binary, so
  verify new work against either. The honest representation floor is now
  corr ≈ 0.998 on cry (64-prototype quantization, by design — see
  verdict §L3). Remaining known intake-adjacent item: none — L1+L2 were
  the two intake machinery bugs; everything else in the verdict's gap
  table is downstream (imagine walk).

## Evidence
- `docs/lab/audio_intake/evidence/repair_metrics.json` (per-clip numbers)
- `docs/lab/audio_intake/evidence/repair_SHA_MANIFEST.txt` (fixtures,
  models, re-emits, binary, sources, toolchain)
