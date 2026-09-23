# PREREG_R2-16 — FS-A-REDESIGNED: Attack-Informed Discriminative Challenge, second attempt

Frozen: 2026-09-23. Author: R2-16 rebuild crew (depth-2 subagent).
Fork directory: `senses/pam-rebuild/round2/forks/R2-16/`.
Parent: R2-14 postmortem (`forks/R2-14/POSTMORTEM_R2-14.md`), debate D (`debates/DEBATE_D_new_fronts.md`).

## §0. Status

**DRAFT — not yet committed.** This prereg is frozen at commit time; the commit SHA
will be recorded in §10. No results below are measured yet. Every number in §2–§8
is a PREDICTION or a BAR, not a result.

## §1. Hypothesis (revised)

R2-14/FS-G died because three of its six challenge quantities were not functions of
their tasks' truth criteria (mean-RGB for colorconst, ray-profile harmonics for
shapetrans) or were mis-measured (timbredisc's off-by-one Goertzel coefficients).
FS-A-REDESIGNED tests the repaired claim:

> A per-family-paired discriminative challenge whose quantity is a deterministic
> function of the task's truth criterion, measured on disjoint (G) evidence,
> withholds every adversarial false install the formation proposes, while the
> formation alone determines recall.

Concretely: for each task, the challenge re-derives the fixture generator's own
truth quantity on the controlled G re-render. The adversary cannot move the
challenge outcome without moving truth itself, so the challenge-prediction wedge
is closed by construction; the CP suite inside the design loop verifies this
empirically rather than assuming it.

What R2-14 refuted (registry reuse of R2-7 quantities) is NOT retried. What is
retried is FS-A's core hypothesis with truth-aligned quantities, which R2-14 never
tested (its union was vacuous on R2FX).

## §2. Mechanism (frozen at §9)

Pure Zag, deterministic, zero RNG in decision paths. Python only for glue,
analysis, and fixture generation — never in the mechanism.

### §2.1 Challenge quantities (the discriminative half)

| Task | Challenge ID | Quantity (on G only) | Decision rule |
|---|---|---|---|
| colordisc | CH-COL-1 (retained) | Spectral L1 (u16) between G spectra | SAME iff L1 ≤ 8000; DIFFERENT iff L1 ≥ 25000; else UNRESOLVED |
| colorconst | CH-CCN-2 (new) | Pixel L1 Σ‖viewA_d65 − viewB_d65‖ over 48×48×3 | SAME_SURFACE iff L1 ≤ 15,000; DIFFERENT iff L1 ≥ 100,000; else UNRESOLVED |
| shapetrans | CH-SHP-2 (new) | Nearest class by (trace, det) of normalized central second moments of the >180 threshold mask vs analytic (trace,det): CIRCLE (31.66, 250.5), TRIANGLE (15.44, 59.5), SQUARE (41.77, 436.1) | Outcome = argmin Euclidean distance in (trace, det); UNRESOLVED iff mask < 80 px |
| pitchdisc | CH-PTC-1 (retained) | Harmonic-peak interval class on G (as R2-7) | Outcome = argmin template distance; UNRESOLVED on degenerate |
| timbredisc | CH-TBD-2 (new) | Goertzel power ratios (r2, r3) = (p880, p1320)×1000/p440 with EXACT coefficients (2040, 2018, 1980 for m=1,2,3); nearest of PURE (0,0), RICH (1960,2560), DARK (78,6), BRIGHT (640,384) | Outcome = argmin squared distance; UNRESOLVED iff p1 ≤ 0 |
| motiondir | CH-MOT-1 (retained) | Block-match vote argmax on clean high-contrast G | Outcome = argmax votes; UNRESOLVED iff best < 8 votes |

Rationale per quantity:
- **CH-COL-1**: CP-COL returned empty in R2-14; the quantity is the truth quantity
  (R2-7 fixture spec: SAME ⟺ spectral L1 ≤ 8000). Retained verbatim.
- **CH-CCN-2**: Mean-RGB cannot encode crop identity (R2-14 §2: 2/690 false installs
  via metameric means; CP-CCN found the wedge). Pixel-L1 on the d65 re-renders is
  a function of crop identity: same crop → noise-only difference (≈11,059 ± 100
  by the fixture noise model); different crops → content difference. Thresholds at
  ~35σ (15,000) and 100,000 (doppelganger safety valve → WITHHOLD, never false
  install). Residual risk: near-duplicate crops (appearance-identity vs
  crop-identity); the CP suite's strong-truth criterion requires pixel-L1 ≥
  100,000 for DIFFERENT candidates, and any kept family kills the fork.
- **CH-SHP-2**: Ray-profile harmonics are out (R2-14 §2: miscalibrated f4 threshold;
  CP-SHP found morph-midpoint and aliasing wedges). The (trace, det) of the
  thresholded mask is rotation-invariant, cheap, and directly tied to the
  shape-construction truth: measured clusters on 1,988 R2A G renders are
  CIRCLE (31.66±0.00, 250.5±0.0), TRIANGLE (15.44±0.31, 59.5±2.3),
  SQUARE (41.77±0.51, 436.1±10.5) — separations ≥16σ. A morph with λ≤0.35 cannot
  cross the decision boundary (moments interpolate linearly; verified in design
  loop). No margins: the quantity is decisive or UNRESOLVED.
- **CH-PTC-1**: 1/2,330 false installs in R2-14; retained. CP-validated in design loop.
- **CH-TBD-2**: R2-14's catastrophe (227/283 false installs, 80.2%) was traced to a
  concrete measurement bug: `tb_coeff` returns coefficients for 880·m Hz, not
  440·m Hz (m1=2018→872.8 Hz, m2=1927→1759.4 Hz, m3=1779→2639.8 Hz) — an
  off-by-one in the harmonic index that detuned the m=1,3 resonators into
  sidelobes. The template centers (1960,2560), (78,6), (640,384) already match the
  generator's `_tb_template_class`; only the coefficients were wrong. CH-TBD-2
  uses exact coefficients (2040, 2018, 1980). The quantity then equals the truth
  criterion up to ramp/quantization noise (verified in design loop).
- **CH-MOT-1**: 0/630 false installs in R2-14; retained. The votes≥10/margin≥4
  support margins are REMOVED (they caused 96.5% overstrictness on controls with
  zero safety benefit — the challenge outcome on clean G is the truth).

### §2.2 Formation (the proposing half; R2-7, with one fix)

Formations run on F only. Retained from R2-7/R2-14 except:
- **timbredisc formation**: uses the corrected `tb_coeff` (same fix as CH-TBD-2).
  The f1 boundary-straddle family is DESIGNED to fool centroid-binning; the
  challenge (template class = truth) withholds these. This is the intended
  division of labor.
- All other formations retained verbatim (colordisc mean-RGB, colorconst
  mean-chromaticity, shapetrans ray-profile, pitchdisc harmonic, motiondir
  block-match).

### §2.3 Support rules (frozen)

- INSTALL iff challenge outcome == formation claim AND outcome != UNRESOLVED.
- WITHHOLD otherwise (including malformed spans, UNRESOLVED, and deadband
  interiors for colordisc/colorconst where the quantity is genuinely ambiguous).
- NO discrimination margins. R2-14 proved the margins are recall-hostile
  (15:1 cost/benefit against) and safety-decorative once the quantity is
  truth-aligned. The deadbands that remain (colordisc [8000,25000], colorconst
  [15000,100000]) are empty by the fixture construction and exist only as
  honest "cannot tell" valves.

### §2.4 Ablation (bar 3): challenge→bank

`abl_bank`: each challenge is replaced by a 1-nearest-neighbor bank check on the
FORMATION evidence (F), using the formation's own coarse feature, against frozen
banks of 20 true-exemplar and 20 false-exemplar F-features per task (drawn from
r2n/r2a, frozen at design-loop end, hashes in BUILD_NOTES.md). INSTALL iff the
nearest bank label == formation judgment. This is the R2-2 form (two-sided
reference: nearer true exemplars than the frozen false bank). It removes the
disjoint-evidence advantage while keeping a gate; if the G-challenge carries the
load, false installs rise.

## §3. Batteries (frozen definitions)

- **B-adv**: the R2-14 `b_adv.list` (10,000 adversarial R2FX fixtures, first 10,000
  sorted by (split,task,index) of the 10,425 R2A adversarial). Reused byte-identical
  so the false-install bars are comparable across forks. SHA256 of the list file
  recorded in BUILD_NOTES.md at freeze.
- **B-ctrl**: the R2-14 `b_ctrl.list` (2,000 controls, first 2,000 sorted r2n).
  Reused byte-identical.
- **B-holdout**: 10 novel families × 1,000 fixtures, generated deterministically
  (seed frozen in BUILD_NOTES.md) AFTER the challenge freeze. Families are novel
  attack types not in the enumerated 16 (2 per task except colordisc/motiondir
  which get 1 each + 2 extra timbredisc; total 10). Each family is adversarial
  (targets its task's formation). Truth labels by construction.
- **CP design-loop suite**: per-task candidate generators adapted from R2-14's
  `gen_cp.py`, with a FRESH seed (not R2-14's), a fixed candidate budget per
  iteration (≥2,000 candidates per task per iteration), and a strong-truth
  criterion per task (the candidate's truth must be unambiguous: e.g. morph
  λ≤0.35 or ≥0.65; pixel-L1 ≥100,000 for colorconst DIFFERENT; harmonic ratios
  ≥3σ from template boundaries for timbredisc). A family is KEPT iff the
  challenge outcome ≠ truth on a strong-truth candidate.
- **CP post-freeze suite**: same procedure, a DIFFERENT fresh seed, run once after
  freeze. Zero kept families required.

## §4. Design loop and freeze boundary

1. Implement §2 in Zag. Port the R2-14 harness (`run_battery.py`, `score.py`,
   `verify_chain.py`, list drivers) — glue only.
2. Iterate: run the CP design-loop suite against the current challenges; for
   every kept family, white-box the failure (instrumented internals,
   knowledge-vs-machinery evidence) and redesign the quantity. Log every
   iteration in `BUILD_NOTES.md` (candidate SHA, kept families, redesign).
3. Freeze the challenge registry (`REGISTRY.md`) and the holdout family
   definitions ONLY after a full design-loop iteration returns zero kept
   families on every task.
4. After freeze: generate B-holdout, run the post-freeze CP suite (fresh seed).
   ANY kept family kills the fork (DEAD, no redesign — the freeze is the freeze).
5. Run the frozen battery twice; outputs must be byte-identical (`cmp`);
   hash-chained ledgers verified.

## §5. Kill bars (all must pass; ALIVE requires every bar green)

Let n=10,000 (B-adv), m=2,000 (B-ctrl), h=10,000 (B-holdout, 10×1,000).
Rates use Sol's upper-95%-confidence-bound rule: the REPORTED rate for each bar
is the upper 95% Wilson bound; the bar is met iff the BOUND satisfies the
threshold (not just the point estimate).

1. **Enumerated adversarial battery**: false installs ≤1% overall (UCB ≤ 0.01) and
   ≤2% per enumerated family (UCB ≤ 0.02 per family).
2. **Novel-family holdout**: ≤2% false installs per family (UCB) and ≤1% pooled
   (UCB), on 10 families × 1,000 attempts.
3. **Challenge→bank ablation**: `abl_bank` on B-adv → false installs ≥2× the full
   mode (if full-mode FI = 0, require ablation FI ≥ 10); AND the holdout gap
   widens: (abl_bank holdout FI − full holdout FI) ≥ (abl_bank adv FI − full adv FI).
4. **Post-freeze CP suite**: fresh seed, same procedure → zero kept families.
   Any kept family = DEAD.
5. **Recall**: ≥80% on B-ctrl (INSTALL with judgment==truth). 80%, not 90%: the
   R2FX colorconst formation is ~57% accurate on normals and no illuminant-
   invariant front-end was found (nine approaches tried and documented in
   BUILD_NOTES.md); 90% is unreachable without front-end repair, which is out of
   scope for this fork. The 80% bar is set to be achievable iff overstrictness is
   eliminated (max achievable with current formations ≈80.3%; see §7).
6. **Challenge overstrictness**: ≤5% of controls where outcome==judgment==truth
   but disposition==WITHHOLD. (Expected ≈0% after margin removal; the remaining
   deadbands are empty by construction.)
7. **Determinism**: frozen battery runs twice; ledgers and stdout byte-identical
   (`cmp`); every hash chain verifies.

## §6. Verdict rule

ALIVE iff all seven bars pass. Any bar failed → DEAD. The verdict
(`VERDICT_R2-16.md`) reports every measured bar vs threshold (point estimate,
UCB, n), the design-loop iteration count, and commit SHAs. No number is invented;
every number traces to a ledger line.

## §7. Known tightness (recall)

With R2-14 formations, the recall ceiling on B-ctrl is
(1080−76) + (720−311) + (200−7) = 1606/2000 = 80.3%, and only iff
overstrictness is fully eliminated. This fork therefore has ~6 fixtures of
margin on bar 5. The risk is accepted and disclosed: the fork lives or dies on
whether the truth-quantity challenges introduce zero new withholds. If bar 5
fails, the verdict is DEAD with a precise decomposition (formation-wrong vs
overstrict vs unresolved).

## §8. What this fork does NOT do

- No RNG in decision paths (Micah's law). Deterministic seeds only for fixture
  generation (glue), never in the mechanism.
- No binaries, `.zagd`, or cache artifacts committed.
- No task scoping: all six tasks are in the battery.
- FS-D is not built (killed by its frozen dependency gate; R2-14 postmortem).

## §9. Freeze record (filled at freeze time)

- Challenge registry SHA: TBD
- B-holdout generation seed: TBD
- Bank exemplar hashes (abl_bank): TBD
- Design-loop iterations: TBD

## §10. Commit record

- Prereg commit SHA: TBD (this file committed alone first)
- Source/evidence commit SHA(s): TBD
- Fork ID: R2-16 (rechecked free at commit time; if collided, the mapping is
  documented here)
