# NATIVE PASS A — the mechanist (independent pass 1 of 3)

Framing: I take the five instrumentally-confirmed white-box root causes as the
complete causal inventory of depth-overconfidence and ask, for each one: what
would a TRAINING/LEARNING process have to install in the system so that this
root cause stops producing overconfidence with depth? Each root cause becomes
at least one training hypothesis. I do not consult the other passes.

Root causes (verified):
(a) sole-survivor confidence pin at 1000 BY CODE at the elimination round;
(b) margin = distance-to-runner-up, distributions overlap for correct/wrong —
    the meter cannot discriminate truth at any magnitude;
(c) elimination irreversible, margin never re-audited;
(d) confidence is a coarse ~12-value quantized scoreboard never calibrated
    to correctness; confidence theater (rising while wrong) on trap/D/P;
(e) rationalization is architectural: whoever seizes the lead inherits the
    defense+kill machinery; no op attacks the leader; O-flip = pure
    reweighting then irreversible kill.

## H-A1 — TRAINED CONFIDENCE HEAD (root cause b + d)

- CLAIM: The margin-to-confidence mapping is the trainable locus: a learned
  confidence head conditioned on the full deliberation trajectory
  (margin path, leader-change count, evidence-consumption rate, kill
  history) can be calibrated where the frozen margin formula cannot, because
  the trajectory contains truth-discriminating information the scalar margin
  destroys.
- MECHANISM: Depth overconfidences because confidence is a monotone function
  of a truth-blind scalar (margin). But the margin PATH differs between
  honest convergence (margin grows on accumulating support, few leader
  changes, kills of low-weight rivals) and flip-driven convergence (late
  leader change, margin discontinuity at the kill round, survivor score
  replacing a two-sided margin). The scalar destroys this; the trajectory
  preserves it.
- TRAINING INTERVENTION: Freeze the deliberation ops. Train a confidence
  head (deterministic function of index-level trajectory features:
  leader-change count, max margin discontinuity, rounds-since-last-kill,
  evidence consumed/total, alive-set size path) on a calibration curriculum:
  honest batteries (admit/revoke/logic/cost) + trap + P/O/D ceiling with
  revealed correctness labels, objective = minimize |head − correctness|
  (Brier-style, deterministic). The head REPLACES hist_c/st.conf at release.
- PREDICTED OBSERVABLE: On O items, the head outputs LOW confidence at deep
  depths post-flip (it has learned the flip signature: late leader change +
  margin discontinuity), so G(d) stays non-increasing and V1/V2 vanish even
  though the released index is still wrong — the law is satisfied by honesty,
  not by accuracy.
- KILL BAR: After training, if on the O battery G(d+1) > G(d) on ANY step
  d→d+1, or ≥1 V1/V2 violation on any battery → KILLED. Also killed if the
  head's Brier score on held-out trap items is not better than the frozen
  margin mapping's by ≥0.05 (then the trajectory carries no extra signal).
- DECIDING BATTERIES: O (the flip signature lives here), trap + D + P (the
  theater families — head must kill V2 there), admit/logic (must not destroy
  honest calibration).
- INFORMATION VALUE: Decides whether truth-discriminating signal exists in
  the trajectory at all — if not, no learned confidence of any kind can
  work and the only honest outputs are abstentions.

## H-A2 — REVERSIBLE-ELIMINATION TRAINING (root cause c)

- CLAIM: Overconfidence with depth is downstream of irreversible elimination:
  because kills can never be revisited, late evidence can only confirm the
  survivor, so confidence is monotone in depth by construction. Training the
  system to RE-OPEN kills when late evidence contradicts them breaks the
  depth→confidence ratchet.
- MECHANISM: (c) + (e): the kill is irreversible AND the kill machinery
  serves the leader, so post-flip deliberation is a one-way street: every
  round can only add support to the false leader or kill its rivals. Depth
  therefore cannot discover its own error — the error is architecturally
  un-discoverable, and confidence accumulates over a frozen kill-board.
- TRAINING INTERVENTION: Developmental curriculum in two phases. Phase 1
  (honest): standard deliberation, kills final. Phase 2 (flip-aware): the
  learner is trained with a "re-admission" operation — when post-kill
  evidence net-attacks the survivor beyond a learned threshold, the killed
  hypothesis is re-admitted and deliberation restarts from the pre-kill
  state (deterministic rule, learned threshold). Trained on P/O/D ceiling
  items with the flip structure revealed: reward = final correctness,
  penalty = confident wrong release. The learned object is the re-admission
  threshold + the contradiction detector over index state.
- PREDICTED OBSERVABLE: On O items, deep-depth runs show re-admission
  events: the truth is re-admitted post-flip, confidence DROPS at the
  re-admission round (V-shaped confidence curve), and the final release is
  either correct or abstained — G(d) non-increasing because confidence is
  no longer monotone in depth.
- KILL BAR: If after training, on the O battery, ≥1 item shows correct(d)=1
  → correct(d+1)=0 (the re-admission fires too late or not at all), or the
  re-admission rate on honest batteries (admit/logic) exceeds 5% of items
  (it destabilizes honest convergence) → KILLED.
- DECIDING BATTERIES: O (re-admission must fire here), P (must NOT fire
  spuriously — P's flip is toward truth; re-admitting there would be
  anti-learning), admit/logic (stability control).
- INFORMATION VALUE: Tests whether irreversibility is the load-bearing wall:
  if learned reversibility fixes O without breaking honest families, (c) is
  the root cause and the fix is architectural-training, not a release gate.

## H-A3 — DE-PIN TRAINING: EVIDENCE-GROUNDED CONFIDENCE (root cause a)

- CLAIM: The sole-survivor pin (conf=1000 BY CODE at the kill round) is a
  learned-or-hardcoded conflation of "no competitors" with "certainly
  right"; training confidence to be a function of CUMULATIVE EVIDENCE WEIGHT
  rather than alive-set size removes the pin and with it the confident-liar
  microsecond.
- MECHANISM: (a): at the kill round, confidence jumps 500→1000 with zero new
  evidence — the jump is pure bookkeeping. Any depth that reaches a kill
  therefore manufactures maximum confidence from nothing. Training cannot
  change the code, but it can change what the system LEARNS to treat as
  confidence-worthy: if the learned confidence is a function of cumulative
  net evidence weight for the released hypothesis (which does not jump at
  kills), the pin never fires in the learned meter.
- TRAINING INTERVENTION: Train the release policy (not the deliberation
  ops): the released confidence = learned monotone function of (net support
  weight for the released hypothesis − net attack weight), normalized by
  total evidence weight seen. Curriculum: all honest batteries + trap, with
  correctness labels; objective: calibration (Brier). The pin event
  (alive-set 2→1) is included in training with label = actual correctness
  (usually 0 on O, 1 on honest) so the learner learns that kills carry no
  information.
- PREDICTED OBSERVABLE: The confidence distribution at release loses its
  1000-spike: on O items the kill round shows NO confidence discontinuity
  (confidence is continuous in evidence weight), and deep-O releases are
  low-confidence wrong or abstentions rather than conf=1000 wrong.
- KILL BAR: If post-training, on ANY battery, ≥1% of releases show a
  confidence discontinuity (>200-point jump) at a kill round with no
  accompanying evidence-weight jump → the pin survived in the learned meter
  → KILLED. Also killed if O G(d) still rises anywhere.
- DECIDING BATTERIES: O (the pin fires 100/100 kill rounds here),
  admit/logic (the learned meter must stay calibrated where kills are
  honest).
- INFORMATION VALUE: Isolates (a) as a separable cause: if de-pinning alone
  satisfies L-OVERCONF on O, the pin was the whole game and the fix is a
  one-line training change, not a redesign.

## H-A4 — LEADER-CHALLENGE TRAINING (root cause e)

- CLAIM: The architectural asymmetry (no op attacks the leader) is trainable:
  a learned "devil's-advocate" operation that spends a fixed deliberation
  budget attacking the CURRENT leader each round prevents the flip from
  becoming irreversible, because the truth gets a learned advocate after
  the flip instead of facing the entire kill machinery alone.
- MECHANISM: (e): whoever seizes the lead inherits defense+kills; the flip
  is pure reweighting and then the machinery locks it in. Depth helps the
  leader and only the leader. A trained counter-operation — each round,
  allocate B% of the evidence-application budget to the strongest attack on
  the leader found so far (deterministic: the max-weight attack link) —
  makes leadership contestable at every depth, so late flips are tested
  rather than coronated.
- TRAINING INTERVENTION: Modify the deliberation ops (this is the "train the
  ops" level): add the advocate operation with learned budget B and learned
  attack-selection. Curriculum: P/O/D ceiling (flip dynamics) + honest
  batteries (must not slow honest convergence by >2× rounds). Objective:
  final accuracy + L-OVERCONF satisfaction; the learner tunes B and the
  selection rule. Deterministic given state (max-weight attack, fixed B).
- PREDICTED OBSERVABLE: On O items, post-flip rounds show the advocate
  re-surfacing truth-supporting evidence: the false leader's margin STOPS
  growing monotonically (margin path flattens or oscillates), kills of the
  truth are delayed or prevented, and deep releases are abstentions or
  correct — accuracy-vs-depth on O becomes flat-or-improving instead of
  1.00→0.00.
- KILL BAR: If on the O battery the accuracy curve still strictly decreases
  over any adjacent depth step after training, or if honest-battery accuracy
  drops by >2 percentage points vs the frozen ops (the advocate is a
  vandal, not a critic) → KILLED.
- DECIDING BATTERIES: O (must flatten the anti-monotone curve), P (the
  advocate must not kill P's true flip — asymmetric risk), admit/logic
  (convergence-speed control), D (dose-response of the advocate budget).
- INFORMATION VALUE: Directly tests the mechanist's strongest claim — that
  (e) is THE load-bearing asymmetry. If a learned leader-challenge fixes O,
  the architecture was the disease and training the ops is the cure level.

## H-A5 — INTERACTION: THE PIN NEEDS THE KILL (a × c × e)

- CLAIM: No single root cause is sufficient: the pin (a) is harmless without
  irreversibility (c) — a reversible kill's pin would be corrected next
  round — and irreversibility is harmless without the pin — a wrong but
  low-confidence survivor violates no law. Depth-overconfidence is the
  PRODUCT a×c: the pin manufactures certainty exactly where (c) makes it
  uncorrectable. Training must break the PRODUCT, and breaking either
  factor alone is predicted to fail.
- MECHANISM: Counterfactual decomposition: (a) without (c): pin fires,
  next round's evidence re-opens the kill, confidence re-grounds — V1 needs
  the wrongness to PERSIST, which needs (c). (c) without (a): the survivor
  is wrong but its confidence is the honest margin — G(d) may still rise
  mildly (the M5/M7 pattern: mild G-violations, G stays negative) but no
  V1/V2 catastrophe. The observed catastrophe (G→+1.000, 40/40 V1) needs
  both.
- TRAINING INTERVENTION: Two-arm training experiment. Arm 1: de-pin only
  (H-A3). Arm 2: reversibility only (H-A2). Arm 3: both. Prediction: Arm 1
  kills V1/V2 but leaves mild G-rise (M5-pattern); Arm 2 kills the
  persistence but leaves pin-spikes on transient wrong releases; only Arm 3
  satisfies L-OVERCONF fully on O. This hypothesis is TESTED by the
  2×2, not by a single intervention.
- PREDICTED OBSERVABLE: The predicted dissociation: Arm 1: zero V1/V2, mild
  G-violations remain. Arm 2: zero 1→0, pin-spikes remain on some items.
  Arm 3: full L-OVERCONF satisfaction on O.
- KILL BAR: If Arm 1 ALONE fully satisfies L-OVERCONF on O (no G-violation,
  no V1/V2) → the interaction claim is FALSE (a) was sufficient → KILLED.
  If Arm 3 fails where the dissociation predicts success → KILLED.
- DECIDING BATTERIES: O (the product lives here), admit/logic (control
  that neither arm breaks honest deliberation).
- INFORMATION VALUE: Highest information-per-experiment of the mechanist
  set: a 2×2 that tells you whether the fix is single-point or must be
  compositional — this determines the entire training program's shape.
