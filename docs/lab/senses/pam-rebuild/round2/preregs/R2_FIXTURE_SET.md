# PAM ROUND 2 — Frozen fixture set R2A (shared by all round-2 preregs)

**Status: FROZEN 2026-09-22. No fixture changes after results — additions require a prereg amendment, never a silent edit.**

Debate B recommendation 1 (answered structurally, not rhetorically): a NEW adversarial suite is frozen here, before any round-2 revision work, so no round-2 claim can be a post-hoc rewrite of round-1 bars against round-1 fixtures. All corruption families below are new or re-instantiated; two round-1 families are carried over explicitly marked CARRYOVER for regression measurement.

## Suite R2A — composition

**Trial** = one `(task, fixture)` execution. Total frozen pool:

- **Normal: 5,000** = 740 frozen harness fixtures (370 primary + 370 noise from `senses/rebuild/harness/fixtures`, MANIFEST.sha256) + 4,260 generated `r2n_<task>_<i>` with the SAME distributions as the frozen primary set per `harness/FIXTURE_SOURCES.md`: colordisc 1080, colorconst 720, shapetrans 1296, pitchdisc 720, timbredisc 720, motiondir 564.
- **Adversarial: 5,000** = 185 frozen harness adversarial + 4,815 generated `r2a_<task>_<i>`, ≥30% deliberately misleading high-confidence inputs, corruption families below. Distribution: colordisc 1150, colorconst 680, shapetrans 1150, pitchdisc 1150, timbredisc 690, motiondir 995.
- Each prereg specifies which subset of R2A it evaluates (all 10,000 unless stated), so the suite is one frozen pool with frozen per-hypothesis trial plans.

## Attack families (fixture ID prefix `r2a_<task>_<i>`; truth from the true stimulus, not the corrupted appearance)

| Family | Task | Method | Target failure mode | Count |
|---|---|---|---|---|
| R2A-COL-1 | colordisc | metamer-pairs — truth=DIFFERENT, two spectra with distinct chromaticity rendered to RGB Euclidean <15 | fools color-appearance features; front-end reads SAME | 400 |
| R2A-COL-2 | colordisc | illuminant-drift — truth=SAME surface, illuminant shifts mid-item | fools static color-balance; front-end reads DIFFERENT | 350 |
| R2A-COL-3 (CARRYOVER) | colordisc | gray-trap — truth=DIFFERENT (ΔE2000 ∈ [2.6,5.0]) but mean-RGB Euclidean <25 | round-1 regression check | 400 |
| R2A-CCN-1 | colorconst | extreme illuminants — blue ≈12000K / red ≈2200K von Kries multipliers + 0.55 exposure | fools illuminant normalization | 340 |
| R2A-CCN-2 | colorconst | mixed-illuminant — half-frame warm, half-frame cool, same surface | fools global-illuminant priors | 340 |
| R2A-SHP-1 (CARRYOVER) | shapetrans | occlusion-bar — solid dark bar across the shape; truth = underlying shape | signature collision (G3's killer) | 400 |
| R2A-SHP-2 | shapetrans | distractor-blob — second same-color blob beside the target; truth = target shape | attention/witness capture | 450 |
| R2A-SHP-3 | shapetrans | low-contrast gray + full clutter | fools segmentation | 300 |
| R2A-PTC-1 (CARRYOVER) | pitchdisc | near-threshold — Δf/f ∈ [0.15%,0.45%] SAME / [0.55%,0.85%] HIGHER/LOWER | fools threshold placement | 350 |
| R2A-PTC-2 | pitchdisc | glide-through-threshold — pitch glides through the discrimination threshold mid-tone; truth from endpoint ratio | fools static-tone models | 400 |
| R2A-PTC-3 (CARRYOVER) | pitchdisc | harmonic-distractor — tone B with 0.6× 2nd + 0.3× 3rd harmonic | fools f0 estimators | 400 |
| R2A-TMB-1 (CARRYOVER) | timbredisc | boundary-straddling — centroid ratio within ±10% of 1075/1400/3000 boundaries | fools coarse bins | 250 |
| R2A-TMB-2 | timbredisc | harmonic-boost ×1.15 on 2nd harmonic — class moves without moving coarse bins (G3's collision) | lossy-signature collision | 250 |
| R2A-TMB-3 (CARRYOVER) | timbredisc | distractor — BRIGHT weak-fundamental, DARK extra-3rd, RICH pushed-bright, near-PURE faint-2nd | fools distractor handling | 190 |
| R2A-MOT-1 | motiondir | reversed-video — constant-velocity motion played backward; truth = true direction | fools constant-velocity predictors (G2's killer) | 350 |
| R2A-MOT-2 | motiondir | flicker/two-motion — 30%-misleading flicker + superimposed second motion; truth = dominant direction | fools lattice support (H1's killer) | 350 |
| R2A-MOT-3 (CARRYOVER) | motiondir | camouflaged — contrast →25%, 1px/frame | fools motion energy | 295 |

## Paired interventional set R2P (fixture ID prefix `r2p_<task>_<i>`) — for R2-3

1,200 fixtures (200/task): each fixture is a **paired pair** (fooled instance F, clean-gate instance G) built from the same underlying scene. F carries a corruption from the family list above attacking the front-end's primary feature band; G is a **disjoint evidence span** declared clean (later temporal window, spatially disjoint region, or second modality) that an honest gate can see. The pairing is mechanical: F and G share the scene ID, differ only in the corrupted band. Gate under test sees F's formation evidence; its gate-evidence must be drawn from G. Withhold bar: ≥90% of F-instances withheld (they must not install).

Disjoint-span declarations per task (frozen):
- colordisc / colorconst: temporal — F = frames 1–60 under corruption, G = frames 61–120 under neutral illuminant.
- shapetrans: spatial — F = full frame with occlusion/distractor, G = the non-overlapping quadrant holding the target unoccluded.
- pitchdisc / timbredisc: temporal — F = seconds 0–2 (corrupted tone), G = seconds 2–4 (same source, uncorrupted token).
- motiondir: temporal — F = frames 1–50 (fooled), G = frames 51–100 (clean high-contrast presentation of the same motion).

## Held-out split R2H (fixture ID prefix `r2h_<task>_<i>`) — for R2-12

1,000 adversarial trials (167/task × 6, one task takes 166; exact split recorded in the generator ledger) drawn from the same generator with stream id 900+taskidx. **Sequestered**: the R2H input list is committed in a sealed manifest whose contents are not read by the revision loop until the revision budget is exhausted; the prereg records the SHA256 of the sealed manifest. Final evaluation reads R2H once, on the frozen flagger.

## Generator (frozen with the suite; generator script committed with build sources as a preregistered instrument)

- MASTER seed = 20260923 (new; round 1's was 20260922). Stream ids: normal-ext = 400+taskidx, adversarial = 500+taskidx, paired = 600+taskidx, holdout = 900+taskidx. Per-fixture seed = splitmix64(splitmix64(MASTER ^ stream·0x9E3779B97F4A7C15) ^ index·0xBF58476D1CE4E5B9) — same construction as `harness/gen.py`.
- Truth files `<id>.truth` written alongside each fixture, from the true stimulus.
- Task index: colordisc=0, colorconst=1, shapetrans=2, pitchdisc=3, timbredisc=4, motiondir=5.
- MANIFEST.sha256 covers all frozen harness fixtures plus every generated byte. No fixture enters scoring without a manifest entry.
