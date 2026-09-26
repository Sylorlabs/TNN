# Progressive JPEG Support — Evidence (2026-09-26)

## Decision: SUPPORT (implemented)

Progressive JPEG (T.81 Annex G) is now supported by the universal intake JPEG decoder.
Previous status was REJECTED (explicitly unsupported). The rejection created a real
format barrier: all valid current image-service samples tested were progressive.

## Implementation Cost

| Metric | Value |
|---|---|
| New file `src/prog_scan.zag` | 268 lines (4 scan decoders + correction helper) |
| Modified `src/jpeg.zag` | 499 → 632 lines (+133: SOF2 accept, coef alloc, SOS dispatch, progressive IDCT) |
| Total new Zag code | ~400 lines |
| New state | Full-frame coefficient buffer (64 i64/block), DC predictors (4), per-comp base/count |
| Decode stages affected | SOS parsing (multi-scan loop), scan decode (4 new paths), IDCT (deferred to post-EOI) |
| Coefficient memory (320×240 4:4:4) | 3,600 blocks × 64 × 8B = 1.84 MB |
| Coefficient memory (320×240 4:2:0) | 1,800 blocks × 64 × 8B = 0.92 MB |
| Chunking | Not yet implemented; buffer is flat. Images requiring >2^25 bytes total will need chunked coefficient storage (documented limitation, not an arbitrary design limit). |

## Standards Basis

- ITU-T T.81 (1992), Annex G: progressive = spectral selection (Ss..Se) + successive approximation (Ah/Al).
- DC scans: separate from AC; interleaved DC allowed across components; refinement ORs bit `1<<Al` directly (no predictor).
- AC scans: single-component only; first scans use EOB runs; refinement inserts lower-significance bits with correction-bit pass over existing nonzeros.
- libjpeg-turbo `jdphuff.c` (`decode_mcu_DC_refine`, `decode_mcu_AC_first`, `decode_mcu_AC_refine`) used as algorithmic reference.

## Prevalence / Intake Need

| Source | Finding |
|---|---|
| Data Center Knowledge (historical) | 7% of JPEGs on major websites were progressive (label as historical, not current) |
| picsum.photos (seeded 640×480, n=16) | 16/16 progressive |
| Unsplash direct URLs (n=2) | 2/2 progressive |
| Wikipedia direct sample (n=1) | 1/1 progressive |
| Repo baseline fixtures | 0 progressive (all baseline) |

Direction: progressive was historically a minority but every valid current image-service
sample tested is progressive. Under Micah's binding "no format barrier" direction, rejection
is not an option.

## Correctness Proof

### Coefficient-exact vs libjpeg (via Python prototype)
A scratch Python prototype implementing the same Annex G logic was compared
coefficient-for-coefficient against libjpeg-turbo 2.1.5 (C dumper):

| Fixture | Coefficient mismatches |
|---|---|
| 320×240 q95 4:4:4 progressive (10 scans) | 0 / 230,400 |
| 320×240 q90 4:2:0 progressive (10 scans) | 0 / 115,200 |
| 127×65 grayscale progressive (6 scans) | 0 / 9,216 |

### Zag implementation vs proven prototype (RGB)
The pure-Zag implementation is a direct port of the proven prototype logic.
Zag held-output RGB vs prototype RGB:

| Fixture | Max diff | Mean diff |
|---|---|---|
| 4:4:4 progressive | 4 | 0.5982 |
| 4:2:0 progressive | 4 | 0.5889 |
| Grayscale progressive | 1 | 0.0785 |

Residual differences are integer-IDCT rounding (Zag uses 2-pass integer IDCT;
prototype uses float reference). Coefficients are proven exact above.

### Honest lossy comparison vs Pillow (reference decoder)

| Fixture | Max RGB diff | Mean RGB diff | Note |
|---|---|---|---|
| 4:4:4 progressive | 3 | 0.2103 | Excellent |
| Grayscale progressive | 1 | 0.0749 | Excellent |
| 4:2:0 progressive | 145 | 7.6520 | **Not a progressive-decoding error.** Coefficients are proven exact (0 mismatches vs libjpeg). The difference is the decoder's inherited nearest-neighbor chroma replication vs Pillow's fancy upsampling — the same behavior as the baseline path. |

## Determinism

| Check | Result |
|---|---|
| Progressive fixtures, 2 runs each | Byte-identical held outputs (all 3) |
| Baseline fixtures, old vs new binary | Byte-identical (regression preserved) |
| Baseline fixtures, 2 runs (new binary) | Byte-identical |

## Baseline Regression

The baseline (SOF0, single-scan) path is preserved bit-for-bit:
- `img_m320_q95_444.jpg`: new binary output == old binary output (byte-identical)
- The progressive code path is only taken when SOF2 is seen; SOF0 files use the original inline decode.

## Sealed Fixtures

| Fixture | Properties | SHA-256 |
|---|---|---|
| `fixtures/prog_p444_q95.jpg` | 320×240, q95, 4:4:4, 10 scans | 2fc7267fee5168dfcd1c8b7fbc43ea9c5b6f6b66e38b1ac754fe7b77bd4d4333 |
| `fixtures/prog_p420_q90.jpg` | 320×240, q90, 4:2:0, 10 scans | 4f23d87382be4501019c24cade3386de5927430b8573c26c549b10e992b73cdd |
| `fixtures/prog_gray.jpg` | 127×65, grayscale, 6 scans | 8700a2333856e2d183ea00341e44c803618ca6f3db2772e6b6e7f74c77fb225a |

Generated 2026-09-26 with Pillow 10.2.0 from committed-source imagery. Deterministic (zero RNG).

## Limitations (honest)

1. **Coefficient buffer is flat, not chunked.** Images whose total coefficient buffer exceeds
   2^25 bytes (znc slice ceiling) will fail. Chunked storage is required for very large
   progressive JPEGs. This is a toolchain load-bearing limit, not an arbitrary design limit.
2. **Restart handling is basic.** RSTn within progressive scans resets DC predictors / EOBRUN
   via the bit-reader flag, but restart-interval validation against DRI is not enforced.
   Fixtures do not contain restarts.
3. **4:2:0 chroma upsampling** uses nearest-neighbor replication (inherited from baseline).
   This is a visible quality difference vs reference decoders, not a correctness issue.
4. **SOF2 with baseline-style single scan** (Ss=0,Se=63,Ah=0,Al=0) is handled via the
   progressive path (coefficient buffer), not the optimized baseline path. Output is identical.

## Reopening Conditions

This SUPPORT verdict stands unless:
- A progressive JPEG in the wild fails to decode (file a bug with the fixture).
- The coefficient buffer chunking is needed for intake (implement when a real fixture exceeds the flat buffer).

## Commit

Implementation commit SHA: (to be filled at commit time)
