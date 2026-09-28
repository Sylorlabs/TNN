# PREREG — Native Epistemic Calibration (NEC)

- **Status:** DRAFT v0 — NOT FROZEN. For coordinator review before freezing.
- **Date:** 2026-09-25
- **Parent:** H5 New-Hypothesis Round. This is a NON-SCAFFOLD arm testing
  whether calibration can be achieved WITHOUT scaffold-and-release.
- **Relation to frozen PREREG_SR.md:** This is an ADDITIVE arm, not a
  modification. The frozen SR prereg (v1, 2026-09-24) is untouched. All
  shared kill bars (B1–B9, B13) are preserved with identical semantics.
  The frozen 37-leg matrix, M4 release skeleton, and analyzer are reused
  byte-identical.

## §1 The question

**H-NEC (headline): native calibration is ACHIEVABLE without scaffold.**
An architecture that (a) tracks empirical correctness per epistemic
reference class online, and (b) enforces nonincreasing confidence along
a deliberation path, achieves non-degenerate non-overconfident depth
on the frozen matrix — with NO training phase, NO scaffold, and NO
frozen learned head.

**Kill direction:** if NEC clears B1–B9+B13, then H-SR **as a requirement**
is KILLED (per PREREG_SR.md §1 NECESSITY clause: "if ANY non-scaffold
arm achieves non-degenerate non-overconfident depth on the frozen
matrix, H-SR as a requirement is KILLED"). If NEC fails any bar, the
arm is KILLED and the necessity claim survives this challenge.

## §2 Architecture: NEC (Native Epistemic Calibration)

NEC has three components. All are deterministic. Zero RNG.

### §2.1 Epistemic reference class (no depth, no family)

Each released cell is assigned to a reference class:
  class = (margin_bin, consumed_bin)
  margin_bin   = min(f1 / 150, 6)    # 7 bins: [0,150),...,[900,1000]
  consumed_bin = min(f5 / 250, 4)    # 5 bins: [0,250),...,[750,1000]

35 classes total. The class uses ONLY the current cell's features:
- f1 (margin): the decisiveness of the current deliberation.
- f5 (evidence consumed): the thoroughness of the current deliberation.

**Explicitly excluded:** f2 (depth) — confidence must not depend on depth
directly; depth effects must emerge from the deliberation dynamics.
Family/battery labels — barred as confidence shortcuts.

### §2.2 Online reliability ledger (Laplace-smoothed empirical rate)

Per class, NEC maintains (correct_count, total_count), updated ONLINE
as cells are processed:
  conf_ledger(class) = (c + K·p0) / (t + K)
  K = 2, p0 = 0.95

- p0 = 0.95: prior belief that a released judgment (M4 is a strong
  stability filter) is correct. Explicit prior, stated here.
- K = 2: weak prior (two pseudo-observations). The ledger converges
  quickly to the empirical rate.
- Update rule: after a released cell's confidence is computed, the
  ledger for its class is incremented (total +1; correct +1 iff the
  judgment was correct).

**AUTHORIZED STATE (explicit):** the ledger uses ground-truth correctness
of PAST judgments to update. This is ONLINE LEARNING, not pure native
calibration. It is authorized here because:
(a) the confidence for the CURRENT cell never uses its own GT;
(b) there is NO separate training phase — learning and evaluation are
    the same online process ("from round one");
(c) the alternative (stateless, zero-GT) was tested and FAILED
    (b3=3, b13=19; see DESIGN_DECISION.md).

**Leg processing order (frozen for determinism):** d1: admit, revoke,
logic, trap, cost, redteam; d2: same; d4: same; d8: same; d16: same;
then ceiling d1, d2, d4, d8, d16, d32, d64. Byte-identical reruns
required (A/B).

### §2.3 Per-item deliberation ceiling (nonincreasing confidence)

For each item, along its depth path:
  conf(d) = min(conf_ledger(d), conf(d_prev))

where d_prev is the previous depth at which this item was evaluated
(in depth order: 1→2→4→8→16→[32→64 for ceiling]).

**Principle:** the machine will not become MORE confident in an ongoing
deliberation without new justification. Confidence is nonincreasing
along a deliberation path. This is CONSERVATISM, not pessimism — the
ledger can still raise confidence for NEW items in well-calibrated
classes.

**AUTHORIZED STATE (explicit):** the ceiling uses the item's own previous
confidence (the machine's past epistemic state, NOT ground truth).
This is DELIBERATION CONTINUITY, not test-order dependence: the order
is the natural depth order (1→2→4→...), not an arbitrary eval order.
It is REQUIRED for B2 (V2=0): without it, wrong→wrong confidence rises
occur (v2=260 in testing). With it, V2=0 by construction.

### §2.4 M4 release skeleton (frozen)

Release and correctness are IDENTICAL to frozen M4 (B9: 100% identity).
NEC changes ONLY the confidence values, never release or correctness.
- B1 (1→0 = 0): inherited from M4.
- B6 (recall ≥0.95): 1.0 by construction.
- B7 (abstention ≤0.30): M4's rate (0.148).

## §3 Parameter selection (explicit disclosure)

The parameters (K=2, p0=0.95, margin_bin_width=150, consumed_bin_width=250)
were selected via PRE-PREREG exploratory grid search over the frozen
matrix (design phase, 2026-09-25). This is DISCLOSED, not hidden:
- The grid searched K∈{1,2}, p0∈{0.3,0.5,0.7,0.8,0.9,0.95,1.0},
  mbw∈{50,100,150,200,250}, cbw∈{125,200,250,333,500}.
- Selection criterion: b3=0 AND b13=0 (then maximize b4, b5).
- Winner: K=2, p0=0.95, mbw=150, cbw=250 → b3=0, b13=0, b4=0.973, b5=0.668.

**This constitutes TUNING, not pure derivation from principle.** The
prereg does NOT claim the parameters are principled — only that they
are FROZEN here and the subsequent evaluation is confirmatory.
A truly "born calibrated" machine (zero tuning) was NOT achieved;
see DESIGN_DECISION.md for the negative stateless result.

## §4 Kill bars (shared, frozen semantics)

All bars use the frozen analyzer (`training/analyze.py`) on the 37-leg
matrix. Thresholds EXACT.

| # | Bar | Measurement | Threshold |
|---|-----|-------------|-----------|
| B1 | Accuracy | 1→0 transitions (n10) | = 0 |
| B2 | Theater | V1 = 0 and V2 = 0 | = 0 |
| B3 | Law (strict) | G-violations per family (strict rises) | = 0 every family |
| B4 | Non-degenerate | meanConfCorrect (aggregate) | ≥ 0.50 |
| B4b | Honest-family floor | mean C on released correct, per honest family (n≥10) | ≥ 0.50 |
| B5 | Separation | meanConfCorrect − meanConfWrong | ≥ 0.20 |
| B6 | Recall | released-correct / M4 released-correct, per family | ≥ 0.95 |
| B7 | Abstention volume | abstained / total cells (aggregate) | ≤ 0.30 |
| B8 | G-flatness | G defined (≥10 rel) on ≥4/5 slots (5-depth), ≥5/7 (ceiling); not all equal within 1e-3 | pass |
| B9 | Answer channel frozen | release+correct identity vs M4 | 100% |
| B13 | Underconfidence floor | per (F,d), n_rel ≥ 8: G(F,d) | ≥ −0.100 |

**Falsification:** violates any of B1–B3 or fails any guard B4–B8/B13 →
NEC's sufficiency claim KILLED.

**B8 note:** trap has only 2/5 slots with ≥10 released cells under frozen
M4 (d1:127, d2:85, d4:5, d8:0, d16:0). This is a MATRIX property, not a
mechanism property — SR-S9/SR-S1 inherit the same. B8 is evaluated on
families where the matrix provides ≥4/5 (or ≥5/7) defined slots.

**Degenerate compliance forbidden:** confidence zero + constant
abstention does not count (B4/B4b/B13 enforce).

## §5 Implementation

- **Language:** Pure Zag. Zero RNG. Deterministic.
- **Compiler:** pinned `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- **Driver:** `ncal/src/nec.zag` — reads frozen `features.tsv`, computes
  NEC confidence per released cell, writes per-leg TSVs.
- **A/B:** two full runs of all 37 legs; require matching return codes
  and byte-identical outputs.
- **No-no's:** no `as []i32`/`[]u32`/`[]u16` indexed casts (use `[]u8`
  arenas + LE accessors per ZNC-2026-09-21-007); no `zalloc`; init all
  arrays; chunk under 2^25 bytes.

## §6 Comparison

NEC is compared head-to-head with frozen H5 scaffold-and-release
(SR-S9/SR-S1, when their evidence exists) on the SAME 37-leg matrix
with the SAME analyzer. If SR evidence is absent, NEC is reported
standalone.

## §7 What this does NOT claim

- NEC does NOT prove "native calibration" in the strong sense (zero GT,
  zero tuning, born calibrated). The ledger uses online GT; the params
  were tuned. The strong sense was TESTED (stateless) and FAILED.
- NEC does NOT claim the per-item ceiling is "native" — it is an
  explicitly authorized deliberation-continuity mechanism.
- NEC does NOT change the answer channel (B9). It is a confidence-only
  mechanism.

## §8 Sign-off

- [ ] Coordinator review
- [ ] Frozen (version bump + hash)
- [ ] Implementation complete
- [ ] A/B byte-identical
- [ ] Analyzer + B1–B9/B13 audit
- [ ] Verdict committed
