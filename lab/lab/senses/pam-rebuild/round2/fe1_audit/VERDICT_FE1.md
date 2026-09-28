# VERDICT — FE1 novel-family formation audit (R3-2)

**Date:** 2026-09-24. **Crew:** FE1 audit crew (no build).
**Prereg:** `PREREG_FE1_AUDIT.md` (committed alone as
`a49dcb237dbfd29b10d12fcf5ab5caaf0a595dc7` BEFORE any measurement).
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.

## 1. Method (per frozen prereg)

- Frozen inputs verified: `v2/redteam/fixtures/sealed/` manifest digest
  `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
  recomputed exactly; 576/576 per-file sha256 match.
- Per family: the prereg-specified deterministic separator run over the 24
  frozen fixtures; accuracy = matches/24; bar ≥ 20/24 (≥80%).
- Reference evaluator: frozen `audit_fe1.py` (numpy only as a vectorized
  multiply-accumulate evaluator for the specified correlator banks — same
  arithmetic as the bounded MAC loops, directly portable to pure Zag; zero
  RNG). Run 3×: predictions-file sha256 identical all three runs —
  `681e8a5bc0a699429aa831281d88761dfe87506a9e56017b2fb51541f11203f3`.
- COL-5 fallback: machine-checked Bayes-ceiling proof (`col5_ceiling.py`).

## 2. Twelve-family verdict table

| family | R2-4 sense | separator accuracy | verdict | separator (feature family → rule) |
|---|---|---|---|---|
| PTC-4 detune-beats | 20/24 | **24/24 (100%)** | SEPARATOR | spectral: correlator-bank pitch of segA vs center of segB's two beat partials; \|Δf\|<2.5 Hz→SAME (SAME cases Δ=0.00 exactly; others \|Δ\|≥5) |
| PTC-5 gap-tone | 24/24 | **24/24 (100%)** | SEPARATOR | spectral: segA pitch vs segB pitch outside the known 60 ms gap window (\|Δ\|≥7 on non-SAME) |
| TMB-4 env-reversal | 9/24 | **24/24 (100%)** | SEPARATOR | spectral: harmonic-sum f0 + A2/A1 ratio (classes 0.25/0.60/0.70 exactly; thresholds 0.42/0.65). The lure is provably inert: time-reversal of a real signal preserves \|X(f)\| exactly |
| TMB-5 formant-twin | 9/24 | **24/24 (100%)** | SEPARATOR | spectral: full-spectrum centroid; DARK 979–1127 Hz vs BRIGHT 2293–2592 Hz (threshold 1600) |
| COL-4 adapt-ramp | 12/24 | **24/24 (100%)** | SEPARATOR | spatial: mean color of left panel vs ramp-neutral edge columns of right panel; d=1.8 (SAME) vs 65.0–65.5 (DIFFERENT), threshold 25 |
| COL-5 drift-metamer | 12/24 | 6/24 attempted; **ceiling 15.5/24 (64.6%)** | DEFENSE-SCOPE | see §4 — no byte-function reaches the bar (machine-checked) |
| CCN-3 checker-illuminant | 12/24 | **24/24 (100%)** | SEPARATOR | spatial: per-quadrant von-Kries inversion with the known 2×2 illuminants, texture MAD vs left panel (0.75 vs ≥14.4, threshold 4) |
| CCN-4 exposure-flicker | 12/24 | **24/24 (100%)** | SEPARATOR | spatial: per-band exposure inversion (middle band ÷0.55), texture MAD (0.65 vs ≥15.4, threshold 4) |
| SHP-4 shadow-decoy | 8/24 | **24/24 (100%)** | SEPARATOR | spatial+color: blue-keyed target mask (target painted last) vs bit-exact shape templates; winning IoU = 1.0000 on all 24 |
| SHP-5 tile-scramble | 10/24 | **24/24 (100%)** | SEPARATOR | spatial: forward tile-displacement templates (exact offsets/order/clipping) vs red mask; winning IoU = 1.0000 on all 24 |
| MOT-4 strobe-alias | 12/24 | **24/24 (100%)** | SEPARATOR | spatiotemporal: frame-0 comet-tail orientation (head centroid minus tail centroid), cos = 1.000; defeats the wraparound alias by reading the depicted tail, not nearest-neighbor differencing |
| MOT-5 induced-motion | 13/24 | **24/24 (100%)** | SEPARATOR | spatiotemporal: absolute dot displacement frame 0→7 (still = 0 px; moving ≥ 27 px); the moving surround is ignored by construction |

**Totals:** 11 SEPARATOR (all 24/24), 0 UNOBSERVABLE, 1 DEFENSE-SCOPE.
Separators: 270/288 overall (93.8%) vs the sense's 154/288 (53%).

## 3. Kill-bar adjudication

- **KB-FE1 per family:** 11 families PASS via ≥80% separators. COL-5 FAILS
  the separator bar AND the unobservability bar (6/24 fixtures are
  byte-unambiguous, so truth is recoverable in principle for those) →
  the "sense can learn COL-5" claim is **KILLED**; COL-5 is DEFENSE-SCOPE.
- **Program-level:** 11/12 families resolve to (a)/(b) with byte-level
  evidence ≥ 4 → the audit is **USEFUL** (not killed).
- No fixture was relabeled or excluded. Any relabel/exclusion recommendation
  requires Micah's prereg amendment; this verdict is evidence, not the change.

## 4. COL-5 — defense-scope finding (the honest reason)

COL-5 is a genuine metamerism trap, and the trap works. The generator
chooses the drift D to satisfy S2·D/255 = S1 almost exactly; the surface
difference (18,−12,+9) survives only as sub-LSB rounding of ONE shared
integer jitter j ∈ [−5,5]. Both panels are flat fills (verified per-pixel),
so the entire stimulus reduces to two RGB triples (S1, obs) with
obs = int(S1 + S2·j/255).

Machine-checked ceiling (`col5_ceiling.py`, committed):
- The generator's f64 drift math is replicated **bit-exactly** (op order
  preserved) — validated by recovering each fixture's ground-truth jitter
  via a replica of `rt_draw`/`rt_mix` and reproducing the observed bytes
  under the true hypothesis on **24/24** fixtures (this also confirms the
  truth sidecars).
- Any separator is a function g(S1, obs) → {SAME, DIFFERENT}. The
  accuracy-maximizing g is the Bayes rule (predict the hypothesis with
  more j-preimages; truth prior 12/12 on the frozen set). It scores
  **15.5/24 = 64.6%**: 17/24 fixtures are byte-ambiguous (the observed
  triple is produced by both hypotheses), 6 resolve correctly, 1 resolves
  wrong.
- The Bayes rule uses full white-box knowledge (true delta, exact f64
  model); no byte-function with less knowledge can exceed it. **15.5/24 <
  20/24, so no ≥80% separator exists — this is a proof, not a failed
  search.**
- It is NOT MOT-1-class unobservable: 6/24 fixtures are byte-unambiguous,
  so truth is recoverable in principle for those. Hence DEFENSE-SCOPE
  rather than UNOBSERVABLE.

**Consequence:** the sense cannot learn COL-5 as a perceptual discrimination
(the signal was erased by the illuminant design, not merely obscured). The
correct posture is refuse-by-construction on metameric pairs: when two
candidate surfaces are related by a near-exact uniform drift with a shared
rounding signature, the gate must withhold rather than guess. This is a
defense (D-line) target, not a front-end (FE2) target.

## 5. Offense-actionable handoff (FE2 targets)

The 11 SEPARATOR families carry **unused signal**: the truth is in the bytes
at 100% separability and the R2-4 sense's formation does not extract it
(worst gaps: SHP-4 8/24→24/24, TMB-4/5 9/24→24/24, SHP-5 10/24→24/24).
Each row's separator column (§2) is the FE2 detector spec: feature family,
exact decision rule, and measured margin. All rules are bounded integer /
MAC-loop computations — directly implementable as pure-Zag structural
detectors over the sense's formation inputs (the V2-C D1 pattern that
already worked: D1 cut PTC-2 400→0).

Per-family notes for FE2:
- PTC-4/PTC-5: the sense already reaches 20/24 and 24/24; the remaining
  PTC-4 gap (4 trials) is the beat-partial confusion the center-of-partials
  rule fixes.
- TMB-4: build the magnitude-spectrum path; the envelope-reversal lure is
  mathematically invisible to it — do not let formation features see the
  raw envelope.
- TMB-5: spectral centroid at 1600 Hz; the sense's 9/24 suggests its
  timbre features key on f0, not the formant.
- COL-4: compare at the ramp-neutral edge; never compare panel means under
  a spatial ramp.
- CCN-3/CCN-4: per-region (not global) white-point normalization before
  any surface comparison.
- SHP-4: color-key the last-painted (saturated) shape before shape
  classification; the shadow decoy is defeated by paint order, not by
  smarter shape features.
- SHP-5: match against forward-displaced templates, not the canonical
  shape — or equivalently, invert the fixed tile offsets first.
- MOT-4: read the depicted motion cues (comet-tail orientation), not
  nearest-neighbor frame differencing, under strobing/wraparound.
- MOT-5: track the target's absolute position; the surround is the lure.

## 6. Limits and caveats

- Separators are measured on the 24 frozen fixtures per family (the
  preregistered bar); thresholds were frozen in the prereg from generator
  constants, but FE2 must re-validate on held-out draws before claiming
  generality. The reported margins (e.g. COL-4 1.8 vs 65, TMB-5 1127 vs
  2293) suggest headroom, not fragility — except COL-5, which is proven
  unlearnable at the bar.
- The reference evaluator uses numpy-vectorized MACs; the specs are
  pure-Zag-portable (bounded loops, integer arithmetic, f64 only where the
  frozen generator uses it). FE2 owns the Zag port.
- PTC-5's frozen 24 contain no SAME cases (all HIGHER/LOWER); the |Δ|<2.5
  SAME rule is validated on PTC-4's SAME cases (Δ=0.00 exactly).
- This audit says nothing about the gate: all verdicts are about signal
  availability at the front end.

## 7. Evidence index (this commit)

- `PREREG_FE1_AUDIT.md` — frozen prereg (committed alone beforehand as
  `a49dcb23`).
- `audit_fe1.py` — frozen separator implementations (zero RNG).
- `predictions.csv` — per-fixture truth/prediction/detail, 288 rows;
  sha256 `681e8a5bc0a699429aa831281d88761dfe87506a9e56017b2fb51541f11203f3`
  (identical across 3 runs).
- `col5_ceiling.py` + `col5_ceiling.csv` — COL-5 Bayes-ceiling proof;
  csv sha256 `a8aa8aeca90a7ac059e2917f673ff9d736c17a5adb8592e606d4c2bb9f41f11e`.
- `digests.txt` — input manifest digest + all evidence digests.
- No binaries, no `.zagd` files.
