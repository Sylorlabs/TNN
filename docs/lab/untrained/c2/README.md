# Workstream B — Confirmatory Run (c2): Untrained Structural Analysis of Novel Inputs

> **STATUS: BINDING CONFIRMATORY RUN.**
> This directory holds the binding Workstream B verdict, run under the
> remediated protocol after the exploratory run (`..`) was invalidated for
> freeze-violation, RNG-fixture, read-cap, and novelty-audit defects.

## Remediation (vs exploratory)

| # | Defect | Fix |
|---|--------|-----|
| 1 | Analyzer changed after real-input exposure | c2 analyzer (`tnn/uanalyze.zag`) frozen (SHA-256 in `tnn/FROZEN_SHA256.txt`) BEFORE any fresh input was acquired; frozen copy verified byte-identical to committed source |
| 2 | `smoke/loudclick.wav` used `np.random.RandomState(7).randn` | Replaced by analytical fixture (`smoke/gen_loudclick.py` documents the formula); 6 onsets @500 ms confirmed, byte-identical regeneration |
| 3 | Arbitrary caller read caps (4M/2M/300K) | `read_all` now does exact-size reads via `lseek(2)`; the ONLY limit is the znc `<2^25`-byte slice ceiling (load-bearing). Proven behavior-preserving: c2 binary reproduces all six exploratory outputs byte-identically |
| 4 | Invalid novelty audit (SHA-256 vs `git cat-file`) | Correct Git-blob audit: `git hash-object` IDs checked against the repo object store (all six 404 = novel) |
| 5 | Gallery provenance stale / not exact bytes | (gallery updated separately with exact fixtures + latest tip) |

## Added characterization

`tests/test_boundary.py` (7 analytical fixtures, all zero-RNG) locks in the
frozen analyzer's honest boundaries: RIFF chunk scanning, percentile/sort
correctness, leading-silence dynamic range, high-frequency pitch ceiling
(6 kHz -> 2 kHz subharmonic), long-period rhythm withholding, fine-detail
texture scale, deforming/churning motion. Report: `tests/boundary_report.txt`.

## Protocol (binding)

1. c2 analyzer frozen; binary built; smoke suite passes.
2. Six FRESH inputs acquired (different tracks/images/video from exploratory).
3. Human structural descriptions written from independent plots/views and
   SHA-256-sealed (`human/SEAL.log`, 2026-09-26 18:29:57 UTC) BEFORE any
   analyzer run on the inputs.
4. Each input run TWICE with the frozen binary; byte-identical required.
5. Claim-by-claim comparison (`compare/worksheets.md`), verdict (`compare/VERDICT.md`).

## Inputs

| ID | Source | Analyzed form |
|----|--------|---------------|
| B1 | archive.org "Surf" (91.0 s) | 16 kHz mono WAV |
| B2 | archive.org "Hoot Owl" (34.9 s) | 16 kHz mono WAV |
| B3 | archive.org "Helicopter Passes Overhead" (72.4 s) | 16 kHz mono WAV |
| B4 | Wikimedia "Forest in the mist 03.jpg" | 480x320 PPM |
| B5 | Wikimedia "Dune 45 in Sossusvlei at sunrise" | 480x320 PPM |
| B6 | Wikimedia "Tresaith Waterfall.ogv" (6.8 s) | 14 PPM frames @2fps |

Provenance (URLs, SHA-256, Git-blob novelty): `SOURCES.md`.

## Layout

- `tnn/` — confirmatory analyzer source (frozen copy + SHA-256) + binary SHA.
- `human/` — sealed human descriptions (6) + seal log + the plots/views used.
- `inputs/` — transport-normalized analyzed fixtures (WAV/PPM/frames) + raw originals (not committed).
- `out/` — TNN outputs (run 1 and run 2; byte-identical).
- `smoke/` — remediated synthetic fixtures (analytical `loudclick.wav` + generator).
- `tests/` — boundary characterization (script + report + fixtures).
- `compare/` — claim worksheets + BINDING verdict.
- `SOURCES.md` — original URLs + hashes + novelty audit.
