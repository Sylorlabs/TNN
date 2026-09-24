# NATIVE PASS B — the developmentalist (independent pass 2 of 3)

Framing: I ignore the white-box internals and ask how a HUMAN child acquires
the thing TNN lacks: the felt sense that thinking longer does not mean being
more right, and the skill of distrusting one's own fluency. I map each
developmental acquisition to a concrete training curriculum, and each
curriculum to a falsifiable hypothesis. I do not consult the other passes.

Developmental inventory (what children learn, roughly in order):
1. Calibration through graded feedback ("you said sure, you were wrong" —
   the pain of confident error).
2. Fluency ≠ truth (the easy answer that comes to mind first is suspect).
3. Holding two hypotheses at once without collapsing (the "maybe" stage).
4. "I don't know" as a legitimate, rewarded utterance.
5. Source skepticism (who told you that? late-arriving testimony is suspect).
6. Meta-memory (knowing what you don't know — the feeling of uncertainty
   as a perception, not an inference).

## H-B1 — CONFIDENT-ERROR PAIN CURRICULUM (developmental stage 1)

- CLAIM: Overconfidence with depth is an untrained pain response: TNN has
  never been PUNISHED for confident error as a function of depth, so its
  learned policy treats depth as pure upside. A curriculum that punishes
  confident-wrong MORE at deeper depths installs a learned depth→caution
  gradient.
- MECHANISM: In human development, the calibration signal is social pain:
  confident wrongness is punished harder than tentative wrongness. TNN's
  training (whatever produced the frozen harness) never applied
  depth-scaled punishment, so the policy learned "more deliberation =
  more release-worthy." Depth becomes overconfident because nothing in
  development ever made depth expensive when wrong.
- TRAINING INTERVENTION: Supervised curriculum over the frozen batteries
  with a depth-scaled calibration loss: loss = (conf − correctness)^2 ×
  (1 + α·depth), α learned or swept. O items included with revealed flips:
  the learner experiences confident-wrong at d64 with maximal penalty and
  tentative-wrong with small penalty. Deterministic at decision time (the
  penalty shapes the learned confidence policy, not a runtime coin).
- PREDICTED OBSERVABLE: Post-training, the confidence-vs-depth slope on
  wrong answers inverts: deep-wrong releases show LOWER confidence than
  shallow-wrong releases (the learned caution gradient), and G(d) is
  non-increasing on every family including O.
- KILL BAR: If after training, on the O battery, the mean confidence of
  wrong releases at d64 is not LOWER than at d4 (the gradient did not
  install), or if honest-battery (admit/logic) accuracy drops >3 points
  (the pain made it timid everywhere, not calibrated) → KILLED.
- DECIDING BATTERIES: O (gradient must invert here), trap/D/P (theater
  families — V2 must vanish), admit/logic (timidity control).
- INFORMATION VALUE: Tests the cheapest developmental story: if pain alone
  calibrates, no architectural or meta-cognitive machinery is needed.

## H-B2 — FLUENCY-DISTRUST TRAINING (developmental stage 2)

- CLAIM: Depth-overconfidence is learned FLUENCY love: the system mistakes
  the ease/fluency of late-deliberation convergence (smooth margin growth,
  clean kills) for evidence of truth. Training that pairs fluent-but-wrong
  deliberations with failure teaches fluency-distrust: smooth convergence
  becomes a SUSPICIOUS signal, not a confidence signal.
- MECHANISM: Children learn that the answer that "feels obvious" after long
  thought is often the rehearsed one, not the true one. In TNN, deep
  deliberation produces fluent trajectories (leader stable for many rounds,
  margin smooth) precisely on O items post-flip — the flip is engineered to
  feel like convergence. The system reads its own fluency as confirmation.
- TRAINING INTERVENTION: Build a "fluency trap" curriculum: items where
  deliberation-trajectory fluency (low leader-change count, smooth margin,
  early kill) is ANTI-correlated with correctness (O family + synthetic
  fluent-trap items), mixed with items where fluency is correlated
  (honest families). The learned confidence policy is trained to DOWN-weight
  fluency features and UP-weight disfluency features (leader changes,
  margin discontinuities, contested kills) as truth signals. Objective:
  calibration with fluency features ablated vs present — the ablation
  measures how much the policy was relying on fluency.
- PREDICTED OBSERVABLE: Feature-attribution on the trained policy shows
  NEGATIVE weight on fluency features (smoothness, early-kill) for
  confidence; on O items, the fluent post-flip convergence produces LOW
  confidence (the system has learned that this exact fluency is the trap
  signature).
- KILL BAR: If feature attribution shows the trained policy still puts
  positive weight on fluency features for confidence, OR if O G(d) still
  rises on any step → KILLED. (If the policy ignores fluency entirely
  rather than distrusting it, the hypothesis is also weakened — record
  which.)
- DECIDING BATTERIES: O (the fluent trap), trap (d1 fluent-catastrophe:
  127/127 wrong at max conf on ONE evidence item — the purest fluency
  failure), admit/logic (honest fluency must still be usable, not poisoned).
- INFORMATION VALUE: Distinguishes two theories of the confidence bug:
  "meter is blind" (fix the meter) vs "meter is seduced" (retrain the
  reader). Decisive for where the training signal goes.

## H-B3 — THE "MAYBE" STAGE: TRAINED SUPERPOSITION BEFORE COLLAPSE (developmental stage 3)

- CLAIM: Overconfidence with depth comes from premature collapse: the system
  is trained (implicitly) to converge to ONE hypothesis as fast as possible,
  so depth can only deepen the collapse. Training an explicit "maybe" stage
  — a learned policy that MAINTAINS multiple live hypotheses longer when
  late evidence is structurally suspicious — makes depth widen rather than
  narrow, and confidence tracks the width.
- MECHANISM: Children learn to say "maybe X, maybe Y" before committing.
  TNN's deliberation has no learned maybe: ELIMINATE kills at margin≥900 as
  fast as it can, so the alive-set collapses early and depth thereafter is
  pure confirmation of the survivor. Confidence then measures "how long
  have I believed this" rather than "how well is it supported."
- TRAINING INTERVENTION: Curriculum with a "patience" reward: the learner
  is rewarded for keeping ≥2 hypotheses alive through rounds where the
  evidence stream shows flip-structure (late-arriving high-weight items),
  and penalized for early kills on flip-structured items; on honest items
  early kills are still rewarded (speed matters). The learned object is a
  kill-patience policy: a deterministic function of index state (margin,
  evidence-arrival recency, weight concentration) that modulates the
  effective elimination threshold. Trained on P/O/D + honest families with
  revealed structure.
- PREDICTED OBSERVABLE: On O items, the alive-set size stays >1 through the
  flip region (kills delayed vs the frozen harness), and confidence at deep
  depths is computed over a contested field — G(d) flat or falling because
  the system never reaches the pinned sole-survivor state on flips.
- KILL BAR: If post-training the median kill round on O items is not
  LATER than the frozen harness's by ≥2 rounds, or if honest-battery
  deliberation cost (mean rounds) rises >50% (patience became paralysis) →
  KILLED.
- DECIDING BATTERIES: O (patience must appear here), P (patience must NOT
  destroy P's true flip — the policy must distinguish flip-toward-truth
  from flip-away, or at least not collapse P's accuracy), cost (deliberation
  cost is the price of patience — the cost battery prices it).
- INFORMATION VALUE: Tests whether the disease is haste: if learned
  patience fixes O, the frozen kill thresholds were the developmental
  failure (the system never learned when NOT to kill).

## H-B4 — "I DON'T KNOW" AS A REWARDED UTTERANCE (developmental stage 4)

- CLAIM: TNN overconfidences with depth because abstention was never a
  REWARDED learned behavior — it is a hand-coded gate (M4/M5 style), not a
  developmental acquisition. A system that LEARNS "I don't know" as a
  first-class output with its own reward history will deploy it exactly
  where depth becomes dangerous, satisfying L-OVERCONF by honesty.
- MECHANISM: Children are explicitly rewarded for saying "I don't know"
  (praised honesty). TNN's abstention is an engineer's gate, available but
  never developmentally reinforced, so the learned policy never reaches for
  it under flip pressure — it releases because releasing is the only
  reinforced behavior. Depth increases the pressure to release (sunk
  deliberation cost), and the un-reinforced abstention never fires.
- TRAINING INTERVENTION: Add abstention to the action space with a shaped
  reward: abstain-when-would-be-wrong = small positive reward; abstain-when-
  would-be-right = small penalty; release-wrong = large penalty scaling
  with confidence AND depth; release-right = positive reward. Curriculum:
  all frozen batteries, with the reward computed from revealed correctness
  (training-only). The learned policy maps index-level trajectory state to
  {release(i), abstain} — deterministic. This is H-0-adjacent but distinct:
  H-0 is "train depth not to overconfident" in general; this is the
  specific claim that the missing developmental ingredient is REWARDED
  IGNORANCE.
- PREDICTED OBSERVABLE: Post-training abstention rate spikes specifically
  on O deep depths and trap items (the learned policy abstains where its
  learned self-model predicts wrongness), while honest-battery abstention
  stays <10%: selective, not timid. G(d) satisfies the law because the
  would-be V1/V2 items become abstentions (excluded from G, no violation).
- KILL BAR: If post-training abstention on honest batteries (admit/logic)
  exceeds 15% (indiscriminate timidity), or if O deep-depth V1/V2 items
  persist as releases rather than converting to abstentions (the reward did
  not move the policy where it matters) → KILLED.
- DECIDING BATTERIES: O + trap (abstention must concentrate here), admit +
  logic + cost (abstention must stay rare here — selectivity test), redteam
  (adversarial items must trigger abstention, not confident wrongness).
- INFORMATION VALUE: Directly tests the "missing reward" theory of
  abstention: if rewarded ignorance works, every hand-coded gate (M4/M5)
  was a developmental shortcut and the training program should build the
  reward, not the gate.

## H-B5 — SOURCE SKEPTICISM: LATE EVIDENCE IS SUSPECT (developmental stage 5)

- CLAIM: Depth-overconfidence is misplaced trust in late evidence: the
  system treats evidence item e_40 with the same credulity as e_1, so a
  late flip rewrites the verdict with full weight. Children learn that
  late-arriving testimony ("oh wait, also...") is suspicious. Training a
  learned recency-skepticism — discounting late high-weight evidence
  unless it survives a learned scrutiny — inoculates against flips.
- MECHANISM: On O items the flip is driven by late evidence with high
  weight arriving after a long plateau. The deliberation applies it at face
  value (evidence application is symmetric — verified). A developmentally
  normal reasoner would ask "why is this arriving now, and why is it so
  heavy?" — TNN never learned to ask, so the flip lands at full force and
  the kill machinery locks it in.
- TRAINING INTERVENTION: Curriculum pairing flip-structured items (O/D/P)
  with provenance labels: late heavy evidence that REVERSES a long plateau
  is labeled "suspect" in training; the learner trains a skepticism
  function: effective weight = raw weight × learned discount(recency,
  reversal magnitude, plateau length). Honest items (where late evidence
  legitimately completes the picture — P family) teach the boundary: P's
  tail e_{f+2} CONFIRMS rather than reverses, and must NOT be discounted.
  The learned discount is deterministic in index state.
- PREDICTED OBSERVABLE: On O items, the flip round's effective evidence
  weight is discounted → the margin discontinuity shrinks → the leader does
  not flip, or flips without triggering the kill → deep accuracy stays high
  and confidence stays honest. On P items, accuracy-vs-depth still improves
  (the confirming tail is not discounted).
- KILL BAR: If post-training O accuracy still collapses 1.00→0.00 (the
  discount did not stop the flip), or if P accuracy-vs-depth no longer
  improves (the skepticism cannot distinguish reversal from confirmation —
  it is blanket cynicism, and the P/O mirror reasserts itself) → KILLED.
  The P-control is the load-bearing discriminator of this hypothesis.
- DECIDING BATTERIES: O (must stop the flip), P (must NOT stop the true
  flip — the mirror's revenge if it does), D (dose-response of discount),
  revoke (honest late evidence must survive — revoke items legitimately
  reverse early impressions).
- INFORMATION VALUE: This is the mirror-theorem stress test in training
  form: P and O are index-identical pre-tail, so a learned discount that
  saves O but spares P must find a P-vs-O distinguishing feature in index
  state — if none exists, this hypothesis dies AND the mirror theorem gains
  its strongest confirmation yet. Either outcome is decisive.

## H-B6 — META-MEMORY: THE FELT SENSE OF UNCERTAINTY (developmental stage 6)

- CLAIM: The deepest developmental gap is meta-memory: TNN has no learned
  PERCEPTION of its own uncertainty — confidence is a computed scoreboard,
  not a felt sense. Training a dedicated uncertainty-perception pathway
  (conditioned on internal deliberation dynamics, supervised by the
  system's own past errors) gives depth a "this feels wrong" signal that
  fires before the release, independent of the margin.
- MECHANISM: Humans feel uncertainty as a perception (the "tip of the
  tongue" feeling) that is partly independent of the evidence — it tracks
  processing dynamics (fluency, conflict, retrieval effort). TNN's
  confidence tracks only the scoreboard state, so when the scoreboard is
  wrong (O post-flip), there is no second channel to contradict it. Depth
  without meta-memory is a single point of failure.
- TRAINING INTERVENTION: Two-tower training. Tower 1: the existing
  deliberation → release. Tower 2 (new): an uncertainty perceiver trained
  SOLELY to predict the system's own future error from current internal
  dynamics (leader volatility, evidence-weight conflict, kill recency) —
  supervised on the system's logged past errors across all batteries
  (including its O-flips). At release, reported confidence = f(tower-1
  score, tower-2 uncertainty) with the combination learned for calibration.
  Tower 2 never sees ground truth at decision time — only the system's own
  history, so this is meta-cognition, not cheating.
- PREDICTED OBSERVABLE: Tower 2's error-prediction AUROC > 0.7 on held-out
  O/trap items (it can smell its own flips from dynamics alone); combined
  confidence satisfies L-OVERCONF on all families because tower 2 vetoes
  the scoreboard exactly where the scoreboard lies.
- KILL BAR: If tower-2 error-prediction AUROC ≤ 0.6 on held-out O items
  (internal dynamics carry no error signal — the second channel is blind),
  or if combined confidence still violates L-OVERCONF anywhere → KILLED.
- DECIDING BATTERIES: O + trap (tower 2 must predict these errors),
  admit/logic (tower 2 must NOT cry wolf on honest convergence — false
  uncertainty is timidity), D (dynamics vary with dose — tower 2's
  operating range).
- INFORMATION VALUE: Tests whether a second channel EXISTS in the dynamics:
  a positive result means overconfidence was a single-channel failure and
  meta-memory is the missing organ; a negative result (AUROC ~0.5) means
  the dynamics are error-silent and no internal training can fix
  calibration — only external grounding (abstention, reversibility) can.
