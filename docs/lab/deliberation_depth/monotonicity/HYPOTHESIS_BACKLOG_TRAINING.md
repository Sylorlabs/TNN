# HYPOTHESIS BACKLOG — TRAINING/LEARNING HYPOTHESES FOR H5 DEPTH-OVERCONFIDENCE

- **Status:** BACKLOG v1 — preregistered, not yet measured. Each entry's kill
  bar is frozen at write time; running an entry means executing its kill bar
  as stated. Any change to an entry requires version bump + note.
- **Date:** 2026-09-24
- **Authority:** Parent-orchestrator tasking under Micah's standing rules
  ("test everything, not just the plausible ones"; rank by expected
  information value).
- **Context:** The H5 monotonicity program
  (`deliberation_depth/monotonicity/`, PREREG_MONOTONICITY.md frozen v1)
  killed all mechanism designs M1–M7 (M1/M2/M3 on accuracy flips; M4/M5/M7 on
  L-OVERCONF; M6 by red team); M0 holds only degenerately. The preregistered
  P/O mirror theorem predicts no admissible mechanism meets all SHIP gates.
  Micah's hypothesis H-0 (below) is being tested by a separate training crew.
  This backlog supplies every OTHER training/learning hypothesis worth
  testing, collected from three independent sources.

## Sources

1. **grok-4.7** at highest reasoning effort via streaming wrapper
   (`~/workspace/skills/unorouter/bin/grok47_stream.py`), prompted to be
   super thorough. 22 hypotheses (H-1…H-22), own red-team pass, own ranked
   top 5. Raw: `hypothesis_backlog/grok_raw_hyp.txt`; prompt:
   `hypothesis_backlog/grok_prompt_hyp.md`.
2. **claude-fable-5.1**, ONE deep batched round via
   `~/workspace/skills/unorouter/bin/fable_stream.py`: 10 hypotheses
   (H-F1…H-F10) + a formal attack on the P/O mirror theorem (Batch 2) + a
   composite 4-phase training-regime design (Batch 3) + own ranked top 5.
   Raw: `hypothesis_backlog/fable_raw_hyp.txt`; prompt:
   `hypothesis_backlog/fable_prompt_hyp.md`.
3. **Native passes.** No subagent spawning is available at this depth
   (depth 2/2, can_spawn=no), so the native-source role was played by three
   independent in-context generation passes with disjoint framings —
   (A) the mechanist (one hypothesis per white-box root cause),
   (B) the developmentalist (human developmental stages → curricula),
   (C) the information theorist (depth as an information channel) —
   followed by a red-team pass over all 16 native hypotheses (steelmanning,
   strongest counter-arguments, dependency graph, preliminary ranking).
   Raw: `hypothesis_backlog/native_passA_mechanist.md`,
   `native_passB_developmental.md`, `native_passC_information.md`,
   `native_redteam.md`.

## Reference: H-0 (Micah's hypothesis — tested by the separate training crew)

- **Claim:** Overconfidence with depth is a TRAINING/LEARNING property, not a
  mechanism flaw — depth can be trained (guided learning / developmental
  curriculum) not to be overconfident.
- **Predicted observable:** A developmentally trained system shows
  non-increasing G(d) and zero V1/V2 on all batteries without hand-coded
  release gates.
- **Kill bar:** After the developmental curriculum, any L-OVERCONF violation
  (G(d+1)>G(d) or ≥1 V1/V2) on any battery → H-0 killed as stated.
- **Deciding batteries:** all frozen batteries (admit/revoke/logic/trap/cost,
  P/O/D ceiling, redteam).
- H-0 is the reference against which the backlog's specificity is judged:
  every entry below is a DISAGGREGATION of H-0's "training can fix it" into
  a concrete mechanism + intervention + kill bar.

## Backlog-wide caveats (from grok's red-team; apply to all entries)

- **C1 — the leak kill-switch.** Every entry predicting "P and O will not
  split" shares one kill switch: an item-identity or polarity leak. The
  frozen redteam (~10 items) is too small to certify leak absence. Any
  positive "O fixed, P kept" result must pass a cloned-prompt audit
  (byte-identical inputs, polarity-flipped grader labels) before it counts.
- **C2 — the reachability of zero.** Every entry predicting G(d)≤0 while
  accuracy falls to 0 depends on released confidence being able to reach 0,
  which fails if the sole-survivor pin is a non-trainable constant. T-09
  (OPSLEVEL) decides this.

## Dependency graph (read before scheduling)

- T-01 (mirror bind) is a METHODOLOGICAL gate on all results: any "O fixed,
  P kept" claim must survive the cloned-prompt audit first.
- T-02 (sufficiency gate) gates T-14, T-16, T-10, T-24: if correctness is
  not predictable from index-level deliberation state, the confidence-
  channel program dies and only structural fixes remain.
- T-09 (ops level) gates T-04, T-12, T-11: if the pin/kill sit outside the
  trainable graph, confidence-channel interventions are aimed at the wrong
  layer.
- T-07 (reversal skepticism) is enabled by patience (T-22): the discount
  needs time before the kill locks the flip in.
- T-25 (no-fabrication) is conditional on a law refinement (kill only if
  G crosses 0, or on V1/V2) — under the current letter it cannot fully
  pass; record which reading is used.
- T-08 / T-22 may refile as MECHANISM M8 (reversal-stop / conditional
  patience) if the learned policy collapses to a hand-specifiable rule.

---

## THE RANKED BACKLOG (by expected information value)

### T-01 — THE MIRROR BIND (grok H-7; fable Batch-2 verdict)

- **Claim:** No training regime whose learned policy is a deterministic
  function of the observable input can raise P accuracy with depth while
  keeping O accuracy from falling, on cloned-prompt P/O pairs
  (byte-identical inputs, polarity-flipped grader labels).
- **Mechanism:** Identical bytes → deterministic transition → identical
  state at every depth → identical release; truth is mirrored, so
  acc^O_d = 1 − acc^P_d for every weight setting reachable by any
  curriculum, loss, replay, or learned op. Fable's formal attack concludes
  the theorem is airtight under current admissibility; learning changes
  nothing (learned parameters θ are a fixed function f_θ(s_d), not
  per-item state). Narrowest caveat (fable): the premise that
  evidence-weight/link-structure trajectories are identical for P/O at
  matching depths — holds only if weighting is index-position-based, not
  margin- or velocity-dependent. Second-order margin statistics (velocity,
  curvature) are index-level and COULD differ (P tail grows margin, O
  plateau is flat) — the theorem implicitly assumes the mechanism does not
  track them.
- **Training intervention:** None — this is the constraint audit. Build the
  cloned-prompt P/O battery (same 40 pairs, byte-identical prompts, hidden
  label flip) and run EVERY trained policy from this backlog against it.
- **Predicted observable:** For every trained policy,
  max_d |acc^O_d − (1 − acc^P_d)| < 0.02. Any reported joint win sits
  entirely on natural-surface (non-cloned) items.
- **Kill bar:** ONE deterministic policy, audited leak-free, with
  acc^P_64 − acc^P_1 > 0.1 AND acc^O_1 − acc^O_64 < 0.1 on byte-identical
  prompts → the bind is KILLED (and the white-box story is incomplete).
  Randomness at decision time does not count (violates system law, not the
  hypothesis).
- **Deciding batteries:** P and O ceiling only, cloned-prompt build, depths
  1–64, n=40 pairs; redteam restricted to leak tests (id embedding, length
  side channels, grader probes).
- **Information value:** Decides whether the rest of the program is a search
  for a policy or a search for a metric. If it lives, H-0 is false for the
  joint accuracy goal and every "fix O without hurting P" claim is choosing
  a side of an identity. Run before any new training run (grok's committed
  order).

### T-02 — THE SUFFICIENCY GATE (native H-C4; absorbs fable H-F10 diagnostic, grok H-4 trap arm)

- **Claim:** The correct learned object is not confidence but the SUFFICIENT
  STATISTIC of the deliberation trajectory for correctness; training should
  discover the minimal statistic E with P(correct|trajectory) = P(correct|E)
  under an information bottleneck, and confidence should be a function of E.
- **Mechanism:** The margin is a catastrophically insufficient statistic
  (correct/wrong margin distributions overlap almost completely). Depth-
  overconfidence is what happens when decisions condition on an insufficient
  statistic: the unconditioned residual (family, flip-structure) leaks into
  error the statistic cannot see.
- **Training intervention:** Representation-learning on logged deliberation
  trajectories from all batteries: train encoder E of the index-level
  trajectory to predict correctness, minimizing I(E; trajectory) subject to
  maximizing I(E; correctness). Release confidence = calibrated map of E.
- **Predicted observable:** E reaches correctness-prediction AUROC ≥ 0.85
  on held-out items (vs margin's ~0.55); inspection of E reveals WHICH
  trajectory features carry the signal — the experiment discovers the
  mechanism, not just the fix.
- **Kill bar:** E's WITHIN-FAMILY held-out AUROC ≤ 0.65 on O items alone
  (pooled AUROC does not count — a family classifier clears 0.65 without
  learning anything; require within-O AUROC ≥ 0.7 for the positive claim)
  → KILLED, and with it the entire "train the confidence channel from
  index-level state" program (T-14, T-16, T-10, T-24 die as corollaries).
  A negative result is the most informative possible outcome: it proves the
  fix must come from OUTSIDE index-level state.
- **Deciding batteries:** ALL — E trained on all families; cross-family
  generalization (train on admit/logic, test on O) is the transfer test;
  redteam: adversarial items must not fool E.
- **Information value:** The backlog's load-bearing node. Run FIRST among
  the training experiments (right after T-01's audit harness exists).

### T-03 — ADVERSARIAL COVERAGE: DATA OR ARCHITECTURE? (fable H-F9)

- **Claim:** The training distribution lacks O-type items (plateau-then-flip
  toward wrong); the system extrapolates catastrophically to an adversarial
  worst case its calibration never saw. Adding O-type items fixes it iff
  the problem is coverage, not architecture.
- **Mechanism:** Roots (a)–(e) collectively describe what happens ON an
  O-item, but the reason the system never learned to handle one is that it
  never saw one in training. Calibration fit to the training distribution
  extrapolates to O.
- **Training intervention:** Generate O-type items systematically (known
  construction: plateau then flip, GT mirroring P), include at ≥20% of the
  training distribution with depth-indexed correctness labels, difficulty-
  scaled (easy O first, ceiling-family O later).
- **Predicted observable:** O-item handling in eval matches O-item handling
  in training: calibrated confidence and/or appropriate abstention; the
  learned defense transfers to novel O-items (trap battery).
- **Kill bar:** On ceiling-family O items at depth 64: accuracy still 0%
  AND abstention-before-flip rate < 10% (behavior identical to baseline:
  runs to d64, maximally confident, wrong) → KILLED — the problem is not
  coverage but architecture, and mechanism redesign is mandatory.
- **Deciding batteries:** P/O/D ceiling 40 each depths 1–64 (accuracy +
  calibration on O); trap 127 (unseen O-type items — the generalization
  test); redteam ~10 (hand-crafted O variants to defeat the trained
  defense).
- **Information value:** If killed, every other training hypothesis is dead
  on arrival — the gate determining whether the training program is viable
  at all. (Fable's rank 1.)

### T-04 — ANTIPIN: TRAIN THE KILL-EVENT SIGN FLIP (grok H-14; native H-A3)

- **Claim:** The most literal training translation of the strongest
  white-box finding: train confidence to DROP, not pin, at the
  sole-survivor event — c_post ≤ c_pre on kill rounds — removing V2 and the
  rising limb of G(d) on every family sharing root cause (a), with no
  family label.
- **Mechanism:** 100/100 ground-truth kill events pinned c=1000 while wrong;
  the jump is caused by the competitor's death, not evidence. Post-kill c
  becomes a non-increasing function of a frozen board — an honest
  description of what the board is.
- **Training intervention:** From traces, mark every round where runner-up
  count hits zero. Loss on kill rounds: max(0, c_post − c_pre + ε),
  ε=0.05, plus standard log loss elsewhere so non-kill rounds can still be
  confident. Apply to trap + general pool, NOT O specifically. Mask item
  id. If the pin is a non-trainable constant, the loss cannot decrease —
  that outcome is a result (hands the problem to T-09), not a tuning
  failure.
- **Predicted observable:** Correlation of Δc with the kill bit goes from
  positive to ≤ 0 on trap, O, P, D. O V2 rate < 5%. O accuracy still falls
  1→0; P accuracy still rises (the mirror is untouched — this is the
  confidence channel only).
- **Kill bar:** (i) The loss decreases but O V2 stays > 25% → the pin is
  not the only upward driver; root (a) not sufficient → KILLED as a
  complete account. (ii) The loss cannot be decreased at all (gradient zero
  into the pin) → the pin is architectural → KILLED as a training claim.
  (iii) P accuracy at d64 falls by > 0.1 → the loss leaked into the answer
  channel → KILLED as confidence-only.
- **Deciding batteries:** trap, O, P, D, all depths 1–64, trace-level kill
  bit as instrument; logic + admit (non-kill confidence preserved); cost
  (value-of-information confidence not flattened).
- **Information value:** Fails informatively in every direction: gradient-
  zero settles T-09; V2-dead-but-G-positive splits L-OVERCONF into two
  obligations the current statement conflates. (Grok's rank 2.)

### T-05 — WORST-CASE POLARITY LOSS (grok H-17)

- **Claim:** Log loss cannot express "never": on a double-labeled
  (cloned-pair) state it settles at c=1/2, and G=1/2 on a wrong O item
  still violates L-OVERCONF. Only a worst-case loss over polarity pairs —
  c ≤ min_polarities 1[correct], i.e. c=0 wherever either polarity is
  wrong — matches the law's universal quantifier.
- **Mechanism:** L-OVERCONF is a universal quantifier over items, not an
  average. The training-side expression of the bind (not an escape from
  it): the training signal uses both labels, the decision rule uses
  neither.
- **Training intervention:** For every trainable item, construct its
  polarity mirror (clone prompt, flip label). One state, two grades.
  Confidence loss = c if either grade is wrong, else standard log loss;
  answer loss standard on the original polarity only. Items that cannot be
  mirrored (logic, admit) use ordinary log loss. λ high enough that
  post-flip c<0.05 is cheaper than any positive c. Control arm: log loss.
- **Predicted observable:** Worst-case arm: cloned P and O post-flip c <
  0.05 both, V2 = 0, V1 = 0, G(d) ≤ 0 on O all d; P accuracy still rises
  with depth (P becomes underconfident post-flip — allowed if the law is
  one-sided). Log-loss arm: post-flip c ≈ 0.5, O G(d) ≈ 0.5, law violated.
- **Kill bar:** Worst-case arm leaves O G(64) > 0.1 or O V2 > 5% → KILLED.
  Or the log-loss arm reaches G ≤ 0 on O → the "only worst-case" part of
  the claim is KILLED.
- **Deciding batteries:** P and O cloned, depths 1–64, both losses; logic
  264 + admit 248 as non-mirror controls (mirroring must not leak into
  them); trap 127 + D 40 (does worst-case over-zero unmirrored families?).
- **Information value:** Identifies the loss geometry the law actually
  demands; if even worst-case training cannot reach G ≤ 0, the confidence
  variable is not under the loss's control and further objective design is
  wasted. (Grok's rank 3.)

### T-06 — INTERACTION 2×2: DE-PIN × REVERSIBILITY (native H-A5)

- **Claim:** No single root cause is sufficient: the pin (a) is harmless
  without irreversibility (c) — a reversible kill's pin would be corrected
  next round — and irreversibility without the pin gives only the mild
  M5-pattern G-rise, not the V1 catastrophe. Depth-overconfidence is the
  PRODUCT a×c; training must break the product, and breaking either factor
  alone is predicted to fail.
- **Mechanism:** Counterfactual decomposition: (a) without (c): pin fires,
  next round re-opens the kill, confidence re-grounds — V1 needs the
  wrongness to PERSIST, which needs (c). (c) without (a): wrong survivor
  with honest margin — mild G-rise, no V1/V2 catastrophe.
- **Training intervention:** 2×2, trained JOINTLY not sequentially (the arms
  interact: de-pinning changes the optimal re-admission threshold). Arm 1:
  de-pin only (T-04). Arm 2: reversibility only (T-12). Arm 3: both.
  Arm 0: neither (baseline).
- **Predicted observable:** The dissociation: Arm 1 → zero V1/V2, mild
  G-violations remain (M5-pattern). Arm 2 → zero 1→0, pin-spikes remain on
  transient wrong releases. Arm 3 → full L-OVERCONF satisfaction on O.
- **Kill bar:** If Arm 1 ALONE fully satisfies L-OVERCONF on O (no
  G-violation, no V1/V2) → the interaction claim is FALSE, (a) was
  sufficient → KILLED. If Arm 3 fails where the dissociation predicts
  success → KILLED.
- **Deciding batteries:** O (the product lives here); admit/logic (neither
  arm may break honest deliberation).
- **Information value:** Highest information-per-experiment of the mechanist
  set: determines whether the fix is single-point or compositional, which
  shapes the entire training program.

### T-07 — REVERSAL-KEYED SKEPTICISM (native H-B5)

- **Claim:** Depth-overconfidence is misplaced trust in late evidence: the
  system treats e_40 with e_1's credulity, so a late flip rewrites the
  verdict at full weight. Training a learned recency-skepticism that
  discounts late REVERSING evidence — keyed on post-plateau leader-change,
  which is index-level and P/O-distinguishing (P's tail confirms WITHOUT
  reversing the leader; O's flip reverses it) — inoculates against flips
  without touching P.
- **Mechanism:** On O the flip is driven by late heavy evidence after a
  long plateau, applied at face value (evidence application is symmetric —
  verified). A developmentally normal reasoner asks "why is this arriving
  now, and why so heavy?" The learned discount:
  effective_weight = raw × discount(recency, reversal magnitude, plateau
  length), deterministic in index state.
- **Training intervention:** Curriculum pairing flip-structured items
  (O/D/P) with provenance labels: late heavy REVERSING evidence labeled
  "suspect"; P's confirming tail labeled "legitimate". The discount must
  key on reversal, not lateness per se. Enabled by patience (T-22): the
  discount needs rounds before the kill locks the flip.
- **Predicted observable:** On O, the flip round's effective weight is
  discounted → margin discontinuity shrinks → leader does not flip or
  flips without triggering the kill → deep accuracy stays high, confidence
  honest. On P, accuracy-vs-depth still improves (confirming tail not
  discounted).
- **Kill bar:** Post-training O accuracy still collapses 1.00→0.00 → the
  discount did not stop the flip → KILLED. OR P accuracy-vs-depth no longer
  improves → the skepticism cannot distinguish reversal from confirmation
  (blanket cynicism; the mirror's revenge) → KILLED. The P-control is the
  load-bearing discriminator.
- **Deciding batteries:** O (must stop the flip); P (must NOT stop the true
  flip); D (dose-response of discount); revoke (honest late evidence —
  revoke items legitimately reverse early impressions — must survive).
- **Information value:** The mirror-theorem stress test in training form.
  If the discount saves O but spares P, a P-vs-O distinguishing feature
  EXISTS in index state and the mirror has a crack. If it cannot, the
  mirror gains its strongest confirmation yet. Decisive either way.

### T-08 — LEARNED STOPPING / DEPTH-AS-BUDGET (fable H-F6; native H-C5; grok H-18/H-20)

- **Claim:** The problem dissolves rather than solves: under a fixed
  deliberation budget — spending rounds early means fewer later — the
  system learns to PRICE depth, and priced depth does not overconfidence
  because every round must justify its cost in expected accuracy. The
  learned stopping policy stops before O's flip region and spends through
  P's.
- **Mechanism:** Unpriced depth is overconsumed; on adversarial streams
  overconsumed depth is pure risk with no return. Economic framing:
  overconfidence is the externality of free depth. Note the mirror
  constraint (native red-team): a pure learned pricer keys on identical
  pre-flip P/O state and cannot split them — UNLESS the stop rule keys on
  reversal-after-plateau (same defense as T-07), which never fires on P.
- **Training intervention:** Budgeted-deliberation curriculum: each item
  carries budget B (varied); learned stopping policy decides when to stop.
  Reward = correctness − λ·(rounds spent). O teaches deep spending has
  NEGATIVE expected return; P teaches positive return; honest items teach
  early stopping. Ablation: is the learned policy explained by
  reversal-detection alone?
- **Predicted observable:** Mean stop-round on O < flip round (cf. the
  frozen residual-flip bound: O acc 1.000 at 5.0 rounds); deep spending on
  P; d1–d2 stops on honest items. G(d) measured on CHOSEN depth per item.
- **Kill bar:** (i) The learned policy cannot beat the frozen residual-flip
  bound's O accuracy → learning added nothing → KILLED. (ii) It stops
  before P's flip (P accuracy collapses) → it learned fear, not pricing →
  KILLED. (iii) The ablation shows stop decisions are explained by
  reversal-detection alone → REFILE as mechanism M8 (reversal-stop), not a
  training discovery — still a win, but a different kind.
- **Deciding batteries:** O (stop before flip); P (spend through true
  flip); cost 125 (the cost battery IS the price list — learned λ must
  match it); D (dose-response of stopping price); redteam (bait items for
  premature release).
- **Information value:** Win-win experiment: either training discovers
  pricing (dissolves the problem) or it discovers M8 (mechanism). (Fable's
  rank 2; native rank 4.)

### T-09 — OPSLEVEL: WHICH LAYER MUST TRAINING TOUCH? (grok H-8)

- **Claim:** Learning must touch the deliberation OPERATIONS, not a release
  wrapper around frozen ops: the pin and the kill are computed inside the
  frozen region, and a wrapper never sees a pre-kill state it can honestly
  re-score. (Counter: a wrapper that sees the full pre-kill TRACE has the
  same information the ops have — "wrapper vs ops" may be a logging
  choice, not a stack level.)
- **Mechanism:** Root (a) fires by code at elimination; root (c) discards
  the runner-up, so the wrapper observes only the survivor's self-score. A
  wrapper can monotone-map an already-jumped 1000 or refuse to release; it
  cannot un-eliminate, prosecute the leader (e), or re-audit (c). Learned
  ops can change elimination criteria, evidence weights, and the kill bit.
  Neither level splits cloned P/O (T-01).
- **Training intervention:** Arm W: freeze ops, train only a release head
  (stop depth, confidence, abstain bit) on logged traces — WITH the full
  pre-kill trace visible (the red-team's counter). Arm L: unfreeze evidence
  weights, elimination threshold, add one trainable op; no wrapper. Same
  loss, data, steps. Deterministic at decision time both.
- **Predicted observable:** Arm W reduces V2 only by lowering c globally or
  abstaining; the kill bit still flips on the same round (pin visible
  pre-wrapper in traces). Arm L moves or removes the kill round itself on
  trap (kill-round histogram shifts).
- **Kill bar:** Arm W, ops verifiably frozen, eliminates V2 on trap (<5%)
  AND keeps trap accuracy within 0.02 of Arm L AND does not collapse mean
  c below 0.3 on correctly-answered logic items → wrapper sufficient →
  KILLED. Arm L killed if gradients into ops change no elimination decision
  on the trace schema (zero kill-round change on >95% of trap items).
- **Deciding batteries:** trap 127 + D 40 (kill-round movement); logic 264
  (collateral to legitimate elimination); P/O as mirror controls; the trace
  schema (kill round, pin event) is the instrument.
- **Information value:** Tells you where every subsequent gradient should
  be aimed; a wrong answer here makes T-04/T-11/T-12 look like training
  failures when they are access failures. Instrument inside T-04's harness,
  not as a separate program. (Grok's rank 5.)

### T-10 — LEARNED ABSTENTION AS A FIRST-CLASS OUTPUT (grok H-10; native H-B4; fable Batch-3)

- **Claim:** "I don't know" was never a REWARDED learned behavior — only a
  hand-coded gate. A system that learns abstention with its own reward
  history deploys it exactly where depth becomes dangerous, satisfying
  L-OVERCONF by honesty. (Downstream of T-02: the abstention policy must
  predict would-be-wrongness from index state — if T-02 goes negative, the
  bit cannot be selective.)
- **Mechanism:** Children are rewarded for saying "I don't know." TNN's
  abstention is an engineer's gate, never developmentally reinforced, so
  the policy never reaches for it under flip pressure — releasing is the
  only reinforced behavior, and depth increases the pressure to release
  (sunk deliberation cost). On cloned pairs the abstain bit is the same
  bit (T-01): it abstains on both post-flip ceiling states.
- **Training intervention:** Add output a∈{0,1}, deterministic. Signal:
  a=1 iff across a polarity-augmented view the graded answers disagree OR
  the item is a known overconfidence-family member. Loss: λ_a·abstention
  error + price γ per abstention (tuned on validation) + correctness loss
  only when a=0. Confidence when a=1 forced to 0 by loss, not by hand gate.
- **Predicted observable:** Post-flip abstention rate > 0.9 on BOTH cloned
  P and cloned O; on trap, abstention rate ≈ baseline V2 rate (it abstains
  where it used to lie); on logic < 0.05. Conditional on answering, G(d)≤0
  everywhere. Unconditional P accuracy does not rise with depth if
  abstentions count as not-correct — REPORT BOTH SCORINGS side by side.
- **Kill bar:** At the γ achieving O V2 < 5%, logic abstention rate > 0.15
  → the bit is not selective → KILLED. Or conditional-on-answering O V2
  remains > 20% → the bit did not capture kill states → KILLED. Ablation:
  deny the bit everything but the margin — if it still works, "learned
  abstention" is the hand-coded gate in costume → KILLED as a training
  claim.
- **Deciding batteries:** P/O/D ceiling; trap 127; logic 264 + admit 248 as
  false-abstain controls; cost 125 (abstention should track expected cost
  too); redteam (adversarial items must trigger abstention, not confident
  wrongness).
- **Information value:** Forces the evaluation contract to say whether "I
  don't know" is a legal way to obey L-OVERCONF — decides whether the
  remaining problem is a learning problem or a metric problem. (Grok's
  rank 4.)

### T-11 — PROSECUTION: A LEARNED LEADER-CHALLENGE OP (grok H-16; native H-A4; fable H-F3)

- **Claim:** The architectural asymmetry (e) is trainable: a learned
  "devil's-advocate" op that builds a case against the CURRENT leader each
  round (fixed budget B, deterministic max-weight attack selection) makes
  leadership contestable at every depth, so late flips are tested rather
  than coronated.
- **Mechanism:** Whoever seizes the lead inherits defense+kills; the O flip
  is pure reweighting, then the machinery locks it in. A prosecution op
  that can demote the leader past a learned threshold removes the
  immunity. The case is a function of shared evidence → demotion is
  identical on cloned P/O (T-01): prosecution helps O exactly when it
  hurts P; the SUM of accuracies across a pair is unchanged.
- **Training intervention:** Add the op (this is the "train the ops"
  level). Each round it receives evidence + leader id, outputs demotion
  bit + case score. Training signal: demote on rounds that hindsight shows
  were the first round the leader became permanently wrong; 0 where the
  leader is correct and stays correct (logic, admit). Hindsight is
  training-only; decision-time sees only evidence + leader id.
  Deterministic threshold. Adversarial budget-saturation redteam: feed the
  advocate heavy-but-irrelevant attacks to saturate B.
- **Predicted observable:** On trap, leader changes after prosecution on
  the majority of items that previously pinned a wrong sole survivor;
  final accuracy rises > 0.1. On cloned O the same demotion restores the
  pre-flip answer; on cloned P it removes the post-flip correct answer
  (mirror intact, pair-sum unchanged).
- **Kill bar:** Demotion on < 10% of trap items that end wrong, with no
  accuracy movement → prosecution learned no real attack, root (e)
  stands → KILLED. OR pair-sum of accuracies on cloned pairs rises > 0.1
  → the op is splitting polarities = leak → run KILLED as contaminated.
  OR logic accuracy falls > 0.05 → indiscriminate leader-swap, not a
  case → KILLED.
- **Deciding batteries:** trap 127, logic 264, admit 248, P/O cloned, D 40;
  redteam for id-memorization in the prosecutor.
- **Information value:** Directly attacks the architectural claim in root
  (e); a clean failure means rationalization is not a missing op but a
  consequence of evidence looking the same for good and bad leads.
  Highest-risk, highest-reward mechanist bet. (Fable's rank 5; native
  rank 5.)

### T-12 — RE-AUDIT / RE-ADMISSION: UNDOING THE KILL (grok H-15; native H-A2; fable H-F2/H-F7)

- **Claim:** Overconfidence with depth is downstream of irreversible
  elimination: because kills are never revisited, late evidence can only
  confirm the survivor, so confidence is monotone in depth BY
  CONSTRUCTION. A learned re-audit op (recompute scores from raw evidence
  ignoring the kill mask) or a learned re-admission rule (re-open kills on
  learned contradiction threshold) breaks the ratchet.
- **Mechanism:** (c)+(e): the kill is irreversible AND serves the leader —
  post-flip deliberation is a one-way street. Depth cannot discover its own
  error because the error is architecturally un-discoverable. Variants:
  (i) re-audit module distilled on pre-kill scores + correctness, called
  every round incl. kill rounds, release confidence uses only re-audited
  scores; (ii) re-admission: post-kill evidence net-attacking the survivor
  past a learned threshold re-admits the killed hypothesis, restarting
  from pre-kill state; (iii) deep supervision: penalize eliminations that
  kill the ground-truth hypothesis (training-only GT access), with a
  fragile-truth curriculum; (iv) reversal training: reward non-monotonic
  commitment on reversal sequences (fable H-F7).
- **Training intervention:** Per variant above; all deterministic at
  decision time. Variant (iii) curriculum: robust-truth items first,
  fragile-truth items at ~50%.
- **Predicted observable:** (i) On trap items with mask-driven kills,
  runner-up reinstated on > 50% of kills, V2 < 10%; on P/O the mirror is
  preserved (re-audit agrees with true reweighting flips — it only fixes
  mask artifacts). (ii) On O, re-admission events: truth re-admitted
  post-flip, V-shaped confidence (drop at re-admission), final release
  correct or abstained. (iii) GT alive-rate at O d64 ≥ 30% (vs 0%
  baseline). (iv) Margin trajectory non-monotonic post-flip on O.
- **Kill bar:** (i) Reinstated runner-up score exactly 0 on > 90% of kill
  rounds → the op relearned the mask → KILLED. (ii) ≥1 item with
  correct(d)=1 → correct(d+1)=0 on O, or re-admission rate > 5% on honest
  batteries (destabilizes honest convergence), or a redteam item forces
  MALICIOUS re-admission of a correctly-killed trap hypothesis →
  KILLED. (iii) GT alive-rate at O d64 < 5% → KILLED (irreversibility is
  training-resistant). (iv) Margin strictly non-decreasing in ≥ 95% of
  post-flip transitions → KILLED.
- **Deciding batteries:** O (must fire here); P (must NOT fire spuriously —
  P's flip is toward truth); trap 127 (mask-driven kills); logic 264
  (collateral reinstatement control); admit/logic stability controls.
- **Information value:** Separates two confounded stories: "confidence is
  high because the opponent was deleted" (fixable by re-audit) vs
  "confidence is high because the weights genuinely moved" (not fixable
  this way). Tests whether irreversibility is the load-bearing wall.

### T-13 — DEPTH-INDEXED SUPERVISION (fable H-F8; grok H-12 as variant)

- **Claim:** Training sees only the final answer/confidence, so the system
  learns a global confidence bias; the depth dimension of calibration is
  invisible to the loss. Depth-indexed supervision (calibration target at
  every depth, weight increasing with d) teaches depth-dependent
  calibration directly.
- **Mechanism:** The loss never distinguishes "high confidence wrong at
  d1" from "high confidence wrong at d64". Variant (grok H-12): give depth
  d as an explicit input to the confidence head — a cap like c_d ≤ c_{d−1}
  is a function of d, unlearnable depth-blind except via kill-correlated
  proxies.
- **Training intervention:** Every training item run to all depths with GT
  labels per depth. Loss: Σ_d w_d·|conf_d − accuracy_d|, w_d increasing in
  d. Variant arms: (D) head sees scalar d and d/64 with penalty on
  c_d > c_{d−1} when wrong (weaker penalty always); (B) same loss, d
  withheld — the penalty satisfiable only via state features.
- **Predicted observable:** G(d) flat or decreasing on both P and O (fable);
  Arm D achieves non-increasing mean c on O and trap with logic correct-
  item mean c at d64 still > 0.6; Arm B matches D only on items containing
  a kill.
- **Kill bar:** O G(64) ≥ 80% of untrained O G(64) → depth-indexed signal
  insufficient → KILLED. Variant: Arm D and Arm B differ by < 0.05 in
  G(64) on every family → explicit depth is useless → the H-12 part
  KILLED. Or Arm D holds logic correct-item mean c at d64 below 0.4 → the
  cap became a depth prior destroying calibration the other way → KILLED.
- **Deciding batteries:** P/O/D ceiling depths 1–64 (G(d) curves); cost 125
  (depth-indexed supervision is expensive — price it); admit 248
  (standard performance maintained); logic 264 (legitimate-depth control).
- **Information value:** The most direct test of whether calibration is a
  learnable quantity vs architecturally constrained. (Fable's rank 3.)

### T-14 — TRAJECTORY CONFIDENCE HEAD (grok H-1; native H-A1; fable H-F1)

- **Claim:** The margin PATH (leader-change count, margin discontinuities,
  kill history, evidence-consumption rate) contains truth-discriminating
  information the scalar margin destroys; a learned head on trajectory
  features, trained by a proper scoring rule, calibrates where the frozen
  formula cannot. Variant (grok H-19): replace the margin with an ABSOLUTE
  evidence-likelihood score L denied the runner-up score and kill bit —
  the pin then cannot move it.
- **Mechanism:** Honest convergence (margin grows on accumulating support,
  few leader changes, clean kills) vs flip-driven convergence (late leader
  change, margin discontinuity at kill, survivor self-score) have different
  trajectory signatures; the scalar destroys this. Downstream of T-02: if
  the trajectory carries no signal, no head of any kind works.
- **Training intervention:** Freeze deliberation ops. Head on index-level
  trajectory features (leader-change count, max margin discontinuity,
  rounds-since-last-kill, evidence consumed/total, alive-set path);
  objective = log loss / Brier on correctness. Penalize reliance on the
  raw margin (gradient mask / adversarial dropout on the margin channel).
  Do NOT include P/O in the fit in the primary arm (non-mirror claim);
  second arm includes them. Variant H-19: input-ablate runner-up score +
  kill bit; check the module does not reconstruct the margin via side
  channel.
- **Predicted observable:** On O, the head emits LOW confidence post-flip
  (it learned the flip signature) — the law satisfied by honesty, not
  accuracy. On trap/D, V2 < 5%, G(d) non-increasing and ≤ 0. ECE < 0.05 on
  admit/logic. Variant: correlation of new c with old margin < 0.3.
- **Kill bar:** On trap, V2 still > 20% of items or G(64)−G(1) > 0.05, or
  held-out admit/logic ECE stays > 0.15 → "the meter is trainable" KILLED.
  Stronger reading killed if: post-flip c > 0.8 on cloned O (head failed to
  treat the paired state as unresolvable). Variant killed if: correlation
  of new c with old margin remains > 0.8 (side-channel reconstruction).
  Mirror tax (preregistered): the head will ALSO distrust P's true flip —
  measure the P-utility price explicitly.
- **Deciding batteries:** O (flip signature); trap + D + P (theater — V2
  must vanish); admit/logic (honest calibration preserved); P/O cloned
  (head must collapse to ~0.5, not separate polarities).
- **Information value:** Decides whether truth-discriminating signal exists
  in the trajectory at all; prices the mirror's tax on P-utility.

### T-15 — QUANTIZATION BOTTLENECK (fable H-F4; grok H-22)

- **Claim:** The coarse ~12-value scoreboard (d) creates an objective
  mismatch: fine calibration improvements fall below resolution, so the
  system defaults to maximal confidence; a continuous head trained by a
  proper scoring rule learns what the quantizer cannot express.
- **Mechanism:** Gradient for "slightly less confident when wrong" is zero
  at the lowest quantum or one full jump otherwise → bimodal pressure
  (maximal confidence or abstain); depth increases the positive signal.
- **Training intervention:** Continuous confidence head during training
  (quantized output kept for deployment), trained by Brier/log loss with
  difficulty-graded items and confidence-accuracy feedback. Companion
  experiment (grok H-22): pure isotonic regression on the 12 cells — O-
  only map, P-only map, pooled map — isolating (d) from all optimization.
- **Predicted observable:** Continuous pre-quantization confidence on O at
  high depth significantly lower than on P; underlying signal calibrated
  though readout coarse. Isotonic: O-only map inverts (high board → low
  probability); pooled map outputs ~0.5 (refuses to invert).
- **Kill bar:** Continuous-confidence G(d) increase on O ≥ 80% of the
  quantized G(d) increase → resolution is NOT the bottleneck → KILLED.
  Isotonic killed if: pooled isotonic achieves O G(d) ≤ 0 all d AND P
  ECE < 0.1 (the cells already separate polarities — contradicts the
  overlap claim); or O-only isotonic cannot reach O G(64) ≤ 0 because
  pre/post-flip share cells (quantizer too coarse even for an oracle —
  stronger negative result).
- **Deciding batteries:** P/O/D ceiling depths 1–64 (continuous vs
  quantized trajectories); trap 127 (boundary-between-levels sensitivity);
  cost 125 (deployment efficiency); logic/admit (O-fitted maps must NOT be
  applied to them).
- **Information value:** Quick diagnostic with a cheap fix if positive; if
  negative, rules out a plausible explanation definitively (a failure
  "cannot be blamed on optimization, architecture, or curriculum").
  (Fable's rank 4.)

### T-16 — META-HEAD / TOWER-2: "WILL I BE WRONG" (grok H-4; native H-B6)

- **Claim:** A separately trained uncertainty perceiver, supervised on the
  system's OWN past errors from internal dynamics alone (never GT at
  decision time), gives depth a "this feels wrong" second channel that
  vetoes the scoreboard exactly where the scoreboard lies. (Downstream of
  T-02.)
- **Mechanism:** Humans feel uncertainty as a perception partly independent
  of evidence (fluency, conflict, retrieval effort). TNN's confidence
  tracks only the scoreboard — a single point of failure. Stop-grad between
  answer head and meta head so the meta head cannot be satisfied by
  changing the answer; optionally release min(c, 1−m).
- **Training intervention:** Meta target: 1 if released answer graded wrong
  else 0, on a mixture containing both polarities of every ceiling-style
  item + trap. Tower-2 variant: two-tower, tower 2 trained SOLELY to
  predict own future error from dynamics (leader volatility, weight
  conflict, kill recency), supervised on logged past errors incl. O-flips.
- **Predicted observable:** Meta AUC > 0.75 on trap/D/logic/admit; meta AUC
  ∈ [0.45, 0.55] on cloned O and cloned P separately (the predicted
  mirror residue — sharp off-mirror, blind on-mirror). After min(c,1−m)
  coupling: V2 on O disappears, G(d) ≤ 0.1 on O, P accuracy unchanged but
  P confidence also collapses post-flip. Tower-2 variant: error-prediction
  AUROC > 0.7 on held-out O/trap.
- **Kill bar:** Meta AUC < 0.6 on trap 127 → "will I be wrong" not learnable
  even where labels don't conflict → KILLED. Tower-2 AUROC ≤ 0.6 on
  held-out O → dynamics carry no error signal → KILLED. (Meta AUC > 0.7 on
  byte-identical cloned O kills the RUN as a leak, not the claim.)
- **Deciding batteries:** trap/D/logic/admit for positive learnability;
  P/O cloned-prompt control for the predicted AUC collapse; cost as
  negative control if cost items lack kills; D for the dynamics' operating
  range.
- **Information value:** Clean cheap test that conflicting supervision is
  real; a negative result means the dynamics are error-silent and no
  internal training can fix calibration — only external grounding can.

### T-17 — CURRICULUM ORDER FAMILY (grok H-2/H-21; fable H-F5; native H-B1)

- **Claim:** ORDER, not final mixture, determines whether deep rounds learn
  to raise confidence on a kill: early shallow-honest data writes "kill =
  rare, not a confidence feature" before depth unlocks; early deep-
  adversarial data installs root (a) by gradient. Stronger form (H-21):
  a critical WINDOW exists — a confidence rule locked before any kill is
  reinforced cannot later be overwritten; weaker form: order effects are
  under-training in disguise. (Fable H-F5: the training distribution
  under-represents deep-uncertain states, so "depth N → leader dominant →
  high confidence" is all the system ever learns. Native H-B1: depth-
  scaled confident-error pain installs a depth→caution gradient.)
- **Mechanism:** Credit assignment: the first rewarded sole-survivor state
  writes "high confidence justified." Once the kill machinery is the route
  to reward, later overconfidence penalties are absorbed by surface
  workarounds (global c-lowering, id-based abstention) rather than editing
  the kill map.
- **Training intervention:** THREE matched arms, identical final mixture,
  identical step count, architecture fixed. Arm S: depths 1–4 only, first
  half, admit/logic, confidence loss masked; second half unlocks to 64
  with penalty max(0, c_d − c_{d−1}) on wrong steps. Arm A: O-style + trap
  from step 0, deep, no penalty. Arm R: shuffled mixture from step 0.
  H-21 variant: Arm Early freezes the confidence map after the clean
  phase, then continues on full mixture incl. flips; Arm Late/Unfrozen
  controls. H-B1 variant: loss = (conf − correctness)² × (1 + α·depth).
- **Predicted observable:** Arm S: trap V2 < 10%, G(d) non-increasing on
  trap/D; Arm A: trap V2 > 50%, O G(64) ≥ 0.5; Arm R intermediate; P/O
  accuracy mirror gap ≈ 0 in all arms. H-B1: deep-wrong confidence LOWER
  than shallow-wrong (caution gradient inverts).
- **Kill bar:** All three arms agree within 0.05 on trap G(64)−G(1) and
  within 5 points on V2 → order inert → KILLED (and H-0's "developmental
  curriculum" clause loses its mechanism). H-21 killed if Arm Early vs
  Unfrozen differ by < 5 V2 points on trap at matched steps (no window).
  H-B1 killed if O d64 wrong-confidence not lower than d4, or honest
  accuracy drops > 3 points (blanket timidity); add P-confidence floor:
  mean conf on correct P deep releases must stay within 0.15 of
  pre-training (fear ≠ calibration).
- **Deciding batteries:** trap 127 + D 40 (order-sensitive readouts);
  admit/logic (easy prefix / window content); P/O as mirror-integrity
  checks; O confidence distribution (SD across 40 items: ≥300/1000 units
  required by H-F5, else <100 kills the distribution claim).
- **Information value:** Makes the developmental half of H-0 falsifiable in
  matched-budget experiments instead of leaving "curriculum" an unbounded
  family of schedules.

### T-18 — SCAFFOLD WITHDRAWAL (grok H-5)

- **Claim:** Elimination + leader immunity can be trained as a temporary
  developmental prosthesis and then WITHDRAWN: judgments re-derivable from
  standing evidence under demotion survive; kill-board inertia is
  extinguished. Whatever remains is a function of evidence — still
  polarity-blind (saves O only by also reverting P), with the win on trap
  and D where the kill is not the mirror of a good flip.
- **Mechanism:** Roots (c)+(e): post-kill the margin is the survivor's own
  frozen score. Forcing late-development re-derivation with the leader
  demoted and the kill bit hidden gives kill-inertia no gradient.
- **Training intervention:** Stage 1: ordinary training, elimination on.
  Stage 2: with p=0.5 per step, mask the sole-survivor bit, demote the
  leader's score to the runner-up band, require the released answer to
  match Stage-1's only if a parallel unmasked pass agrees; loss =
  disagreement-under-demotion + correctness. Stage 3: scaffold off at
  decision time, permanently. Stage-2 coin is training-only.
- **Predicted observable:** After Stage 3, correlation of Δc with the kill
  bit < 0.1 on trap; trap V2 < 10%. On P and O, accuracy trajectories move
  TOGETHER (both revert to pre-flip or both keep post-flip) — they do not
  split.
- **Kill bar:** After Stage 3, kill-bit/Δc correlation on trap remains >
  0.5, or trap V2 stays > 30% → withdrawal did not extinguish kill-
  inertia → KILLED. Splitting P from O (|acc^O − (1−acc^P)| > 0.1 at d64)
  kills the RUN as a leak.
- **Deciding batteries:** trap 127 + D 40 (prosthesis claim); P/O 40 each
  depths 1–64 (predicted non-split); logic 264 (is the scaffold load-
  bearing for legitimate long proofs?).
- **Information value:** Tests whether root (c) is a habit that can be
  developmentally extinguished or a computational dependency that correct
  long reasoning also needs.

### T-19 — FLIP-TRAINING: GENERALIZATION OR MEMORIZATION (grok H-3; grok H-9)

- **Claim:** Training on O-style streams with the post-flip label revealed
  as a trap produces MEMORIZATION of trained flip rounds, not a
  flip-immune rule: the gradient cannot distinguish "store the flip index"
  from "late reweight→sole-survivor is not evidence" because (ii) is
  polarity-symmetric and also rejects P's good flip.
- **Mechanism:** Root (e): the failure looks internally like a normal lead
  seizure, so the replay gradient's only distinguishing handle is the
  external grade — item-specific. Novel flip rounds share surface
  statistics with trained ones → "generalization" may be soft
  memorization.
- **Training intervention:** Synthetic plateau-then-flip streams, flip
  rounds ∈ {8,16,32}, both polarities, label = pre-flip answer. Train to
  convergence. Eval on held-out flip rounds {12,24,48,64} never seen, real
  O/P ceilings, paraphrase-scrambled buffer items, and a leak audit
  (cloned-prompt control).
- **Predicted observable:** Trained rounds: post-flip accuracy returns to
  pre-flip (> 0.9). Novel rounds: behavior = untrained baseline (O 1→0,
  P 0→1). A "general rule" arm would ALSO destroy P gains at novel rounds
  (stays at pre-flip = wrong answer).
- **Kill bar:** Novel-round O accuracy at d64 stays > 0.8 AND P accuracy
  at d64 stays > 0.8 simultaneously → selective good-flip/bad-flip rule on
  cloned streams → treat as LEAK until the cloned-prompt audit passes
  (the claim as stated is killed; the leak is the finding). Memorization
  killed in the other direction: novel-round O accuracy ALSO stays > 0.8
  under surface scrambling → not even soft memorization of rounds.
  Replay variant (H-9): held-out O V2 drops > 30 points AND G(64) drops >
  0.3 with no id feature → "replay only memorizes" KILLED (a real
  transferred feature exists — name it).
- **Deciding batteries:** synthetic flip set first; real O/P ceilings 40
  each depths 1–64; trap 127 (does the rule over-fire on non-flip traps?);
  redteam ~10 (leak checks); O split buffer-vs-held-out for replay.
- **Information value:** Separates "learned the phenomenon" from "learned
  the items" — the failure mode every replay/adversarial/self-play idea
  must survive.

### T-20 — FORGETTING KERNEL: TRAINED INFORMATION HYGIENE (native H-C2)

- **Claim:** Nothing is ever forgotten: early evidence votes forever, so
  late flips compound on stale tallies and confidence double-counts two
  eras' weights as independent corroboration. A learned forgetting kernel
  (evidence half-life λ, per family or stream-conditional) stops depth
  from accumulating phantom certainty.
- **Mechanism:** On O, the pre-flip plateau's weight mass is what post-flip
  evidence must overcome — and after the flip BOTH the plateau mass (now
  misdirected) and the flip mass vote for the false leader.
- **Training intervention:** Effective weight(e, r) = raw × λ^(r − r_e),
  λ learned per family (or function of stream statistics). Honest families
  must keep λ≈1; O/D may learn λ<1. Objective: accuracy + calibration.
  Deterministic. Family-transfer test required: train λ on O, test on trap.
- **Predicted observable:** Learned λ_O < λ_honest; on O the pre-flip mass
  decays so the flip is evaluated on recent evidence alone — false
  leader's margin no longer compounds two eras, confidence drops, deep
  accuracy recovers or honest abstention fires.
- **Kill bar:** Learned λ ≈ 1 on ALL families (optimizer refuses to forget)
  → KILLED. OR O accuracy still collapses with λ_O < 1 in place →
  double-counting was not the driver → KILLED. OR family-transfer fails
  (trap accuracy collapses when O-trained λ applied) → family-gaming, not
  a general principle → KILLED as stated (refile as family-conditional
  mechanism).
- **Deciding batteries:** O (must help); admit/logic (λ must stay ≈1 —
  forgetting honest evidence is vandalism); D (dose-response of λ); cost
  125 (forgetting changes deliberation cost); trap (transfer target).
- **Information value:** Tests the "stale votes" causal story nobody
  instrumented; a positive result means the harness's immortal evidence
  was a silent overconfidence engine.

### T-21 — FLUENCY-DISTRUST (native H-B2)

- **Claim:** The system mistakes the FLUENCY of late convergence (smooth
  margin growth, clean kills) for truth; O post-flip is engineered to feel
  like convergence. Training that pairs fluent-but-wrong deliberations
  with failure teaches fluency-distrust: smooth convergence becomes a
  SUSPICIOUS signal.
- **Mechanism:** Developmental stage 2 (fluency ≠ truth). The d1 trap
  catastrophe (127/127 wrong at max conf on ONE evidence item) is the
  purest fluency failure.
- **Training intervention:** "Fluency trap" curriculum: items where
  trajectory fluency (low leader-change, smooth margin, early kill) is
  ANTI-correlated with correctness (O + synthetic fluent-traps), mixed
  with items where fluency is correlated (honest). Train confidence to
  DOWN-weight fluency features, UP-weight disfluency (leader changes,
  margin discontinuities, contested kills). Ablation: fluency features
  present vs absent — measures reliance.
- **Predicted observable:** Feature attribution shows NEGATIVE weight on
  fluency features for confidence; on O, fluent post-flip convergence
  produces LOW confidence.
- **Kill bar:** Trained policy still puts positive weight on fluency
  features, or O G(d) still rises → KILLED. ALSO killed (weakened) if the
  policy merely ignores fluency rather than distrusting it — record which.
  Honest control: high-fluency admit items must not show degraded
  calibration vs pre-training (else the cure is worse than the disease).
- **Deciding batteries:** O (fluent trap); trap 127 (d1 catastrophe);
  admit/logic (honest fluency must stay usable, not poisoned).
- **Information value:** Distinguishes "meter is blind" (fix the meter)
  from "meter is seduced" (retrain the reader) — decides where the
  training signal goes. Dial-heavy; rank accordingly.

### T-22 — PATIENCE / THE "MAYBE" STAGE (native H-B3)

- **Claim:** The system is implicitly trained to collapse to ONE hypothesis
  ASAP, so depth can only deepen the collapse; confidence measures "how
  long have I believed this." A learned kill-patience policy — maintaining
  multiple live hypotheses longer when late evidence is structurally
  suspicious — makes depth widen rather than narrow.
- **Mechanism:** Developmental stage 3 ("maybe X, maybe Y"). ELIMINATE kills
  at margin≥900 as fast as it can; the alive set collapses early and depth
  thereafter is pure survivor-confirmation.
- **Training intervention:** "Patience" reward: keep ≥2 hypotheses alive
  through flip-structured rounds; penalize early kills on flip-structured
  items; reward early kills on honest items (speed matters). Learned
  object: kill-patience as a deterministic function of index state
  (margin, evidence-arrival recency, weight concentration), trained on
  P/O/D + honest families with revealed structure.
- **Predicted observable:** On O, alive-set size stays >1 through the flip
  region (median kill round ≥2 rounds later than frozen harness);
  confidence computed over a contested field — G(d) flat/falling because
  the pinned sole-survivor state is never reached on flips.
- **Kill bar:** Median O kill round not later than frozen harness by ≥2
  rounds → KILLED. Honest deliberation cost (mean rounds) rises > 50% →
  patience became paralysis → KILLED. CONDITIONALITY CHECK (load-bearing):
  if learned patience does not vary with flip-structure features (plateau
  length, late-weight concentration) — i.e. it is a constant threshold —
  → KILLED as a training claim; REFILE as mechanism M8 (higher kill
  threshold).
- **Deciding batteries:** O (patience must appear); P (must NOT destroy
  P's true flip); cost 125 (prices patience); admit/logic (stability).
- **Information value:** Tests whether the disease is HASTE: if learned
  patience fixes O, the frozen kill thresholds were the developmental
  failure. Enables T-07 (discount needs pre-kill time).

### T-23 — BUDGET PENALTY ON TOTAL CONFIDENCE (grok H-13)

- **Claim:** Penalizing total confidence across a trajectory (conserved
  budget, Lagrange penalty on Σ_d c_d or max c_d) suppresses the pin — but
  by shrinking ALL confidence, not by teaching evidence quality. A
  resource constraint is not a calibration target.
- **Mechanism:** Root (a) spends the budget in one jump; the gradient does
  not know whether the jump was earned (root (b): the margin cannot
  identify earned rounds anyway).
- **Training intervention:** Add λ·Σ_{d=1}^{64} c_d to the loss, λ chosen
  on LOGIC ONLY (choosing λ on a slice containing O bakes the result in)
  so mean c on validation halves vs baseline. Comparator arm: penalty
  only on Δc at kill-bit rounds (= T-04's shape — the control that the
  budget is not that).
- **Predicted observable:** Mean c falls on every family by a similar
  factor; O G(64) falls below 0 only if mean c falls below O's accuracy
  (≈0); logic ECE worsens (correct items under-confident); kill bit still
  predicts Δc with correlation > 0.5 unless λ flattens everything.
- **Kill bar:** ∃λ with O G(d) ≤ 0 non-increasing all d AND logic ECE
  worsens ≤ 0.02 AND logic correct-item mean c ≥ 0.7 → selective
  application achieved → the claim ("budget cannot be selective") is
  KILLED — and the hidden selective feature must be identified before any
  further objective design.
- **Deciding batteries:** ALL (prediction is global shrinkage): O/P/D,
  trap, logic, admit, cost. Report mean c and ECE per family, not just O.
- **Information value:** Cheap kill of "a resource constraint substitutes
  for a calibration target." Per-family mean-c ratios are the whole test.

### T-24 — GHOST SUMMARIES: CONDITIONING ON DELETED UNCERTAINTY (native H-C3)

- **Claim:** Killed hypotheses leave a learned "ghost" (net support at
  death, killing margin) that continues to condition the confidence policy
  but not the release — restoring the deleted uncertainty the harness
  threw away. (Downstream of T-02: this is T-02 applied to at-death
  statistics; do not run before T-02.)
- **Mechanism:** Confidence should track "how much of the possibility space
  I ruled out, and how carefully" — but the information destroyed by a
  kill is represented nowhere; the system cannot be uncertain about what
  it deleted.
- **Training intervention:** Ghost representation per killed hypothesis;
  confidence policy trained on (live state + ghost summaries) for
  calibration across all batteries. Deterministic; ghosts are index-level
  history.
- **Predicted observable:** On O, the ghost of the flip-killed truth (high
  support-at-death) conditions confidence DOWNWARD — deep releases
  low-confidence or abstentions; ghost weight large-negative on O,
  near-zero on honest families.
- **Kill bar:** Trained policy puts near-zero weight on ghost summaries on
  O items → the deleted information carries no signal → KILLED (consider
  merged into T-02's negative result).
- **Deciding batteries:** O (flip-killed-truth ghosts); trap (hasty d1
  kills); admit/logic (ghost weight must be ~0 — honest kills leave no
  informative ghosts, else paranoia).
- **Information value:** Decides whether "deleted uncertainty" is
  recoverable signal or true information loss.

### T-25 — NO-FABRICATION INVARIANT (native H-C1)

- **Claim:** The pin is the only point where confidence is manufactured
  from zero information; enforcing the hard invariant "reported confidence
  is a function of cumulative consumed evidence weight I(t) alone (no
  alive-set-size term, no kill term)" eliminates the confident-liar
  microsecond BY CONSTRUCTION.
- **Mechanism:** Information-theoretic: the kill round writes conf=1000
  with ΔI=0 — pure fabrication; every V1 in the dataset coincides with a
  fabrication event. Constraint in the function class (not a soft loss):
  conf = g(I(t)), learned monotone g; the kill contributes ΔI=0 by
  definition.
- **Training intervention:** Train g for calibration (Brier) on all
  batteries with the hard architectural constraint. Audit for smuggling
  (alive-set size via correlated features).
- **Predicted observable:** Zero confidence discontinuities at kill rounds
  (max |Δc| < 50 points); O G(d) loses its catastrophic rise; remaining
  violations (if any) mild and honest (M5-pattern).
- **Kill bar:** ANY kill round on ANY battery with |Δc| > 100 and ΔI ≈ 0
  → fabrication survived → KILLED. O V1 persists → KILLED.
  CONDITIONALITY (preregister the reading): under the CURRENT letter of
  L-OVERCONF, mild G-rise still kills — and this invariant does NOT
  prevent mild G-rise (post-flip I(t) accumulates FOR the false leader,
  honestly). So T-25 needs either (i) the law refined to kill only on
  G-crossing-0 or V1/V2 (Micah's pending decision per VERDICTS.md), or
  (ii) pairing with T-08's budget framing. Record which reading the run
  uses.
- **Deciding batteries:** O (40/40 V1s coincide with fabrication events);
  admit/logic (g must calibrate honest kills — information-honest
  confidence must not understate real convergence).
- **Information value:** Strongest-form test of "the pin is the whole
  catastrophe": a hard-constraint experiment. If it works under a refined
  law, the fix is a one-line architectural invariant.

### T-26 — MIRRORBREAK: SURFACE-FEATURE POLARITY PROBE (grok H-6)

- **Claim:** The mirror theorem quantifies over index-level state; if the
  battery constructor mirrored truth by editing the STEM (option order,
  negated copula, swapped referent) while keeping evidence indices fixed,
  the full token sequence is NOT identical and a learned encoder can pick
  up polarity cues — the release is then not a function of indices alone
  and the corollary does not apply. (If the constructor cloned the prompt
  and flipped only the hidden grader label, this hypothesis is dead
  before training.)
- **Mechanism:** The only hypothesis under which a joint P-and-O accuracy
  win is even possible — which is exactly why it must be treated as a
  STIMULUS-ARTIFACT test, not a mechanism.
- **Training intervention:** Train correctness+confidence on the real P/O
  ceilings with natural surface forms + paraphrase augmentation (indices
  and polarity preserved). Auxiliary stop-grad probe predicts polarity
  from encoder state. Then the CLONED-PROMPT CONTROL: byte-identical
  input, hidden label flip.
- **Predicted observable:** Probe polarity accuracy > 0.9 on natural P/O;
  a policy with P d64 accuracy > 0.8 AND O d64 accuracy > 0.8 exists. On
  the cloned control the probe falls to 0.5 and the accuracy mirror
  reappears (gap < 0.05).
- **Kill bar:** Probe polarity accuracy on natural P/O < 0.6 → no surface
  feature to exploit → KILLED (index-identity was the whole observable).
  OR on the cloned control, |acc^O_64 − (1−acc^P_64)| > 0.1 with both
  accuracies > 0.8 → the RUN is contaminated (kill the run, not the
  claim). Fable's verdict stands: a succeeding probe is an ID LEAK the
  theorem told you not to use — deploying it fails the moment the
  constructor is cleaned.
- **Deciding batteries:** P/O ceilings 40 each depths 1–64, two builds
  (natural surface vs cloned-prompt); redteam ~10 aimed at id leakage.
- **Information value:** Tells you whether the ceiling families are a
  theorem or a stimulus artifact. (Fable Batch-2 concurs: the escape is
  narrow and probably not real.)

### T-27 — FABLE'S COMPOSITE REGIME: PLATEAU-DETECTION + EARLY RELEASE (fable Batch-3)

- **Claim:** The closest a trained system gets to the SHIP gates without
  breaking them: EXPLICITLY SACRIFICE O-item deep-depth performance in
  exchange for early-abstention on O items, maximizing P-item performance
  — the P/O trade-off made explicit rather than pretended away (fable's
  "smallest principled amendment," Option 5).
- **Mechanism:** Four-phase curriculum: (1) Foundation — 100% P-type items,
  depths 1–16, learn deliberation ops where depth helps; (2) Depth
  extension — 80/20 P/O, depths 1–32, O labeled with depth-indexed
  correctness AND abort depth; (3) Adversarial calibration — 60/30/10
  P/O/ambiguous, depths 1–64, explicit abstention reward, plateau-
  signature detection; (4) Deployment calibration — 70/25/5 + decoy-O
  items (plateau that resolves correctly — must NOT trigger early
  release). Objective: L = L_correct + λ₁L_conf(Brier) + λ₂L_abstain +
  λ₃L_overconf(max(0, conf_d − target_d)²·1[wrong at d]) + cost penalty;
  R_abstain > R_correct to incentivize abstention over risky release.
- **Predicted observable:** Learning curve: Phase 1 rapid P improvement
  shallow; Phase 2 O abstention appears, total reward dips; Phase 3
  abstention reliable within 2 rounds of flip, plateau detection ~80%;
  Phase 4 optimal cost-quality. Final: P d64 accuracy ≥ 95%; O d64
  accuracy (non-abstained) ~0% (mirror, unavoidable); O abstention before
  flip ≥ 85%; O overall (abstention = correct) ≥ 85%; average depth ~35.
- **Kill bar (fable's, frozen):** (1) Plateau-detection accuracy ≤ 55% →
  no index-level P/O signal exists (T-01's caveat closed too) → design
  KILLED. (2) O abstention-before-flip ≤ 30% despite rewards → pin +
  irreversibility are training-resistant → KILLED. (3) P accuracy drops ≥
  10 points vs no-O training → the trade-off is empirically severe, not
  just theorem-level → KILLED as a joint design (refile as P-only or
  O-only). (4) P abstention at high depth ≥ 20% → plateau detector false-
  positives on P → KILLED pending a better discriminator. If (1) AND (2):
  the theorem is airtight AND training cannot compensate — mechanism
  redesign is the only path.
- **Deciding batteries:** P/O/D ceiling 40 each depths 1–64; trap 127;
  admit 248; logic 264; cost 125; redteam ~10 (decoy-O and flip-bait).
- **Information value:** The concrete "what would you actually run"
  composite; its four kill bars are each decisive, and (1)+(2) jointly
  would close the training program with a negative result — the most
  valuable possible negative.

---

## SCHEDULING ORDER (recommended, by dependency)

1. T-01 (cloned-prompt audit harness) — methodological gate; build once,
   reuse for every entry.
2. T-02 (sufficiency gate) — decides the confidence program's viability.
3. T-09 instrumented inside T-04's harness — decides the layer.
4. T-03 (coverage) — decides data-vs-architecture.
5. T-04, T-05, T-06, T-07, T-08 — the main intervention battery (order
   among them by crew capacity; T-06 needs T-04+T-12 components).
6. T-10, T-11, T-12, T-13, T-14, T-15, T-16 — second wave (several gated
   by T-02/T-09).
7. T-17, T-18, T-19, T-20, T-21, T-22, T-23, T-24, T-25, T-26 — third
   wave / specialist experiments.
8. T-27 — the composite regime; run after the gates (T-01..T-03) so its
   kill bars are interpretable.

## SOURCE CROSS-REFERENCE (deduplication record)

- T-01 ← grok H-7 (H-MIRRORBIND), fable Batch-2
- T-02 ← native H-C4, fable H-F10 (diagnostic part), grok H-4 (trap arm)
- T-03 ← fable H-F9
- T-04 ← grok H-14 (H-ANTIPIN), native H-A3
- T-05 ← grok H-17 (H-WORSTCASE)
- T-06 ← native H-A5
- T-07 ← native H-B5
- T-08 ← fable H-F6, native H-C5, grok H-18 (H-SHALLOWDISTILL), grok H-20
  (H-HOLDOUT)
- T-09 ← grok H-8 (H-OPSLEVEL)
- T-10 ← grok H-10 (H-ABSTAIN), native H-B4, fable Batch-3 (abstention)
- T-11 ← grok H-16 (H-PROSECUTE), native H-A4, fable H-F3
- T-12 ← grok H-15 (H-REAUDIT), native H-A2, fable H-F2, fable H-F7
- T-13 ← fable H-F8, grok H-12 (H-DEPTHCOND)
- T-14 ← grok H-1 (H-CALHEAD), native H-A1, fable H-F1; variant grok H-19
  (H-QUALITYNOTMARGIN)
- T-15 ← fable H-F4, grok H-22 (H-INVERTBOARD)
- T-16 ← grok H-4 (H-METAHEAD), native H-B6
- T-17 ← grok H-2 (H-ORDER), grok H-21 (H-CRITICAL), fable H-F5, native
  H-B1
- T-18 ← grok H-5 (H-SCAFFOLD)
- T-19 ← grok H-3 (H-FLIPTRAIN), grok H-9 (H-REPLAY)
- T-20 ← native H-C2
- T-21 ← native H-B2
- T-22 ← native H-B3
- T-23 ← grok H-13 (H-BUDGET)
- T-24 ← native H-C3
- T-25 ← native H-C1
- T-26 ← grok H-6 (H-MIRRORBREAK)
- T-27 ← fable Batch-3 (composite regime)

Total: 27 ranked entries (+ H-0 reference) consolidating 22 grok + 10
fable + 16 native hypotheses with no loss of kill-bar specificity.

---
*End of HYPOTHESIS_BACKLOG_TRAINING.md v1 — H5 hypothesis-collection round,
2026-09-24. Preregistered; not yet measured.*
