# H5 Fork Ideas — Fable Deep Pass (2026-09-24)

Source: one deep batched round via `~/workspace/skills/unorouter/bin/fable_stream.py`
(model claude-fable-5.1). Full raw output: `~/workspace/h5_fork_round/ideas/fable_forks_raw.md`.
Four mechanisms proposed; none is a NEC iteration (NEC runs in parallel).

---

## Mechanism A — Differential Evidence Budget (DEB)

**Head form (integer math, thousandths):**
```
budget_0 = 1000
budget_t = clamp(budget_{t-1} + margin_t * (1000/nh) − (t * 1000 / max_depth), 0, 1000)
C(s)     = clamp(min(budget_t, clamp(margin_t * 1000 / nh, 0, 1000)), 0, 1000)
```
`nh` = hypothesis pool size (known at compile time). Budget is stateful per item
across the depth schedule: margin "purchases" budget, depth progression "charges"
it; depth_charge is monotone in t (a structural downward ratchet), while the
budget itself may be replenished by strong margin.

**Training/update:** budget parameters (charge scale) learned online; updates are
*clamped to never increase the depth_charge coefficients* — decrements allowed
only on epochs where G(d) shows positive slope for some family (monotone training
constraint).

**Q2 falsifiable prediction:** beats NEC on logic@8/16 and admit@16/32 (items
that keep strong margin across many depths get budget replenishment; NEC's
ceiling is fixed from the start). Loses to NEC on redteam@1–4 (tiny-n → noisy
margin → erratic budget) and trap@8/16 (adversarially sustained fake margin
fools replenishment); underperforms on cost@8 B5 separation.

**Q3 failure mode:** (6) M4 selection effects — most likely death. Budget tracks
*individual* items, not the population effect, so G-rises from released-population
shift are invisible to it. Structural property that helps: margin-replenishment
means survivors are repeatedly margin-tested, giving an implicit (if insufficient)
selection encoding; gradual depletion structurally prevents B1 (no 1→0 collapses)
and B2 (replenishment requires margin, which correlates with correctness).

**Q4 rank: #4, P(clear strict B3) ≈ 0.25.** Most NEC-like of the four; NEC
already fails B3 with 6 violations. Individual-item tracking cannot prevent
population-level G-rises when abstention rates shift across depths.

---

## Mechanism B — Disagreement-Geometry Head (DG)

**Head form (integer math):**
```
// D_t = pairwise disagreement fraction among survivors, in thousandths:
D_t = Σ_{i<j alive} |h_i − h_j| * 1000 / (nalive*(nalive−1)/2)   // h binary; 0 if nalive≤1
S_t = clamp(1000 − D_t, 0, 1000)                                 // agreement fraction
ΔD_t = clamp(D_t − D_{t−1}, −1000, 1000)                          // negative = converging
depth_suppress(t) = clamp(1000 − t*1000/64, 0, 1000)
C(s) = clamp((S_t*w_s + margin_t*w_m + (1000 − clamp(ΔD_t,0,1000))*w_v
             + depth_suppress(t)*w_d)/1000, 0, 1000)
```
Weights w_s, w_m, w_v, w_d ∈ [0,1000], sum ≤ 1000. All divisions bounded
(denominator ≤ 64·63/2 = 2016). The disagreement index is *not* reachable from a
flat weighted sum — it requires pairwise survivor structure.

**Training/update:** weights updated with a ratchet: if G(d+1) > G(d) for any
family in a batch, all weight updates in that batch are reversed for the
offending direction — weights only move in directions that reduce G-rise.

**Q2 falsifiable prediction:** beats NEC on redteam@16/32 (disagreement is
structural, robust to misleading margin; nalive=1 → D_t=0 is the correct
answer) and logic@16/32 (rich disagreement structure correlates with
correctness); should clear B3 better on ceiling families P/O/D by flagging the
interaction effects directly. Loses to NEC on admit@4/8 (disagreement is binary
0/1000 on simple items — overhead with no gain over margin) and all tiny-n legs.

**Q3 failure mode:** (4) spread anti-learning — most likely death. At high
depths where only adversarial items survive, survivors may have *low*
disagreement (all converged on the wrong answer) → D_t ≈ 0 → high confidence on
wrong items → G-rise. Structural property: the *velocity* feature ΔD_t detects
sudden convergence-at-depth as an anomaly (normal convergence is gradual), so
the head can learn to suppress it — but this is *learned*, not architectural,
and only works if training sees enough adversarial-convergence examples.

**Q4 rank: #3, P(clear strict B3) ≈ 0.35.** Disagreement captures the
population-level structure G(d) measures, but success depends on learned
features surviving adversarial convergence; on redteam/trap, low disagreement on
converged-wrong survivors raises G.

---

## Mechanism C — Two-Head Adversarial Cap (THAC)

**Head form:**
```
P(s) = clamp((Σ w_i·f_i^P)/1000 + b_P, 0, 1000)      // optimistic predictor
C_n(s) = clamp(min(
           margin_t,                                   // censor never exceeds margin
           1000 − (t*1000/64),                         // structural depth penalty
           1000 if nalive≤2 else clamp(nalive*1000/nh, 0, 1000)
         ) + b_c, 0, 1000)                            // b_c ∈ [−500,0], non-positive
C(s) = clamp(min(P(s), C_n(s)), 0, 1000)
```

**Training/update:** predictor trained with G-penalized loss (updates reversed
if they increase the minimum); censor trained with an adversarial objective —
reinforced on every item where the predictor assigned conf > accuracy at any
depth; censor updates always accepted, never reversed.

**Q2 falsifiable prediction:** beats NEC on admit@16, revoke@16 (censor's
monotone depth penalty prevents overconfidence NEC's once-set ceiling
permits), cost@32/64 (censor is a structural backstop against predictor
fooledness). Loses to NEC on redteam@1 (depth penalty + negative bias
over-suppresses easy single-depth items → B5 damage) and logic@8 (censor's
survivor-fraction cap too aggressive when 8–10/64 survive). B2 (theater) is
*structurally* guaranteed: min(P, monotone-C_n) can never increase with depth
for censor-bound items — stronger than NEC's guarantee.

**Q3 failure mode:** (5) mask-invisible depth schedule — most likely death. The
censor's depth penalty is a *global* schedule, blind to per-family difficulty:
on families where high confidence at high depth is correct (ceiling P), it
suppresses unnecessarily → B4/B5 damage. Structural property: min(P, C_n) is an
*asymmetric* guarantee — the censor can only suppress, never boost, so it
cannot create new overconfidence. But it cannot prevent systematic
*underconfidence* either; the asymmetry is the guarantee and the cost.

**Q4 rank: #2, P(clear strict B3) ≈ 0.50.** Monotone censor depresses high-depth
confidence, counteracting selection. But censor only helps where it binds; for
predictor-bound items at low depth there's no monotonicity constraint. Blanket
depression can also *create* apparent G-rises (G deeply negative at low depth
→ zero at high depth = a rise).

---

## Mechanism D — Depth-Discounted Calibration Ledger (DDCL)

**Head form:**
```
B(s) = clamp((Σ w_i·f_i)/1000 + b, 0, 1000)            // base score
Ledger: L[0..64] per-depth (sum_conf, sum_correct, count), FIFO bounded at
        LEDGER_CAPACITY = 2048 total entries
G_empirical(d) = (L[d].sum_conf / max(count,1)) − (L[d].sum_correct*1000 / max(count,1))
offset(d) = clamp(G_empirical(d) * damp, −200, 200)    // damp ∈ [200,800]
C(s) = clamp(B(s) − offset(d), 0, 1000)
```
Forgetting is FIFO (monotone in recency). All integer ops. Ledger is purely
online; only base-head weights and damp are learned. Meta-update: if
G_empirical oscillates, damp −50 (min 200); stable for 100 updates → damp +50
(max 800).

**Q2 falsifiable prediction:** beats NEC on *all families at depths 16–64*
(empirical correction is the only one that directly measures G(d)), on
O@32/64 (ceiling/O pooling corrected empirically), and is the strongest B13
candidate (per-depth offset drives G(d) ≈ 0 where ledger is full). Loses to NEC
on redteam@1–2 (1–3 items → noisy ledger → oscillating offsets) and logic@1
(unnecessary offset on easy depth-1 items → B5 depression); B7 risk of
over-abstention at large-G depths like O@64.

**Q3 failure mode:** (1) clamp attractor (conf≡0) — most likely death. Feedback
loop: high offset → low confidence → low mean_conf → high G_empirical → higher
offset. Structural prevention: hard architectural bound — offset ∈ [−200, 200]
and damp ≤ 800 cap the maximum depression at 200 thousandths (20% of range),
so total collapse is impossible by construction (though large-G correction is
correspondingly limited). Feedback instability additionally damped by the
low-pass damp meta-rule.

**Q4 rank: #1, P(clear strict B3) ≈ 0.65.** Only mechanism that directly
measures and corrects G(d). Fundamental weakness: strict B3 has no n-filter, so
noisy single-item legs (redteam@32) create apparent G-rises the ledger cannot
fix.

---

## Q5 — B3 satisfiability under M4 (mechanism-theoretic answer)

**Strict B3 is not practically satisfiable — but not for the reason the
selection-effect folk argument suggests.** An omniscient head *can* trivially
satisfy B3 by setting conf = accuracy per item (G(d) ≡ 0). The real result:

1. The released population A(d+1) ⊆ A(d) is a *function of the head's own
   output* at all prior depths (through M4's abstention rule). This creates a
   circularity: the head determines what gets released → that determines
   population statistics → that determines G(d).
2. No head of the form C(s) = f(index-level features) can *guarantee* strict
   B3 across all families/depths, because guaranteeing it would require solving
   a fixed-point equation (conf = accuracy over a population that depends on
   conf) with bounded integer-math features — that fixed point may not exist or
   be reachable via training.
3. The selection effect proper: even when every item's confidence is
   nonincreasing, family G can rise because the removed items had
   below-average confidence — low confidence correlates with leader
   instability → M4 abstention → mean_conf(d+1) > mean_conf(d) while accuracy
   need not keep up. **This is a mathematical consequence of M4's selection
   rule on a non-uniform population, not a failure of any confidence head.**

**Minimal sufficient relaxation:** per-item B3 — for each item i released at
both d and d+1, require `conf_i(d+1) − acc_i(d+1) ≤ conf_i(d) − acc_i(d) + δ`
(δ ≈ 1e-3). This eliminates the population-level selection effect entirely,
is trivially satisfiable by an omniscient head, is achievable by a
bounded-complexity head (NEC's per-item ceiling already maintains per-item
tracking), and preserves the calibration intent. Equivalent cohort framing:
fix the cohort released at all depths and require G nonincreasing within it.

**Practical implication for the fork round:** current strict B3 (no
n-filter) should be interpreted with the B13 `n_rel ≥ 8` filter applied, and
the competition should minimize violations on that relaxed standard. The
per-item B3 reformulation is the cleanest provably-satisfiable version.

---

## Fable's P(clear strict B3) ranking (summary)

| Rank | Mechanism | P(B3) | Core reason |
|------|-----------|-------|-------------|
| 1 | D — Depth-Discounted Calibration Ledger | ~0.65 | Only one that directly measures/corrects G(d) empirically; hard-capped offset blocks clamp death |
| 2 | C — Two-Head Adversarial Cap | ~0.50 | Structural monotone censor via min(); asymmetric guarantee (suppresses only); fails where censor doesn't bind or over-suppresses |
| 3 | B — Disagreement-Geometry Head | ~0.35 | Genuinely new structural signal; learned, not architectural — dies to adversarial convergence |
| 4 | A — Differential Evidence Budget | ~0.25 | NEC-like individual-item tracking; structurally blind to population-level selection effects |

**Head-form verdict from Q5:** no head — not even an omniscient one — can
*guarantee* strict B3 on the released population under M4, because the released
population is a function of the head's own output (fixed-point circularity).
The satisfiable target is per-item B3 (conf_i(d+1) − acc_i(d+1) ≤
conf_i(d) − acc_i(d)), not family-mean G nonincrease.
