# EVIDENCE: D-VID-1 V3 (in-plane geometry-churn video lever)

Wave: wave-20260925-0221pdt. Worker: Worker 1.
Branch: tnn-native-lab. HEAD at start: b4507fb22.
Run dir: docs/lab/rsi/runs/wave-20260925-0221pdt/dvid1_geomchurn_v3/
No commit made by this worker. Zero Python contact (no python3, no
scripts, no heredocs, for build, verify, hashing, analysis, or scratch).

## Provenance

- Certified prereg read-only from commit 0ba679b11:
  docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn_v3/PREREG_DVID1_V3_2321.md
  (328 lines). The 2321pdt void directory was never opened or reused.
- Baseline source docs/lab/imagination_discovery/vid/ocean.zag: not
  modified. Byte copy in baseline/ocean.zag matches source:
  sha256 9df721dadc6c1de380ba8130958b86a2ff19e22cce4b3be576501f3ec0a8ef13.
- Variant generator: ocean_dvid1_v3.zag =
  RENDER_SHA c654ebe4ba3a96361324fdcf362324da30ef857feed4a60202d07d4e00d3827c
  (system sha256sum). Baseline plus: provenance comments, frozen
  o_sin_bh / o_sin1000, frozen geometry-churn block after the spire
  ring and before the foam clamp. Prereg trailing semicolons after
  inline ifs omitted (Zag grammar rejects them); formulas and ordering
  unchanged.
- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
  All builds used --no-zagd --no-analyze --no-foreground-cache.
- v3_verify.zag sha256:
  7f84fbdf3c42c017b9640d1df8cf58d17545469f3e4ff527f5fb7fd74347f8fb
- v3_sha.zag sha256:
  b564057075aa3ea0ef5e829b6b3ceef05618020b8f608e2e26da8e95e8add24b
- Pure-Zag SHA-256 validated: "abc" test vector
  ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
  matches system sha256sum; 5 sample frames (baseline f00, r1 f23,
  r2 f47, r3 f10, foam dbg v3 f10) match system sha256sum exactly.

## Renders (48 frames, 1024x1024 24-bit BMP, 3145782 bytes each)

- Baseline (baseline/frames_base): 48/48 frames, every frame exactly
  3145782 bytes. Wall 1m35.432s, user 1m31.913s. Mean 1.915 s/frame
  (user CPU).
- Variant r1 (frames_v3_r1): 48/48. Wall 1m36.577s, user 1m35.214s.
  Mean 1.984 s/frame.
- Variant r2 (frames_v3_r2): 48/48. Wall 1m52.848s, user 1m35.025s.
- Variant r3 (frames_v3_r3): 48/48. Wall 2m5.107s, user 1m35.488s.
  (Wall-time inflation on r2/r3 is IO/scheduling; user CPU is flat
  across all three runs.)
- Cost ratio (user CPU mean): 1.984 / 1.915 = 1.036x. Within 2x.

## VKB1: byte-identical determinism

- Pure-Zag sha256 of all 48 frames in all three runs:
  hashes_v3_r1.txt, hashes_v3_r2.txt, hashes_v3_r3.txt.
- cmp hashes_v3_r1.txt hashes_v3_r2.txt: identical.
- cmp hashes_v3_r2.txt hashes_v3_r3.txt: identical.
- VKB1 PASS: 48/48 frames identical across three independent renders.
- Variant differs from baseline (expected: the churn is live).
- Frozen manifest: MANIFEST_V3_SHA256.txt (r1 hashes, 48 entries).

## VKB2: metric bars (verifier output: verify_v3.log)

- T1-GC baseline: 572 pm. Validation gate |572 - 580| = 8 <= 25: PASS.
- T1-GC variant: 572 pm.
- T1-GC bar (variant*1000 >= baseline*1300): 572000 >= 743600: FAIL.
  Ratio 1.000. Required >= 1.30.
- Per-pair detail: all 47 consecutive pairs have IDENTICAL flip
  per-mille in baseline and variant (e.g. pair 0: 398=398,
  pair 23: 626=626, pair 46: 647=647). The temporal flip pattern is
  unchanged pair-by-pair, not just on average.
- T2 baseline: min 859, max 1075, mean 977 (pct_x100).
  T2 variant: min 859, max 1074, mean 976.
  Bar (every variant pair in [50, 1500)): PASS.
- T3 baseline: f0=1608, f47=1543. Validation vs 1607/1543 within 10:
  PASS (|1608-1607|=1, |1543-1543|=0).
  T3 variant: f0=1607, f47=1543. Bar (within 10 of baseline): PASS.
- D1 diagnostic (f10 region diff): 0 pm. The churn does not flip the
  foam mask in the metric region at f10.
- V-RES: 48/48 variant frames at 1024x1024 24-bit: PASS.
- VKB2 verdict: FAIL (T1-GC bar). T2 and T3 pass.

## VKB3: tell list

1. Strobing / banding: T2 variant max 1074 pct_x100 < 1500, no
   strobing. Displacement field is sine-smooth (no high-frequency
   spatial stripes by construction); foam debug frames rendered for
   eye confirmation (see below). Machine: PASS.
2. Frozen overlay: T2 variant min 859 > 50, not frozen; foam debug
   sequence (f0/f10/f23/f47) evolves frame to frame. Machine: PASS.
3. Outside-disc swimming: verifier byte comparison outside the disc
   projection bbox: 0 differing pixels across all 48 frames. PASS.
4. Spire rings attached: spire region is outside the disc
   (churn_gate = 0 there); covered by the outside-disc byte check.
   PASS.
5. V-RES 48/48 PASS; V-COMP: grep finds zero rand/random/srand,
   zero time/clock, zero tokens over 2^25, zero fill/rect/circle/
   sprite/blit/place calls (V-COMP words appear only in comments).
   PASS.

## VKB4: cost

- Variant mean 1.984 s/frame vs baseline 1.915 s/frame (user CPU):
  ratio 1.036x, within the 2x bar. PASS.

## VKB5: clean build

- Pinned compiler only; pure Zag (verifier, SHA tool, analysis
  tools all Zag); zero RNG tokens; no Python contact at any step.
  PASS.

## VKB6: eye review

- Not performed by this worker (separate worker per prereg).
- Foam-channel debug frames (dbg=6) rendered for the eye worker:
  foam_dbg/base/dvid1_f00.bmp, dvid1_f10.bmp, dvid1_f23.bmp,
  dvid1_f47.bmp and foam_dbg/v3/ (same four frames).

## Diagnostic findings (why the bar failed)

- The churn block IS live and deterministic: baseline-vs-variant
  byte diffs are confined to the disc footprint (f0: 210 bytes,
  f10: 85, f23: 154, f47: 170), at x 509..986, y 397..406 for f10.
  Outside the disc: bit-identical (0 diffs).
- The world disc (160 world-unit radius at depth ~710) projects to a
  foreshortened band about 477 px wide but only ~10 px tall on
  screen (grazing camera angle), not the 204 px radius circle the
  frozen T1-GC region assumes. Measured at f10: disc center
  (xc=716, yc=407), T1-GC radius 207 px.
- In a tight tracking rectangle around the true disc footprint,
  temporal boil is 57 pm for BOTH baseline and variant (band_bin).
  The churn rearranges foam spatially (a few dozen pixels per frame
  change, displaced samples saturating to foam 1000 at affected
  pixels) but does not change the frame-to-frame mask flip rate.
- The frozen displacement amplitudes (22/14/20/12, max ~36 world
  units axis-aligned) are small relative to foam feature scale, and
  disc foam is often saturated, so displaced sampling returns
  bit-identical foam for ~99 percent of disc pixels.
- Implementation note: the committed churn block recomputes
  displaced foam via o_height out-params (fall2, arm2, sprox2) at the
  displaced point, matching the prereg's "recomputed at the moved
  point" spec. No spec deviation found on re-inspection.

## Verdict

- G-LIVE: PASS. VKB1: PASS. VKB2: FAIL (T1-GC bar 1.000 < 1.30).
  VKB3: PASS (machine). VKB4: PASS. VKB5: PASS. VKB6: pending
  separate worker (moot for verdict).
- Per the frozen verdict mapping (G-LIVE passes and any VKB fails):
  DEAD [NEW].
- New knowledge claim (past tense, measured): In-plane geometric
  churn of the disc foam with the frozen displacement field
  (amplitudes 22/14/20/12, deterministic, zero RNG) produced zero
  measurable change in vortex foam boil: T1-GC 572 pm variant vs
  572 pm baseline (ratio 1.000 against a >= 1.30 bar), with all 47
  per-pair flip rates identical between the two sequences. The lever
  is live (deterministic disc-local pixel changes, bit-identical
  elsewhere) but too weak to move temporal dynamics: the displacement
  is small versus foam feature scale and disc foam is often
  saturated.
- No sealed blind pair prepared (verdict is not READY-FOR-JUDGE).

## Files written (all under the run dir)

- ocean_dvid1_v3.zag (RENDER_SHA c654ebe4...)
- substrate/R33_NATIVE_IO_V1.zag, baseline/ocean.zag,
  baseline/substrate/R33_NATIVE_IO_V1.zag
- v3_verify.zag, v3_sha.zag, dist.zag, band.zag
- ocean_v3_bin, v3_verify_bin, v3_sha_bin, dist_bin, band_bin,
  baseline/ocean_base_bin (build artifacts, not for commit)
- baseline/frames_base/ (48 BMP), frames_v3_r1/, frames_v3_r2/,
  frames_v3_r3/ (48 BMP each)
- hashes_v3_r1.txt, hashes_v3_r2.txt, hashes_v3_r3.txt,
  hashes_base.txt, MANIFEST_V3_SHA256.txt
- verify_v3.log, verify_selfcheck.log
- foam_dbg/base/ and foam_dbg/v3/ (4 foam-channel BMPs each)
- JUDGE_BRIEF.md (completed below), EVIDENCE_V3_0221.md (this file)
