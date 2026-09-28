# H5 Fork Ideas — Native Brainstorm 2 (native2)

Independent native brainstorm. No external models. Four fork designs, each a NEW
mechanism for the confidence head — none is a per-item monotonicity (ceiling)
constraint, none is a ledger/counter variant.

## Ground rules (shared by all forks)

- Release rule FIXED (M4 skeleton: release L_t iff L_t == L_1). The head never
  changes which cells are released, so **B1, B6, B7 are release/learner
  properties the head cannot move**. The head's battleground is exactly:
  **B2** (theater), **B3** (strict G nonincreasing), **B4/B4b** (mean conf on
  correct / honest-family), **B5** (separation), **B8** (G-flatness), **B13**
  (G ≥ −0.100 per (family,depth) with n_rel ≥ 8).
- Pure Zag, zero RNG, deterministic integer math, byte-identical reruns.
- Integer conventions: confidences and features in thousandths, integers in
  [0,1000]. Weights in thousandths, integers in [−1000,1000]. Every term is
  `(w·f)/1000` computed in i64, then Zag integer division (deterministic;
  truncation semantics fixed by the toolchain). `clamp(x,0,1000)` explicit.
  All features are nonneg, so sign behavior is fully determined.
- Correctness labels (y ∈ {0,1}, scaled to 0/1000) may be used at TRAINING time
  only, to fit weights. At inference the head sees only deliberation-state
  features. No family labels, no text, no baked-in tables anywhere.
- Shared deterministic trainer **TRAIN-COORD**: parameters start at 0; fixed
  sweep order; each parameter tried at ±50 steps within its box; first strict
  improvement accepted; 8 sweeps max; deterministic. Base objective: squared
  calibration error Σ(C − 1000·y)² over training cells. Hard vetoes on every
  candidate: (V1) theater V1+V2 > 0 on training cells → reject; (V2) training
  meanConfCorrect < 0.55 → reject (0.05 safety margin over B4); (V3) any
  training (family,depth) with n_rel ≥ 8 and G < −0.080 → reject (0.020 safety
  margin over B13).
- Notation: R_d = released set at depth d in a leg; N = leg item count;
  G(d) = mean_{i∈R_d}[C_i] − acc(R_d).

---

## FORK 1 — POPNORM: Population-Normalized Confidence (selection-debias head)

**Spirit:** compositional debias. The M4 selection effect is a *population*
phenomenon; fight it with a *population* observable, not a per-item constraint.

**Mechanism.** New feature (same value for every cell in a leg — legal: it is a
within-run population statistic, not a family label, not text):

- `f9 = 1000·(N − R_d)/N` (integer division), where `R_d = |R_d|`.
  f9 = 0 at depth 1 (nothing selected out yet); grows as M4 abstains more.

Head form:

```
C(s,d) = clamp( (Σ_{i=1..8} w_i·f_i)/1000 + b − (w_9·f_9)/1000, 0, 1000 )
```

**Training rule (two-stage, both TRAIN-COORD-based, deterministic):**
1. Fit `w_1..w_8, b` on depth-1 training legs only (f9 ≈ 0 there, so the base
   head learns calibration on the *unselected* population). Objective: squared
   calibration error + vetoes V1–V3.
2. Freeze base weights. Fit `w_9` on training legs at d > 1 over grid
   {0,50,…,1000}: primary objective = number of strict B3 violations on
   training legs (minimize), tie-break = Σ_d |G(d) − G(1)|. Extra veto: reject
   any `w_9` candidate that pushes a training (family,depth) below G = −0.080.

**Targets:** failure mode **(6) M4 selection effects** (primary), **(7)
tiny-n noise** (secondary — f9 is a leg-level statistic, immune to per-cell
noise).

**Mechanistic argument.** Write G(d) = E[C|R_d] − P(correct|R_d). Under M4 the
released set turns over with depth (items leave when they diverge, returnees
re-enter), and P(i ∈ R_d) correlates with the head's own base features
(stability looks like confidence). So E[C|R_d] drifts upward with d *even when
every item's confidence is flat* — the drift is first-order in selection
intensity, and selection intensity is exactly what f9 measures
(`1 − |R_d|/N`). Subtracting `w_9·f_9` cancels the first-order compositional
term by construction, leaving only the per-item signal in the G(d) sequence.
This is NOT a ceiling: an individual item's confidence may rise along its
path; only the leg-level mean is debiased. It also cannot introduce theater
(B2): f9 is constant within a leg at fixed d, so within-leg conf ordering is
untouched, and the V1 veto guards the base head.

**Predicted bar outcomes.**
- B3: zero violations on training *by construction* (stage-2 objective);
  eval: expect 0–2 residual violations (the drift is only first-order linear
  in f9; nonlinear residue remains). Strictly fewer than base.
- B2: pass (V1 veto on base; f9 can't create within-leg theater).
- B5: unaffected (leg-level intercept shift preserves within-leg ranking).
- B4/B4b: the debias shifts means down at depth; expect pass with margin only
  if stage-2 drift is moderate — **flagged risk** if any family needs w_9 > 600.
- B13: guarded by the −0.080 veto on training; eval risk concentrated on
  sparse legs where f9 is large and accuracy didn't rise to meet it.
- B1/B6/B7: unmoved (release-fixed).

**Falsification (kills it).** (a) Eval strict-B3 violations ≥ the base head's
count → the compositional model bought nothing. (b) On >1/3 of eval families
the G-drift-vs-f9 slope has the wrong sign or is ~0 while G still rises →
the drift is not selection-intensity-driven; the mechanism's premise is
false. (c) B13 failures exceed base's → the cure is worse than the disease.

**Adversarial notes (against myself).** B3's tolerance is 1e-12 — *strict*.
A linear correction will not achieve literal zero on unseen legs; claiming
"B3 passes" outright would be dishonest — the honest claim is "violations
collapse toward zero, residual risk from nonlinearity." Second: f9 correlates
with family difficulty (trap legs abstain more), so w_9·f9 acts as a
difficulty proxy — defensible as a live population observable, but if the
round judges it a family label by another name, this fork is disqualified on
legality, not performance. Third: if accuracy rises with selection as fast as
mean conf does on some family, w_9 overshoots and manufactures
underconfidence — the V3 veto only guards training legs.

---

## FORK 2 — DISMIN: Disjoint-Feature Min Ensemble (pessimistic redundancy)

**Spirit:** redundancy, not constraint. Two heads that *cannot* share a crutch;
confidence is what both of them endorse.

**Mechanism.** No new features. Split the existing eight into disjoint sets —
A sees only trajectory/margin features, B sees only evidence/survivor
features:

```
A(s) = clamp( (Σ_{i=1..4} a_i·f_i)/1000 + a_0, 0, 1000 )
B(s) = clamp( (Σ_{i=5..8} b_i·f_i)/1000 + b_0, 0, 1000 )
C(s) = min(A(s), B(s))
```

**Training rule:** fit A and B independently with TRAIN-COORD (squared
calibration error, vetoes V1–V3 each). Then bias-shift: grid-search a common
Δ ∈ {0,50,…,500} added to both a_0 and b_0, maximizing training B4 margin
subject to V3; this compensates min's structural pessimism. Final C = min.

**Targets:** failure mode **(2) crutch collapse** (primary), **(1) clamp
attractors** and **(3) uniform-manifold escape** (secondary).

**Mechanistic argument.** Crutch collapse is learning finding the laziest
separator: one dominant feature, seven atrophied weights. A single head cannot
be made crutch-proof because any structural fix is itself learnable-around.
With disjoint feature sets, a single-feature crutch (say f7, sole-survivor
pin) can corrupt *at most one* head — the other never sees f7 — and `min`
takes the uncorrupted head's lower value. The veto is automatic and needs no
detection step. Clamp attractors: C ≡ 1000 now requires *both* heads
saturated — strictly harder than one head saturating. Uniform manifold: with
all features middling, both heads agree at middling; there is no single weird
feature for the head to escape through, because any escape route lives in only
one head and gets minned away. Note this is *not* a ceiling in any sense:
both heads are ordinary snapshot heads; confidence may rise, fall, or do
anything along a path — the only structure is cross-head pessimism within a
cell.

**Predicted bar outcomes.**
- B2: pass — min of two theater-free heads is theater-free (if neither head's
  conf rises on a correct→wrong / wrong→wrong cell, neither does the min).
  V1 veto enforced per head.
- B3: improves *only if* the base's violations were crutch-driven; if they
  were selection-driven (mode 6), DISMIN ≈ base on B3. Honest expectation:
  partial.
- B4/B4b: **main risk** — min is structurally pessimistic; the Δ bias-shift
  is load-bearing. Expect pass on training by construction; eval margin thin.
- B5: expect pass — both heads are fitted to separate, so the min mostly
  preserves the correct/wrong gap (fails only if one head is systematically
  low on correct items — measurable on training).
- B13: secondary risk from underconfidence; guarded by V3 + Δ search.

**Falsification (kills it).** (a) Measured veto rate on eval —
fraction of cells with min(A,B) < max(A,B) − 50 — below 2% **and** B3/B8 no
better than base → the disjointness never fired; the fork is decorative.
(b) B4 fails after the full Δ shift → min-pessimism is unfixable within the
bias box; the architecture is too gloomy to survive. (c) Both heads collapse
onto *correlated* crutches (A leans on f1, B on f5, and f1≈f5 on the eval
manifold) → single-crutch protection was the wrong threat model.

**Adversarial notes.** The design buys robustness against *single*-feature
crutches only; a two-feature crutch with one foot in each set walks straight
through. The Δ bias-shift is slightly embarrassing: we fit two honest heads,
then deliberately miscalibrate both upward so their min lands right — the
"honesty" lives only in the min operation. If the round's philosophy demands
each component be calibrated, this fork is philosophically disqualified even
if it passes bars. Also: min *discards* information (the higher head's
opinion is thrown away) — on legs where one head is simply better, DISMIN
underperforms the better head alone; check per-head vs min B8 on training.

---

## FORK 3 — EFFIC: Deliberation-Efficiency Head (cost of conviction)

**Spirit:** a new information channel. Don't weigh the margin harder — ask what
the margin *cost*.

**Mechanism.** New feature — deliberation efficiency (margin per unit evidence
spent along the item's path):

- `cumE` = cumulative evidence units examined along the item's path to depth
  d (integer, monotone nondecreasing in d; the harness already logs per-depth
  evidence for f5 — this is its running sum).
- `E_ref` = median `cumE` over the leg's released cells at depth d
  (deterministic; even-count ties take the lower median).
- `q = (cumE·1000)/E_ref` (integer division; q = 1000 ⇔ spent exactly the
  leg-median evidence).
- `f9 = (f_1·1000)/(1000 + q)` — the clamped margin f1, discounted by evidence
  spent. Converged fast on median evidence → f9 ≈ f1/2·… precisely:
  q=1000 ⇒ f9 = f1·1000/2000 = f1/2. Spent 10× median ⇒ f9 ≈ f1/11.

Head form:

```
C(s) = clamp( (Σ_{i=1..8} w_i·f_i + w_9·f_9)/1000 + b, 0, 1000 )
```

**Training rule:** TRAIN-COORD over w_1..w_9, b (squared calibration error,
vetoes V1–V3). Pre-registration gate (stillborn check on training legs):
if within-leg std(q) < 100 on >50% of training legs, the fork is degenerate
(see falsification) — report and do not burn eval on it.

**Targets:** failure mode **(8) ceiling/O pooling** (primary), **(5)
mask-invisible depth schedule** (secondary).

**Mechanistic argument.** At high depth the released survivors pool: margins
saturate, leader flags go quiet, and every margin-derived feature goes blind —
but `cumE` keeps growing and *differs across pooled items*: some converged in
3 depths, some churned for 60. Efficiency discounts the churners: reaching the
same margin at 10× the evidence is evidence of ambiguity, not conviction.
This is spread done right — the earlier spread attempt anti-learned (mode 4)
because raw feature-spread conflates healthy debate with confusion; a
*monotone* ratio (less evidence for the same margin is always better) has no
such ambiguity. For mode 5: cumE is inherently depth-visible and monotone in
d by construction — even if w_2 (the f2 depth weight) collapses to zero, depth
information still flows through w_9·f9. The schedule cannot be masked because
it is baked into the feature's definition, not its learned weight.

**Predicted bar outcomes.**
- B8: expect visibly flatter G at d ∈ {16,32,64} — exactly where pooling was
  worst. This is the fork's headline prediction.
- B3: expect fewer violations at high d; low-d violations (selection-driven)
  largely untouched — EFFIC does not model composition.
- B2: **flagged risk** — f9 is not monotone along a path (a margin jump can
  outrun evidence accrual), so theater is possible in principle; V1 veto
  guards training, eval is the test.
- B4/B5: expect pass — efficiency preserves ranking among correct items
  (fast-converging correct items keep high conf).
- B13: secondary risk — f9 adds within-leg variance, which is exactly what
  tiny-n legs punish.

**Falsification (kills it).** (a) Degeneracy: within-leg std(q) < 100 on
>50% of eval legs → cumE is ~constant within (leg,depth) (the learner spends
fixed evidence per depth regardless of item) → f9 is just a depth-rescaled
f1 and the fork collapses to the base head. Stillborn, by the pre-registered
gate. (b) High-depth B3/B8 no better than base despite non-degenerate q →
efficiency doesn't predict correctness; the "cost of conviction" story is
wrong. (c) Fitted w_9 ≈ 0 → the trainer itself found no signal; believe it.

**Adversarial notes.** The most dangerous trap for this fork is the
*fast-wrong* item: a distractor that snaps shut early (high efficiency, wrong
answer) gets HIGH confidence — EFFIC is confidently wrong there, and no
within-design element catches it. If trap legs are built from fast-snapping
distractors, this fork dies by B8/B13 on trap families specifically — check
the per-family breakdown, not just the aggregate. Second: E_ref as a per-leg
median means f9's meaning shifts per leg (efficiency *relative to this leg's
typical spend*) — a leg of uniformly fast items makes a normal item look
wasteful. That relativity is a feature for pooling (comparisons are
within-pool) but a bug for absolute calibration; B13 on odd legs will tell.

---

## FORK 4 — DIVE-TAX: Divergence-History Honesty Tax (returnee distrust)

**Spirit:** price the item's history instead of constraining its future. M4
judges only the endpoint (L_t == L_1); the head taxes the path.

**Mechanism.** New feature — graded divergence history:

- `D` = count of depths k < d with L_k ≠ L_1 (integer; the harness carries a
  running divergent-depth count per item — deterministic).
- `f9 = (1000·D)/d` (integer division) = fraction of the path spent diverged,
  in thousandths. Pristine items: f9 = 0. Chronic divergers: f9 → 1000.

Head form:

```
C(s) = clamp( (Σ_{i=1..8} w_i·f_i)/1000 + b − (w_9·f_9)/1000, 0, 1000 ),
w_9 ≥ 0 (box-constrained in TRAIN-COORD)
```

**Training rule:** TRAIN-COORD over w_1..w_8, b, w_9 ≥ 0 (squared calibration
error, vetoes V1–V3). Stillborn gate: fire rate (fraction of released
training cells with f9 > 0) must exceed 5%, else the tax never fires — report,
don't eval.

**Targets:** failure mode **(6) M4 selection effects via returnee
composition** (primary), trap legs (secondary).

**Mechanistic argument.** M4 has endpoint blindness: an item that diverged at
depths 2–4, returned at 5, and sat stable through 8 is released at d=8 looking
*pristine* — f3 (last-step leader-changed flag) is 0, margin is high, the
snapshot features have amnesia. But early divergence means the evidence was
genuinely ambiguous: two leaders both had support, and the final leader won by
deliberation-depth, not by decisive evidence. Such items sit closer to the
decision boundary → higher error rate at equal snapshot margin. The tax
prices exactly this: a one-time honesty discount for past divergence, with no
monotonicity imposed on the path (confidence may still rise later — this is
pricing, not a ceiling). Compositionally, returnees *accumulate* with d
(longer paths have more chances to diverge-and-return), so the tax
specifically flattens the returnee-driven component of the G(d) rise — a
per-item attack on failure mode 6, complementary to POPNORM's population
attack. On trap legs: traps are engineered ambiguity; diverged-and-returned
trap items are the precise population the base head over-trusts.

**Predicted bar outcomes.**
- B3: expect the returnee-driven part of drift to flatten; pure-selection
  drift (low-conf items leaving) remains — so expect *reduction*, not
  elimination, of violations. Weaker B3 claim than POPNORM, more honest.
- B2: pass expected (V1 veto); note f9 = 1000D/d can move either way along a
  path, so the tax term can shrink — conf may rise along a path, which is
  allowed, and the veto ensures it never rises on the forbidden transitions.
- B4/B5: expect pass — the tax hits a minority subpopulation (the diverged);
  pristine correct items untouched.
- B13: the tax *lowers* conf on exactly the items most likely to be wrong →
  should *improve* G floors on legs with returnee-heavy errors. If anything,
  this fork's B13 direction is favorable.
- B8: mild improvement where returnees were the pooling population.

**Falsification (kills it).** (a) Fire rate < 5% on eval → the taxed
population barely exists in released sets; the fork is a no-op. (b) Fitted
w_9 = 0 on training → no signal; believe the trainer. (c) **Wrong-sign:**
accuracy(taxed cells) ≥ accuracy(untaxed cells) − 0.02 on eval → divergence
followed by return is *evidence for* correctness (the "what doesn't kill me"
hypothesis: deliberation stress-tested L_1 and it survived) and the tax is
anti-calibrated. This is the kill condition I most expect to matter — the
mechanistic story is genuinely ambiguous, and the data decides. (d) B3
violations ≥ base → the returnee component wasn't the driver.

**Adversarial notes.** The "what doesn't kill me" objection (c) is the
strongest attack and I cannot dismiss it a priori: surviving a challenge can
signal robustness, not fragility. The fork bets the ambiguity story beats the
robustness story *for the M4-released population specifically* — note the
subtlety: among ALL items, return-to-L_1 might signal robustness; among
M4-RELEASED items at high d, the base rate of correctness is already high and
the marginal returnee is the suspicious one. The falsification condition is
scoped to the released population for exactly this reason. Second attack:
D/d dilutes the tax at high d (2 divergent depths at d=64 → f9=31, negligible)
— precisely where returnees accumulate most. A dilute-at-the-scene tax may do
nothing where it's needed; consider this a known weakness, measurable via the
per-depth B3 breakdown. Third: D requires the harness to log per-item leader
history — if the harness only kept snapshots, this fork has an implementation
dependency the others don't.

---

## Comparison

| fork | new observable needed | primary failure mode | spirit in one line |
|------|----------------------|----------------------|--------------------|
| POPNORM | per-leg N, R_d (harness already has) | (6) selection effects | debias the composition, not the item |
| DISMIN | none (f1..f8 only) | (2) crutch collapse | two heads that can't share a crutch; believe both |
| EFFIC | cumE per cell + per-leg median | (8) ceiling/O pooling | ask what the margin cost |
| DIVE-TAX | per-item divergent-depth count D | (6) via returnees; traps | M4 judges the endpoint; tax the path |

What was deliberately NOT proposed: any per-item monotonicity along the depth
path (ceiling family — best arm already exhausted it and it still fails
strict B3/B13); any audit/counter ledger variant; any isotonic/lookup-table
calibration (baked-in table, banned); any use of labels at inference.

## Cross-fork note for the round

POPNORM and DIVE-TAX attack failure mode 6 from opposite ends (population vs
per-item) and compose cleanly — a POPNORM+DIVE-TAX hybrid is the obvious
follow-up if both show partial B3 wins. DISMIN is the only fork requiring no
new harness observables (cheapest to run first). EFFIC has a pre-registered
stillborn gate — check it on training legs before spending eval budget.
