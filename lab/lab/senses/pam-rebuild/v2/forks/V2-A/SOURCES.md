# V2-A Sources — Build Manifest

**Fork:** V2-A (adjudicator) | **Date:** 2026-09-23

## src/ (all buildable from this directory with znc)
| File | SHA256 | Provenance |
|------|--------|------------|
| vsense.zag | cf4ffb43…997a78e | Byte-identical to R2-4 `sense_r24.zag` |
| deliberate.zag | 63228c64…b97663b6 | Byte-identical to R2-4 `deliberate.zag` |
| vgate_a.zag | ebcfaf9d…0182a0f1 | Fork's gate + adjudicator (this fork's mechanism) |
| R33_NATIVE_IO_V1.zag | e6379ddb…641e9f61d8 | Byte-identical to R2-4 (substrate) |
| R33_NATIVE_SHA256_V2.zag | 9824f6db…7ca683bcf | Byte-identical to R2-4 (substrate) |
| lut.zag | 9379d988…46a006 | Vendored byte-identical from R2-4 (vsense.zag imports it) |
| gcheck.zag | 8cae32a8…3efb58b51b | Vendored byte-identical from R2-4 (vsense.zag imports it) |

Build: `cd src/ && znc vgate_a.zag -o vgate_a` — succeeds (analyzer warnings only).
Re-verified 2026-09-23: rebuilt binary reproduces committed disposition/ledger digests byte-identically.

## evidence/
- RUN_DIGESTS.md (digests + source SHAs, re-verified)
- VERDICT_V2-A.md (DEAD on RK-3)
- metrics.json (frozen bars)
- EXPOSURE_CORRELATED_FAILURE.md (known exposure, documented)

## Deferred: none. Fork is complete and buildable.
