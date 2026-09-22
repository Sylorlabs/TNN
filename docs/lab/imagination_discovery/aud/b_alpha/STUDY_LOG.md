# Fork B-α — Study Log

**Position:** (b) study-then-invent, pure. "You can't imagine what you've never understood."
**Date:** 2026-09-22
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pure Zag, zero RNG in decision paths)

---

## Study sets (local only — never committed)

### Set 1: Playground (Test 1 — kids playing and laughing)

| File | Material | Duration | Source / license |
|---|---|---:|---|
| `w1.wav` | Berlin playground | 92.389 s | Wikimedia Commons, CC0 |
| `w2.wav` | Dozen children on playground | 48.849 s | Wikimedia Commons, public domain |
| `w3.wav` | Four-year-old laughing | 11.260 s | Wikimedia Commons, CC BY 3.0 |
| `w4.wav` | Children playing in park | 30.034 s | Wikimedia Commons, CC BY-SA 4.0 |
| `w5.wav` | Children playing janken | 9.809 s | Wikimedia Commons, CC BY-SA 4.0 |

All converted to 44.1 kHz mono PCM16. Total: ~192 s.

**Catalog (`catalog.bin`, BAL2 format):** 131 atoms, 13 quiet texture chunks.
- 95 voice-like events → 4 descriptor clusters (sizes 22 / 18 / 25 / 30)
- Descriptor-derived class proxies: 32 laugh-like, 63 call-like, 36 foot/impact-like
- **Caveat:** classes/clusters are descriptor proxies, not human-verified identities.

### Set 2: Planet (Test 2 — Kethra's planet voice)

| File | Material | Duration |
|---|---|---:|
| `p1.wav` | Mars wind | 40.0 s |
| `p2.wav` | Mars dust devil | 27.0 s |
| `p3.wav` | Ice crackling | 74.1 s |
| `p4.wav` | Storm / thunder | 302.8 s |

**Catalog (`catalog2.bin`):** 74 atoms, 88 texture chunks (10.6 MB).

### Set 3: Ocean/vocal (Test 3 attempt — SUPERSEDED)

| File | Material | Duration |
|---|---|---:|
| `o1.wav` | Tropical ocean | 384.3 s |
| `o2.wav` | Sea waves | 20.9 s |
| `o3.wav` | Throat singing | 18.8 s |
| `o4.wav` | Whale song | 52.7 s |

**Catalog (`catalog3.bin`):** 281 atoms, 18 texture chunks.

**⚠️ INVALIDATED:** Using ocean/wave recordings as study inputs for "an alien ocean's surf"
violates the explicit "no direct study referent" requirement. `catalog3.bin` and the
`score_ocean` render are retained as a negative control (what the invalid path sounds like)
but CANNOT support Test 3. The valid Test 3 (`score_alien`) uses ONLY catalog2
(Mars wind/dust-devil/storm/ice — no ocean material whatsoever).

---

## Study pipeline (`src/study.zag`)

1. **10 ms amplitude analysis** with hysteretic segmentation.
2. **Dense-material guard** based on sampled p90 RMS (prevents over-segmentation of beds).
3. **Overlong-event splitting** with guaranteed progress.
4. **Descriptors per event:** duration, peak, RMS, ZCR, spectral-tilt proxy, attack.
5. **Descriptor-based classes:** laugh-like / call-like / foot-impact-like (proxies).
6. **Deterministic 4-cluster k-means** on voice-like events.
7. **Class bigrams** (16) and **timing-gap quantiles** (12: p10/p50/p90 per class) — the "grammar."
8. **Catalog:** whole event waveforms + quiet texture chunks + grammar. BAL2 format adds
   per-atom source-file index.

**Determinism:** Study is deterministic from inputs (zero RNG). Catalog SHA-256 recorded
at build time.

---

## Compiler issues encountered (documented for the record)

1. **BAL2 header-patch bug (my code, not compiler):** `study.zag` wrote the initial header
   as BAL2 but the end-of-run header-patch (final counts) still stamped BAL1. Fixed.
2. **ZNC bed() miscompile (compiler bug):** In the large render binary, `bed()`'s inner loop
   panicked "slice index out of bounds" on a provably valid index (verified: idx=10,516,968
   < len=10,584,000). Minimal reproducer with identical logic/data worked. Workaround:
   restructured so `bed()` is called directly from `main()` (not via `score_*()`), with
   catalog loading inlined in `main()`. Deterministic builds (same SHA) reproduce the panic
   in the old structure and success in the new. Characterized 2026-09-22.
3. **txwave arena overflow (my code):** catalog2's textures total 10.6 MB > 4 MB arena.
   Enlarged to 12 MB. Similarly enlarged audit's study arena to 24 MB.
4. **atab field overlap (my code):** `fno` at offset 20 collided with `woff` u64 at 16.
   Moved to offset 12.
