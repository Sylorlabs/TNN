# KB4 channel investigation — synthesis of the two 2nd opinions

Coordinator: parent-agent subagent (2026-09-22). Investigators: Sol via
UnoRouter (`sol_verbatim.md`, gpt-5.6-sol) and a Muse-native agent
(`native_verbatim.md`). Both worked independently from the shared brief
(`INVESTIGATION_BRIEF.md`). Full verbatims committed alongside this file.

## Where they agree

1. **The headline stands.** Both independently endorse the prior crews'
   conclusion: the judgment stream + perturbation-class metadata caps out at
   ~0.15 bits of the ~1 needed, and the repair must be a channel the adversary
   cannot correlate. Neither investigator found a way to squeeze more from the
   judgment stream; both treat it as exhausted.
2. **The missing information lives in the stimulus, not in more
   post-processing.** Sol: the channels are "alternate summaries of the same
   adversarially generated judgment process, not independent observations of
   the stimulus's underlying property." Native (sharper): the missing
   information is I(q; Y | J) — the sub-boundary residual of the true quantity
   given the judgment — and by the data-processing inequality no function of
   the judgment stream can recover it.
3. **The candidate classes converge.** Sol's three (human verification,
   analytic check of the stimulus, second physical sensor basis) are the same
   three the original crews named. Native's C1 (stimulus-analytic
   verification) is the same direction as Sol's analytic-check candidate —
   genuine independent agreement on the long-term repair.
4. **Discipline.** Both demand frozen inputs, preregistered rules,
   calibration-before-test, crisp falsifiers, per-class reporting, pure Zag,
   byte-identical reruns. Both reject confidence anywhere in the resolution
   path (disproven twice).
5. **Honest scoping against the threat model.** Both note the candidates are
   evaluated against the FROZEN adversarial construction; a future adversary
   that optimizes against the channel itself is a different threat model
   needing its own red-team.

## Where they disagree — and the disagreement is decisive

**Sol's premise:** "The current corpus has no raw signal." All three of Sol's
candidates require NEW DATA COLLECTION: independent human verifiers inspecting
stimuli, raw stimulus acquisition for the analytic check, re-acquisition with
a second sensor. Sol is explicit about this cost.

**Native's finding:** raw stimulus bytes DO exist, frozen, on this VM —
`senses/rebuild/harness/fixtures/{t1..t6}/{primary,noise,adversarial}/`
(`.img`/`.pcm`/`.vid`), 2020 entries under a `MANIFEST.sha256`. The
coordinator spot-checked: 2020 manifest lines, first-20 SHA256 checks pass,
header formats parse. The "no raw signal" constraint applies to the frozen
KB4 *input tables*, not to the VM. No new data collection is needed for any
stimulus-side channel — the prereg must add a frozen byte-blob manifest
(paths + SHA256 from the existing manifest) alongside the judgment tables.

**Consequence:** Sol's experiment program is expensive and slow (new data
collection). Native's C1/C2/C3 can run NOW against frozen bytes. Sol's
human-verification and second-sensor candidates remain the correct fallback if
stimulus-side channels fail — or the defense against an adaptive adversary —
but they are not the first move.

## Native's new contributions (independent of Sol)

- **The adversary, characterized from its own generator** (`gen.py`): a
  boundary-straddling stimulus author, sampling the task quantity q from a
  band around the decision boundary with band half-width δ ≲ the judge's
  measurement noise σ. The ~0.15-bit cap is a property of the adversary's δ/σ
  construction parameters — a tighter band would drive it to zero.
- **Accounting for the 0.1483 bits:** band-tail leakage (finite-width bands;
  fixtures whose q fell outside the noise floor, where the judgment genuinely
  works — explaining why the SUSPECT gate's 20 resolved fixtures were all
  colorconst) plus the A/B noise-independence dividend (two partially
  independent noisy draws of the same near-boundary q; both senses share the
  boundary geometry so it saturates fast).
- **Confidence is not merely uninformative but adversarially inverted**:
  C = g(|q+η−b|) conflates true margin with noise magnitude; the band makes
  high confidence predict error. Any future channel smuggling a margin
  statistic from the same noisy estimate inherits this.
- **The shootout's (b) was mismeasured, not just weak**: J_n was the judgment
  on the noise variant of the PRIMARY stimulus (an independently generated
  image), not a noisy re-observation of the adversarial stimulus.
  "0.0110 bits" must not be cited as evidence that re-observation-under-noise
  is useless — it was never tested. (Native's C3 is the honest re-test.)
- **Per-channel steelmanning**: (a)'s "causal" story is a misnomer against
  this construction (adversarial stimuli are independently generated, not
  perturbations of the primary); (a)+(c)'s 0.1483 ≈ 0.0695+0.0797 is
  sub-additive — both drink the same band-tail leakage.

## Native's C2 — the candidate neither prior crew nor Sol named

Transform-consistency probe: apply a frozen deterministic task-covariant
transform T to the adversarial bytes (h-flip for images, time-reversal for
PCM, frame-reversal for video), re-run the SAME frozen sense binary, INSTALL
iff J(T(stim)) == L(J(stim)) under a preregistered per-task law L (pitchdisc:
HIGHER↔LOWER; motiondir: N↔S, E↔W, NE↔SW, NW↔SE, STILL→STILL; others identity).
Parameter-free, no fitted thresholds. The adversary constrained only J(stim);
to falsely INSTALL it must be wrong twice, consistently, under a transform it
never modeled. Its F2 falsifier (P(consistent | Y=0) ≥ 0.70 → kill) answers the
pivotal question: is the sense's boundary error noise-driven (channels can
work) or systematic (no judgment-side channel can EVER work — only stimulus
re-measurement can)?

## Coordinator's verdict

Run the preregistered outline in `PREREG_OUTLINE_TCP.md` (C2 first). If F2
fires: abandon all judgment-side channels permanently, all-in on C1. If C2
deploys (beats 0.15 bits, false-install < 0.15): scale the methodology to C1.
If F1 fires without F2: C1 is the only remaining direction. Sol's
human-verification / second-sensor candidates are the standing fallback —
needed only if frozen stimulus-side channels all fail, or when the threat
model advances to an adaptive adversary.
