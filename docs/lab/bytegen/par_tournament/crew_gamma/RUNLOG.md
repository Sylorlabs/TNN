# CREW GAMMA — RUNLOG
**Order:** Micah, 2026-09-24 — "for gamma disease repair for audio test your hypothesis."
**Hypotheses:** H1 = re-stage fixture plan energies for gain 1; H2 = one fixed, output-independent mastering gain on every render; control = restore old output-derived peak normalizer.
**Frozen sources:** `~/workspace/tnn-lab/bytegen/gamma_repair/REPAIR_NOTE.md`, `REPAIR_PREREG.md`.
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Rules:** zero RNG; 3 byte-identical reruns (SHA/cmp); analyzer-driven only (agents cannot hear audio).
**Work dir:** `~/workspace/tnn-lab/bytegen/par_tournament/crew_gamma/`

## 1. Control integrity check
- Copied production `imagination/src/field.zag` (gain-1 post-repair) → `src/field_ctl.zag`; adjusted build-dir import to `../../../../toolchain/R33_NATIVE_IO_V1.zag`; built `build/field_ctl`.
- Rendered 4 hifi fixtures → reproduced frozen repair SHAs:
  - `f3song_hifi.wav` = `0742f7ec87627c281dfa9a15dffaa3cc3eba107880d77938481715fb72f2b906`
  - `f3mood_happy.wav` = `4a7169faa90ce19d61515df9ddad15da2cc52f7883fe9c982b8d442b56299be1`
  - calm = `0e3c82db3696239c0b0c88f7015eedcd6df6a552178391557a1160df4acacbae`
  - scary = `a7d86ce2164d75b7c9384aac8ca4cfb2b24e4b12ba52345396af1721b924efed`

## 2. Diagnostic scaffolding (experiment-only, `src/patch_variant.py`)
- `f3mixpeak`: unclipped hifi mix peak per fixture. `f3mixdump`: raw pre-emit s32 mixes.
- `build/field_diag` reproduces `f3song_hifi.wav` SHA exactly → scaffolding does not alter hifi output.
- Measured unclipped mix peaks: song **117734**, happy **124074** (hottest), scary **104680**, calm **27441**.
- Fixed H2 gains derived: hottest@FS G=32767/124074≈0.26409; bracket: 32767/104680 (scary@FS), 32767/248148 (half), 32767/27441 (calm@FS, deliberately hot).

## 3. H1 — plan-authoring re-stage (`src/h1_census.py`, `src/h1_restage.py`)
- Mechanical voice census of the generator source (no render measured):
  - song B=420743 (24 voices) | happy B=503783 (35) | scary B=285954 (10) | calm B=61240 (9)
  - B = max_frame Σ active_voice_bounds; tone voice_bound = energy×28×Σ_h(w_h/1000) (LUT max 32767 confirmed); noise = all 48 bins; sweeps = 3 bins; harmonic strokes = 1.0/0.6/0.4 parts.
- `h1_restage.py` rewrote all 60 authored energy literals as `(e*32767/B)` per fixture → `src/field_h1.zag`. Verified by diff: only energy args + header comments changed.
- Mix peaks after re-stage (f3mixpeak): song 8726, happy 7577, scary 11645, calm 14608 — all ≤ 32767 ✓.

## 4. H2 variants + revert control (`src/patch_variant.py --h2 N D`, `--revert`)
- H2: replaced emit-time `/1` scale with fixed `v*N/D` in f3_emit (mix path untouched). Built field_h2a/b/c/d.
- Revert: restored old behavior (peak scan → scale every sample by 24000/peak → fixed rails) in `src/field_revert.zag`. Built `build/field_revert`.
- Mix peaks (f3mixpeak) for h2a–d identical to control (117734/124074/104680/27441) → gain is emit-only.

## 5. Consistency gate port (`src/analyze_gate.py`)
- Python port of the 9 frozen V10 bars (G-PER, G-STA, G-LURCH, G-DRIFT, G-FLUXm, G-SIL1, G-SIL2, G-G-CLIP, G-CREST) with only the ≥10 s guard relaxed for 2.6–3.1 s fixtures.
- Validated against real `gate_bin` on fork_par `par_seq1.wav` (30 s): all 9 bars agree to ~0.1% (e.g. G-PER 0.341 vs 0.340, G-DRIFT 479.772 vs 480.284).

## 6. Renders + gamma proof
- `f3hifi` + `f3gammaproof` rendered for ctl, h1, h2a, h2b, h2c, h2d, revert (all rc=0).
- R3 gamma proof, shared region [0,107484) hifi / [0,20000) 8 kHz: ctl/h1/h2a/h2b/h2c/h2d = **0 diffs**; revert hifi = **107,428 diffs** (matches repair's OLD binary exactly → revert reconstruction faithful).

## 7. Determinism
- 3 reruns per variant × 4 fixtures: all byte-identical by SHA-256 (84 comparisons, 0 mismatches).

## 8. Metrics (`src/analyze_all.py`) — full tables in VERDICT.md
- Per file: rail%, peak, RMS, crest, per-1s-window RMS ratio vs ctl (max dev dB), 9 bars.

## 9. Mix-level identity
- `f3mixdump` pre-emit mixes: h2a–d byte-identical to ctl on all 4 fixtures; h1 differs (re-staged plan — intended).
- Tournament: stock `render_par` vs H2-style variant (fixed 0.5 gain replacing the 0.85-FS peak normalizer in `wav_write` only; source at `build/render_par_h2.zag`):
  - `seq+mix` raw dumps: `cmp` → **byte-identical** (mix SHA `a30c6577e265152d0a3df1ffb77eb724321f5e5a1a39a49e1cf625a42b494117`).
  - `seq` WAVs differ (peak 27852 vs 21668) → genuine mastering change, mix untouched.
- Frozen `plan_v1.txt` H1-bound audit: 24 voices, max 2 simultaneous (bed + 1 event, no event–event overlap), authored worst-case **0.950 FS < 1.0** → complies with the H1 discipline already; rendered mix peak 43337 q16 vs bound 62259 q16 (1.44× headroom).
- SURFACED: tournament `render_par.zag` `wav_write` has its own output-derived 0.85-FS peak normalizer (`(mix*27852)/peak`) — the tournament's own gamma-disease instance.

## 10. Excerpts
- 7 clips under `excerpts/`, all `WITHHELD-NOT-FOR-REVIEW`, manifest with peak/rail%/RMS. Never presented to Micah.

## 11. Commit
- Committed source + evidence docs (no binaries, no .zagd, no .zag-cache, no WAV renders — all regenerable byte-identically from committed sources; SHAs recorded here).
- Tool: `TMPDIR=~/workspace/tmp_commit ~/workspace/commit_racefree.py tnn-native-lab <msgfile> <lab-relative paths>`; verified via GitHub branch read + content read-back.

## Files
- `src/`: field_ctl.zag, field_diag.zag, field_h1.zag, field_h2a/b/c/d.zag, field_revert.zag, patch_variant.py, h1_census.py, h1_restage.py, analyze_gate.py, analyze_all.py, analyze_gamma.py
- `build/`: binaries (NOT committed) + render_par_h2.zag (tournament H2 variant source)
- `out/`: per-variant renders, reruns (r2/r3), proof pairs, mixdumps (NOT committed — regenerable)
- `excerpts/`: withheld clips + manifest (clips NOT committed — withheld; manifest committed)
