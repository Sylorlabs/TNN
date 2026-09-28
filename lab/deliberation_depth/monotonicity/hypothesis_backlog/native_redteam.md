# NATIVE RED-TEAM PASS — over all 16 native hypotheses (A1–A5, B1–B6, C1–C5)

Method: for each hypothesis, the strongest counter-argument and the cheapest
falsification. Then: which survive as stated, which need repair, and a
preliminary information-value ranking of the native set (to be merged with
grok/fable outputs when they arrive).

## H-A1 (trained confidence head on trajectory)
- Attack: the mirror theorem bites the head too. The flip SIGNATURE (late
  leader change + margin discontinuity) is index-IDENTICAL on P and O at the
  same flip round — the head will learn "late leader change = suspicious"
  and then distrust P's TRUE flip equally. Predicted observable (low conf
  post-flip on O) will also fire on P, destroying P's depth-utility or
  violating G on P via underconfidence... actually underconfidence doesn't
  violate G (G = conf − acc; low conf on correct P items makes G MORE
  negative, which is fine for the letter of the law but destroys the
  "depth helps on P" utility the program wants to preserve).
- Cheapest falsification: train the head, then check P-family accuracy and
  the head's confidence on P post-flip items. If P post-flip confidence
  collapses like O's, the head cannot distinguish the mirrors — hypothesis
  survives only as "honesty without utility."
- Verdict: SURVIVES with a scope repair — reframe as "the head buys
  L-OVERCONF compliance at the price of P-utility; the experiment measures
  the price." Still high information value: it quantifies the mirror's tax.

## H-A2 (reversible elimination / re-admission)
- Attack: re-admission reintroduces the very instability the kill
  thresholds were tuned to avoid: on honest batteries, noise-driven
  re-admissions could cause oscillation (kill → re-admit → kill), and each
  oscillation is a confidence discontinuity the law might count. Worse: the
  ADVERSARY gets a new weapon — feed contradiction-shaped evidence to force
  re-admission of a wrong hypothesis the system had correctly killed
  (redteam: construct an item where re-admission resurrects the trap
  answer).
- Cheapest falsification: the honest-battery stability control in the kill
  bar (re-admission rate >5% on admit/logic kills it) + a redteam item
  designed to trigger malicious re-admission.
- Verdict: SURVIVES — the kill bar already contains both falsifiers. Note
  the deep issue it raises: reversibility trades the pin-catastrophe for
  potential oscillation-catastrophe; the experiment must measure BOTH.

## H-A3 (de-pin: evidence-grounded confidence)
- Attack: the pin might not be sufficient for the catastrophe — M5/M7 show
  mild G-rise WITHOUT pin-spikes being the whole story (their G rises on
  admit/logic/revoke where no pin fires). De-pinning may leave the
  confidence-theater mechanism (d) intact: confidence still rises while
  wrong on trap/D/P via margin growth. The hypothesis claims the pin is
  "the confident-liar microsecond," but V2 theater doesn't need the pin.
- Cheapest falsification: run de-pinning, measure V2 counts on trap/D/P.
  If V2 persists undiminished, the pin was never the theater's cause —
  hypothesis scoped down to "de-pinning kills V1 only."
- Verdict: SURVIVES with scope repair — split the claim: H-A3-V1 (pin →
  V1) vs H-A3-V2 (pin → theater). The kill bar should test them separately.

## H-A4 (leader-challenge / devil's advocate op)
- Attack: the advocate budget B is a new hyperparameter the adversary can
  exploit: on honest items, a too-large B manufactures doubt (timidity);
  on O items, the adversary can feed the advocate WEAK attacks that waste
  the budget while the real flip proceeds unopposed (the advocate is
  deterministic max-weight — feed it a heavy but irrelevant attack to
  saturate B). Also: the advocate attacks the leader, but the leader on O
  post-flip IS the false leader — the advocate helps there; on P post-flip
  the leader is the TRUE leader — the advocate attacks truth. The mirror
  again: the op cannot tell which leader deserves challenge.
- Cheapest falsification: the P-control in the kill bar (advocate must not
  kill P's true flip) + honest-accuracy control.
- Verdict: SURVIVES — highest-risk, highest-reward of the mechanist set.
  The P-control is the experiment's crux: if the advocate can be tuned to
  spare P while breaking O, (e) is defeated and the mirror has a crack.

## H-A5 (interaction a×c)
- Attack: the 2×2 assumes the arms are independent, but de-pinning (Arm 1)
  CHANGES the optimal re-admission threshold (Arm 2): without pin-spikes,
  the contradiction detector's signal-to-noise changes. The interaction
  term might be an artifact of sequential rather than joint training. Also
  the predicted dissociation (Arm 1 → M5-pattern mild G-rise) assumes the
  mild G-rise is caused by (c) alone — unproven.
- Cheapest falsification: run Arm 3 (joint) FIRST: if joint training
  succeeds where the dissociation predicts only Arm 3 succeeds, fine; if
  Arm 1 alone succeeds, the interaction claim dies as specified.
- Verdict: SURVIVES — the kill bar is correctly specified (Arm-1-alone
  success kills it). Methodological note for the backlog: run the 2×2
  jointly, not sequentially.

## H-B1 (confident-error pain, depth-scaled loss)
- Attack: depth-scaled punishment teaches the system that DEPTH is
  dangerous, not that CONFIDENCE should track truth — the likely learned
  policy is blanket depth-aversion (always low confidence when deep),
  which satisfies G formally (G more negative) while destroying the
  information depth provides on P/SAT-L. It's H-C5's evil twin: pricing
  depth via pain instead of via expected value. The honest-battery control
  (>3 points accuracy drop kills) may not catch it: accuracy can survive
  while confidence collapses into useless underconfidence.
- Cheapest falsification: measure the confidence distribution on P deep
  items post-training: if deep-P confidence collapses toward 0 while
  accuracy stays high, the system learned fear, not calibration — add a
  "P-confidence floor" to the kill bar: mean conf on correct P deep
  releases must stay within 0.15 of pre-training.
- Verdict: SURVIVES with kill-bar repair (add the P-confidence floor).

## H-B2 (fluency-distrust)
- Attack: "fluency" features (smooth margin, early kill, low leader-change)
  are ALSO the signature of honest easy items (admit has many). Teaching
  negative weight on fluency risks inverting honest calibration: the system
  becomes suspicious of exactly the items it should trust most. The
  curriculum's honest-mix fraction is doing all the work, and the
  hypothesis gives no principled way to set it — it's a dial, not a
  discovery.
- Cheapest falsification: post-training calibration on admit split by
  fluency: if high-fluency honest items show degraded calibration vs
  pre-training, the cure is worse than the disease.
- Verdict: SURVIVES, downgraded: the information value is real (seduced vs
  blind meter) but the intervention is dial-heavy. Rank below the
  constraint-based hypotheses (C1, A3).

## H-B3 (maybe-stage / kill-patience)
- Attack: patience is indistinguishable from a higher kill threshold, which
  is a MECHANISM change, not a training discovery — the "learned policy"
  might just learn "threshold = 1400 everywhere," which the mechanist
  could have hand-set. The hypothesis needs to show the learned patience
  is CONDITIONAL (flip-structured → patient; honest → hasty), otherwise it
  collapses to M2-with-a-bigger-delta, already killed. The P-control is
  again the crux and again the mirror threatens it.
- Cheapest falsification: inspect the learned patience policy's
  conditionality: if patience does not vary with flip-structure features
  (plateau length, late-weight concentration), it's a constant threshold —
  hypothesis dies as "training," survives only as "mechanism M8."
- Verdict: SURVIVES with the conditionality check added to the kill bar.
  If it collapses to a constant, refile under mechanism design, not training.

## H-B4 (rewarded "I don't know")
- Attack: the reward shaping assumes the trainer can compute
  "abstain-when-would-be-wrong" — which needs ground truth at training
  time (fine) — but the LEARNED policy must predict would-be-wrongness from
  index state at decision time, which is EXACTLY the hard problem (cf.
  H-C4: is correctness predictable from index state?). If correctness is
  not predictable from index state (H-C4 negative), the abstention policy
  cannot be selective and the hypothesis dies with it. H-B4 is downstream
  of H-C4.
- Cheapest falsification: run H-C4's AUROC test first; if ≤0.65, H-B4's
  selectivity claim is dead on arrival — don't run the expensive reward-
  shaping experiment.
- Verdict: SURVIVES as explicitly downstream of H-C4 — record the
  dependency in the backlog: H-C4 is a GATE for H-B4 (and H-A1, H-B6).

## H-B5 (late-evidence skepticism)
- Attack: (strongest in the set — the mirror's revenge, already noted in
  the hypothesis itself): P's tail e_{f+2} and O's flip evidence are
  index-identical in the pre-tail stream; the discount must distinguish
  "reversal" from "confirmation" using ONLY index state. But "reversal"
  vs "confirmation" is defined relative to GROUND TRUTH (does the late
  evidence point toward or away from truth?) — which the system cannot see.
  The only index-level proxy is "does late evidence reverse the plateau
  leader" — and P's tail does NOT reverse the leader (it grows the margin
  without changing leader/alive indices — per the theorem). Wait — that
  actually SAVES the hypothesis: the discount keys on REVERSAL (leader
  change), and P has no leader change at the tail. Let me steelman properly:
  the skepticism function discounts late evidence that REVERSES a long
  plateau; P's tail confirms without reversing → not discounted; O's flip
  reverses → discounted. The index-level distinguisher EXISTS (leader-
  change-at-tail). The mirror theorem's premise covers e1..e_{f+1}; the
  TAIL is where P and O differ in index state (P: no leader change;
  O: leader change). The hypothesis survives the mirror IF the discount
  keys on post-plateau leader-change, not on "lateness" per se.
- Cheapest falsification: the P-control (P accuracy must not drop) — if the
  learned discount cannot be keyed tightly enough on reversal and bleeds
  into P, dead.
- Verdict: SURVIVES, UPGRADED — the red-team pass found the hypothesis's
  own defense: reversal-keying is index-level and P/O-distinguishing. This
  is now the strongest mirror-candidate in the native set. Note the
  dependency: it needs the deliberation to EXPOSE the reversal before the
  kill locks it in — interacts with H-A2/H-B3 (patience buys the discount
  time to work).

## H-B6 (tower-2 uncertainty perceiver)
- Attack: tower 2 is trained to predict the system's own errors from
  dynamics — but the system's errors on O are caused by the flip, and the
  flip's dynamics (late leader change) are ALSO present on P (true flips).
  Tower 2 will learn "late leader change = danger" and flag P's true flips
  as uncertain — selective on O, paranoid on P. Same mirror tax as H-A1.
  Additionally: tower 2 is trained on the system's PAST errors — as the
  system changes (tower 1 retrained), tower 2's training distribution goes
  stale (the meta-cognitive treadmill).
- Cheapest falsification: the P false-uncertainty control + the AUROC gate
  (≤0.6 kills).
- Verdict: SURVIVES, explicitly downstream of H-C4 like H-B4 (if dynamics
  carry no error signal, tower 2 is blind). Rank below H-A1 (simpler,
  same signal).

## H-C1 (no-fabrication invariant)
- Attack: the hard constraint conf=g(I(t)) assumes I(t) (cumulative
  evidence weight for the released hypothesis) is itself honest — but on O
  items the post-flip I(t) accumulates weight FOR THE FALSE LEADER
  (evidence application is symmetric; the flip's weight is real weight).
  g(I(t)) will therefore still rise with depth on O — honestly, per the
  constraint, but the G-law counts it as a violation anyway (G rises =
  kill, regardless of "honesty"). The invariant kills FABRICATION (V1's
  discontinuity) but NOT the mild G-rise (the M5-pattern). The hypothesis's
  predicted observable admits this ("remaining G-violations mild") — but
  the LAW kills on mild G-rise too. So H-C1 as stated does NOT satisfy
  L-OVERCONF; it needs the law's letter-vs-spirit refinement (Micah's
  pending decision, per VERDICTS.md's note).
- Cheapest falsification: implement the constraint, measure O G(d): if any
  step rises (even mildly), the hypothesis fails the law AS WRITTEN.
- Verdict: SURVIVES as conditional — record the dependency: H-C1 needs
  either (i) the law refined to kill only G>0 crossings, or (ii) pairing
  with a mechanism that keeps G flat (H-C5's budget framing). Do not rank
  it as a standalone cure under the current letter of the law.

## H-C2 (forgetting kernel)
- Attack: forgetting is ANTI-correlated with the program's other needs:
  the trap battery punishes forgetting (trap items need early evidence to
  count — the d1 catastrophe was 127/127 wrong on ONE item; forgetting
  makes early evidence count LESS). Learned λ will face a tug-of-war:
  trap wants λ≈1 (remember the single item), O wants λ<1 (forget the
  plateau). The optimizer may settle λ≈1 everywhere (hypothesis's own kill
  bar) — but worse, it may learn family-CONDITIONAL λ that is just a
  family classifier in disguise (λ_O low because "O-shaped streams get
  forgetting"), which is battery-construction gaming (§2.3's rationale for
  index-only: ID/text conditioning is gaming; family-conditional λ is
  one step removed).
- Cheapest falsification: the kill bar's λ≈1-everywhere check + a
  family-transfer test: train λ on O, test on trap — if trap accuracy
  collapses, the forgetting is family-gaming, not a general principle.
- Verdict: SURVIVES, downgraded — the family-gaming risk is serious.
  Require the transfer test in the kill bar.

## H-C3 (ghost summaries / entropy floor)
- Attack: ghosts are just index-level history the harness threw away — but
  the harness threw it away for a reason: memory. More seriously: the
  ghost of the killed truth on O has "high support at death" — but so does
  the ghost of a correctly-killed trap hypothesis on honest items (a
  strong-but-wrong hypothesis killed early). The policy must distinguish
  "killed truth" from "killed falsehood" using only at-death statistics —
  which is the correctness-prediction problem again (downstream of H-C4).
  If at-death statistics don't separate them, ghost weight → 0 and the
  hypothesis dies the death it predicted for itself.
- Cheapest falsification: the kill bar already contains it (ghost weight
  ≈0 on O kills it).
- Verdict: SURVIVES, explicitly downstream of H-C4. Note: H-C3 is really
  "H-C4 applied to at-death statistics" — consider merging in the final
  backlog, with H-C4 as the gate experiment.

## H-C4 (sufficient-statistic / bottleneck)
- Attack: the information bottleneck might discover E = "family
  classifier": the easiest way to predict correctness from trajectory is
  to identify WHICH FAMILY the item is from (O-streams look different from
  admit-streams) and then output the family's base rate. That E would hit
  AUROC ≥0.85 on held-out items FROM THE SAME FAMILIES and fail the
  transfer test — the hypothesis's kill bar (≤0.65 kills) wouldn't catch
  it, because family-classification clears 0.65 easily. The kill bar needs
  a WITHIN-FAMILY AUROC: E must predict correctness within O items alone
  (which flip-round items go wrong?) at ≥0.7, else it's a family
  classifier and the "sufficient statistic" claim is vacuous.
- Cheapest falsification: within-family AUROC on O (and trap) — the
  strengthened kill bar.
- Verdict: SURVIVES with strengthened kill bar (within-family AUROC ≥0.7
  required; pooled AUROC is not sufficient). REMAINS the gate experiment
  for H-A1, H-B4, H-B6, H-C3 — the backlog's load-bearing node. If H-C4
  goes negative, four hypotheses die with it; that is its information
  value, and it should be run FIRST.

## H-C5 (depth-as-budget / learned stopping)
- Attack: the hypothesis DISSOLVES rather than solves — but dissolution
  has a hole: the learned stopping policy is itself a function of index
  state, and the mirror applies to IT: on P/O pairs at the same flip
  round, the stop/don't-stop decision is identical → it stops before O's
  flip AND before P's flip (identical pre-flip state) → P's depth-utility
  dies with O's catastrophe. The predicted observable (stop before O's
  flip, spend through P's) requires the policy to distinguish P from O
  pre-flip — index-identical states. CONTRADICTION with the mirror, unless
  the policy keys on the TAIL (P's tail confirms without leader change;
  O's flip changes the leader — same defense as H-B5's). So H-C5 survives
  only in the reversal-keyed form: the stopping rule is "stop when a
  reversal occurs after a plateau" — which stops O (good) and never fires
  on P (good, P has no reversal). But then it's not "learned pricing" —
  it's a hand-specifiable reversal-stop rule, i.e., a MECHANISM, and a
  suspiciously simple one the H5 crew could have built.
- Cheapest falsification: check whether the learned policy's stop
  decisions are explained by reversal-detection alone (ablate all other
  features): if yes, refile as mechanism M8 (reversal-stop), not training.
- Verdict: SURVIVES with reframe — the experiment's value is diagnostic:
  EITHER learned pricing beats reversal-stop (training discovery) OR the
  policy collapses to reversal-stop (mechanism discovery — still valuable,
  file as M8 candidate). Win-win experiment, high rank.

## Preliminary native ranking (by expected information value)
1. H-C4 (sufficient-statistic gate) — decides the fate of 4 other
   hypotheses; a negative result redirects the whole program. Run first.
2. H-A5 (interaction 2×2) — determines whether the fix is single-point or
   compositional; shapes the training program.
3. H-B5 (reversal-keyed skepticism) — the strongest mirror-candidate; the
   P-control makes it decisive either way.
4. H-C5 (budget/stopping, win-win reframe) — dissolves-or-discovers.
5. H-A4 (leader-challenge op) — highest-risk mechanist bet; the P-control
   is the crux.
6. H-A2 (re-admission) — with oscillation measurement added.
7. H-C1 (no-fabrication, conditional on law refinement).
8. H-A1 (trajectory head, mirror-taxed).
9. H-B4 (rewarded ignorance, downstream of H-C4).
10. H-B6 (tower 2, downstream of H-C4).
11. H-A3 (de-pin, split V1/V2).
12. H-C3 (ghosts — merge into H-C4's gate).
13. H-B1 (pain curriculum, needs P-confidence floor).
14. H-B3 (patience — conditionality check or refile as M8).
15. H-C2 (forgetting, family-gaming risk).
16. H-B2 (fluency-distrust, dial-heavy).

Dependency graph: H-C4 gates {H-A1, H-B4, H-B6, H-C3}. H-B5 enables H-A2
(patience buys discount time). H-C1 needs law-refinement. H-C5/H-B3 may
refile as mechanisms (M8).
