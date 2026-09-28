# Self-PAM push-to-100% — Round 2 adversarial expansion corpus

**Status: FROZEN 2026-09-27.** This corpus was frozen BEFORE any gate
measurement. No gate (current or fixed) has been run against it; a later
round measures the gates against this frozen set.

**Location:** `docs/lab/senses/pam-rebuild/selfpam/push100/expansion/`

**Generator:** `gen_expansion.py` (committed, frozen). Deterministic, zero
RNG: all variation comes from splitmix64 seeded by `MASTER = 20260927`,
per-pair seed = splitmix64 over (family stream, task id, pair index). No `random` module, no
wall clock, no dict-order dependence. Regeneration verified byte-identical
across 2 independent runs (`diff -r` clean).

**Regenerate:** `python3 gen_expansion.py <outdir>` then
`sha256sum -c MANIFEST.expansion.sha256` (from inside the corpus dir).

**Format:** each pair is `<name>.pair` + `<name>.pair.truth`, matching the
on-disk `round2/fixtures/r2p/` layout:
- 64-byte header: `R2P1`@0, task\<i32\>@4, idx\<i32\>@8, scene\<u64\>@12,
  f_len\<i32\>@20, g_len\<i32\>@24, 36 zero pad bytes @28..63
- then F bytes (f_len), then G bytes (g_len)
- truth file: `truth=`, `family=`, `task=`, `scene=`, `note=`
  (+ `calibration=1` for family 7)

Task ids: colordisc=0, colorconst=1, shapetrans=2, pitchdisc=3, timbredisc=4,
motiondir=5 (same as `round2/fixtures/gen_r2p.py`).

Payload encodings mirror `gen_r2p.py`: video spans are
`<IHH`(nframes,w,h) + raw RGB frames; audio spans are `<II`(rate,nsamples) +
i16-LE PCM.

**Corpus size:** 352 pairs (704 files).

---

## Family 1 — `fshuffle`: frame-shuffle (48 pairs)

- **Construction:** G = forward frame sequence (motiondir: white 2×2 dot
  moving E across 8 frames of 16×8 RGB; shapetrans: red 3×3 square
  translating E across 8 frames). F = the same frames in a deranged
  permutation p (Fisher–Yates + rejection sampling, deterministic).
- **Count:** 24 motiondir + 24 shapetrans.
- **Attacks:** order-blindness beyond simple reversal — the current gate
  judges `span_sum/8`, which cannot see permutation at all.
- **Assertion logic:** p has no fixed points, p ≠ identity, p ≠ reversal;
  frames pairwise distinct; sorted(F frames) == sorted(G frames); F ≠ G.
- **Truth:** `DIFFERENT`; note records the permutation and the G motion.

## Family 2 — `audiorev`: audio time-reversal (48 pairs)

- **Construction:** G = PCM (8000 Hz, 2000 samples): pitchdisc = 400→800 Hz
  rising glide (sine + 2nd harmonic, 10 ms ramps); timbredisc = bright
  pluck (4 harmonics, 5 ms attack, 60 ms exp decay). F = the sample sequence
  reversed in time (sample-level reversal, then re-packed as i16-LE —
  byte-reversal would corrupt sample endianness, so this is a true
  time-reversal).
- **Count:** 24 pitchdisc + 24 timbredisc.
- **Attacks:** order-blindness in the audio domain. The fact genuinely
  differs: rising vs falling glide; sharp-attack/decay vs
  slow-swell/abrupt-cutoff.
- **Assertion logic:** F samples == reverse(G samples) exactly; sample
  multiset identical; F ≠ G.
- **Truth:** `DIFFERENT`.

## Family 3 — `pxperm`: pixel permutation (48 pairs)

- **Construction:** G = frame(s) with spatial structure (colordisc /
  colorconst: 1 frame, left-red/right-blue split field; shapetrans: 8
  translating-square frames). F = pixels permuted within each frame by a
  fixed derangement q (same q every frame).
- **Count:** 16 colordisc + 16 colorconst + 16 shapetrans.
- **Attacks:** spatial-structure blindness — same pixel multiset, depicted
  layout destroyed.
- **Assertion logic:** per-frame pixel multiset identical; q has no fixed
  points; F ≠ G.
- **Truth:** `DIFFERENT`.

## Family 4 — `cycshift`: cyclic phase shift (48 pairs)

- **Construction:** F = G rotated left by N = len(G)//3 bytes
  (F = G[N:] + G[:N]).
- **Count:** 24 shapetrans (video payload) + 24 pitchdisc (PCM payload).
- **Attacks:** pure order-only difference; byte-sum blind by construction.
- **Assertion logic:** rotation exact; byte multiset identical; F ≠ G
  (G not periodic under this rotation — asserted).
- **Truth:** `DIFFERENT`; note records N.

## Family 5 — `blkswap`: block swap (48 pairs)

- **Construction:** F = G[m:] + G[:m] with m = len(G)//2.
- **Count:** 24 shapetrans + 24 pitchdisc.
- **Attacks:** coarse order-only difference; byte-sum blind.
- **Assertion logic:** block structure exact; byte multiset identical;
  F ≠ G.
- **Truth:** `DIFFERENT`; note records m.

## Family 6 — `sumswap`: sum-preserving targeted swap (48 pairs)

- **Construction:** F = G with two bytes at positions i≠j exchanged, where
  G[i] ≠ G[j] (positions drawn deterministically; rejection-sampled).
- **Count:** 24 shapetrans + 24 pitchdisc.
- **Attacks:** the CURRENT sum measurement directly — plain byte sum is
  preserved exactly, so `span_sum(F)/8 == span_sum(G)/8` while the depicted
  content differs at 2 positions.
- **Assertion logic:** plain sums equal exactly; exactly 2 byte positions
  differ; values at those positions differ; F ≠ G.
- **Truth:** `DIFFERENT`; note records i, j and the swapped values.

## Family 7 — `calib`: tolerance probes (40 pairs, CALIBRATION — not attacks)

- **Construction:**
  - 7a (idx 0–19): F = G byte-identical (must-admit controls; 10 shapetrans
    video + 10 pitchdisc audio, alternating).
  - 7b (idx 20–39): F = G with a single byte changed by exactly ±1
    (tolerance-boundary probes; sign chosen deterministically, clamped at
    0/255).
- **Count:** 20 + 20.
- **Purpose:** calibration. 7a must be admitted by any correct gate
  (identical spans ⇒ identical judgments). 7b probes the sum/8 quantization
  boundary: a ±1 sum change flips the judgment iff it crosses a multiple
  of 8.
- **Assertion logic:** 7a: F == G. 7b: exactly one byte differs, by exactly
  ±1.
- **Truth:** `SAME` with `calibration=1`; notes marked CALIBRATION.

## Family 8 — `wsumcol`: weighted-sum collision attempts (24 pairs)

**Honest result: SUCCEEDED — exact collisions constructed, not just
mod-2^31 / post-quantization near-misses.**

- **Construction:** positions p0 < p1 < p2 in arithmetic progression
  (p1 = p0+d, p2 = p0+2d, d=151) hold values (x, z, y) with **2y = x+z**
  (y the midpoint; per-pair x ∈ {16, 32, 48}, z = x+200, y = x+100).
  G has (x, z, y) at (p0, p1, p2); F applies the 3-cycle
  F[p0]=y, F[p1]=x, F[p2]=z. Four disjoint triples per pair → 12 bytes
  genuinely change value (e.g. 16→116, 216→16, 116→216).
- **Math (why it collides):** with A = p0+1, the position-weighted delta is
  ΔW = A(y−x) + (A+d)(x−z) + (A+2d)(z−y)
     = A(y−x+x−z+z−y) + d(x−z+2z−2y)
     = d(x+z−2y) = 0, since 2y = x+z.
  The plain byte sum is preserved because a permutation preserves the
  multiset. Hence **both** Σbᵢ and Σ(i+1)·bᵢ are identical **exactly**
  (not merely mod 2^31), so /8 quantization collides trivially.
- **Count:** 24 (shapetrans video payloads).
- **Attacks:** the *future* fixed gate (position-weighted sum): these pairs
  defeat it by construction while carrying a genuine fact difference
  (12 pixel bytes changed by large amounts).
- **Assertion logic:** plain sums equal exactly; weighted sums equal exactly
  (big-int, hence mod-2^31 and /8-quantized equal — both asserted);
  exactly 12 bytes differ; triples pairwise disjoint; F ≠ G.
- **Truth:** `DIFFERENT`; note records the triple positions, d, (x,z,y),
  and both sums.

---

## Manifest

`MANIFEST.expansion.sha256` holds SHA-256 for every file in this directory
(generator, this doc, all 704 corpus files). The manifest excludes itself.

## What this corpus does NOT contain

No gate was run against these pairs during construction — the corpus is
frozen pre-measurement. Expected behavior under the R2-3 instrument
(withhold iff F-blob and G-blob judgments differ) is a *prediction for the
later measuring round*, not a verified claim: families 1–6 and 8 should
withhold-fail the current sum gate (identical judgments on identical sums),
family 7a must admit, family 7b is a boundary probe.
