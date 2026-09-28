# Wall-3 residual #5 — fix verification (RESULTS)

Workdir: `~/workspace/desynth_r2/w4_ext/`
Base: `extract_atom_v2_base.py` (byte-copy of `../base/extract_atom_v2.py`)
Patched: `extract_atom_v2.py` (diff: `extract_atom_v2.patch`, 47 lines)
Test sources: deterministic synthetic low-F0 WAVs in `test_wavs/` (sum of 8
fixed-phase harmonics, 1.5 spectral slope, gentle attack envelope — **no RNG**)
plus real corpus WAVs.

## 1. Crash reproduction (base script, before fix)

```
$ python3 extract_atom_v2_base.py test_wavs/synth_80hz.wav atoms_base/synth_80hz.bin
sr=44100 n=132300
measured f0=80.00 Hz T0=551.25 samples
harm: NBINS=551 rms=18419.5
Traceback (most recent call last):
  ...
  File "extract_atom_v2_base.py", line 212, in main
    h_padded[:NBINS] = harm
ValueError: could not broadcast input array from shape (551,) into shape (256,)
```

| source | f0 | NBINS | base |
|---|---|---|---|
| synth_80hz.wav | 80.0 Hz | 551 | **CRASH** `shape (551,) into shape (256,)` |
| synth_140hz.wav | 140.1 Hz | 315 | **CRASH** `shape (315,) into shape (256,)` |
| synth_172hz.wav | 172.2 Hz | 256 | OK — boundary, fits exactly |
| synth_200hz.wav | 200.0 Hz | 220 | OK |

## 2. After fix — low-F0 extraction succeeds (down to the 80 Hz organ floor)

Patched script, synthetic sweep:

| source | f0 | NBINS | SPEC_N | patched |
|---|---|---|---|---|
| synth_80hz.wav | 80.0 Hz | 551 | 1024 | **OK**, valid atom |
| synth_90hz.wav | 90.0 Hz | 490 | 512 | **OK** |
| synth_120hz.wav | 120.1 Hz | 367 | 512 | **OK** |
| synth_140hz.wav | 140.1 Hz | 315 | 512 | **OK** |
| synth_160hz.wav | 160.2 Hz | 275 | 512 | **OK** |
| synth_171hz.wav | 171.0 Hz | 258 | 512 | **OK** |
| synth_172hz.wav | 172.2 Hz | 256 | 256 (unchanged path) | **OK** |
| synth_200hz.wav | 200.0 Hz | 220 | 256 (unchanged path) | **OK** |

Structural validation of the previously-crashing outputs (parsed field by
field, trailer lands exactly at EOF):

| atom | magic/ver | NBINS | K×TEXLEN | harm_rms | tex_rms/harm_rms | all finite |
|---|---|---|---|---|---|---|
| synth_80hz.bin | 0x4D4F5441 / 2 | 551 | 8×256 | 619.8 | 0.150 | yes |
| synth_90hz.bin | 0x4D4F5441 / 2 | 490 | 8×256 | 619.8 | 0.150 | yes |
| synth_140hz.bin | 0x4D4F5441 / 2 | 315 | 8×256 | 619.8 | 0.150 | yes |
| synth_171hz.bin | 0x4D4F5441 / 2 | 258 | 8×256 | 619.8 | 0.150 | yes |

TEXLEN=256 in the file, K=8, the 0.15 texture mix and the 619.8 level-norm hold
exactly — measured semantics preserved on the new path.

**Determinism:** two patched runs on the 80 Hz source →
`55a7c86737613365945bb64112dccc034b198eb5595a6fa981e180643ccc83f0` twice
(byte-identical).

Note: a 100 Hz synthetic variant fails f0 estimation (`FAIL: no voiced f0
found`) **identically on base and patched** — its waveform fails the
pre-existing 2-zero-crossing period validation before the texture step. Test-
signal artifact, orthogonal to this residual, unchanged by the fix.

## 3. Byte-identity of existing atoms (base vs patched)

The four Wall-3 atoms (`atom2_rise`, `atom3_rise`, `atom4_decay`, `atom5_decay`)
have NBINS ∈ {200, 112, 47, 85} — all ≤ 256, so the patched script provably
executes the identical instruction sequence (the only changed lines sit inside
`if NBINS > TEXLEN:`, which is False). Their sources are documented in
`~/workspace/desynth_closure/wall3/PROVENANCE_NEW.md` (found after the first
draft of this report via a killed background search's partial output — the
claim below that they were "undocumented" was wrong and is corrected here):

| atom | source WAV |
|---|---|
| atom2_rise.bin | `audio_longhorizon/corpus/prosody/prosody-cremad-1011-NEU.wav` |
| atom3_rise.bin | `audio_longhorizon/corpus/speech/speech-e22-006.wav` |
| atom4_decay.bin | `audio_longhorizon/corpus/prosody/prosody-cremad-1009-FEA.wav` |
| atom5_decay.bin | `audio_longhorizon/corpus/prosody/prosody-ravdess-2-04.wav` |

Direct re-extraction of **all four** with base and patched scripts gives
byte-identical output (4/4, see §3 table). The measured harmonic stacks are
bit-comparable before and after the fix — no deviation to explain.

| source | NBINS | base SHA-256 | patched SHA-256 | match |
|---|---|---|---|---|
| prosody-cremad-1011-NEU.wav (**atom2_rise**) | 200 | = | = | **identical** |
| speech-e22-006.wav (**atom3_rise**) | 112 | = | = | **identical** |
| prosody-cremad-1009-FEA.wav (**atom4_decay**) | 47 | = | = | **identical** |
| prosody-ravdess-2-04.wav (**atom5_decay**) | 85 | = | = | **identical** |
| child-fsd50k-171101.wav (atom0) | 112 | d1ee1896…5d8542 | d1ee1896…5d8542 | **identical** |
| speech-e22-000.wav (atom1) | 95 | e411c24e…5c9ef2 | e411c24e…5c9ef2 | **identical** |
| synth_172hz.wav (NBINS=256 boundary) | 256 | f55a3b19…499ffd67b | f55a3b19…499ffd67b | **identical** |
| synth_200hz.wav | 220 | 66b64b4f6…73f7b2d3 | 66b64b4f6…73f7b2d3 | **identical** |
| lowf0-ptdb-000-M09_sa1.wav (real corpus) | 141 | bb189119…5f7b2e3a5 | bb189119…5f7b2e3a5 | **identical** |
| lowf0-ptdb-016-M01_si459.wav (battery tgt) | 105 | b6957ba7…4229d09a8 | b6957ba7…4229d09a8 | **identical** |
| speech-e22-022.wav (battery tgt) | — | d59deba4…920dfadf | d59deba4…920dfadf | **identical** |

Zero deviation on the unchanged path — all four Wall-3 atoms re-extract
byte-identically with the fix (`atoms_wall3_base/` vs `atoms_wall3_fixed/`).

## 4. Explained deviation: base re-extractions vs committed fixtures

Fresh base-script extractions of atom0/atom1 do **not** match the committed
fixtures (`atom0`: d1ee1896… vs 05f95cf1…; `atom1`: e411c24e… vs 8ea7e03d…).
This is pre-existing and fully explained, not caused by this fix:

- The repo's `src/extract_atom.py` (used for the fixtures) is the pre-level-norm
  version; `base/extract_atom_v2.py` adds the documented Wall-3 defect-#1 fix:
  uniform scaling of all amplitude components to REF_RMS=619.8.
- Verified: T0 and NBINS are bit-identical between fixture and re-extraction;
  `harm` and `tex` differ by a **perfectly uniform** scale factor
  (min ratio == max ratio == 0.999955 = 619.8/619.8279, zero spread).

## 5. Files delivered

- `extract_atom_v2.py` — patched extractor (full file, drop-in replacement)
- `extract_atom_v2_base.py` — pristine base copy (reference for the diff)
- `extract_atom_v2.patch` — unified diff base → patched
- `ANALYSIS.md` — root-cause analysis
- `RESULTS.md` — this file
- `test_wavs/` — deterministic synthetic low-F0 sources (80–200 Hz)
- `atoms_base/`, `atoms_fixed/` — before/after extraction outputs
- `atoms_wall3_base/`, `atoms_wall3_fixed/` — the 4 Wall-3 atoms re-extracted
  with base and patched (byte-identical pairs)

## Correction log

- v1 of this report claimed the Wall-3 atom sources were undocumented in the
  repo. Wrong: they are documented in
  `~/workspace/desynth_closure/wall3/PROVENANCE_NEW.md` (with source SHAs and
  a 4/4 byte-identical re-extraction proof). The direct 4-atom verification in
  §3 supersedes the path-equivalence argument as the primary evidence.

## Conclusion

Residual #5 is closed: the crash mechanism is the fixed 256-sample FFT pad
buffer vs the F0-determined NBINS; the adaptive-grid fix removes it at the
coupling point, extracts valid atoms down to the 80 Hz organ floor, leaves the
atom binary format untouched, and re-extracts every existing atom
byte-identically.
