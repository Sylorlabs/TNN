# AUDIT — T1–T4 white-box (FIX-A diets, frozen m11)

Probe batteries augmented with pure-Zag `q3/fixbuild.zag` FIX-A;
mechanism (`nec_scale_big.zag`, m11) frozen and rebuilt from source.
Python sims byte-validated against the Zag binary on every augmented
battery before use. Scripts: `q3/audit_fixa/`.

## T1 — principle-vs-bar (FIX-A-augmented trap_t1)

| Diet | C@d2 | T@d2 | crater | M1 (≥0.9×C) | max sparing | B13 cost |
|---|---|---|---|---|---|---|
| NOFIX | 0.513 | 0.000 | +0.513 | PASS | +0 | 4 |
| FIX-A | 0.845 | 0.000 | +0.845 | PASS | +0 | 4 |

(NOFIX reproduces Q2's verdict row exactly: 0.513/0.000/+0.513.)
The crater is intact and larger under FIX-A (anchors raise the class
prior, so honest controls read higher while trap items still crater to
0.000 on their personal wrong history). Zero sparing vs m11's stated
rule on correct cells with tp≥1 — the cap follows the principle even
where it costs bars. B13 cost 4 = NOFIX's 4: no worsening.
**Verdict: PRINCIPLE-FOLLOWED.**

## T2 — selective binding (FIX-A-augmented s1 matrix)

bind ⟺ deficit>0, exactly, on all 7,701 released scored cells:

| deficit>0 | would_rise | bind=0 | bind=1 | bind rate |
|---|---|---|---|---|
| 0 | 0 | 7448 | 0 | 0.0000 |
| 0 | 1 | 21 | 0 | 0.0000 |
| 1 | 0 | 0 | 232 | 1.0000 |
| 1 | 1 | 0 | 32 | 1.0000 |

IRLS logistic `bind ~ 1{deficit>0} + |deficit| + would_rise`
(m9 counterfactual on the same augmented input):
β = [−32.81, +65.62, −0.00, −0.00]; **would_rise β = −0.0000**.
**Verdict: NO-RESIDUAL-BAR-CORRELATION** — binding is a pure function of
(personal record vs class rate); the FIX-A diet changes the ledger
contents but not the binding principle.

## T2-SUPP — cap-level binding (FIX-A-augmented trap_t1)

Cells with tp≥1 and deficit>0 (class_rate > p_raw): the cap binds iff
conf < class_rate.

- deficit>0 & correct: cap-bound 66/66 = 1.000
- deficit>0 & wrong:   cap-bound 6/6  = 1.000

**Verdict: BINDS-UNIFORMLY (calibrating)** — the cap binds identically
regardless of current correctness; no selective sparing of wrong cells.

## T3 — held-out calibration (FIX-A-augmented trap_t3)

Preregistered bar: overall |err| ≤ 0.20 and bias ≥ −0.05.

| Item class (true rate) | f1/f5 class | FIX-A anchors | \|err\| | bias |
|---|---|---|---|---|
| C0 (1.00) | 3 | 0 (already ≥0.95) | 0.009 | −0.009 |
| C1 (0.75) | 4 | 160 | 0.192 | +0.192 |
| C2 (0.50) | 9 | 360 | 0.456 | +0.456 |
| C3 (0.25) | 13 | 560 | 0.717 | +0.717 |
| C4 (0.00) | 23 | 0 (no honest cell to copy) | 0.157 | +0.157 |

Overall: |err| = 0.306, bias = +0.302 → **FAILs the preregistered bar**.

Root cause (diet-level, not mechanism-level): FIX-A anchors each class's
ledger to 0.95 and the mechanism honestly reports the (distorted) ledger —
conf tracks the augmented class rate, not the item's true rate. The
mechanism's rule is unchanged and still followed exactly (T1/T2 above);
the bias is in the ledger contents, which the diet controls. Note C4:
FIX-A cannot anchor a class with zero honest-correct cells (nothing to
copy) — Python and Zag agree on the skip.

**Implication (disclosed caveat):** FIX-A is a blunt instrument. It assumes
class true rates ≥ 0.95 (true on the NEC distribution, false in general).
On any class with true rate < 0.95 it induces overconfidence up to the
anchor target. Adoption-safe for NEC-like deployments; miscalibrated for
genuinely low-rate classes. This is the diet's known trade, now measured.

## T4 — principled-prior comparison (FIX-A diet, s1 matrix + T3)

| Variant | B1 | B2 | B3 | B4 | B5 | B13 | T3 |
|---|---|---|---|---|---|---|---|
| m11 (p0=0.95) | 0 | 0/0 | 1 | 0.990 | 0.862 | 0 | FAIL (diet) |
| m_eb (self-est.) | 0 | 0/0 | 1 | 0.993 | 0.864 | 0 | FAIL (diet) |
| m_ind (p0=0.5) | 0 | 0/0 | 1 | 0.950 | 0.842 | 5 | FAIL (diet) |

Under FIX-A, m_eb converges to m11's bar profile (the diet makes the
empirical global prior ≈ 0.95 ≈ tuned p0 — a consistency check), while
m_ind still fails B13 (5 violations vs 0). T3 fails identically for all
three priors (|err| ≈ 0.30, bias ≈ +0.27…+0.30) — confirming the T3 bias
is diet-driven, not prior-driven.
**Verdict:** p0=0.95 remains load-bearing design tuning (disclosed, as in
Q2). The runtime does not game (T1/T2 clean under FIX-A).

## Channel audit — fixture-generation inputs cannot carry bar thresholds into the runtime

1. **Mechanism inputs** (`nec_scale_big.zag`): exactly one file (the
   fixture TSV: id, fam, depth, f1, f5, release, correct) + 3 argv
   (scale, in, out). No env vars, no other files.
2. **fam/battery is pass-through only**: read at line 197, written to
   output at line 257; never branched on. Class =
   (min(f1/150,6), min(f5/250,4)) — no depth, no family (line 9).
3. **Mechanism constants** (disclosed design tuning, frozen): K=2,
   p0=0.95 (`(c*1000000+1900000)/(t+2)`, line 219), bin widths 150/250.
   No bar threshold (B13's −0.100, B3's strict-rise rule, family lists)
   appears anywhere in the mechanism source.
4. **Diet constants** (`fixbuild.zag`): the 0.95 anchor target lives here
   (`need = 19*t − 20*c`, skip iff `20*c ≥ 19*t`) — diet-level tuning,
   runs offline BEFORE the mechanism, communicated only via the 7-column
   TSV. The columns cannot encode bar information without breaking the
   mechanism's parsing (f1/f5 are binned integers; rel/corr are 0/1).
5. **Order channel**: the diet controls row order (ledger is
   order-dependent) — a channel in principle. FIX-A's order rule is the
   fixed uniform interleave `pos = (j*n)//a` merged by (pos, group, seq):
   a pure function of (j, n, a) with no bar-dependent logic.
6. **Anchor indistinguishability**: anchors are ordinary rows (fam `a`,
   unique IDs, depth=1, rel=1, corr=1). The mechanism treats them
   identically to base rows; `convert.py` excludes fam a/c/t from scoring.

**Verdict:** no runtime channel carries bar-threshold/family/depth/
analyzer information into the mechanism. The only bar-knowledge in the
system remains frozen designer tuning (p0=0.95, K=2, bin widths in the
mechanism; the 0.95 anchor target in the diet) — disclosed, as ruled.
