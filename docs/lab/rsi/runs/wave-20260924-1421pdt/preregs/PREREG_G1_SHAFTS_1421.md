# PREREG_G1_SHAFTS_1421.md - G1 SUNSHAFTS re-freeze, wave-20260924-1421pdt

Frozen before any G1 v2 code exists. This prereg repairs the two defects
that discarded G1 in wave-20260924-1121pdt (see
docs/lab/rsi/runs/wave-20260924-1121pdt/candidates/g1/VERDICT_G1.md):
(1) the frozen verifier point-set was geometrically defective (sun below
the horizon, sample points inside the gas-giant disc), so KB2/KB3/KB5/KB7
were unevaluable as frozen; (2) the frozen T-gate (400) sat far below the
shaft field mean (~511), producing a broad sky wash (97.14 percent of sky
pixels lifted, mean dL +33.07) instead of confined shafts. The march and
transmittance machinery itself worked as specified in 1121pdt and is
inherited unchanged. This is a re-freeze, not a continuation: no constant
below may be tuned against renders. Geometry was validated against the
world-model functions copied verbatim from the r8c substrate before this
freeze (scratch probe, pure Zag); the runtime geometric validator below
re-checks the same geometry on every run.

## Substrate (frozen)

- Source: docs/lab/imagination_discovery/img/r8c_alien.zag (Fork C,
  mind's-eye elaboration, 1024x1024 BMP output).
- Vendored IO: candidates/g1_v2/sub/R33_NATIVE_IO_V1.zag, byte-identical
  copy of the committed file, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
- Baseline: candidates/g1_v2/r8c_baseline.zag is a byte copy of
  r8c_alien.zag with only the @import line repointed. Frozen gate:
  baseline BMP sha256 must equal
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d
  (the S14 record). A mismatch aborts the battery before any variant
  work is evaluated.
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  verified with sha256sum before use.

## Mechanism: G1 v2 sunshafts (frozen)

Screen-space raymarched crepuscular shafts, a new pass
g1_pass_sunshafts running after r8c_pass3 (light logic) and before
r8c_pass4 (fixations). Pure Zag, zero RNG, fully deterministic.

Frozen constants:

- SUN S = (110, 300). Screen-space convergence point of the shaft fan.
  Above the horizon by construction: ridge_y(110) = 376, so the sun sits
  76 px above the ridge line (frozen margin requirement: at least 40,
  see validator V1). tier_at(110,300) == 0 (sky; outside the gas-giant
  disc centered (700,250) r150 and the moon disc centered (170,120) r26).
- Cloud-deck density field D(x,y) =
  r8c_fbm(x*256/520, y*256/180, 9131, 3). Shaft machinery only, never
  rendered as visible cloud. Unchanged from 1121pdt.
- March: each sky pixel marches N = 12 steps screen-space toward S.
  Step k: t = k*1024/N; jitter jx = r8c_h01(x,y,9132+k)/64-8,
  jy = r8c_h01(y,x,9133+k)/64-8; qx = x + (110-x)*t/1024 + jx,
  qy = y + (300-y)*t/1024 + jy, clamped to [0,1023]. Unchanged from
  1121pdt except the sun coordinates.
- Density table: full-resolution exact memoization of D (1024x1024 u32).
- Transmittance T(P) = mean over the N march steps of (1024 - D(q)).
  Unchanged from 1121pdt.
- Sky pixel set for the march: tier_at(x,y) == 0, i.e. y < ridge_y(x)
  and outside the giant and moon discs. Terrain skipped by construction.
- Lift color: sun color (255,172,112), per-channel clamp at 255.
  Max lift scale 90, as in 1121pdt.

T-gate recalibration (frozen procedure, the core repair of defect 2):

1. The variant binary renders the baseline passes first (byte-identical
   baseline, gate above), then marches every sky pixel toward S and
   records T(P). This measurement happens on the rebuilt baseline run,
   before any lift is applied. T(P) is canvas-independent, so the field
   statistics are a pure function of the frozen D field and S.
2. Pass A accumulates sum_T and sum_T2 over the sky pixels:
   mean_T = sum_T / n; var_T = sum_T2 / n - mean_T*mean_T;
   std_T = isqrt(var_T) (integer math, population statistics).
3. The frozen gate is G = mean_T + std_T + std_T/2 (1.5 standard
   deviations above the measured field mean). Documented margin: 1.5
   sigma. Rationale, from 1121pdt evidence: the field mean measured
   ~511 while the hardcoded gate 400 sat ~2.75 sigma below it, lifting
   97.14 percent of sky pixels. Under an approximately normal T field,
   mean + 1.5 sigma lifts about 7 percent of sky pixels: the
   statistically distinct low-density corridors (shafts), not the sky.
   No hardcoded constant replaces the measurement; the 400 gate is gone.
4. Pass B applies L(P) = max(0, T(P)-G) * 90 / (1024-G), sky-only,
   clamp 255. Pixels at or below the gate are untouched.
5. The elaboration trace records G1.8: mean_T, std_T, gate G, lifted
   sky pixel count and per-mille fraction. Stdout prints
   "G1 shafts: N=12 sky_px=<n> gate=<G>".

## Geometric validator (frozen procedure, the repair of defect 1)

A pure-Zag program candidates/g1_v2/g1_validate.zag runs BEFORE the
verifier on every battery run. It embeds the frozen point-set
generation below (identical code in the verifier) and the world-model
functions copied verbatim from the substrate. It prints one line per
check and exits 0 iff every check passes. The runner aborts the whole
battery (verdict DISCARD, no sealed pair) if the validator fails.

Frozen point sets (coordinates in top-origin pixels, frame 1024x1024):

- WEDGE: 6 rays from S, ray r (0..5) direction (dx,dy) = (r-1,-1),
  step 36, t = 1..8: (110 + t*(r-1)*36, 300 - t*36). 48 candidates.
  Pre-freeze validation: 39 kept (5 drop out of frame left, 2 out of
  frame right, 2 inside the giant disc). Frozen assert: kept >= 36.
- OFFWEDGE: k = 0..47: (880 + (k*37 % 120), 60 + (k*53 % 180)).
  Pre-freeze validation: 48 kept. Frozen assert: kept >= 36.
- TERRAIN: k = 0..63: (40 + (k*61 % 944),
  ridge_y(x) + 40 + (k*37 % 200)), kept iff in frame and tier_at >= 1.
  Pre-freeze validation: 64 kept. Frozen assert: kept >= 56.
- RADCUT: t = 1..24: (110 + t*20, 300 - t*10), kept iff in frame and
  tier_at == 0, t order preserved. Pre-freeze validation: 24 kept.
  Frozen assert: kept >= 16.

Frozen pass criteria (validator):

- V1: sun above the horizon: ridge_y(110) - 300 >= 40.
- V2: sun in the sky region: tier_at(110,300) == 0.
- V3: every kept WEDGE point satisfies tier_at == 0 (inside the sky
  region, hence above the ridge and outside the gas-giant and moon
  discs).
- V4: every kept OFFWEDGE point satisfies tier_at == 0.
- V5: every kept RADCUT point satisfies tier_at == 0.
- V6: keep-count asserts: WEDGE >= 36, OFFWEDGE >= 36, TERRAIN >= 56,
  RADCUT >= 16.

Cross-check (runner-enforced): the verifier prints the same kept
counts; the runner diffs the validator and verifier *_KEPT lines and
requires them identical, proving both programs evaluated the same
frozen point sets.

## Frozen kill bars

Luma L = (299R + 587G + 114B)/1000; dL = L_variant - L_baseline.
Thresholds are inherited unchanged from the 1121pdt freeze.

- KB1 determinism: 3 reruns of the N=12 variant are byte-identical
  (shas recorded).
- KB2 shaft ratio: mean variant luma / mean baseline luma over kept
  WEDGE points >= 1.12.
- KB3 shaft variance: var(dL) over kept WEDGE points >= 60.0.
- KB4 terrain untouched: mean|dL| over kept TERRAIN points <= 1.0.
- KB5 no broad wash: mean|dL| over kept OFFWEDGE points <= 6.0.
- KB6 acutance: D19 acutance ratio (variant/baseline, 2px step) over
  the frozen SKY12 points <= 1.10. SKY12: q = 0..11,
  (80 + 72*q, 60 + 15*(q % 4)); all twelve verified tier_at == 0
  pre-freeze.
- KB7 smoothness: max |second difference of dL| along the kept RADCUT
  in t order <= 25.
- KB8 cost: variant total wall time <= 3.0x baseline total wall time.

## Verdict mapping (frozen)

READY-FOR-JUDGE (sealed blind A/B pair plus JUDGE_BRIEF.md carrying
the machine-checkable provenance header) iff the geometric validator
passes AND KB1 through KB8 all pass as specified. Any validator check
failed, any bar failed, or any bar unevaluable maps to DISCARD: no
sealed pair is prepared and nothing enters the judge queue. No bar may
be weakened, narrowed, or re-interpreted to force a pass. The E3 film
grain rejection is honored: KB6 guards acutance, and no grain is added.

## Provenance header (required on JUDGE_BRIEF.md if the verdict is
READY-FOR-JUDGE)

- RENDER_SHA: sha256 of the adopted variant BMP.
- FIRST_RENDERED_WAVE: wave-20260924-1421pdt.
- COMPONENT_LINEAGE: r8c substrate inherited from
  docs/lab/imagination_discovery/img/r8c_alien.zag; variant BMPs are
  new renders of this wave; prior judge-queue items R9, C1, C2v3,
  S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform untouched and
  listed QUEUED-UNJUDGED.
- NEW_KNOWLEDGE_CLAIM: one sentence stating what this candidate
  teaches that no prior wave established.

## Purity and discipline (frozen)

Pure Zag only: no Python anywhere, not glue, not analysis, not
verifiers, not harnesses, not /tmp scratch. Any Python contact voids
the evidence: self-disclose, void tainted results, redo clean. Static
checks in the runner grep for .py files, python tokens in .zag
sources and the runner, and rand/time/clock calls. Commits stay local
on tnn-native-lab; nothing is pushed to GitHub. Commit order: this
prereg commit strictly first, then implementation and evidence commits.
Only the candidate's own paths are added. No em-dashes in loop
documentation.
