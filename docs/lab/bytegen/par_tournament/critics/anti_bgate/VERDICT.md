# CRITIC 1 (anti-B-gate) — VERDICT

**Classification: BEAT**

Contender F ("FLAT"): flat sorted timeline, no fixed render regions, region
resets, allocations, or prefix resimulation. Pure Zag, zero RNG, pinned
compiler `znc_linux_x86_64_abed8aa1`.

Prereg: `fd61a6b6b792e8e9aa50944dab002eed053173f1`
(`docs/lab/bytegen/par_tournament/critics/anti_bgate/PREREG_CRITIC.md`)

Final source SHA-256: `5f79b784ed81d4d8170ec55cb307a87daccdba4bcac2b2420a3ae65657cc2470`
Final binary SHA-256: `e9eae2a1bd3ce1b851d77b07ef04771aa06ebf46f93a4edf921ae120f6892360`

## Strict-win axis (COST)

Prereg bar: ≥1.5× faster than B on 30 s, preserving all other frozen bars and
fixture byte identity.

Final interleaved 30 s timing, N=9 (same frozen fixture, same battery):
- B mean 3.963 s, stdev 0.794
- F mean 2.133 s, stdev 0.303
- **F speedup: 1.858×** — clears the 1.5× bar.

(An earlier optimized build measured 1.908×; the final binary with the
`[]i64` LUT and `>>22` strength reductions measures 1.858×. Both clear the bar.)

The speed comes from: (1) flat single-pass timeline (no per-region
allocation/reseed/resimulation), (2) `[]i64` sine LUT (clean indexed reads,
no byte-unpack), (3) specialized `voice_bed` (3-harmonic closed form),
(4) `>>22` strength-reduced LUT indexing. All proven fixture-byte-identical.

## Fixture byte identity (B1)

- F frozen mix SHA-256: `b7d3a71ebc9066b46a7c493a8cc0c8fe26fa017b22fcba4b2f4de49df9cd8784`
  — exactly the frozen B mix SHA.
- 20/20 rerenders byte-identical to B reference (cmp, no diff).
- WAV output byte-identical to B.

Because the waveform is byte-identical, F exactly reproduces B's analyzer
results (analyzer-first, no listening claims):
- All 9 gates pass with frozen values (PER 0.324, STA 1.841, LURCH 2.373,
  DRIFT 383.553, FLUXm 213.116, SIL1/2 0, CLIP 0.915, CREST 3.860).
- CHOP: 0 discontinuities, no ≥150 ms gaps, 16 flux spikes / 0 unexplained.
- Coherence: xcorr 1.000000, pitch-contour 1.000000, IOI-contour 1.000000.
- RT-LONG: 440 Hz, +0.00¢ (FFT; autocorrelation locks to the 110 Hz bed and
  is not used — matches crew_b's caveat).
- RT-CASCADE (correct i64 postcut checker): 1-bit fault 1 fault-window / 0
  post-fault; 4096-burst 4096/0; 512-dropout 512/0; 1 s DC 44100/0.
- RT-EDGE: 0 pre-14.8 s diffs, cut step 0, bed ends at zero.
- Order permutations (reverse + deterministic shuffles): byte-identical.

## Deliberate differences (preregistered)

F removes the render-layer `[40,4000]` pitch clamp; parser safety rail
`[0,20000]` honored. Decision-layer latch vetoes preserved exactly.

1. **Honest 30 Hz**: no-vibrato 30 Hz EVENT → F renders 30.0 Hz (FFT),
   B clamps to 40.0 Hz.
2. **Honest 5000 Hz**: no-vibrato 5000 Hz EVENT → F renders 5000.0 Hz,
   B clamps to 4000.0 Hz.
3. **Latch parity**: all 8 trap/lie latch decisions byte-identical to B
   (normalized stdout diff). Latch vetoes (output-veto, nominal-lie) behave
   identically; only the render layer differs.

Note on vibrato at high f0 (shared B/F behavior, not a divergence): B's
vibrato is FM with depth in cents → modulation index scales with f0. At
5000 Hz / 15 cents, β≈49.6 rad suppresses the carrier (sidebands ±~260 Hz).
The honest-rendering claim is verified on no-vibrato probes; the FM
vibrato itself is B's math, preserved exactly.

## B-bug fix: overlapping-note attack (found during red team)

**B drops the attack of overlapping notes at region boundaries.**
When an overlapping event starts in region k but region k's main loop exits
(after the bus span reaches R1) before visiting it, the overlay deferral
never happens for region k. The note is only rendered from region k+1's R0.

Proven: `iso_pair` (220 Hz 20.60–21.10 + 233.08 Hz 20.95–21.45). B renders
the overlapping note as [21.00, 21.45) — its [20.95, 21.00) attack is
silent. F renders the full [20.95, 21.45).

This is a strict improvement: B's region architecture leaks into the
musical result (a note loses up to 3 s of attack depending on region
alignment). F's flat timeline has no regions, so no such leak is possible.

The frozen fixture has 0 overlapping pairs, so B1 is unaffected. `leak_chain`
(4 overlapping pairs) is the only battery plan where F and B differ, and
the difference is F being correct.

## Red team / fuzz

- 14/14 `fz_*` plans complete without timeout/crash.
- F vs B byte identity: 12/14. The 2 differences are the intended
  honest-rendering (`fz_rail_freq`: 1e18 Hz EVENT → parser rail 20000 Hz,
  F renders 20000 vs B's 4000; `fz_resp_bad`: malformed response windows).
- Corrupt plan (invalid UTF-8 + huge freq): graceful degradation, no
  crash/hang, deterministic; rerender of clean fixture byte-identical.
- Polyphony/sub-octave probes: F/B byte-identical.

## Long-horizon / limits (honest findings)

- **90 s drift probe**: F/B byte-identical; bed 110.0000 Hz at start, middle,
  end — zero drift (closed-form bed seeding, no accumulation possible).
- **600 s not reachable**: DUR_S parser caps at 300 s, and the znc 2^25-byte
  slice ceiling panics above ~95 s of i64 mix (both B and F; toolchain limit,
  not a design choice). The prereg 600 s probe is replaced by the 90 s probe
  with this documented ceiling.
- **300 s DUR_S cap**: shared parser limit (both B and F). Noted as an
  arbitrary limit per the no-stupid-limits law; changing it would diverge F
  from B, so it's preserved.

## Hygiene (B16)

- Zero RNG in decision/render paths (grep clean; deterministic reruns).
- Pinned compiler throughout.
- Same frozen fixture and battery as crew_b.
- cmp/SHA-256 on every identity claim.
- Analyzer-first: spectra, HNR-equivalent (via byte identity), envelopes,
  drift, transients, deltas, SHA identity. No listening claims.

## Why this BEATs B-gate

1. **Faster**: 1.858× on the frozen 30 s (strict-win bar: 1.5×).
2. **More faithful**: honest 30/5000 Hz rendering (B clamps); full
   overlapping-note attacks (B drops them at region boundaries).
3. **Same quality**: byte-identical fixture → all 9 gates, CHOP, coherence,
   RT-* results exactly preserved.
4. **Same decisions**: latch layer byte-identical.

F is not a trade-off. It is faster, more faithful, and exactly preserves
every frozen bar.
