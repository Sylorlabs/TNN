# H5 Fork-Architecture: Deep Batched Round

## Q1: Four Genuinely New Mechanisms for Non-Overconfident Depth

---

### Mechanism A: Differential Evidence Budget (DEB)

**Core idea:** Each depth level costs "evidence currency." The confidence head maintains a virtual budget that must be *spent* by margin quality and *charged* by depth progression. If the budget is depleted, confidence is capped regardless of margin.

**Head form:**

```
budget_0 = 1000

For each depth t ≥ 1:
  budget_t = clamp(
    budget_{t-1}
    + margin_t * α_div   // margin purchases budget (α_div = 1000/nh, integer division)
    − depth_charge(t)    // depth consumes budget
  , 0, 1000)

depth_charge(t) = (t * 1000 / max_depth)   // linear ramp scaled to thousandths

C(s) = clamp(min(budget_t, margin_score(s)), 0, 1000)

margin_score(s) = clamp(margin_t * 1000 / nh, 0, 1000)   // scaled margin
```

Where `nh = 64` (or the actual hypothesis pool size known at compile time), and `α_div = 1000 / nh`.

**Key properties:**
- `budget_t` is *not* required to be nonincreasing; it can be replenished if margin is strong enough. But the depth_charge is monotonically increasing in `t`, creating a structural downward ratchet.
- The budget tracks a per-item "state" across depths. Since the system processes items through the depth schedule sequentially, budget_t can be maintained as a side-channel state variable per item.
- Integer math: all divisions are i64 safe since operands are bounded to 0–1000 and 1–64.

**Training/update:** Budget parameters (`α_div` numerator, depth_charge scaling factor) are learned via online gradient estimation on a per-batch basis, but the update is *clamped to never increase depth_charge coefficients* — a monotonicity constraint enforced structurally by only allowing parameter decrements during training epochs where G(d) shows a positive slope for any family.

---

### Mechanism B: Disagreement-Geometry Head (DG Head)

**Core idea:** Instead of a weighted sum of scalar features, compute confidence from the *geometric structure* of how surviving hypotheses disagree. The key insight: if surviving hypotheses are tightly clustered in their output space, high confidence is warranted; if they are scattered, confidence should be suppressed regardless of margin.

**Head form:**

```
// Pairwise disagreement among surviving hypotheses
// Let h_i, h_j be surviving hypothesis outputs (binary: 0 or 1)
// Disagreement index:

D_t = Σ_{i<j, both alive} |h_i − h_j| * 1000 / (nalive * (nalive−1) / 2)
// This is the fraction of surviving pairs that disagree, scaled to thousandths
// If nalive ≤ 1: D_t = 0 (no disagreement possible = high structural confidence)

// Surviving margin variance proxy:
// Instead of margin = |#yes − #no|, compute the "spread"
S_t = clamp(1000 − D_t, 0, 1000)   // agreement fraction

// Disagreement velocity: is the surviving group converging?
ΔD_t = clamp(D_t − D_{t−1}, −1000, 1000)   // negative = group converging (good)

C(s) = clamp(
    (S_t * w_s + margin_t * w_m + (1000 − clamp(ΔD_t, 0, 1000)) * w_v) / 1000
    + depth_suppress(t) * w_d / 1000
  , 0, 1000)

depth_suppress(t) = clamp(1000 − (t * 1000 / 64), 0, 1000)

// Weight structure (learned but constrained):
// w_s, w_m, w_v, w_d are integers in [0, 1000], sum ≤ 1000
```

**Key properties:**
- The disagreement index `D_t` is *not* available to flat-sum heads because it requires pairwise structure. It directly measures the *reasonableness* of high confidence: if 40% of survivors disagree, no margin should yield high confidence.
- The disagreement velocity `ΔD_t` captures whether depth is *resolving* conflict. If the group is converging, confidence can rise; if it's diverging, confidence must fall.
- The sole-survivor case (`nalive ≤ 1`) gives `D_t = 0`, meaning structural agreement, which is correct — a single survivor has no internal disagreement.
- All computations are integer-safe: counts, products of small integers, division by at most `64*63/2 = 2016`.

**Training/update:** Weights `w_s, w_m, w_v, w_d` are updated via a batch-level signal where the loss penalizes G-rise: if `G(d+1) > G(d)`, all weight updates in that batch are reversed for the offending direction. This is a *ratchet*: weights only move in directions that reduce G-rise.

---

### Mechanism C: Two-Head Adversarial Cap (THAC)

**Core idea:** Two independent heads compute confidence. The *predictor* head is optimistic; the *censor* head is pessimistic. The final confidence is `min(predictor, censor)`. The censor's *sole training objective* is to identify cases where the predictor is overconfident. This creates a structural guarantee: confidence can only be as high as the more conservative head allows.

**Head form:**

```
// Predictor head (familiar form):
P(s) = clamp((Σ w_i·f_i^P) / 1000 + b_P, 0, 1000)
// 8 features as described, different weights from censor

// Censor head (specialized):
C_n(s) = clamp(
    min(
      margin_t,                           // censor never exceeds margin
      1000 − (t * 1000 / 64),            // depth penalty
      1000 if nalive ≤ 2 else
        clamp(nalive * 1000 / nh, 0, 1000)  // survival fraction as cap
    )
  , 0, 1000)

// Censor has its own learned scalar modifier:
C_n(s) = clamp(C_n(s) + b_c, 0, 1000)
// where b_c ∈ [−500, 0] is a learned negative bias (censor is structurally pessimistic)

// Final:
C(s) = clamp(min(P(s), C_n(s)), 0, 1000)
```

**Key properties:**
- The `min` operation is the structural safeguard. Even if the predictor learns to be overconfident at depth, the censor's depth penalty `1000 − (t * 1000 / 64)` enforces that confidence is at most linearly decreasing in `t`. This is *architectural*, not learned.
- The censor's bias `b_c` is constrained to be non-positive, so it can only suppress, never boost.
- The margin cap in the censor ensures B2 (no wrong→wrong with rising confidence) is structurally enforced: if the wrong answer persists, margin stays small or negative, and the censor blocks any confidence increase.
- The `min` of two heads is an i64-safe operation.

**Training/update:** Predictor is trained normally with G-penalized loss. Censor is trained with an *adversarial objective*: for each item where the predictor assigned conf > accuracy at any depth, the censor is reinforced. The censor's weight updates are *always accepted* (never reversed), while predictor updates are reversed if they increase the minimum.

---

### Mechanism D: Depth-Discounted Calibration Ledger (DDCL)

**Core idea:** Maintain a fixed-size online ledger of recent (depth, outcome, confidence) triples, binned by depth. For each depth level, compute an empirical *calibration offset* from the ledger. Confidence is the base score minus this offset, where the offset is the empirical G(d) from recent history. The ledger forgets old entries with a *monotone* forgetting rule: older entries always contribute less than newer entries.

**Head form:**

```
// Base score (same structure as current head):
B(s) = clamp((Σ w_i·f_i) / 1000 + b, 0, 1000)

// Ledger: array L[0..64] of (sum_conf, sum_correct, count) per depth
// All values are i64, bounded by ledger capacity
LEDGER_CAPACITY = 2048  // max entries total across all depths

// For each new (depth=d, conf=c, correct=acc) triple:
//   L[d].count += 1
//   L[d].sum_conf += c
//   L[d].sum_correct += c * acc   // acc is 0 or 1, c is in thousandths
//   If Σ L[d].count > LEDGER_CAPACITY:
//     Remove oldest entry (FIFO within each depth bin)
//     This is the forgetting rule: oldest-first is monotone in recency

// Calibration offset for depth d:
G_empirical(d) = (L[d].sum_conf / max(L[d].count, 1))
                 − (L[d].sum_correct * 1000 / max(L[d].count, 1))
// This is mean_conf − accuracy at depth d, in thousandths

// Offset with dampening (avoid overcorrection):
offset(d) = clamp(G_empirical(d) * damp, −200, 200)
// damp ∈ [200, 800] learned, prevents oscillation

// Final confidence:
C(s) = clamp(B(s) − offset(d), 0, 1000)
```

**Key properties:**
- The ledger is *online* and *bounded*. The FIFO forgetting rule is trivially monotone: as entries age, they fall off, so only recent calibration history matters.
- The dampening factor `damp` prevents the offset from overshooting. If `damp = 500`, the correction is 50% of the empirical G, which is conservative but safe.
- The offset is *subtractive*: it directly corrects for the empirical over/under-confidence at each depth. If G(d) = +50 (overconfident), the offset pulls confidence down by 25 at damp=500.
- The structural guarantee: as long as the ledger contains enough entries at each depth, the offset converges to the true G(d), and `C(s) − offset(d)` should have near-zero G(d). The ledger's bounded size ensures this is computable in constant time.
- All integer arithmetic: sums, counts, divisions.

**Training/update:** Only the base head weights `w_i, b` and the dampening factor `damp` are learned. The ledger itself is purely online (no training). The dampening factor is updated via a meta-signal: if the ledger's G_empirical oscillates (changes sign between updates), damp is decreased by 50 (minimum 200). If G_empirical is stable for 100 updates at a given depth, damp is increased by 50 (maximum 800).

---

## Q2: Falsifiable Predictions per Mechanism

### Mechanism A (DEB)
- **Beats NEC:** Budget depletion creates a hard ceiling that is *stateful* per item. Unlike NEC's per-item ceiling (which is a post-hoc clamp), the budget integrates margin quality over depth. This should help on **logic@8 and logic@16** where items survive many depths with adequate margin — DEB will allow confidence to persist (margin replenishes budget) while NEC's ceiling is fixed from the start.
- **Beats NEC on:** **admit@16, admit@32** — items that maintain strong margin across many depths get budget replenishment, so confidence stays informative rather than collapsing to ceiling-estimated values.
- **Loses to NEC on:** **redteam@1–4** — tiny-n environments where the budget mechanism's margin_signal is noisy (few hypotheses → coarse margin → erratic budget updates). Also **trap@8, trap@16** — adversarial items designed to look like strong margin is sustained; DEB's budget replenishment will be fooled.
- **B5 separation:** May underperform NEC on **cost@8** because budget depletion for wrong answers is slow (wrong items can maintain moderate margins in cost families), reducing separation.

### Mechanism B (DG Head)
- **Beats NEC on:** **redteam@16, redteam@32** — disagreement geometry is robust to tiny-n at earlier depths because it captures *structural* information about hypothesis clustering. A single survivor (nalive=1) gets D_t=0 automatically, which is correct. The key advantage: on redteam items where margin is misleading (adversarially crafted), the disagreement index provides an independent signal.
- **Beats NEC on:** **logic@16, logic@32** — complex logic items where the surviving hypothesis set has rich disagreement structure that correlates with correctness better than margin alone.
- **Loses to NEC on:** **admit@4, admit@8** — simple items where the disagreement index is either 0 or 1000 (all agree or all disagree), providing no nuance beyond what margin already captures. DG Head adds overhead without benefit.
- **B3 (G-flatness):** Should clear B3 better than NEC on **ceiling families (P, O, D)** because disagreement geometry captures the *interaction effects* that create G-rises. The ceiling effect on O family creates situations where high-confidence items survive while low-confidence ones abstain; DG Head's disagreement index would flag this directly.
- **B5 separation:** Should excel on **P@32, P@64** where deep items with persistent disagreement among many survivors clearly signal wrong answers.

### Mechanism C (THAC)
- **Beats NEC on:** **admit@16, revoke@16** — the censor's structural depth penalty provides a clean, monotone decrease that prevents the overconfidence that NEC's ceiling sometimes permits (NEC sets ceiling once and doesn't adjust).
- **Beats NEC on:** **cost@32, cost@64** — the censor's min(margin, depth_penalty) caps ensure that even if the predictor is fooled by cost family complexity, the censor provides a structural backstop.
- **Loses to NEC on:** **redteam@1** — the censor's depth penalty is too aggressive for single-depth evaluation; at depth 1, the censor allows conf ≤ 1000 − (1*1000/64) = 984, which is fine, but the censor's bias `b_c` may suppress confidence below useful levels on easy single-depth items, hurting B5.
- **Loses to NEC on:** **logic@8** where the predictor should assign high confidence but the censor's nalive cap (`nalive * 1000 / nh`) may be too aggressive when only 8–10 of 64 hypotheses survive.
- **B2 (theater):** THAC is structurally guaranteed to clear B2 because the censor's depth penalty is monotonically decreasing in `t` — even if the predictor's output is non-decreasing, `min(P, C_n)` can never increase with depth. This is a stronger guarantee than NEC.
- **B3:** Should clear B3 on most batteries because the censor provides a systematic depression of confidence at higher depths, counteracting the selection effect. However, may still fail B3 on **ceiling O** because O's ceiling creates items where correct and wrong items have similar depth-survival patterns.

### Mechanism D (DDCL)
- **Beats NEC on:** **ALL families at depths 16–64** — the calibration ledger directly measures and corrects for the empirical G(d) at each depth. Since the selection effect is an empirical phenomenon, an empirical correction should handle it. This is the mechanism most likely to clear B3.
- **Beats NEC on:** **O@32, O@64** — the ceiling/O pooling problem is addressed empirically: the ledger will learn that at depth 32 on O-family, the empirical G is large, and apply a correspondingly large offset.
- **Loses to NEC on:** **redteam@1–2** — with only 1–3 items per family at these depths, the ledger's empirical estimates are too noisy to be useful. The offset may oscillate wildly.
- **Loses to NEC on:** **Logic@1** — the ledger at depth 1 is the most stable, but the offset may be non-zero even at depth 1 (because the base head is imperfect), causing unnecessary confidence depression on easy items, hurting B5.
- **B13 (G ≥ −0.100 per family-depth with n≥8):** DDCL is the strongest candidate for B13 because it directly targets per-depth calibration. The offset mechanism ensures that G(d) ≈ 0 at depths with enough ledger entries.
- **B7 (abstention ≤ 0.30):** Risk of over-abstention if the ledger offset is too large. The dampening factor mitigates this, but at depths where G_empirical is large (e.g., O@64), the offset could push many items into the abstention zone.

---

## Q3: Failure Mode Analysis per Mechanism

### Mechanism A (DEB)
- **Most likely death:** **(6) M4 Selection Effects** — the budget mechanism doesn't directly address the fact that the *released population changes with depth*. An item that would be overconfident at depth 4 might have its budget depleted appropriately, but the *mean accuracy of released items at depth 8* could be higher because low-confidence items from depth 4 were absorbed into abstentions. This raises G(8) even though every individual item's confidence is nonincreasing.
- **Structural prevention property:** The budget's replenishment via margin creates a *stateful* tracking that implicitly encodes some selection information: items that survive multiple depths have been repeatedly margin-tested. However, this is insufficient because budget tracks *individual* items, not the *population* effect. The budget mechanism structurally prevents B1 (no 1→0 transitions, since budget depletes gradually) and B2 (budget can only be replenished by margin, which correlates with correctness), but cannot structurally prevent the population-level selection effect.
- **Secondary risk:** **(3) uniform-manifold escape** — if budget parameters converge to a regime where `depth_charge` dominates and budget always depletes by depth 4, then all items above depth 4 get conf=0, creating a clamp attractor on the high-depth side. Structural prevention: the budget is replenished by margin, so items with strong margin at depth 4+ can still have non-zero budget.

### Mechanism B (DG Head)
- **Most likely death:** **(4) spread anti-learning** — increasing the weight on disagreement features could raise G if the disagreement index correlates with accuracy in the wrong direction at certain depths. Specifically, at high depths where only adversarial items survive, the surviving set may have *low* disagreement (they all converge on the wrong answer), which would give D_t ≈ 0 → S_t ≈ 1000 → high confidence. This is exactly the wrong signal for wrong items that have survived by mimicking the correct answer.
- **Structural prevention property:** The disagreement velocity feature `ΔD_t` provides a *temporal* signal: if the group converges suddenly at high depth, this looks suspicious (the velocity is large and negative), which the head can learn to suppress. The structural property is that convergence-at-depth is *detectable* as an anomaly in the velocity signal, because normal convergence should happen gradually. However, this is a *learned* prevention, not an architectural one — if the training data doesn't contain enough examples of adversarial convergence, the head won't learn to suppress it.
- **Secondary risk:** **(7) tiny-n noise** — at redteam@1, nalive=1, so D_t=0 always, providing no information. The head effectively becomes a margin-only head for tiny-n, losing its primary advantage. Structural prevention: the head falls back to the margin and depth features, which is correct behavior (there's no disagreement to measure with one survivor), but this means it has no advantage over simpler heads on tiny-n.

### Mechanism C (THAC)
- **Most likely death:** **(5) mask-invisible depth schedule** — the censor's depth penalty `1000 − (t * 1000 / 64)` is a *global* depth schedule, not adapted per family. For families where high confidence at high depth is *correct* (e.g., ceiling P family where deep analysis is reliable), the censor suppresses confidence unnecessarily, hurting B4 (meanConfCorrect ≥ 0.50) and B5 (separation). The depth penalty is "invisible" to the actual difficulty structure of different families.
- **Structural prevention property:** The `min(P, C_n)` operation ensures the censor can only *suppress*, never *boost*. This means overconfidence is structurally prevented, but *underconfidence* is not. The structural property is the asymmetric guarantee: the censor cannot create new overconfidence, it can only destroy it. The risk is that this asymmetry causes systematic underconfidence.
- **Secondary risk:** **(2) crutch collapse** — the censor head's simple structure (min of margin and depth penalty) may become a "crutch" that the system relies on, causing the predictor head to receive weak training signal (because the censor is always the binding constraint). Over time, the predictor may converge to a trivial function, and the system becomes equivalent to a depth-only schedule.

### Mechanism D (DDCL)
- **Most likely death:** **(1) clamp attractors (conf≡0)** — if the ledger's calibration offset grows too large (because empirical G(d) is persistently high), the offset dominates the base score, and `C(s) = clamp(B(s) − offset(d), 0, 1000)` collapses to 0 for all items above a certain depth. This is a clamp attractor driven by the ledger's own momentum: high offset → low confidence → low mean_conf in ledger → high G_empirical → higher offset.
- **Structural prevention property:** The dampening factor `damp ∈ [200, 800]` and the offset clamp `offset(d) ∈ [−200, 200]` provide a hard architectural bound on how much the offset can depress confidence. With `damp ≤ 800` and offset clamped to `[−200, 200]`, the maximum depression is 200 thousandths (20% of the confidence range). This means even with a terrible ledger, the base score is only reduced by 20%, preventing total collapse. However, this also limits the mechanism's ability to correct for large G(d) values.
- **Secondary risk:** **(6) M4 Selection Effects** — the ledger measures G(d) from the released population, which is itself affected by the confidence head's output. This creates a feedback loop: the head's confidence determines what gets released, which determines the ledger's empirical G, which determines the offset, which determines the head's confidence. If this feedback loop is unstable, the ledger may oscillate. Structural prevention: the dampening factor acts as a low-pass filter on the feedback, and the bounded ledger size prevents the loop from accumulating unbounded memory.

---

## Q4: Ranking by P(clears strict B3)

### Rank 1: Mechanism D (DDCL) — P(B3) ≈ 0.65
**Reasoning:** B3 requires zero G-rises per family across all depths. DDCL is the *only* mechanism that directly measures and corrects for G(d) empirically. The calibration offset is specifically designed to flatten G(d). The dampening and clamping prevent overcorrection. The main risk is the feedback loop (mechanism death mode 1), but the architectural bounds (offset ∈ [−200, 200]) prevent catastrophic failure. The mechanism is most likely to fail B3 on families where the ledger's sample size is too small to estimate G(d) accurately — but strict B3 has no n-filter, so even single-item legs contribute. This is the fundamental weakness: the ledger at depths with few released items (e.g., redteam@32) will have noisy G estimates, potentially creating apparent G-rises due to noise.

### Rank 2: Mechanism C (THAC) — P(B3) ≈ 0.50
**Reasoning:** The censor's structural depth penalty provides a *monotone* decrease that should prevent most G-rises. The `min(P, C_n)` operation means that even if the predictor increases confidence with depth, the censor's monotone decrease forces the final output to be non-increasing for items where the censor is binding. However, for items where the predictor is binding (i.e., P < C_n), the predictor's output determines confidence, and the predictor has no structural monotonicity constraint. The censor only helps when it's the binding constraint, which is most of the time for items at high depth (because the depth penalty becomes aggressive), but not for items at low depth. The ranking risk: on families where accuracy increases with depth (logical possibility under M4's selection), G(d) should naturally decrease, but the censor's blanket depression might push G(d) negative at low depths and zero at high depths, creating an apparent G-rise from deeply negative to zero.

### Rank 3: Mechanism B (DG Head) — P(B3) ≈ 0.35
**Reasoning:** Disagreement geometry provides a genuinely new signal that captures population-level structure, which is what G(d) measures. However, the mechanism is *learned*, not *architectural*: whether it captures the right disagreement patterns depends on training data and optimization. The risk is that the disagreement features at high depth are dominated by adversarial survival effects (wrong items that have converged to look correct), which would give misleadingly low disagreement and high confidence for wrong items, *raising* G(d). The mechanism is most likely to clear B3 on families where disagreement is a reliable signal of correctness (P, D families at moderate depth) but fail on families where survival is adversarial (redteam, trap).

### Rank 4: Mechanism A (DEB) — P(B3) ≈ 0.25
**Reasoning:** The budget mechanism is the most "NEC-like" of the four, and NEC itself fails B3 with 6 violations. The budget adds stateful tracking, but the fundamental problem is the same: the budget tracks *individual* items, not the *population* effect. A budget that depletes appropriately for each item doesn't prevent the selection effect from creating G-rises in the released population. The budget mechanism is most likely to clear B3 on families where the selection effect is weakest (i.e., where abstention rates are similar across depths) and fail where abstention rates change dramatically with depth (ceiling families).

---

## Q5: Is Strict B3 Satisfiable Under M4?

### The Selection-Effect Argument (Formal)

**Claim:** Strict B3 (zero G-rises per family with no n-filter) is **not universally satisfiable** under M4, even by an omniscient confidence head, due to the selection effect created by M4's abstention rule.

**Proof sketch:**

Consider a family F and two consecutive depths d and d+1. Define:
- A(d) = set of items released at depth d
- A(d+1) ⊆ A(d) (M4 only releases items whose leader hasn't changed)
- G(d) = mean_conf(A(d)) − accuracy(A(d))
- G(d+1) = mean_conf(A(d+1)) − accuracy(A(d+1))

The selection effect operates as follows: M4's abstention rule ("leader-changed → abstain") means that items with *unstable* leaders (which tend to be items where the initial evidence was misleading) are preferentially removed from the released set at higher depths. This means A(d+1) is a *selected* subset of A(d) where the selection criterion is correlated with correctness.

Now consider two scenarios:

**Scenario 1 (Easy family, low selection):** If the family has very low abstention rates at all depths (e.g., logic with very easy items), then A(d+1) ≈ A(d), the selection effect is negligible, and an omniscient head could set conf = accuracy for all items, making G(d) ≈ 0 for all d. Strict B3 is satisfiable in this regime.

**Scenario 2 (Hard family with strong selection):** Consider a family where at depth d, 50% of items are correct and the head assigns conf = accuracy = 0.5 for all items, so G(d) = 0. At depth d+1, the selection effect removes half of the wrong items (their leaders changed), so the released set at d+1 is 50% correct items (all still released) + 25% wrong items (the other 25% were removed). Now the released population at d+1 is 67% correct. The omniscient head assigns conf = accuracy = 0.67 for correct items and conf = accuracy = 0.33 for wrong items. Mean_conf = 0.67 × 0.67 + 0.33 × 0.33 = 0.556, accuracy = 0.67. G(d+1) = 0.556 − 0.67 = −0.114.

This is a G-*decrease* (from 0 to −0.114), which satisfies B3. But now consider a more adversarial scenario:

**Scenario 3 (Ceiling O family):** At depth d, the released set has 60% accuracy. The omniscient head sets conf = 0.60 for all, G(d) = 0. At depth d+1, selection removes only *correct* items whose leaders changed (perhaps the correct answer had a complex leader-history), leaving 40% accuracy in the released set. The omniscient head sets conf = 0.40 for all, mean_conf = 0.40, G(d+1) = 0. Still no G-rise. But what if the selection is *non-monotone* in accuracy? If at d+2, the released set is again 60% accuracy (because some wrong items that were previously retained now have their leaders stabilized), then G(d+2) = 0 again. This is flat, still satisfying B3.

**The critical issue is NOT the omniscient head's ability to set conf = accuracy.** An omniscient head *can* always set conf = accuracy for each item, making G(d) = 0 for all d (since G(d) = mean_conf − accuracy = mean_accuracy − accuracy = 0 when conf = accuracy for every item). **An omniscient head trivially satisfies strict B3.**

**But the omniscient head is not the question.** The question is whether a *finite, integer-math head* with bounded feature inputs can achieve this. The omniscient head would need to know each item's true accuracy at each depth, which requires omniscience. The features available to the head are index-level statistics (margin, depth, evidence fraction, etc.), not item-level truth.

### The Real Impossibility Result

**Theorem (informal):** No head of the form C(s) = f(features) where features are functions of index-level statistics (margin, depth, evidence fraction, survivor count, etc.) can guarantee strict B3 across all families and depths under M4, because:

1. **The released population at depth d+1 is a *function of the confidence head's output at all prior depths*** (through M4's abstention rule). This creates a circularity: the head determines what gets released, which determines the population statistics, which the head uses to compute confidence.

2. **This circularity means the head cannot compute conf = accuracy without solving a fixed-point equation** that depends on the head's own output across all items and depths.

3. **For a fixed head (no learning), this fixed point may not exist or may not be unique.** For a learning head, the training objective is to find a fixed point where G(d) = 0 for all d, but the nonlinearity of M4's selection rule means this fixed point may not be reachable via gradient-based optimization from any starting point.

**However,** this impossibility is *practical*, not *logical*. An omniscient head satisfies B3. The impossibility is that no *bounded-complexity* head can guarantee it.

### The Selection Effect Specifically

The selection effect is: **G(d+1) > G(d) can occur even when every individual item's confidence is nonincreasing across depths**, because the *population* changes. Specifically:

Let item i have conf_i(d) and acc_i(d) at depth d. Then:
- G(d) = (1/|A(d)|) Σ_{i∈A(d)} conf_i(d) − (1/|A(d)|) Σ_{i∈A(d)} acc_i(d)
- G(d+1) = (1/|A(d+1)|) Σ_{i∈A(d+1)} conf_i(d+1) − (1/|A(d+1)|) Σ_{i∈A(d+1)} acc_i(d+1)

Even if conf_i(d+1) ≤ conf_i(d) for all i, the *mean* over A(d+1) can be higher than the mean over A(d) if the items removed from A(d) had *below-average* confidence. This happens when:
- Items with low confidence are preferentially removed (because low confidence correlates with leader instability → M4 abstention)
- The remaining items have above-average confidence

This raises mean_conf(d+1) > mean_conf(d). If accuracy doesn't increase as much (or decreases), G(d+1) > G(d).

**This is not a failure of the confidence head — it's a mathematical consequence of the M4 selection rule operating on a non-uniform population.**

### Minimal Sufficient Relaxation

The minimal relaxation that makes B3 satisfiable:

**Option 1 (n-filter, current B13):** B3 with `n_rel ≥ k` where k ≥ 8. This excludes legs where the released population is too small for the selection effect to be meaningful. At n_rel ≥ 8, the selection effect is bounded: the maximum possible G-rise due to selection alone (with conf nonincreasing per item) is bounded by `(n_removed_wrong / n_rel) * max_conf_difference`, which decreases as n_rel increases. For k = 8, this bound is approximately 1000 * (n_removed / 8), which can be as large as 125 if one item is removed. This is still too large for strict B3.

**Option 2 (abstention-rate constancy):** B3 on released cells only when the abstention rate is held approximately constant across depths: `|A(d+1)| / |A(d)| ≥ 1 − ε` for some ε < 0.1. This ensures the population doesn't change much, bounding the selection effect. This is *sufficient* because if the population is nearly constant, the selection effect is negligible, and a well-calibrated head can achieve G(d) ≈ constant.

**Option 3 (per-item B3):** Instead of G(d) = mean_conf − accuracy over the released population, define per-item G_i(d) = conf_i(d) − acc_i(d), and require G_i(d+1) ≤ G_i(d) for all items i that are released at both d and d+1. This eliminates the population-level selection effect entirely because it compares each item to *itself* across depths. **This is the minimal and sufficient relaxation**: it preserves the spirit of B3 (confidence should not become less calibrated with depth) while removing the population-level selection effect.

**Option 4 (constant-cohort B3):** Fix a cohort of items that are released at all depths d through d_max, and require G(d) to be nonincreasing within this fixed cohort. This is equivalent to Option 3 but framed as a cohort analysis rather than per-item analysis.

### Recommendation

The **minimal sufficient relaxation** is **per-item B3**: for each item i that is released at both depth d and depth d+1, require `conf_i(d+1) − acc_i(d+1) ≤ conf_i(d) − acc_i(d) + δ` for tolerance δ ≈ 1e-3 (one thousandth). This:
- Eliminates the selection effect entirely
- Is trivially satisfiable by an omniscient head (set conf = accuracy)
- Is achievable by a bounded-complexity head (e.g., NEC's per-item ceiling)
- Preserves the spirit of the calibration requirement
- Can be computed from the same per-item tracking that NEC already maintains

For the *current* strict B3 (no relaxation), the answer is: **no head — including an omniscient one — can guarantee strict B3 if we require it over the released population under M4, because the released population is itself a function of the head's output, creating a circularity that may not admit a fixed point where G(d) = 0 for all d simultaneously.** An omniscient head *can* achieve G(d) = 0 by setting conf = accuracy, but this requires the head to *know* accuracy, which is circular (accuracy is defined over the released population, which depends on the head).

**Practical implication for the fork competition:** The current B3 standard should be interpreted as B3-with-n-filter (which is already B13's `n_rel ≥ 8`), and the goal should be to minimize the number of violations while maximizing performance on the *relaxed* B3. The per-item B3 relaxation (Option 3) is the cleanest reformulation that preserves the evaluation's intent while being provably satisfiable.
