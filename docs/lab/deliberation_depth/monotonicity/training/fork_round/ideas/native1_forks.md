# H5 Fork Ideas — Native Brainstorm 1 (muse subagent, no external models)

Date: 2026-09-24. First-principles fork designs for the overconfidence-with-depth round.

## Fixed context (not negotiable)
- Release rule FIXED: M4 skeleton (release L_t iff L_t == L_1, else abstain). Forks may not touch it.
- Head battleground only: C(s) = clamp((Σ w_i·f_i)/1000 + b, 0, 1000), thousandths, pure Zag integer math, zero RNG, byte-identical reruns.
- Base features: f1=clamp(margin_t,0,1000); f2=t·1000/64; f3=leader-changed×1000; f4=margin velocity; f5=evidence fraction×1000; f6=survivor fraction×1000; f7=sole-survivor pin×1000; f8=flip trauma. No family labels, no text inputs.
- Bar interpretations used below (flag if the frozen prereg defines differently): B1 "1→0=0" = zero cells going conf≡1000 at rung d to conf≡0 at a deeper rung (clamp slam). B2 theater: V1 = conf strictly rising across depths on same item while correct→wrong; V2 = same while wrong→wrong. B3 strict: zero rungs with G(d+1)>G(d) per family, G(d)=mean_conf−accuracy over released cells, tol 1e-12. B13: per (family,depth) with n_rel≥8, G ≥ −0.100 (underconfidence floor — this already anti-games B3: you cannot fake nonincreasing G by diving negative, the floor caps gaming room at 0.100).
- Best so far: per-item confidence ceiling → only zero-theater arm, killed by strict B3 via failure mode 6 (selection) and B13 via 6. **None of the forks below use a per-item monotonicity constraint — no ceiling iterations.**

---

## Fork 1 — "Unearned-Stability Discount" (USD head)

**Mechanism (head form change, integer-safe).**
New feature: `f9 = max(0, STAB − EV)`, where `STAB = (f6 + f7)/2` (survivor fraction + sole-survivor pin, thousandths) and `EV = f5` (evidence fraction ×1000). All integer ops.
Head: `C(s) = clamp((Σ_{i=1..8} w_i·f_i − w9·f9)/1000 + b, 0, 1000)`, with `w9 ≥ 0` enforced by projection in the fitter (if w9<0 → 0 after each update).

**Targets:** failure mode 6 (M4 selection effects), via 2 (crutch collapse).

**Mechanistic argument.** Mode 6's engine is not generic attrition — it is *selection concentrating trap survivors*. The items that survive to d=16/32/64 with high confidence and zero accuracy are traps: leaders that never flip (high f6, f7) on thin evidence (low f5) — confidence without basis. Their residuals are large-positive, and as depth attrites honest-but-contested items, traps dominate the released pool → G rises. The ceiling arm cannot touch this: per-item nonincreasing conf leaves trap conf HIGH (it was already high at depth 1). USD pins trap survivors' conf down at *every* rung through the stability−evidence gap — exactly the trap signature, and ≈0 for honest items (evidence tracks stability). So the selected population's conf ≈ its accuracy at every rung → G flat by construction of the population the metric scores, not by constraining item paths.

**Predicted bars.** B3 violations → 0 on trap/redteam/admit legs; B5 separation ↑ (traps pushed down, honest-correct untouched); B4/B4b hold (honest items have f9≈0, discount doesn't fire); B13 holds (G tracks accuracy, no underconfidence overshoot); B2 unchanged-or-better (trap conf starts low, can't theatrically rise).

**Falsification (kill if ANY holds).**
- (a) Any trap/redteam leg still shows a strict G(d+1)>G(d) with n_rel≥16 at both rungs → the trap-signature theory of mode 6 is wrong.
- (b) B4 < 0.50 on any honest leg → f9 fires on honest items (evidence accounting ≠ stability accounting) → the feature is a false positive generator.
- (c) w9 fits to 0 on a majority of legs → the feature is dead weight, not a mechanism.

**Adversarial note.** If the fitter sets w9>0 by merely re-weighting f6/f7 downward for everyone, B4b (honest-family ≥0.50) dies first — watch B4b, not just B4.

---

## Fork 2 — "Per-Depth G-Anchored Fitter" (GRAF)

**Mechanism (training rule change; head form UNCHANGED).**
The pooled fitter is blind to what B3 scores. Replace the objective with (all fixed-point integer):
`L = Σ_{d ∈ rungs} n_d · G(d)²  +  λ Σ_{cells} (c − y)²  +  μ Σ_{items} Σ_{d} max(0, c_{d+1} − c_d)`
where `G(d) = 1000·Σ_{rel@d}(c − y)/n_d` in i64 accumulators, y ∈ {0,1000} correctness, and the μ term is a *soft* per-item theater penalty (trainable, escapable — not a hard ceiling). Optimize by deterministic coordinate descent on the integer weight lattice (weights in thousandths, steps ±8, then ±1 refine). Pure integer, zero RNG, byte-identical.

**Targets:** failure mode 6 directly; B2 via the μ term; mode 7 handled by the n_d weighting (tiny-n rungs contribute little to L — their G² is downweighted by n_d, and falsification uses an n_rel≥16 gate).

**Mechanistic argument.** B3 scores per-depth MEANS over the released population at each depth. Selection can only raise G(d+1) above G(d) if the head is miscalibrated *on the survivor population* — a pooled fitter never prices that population. GRAF fits the head to be calibrated on exactly the population each rung is scored on: if E[c−y|d]≈0 ∀d, then G(d)≡0, strict B3 holds with equality (0>0 is false), B8 is flat, B13 is satisfied (0 ≥ −0.100) — immune to selection *by construction*, because the objective already contains the selected population. No per-item path constraint is needed; the μ term buys B2 without fiat. This is the complement of the ceiling arm: the ceiling constrained *items*; GRAF constrains *rung means*, which is what the bar actually measures.

**Predicted bars.** B3 → 0 violations on all legs with adequate n; B8 PASS; B13 PASS; B2 V1=V2=0 (μ term); B6 ≥ 0.95 (form unchanged, primary calibration preserved by the λ term); B4 ≥ 0.50 (G≈0 ⇒ conf tracks accuracy; accuracy on released cells is high).

**Falsification (kill if ANY holds).**
- (a) Any leg with n_rel ≥ 16 at *every* rung still shows a strict B3 violation → per-depth anchoring failed ⇒ the violation is driven by within-rung compositional shift the linear head cannot express (subpopulations the features don't separate) → the fitter cannot fix a capacity problem.
- (b) B6 < 0.95 or B4 < 0.50 → the μ/λ tradeoff broke primary calibration → the objective is misweighted, not the idea — but per round rules, kill the fork as specified (a re-weighted revival is a new fork).
- (c) B3 passes while B2 fails (V1+V2>0) → the fork is gaming the bar: flat G with live per-item theater is dishonest calibration → kill for bar-gaming.

**Adversarial note.** GRAF's biggest risk is (a): if survivors at d=16 need systematically different weights than the d=1 pool, one linear head cannot be calibrated at all rungs simultaneously and L will compromise — watch the per-rung G(d) profile, not just the violation count.

---

## Fork 3 — "Foreshadow Head" (abstention-predictive discount)

**Mechanism (new predictive feature + discount).**
New feature `f9` = predicted P(release at d+1 | state at d), thousandths, deterministic:
`f9 = clamp(1000 − [α·(1000−f1) + β·f3 + γ·(1000−f6) + δ·f8]/1000, 0, 1000)`
Low margin, leader-changed flag, low survivor fraction, high flip trauma ⇒ unlikely to survive the next M4 gate. α,β,γ,δ ≥ 0 fitted per-leg alongside w (same fitter; projection to nonnegative).
Head: `C(s) = clamp((Σ_{i=1..8} w_i·f_i)/1000 + b − (w9·(1000 − f9))/1000, 0, 1000)`, w9 ≥ 0 projected.

**Targets:** B2 theater at its root; mode 5 (mask-invisible depth schedule); mode 1 (clamp attractors).

**Mechanistic argument.** Theater is conf high while correctness flips correct→wrong across depths — but the flip is never a surprise in deliberation state. It is telegraphed: margin decay (f1↓), velocity turning negative (f4), leader-change flags (f3), flip trauma (f8). The current head is myopic: it scores the present. Foreshadow scores the *future*: conf falls BEFORE the doomed release, so the released-at-d cell of an item about to flip carries low conf, and when it flips wrong at d+1 the residual stays small. Mode 5: the depth schedule becomes visible through the hazard term — a function of deliberation dynamics, not the rung index — so depth effects can't hide behind the mask. Mode 1: the discount injects a state-dependent term that varies even when margins saturate at clamps, breaking attractor lock. Note the release rule is untouched — foreshadow moves conf only, never release (B7 abstention rate unchanged by construction).

**Predicted bars.** B2 V1=V2 → 0; B1 holds (conf descends smoothly along the foreshadow gradient rather than slamming 1000→0); B3 improves on logic/trap legs where flips are telegraphed; B4 holds if foreshadow is specific (false-foreshadow on honest stable items is the risk — see falsification (c)).

**Falsification (kill if ANY holds).**
- (a) B2 V1+V2 > 0 on any leg with n_rel ≥ 16 → flips are NOT telegraphed in deliberation state → the core premise is false.
- (b) α,β,γ,δ fit to ≈0 on a majority of legs → the feature is dead weight, not a mechanism.
- (c) B4 < 0.50 on any honest leg → the discount punishes honest stable items (false foreshadow) → the hazard model is mis-specified.

**Adversarial note.** The linear hazard is crude — f3 at depth d says the leader *already* changed arriving at d, which under M4 may mean the item already abstained; the fitter must learn the *forward* dynamics from a backward-looking flag. If (a) kills it, the honest conclusion is that deliberation state lacks forward information, which is itself a finding.

---

## Fork 4 — "Self-Normalized Margin Head" (scale-free features)

**Mechanism (feature transform; head form otherwise unchanged).**
Replace absolute margin features with self-normalized ones. `f1' = clamp(1000·f1 / max(64, M1), 0, 1000)` where M1 = trailing max of f1 over the item's depth path up to the current rung (integer; denominator floored at 64). The 64 floor is load-bearing against mode 7 (margins below 6.4% of full scale are below the thousandths quantization signal — derived from the representation, not an arbitrary cap). Similarly `f4' = clamp(1000·f4 / max(64, M4a), −1000, 1000)` with M4a = trailing max |f4|.
Head: `C(s) = clamp((w1·f1' + w4·f4' + Σ_{i∉{1,4}} w_i·f_i)/1000 + b, 0, 1000)`.

**Targets:** mode 1 (clamp attractors); mode 8 (ceiling/O pooling); mode 3 (uniform-manifold escape).

**Mechanistic argument.** Clamp attractors come from ABSOLUTE margin scales: across pooled families, one family's "decisive" margin is another family's noise, so the linear head saturates at 0/1000 on whole families (mode 8 makes this structural). Self-normalization makes each item its own yardstick: conf reflects how decisive the current margin is *relative to what this item has shown* — scale-free, so no family can pin the head at a clamp. Mode 3: on a uniform manifold absolute features are constant and gradients die; normalized features retain within-path variation (relative decisiveness), keeping the fitter's gradients informative. Trap interaction (honest secondary effect): trap survivors have large-but-flat absolute margins — absolute f1 rewards them; normalized f1' asks "large relative to what?" and normalized velocity f4' separates *growing* decisiveness (honest convergence, f4'>0) from flat-high margins (traps, f4'≈0) — with w4>0 the head rewards becoming-decisive, which traps cannot fake without actually accumulating evidence.

**Predicted bars.** Clamp-attractor legs recover: B4/B4b ≥ 0.50 on pooled ceiling/O legs; B8 flatness improves across pooled families; B5 separation ↑ (scale alignment lets one weight vector separate across families); B2 no worse than baseline.

**Falsification (kill if ANY holds).**
- (a) Clamp attractors persist (any leg with >50% released cells at conf ≡ 0 or ≡ 1000) → absolute-scale saturation wasn't the cause.
- (b) B2 theater rises vs baseline → normalization amplified noise-driven conf jumps (the 64 floor insufficient) → the transform is unsafe.
- (c) Fitted w1 on f1' ≈ 0 on a majority of legs → the transform destroyed the margin signal rather than rescaling it.

**Adversarial note.** The trailing max is path-dependent: an item whose margin spikes once early (f8 trauma territory) gets a huge M1 and then permanently suppressed f1' — the very items foreshadow cares about. Forks 3 and 4 compose badly on this point; if both survive independently, the composition needs a trauma-aware M1 (e.g., trailing max over a capped window — itself a new fork, not assumed here).

---

## Composition + anti-gaming notes
- Forks 1+2 compose cleanly (feature discount + rung-anchored fitter; GRAF's per-depth objective would price USD's trap correction at each rung). Forks 3+4 compose with the caveat noted above.
- Anti-gaming: B13's −0.100 floor caps B3-gaming room at 0.100 — none of these forks can pass B3 by diving G negative. Fork 2's falsification (c) explicitly kills flat-G-with-theater.
- All forks: pure integer thousandths math, no family labels, no text, zero RNG, deterministic. Division only with floored denominators (64). w9/α..δ nonnegative by projection.
- Open interpretation risk: B1 "1→0=0" assumed to mean no 1000→0 clamp slam across rungs; if the frozen prereg defines it as released→abstain transitions, Fork 3's predictions are unaffected (it never touches release) but its B1 argument is vacuous — re-map on the true definition.
