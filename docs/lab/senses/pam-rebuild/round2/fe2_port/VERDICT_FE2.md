# VERDICT_FE2 — FE2 separator port, Crew 1 (Round 3)

Date: 2026-09-24 (America/Los_Angeles)

## Frozen protocol (PREREG_FE2_PORT.md, commit f8e4dfa5d444b30f8668d0bf445e64dcb69af539)

- 11 FE1 SEPARATOR specs ported into sense formation (pure Zag, zero RNG).
- COL-5 excluded as DEFENSE-SCOPE (explicit refusal, exit 3).
- Held-out: indices 24–47 per family, 24 fixtures/family, 264 total.
- Held-out target manifest SHA-256: `60d4a912432bbc92ba04e200cf34fe117f9726f996b24c5fd8c5d95c6030682a`
- Per-family SURVIVE iff: (1) FE2 ≥20/24, (2) FE2 ≥ baseline, (3) if baseline <20/24 then FE2 leads by ≥4/24.
- Program USEFUL iff ≥9/11 survive.
- All held-out FE2 predictions byte-identical across three runs.

## Implementation

Source: `fe2.zag` (pure Zag, pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
Source SHA-256: `0a5063ab43eaf39816cf139bf537feaaf1f771631b0ae829fb817a7cf54b8933`

Mechanism notes (all faithful to frozen FE1 audit specs, extracted by script from
`PREREG_FE1_AUDIT.md` / `VERDICT_FE1.md` / `audit_fe1.py`):
- PTC-4: FFT-free spectral correlation, zero-padded DFT, threshold 0.7.
- PTC-5: segA vs segB correlation excluding the [3400,4600) region (concatenated local-time indexing, exactly as the frozen Python reference).
- TMB-4: fixed-point harmonic-sum pitch detector (decimated /8, exact fixed-point arithmetic).
- TMB-5: full-rate direct DFT, 1 Hz bins 0–8000 Hz, stable f64 phase recurrence, spectral centroid vs 1600 Hz. (Decimated /8 and 5 Hz variants rejected: aliasing bias.)
- COL-4: RGB histogram distance, threshold 0.5.
- CCN-3: LAB-space ΔE, banker's rounding, threshold 2.0.
- CCN-4: LAB-space ΔE, threshold 2.0.
- SHP-4: Hu-moment shape classifier.
- SHP-5: Hu-moment shape classifier (finer grid).
- MOT-4: optical-flow direction, 8-way.
- MOT-5: optical-flow direction with STILL.

Build self-check (indices 0–23, frozen FE1 fixtures): **264/264** FE2 predictions match the FE1 audit separators exactly (11/11 families 24/24).

## Held-out results (indices 24–47)

| Family | FE2 | Baseline (sense) | Bar a (≥20) | Bar b (≥base) | Bar c (margin) | Verdict |
|--------|-----|------------------|-------------|---------------|----------------|---------|
| PTC-4  | 24/24 | 20/24 | ✓ | ✓ | n/a (base≥20) | SURVIVE |
| PTC-5  | 24/24 | 24/24 | ✓ | ✓ | n/a (base≥20) | SURVIVE |
| TMB-4  | 24/24 | 12/24 | ✓ | ✓ | ✓ (+12) | SURVIVE |
| TMB-5  | 24/24 | 8/24  | ✓ | ✓ | ✓ (+16) | SURVIVE |
| COL-4  | 24/24 | 11/24 | ✓ | ✓ | ✓ (+13) | SURVIVE |
| CCN-3  | 24/24 | 12/24 | ✓ | ✓ | ✓ (+12) | SURVIVE |
| CCN-4  | 24/24 | 11/24 | ✓ | ✓ | ✓ (+13) | SURVIVE |
| SHP-4  | 24/24 | 8/24  | ✓ | ✓ | ✓ (+16) | SURVIVE |
| SHP-5  | 24/24 | 8/24  | ✓ | ✓ | ✓ (+16) | SURVIVE |
| MOT-4  | 24/24 | 12/24 | ✓ | ✓ | ✓ (+12) | SURVIVE |
| MOT-5  | 24/24 | 11/24 | ✓ | ✓ | ✓ (+13) | SURVIVE |

- **Survived: 11/11. USEFUL: True** (≥9/11 required).
- FE2 total: **264/264**. Baseline total: **137/264**.

## Determinism

Three complete held-out runs, byte-identical:
- run 1: `dee3d8adefc683ac57a481153d16cb5fe52098737c6ac4a743af01791c886580`
- run 2: `dee3d8adefc683ac57a481153d16cb5fe52098737c6ac4a743af01791c886580`
- run 3: `dee3d8adefc683ac57a481153d16cb5fe52098737c6ac4a743af01791c886580`
- 3× byte-identical: True.

## COL-5 negative control

`fe2 COL-5 <fixture>` → exit code **3**, stderr contains `COL-5 is defense-scope`, no prediction emitted. COL-5 remains defense-scope per the frozen exclusion.

## Files

- `fe2.zag` — implementation source
- `specs.json` — script-extracted FE1 specs
- `extract_specs.py` — extraction script
- `selfcheck.py`, `run_verdict.py` — harnesses
- `baseline.json` — held-out sense baseline (137/264)
- `heldout_MANIFEST.sha256` — frozen held-out manifest
- `predictions_run1.txt` (run2/run3 byte-identical) — 264 predictions
- `verdict.json` — machine-readable verdict
- `PREREG_FE2_PORT.md` — frozen prereg (committed alone as f8e4dfa5d444b30f8668d0bf445e64dcb69af539)

## Build

```
cd <build>  # with R33_NATIVE_SHA256_V2.zag + R33_NATIVE_IO_V1.zag beside fe2.zag
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 fe2.zag -o fe2
./fe2 <FAMILY> <fixture> [<fixture> ...]
./fe2 COL-5 <fixture>   # refuses, exit 3
```
