# PREREG — Native Epistemic Calibration (NEC), FROZEN v1

- **Status:** FROZEN v1 — 2026-09-25. Supersedes DRAFT v0.
- **Frozen by:** NEC coordinator, per Micah's ruling (2026-09-24 PDT):
  **B3 (strict: zero confidence-rises with depth, Gviol=0 per family) is the
  OPERATIVE default bar.** The refined reading (G>0 crossings) does not
  replace it. B3 stays the default for all continued NEC development.
- **Parent:** H5 New-Hypothesis Round. NEC is a NON-SCAFFOLD arm.
- **Baseline commit:** `7c01e2cad9ebc5b07839c4ecd50475cbcfedeb77`
  (`docs/lab/deliberation_depth/monotonicity/training/ncal/`).
- **Relation to frozen PREREG_SR.md:** additive arm, not a modification.
  The frozen SR prereg (v1, 2026-09-24) is untouched. All shared kill bars
  (B1–B9, B13) keep identical semantics. The frozen 37-leg matrix, M4
  release skeleton, and analyzer (`training/analyze.py`) are reused
  byte-identical.

## §1 The question

**H-NEC-v1 (headline): a non-scaffold architecture clears the FULL bar
set with B3 strict as the default bar.** The v0 round showed NEC is the
best-calibrated arm tested (only V2=0; fewest G-violations) but it does
NOT clear B3/B13, so H-SR as a requirement SURVIVED the v0 challenge.
This round continues NEC development to drive B3 failures to zero
without breaking B2, then holds the bars at long horizon (s1/s10/s100).

**Kill direction:** if a NEC variant clears B1–B9+B13 with B3 strict,
H-SR as a requirement is KILLED (per PREREG_SR.md §1 NECESSITY clause).
If no variant clears the set, the arm's sufficiency claim stays KILLED
and the residual is reported honestly — bars are never weakened to
manufacture a pass.

## §2 Baseline mechanism (NEC as built, frozen)

Three components. All deterministic. Zero RNG.

### §2.1 Epistemic reference class (no depth, no family)

class = (margin_bin, consumed_bin),
margin_bin = min(f1/150, 6) (7 bins), consumed_bin = min(f5/250, 4)
(5 bins). 35 classes. Uses ONLY the current cell's f1 (margin) and f5
(evidence consumed). f2 (depth) and family/battery labels are BARRED as
confidence inputs.

### §2.2 Online reliability ledger (Laplace-smoothed empirical rate)

Per class: conf_ledger = (c + K·p0)/(t + K), K=2, p0=0.95. Updated
ONLINE after each released cell's confidence is computed (total +1;
correct +1 iff the judgment was correct). **AUTHORIZED STATE
(explicit):** the ledger uses ground-truth correctness of PAST
judgments. This is ONLINE LEARNING, not pure native calibration.
Authorized because (a) the current cell's confidence never uses its own
GT; (b) no separate training phase — learning and evaluation are the
same online process; (c) the stateless zero-GT alternative was tested
and FAILED (b3=3, b13=19).

**Leg processing order (frozen for determinism):** d1: admit, revoke,
logic, trap, cost, redteam; d2, d4, d8, d16: same; then ceiling
d1–d64. A/B byte-identical reruns required.

### §2.3 Per-item deliberation ceiling (nonincreasing confidence)

conf(d) = min(conf_ledger(d), conf(d_prev)) along each item's depth
path (1→2→4→8→16→[32→64]). **AUTHORIZED STATE (explicit):** uses the
item's own previous confidence (deliberation continuity, not GT). This
is what achieves V2=0 (first and only in H5).

### §2.4 M4 release skeleton (frozen)

Release and correctness are IDENTICAL to frozen M4 (B9: 100% identity).
NEC changes ONLY confidence values.

## §3 Parameter selection (explicit disclosure — TUNED, not confirmatory)

K=2, p0=0.95, margin_bin_width=150, consumed_bin_width=250 were
selected via PRE-PREREG exploratory grid search over the frozen matrix
(K∈{1,2}, p0∈{0.3,…,1.0}, mbw∈{50,…,250}, cbw∈{125,…,500}; criterion
b3=0 AND b13=0 then max b4/b5). **This is TUNING, not derivation from
principle.** The prereg does NOT claim these parameters are principled
— only that they are FROZEN here. A "born calibrated" machine (zero
tuning) was NOT achieved.

## §4 Kill bars (shared, frozen semantics — B3 IS THE DEFAULT)

All bars use the frozen analyzer on the 37-leg matrix. Thresholds EXACT.
G(d) = mean_conf(released) − acc(released) per (family, depth), conf in
thousandths/1000. Gviol = strict rises G(d+1) > G(d) + 1e-12.

| # | Bar | Measurement | Threshold |
|---|-----|-------------|-----------|
| B1 | Accuracy | 1→0 transitions | = 0 |
| B2 | Theater | V1 = 0 and V2 = 0 (per-item wrong→wrong rises) | = 0 |
| **B3** | **Law (strict, DEFAULT)** | **G-violations per family** | **= 0 every family** |
| B4 | Non-degenerate | meanConfCorrect (aggregate) | ≥ 0.50 |
| B4b | Honest-family floor | mean C on released correct, per honest family (n≥10) | ≥ 0.50 |
| B5 | Separation | meanConfCorrect − meanConfWrong | ≥ 0.20 |
| B6 | Recall | released-correct / M4 released-correct, per family | ≥ 0.95 |
| B7 | Abstention volume | abstained / total cells (aggregate) | ≤ 0.30 |
| B8 | G-flatness | per frozen note (matrix-limited families excluded) | pass |
| B9 | Answer channel frozen | release+correct identity vs M4 | 100% |
| B13 | Underconfidence floor | per (F,d), n_rel ≥ 8: G(F,d) | ≥ −0.100 |

**Falsification:** violates B1–B3 or fails any guard B4–B8/B13 →
the variant's claim KILLED. **B2 must hold for every variant** (zero
theater is non-negotiable). Degenerate compliance forbidden
(confidence-zero + constant abstention does not count).

## §5 Baseline results (frozen analyzer, exact — the residual to attack)

| Bar | NEC v0 (m9) | Threshold |
|-----|-------------|-----------|
| B1 | 0 ✓ | =0 |
| B2 | V1=0, V2=0 ✓ | =0 |
| B3 | **6** ✗ | =0 |
| B4 | 0.972 ✓ | ≥0.50 |
| B4b | ≥0.984 ✓ | ≥0.50 |
| B5 | 0.668 ✓ | ≥0.20 |
| B6/B7/B9 | 1.00 / 0.148 / 100% ✓ | |
| B13 | **6** ✗ | =0 |

B3 violations (exact G curves):
- **ceiling/D: 2.** G = 1:+0.027, 2:+0.028 (+0.001), 4:+0.033 (+0.005),
  8:-0.004, 16:-0.004, 32:-0.004, 64:-0.004. Source: M4 selection —
  relrate 1.00→0.75→0.50 with acc fixed at 0.250; low-conf items
  abstain, released-set mean conf rises while every per-item conf is
  nonincreasing.
- **ceiling/O: 2.** G = 1:-0.414, 2:-0.439, 4:-0.449, 8:-0.430
  (+0.019), 16:-0.425 (+0.005), 32:-0.433, 64:n/a. Source: M4
  selection — relrate 1.00→0.75→0.50, released acc stays 1.000, mean
  conf of survivors rises 0.551→0.570→0.575.
- **redteam: 2.** G = 1:+0.313, 2:+0.311, 4:+0.472 (+0.161),
  8:+0.994 (+0.522), 16:+0.994. n=3 items. Source: tiny-n noise PLUS
  one wrong item (RT-K12-01) carrying conf 0.994 — its
  (margin,consumed) class is saturated with honest-correct items, so
  the class ledger cannot see it as adversarial; at d8 it is the sole
  released item.

B13 violations (6, all ceiling/O; n_rel ≥ 8 at d1,d2,d4,d8,d16,d32):
G ≈ −0.41…−0.45 (need ≥ −0.100). Items are correct (released acc
1.000) but receive conf ≈ 0.55–0.57: they sit in low-(margin,
evidence) classes pooled with trap/wrong items, and the ledger cannot
distinguish them without family labels (barred).

**Joint-constraint note:** on ceiling/O, B3 and B13 pull in opposite
directions — B13 wants G raised toward 0 (conf up toward acc=1.0),
while B3 forbids any upward step. A fix must raise O confidence
SMOOTHLY and MONOTONICALLY (or uniformly), never in steps.

## §6 Development protocol (variants v2, v3, …)

Each variant is a dated addendum: mechanism change + the §5 failure
source it attacks, written BEFORE running. Variants compete
head-to-head on the frozen 37-leg matrix with the frozen analyzer.

**Selection rule.** A variant is ADOPTED only if, vs the v0 baseline,
it (a) keeps B2 = 0 (V1=0, V2=0) — non-negotiable; (b) strictly
reduces B3 Gviol; (c) breaks no other currently-passing bar; (d) does
not increase B13 violations. If NO variant reaches B3=0, the round
reports the best variant and the exact residual — the bar is not
weakened, the residual is not hidden.

**PROHIBITED (bar-gaming, kills the variant on sight):**
- Family-level ceilings, caps, or adjustments — encoding B3 into the
  mechanism is hardcoding, not calibration.
- Quantization levels, smoothing constants, or priors chosen to clear
  the bar rather than from epistemic principle (record the principle
  or don't use the constant).
- Family/battery labels, or features that are family proxies, as
  confidence inputs.
- Post-hoc parameter selection against the frozen analyzer without
  disclosure (any tuning is recorded per §3 honesty standard).

**ALLOWED (principled directions):**
- Better reference classes: feature expansion over epistemically
  legitimate features (the features TSVs carry more than f1/f5; no
  depth, no family). Finer/coarser binning WITH a stated principle.
- Hierarchical / personal ledgers: shrinkage between a class ledger
  and the item's own track record (online learning from direct
  experience — same authorized GT class as §2.2, disclosed).
- Symmetric continuity: a per-item floor from the item's own
  correctness history (the mirror of the §2.3 ceiling), if it can be
  stated as a principle and doesn't break B2.
- Prior/strength changes (K, p0) WITH honest recording per §3.
- Reducing GT reliance where possible — but never faked: if a
  variant still uses online GT, it says so.

## §7 Long-horizon protocol (s1/s10/s100)

- s1: the frozen 37-leg matrix (this prereg's bars).
- s10/s100: the same matrix at 10x/100x item scale (per the
  training/build_10x, build_100x, results_10x, results_100x precedent;
  mech id 10; A/B byte-identical).
- The depth law (B2, B3) must hold at 100x: zero confident
  disagreements with depth, zero G-rises, at every scale.
- Red-team at horizon: the frozen H5 red-team battery's vectors,
  all contained, at s1/s10/s100.
- Scale legs use one binary with argv[1] selecting the config
  (s1/s10/s100); the runner diffs A/B per leg for determinism.

## §8 Implementation constraints

- Pure Zag. Zero RNG. Deterministic. Pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- No `as []i32`/`[]u32`/`[]u16` indexed casts (use `[]u8` arenas +
  LE accessors per ZNC-2026-09-21-007); no `zalloc`; initialize all
  arrays; chunk allocations under 2^25 bytes.
- Commit incrementally to `tnn-native-lab`; no binaries, no `.zagd`.
- The ledger's online GT use stays disclosed in every variant; a
  variant that reduces GT reliance PROVES it (ablation), not asserts it.

## §9 What this does NOT claim

- v0 does NOT prove "native calibration" in the strong sense (zero
  GT, zero tuning, born calibrated). The strong sense was TESTED and
  FAILED.
- Clearing B3 would not by itself prove the mechanism is "native" —
  only that it meets the frozen bars. The honesty disclosures (§3,
  §8) are part of the claim.
- The strict B3 bar may be partially unsatisfiable (tiny-n redteam);
  §6's honest-residual rule governs that outcome.

## §10 Sign-off

- [x] Frozen v1 per Micah's B3-default ruling (2026-09-25)
- [ ] Baseline reproduced byte-identical (SHA
      10b7a1f7ffac3006666943de074e306e899dd91e0d44be6613255e69f7cd471e)
- [ ] Variant addenda (each: mechanism + target + principle, pre-run)
- [ ] 37-leg head-to-head, frozen analyzer
- [ ] s10/s100 long horizon, A/B byte-identical
- [ ] Verdict committed (adopted variant or honest residual)
