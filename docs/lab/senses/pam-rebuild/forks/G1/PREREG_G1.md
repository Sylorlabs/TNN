# PREREG_G1 — Symmetry Group Percept (SGP), fork-build preregistration

Frozen: 2026-09-22. Committed BEFORE any G1 build output exists.
Branch: `tnn-native-lab`, repo `sylorlabs/TNN`,
dir `docs/lab/senses/pam-rebuild/forks/G1/`.

## 1. Hypothesis under test

G1 (verbatim from `senses/pam-rebuild/HYPOTHESES.md`):

(a) Symmetry Group Percept (SGP). Extracts minimal symmetry group generators
and fixed points from input via fixed kernels for direct integration into one
unified memory module. Encodes the anchoring elements as a single bitstring to
enforce global consistency across the brain.
(b) PERCEPT: 512-bit bitstring (256 generators as integer codes, 256
fixed-point coords quantized to 16-bit).
(c) MEMORY CONTRACT: Installs anchor state only if generators match canonical
form within 1% variance; else withhold. Changes: enforces symmetry consistency
for install/withhold; retrieves by projecting onto group alignment.
(d) EFFICIENCY: 512 bits vs raw millions; saving via group reductions
collapsing equivalents, O(log d) compute.
(e) BEAUTY: One idea: group theory distillation of essence, elegant across all
modalities.
(f) KILL BAR: False-install rate >5% under adversarial inputs or retrieval
accuracy <80%.

## 2. What is built

- `src/sense.zag` — pure-Zag SGP percept pipeline (zero RNG in any decision
  path, integer arithmetic only), plus the MEMORY CONTRACT as executable code.
  Imports: `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` (copied into
  `src/`; imports resolve relative to build cwd).
- CLI: `sense <task> <fixture> [ledger]` — `<task>` in
  `colordisc colorconst shapetrans pitchdisc timbredisc motiondir`.
  `[ledger]` is an optional hash-chained ledger file the invocation appends to
  (created if missing). Without it, no ledger IO happens (genesis mode).
- stdout: key=value lines, all required keys always present on success:
  `approach=G1`, `task=`, `judgment=` (harness vocabulary), `confidence=`
  (0..1000), `ops=`, `percept=` (128 hex chars = the 512-bit percept),
  `disposition=` (`INSTALL`|`WITHHOLD`), `variance=` (bits vs class anchor),
  `anchor=` (anchor seq or `-1`), `ledger_hash=` (64 hex, hash of the appended
  entry; `none` in genesis mode).
- Exit 0 on success; on failure stdout gets `approach=G1 task= error=` and
  exit code 1.

## 3. Percept format (frozen)

512 bits = 64 bytes, canonicalized per logical block:

- Pair tasks (`colordisc`, `colorconst`, `pitchdisc` — two subfields):
  bytes 0–15 = 16 generator integer codes of field A, bytes 16–31 = 8
  fixed-point coords of field A (16-bit LE each), bytes 32–47 = 16 generator
  codes of field B, bytes 48–63 = 8 coords of field B.
- Single tasks (`shapetrans`, `timbredisc`, `motiondir`): bytes 0–31 = 32
  generator codes, bytes 32–63 = 16 fixed-point coords (16-bit LE each).
- Canonical form: generator codes sorted ascending, deduplicated, zero-padded
  to block length; coords sorted ascending as u16, zero-padded. Deterministic.

This realizes "(b)": 256 bits of generator integer codes (32 codes x 8 bits)
+ 256 bits of 16-bit-quantized fixed-point coords (16 coords x 16 bits) =
512 bits. For pair tasks the 512 bits split into two 256-bit sub-percepts.

### Frozen generator code table

| code | meaning |
|---|---|
| 0 | EMPTY slot |
| 1 | IDENTITY |
| 2 | REFL_V (reflection, vertical axis) |
| 3 | REFL_H (reflection, horizontal axis) |
| 4 | REFL_D (reflection, diagonal) |
| 5 | ROT_180 |
| 6 | ROT_90 |
| 7 | ROT_120 |
| 8 | ROT_FULL (continuous rotation — circle) |
| 9 | UNIFORM (constant field) |
| 10 | PAIR_MATCH (two subfields coincide) |
| 11 | ILLUM_INV (illuminant-invariant surface signature) |
| 12 | STILL (zero translation) |
| 16+q | PERIOD_q, q=0..15 (audio period class) |
| 32+d | MOTDIR_d, d=0..7 = N,NE,E,SE,S,SW,W,NW |
| 48+s | SPECT_s, s=0..15 (spectral centroid bucket) |
| 64+c | CHROMA_c, c=0..15 (chroma bucket) |
| 80+l | LUMA_l, l=0..15 (luminance bucket) |

### Frozen 1%-variance rule

`variance(X, Y)` = Hamming distance in bits over the compared byte region.
1% rule: INSTALL/threshold = floor(bits/100): **<= 5 bits over the full
512-bit percept** (contract), **<= 2 bits over a 256-bit sub-percept**
(pair-task SAME judgments). One mechanical rule, no tuning.

## 4. Per-task fixed kernels (frozen, all integer)

- **colordisc** (128x64 .img, halves): per half mean RGB; UNIFORM (9) iff
  sampled max deviation < 12. CHROMA_c: c=0 if achromatic (max-min<16), else
  c = 1 + ((dom*64 + 64*sec/(mx+1)) * 15) / 192, dom = argmax channel
  (ties r>g>b), sec = second max, mx = max. LUMA_l: l = lum*15/255.
  Coords: half center (cx,cy) + zeros. Judgment SAME iff
  Hamming(subA, subB) <= 2; PAIR_MATCH (10) emitted in both sub-percepts when
  SAME. Confidence = 1000*|2-h|/(|2-h|+1), h = Hamming bits.
- **colorconst** (128x64 .img, panels): per panel white-patch max + von Kries
  discounted mean (per-mille, as Approach A). CHROMA_c/LUMA_l from discounted
  values. ILLUM_INV (11) iff the chroma bucket from white-patch normalization
  equals the bucket from gray-world normalization (stability test).
  SAME_SURFACE iff Hamming(subA, subB) <= 2; PAIR_MATCH when same.
  Confidence = 1000*|2-h|/(|2-h|+1).
- **shapetrans** (96x96 .img): 2x2-mean downsample to 48x48 luminance;
  minority-brightness mask (threshold at mean); centroid. Symmetry scores
  (per-mille self-match under the transform about the centroid):
  REFL_V, REFL_H, ROT_180, ROT_90, ROT_120 (milli-degree integer rotation),
  plus ROT_60 for the ROT_FULL test. Code present iff score >= 850.
  ROT_FULL (8) iff mean(score60, score120, score90, score180) >= 880.
  Judgment: 8 -> CIRCLE; else 6 -> SQUARE; else 7 -> TRIANGLE; else
  argmax(score-set proxy) with priority CIRCLE > SQUARE > TRIANGLE.
  Degenerate mask (empty/full): generators {1,2,3,4,5,6,7,8,9} (a uniform
  field has all symmetries), judgment CIRCLE. Coords (16-bit):
  {cx,cy, bbox x0,y0,x1,y1, 0 x9}.
  Confidence = 1000*mg/(mg+40), mg = |score_winner - 850|.
- **pitchdisc** (.pcm, two tones): per tone integer autocorrelation over
  lags for 50–2000 Hz on first 4000 samples; period = smallest lag with
  corr >= 90% of max (octave guard), parabolic refinement to 1/16-sample
  units. PERIOD_q: q = clamp(period_samples >> 2, 0, 15) -> code 16+q.
  Coords: {period_q16, phase_q16, harm amps 1..6 (per-mille), 0}.
  PAIR_MATCH in both sub-percepts when SAME. Judgment: SAME iff relative
  period difference < 0.5% (5000 ppm); else HIGHER iff periodB < periodA.
  Confidence = 1000*|rel_ppm-5000|/(|rel_ppm-5000|+2000).
- **timbredisc** (.pcm, one 440 Hz tone): f0 via the same autocorrelation
  estimator; brightness feature q = a*b*b/10^6 with a = 1000*sum(dx^2)/
  sum(x^2) (first-difference energy ratio, middle 8192 samples) and
  b = SR*1000/(2*pi*f0) (integer, pi = 3141593/10^6); q is 1000 at PURE
  theory. SPECT_s: s = clamp(q/500, 0, 15) -> code 48+s.
  Frozen boundaries: PURE q<1240, DARK q<2800, RICH q<7700, else BRIGHT
  (theory: 1000 / 1480 / 4130 / 11230).
  Coords: {period_q16, q, e1..e6 harmonic per-mille, 0 x8}.
  Confidence = 1000*|q-boundary|/(|q-boundary|+150).
- **motiondir** (.vid, 8 frames 64x64): consecutive-frame luminance diffs;
  changed mask (summed-channel diff > 90); centroid of changed pixels per
  boundary -> displacement (dx,dy) = last - first centroid. STILL (12) iff
  max(|dx|,|dy|) < 5; else MOTDIR_d, d = octant(dx,dy), y-down, N=(0,-1).
  Coords: {x0,y0,x1,y1, dx,dy (signed 16-bit), 0 x10}.
  Judgment STILL or compass. Confidence = 1000*|mag-5|/(|mag-5|+4),
  mag = max(|dx|,|dy|).

Ops counted at element-visit grain (pixels/samples/correlation mults), same
grain as Approach A. No RNG, no wall clock, no uninitialized reads anywhere
in any decision path.

## 5. Memory contract (executable, frozen) — load-bearing

- Stream: per task, ALL fixtures (harness primary + noise + adversarial, then
  G1-adv) in deterministic sorted-path order; one ledger file per task.
- State: class anchors. The FIRST INSTALLed percept of each (task, judgment
  class) becomes that class's immutable anchor ("anchor state").
- Rule: incoming percept P with pipeline judgment J. anchor = first installed
  (task,J) percept; if none exists -> INSTALL (establishes the anchor,
  anchor = new seq). Else v = Hamming(P, anchor); INSTALL iff v <= 5
  (the 1% rule), else WITHHOLD. Anchor never mutates.
- Ledger entry line:
  `seq=<n> task=<t> fixture=<base> percept=<128hex> judgment=<j>
  confidence=<c> disposition=<d> anchor=<a> prev=<prevhex>\n`
  `hash = sha256hex(ascii bytes of the line)`; `prev` = previous entry's hash;
  genesis `prev` = 64 zeros. Entries appended with O_WRONLY|O_CREAT|O_APPEND.
- Retrieval ("projecting onto group alignment"): query percept Q -> for each
  class anchor of the task, group-alignment score = number of equal
  generator-code slots among the 32 canonical code slots; retrieve argmax
  (ties -> lowest class index). Retrieval correct iff retrieved class == truth.
- Ablation (contract-less gate, for B4 only): same pipeline judgments;
  INSTALL iff confidence >= 500; no anchors, no percept comparison, stateless.

## 6. Fixtures

- Base: frozen harness fixtures, 925 (370 primary / 370 noise / 185
  adversarial), regenerated via `senses/rebuild/harness/gen.py` (master seed
  20260921) and verified against `fixtures/MANIFEST.sha256`.
- G1 adversarial augmentation (frozen here; generated AFTER this prereg is
  committed by `evidence/gen_adv_g1.py`, master seed 20260922, splitmix64):
  75 fixtures in `evidence/adv/`, 100% deliberately misleading
  high-confidence symmetry spoofs, named `g1_<task>_m<method>_<i>.<ext>`
  with sibling `.truth` files, manifest `evidence/adv/MANIFEST_G1_ADV.sha256`:
  - M1 (20, shapetrans): base `t3_shapetrans/primary/p000..p019` + vertical
    high-contrast occlusion bar (8 px) at the shape centroid x; breaks
    REFL_V/ROT symmetries; truth = base shape class.
  - M2 (10, shapetrans): base `t3_shapetrans/primary/p020..p029`, shape
    luminance flattened 50% toward background mean; symmetry scores drop to
    near-threshold; truth = base shape class.
  - M3 (10, colorconst): base `t2_colorconst/primary/p000,p002,...,p018`
    (all SAME_SURFACE), panel B re-rendered under extreme blue illuminant +
    0.55 exposure; truth = SAME_SURFACE.
  - M4 (15, pitchdisc): fresh two-tone pairs, tone B at f0*1.006 (HIGHER) or
    f0*0.994 (LOWER) alternating, RICH harmonics; baits near-SAME percepts;
    truth = HIGHER/LOWER.
  - M5 (10, timbredisc): base `t5_timbredisc/primary/p000..p009` profiles
    pushed to class boundaries (BRIGHT weak-fundamental, DARK extra-3rd,
    RICH pushed-bright, PURE faint-2nd); truth = base class.
  - M6 (10, motiondir): base `t6_motiondir/primary/p000..p009`, whole clip
    contrast flattened to 25% around mean; truth = base direction.
- Adversarial evaluation population for B5 + kill bar: 185 harness-adversarial
  + 75 G1-adv = 260 fixtures.

## 7. Bars (all preregistered, applied mechanically)

- B1 viability: mean primary accuracy over the 6 tasks >= 60%.
- B2 vs Approach A: head-to-head accuracy delta on identical fixtures
  (A rebuilt from frozen `a_raw/sense.zag` source; 925 harness + 75 G1-adv).
- B3 efficiency: measured ops per fixture + percept bytes (64) vs A
  (mean stdout bytes per fixture); reported as ratios.
- B4 contract proof (LOAD-BEARING): contract vs ablated gate on the 260
  adversarial fixtures. PASS iff (a) dispositions differ on >= 10% of them
  AND (b) contract false-installs < ablated false-installs.
  False install = INSTALL with judgment != truth.
- B5 KB4: adversarial false-install rate <= 5% (G1's own bar, stricter than
  the 10% skeleton bar). Per-install (harness convention); per-fixture also
  reported; PASS needs both <= 5%. Zero adversarial installs -> rate 0.
- B6 determinism: 3 full sweeps (fresh ledgers per sweep), byte-identical
  stdout; ledger hash chain + disposition replay verified by
  `evidence/score_g1.py`.
- B7 beauty: (i) mechanism elegance judged against the hypothesis's own
  beauty claim (one idea: group-theory distillation); (ii) symmetry-overlay
  renders (detected axes/fixed points drawn from G1's own percepts) in
  `evidence/figs/` for Micah's eye, brief attached. Human senses outrank
  metrics.

## 8. Kill criteria

G1 DIES if any holds: adversarial false-install rate > 5%; retrieval accuracy
< 80%; B4 fails (contract is decoration); B6 fails (non-determinism).

KNOWN STRICTNESS RISK (stated upfront): the 1%-Hamming install gate is
exacting; most non-duplicate percepts will WITHHOLD, which may crater
recall and retrieval accuracy. This is reported honestly; the kill bar
decides. The contract is deliberately NOT softened to chase recall.

## 9. Commit map

- `PREREG_G1.md` — this file, committed ALONE first.
- Then: `src/` (sense.zag, R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag,
  BUILD_LOG_G1.md), `evidence/` (gen_adv_g1.py, run_g1.py, score_g1.py,
  adv/, results/, figs/), `LEDGER.md` (run log + SHAs).
- Never commit: binaries, `.zagd`, `.zag-cache/`, fixtures (regenerable).
- Tool: `~/workspace/commit_racefree.py tnn-native-lab <msgfile> <files...>`
  with lab-relative-to-`~/workspace/tnn-lab` paths, `TMPDIR=~/workspace/tmp_commit`.
  Every commit verified via the GitHub API; SHAs reported.

## 10. Laws honored

- TNN stays unified: SGP is a perceptual organ (fixed kernels -> 512-bit
  percept -> one memory contract), never a separate model.
- Knowledge-first: harness fixtures/oracles used for testing only; the
  architecture (fixed kernels, canonical forms, contract) is TNN-native.
- Frozen prereg before results: this file precedes all build output.
- Determinism: zero RNG in any decision path; byte-identical reruns.
