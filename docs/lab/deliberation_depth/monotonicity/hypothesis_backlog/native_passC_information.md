# NATIVE PASS C — the information theorist (independent pass 3 of 3)

Framing: I treat deliberation as an information channel and ask what
information depth ADDS versus what it DESTROYS. Overconfidence is then a
channel pathology: the system's confidence claims more information than the
channel delivered. Training is information-diet design: what the learner is
allowed to condition on, what it must forget, and what invariants the channel
must preserve. I do not consult the other passes.

Channel facts (from the verified findings, recast):
- The margin is a LOSSY statistic: it collapses the full evidence-weight
  history into distance-to-runner-up. Information destroyed: everything
  about HOW the margin was reached.
- Elimination is information DESTRUCTION: the killed hypothesis's
  supporting evidence is dropped from all future conditioning (alive[]=0 —
  written in exactly 3 places, never restored).
- The pin is information FABRICATION: conf=1000 is written with zero new
  evidence — confidence claims information the channel never received.
- The O-flip is information-neutral reweighting (truth alive but
  out-scored) followed by destruction (the kill). Depth's information
  content post-flip is ~zero; its confidence claims ~maximum.

## H-C1 — NO-FABRICATION TRAINING: CONFIDENCE ≤ INFORMATION (channel invariant)

- CLAIM: The pin is the only point in the pipeline where confidence is
  manufactured from zero information; a training regime that enforces the
  invariant "reported confidence may never exceed the information actually
  received since the last grounding event" eliminates the confident-liar
  microsecond by construction, and everything else follows.
- MECHANISM: Information-theoretic: let I(t) = cumulative net evidence
  weight actually consumed for the released hypothesis. The pin writes
  conf=1000 while ΔI=0 — a pure fabrication event. Every V1 violation in
  the dataset (40/40 O) coincides with a fabrication event (the kill
  round). If the learned confidence policy is constrained to be a function
  of I(t) alone (no alive-set-size term, no kill term), fabrication is
  impossible and confidence is automatically continuous in information.
- TRAINING INTERVENTION: Train the confidence policy with a hard
  architectural constraint (not a soft loss): conf = g(I(t)) for a learned
  monotone g, where I(t) is cumulative consumed evidence weight for the
  released hypothesis. The kill event contributes ΔI=0 by definition, so
  the pin cannot fire in the learned meter. Curriculum: all batteries with
  correctness labels; g learned for calibration (Brier). The constraint is
  enforced in the function class, not hoped for in the loss.
- PREDICTED OBSERVABLE: Zero confidence discontinuities at kill rounds
  across all batteries (measured: max |Δconf| at kill rounds < 50 points);
  O G(d) loses its catastrophic rise because the kill round no longer
  manufactures certainty; remaining G-violations (if any) are mild and
  honest (the M5-pattern).
- KILL BAR: If post-training ANY kill round on ANY battery shows
  |Δconf| > 100 with ΔI ≈ 0 (fabrication survived the constraint — e.g.
  the learner smuggled alive-set size into g via a correlated feature), or
  if O still shows V1 violations → KILLED.
- DECIDING BATTERIES: O (40/40 V1s all coincide with fabrication events),
  admit/logic (g must still calibrate honest kills — information-honest
  confidence must not understate real convergence).
- INFORMATION VALUE: The strongest-form test of "the pin is the whole
  catastrophe": a hard constraint experiment. If it works, the fix is a
  one-line architectural invariant, and every softer hypothesis was
  overkill. If it fails, fabrication was never the load-bearing cause.

## H-C2 — FORGETTING CURRICULUM: TRAINED INFORMATION HYGIENE (double-counting)

- CLAIM: Depth overconfidences partly because NOTHING IS EVER FORGOTTEN:
  early evidence keeps voting forever, so late flips compound on stale
  tallies rather than replacing them — and the confidence meter counts the
  stale votes. Training a learned FORGETTING policy (evidence half-life,
  learned per family) stops depth from accumulating phantom certainty.
- MECHANISM: In the frozen harness, evidence weights are immortal: e_1's
  support still counts at round 64. On O items, the pre-flip plateau's
  weight mass is what the post-flip evidence must overcome — and after the
  flip, BOTH the plateau mass (now misdirected) and the flip mass vote for
  the false leader. Confidence then double-counts: it reflects the sum of
  two eras' weights as if they were independent corroboration. Depth adds
  votes but never retires them.
- TRAINING INTERVENTION: Train a forgetting kernel: effective weight of
  evidence item e at round r = raw weight × λ^(r − r_e), with λ learned per
  family (or a learned function of stream statistics). Curriculum: honest
  families (where forgetting must stay near λ≈1 — old evidence stays valid)
  vs O/D (where stale plateau weight must decay for the flip to be
  honestly re-evaluated). Objective: final accuracy + calibration; λ is the
  learned parameter. Deterministic given state.
- PREDICTED OBSERVABLE: Learned λ_O < λ_honest (the system learns that
  flip-structured streams need forgetting); on O items the pre-flip weight
  mass decays so the flip is evaluated on recent evidence alone — the false
  leader's margin no longer compounds two eras, confidence drops, deep
  accuracy recovers or abstention fires honestly.
- KILL BAR: If learned λ is ≈1 on ALL families (the optimizer refuses to
  forget — forgetting hurts honest accuracy more than it helps O), or if O
  accuracy still collapses with λ_O < 1 in place (double-counting was not
  the driver) → KILLED.
- DECIDING BATTERIES: O (forgetting must help here), admit/logic (λ must
  stay ≈1 here — forgetting honest evidence is vandalism), D (dose-response:
  λ should vary smoothly with flip dose), cost (forgetting changes
  deliberation cost — the cost battery prices the tradeoff).
- INFORMATION VALUE: Tests a completely different causal story from the
  pin/kill narratives: the "stale votes" theory. Positive result means the
  harness's immortal evidence was a silent overconfidence engine nobody
  instrumented.

## H-C3 — ENTROPY-FLOOR TRAINING: KEEP THE FIELD WIDE (pool collapse)

- CLAIM: Depth destroys information by collapsing the hypothesis pool:
  alive-set entropy goes to zero (2→1) exactly when confidence goes to max.
  Training a policy that maintains a minimum alive-entropy (or equivalently
  penalizes pool collapse) keeps the system's uncertainty REPRESENTED in
  its state, so confidence cannot outrun the represented alternatives.
- MECHANISM: Confidence should track "how much of the possibility space
  have I ruled out, and how carefully." The frozen harness rules hypotheses
  out with a fixed threshold and then reports confidence as if the ruling-out
  were infallible. The information actually destroyed by a kill (the dead
  hypothesis's entire support structure) is never represented anywhere —
  the system cannot be uncertain about what it has deleted. Depth →
  collapse → certainty, with the uncertainty deleted rather than resolved.
- TRAINING INTERVENTION: Add a "ghost" representation: killed hypotheses
  leave a learned summary (their net support at death, the killing margin)
  that continues to condition the confidence policy but not the release.
  Train the confidence policy on (live state + ghost summaries) for
  calibration across all batteries. The ghosts are the deleted uncertainty,
  restored as conditioning information. Deterministic; ghosts are just
  index-level history the frozen harness threw away.
- PREDICTED OBSERVABLE: On O items, the ghost of the killed truth (high
  support-at-death, killed by a flip) conditions confidence DOWNWARD —
  deep releases are low-confidence or abstentions; the ghost-summary
  weight in the trained policy is large and negative on O, near-zero on
  honest families (where kills are clean).
- KILL BAR: If the trained policy puts near-zero weight on ghost summaries
  on O items (the deleted information carries no signal — the optimizer
  ignores the ghosts), or if L-OVERCONF still fails on O → KILLED.
- DECIDING BATTERIES: O (ghosts of flip-killed truth live here), trap
  (ghosts of hasty d1 kills), admit/logic (ghost weight must be ~0 —
  honest kills leave no informative ghosts, else the policy is paranoid).
- INFORMATION VALUE: Decides whether "deleted uncertainty" is recoverable
  signal or true information loss: if ghosts condition calibration, the
  harness was throwing away the very information confidence needed.

## H-C4 — SUFFICIENT-STATISTIC TRAINING: LEARN WHAT TO CONDITION ON

- CLAIM: The real learned object should not be confidence at all — it
  should be the SUFFICIENT STATISTIC of the deliberation trajectory for
  correctness. The margin is a catastrophically insufficient statistic
  (verified: overlapping distributions). Training should discover the
  minimal statistic that screens off correctness from the trajectory, and
  confidence should be a function of THAT.
- MECHANISM: Information-theoretic framing of (b): a statistic T of the
  trajectory is sufficient for correctness iff P(correct | trajectory) =
  P(correct | T). The margin fails sufficiency spectacularly (same margin,
  wildly different correctness across families). Depth-overconfidence is
  what happens when you condition a decision on an insufficient statistic:
  the unconditioned residual variation (family, flip-structure) leaks into
  error that the statistic cannot see. Training the statistic — not the
  confidence number — is the correct level of intervention.
- TRAINING INTERVENTION: Representation-learning phase on logged
  deliberation trajectories from all batteries: train an encoder E of the
  index-level trajectory to predict correctness, with an information
  bottleneck (minimize I(E; trajectory) subject to maximizing I(E;
  correctness)). The learned E is the trained sufficient statistic.
  Release confidence = calibrated map of E. Then measure: how much does
  E improve correctness-prediction over the margin (ΔAUROC), and does
  confidence(E) satisfy L-OVERCONF?
- PREDICTED OBSERVABLE: E achieves correctness-prediction AUROC ≥ 0.85 on
  held-out items (vs margin's ~0.55 — barely above chance, implied by the
  overlapping distributions), and inspection of E reveals WHICH trajectory
  features carry the signal (leader-change timing? margin-path shape? kill
  recency?) — the experiment also DISCOVERS the mechanism, not just the fix.
- KILL BAR: If E's held-out correctness-prediction AUROC ≤ 0.65 (the
  trajectory contains no sufficient statistic — correctness is not a
  function of index-level deliberation state at all, and the mirror theorem
  is then not just true but COMPLETE: no index-level learning can ever
  work), → KILLED, and the whole "train the confidence" program dies with
  it. This is the highest-stakes kill bar in the backlog.
- DECIDING BATTERIES: ALL — E is trained on all families and must predict
  across them; the cross-family generalization of E (train on admit/logic,
  test on O) is the transfer test. Redteam: adversarial items must not
  fool E (else E is just a fancier margin).
- INFORMATION VALUE: The meta-hypothesis: it decides whether ANY
  index-level training approach can work. A negative result is the most
  informative possible outcome — it would prove the fix must come from
  OUTSIDE index-level state (content, provenance, or amended
  admissibility), redirecting the entire program.

## H-C5 — CHANNEL-CAPACITY CURRICULUM: DEPTH AS A BUDGET, NOT A LADDER

- CLAIM: Overconfidence with depth is a framing artifact of treating depth
  as a LADDER (more = better) rather than a BUDGET (fixed total
  deliberation to spend). Training under a fixed deliberation budget —
  where spending rounds early means fewer later — teaches the system to
  price depth, and priced depth does not overconfidence because every
  round must justify its cost in expected accuracy.
- MECHANISM: The frozen harness treats depth as free: the sweep runs d64
  because it can. Nothing in training ever taught the system that round 40
  COSTS something (compute, and the risk of flip exposure). Unpriced depth
  is overconsumed, and overconsumed depth on adversarial streams is pure
  risk with no return — the O collapse is what unpriced depth BUYS.
  Economic framing: overconfidence is the externality of free depth.
- TRAINING INTERVENTION: Budgeted-deliberation curriculum: each item comes
  with a deliberation budget B (varied across training); the learned
  stopping policy decides when to stop spending. Reward = correctness −
  λ·(rounds spent), λ swept. The system learns a price of depth: it spends
  deep only where the expected accuracy gain exceeds the price. O items
  teach that deep spending has NEGATIVE expected return (the flip region);
  P items teach positive return; honest items teach early stopping.
- PREDICTED OBSERVABLE: The learned stopping policy stops BEFORE the flip
  region on O items (mean stop-round on O < flip round — the residual-flip
  bound's adaptive policy already does this: O acc 1.000 at 5.0 rounds),
  spends deep on P, stops at d1–d2 on honest items. Depth is then never
  "overconfident" because depth is never spent where it harms — the G(d)
  curve is measured on the CHOSEN depth per item, not the forced sweep.
- KILL BAR: If the learned stopping policy cannot beat the frozen
  residual-flip bound's O accuracy (1.000 at 5.0 rounds) — i.e., learning
  adds nothing over the hand-coded bound — or if on P items it stops
  before P's flip (it learned fear, not pricing: P accuracy collapses) →
  KILLED.
- DECIDING BATTERIES: O (must stop before the flip), P (must spend through
  the true flip — the pricing discriminator), cost (the cost battery IS the
  price list — the learned λ must match it), D (dose-response of the
  stopping price).
- INFORMATION VALUE: Reframes the entire problem: maybe monotonicity was
  never about making d64 safe — it was about learning not to GO to d64.
  A positive result dissolves the problem rather than solving it, which is
  the most valuable kind of result.
