# JUDGE BRIEF: D-VID-1 V3 (in-plane geometry-churn video lever)

Wave: wave-20260925-0221pdt. Worker: Worker 1 (D-VID-1 V3 implementation).
Branch: tnn-native-lab. Run dir:
docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/.

## Machine-checkable provenance header (frozen at implementation)

- RENDER_SHA: c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c
  (sha256 of the committed variant generator source
  ocean_dvid1_v3.zag, 64 hex chars; system sha256sum).
- FIRST_RENDERED_WAVE: wave-20260925-0221pdt
- COMPONENT_LINEAGE:
  - D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW],
    wave-20260923-2321pdt. Killed on frozen T1 bar: variant 606 vs
    baseline 580 per-mille foam flips, ratio 1.045 against bar <= 0.700.
  - D-VID-1 V2 (co-rotating foam breakup): DEAD [VOID],
    wave-20260924-0521pdt. Analytic no-op proof: bfade =
    o_clamp01k((200 - wz) * 1000 / 140) = 0 for wz >= 200; vortex disc
    wz 560..880, so every V2-retargeted term is gated dead (bupm = 1000,
    streak multiplier = 1, abupm dead code); ocean.zag diff exactly
    three hunks. Wave evidence VOID on a mid-wave python3 heredoc
    touching v2_verify.zag (frozen VKB5).
  - Whirlpool SCOOP: DISCARDED.
  - Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED.
  - D-VID-1 V3 (in-plane geometry churn of disc foam): fresh
    implementation this wave under certified prereg commit 0ba679b11;
    the 2321pdt implementation was VOID on a Python breach and its bytes
    were never read or reused for this implementation.
- NEW_KNOWLEDGE_CLAIM: In-plane geometric churn of the disc foam with
  the frozen displacement field (amplitudes 22/14/20/12, deterministic,
  zero RNG) produced zero measurable change in vortex foam boil: T1-GC
  572 pm variant vs 572 pm baseline (ratio 1.000 against a >= 1.30 bar),
  with all 47 per-pair flip rates identical between the two sequences.

## What V3 is

Single mechanism, frozen in prereg 0ba679b11: in o_shade_water, after the
spire foam-ring term and before the foam clamp, the foam geometry is
re-sampled at disc-plane positions displaced by a frozen deterministic
displacement field (pure function of frame f and world (wx, wz), integer
arithmetic, zero RNG). The breakup sampling coordinates (bup seed 51,
sbup seed 54, abup seed 52), the bfade fade law, capth, ridge scale/seed,
ring scale, fog, dither, frame count, resolution, scene, and camera are
all untouched. Outside the disc (churn_gate = 0) the variant is
bit-identical to the baseline by construction
(foam = o_mix(foam, foam_d, 0) = foam); the verifier byte-checks this.

## Frozen bars and this wave's results

- G-LIVE (analytic trust gate, from the committed source): PASS.
  G1: in the disc (wz >= 200) bfade = 0, so bupm = o_mix(1000, X, 0) =
  1000 and the streak breakup factor o_mix(1000, Y, 0)/1000 = 1; the
  displaced terms reach foam_d through max() with no bfade-gated zero
  factor. G2: foam_d = max(crestf2, steepf2, armf2, streakf2, ringf2),
  each a pure function of the displaced position; foam = o_mix(foam,
  foam_d, churn_gate) with churn_gate = 1000 for r <= 150 world units.
  G3: A1..A4 = 22, 14, 20, 12 all positive; the four sine components use
  incommensurate spatial/temporal frequencies (9,35), (14,55), (11,45),
  (17,28). Honest limitation (frozen): ringf2 is dead in the disc
  because sprox2 = 0 there; liveness rests on crestf2, steepf2, armf2,
  streakf2.
- VKB1 byte-identical determinism (three independent 48-frame renders,
  pure-Zag SHA-256 per frame, validated against system sha256sum):
  PASS. All 48 frames identical across r1/r2/r3 (cmp of hash lists).
  Frozen manifest: MANIFEST_V3_SHA256.txt (r1 hashes).
- VKB2 metric bars: T1-GC bar (variant >= 1.30x baseline, with the 580 pm
  validation gate), T2 (all 47 variant pairs in [50, 1500] pct_x100), T3
  (within 5 percent on f0 and f47, with the 1607/1543 validation gate):
  T1-GC baseline 572 pm (validation |572-580|=8 PASS), variant 572 pm,
  bar 572000 >= 743600 FAIL (ratio 1.000); all 47 per-pair flip rates
  identical between sequences. T2 variant min 859 / max 1074 /
  mean 976: PASS. T3 variant f0=1607, f47=1543 vs baseline 1608/1543:
  PASS. VKB2 FAILS on the T1-GC bar.
- VKB3 tell list vs the rebuilt baseline:
  (1) strobing/banding: T2 max 1074 < 1500, no strobing; sine-smooth
  displacement, no high-frequency stripes by construction; foam debug
  frames rendered for eye confirmation. Machine PASS.
  (2) frozen overlay: T2 min 859 > 50, not frozen; foam debug sequence
  evolves. Machine PASS.
  (3) outside-disc swimming: 0 differing pixels outside the disc bbox
  across all 48 frames. PASS.
  (4) spire rings attached: spire is outside the disc (gate = 0),
  covered by the outside-disc byte check. PASS.
  (5) V-RES 48/48 PASS; V-COMP zero RNG/time/alloc/placement tokens.
  PASS.
- VKB4 cost (variant per-frame within 2x baseline mean): PASS, 1.036x
  (user CPU: 1.984 s/frame vs 1.915 s/frame).
- VKB5 clean build (pinned compiler sha
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  zero RNG, no slice over 2^25, pure Zag, zero Python contact): PASS
- VKB6 red-team eye review: done by a separate worker (not this brief).
- VKB7 sealed blind pair: prepared only if the verdict mapping says
  READY-FOR-JUDGE.

## Verdict recommendation

DEAD [NEW], per the prereg's frozen verdict mapping: G-LIVE passes and
VKB2 fails (T1-GC bar: 572 pm variant vs 572 pm baseline, ratio 1.000,
bar >= 1.30). The lever is live and deterministic (disc-local pixel
changes, bit-identical outside the disc, 3/3 renders identical) but
does not move vortex foam boil: the frozen displacement amplitudes are
too small relative to foam feature scale and disc foam is often
saturated, so displaced sampling returns bit-identical foam for ~99
percent of disc pixels and the frame-to-frame mask flip rate is
unchanged (all 47 per-pair rates identical between sequences). No
sealed blind pair prepared. Full measurements in EVIDENCE_V3_0221.md.

## Frame locations (for the VKB6 eye worker)

- Baseline: docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/baseline/frames_base/dvid1_f00.bmp .. dvid1_f47.bmp
- Variant (VKB1-frozen manifest run r1):
  docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/frames_v3_r1/dvid1_f00.bmp .. dvid1_f47.bmp
- Foam-channel debug frames (dbg=6):
  docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/foam_dbg/base/dvid1_f00.bmp,
  dvid1_f10.bmp, dvid1_f23.bmp, dvid1_f47.bmp and
  docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/foam_dbg/v3/
  (same four frames).
