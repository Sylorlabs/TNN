# B-β study log

## 2026-09-22 — kids benchmark study

**Tools** (local, deterministic, never committed): `work/probe.py`,
`work/study_kids.py`, `work/analyze.py`, `work/mine_bed.py`.

**Source statistics** (uniform s16 mono 44.1 kHz staging in `work/wav/`):

| File | Peak | RMS | ZCR | Notes |
|---|---|---:|---:|---|
| `kids_park.wav` | 24,611 | 3,168 | 0.043 | loud group moments ~10.4 s, 22–26 s |
| `kids_playground.wav` | 23,359 | 2,606 | 0.040 | loudest block ~24 s |
| `kid_laugh.wav` | 31,455 | 2,242 | 0.070 | laugh clusters 0.35–1.9, 3.2–4.0, 9.25–11.15 s |

**Event mining** (`study_kids.py`): onset detection (envelope flux,
median+4·MAD, ≥150 ms gaps) + deterministic spectral clustering on
[log centroid, log duration, log RMS] with k-means++ seeded fixed.

**Catalog** `catalog_kids.bin`: 85 × 20-byte records
(start_u32, end_u32, src_u16, voice_u16, peak_u16, centroid_u16, durms_u16,
flags_u16). Voice assignment:

- voice 0 (PIP): `kid_laugh` — documented single 4-year-old; 11 events
- voices 1/2: `kids_park` centroid clusters (8 + 6 events)
- voices 3/4: `kids_playground` centroid clusters (~20 + ~12 events)
- voice 5: distant calls from `kids_berlin` (background)
- voice 8: 12 quiet "air" bed segments mined by `mine_bed.py`
  (lowest-energy non-overlapping 1.5–2.5 s windows, berlin + playground)
- voice 9: 7 real footstep events (1 gravel + 6 from `forest_track4`)

**Corrections during study:**
- A first attempt classified sharp vocal attacks as footsteps; caught on
  inspection and removed — feet come only from footstep recordings.
- Honesty boundary: clustering suggests voice *groups*; only voice 0 has
  documented single-speaker provenance. Character assignment (PIP/WREN/ASH)
  is dramaturgical, recorded as such in DERIVATION_kids.md.

**Production tools** (frozen with the piece):
- `assemble.zag` + `mech_kids.zag`: pure-Zag event assembler, seed 20260922
- `work/nocopy.py`: no-copy audit (2 s windows, NCC < 0.75)
- `work/social_check.py`: 8 social-falseness gates (S1–S5 + lineage)
- `../native_check.py`: A-NATIVE verifier

## Open study items (Tests 2–3)

- Catalog the ocean/animal/voice sources (`ocean_tropical`,
  `sea_waves`, `loon_yodels`, `throat_singing`, `whale_song`) with the
  same onset+cluster pipeline, extended for long gestures (whale/loon
  phrases are 2–10 s; the 150 ms minimum gap is wrong for them).
- Study surf morphology: what makes a wave event (attack/decay/asymmetry)
  from `ocean_tropical` + `sea_waves` before Test 3 mechanisms are written.

## 2026-09-22 — Kethra/ocean study (done)

**Tool:** `work/study_kethra.py` (deterministic; O(n) cumsum envelopes —
an early `np.convolve` version was killed after it proved O(n·k)).

**Catalog** `catalog_kethra.bin`: 48 × 20-byte records. Flags: bit1
vocal (2), bit2 swell (4), bit3 crash (8), bit4 bed (16).

| Voice | Source | Records | Content |
|---|---|---:|---|
| 11 loon | `loon_yodels` | 7 | discrete rising yodel gestures (onset-bounded, 400 ms min gap) |
| 12 whale | `whale_song` | 9 | phrases (600 ms min gap) |
| 13 throat | `throat_singing` | 4 | 3 s sustained drones, lowest spectral variance |
| 14 swell | `ocean_tropical` + `sea_waves` | 8+3 | 16 s windows at envelope maxima; sea_waves long events |
| 15 crash | `ocean_tropical` | 12 | wave-crash attacks via 0.5 s rise detector (p99.5, 4 s separation) |
| 16 air | `ocean_tropical` | 5 | lowest-energy 2 s windows |

**Corrections during study:** the first crash miner (absolute envelope
threshold) found 0 events — surf is too continuous; replaced with a
rise-based detector (32 strong rises found, 12 catalogued). Throat drone
mining returned 4 non-overlapping windows, not 6 (18.8 s file limits it);
documented, not padded.

**Production:** `mech_kethra.zag` + `mech_ocean.zag` share the assembler
core; per-piece helpers only (`ktab_new`, `kbcount`/`kbkth`). Placement
logs: `work/place_kethra.log` (51), `work/place_ocean.log` (40).
