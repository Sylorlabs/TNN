# V2-A Evidence — Run Digests

**Fork:** V2-A (adjudicator)  
**Date:** 2026-09-23  
**Toolchain:** ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Source SHAs (frozen)
- `src/vsense.zag`: cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e (byte-identical to R2-4 sense_r24.zag)
- `src/deliberate.zag`: 63228c648f4a87a37c7beeb5eb30f828d21b97663b6c94c111e98672862111b6 (byte-identical)
- `src/vgate_a.zag`: (to be computed)
- `src/R33_NATIVE_IO_V1.zag`: (byte-identical)
- `src/R33_NATIVE_SHA256_V2.zag`: (byte-identical)

## Build
- Binary: `/tmp/vga` (scratch, not committed)
- Build log: `/tmp/vga_build.log`

## Three Byte-Identical Runs (B6)
All three runs produced byte-identical outputs:

### Dispositions
- Run 1: `8e78aaf0053b17cd8e112f09acc0299c3ab71c9990e71da3291140addfa7aba6`
- Run 2: `8e78aaf0053b17cd8e112f09acc0299c3ab71c9990e71da3291140addfa7aba6`
- Run 3: `8e78aaf0053b17cd8e112f09acc0299c3ab71c9990e71da3291140addfa7aba6`
- **Unique SHAs: 1** ✓

### Ledgers
- Run 1: `aaf13a7150fefb42008d789d036d64356a22bf8c8173a21324f2e529e58561fe`
- Run 2: `aaf13a7150fefb42008d789d036d64356a22bf8c8173a21324f2e529e58561fe`
- Run 3: `aaf13a7150fefb42008d789d036d64356a22bf8c8173a21324f2e529e58561fe`
- **Unique SHAs: 1** ✓

**B6: PASS** — Three byte-identical reruns with digests.
