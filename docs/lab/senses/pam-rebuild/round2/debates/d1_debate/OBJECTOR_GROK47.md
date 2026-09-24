# D-1 DEBATE — EXTERNAL STEELMAN OBJECTOR (grok-4.7, streaming round)

Date: 2026-09-24. Status: EXTERNAL objector round COMPLETE (deferred item from DEBATE_RECORD.md, open item 3).

- Model: grok-4.7 via UnoRouter streaming SSE wrapper
  (`~/workspace/skills/unorouter/bin/grok47_stream.py`), highest reasoning
  effort ("reasoning_effort": "high"), explicitly requested maximum thoroughness
  per standing policy. Usage: completion_tokens 10655 (reasoning 5283), prompt 3756.
- Prior attempts this session all failed: non-streamed grok-4.7 HTTP 524 x3,
  claude-fable-5.1 HTTP 524, gpt-5.6-sol `choices:null` / 0 tokens (known
  failure mode: non-streamed long generations 524 at ~120s). Streaming succeeded
  first try; NO retries, NO model substitution.
- Prompt: `objector_prompt.txt` (assigned F7a / F8c+F8a / F10a+F10c attacks, output
  format) + current debate state (probe results, narrowed cores, D1 hybrid commit
  rule from DEBATE_RECORD.md) + native objector record. Objector instructed to
  attack the NARROWED cores and the hybrid, state agree/disagree with the native
  objector by name, and steelman new hybrid attacks.
- The full grok response follows verbatim below. Nothing redacted; only this
  provenance header is added.

NOTE ON DIVERGENCE: this objector DISAGREES with DEBATE_RECORD.md's verdicts on
two material points: (1) it ranks the survivors 8-audit(tripwire) > 7-residue > 10,
reversing the native 7 > 10 > 8; (2) it kills the D1 hybrid commit rule itself
(Class H blind-quadrant conjunction, handoff inversion, abstain-policy bind,
parameter farming, determinism/secrecy contradiction, replay-split) and demands a
Class H battery with equal-read adversary before the hybrid stands. This is a
debate input, not an adjudication; the D1 crew decides whether it moves the
verdicts.

---

The narrowed cores and the hybrid are what is on trial. The general claims are already dead; I will not re-litigate them except where a corpse is still load-bearing inside the commit rule.

Program constraint I treat as binding, because the debate itself made it binding: pure deterministic mechanisms, zero randomness, byte-identical reruns under 3× SHA-compare. Any warrant whose discrimination exists only when the adversary’s read set is strictly smaller than the verifier’s is an artifact of the battery’s information partition, not a property of the mechanism. I use that constraint as a knife. The native objector did not.

## H-PAM-7 — narrowed core (static-frame / unimodal locus; Class B only via a trusted channel)

**Steelman.** The surviving claim is not “priced response.” The probe killed the price: a perturbation-consistent renderer, built once, installs 120/120, tau-inert. What remains is “Class A static injection fails 0/120, and Class B is outsourced to an unobservable intervention channel or to P10.”

That residue dies in three sub-mechanisms.

First, **response-table collapse of the A/B cut.** Class A vs Class B is an implementation choice of the attacker, not a physical cut. If the perturbation vocabulary (crop index, gain, temporal offset) is finite — and under a deterministic gate it is a pure function of the transcript — the attacker does not need an online renderer. They materialize the renderer as a table at build time: for each vocabulary atom, the lawful-looking answer. Emitting the table entry is static injection. It is Class A in the byte pipe and Class B in effect. Composition of probes composes the table; cost stays at build time. The 0/120 result only measures adversaries who refuse to index the vocabulary. A capability filter is not a locus.

Second, **abstain is a selectable hole, not a safety behavior.** F7b honest-loss at 30% already exceeds the D1 K6 bar of ≤15%. The narrowed core’s patch — abstain-to-provisional on complex scenes — hands the attacker the routing bit. Dominant strategy: put the lie in a scene the complexity predicate flags (or add the cheap features that flag it). The gate abstains exactly on the frames that matter and spends its perfect Class A detection on the frames the attacker left clean. Abstention does not preserve the static-locus win; it quarantines that win away from the attack.

Third, **the trusted-channel regress contradicts replay.** The only stated survival path back to Class B is an intervention channel the adversary cannot see and cannot answer, plus an audit of that channel. Under SHA-identical reruns the channel’s parameters are either in the transcript or they are not. If they are in the transcript, a transcript-level adversary — the same adversary who already built the renderer — reads crop, gain, and offset before answering, and the channel is not unobservable. If they are not in the transcript, a third party cannot recompute the expected response, the 3× SHA-compare does not verify the check, and the mechanism is illegal in this program. There is no third option where the audit of the channel is public and the channel contents stay secret: the audit has to mention what it audited. Unobservability and byte-identical verification are mutually exclusive. The narrowed core’s Class B patch is not an open engineering item. It is empty.

P10 cannot plug this hole from outside either: invoking P10 on P7’s abstain is a hybrid interaction, handled below, and it imports P10’s own dead assumption.

**Concede.** Against a genuinely non-adaptive, single-frame injector who does not index the perturbation vocabulary, the static locus is perfect as measured (Class A 0/120). That measurement is real. It is also the entire remainder.

**Native objector.** Agree: the asymmetry “must answer in real time” is false; the command is on the bus; the renderer is O(1) after one build; composition does not reprice; 120/120 ends “priced, not impossible.” Agree that the claim narrows to non-adaptive injectors. Disagree on the survival condition. The native objector left “unobservable, unanswerable channel, with its own preregistered audit” as an achievable requirement. I close it: under the program’s determinism and replay rule that audit cannot exist without either leaking the channel into the transcript or exiting the set of legal mechanisms. The native mind-changer (“a Class B battery where the fake is caught”) is the right measurement and, as they said, the probe already says it will not fire — including against the narrowed core, once the adversary is allowed the transcript the verifier gets.

**Survival condition.** A Class B catch that holds when the adversary receives exactly the verifier’s transcript, the schedule is an in-transcript pure function, and no hidden state exists outside the hash. Absent that, the narrowed core does not survive as a deployable locus; the Class A number survives only as a battery note about lazy injectors.

**Mind-changer.** One battery: perturbation-consistent adversary, equal read set, deterministic in-transcript schedule, no side secret. Install rate substantially below 100% at fixed honest-loss ≤15% with no abstain-on-complex carve-out. If the catch requires hidden parameters, it does not count.

## H-PAM-8 — narrowed core (continuous path-independence audit, not a warrant)

**Steelman.** Dropping the warrant was correct. premium_bp = 0, effective-n = 1.0, 600/600 agreement with SHARED_SOURCE is the fusion-layer result: one lie above the split is consistent in both paths by construction, and neither path’s integrity is touched. What remains is the audit as a hybrid component. The audit is weaker than the narrowed writeup claims, for a named reason: **synthetic residual independence.**

The audit does not observe causal ancestry. It observes statistics at its taps. The cheapest way to satisfy a continuous independence attestation is a shared semantic payload plus independent noise per modality, generated in the adversary’s renderer, injected at or above fusion, or pushed down both drivers. Disjoint residuals, shared lie. The audit’s feature set — disagreement, clock skew, noise correlation — reports INDEPENDENT. Build cost is one noise model, paid once. Every subsequent fused percept inherits a passing attestation. The native attack stopped at “inject above the split so both paths agree and the audit says SHARED_SOURCE.” That catches the lazy common-cause. It does not catch the attacker who wants the audit to pass. Passing is the goal once the audit is a gate inside the hybrid rather than a post-hoc lamp.

There is a bind if you try to close this. Real hardware shares firmware, clocks, power rails, and a chassis, so honest paths are statistically dependent. Tighten the audit until synthetic residuals fail and same-chassis honest runs start tripping SHARED_SOURCE or eating the honest-loss bar. Loosen it until honest chassis pass and synthetic residuals pass with them. The audit cannot, on features computable from the two streams alone, separate “one lie plus forged independence” from “two sensors on one robot.” That separation was the warrant, and the warrant is already dropped; the audit inherits the same indistinguishability for any adversary who forges the features.

**F8a still applies inside the hybrid**, stronger than in the warrant era. Unimodal-spoof-into-the-fallback was an attacker choice when P7 was a named carve-out. In the commit rule, fallback-to-P7 on a bad audit is policy. The attacker no longer routes around P8. A passing audit is the more useful route, because it licenses fusion. So the rational adversary buys synthetic independence and never enters the fallback. The premium quadrants remain a laziness meter.

**Concede.** Evidence-independence as a logged causal-path property is real (the 1,200/1,200 result), and forcing SHARED_SOURCE to be a first-class outcome is the right instrumentation. The audit is the only component of the three that does not need a secret and is legal under SHA-replay. That is why it ranks first below — as a tripwire, not as attestation.

**Native objector.** Agree: disjoint-by-construction is a build-time assertion; the deployed common causes are firmware, clock, power, mount, and one adversary; fusion-layer injection solves consistency once; the probe’s premium_bp = 0 is decisive against the warrant; F8a makes the fallback attacker-chosen; the premium measures laziness. Agree the audit is the valuable remainder and that Class C belongs in the battery as a named killer. Disagree that “continuous per-deployment independence attestation” is a survival condition that can be satisfied. Attestation of taps is not attestation of ancestry. The native mind-changer (premium > 0 on Class B vs Class A with the audit genuinely passing) tests the dead warrant. The live question is whether the audit rejects synthetic residuals. They did not pose that battery.

**Survival condition.** A preregistered feature set that rejects shared-semantic-payload plus independent per-path residuals, with honest same-chassis loss inside the K6 bar (≤15%), evaluated per deployment rather than against the design doc. If no such feature set exists without exceeding honest-loss, the audit survives only as a tripwire for un-noised shared source, and must not be wired as a license to trust fusion.

**Mind-changer.** Class C synthetic-residual battery: one semantic lie, independent noise per modality, injection above the split, audit required to fire, honest chassis controls required to stay under the abstain bar. A catch at the preregistered rate on that battery, and only that battery, reverses me.

## H-PAM-10 — narrowed core (Class-S specialist; 5 bits on driver-level spoof)

**Steelman.** The specialist claim is: coverage may be 25%, the general gate is dead, but on the driver-level spoof class P10 is the only nonzero discrimination in the family (5 bits vs P7’s 0), so it earns the fallback seat for covered classes, blocked from promotion by F10c and by the named ledger-read assumption.

The 5 bits do not survive contact with the verifier’s own interface.

**Equal-read collapse.** The verifier accepts the check iff the world outcome matches a prediction that is a function of (action, parameter, world model). The action is observable — it is a physical emission. The world model is not a secret: a driver-level adversary who can spoof plausibly already has a model good enough to predict what the verifier will call lawful, or they fail every other battery too. The only remaining secret is the parameter. The parameter must be available to the verifier, hence it is in the ledger or it is recomputed from the transcript. A driver-level adversary is defined as sitting on the driver stack the ledger is read through; the wall already falsified “the adversary cannot read the ledger.” Replay makes it worse: byte-identical verification publishes every input to the pure function. Set the adversary’s read set equal to the verifier’s and the prediction is computable by both. Discrimination goes to 0. The 5 bits are the entropy of an information partition the battery imposed and deployment plus replay remove. “Incomputable from a byte-spoof while the parameter stays unpredictable” concedes the whole claim in the subordinate clause. Under zero randomness the parameter does not stay unpredictable. A committed seed in the transcript is not unpredictability; it is a constant the renderer closes over.

**Coverage is attacker-selected.** 25% < 50% already killed the general gate. Specializing does not change the quantifier. The attacker presents the lie in the uncovered three-quarters. “Named as uncovered” is an inventory of holes. A fallback that is absent on the attacker’s chosen class does not complement anything.

**F10c is the right block and it is not a formatting gap.** “Manipulation succeeds zero times” cannot be given a testable formulation that P10 can pass, because P10’s evidence is a world-delta and the adversary’s win condition on this surface is a world-delta. Budgeted and reversible does not help: a reversible reach still displaces, still reveals that a check fired, and still localizes the agent. Any formulation that exempts “deltas caused by the check” has exempted the attack. Any formulation that counts them fails the mechanism by design. The open item “needs a testable formulation before promotion” should be closed as unsatisfiable inside this locus, not left procedural.

**Check-firing oracle.** Even restricted to covered classes, firing is informative. Covered classes are enumerable. The pattern of which checks fire is a belief oracle about the agent’s class assignment. Rarity does not hide this; rarity is the signal.

**Concede.** If you artificially keep the parameter out of the adversary’s read set and you only score byte-spoof prediction error, P10 is the only family member with nonzero numbers on that class (5 vs 0). World-outcome evidence is not a pure function of the spoofed bytes alone under that partition. I concede the arithmetic. I do not concede that the partition is a legal deployment.

**Native objector.** Agree: the check is remote control; F10c is untestable as written; reversible does not bound harm; 25% coverage is fatal to the general claim; 5.0× cost and serial action make delay binding; the ledger-read assumption is load-bearing and already in conflict with the wall; naming uncovered classes is bookkeeping. Disagree on the concession that the 5 bits are a real specialist remainder worth a hybrid seat. They are real inside the battery’s read partition and void once that partition is equalized, which determinism and SHA-replay do automatically. The native survival condition (coverage ≥ 50% and literal-zero F10c and the ledger assumption “attacked as named”) still treats the ledger assumption as something that might survive attack. I treat the replay rule as the attack already succeeding. Their mind-changer (Class M, zero elicitations, full repertoire) is right and, correctly scored, counts check-caused deltas as elicitations — in which case the mind-changer is a demand that P10 stop being P10.

**Survival condition.** Nonzero discrimination on Class S when the adversary’s read set equals the verifier’s, the parameter schedule is a pure function with no randomness, repertoire coverage is whatever you still claim, and check-caused world-deltas count against F10c. I do not believe that conjunction is nonempty. If the program exempts P10 from the determinism rule, say so; under the rule as written the specialist core is dead.

**Mind-changer.** Equal-read, deterministic-schedule Class S battery with discrimination reliably above 0, and a simultaneous F10c score that counts physical deltas during checks and still hits the preregistered bound. A nonzero that depends on a hidden ledger does not change my mind.

## Hybrid — new attacks

The commit rule says P7 (static/unimodal) + P10-specialist (covered driver-level) + the independence audit, justified because the loci’s failures are complementary and non-overlapping, and because neither locus alone survives Class B/C. “Both die alone” does not entail “together they live.” That inference is the hole. Complementarity was assumed from pairwise batteries. It was not measured. The following adversary classes kill the composition as a composition. The native objector did not field them.

**1. Class H, blind-quadrant conjunction.** Each locus’s measured corpse has a blind quadrant, and the quadrants intersect.
- P7 is blind on adaptive answers and, after the honest-loss patch, on anything the complexity predicate abstains.
- The audit is blind on synthetic residuals (shared lie, independent noise) and, by the dropped warrant, on fusion-layer semantics.
- P10 is blind on the uncovered 75% and on every class it is not invoked for.

One adversary, one artifact: fusion-layer semantic lie, independent residual noise per modality so the audit returns INDEPENDENT, scene features set so P7 abstains, action class chosen from the uncovered set so P10 never arms. No locus is defeated inside its strong quadrant. Each is left uninvoked or satisfied. Install rate of this class is the hybrid’s real number, and nothing in D1 or D4 measures it. Call the class Class H. Predicted install: the same order as Class B’s 100%, because every active check is in its tau-inert or out-of-coverage regime and the audit is given the statistic it wants.

**2. Handoff inversion.** Wire the audit’s success and failure into policy and both wires are attacker-chosen.
- Audit passes (synthetic residuals) → hybrid trusts fusion → Class C lands. The audit’s “success” is the license.
- Audit fails (SHARED_SOURCE, including a deliberately crude common-cause the attacker can toggle) → policy falls through to unimodal P7 → attacker is now in P7’s Class B regime, already measured at 100% install, tau-inert.

The native F8a objection said the fallback is a carve-out the attacker chooses. In the hybrid the carve-out is the commit rule. A failing audit is no longer evidence the defender caught something. It is a routing bit into the locus with zero Class B discrimination. Complementarity would require that routing into P7 be safe. The probe says routing into P7 is how Class B gets admitted.

**3. Abstain-policy bind.** F7b at 30% forces a wiring choice the pairwise results hide.
- Abstain → provisional admit: the attacker lives in complex scenes and the lie is admitted at low confidence. That is admission.
- Abstain → P10: 30% of honest complex scenes pay 5×, emit observable actions, and, if any of those scenes are covered classes, farm the parameter. On attack traffic the attacker forces the complex predicate to mint P10 invocations on demand.

Either wire destroys a side of the hybrid. There is no third wire that is both deterministic and non-admitting. This is an interaction effect, not a per-locus failure mode.

**4. Parameter farming through the specialist seat.** Covered classes are a menu. The attacker triggers covered-class checks to observe action plus outcome, recovers the pure function’s parameter schedule (deterministic, so a short prefix fixes the rest), then uses the recovered schedule on later byte-level spoofs of the same class. P10’s 5 bits are then a one-time disclosure, not a per-check warrant. Serial world actions make the farm cheap relative to the attacker’s goal and expensive relative to the agent’s actuator budget — a availability hit on the agent that the discrimination-per-cost ratio (136 vs 11) never priced, because that ratio scores detection yield, not invocation externalities.

**5. Determinism as a single kill for both intervention loci.** P7’s Class B patch needs an unobservable channel. P10’s 5 bits need an unpredictable parameter. The hard rule says the entire hybrid is a pure function with public reruns. A pure function’s intervention schedule is precomputable by anyone who holds the transcript. The hybrid’s two “active” loci both require a secret the legality rule forbids, and the one component compatible with the rule — the audit — is satisfiable by synthetic residuals. The commit rule assembles two mechanisms that are illegal in their strong form with one mechanism that is legal in its weak form, and calls the assembly a warrant.

**6. Replay-split.** If the implementation cheats the hard rule — secret channel or secret ledger outside the hash — then the 3× SHA-compare verifies a different object than the one that admitted the percept. The admitted decision depends on unaudited state. That is a hidden warrant, which this program’s own standard rejects. The hybrid cannot both verify and stay unanswerable.

Predicted picture: there is no adversary who must beat P7 and P10 and the audit. There is an adversary who shops in the intersection of the blinds, and the handoff policy walks them there.

## Verdicts

**H-PAM-7 narrowed: DEAD.** What died: the claim that the static-frame locus plus a trusted intervention channel is an achievable Class B audit under determinism and SHA-replay. Class A 0/120 remains a true battery fact about non-indexing injectors and is not a locus you can hand work to. Abstain-to-provisional, required by the 30% honest-loss, deletes the locus on the frames that matter.

**H-PAM-8 narrowed audit: LIVE narrowed, tripwire only.** What lives: a continuous detector of un-noised shared source, legal under replay, already shown to report SHARED_SOURCE. What died, and stays dead: using a pass as attestation of causal independence or as a license to fuse. Synthetic residuals kill any stronger reading. I do not restore the warrant.

**H-PAM-10 specialist: DEAD.** What died: the 5-bit specialist remainder as a deployable Class-S fallback. It is an artifact of a strictly weaker adversary read set. Equalize reads, apply zero-randomness, and count check-caused deltas in F10c, and the remainder is empty. Coverage at 25% was already fatal to any claim that the fallback is usually present.

**D1 hybrid: DEAD.** What died: the inference from complementary pairwise failures to joint coverage. Class H (blind-quadrant conjunction), handoff inversion, the abstain-policy bind, and the determinism/secrecy contradiction kill the assembly even if you stipulate every pairwise measurement the commit rule cites. “Neither alone suffices” was never evidence that both together suffice.

## Ranking — most likely to survive its objector

1. **H-PAM-8 audit, tripwire reading only.** Only piece compatible with byte-identical replay, already measured, no secret required. Survives by being demoted, which has already happened. Least likely to be restored to a warrant, and that is the correct outcome.
2. **H-PAM-7 Class A residue, not the narrowed channel claim.** The 0/120 fact will replicate against lazy injectors. It will not grow a legal Class B channel. Ranked above P10 only because the residue is real without a secret.
3. **H-PAM-10.** Least likely to survive. Its unique number requires the information partition the program’s hard rule destroys. I reverse the native ranking, which ordered “measured mechanism with a boundary” and treated the 5 bits as specialist value.

Native ranking was 7 > 10 > 8 on the grounds that 7 has a real boundary and 8’s warrant is dead. I agree 8’s warrant is dead. I rank the legal tripwire above two intervention claims that are only alive inside an illegal secrecy assumption.

## D1 and D4 — design

Both experiments are well-built pairwise batteries and were then over-read into an existence proof for the hybrid. That over-read is the design failure.

D1 asked which trust locus wins, 7 against 8, and correctly grew a Class C cell. It misses the actual crux in two ways. First, it never runs Class H: one artifact that is simultaneously fusion-layer, synthetically independent, complexity-abstaining, and outside P10’s cover. Pairwise death does not locate the conjunction. Second, it scores P7’s intervention as if a hidden channel could be both audited and replayed. The deciding contrast is not “P7 locus vs P8 locus.” It is “any intervention whose parameters sit in the SHA transcript vs an adversary who is handed that transcript.” Under that contrast D1’s winner is not a trust locus at all; the only legal survivor is the audit tripwire, which D1 has already stripped of warrant status. Committing a hybrid from D1 copies the untested complementarity step into the architecture.

D4 asked discrimination-per-cost and awarded the intervention locus to P7 (136 vs 11), with P10 as Class-S fallback. The ratio prices detection yield per check. It does not price handoff externalities: honest-scene actuation at 30% abstain, parameter farming, check-firing as a class oracle, or the availability cost of serial world actions the attacker can mint by forcing the abstain predicate. Worse, the 136 and the 5 bits are computed under unequal read sets. The correctly designed D4 equalizes the adversary’s read set with the verifier’s, forces a pure-function schedule, and rescores. On that design I expect P7’s Class B discrimination back to the measured 0 and P10’s 5 bits back to 0, at which point discrimination-per-cost is undefined or zero for both and there is no winner to hand the locus to. D4 as run answers “who looks better when the attacker cannot see the verifier’s inputs.” The debate’s own hard rule is that those inputs are public. The experiment misses the crux by construction, and the fallback seat it awarded is the seat Class H simply declines to sit in.

The single hybrid measurement that replaces both over-reads: Class H install rate, adversary read set equal to the verifier, deterministic transcript, no abstain carve-out hiding the miss, honest-loss reported beside it. Near 100% install kills the commit rule. A low install at honest-loss ≤15% would be the first evidence the loci actually complement, and it has not been taken.
