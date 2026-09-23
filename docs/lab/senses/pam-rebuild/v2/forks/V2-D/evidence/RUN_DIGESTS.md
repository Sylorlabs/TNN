# V2-D Evidence — Run Digests

**Fork:** V2-D (confidence-separation)  
**Date:** 2026-09-23  
**Toolchain:** ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Source SHAs (frozen)
- `src/vsense.zag`: cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e (byte-identical to R2-4 sense_r24.zag)
- `src/deliberate.zag`: 63228c648f4a87a37c7beeb5eb30f828d21b97663b6c94c111e98672862111b6 (byte-identical)
- `src/vgate_d.zag`: 3f3cdd3142d37076f32cdec0d54e923d6ad3dbf04bb235513378d5ddeaef08b7
- `src/R33_NATIVE_IO_V1.zag`: e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8 (byte-identical)
- `src/R33_NATIVE_SHA256_V2.zag`: 9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf (byte-identical)
- `src/lut.zag`: 9379d9880fd47a47557a0e619ba56d256d7a6e1f47e5584deba434f1db46a006 (vendored byte-identical from R2-4; vsense.zag imports it)
- `src/gcheck.zag`: 8cae32a86a3c4dbfe93026beb26d6361e37470b6eb3112fbd277ae3efb58b51b (vendored byte-identical from R2-4; vsense.zag imports it)

## Build (re-verified 2026-09-23)
- Clean build from repo file set: `znc vgate_d.zag` succeeds (analyzer warnings only).
- Rebuilt binary re-run on rebuilt records reproduces committed digests byte-identically:
  - Dispositions: `383b6e4f3b190bf4b3f54f1a313bcc1c8313d07831efce3b0ae554046406d9e9` ✓
  - Ledger: `bc2db09685d8a09c3c0c8ca93fba7c0fb899c1be695c6978c8f27f0d1d128989` ✓

## Three Byte-Identical Runs (B6)
All three runs produced byte-identical outputs:

### Dispositions
- Run 1: `383b6e4f3b190bf4b3f54f1a313bcc1c8313d07831efce3b0ae554046406d9e9`
- Run 2: `383b6e4f3b190bf4b3f54f1a313bcc1c8313d07831efce3b0ae554046406d9e9`
- Run 3: `383b6e4f3b190bf4b3f54f1a313bcc1c8313d07831efce3b0ae554046406d9e9`
- **Unique SHAs: 1** ✓

### Ledgers
- Run 1: `bc2db09685d8a09c3c0c8ca93fba7c0fb899c1be695c6978c8f27f0d1d128989`
- Run 2: `bc2db09685d8a09c3c0c8ca93fba7c0fb899c1be695c6978c8f27f0d1d128989`
- Run 3: `bc2db09685d8a09c3c0c8ca93fba7c0fb899c1be695c6978c8f27f0d1d128989`
- **Unique SHAs: 1** ✓

**B6: PASS** — Three byte-identical reruns with digests.
