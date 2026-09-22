# SENSES_UNLIMITED — format spec: u4f + ufreq (2026-09-22)

Binding for the pure-Zag implementation `senses_unlimited/src/uspec.zag`.

## u4f — multi-spectral image field

- Grid W×H cells, 10 channels/cell, i64 per channel, little-endian in a `[]u8` arena.
- Cell stride 80 bytes; channel `c` of cell `(x,y)` at `(y*W+x)*80 + c*8`.

| ch | name | band / meaning | unit | range |
|---|---|---|---|---|
| 0 | R_VIS | 380–750 nm | millionths of scene reference | i64 (≥0; <0 sets SATFLAG) |
| 1 | G_VIS | 380–750 nm | millionths of scene reference | i64 |
| 2 | B_VIS | 380–750 nm | millionths of scene reference | i64 |
| 3 | UV | 10–380 nm | millionths of scene reference | i64 |
| 4 | NIR | 750 nm–2.5 µm | millionths of scene reference | i64 |
| 5 | XRAY | 0.01–10 nm, attenuation-as-data | millionths of scene reference | i64 |
| 6 | DEPTH | distance | micrometers, i64 | i64 (signed OK) |
| 7 | ALPHA | coverage | millionths | i64 |
| 8 | ROUGH | roughness | legacy 0..1000 scale, uncapped | i64 |
| 9 | SATFLAG | bitmask: bit c = channel c hit a boundary | bits | i64 |

Rules:
- EM channels 0–5: values > 1_000_000 are LEGAL (brighter than reference — no 255 ceiling).
  Negative EM energy is domain-invalid: the value is still stored (representation never
  refuses) AND the SATFLAG bit is set. Represented + flagged, never silent.
- `u4_add` uses checked arithmetic: overflow saturates at i64 max/min and sets SATFLAG.
  Nothing wraps.
- Out-of-bounds cell/channel access returns a status code (-1); nothing is written.

## False-color emission (declared mappings, never silent)

| id | name | mapping | purpose |
|---|---|---|---|
| 1 | HUMAN | (R_VIS,G_VIS,B_VIS) → RGB, scale 255/1e6 | what a human sees |
| 2 | BEE | UV→B, NIR→R, G_VIS→G | bee-visible structure |
| 3 | XRAY | XRAY → grayscale | attenuation view |

- Render clips channel values > 1e6 ONLY in the emitted BMP (the field keeps true values).
- Every BMP ships with a `.txt` sidecar: mapping id, scale, clipped-pixel count,
  satflag-pixel count. An RGB-only consumer that ignores the sidecar is lying to
  itself; the record exists.

## ufreq — unbounded-frequency signal atoms

- Atom = 40 bytes: `freq_hz:i64 @0`, `amp:i64 @8` (millionths), `phase_pm:i64 @16`
  (0..999), `t0_us:i64 @24`, `t1_us:i64 @32`. Waveform = sine LUT (DECLARED;
  the non-fixed-waveform replacement is a separate track).
- `freq_hz` is i64: 0..9.2e18 Hz (covers radio through ~38 MeV gamma). The i64
  boundary is DOCUMENTED (AUDIT.md S2); values beyond it cannot be constructed —
  the constructor returns status 2. Never wrapped.
- Arena: 1024 atoms; `uq_add` returns 0 ok / 1 full / 2 freq-out-of-range. Explicit.
- Time in µs (i64): ±292,000 years. No duration clamp.

## Pitch-shift emission (declared mapping)

- Per BAND: `k` = smallest integer with `(maxf >> k) < 20000`. Rendered freq =
  `(freq_hz + 2^(k-1)) >> k` (ROUNDING shift, not truncation — halves quantization;
  fidelity and render use identical shifted values).
- Bands (declared partition): A < 2 MHz (AM), B 2 MHz–2 GHz (FM/GPS), C ≥ 2 GHz.
  Each band emits its own WAV with its own k. The single-shift full-spectrum
  mapping FAILED the fidelity bar (2026-09-22: low bands collapsed); multi-band
  is the repair. The failure is preserved in RESULTS.md, not rewritten.
- The WAV filename contains the band; the sidecar records k, original `[fmin,fmax]`,
  and the fidelity number per band. Shifted files are never presented as the signal.
- Fidelity metric (integer): over all atom pairs with `fi/fj ≤ 1e6`,
  `r_pm = (fi/fj)*1000 + ((fi%fj)*1000)/fj`, same for shifted; per-pair error
  `e = |rs_pm − ro_pm|*1000 / max(ro_pm,1)`; report max e in permille.
  BAR: max e < 10 permille (1%). Ratios are what survive transposition; absolute
  pitch is the declared casualty of the mapping.
- Render clip: IMPOSSIBLE by construction — peak-normalized to 24000 < 32767, so
  the 16-bit WAV stage cannot clip. Atoms keep true amplitudes regardless.

## Probes

- **P1 city-radio**: 14 atoms — FM 88–108 MHz ×5, AM ×3, GPS 1575.42 MHz,
  WiFi 2.412/2.437/2.462 GHz with burst windows, microwave 2.45 GHz, 5 GHz ×2.
- **P2 bee-vision**: 64×64 u4f — UV-bright sky, 3 flowers with UV nectar guides,
  NIR-bright foliage. Renders BEE + HUMAN BMPs. Metrics (permille):
  M1 = UV nectar contrast; M2 = same contrast on HUMAN render's blue channel
  (expect ≈0: proves the structure is UV-only, invisible to RGB).
- **P3 2.4GHz-band**: 20 atoms — ISM band composition. Shift-render WAV for ears;
  ratio-fidelity measured on atoms.
- **rt**: round-trip battery — u4f paint→readback arena equality; ufreq
  add→readback; fidelity bar; SATFLAG behavior; oob status codes.
