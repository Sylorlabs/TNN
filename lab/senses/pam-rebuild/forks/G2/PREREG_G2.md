# PREREG — Fork G2: Predictive Residual Percept (PRP)

Frozen: 2026-09-22. Committed BEFORE any G2 build output exists.
Branch `tnn-native-lab`, repo `sylorlabs/TNN`,
`docs/lab/senses/pam-rebuild/forks/G2/`.

## 1. Hypothesis under test

ID: **G2** (verbatim text in `senses/pam-rebuild/HYPOTHESES.md` — Grok-4.6 G2):

> (a) Predictive Residual Percept (PRP). Generates forward prediction from
> current invariants and outputs residual vector as percept to unified memory.
> Creates contract requiring predictive consistency for state handling.
> (b) PERCEPT: 256-element vector of 8-bit signed residuals in invariant space.
> (c) MEMORY CONTRACT: Installs if norm < epsilon and predicted hash matches;
> else withhold. Changes: install requires match, affects retrieve by biasing
> memory search with prediction.
> (d) EFFICIENCY: O(N) compute vs O(N^2) raw; saving by invariant reuse for
> prediction, 256 bytes compressed.
> (e) BEAUTY: Prediction as bridge from perception to memory, elegant unified
> extension to action.
> (f) KILL BAR: False-install rate >8% or integration success <85%.

Distinct from sibling fork H3 (Sol): H3 emits state transitions with
confirmations from subsequent evidence; G2 emits a residual vector against a
forward prediction and gates install on norm+hash-match. No shared code.

## 2. What is built

- Pure-Zag percept pipeline `src/g2_sense.zag` (+ local copy of
  `R33_NATIVE_IO_V1.zag`; same import convention as Approach A).
- The MEMORY CONTRACT as executable code: the exact install/withhold rule
  from the hypothesis, wired to a deliberate-memory install gate inside the
  binary (batch/stream mode). No RNG anywhere in any decision path;
  all arithmetic integer; deterministic.
- A `sense` CLI:
  - `sense <task> <fixture>` → percept record + judgment + INSTALL/WITHHOLD
    disposition + hash-chained ledger line on stdout (exit 0).
  - `sense batch <manifest>` → runs a memory stream over
    `<task> <fixture> <contract|ablated>` lines: per-fixture records,
    retrieval ranking biased by prediction, ledger chain, SUMMARY stats.
    The `ablated` mode is the B4 control: identical percepts through a
    contract-less (always-install) gate.
- Zero wall-clock, zero uninitialized reads: ≥3 runs byte-identical.

### 2.1 Percept format (frozen)

256-element vector of 8-bit signed residuals in invariant space, layout:

| dims | content |
|---|---|
| 0–63 | fine residuals r_f[i] = clamp(q8(I_i) − q8(P_i), −128, 127), primary invariants |
| 64–127 | coarse residuals r_c[i] = q4(I_i) − q4(P_i) (16-level), primary invariants |
| 128–191 | fine residuals, secondary (stability) invariants |
| 192–255 | reserved, always 0 |

- q8(v) = clamp(v / S_f, −128, 127) with per-task fine scale S_f (frozen §2.3).
- q4(v) = q8(v) / 16 (16 coarse levels).
- pred_hash = FNV-1a-64 over the coarse PREDICTED bytes of active dims;
  obs_hash = FNV-1a-64 over the coarse OBSERVED bytes of active dims.
  "Predicted hash matches" = exact equality of the two 64-bit hashes
  (equivalently: all coarse residuals are 0).
- residual norm = isqrt(Σ r_f[i]²) over ACTIVE fine dims only.

### 2.2 Memory contract (executable, load-bearing)

```
INSTALL  iff  (residual_norm < EPS) AND (pred_hash == obs_hash)
WITHHOLD otherwise
```

Retrieval bias: the batch-mode memory store keeps installed entries
(task, judgment, coarse predicted bytes, pred_hash). For each new percept,
installed memories are ranked by prediction-consistency
= count of equal coarse-predicted bytes vs the query's predicted bytes
(higher first, ties broken by install order). The ledger records the top-3
ranks per fixture. Retrieval agreement modulates confidence: +100 if the
top-ranked memory's judgment equals the current judgment, −100 if it
contradicts (clamped 0..1000). The install gate itself is exactly the
two-condition rule above — nothing else.

### 2.3 Forward models and frozen constants

The forward prediction is always "the world continues as it is"
(stationarity/continuity prior), generated deterministically from current
invariants. Per task:

| task | primary invariants I (observed) | prediction P | judgment rule (frozen) |
|---|---|---|---|
| colordisc | inv(B): 6-dim patch-mean relations [lum/4, (R−G)/2, (G−B)/2, (R−B)/2, R/8, B/8] | P = inv(A): "B persists A's surface" | SAME iff RGB-space dist ≤ **40** (Approach A's validated threshold) |
| colorconst | inv(B): von-Kries discounted means (per-mille, A's method), 6-dim /16 | P = inv(A): "surface persists across illuminant" | SAME_SURFACE iff dist ≤ **150** (A's threshold) |
| shapetrans | 16-dim: fill-ratio/8 + 15-bin rotation-invariant radial profile | P = profile under 90° rotation: "rigid shape persists" | nearest prototype **1000/637/414** per-mille (A's) |
| pitchdisc | dppm = (f0B−f0A)·10⁶/f0A, q8 scale **250**; tone-B centroid predicted from tone-A | P: dppm = 0, "pitch persists" | SAME iff \|dppm\| < **5000** (= 0.5%, the truth boundary) |
| timbredisc | 7 harmonic ratios E_h/E_1 (×64), first vs second half | P: second-half ratios = first-half: "timbre persists forward" | centroid r, boundaries **1075/1400/3000** (A's) |
| motiondir | per-step displacements t=2..7 (12 dims, ×4) | P: disp_t = disp_{t−1}, "constant velocity" | STILL iff \|disp\|<3px else 8-way octant (A's rule) |

Secondary invariants: spatial stationarity (top/bottom halves) for t1–t3,
inter-half f0/centroid drift for t4–t5, linear-extrapolation centroid residual
for t6.

Frozen: **EPS = 24** (residual-norm units; ≈ 3 LSB mean deviation over the
active dims). Rationale: predictive consistency should tolerate small
measurement noise but not structural surprise; chosen by design, not by
measurement on the eval set. All judgment thresholds above are Approach A's
previously validated constants or the tasks' published truth boundaries —
no tuning on G2 results.

f0 estimation ports Approach A's robust estimator (autocorrelation coarse +
harmonic-energy fine grid + octave guard); shape mask ports A's
minority-brightness method. The G2 innovation is the
invariant→prediction→residual→contract layer, not the front-end estimators.

### 2.4 Ledger

FNV-1a-64 chain: L_0 = FNV("G2-PRP-1"); L_n = FNV(L_{n−1} ∥ record bytes).
Single-fixture mode emits the one-record chain; batch mode chains across the
manifest in order. No timestamps.

## 3. Fixtures

- Base: frozen harness fixtures (`senses/rebuild/harness/fixtures`,
  MANIFEST.sha256): 370 primary + 370 noise + 185 adversarial, 6 tasks.
- Adversarial augmentation (G2-specific, KB4-targeted), 240 fixtures,
  deterministic generator `augment/augment.py` (splitmix64, master seed
  20260922; committed with sources). IDs `g2a_<task>_001` … `g2a_<task>_040`.
  Source selection: sorted primary fixture names of the task, methods
  round-robin in the order listed; each method's truth-invariance rule is
  stated and machine-checked by the generator (it asserts the invariant
  before writing):

| task | methods (round-robin) | truth rule |
|---|---|---|
| colordisc | M1 swap halves; M2 add ±24 uniform noise | invariant by construction (swap); M2 restricted to SAME-identical and DIFFERENT-easy sources (ΔE margin ≫ noise shift) |
| colorconst | M1 swap halves; M2 global ×0.5 exposure | invariant: same-photo relation preserved |
| shapetrans | M1 horizontal flip; M2 ±40 noise; M3 thin dark occlusion bar (10% width) | invariant: drawn class unchanged |
| pitchdisc | M1 per-tone time reversal; M2 ±900 int16 noise; M3 swap tone order | M1/M2 invariant (f0 unchanged); M3 maps HIGHER↔LOWER, SAME→SAME |
| timbredisc | M1 time reversal; M2 ±900 noise; M3 linear fade ×0.5 | invariant: harmonic class unchanged (M2/M3 on primary sources only) |
| motiondir | M1 frame-order reversal; M2 50% contrast flatten; M3 drop last frame | M1 maps N↔S, E↔W, NE↔SW, NW↔SE, STILL→STILL; M2/M3 invariant |

Total adversarial: 185 (harness) + 240 (augmentation) = 425 of 1165
fixtures = 36.5% deliberately misleading — satisfies the ≥30% requirement.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability**: mean primary accuracy ≥ 60% (equal task weights, same
  computation as the harness `score.py`).
- **B2 vs Approach A**: head-to-head judgment accuracy delta on the identical
  925 harness fixtures (A = frozen `a_raw` rebuilt from committed source).
  Win/lose reported; no significance theater — the table is the result.
- **B3 efficiency**: measured ops per percept (instrumented at element-visit
  grain, documented in BUILD_LOG) and bytes per percept (256-byte residual
  vector + record overhead) vs Approach A's measured ops/bytes.
- **B4 memory-contract proof (LOAD-BEARING)**: batch mode, adversarial
  fixtures (425), contract vs ablated (always-install) gate on identical
  percepts. PASS iff (a) dispositions differ on ≥10% of adversarial fixtures
  AND (b) contract false-installs < ablated false-installs. Else the contract
  is decoration → fork FAILS.
- **B5 KB4**: adversarial false-install rate ≤ 8% per install (the stricter
  of the skeleton's 10% and G2's own 8% bar). Also reported per fixture.
- **B6 determinism**: first 10 primary fixtures per task, 3 runs each,
  byte-identical stdout; ledger chain re-verified by an independent checker.
  Any mismatch → fork FAILS.
- **B7 beauty**: (i) elegance of the mechanism against the hypothesis's own
  beauty claim (prediction as the single bridge from perception to memory);
  (ii) output quality — G2 emits invariant-space residual vectors, not
  sensory reconstructions, so human ear/eye judging is N/A (documented, not
  evaded: there is no audio/image artifact to judge).

## 5. Kill criteria

G2's own kill bar, verbatim: **false-install rate > 8%** (adversarial,
per install) **or integration success < 85%** kills G2.
Integration success = fraction of primary fixtures yielding a complete
percept record + disposition + ledger entry with exit 0.
PLUS: fork dies if B4 fails (contract is decoration) or B6 fails
(non-determinism). No other bars kill.

## 6. Evaluation procedure (frozen)

`evidence/eval_g2.py` (committed with sources): rebuilds A from frozen
source; runs G2 single-fixture mode over all 1165 fixtures; runs G2 batch
mode (contract + ablated) over the 425 adversarial fixtures; computes
B1–B6 mechanically; writes `evidence/EVAL_G2.md` and `evidence/LEDGER.md`.
Development (before this prereg commit): none on the eval set — constants
above are design choices and Approach A's published values. Post-freeze
code changes are bug fixes only; EPS/thresholds/scales are never touched
after this commit.

## 7. Commit map

`senses/pam-rebuild/forks/G2/`: `PREREG_G2.md` (this file, alone first),
`src/` (g2_sense.zag, R33_NATIVE_IO_V1.zag), `augment/` (augment.py),
`evidence/` (eval_g2.py, EVAL_G2.md, LEDGER.md, BUILD_LOG.md).
Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via
`~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`.
No binaries, no `.zagd`.
