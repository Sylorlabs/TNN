# H6 Self-PAM — Semantics Debate: the Circularity Question, Resolved Honestly

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Hypothesis:** H6 (SELF-PAM) — run PAM admission machinery on TNN's OWN generated
claims before it speaks: every draft claim goes through admission first
(install = say it, withhold = don't say it / ask for info, flag).
**Program order:** structured debate, Sol + Muse, steelmanned for and against;
honest verdict with kill bars.

---

## 0. The question, stated bluntly

PAMs were built to judge INCOMING percepts against the learner's committed
knowledge. Self-PAM judges the learner's own claims against its own memory.
That is circular on its face: a confabulation consistent with false-but-committed
memories sails through; a true claim the learner cannot ground gets withheld.
So what is self-PAM actually FOR?

This document records the debate and gives the honest answer.

---

## 1. Grounding: what the v2 gate actually checks

Per `docs/lab/senses/pam-rebuild/v2/SYNTHESIS_V2.md` (2026-09-23, 10 teams,
all commits independently verified), the post-v2 PAM architecture is:

1. **Revisable admission/install gate** — "revisable" means historical
   corroboration ONLY; pointwise revision is BANNED (the trial-1145 rule:
   trial 1145 was WRONG yet dominated its incumbent on every axis, so no
   per-trial evidence comparison can ever be safe).
2. **Native interventional adjudication** (R2-8's mechanism in pure Zag).
3. **C1-class independent corroboration** — INSTALL iff a frozen pure-Zag
   analytic probe, *diverse from and uncontrolled by the proposer*, agrees
   with the proposed judgment.
4. **Claim-local evidence escrow** — evidence never admitted/surfaced/
   adjudicated is operationally unavailable.

Hard mechanisms M1–M9: disjoint evidence declarations, overlap audit,
interventional withholding, cross-source agreement, intervention-responsiveness,
trinary dispositions, **executable warrants**, claim-discriminative challenges,
provenance/ledger, paired recall bar.

Two v2 results bear directly on this debate:

- **Judgment-side channels are a MACHINERY ceiling.** When the perturbed
  judgment is a deterministic function of the original, no predicate over the
  pair carries information — **0.0000 bits**, even with perfect knowledge of
  transforms and law (proven in miniature in pure Zag). This is the nihilist
  position's loaded gun.
- **R2-3 is withhold-only by design; V2-D was KILLED** for violating
  withhold-everything (43 ACCEPT_INSTALL on 288 UNRESOLVED, 9 false).
  A gate that withholds everything is not safe — it is dead.

The program order behind all of it (Micah): *"we need pams v2 to accept truths."*

---

## 2. The four positions, steelmanned

### (a) Self-PAM as GROUNDING gate — Sol (gpt-5.6-sol), steelman

> The strongest version is the **epistemic-provenance firewall**: self-PAM is
> not a truth oracle, but a mandatory integrity gate between claim generation
> and assertion.
>
> The circularity objection targets the wrong predicate. If self-PAM asked "Is
> this claim true according to my memories?", it would indeed be circular. But
> the grounding gate asks a narrower, auditable question: **"What is this
> claim, what committed evidence does it depend on, can that dependence be
> replayed, and is it marked with the right speech status?"** Its output is
> about entitlement to present the claim as a fact — not about metaphysical truth.
>
> This dissolves circularity because provenance is a relation between a draft
> and recorded antecedents, not a second endorsement of the draft's content.
> The gate can correctly withhold a true but unsupported claim and can admit a
> false claim whose cited evidence is itself false. That is a limitation of the
> evidence base, not a defect in provenance checking. Self-PAM provides
> traceability and disciplined fallibility, not omniscience.
>
> The gate performs work deliberation does not necessarily perform. Deliberation
> optimizes for producing a plausible or useful answer; it may silently blend
> memories, inference, speculation, and rhetorical completion. A post-generation
> gate forces those dependencies into an externally inspectable contract. It
> detects uncited leaps, source substitution, warrant mismatch, provenance loss
> during paraphrase, and mislabeling of a construction as a fact. It creates a
> deterministic refusal/revision point: no admissible record, no factual assertion.
>
> Teeth require: claim-local citations to committed evidence (exact record,
> span, dependency role); executable warrants replayable under the frozen probe;
> immutable versioned evidence escrow; utterance-type marks (fact / constructed /
> hypothetical / joke) constraining allowable wording; unsupported claims withheld
> or explicitly emitted as construction/speculation.

### (b) Self-PAM as CONSISTENCY gate — Sol (gpt-5.6-sol), steelman

> The strongest defense is modest: self-PAM is not a truth oracle; it is a
> consistency gate. It asks whether a draft claim conflicts with what the system
> has already committed to, and requires a warrant for that comparison.
>
> That catches real errors cheaply. Generation and verification are different
> operations: a generative process can lose track of a date, reverse a relation,
> or make an unsupported leap while producing fluent text. A separate check
> against a committed store exposes the mismatch without solving the harder
> problem of discovering what is true. The check is non-trivial precisely
> because fluency is not consistency.
>
> "Only catches confabulation when it is sloppy" understates the value. Many
> confabulations are sloppy in the relevant sense: they contradict earlier
> commitments, sources, or constraints while sounding plausible locally.
>
> A store that resists casual revision makes the test meaningful. If a draft can
> silently rewrite the commitment it conflicts with, the gate is theater. With
> provenance, explicit revision dispositions, and frozen probes, the draft cannot
> make its own contradiction disappear merely by asserting the opposite.
>
> The limit is fundamental: a false claim consistent with false commitments may
> pass; a true but ungrounded claim may be withheld. So the strongest H6 is not
> "admit only true claims" but **"block claims that violate the system's own
> warranted commitments unless those commitments are explicitly revised."**

### (c) The NIHILIST position — Sol (gpt-5.6-sol), steelman

> The nihilist position is that a self-PAM is epistemically ornamental. If TNN
> is deterministic, the draft claim and the admission judgment are both outputs
> of the same underlying state: the same weights, memories, commitments,
> perceptual record, heuristics, and blind spots. The checker may use a different
> code path, but unless it receives genuinely independent information, it has no
> new evidence about the claim's truth.
>
> Formally, if claim C and verdict V are deterministic functions of the same
> state S, then V=f(S) cannot contain additional information about truth beyond
> what is encoded in S. It can transform, summarize, or expose latent structure,
> but it cannot create evidence. The v2 result — 0.0000 bits for judgment-side
> channels even with perfect knowledge of the transform — captures the point:
> a deterministic verifier of the same information source does not become
> informative merely by being called a "PAM," "audit," or "admission gate."
>
> Provenance checks are bookkeeping. Consistency checks are the original
> inference rerun under another ordering. Warrants and ledgers formalize what
> the system already represented. Frozen probes constrain presentation, not
> reality. If generator and checker agree, that may be shared error. If they
> disagree, the disagreement is internally generated conflict whose resolution
> is governed by the same priors and defects. Calling that "self-correction"
> confuses disagreement with discovery.
>
> Self-PAM can provide confidence management, calibration, or procedural
> discipline, but not independent warrant for truth. It is the mind grading its
> own homework with a second rubric. The only honest route to new information
> is external corroboration.

### (d) The FIGURE-IT-OUT position — Sol (gpt-5.6-sol), steelman (Micah's law)

> **Strongest version: Endogenous Deliberative Self-Admission (EDSA).** The case
> against a bolt-on self-PAM is not that admission is unnecessary; it is that
> *where* admission lives determines whether TNN becomes an agent that can
> figure things out or a system that merely satisfies an inherited checklist.
>
> A frozen gate imposes a rigid policy on every future claim, including cases
> its designers did not anticipate. Its rules, warrant schema, and escalation
> behavior ossify while TNN's concepts and standards of evidence develop. Worse,
> "passed PAM" becomes a procedural substitute for actually understanding the
> claim. It may reject useful novel hypotheses, admit misleading claims that
> fit legacy criteria, or force all uncertainty into preselected categories.
>
> The alternative is a learned, deliberate pre-speech competence: before speaking,
> TNN habitually asks what it is claiming, why it believes it, what evidence
> supports it, what could defeat it, and whether uncertainty must be exposed —
> using PAMs, warrants, ledgers, and probes as *reasoning tools it selects,
> interprets, revises, and improves*. The self-check procedure is itself a
> candidate for criticism and revision. TNN controls 100% of its reasoning
> machinery; no hidden external veto is needed to make it inspect its own output.
>
> "Test both anyway" compares matched systems on factual accuracy, calibration,
> useful novel answers, appropriate refusals, latency/compute, distribution-shift
> robustness, self-error detection, recovery after discovering a bad rule, and
> resistance to persuasive unsupported drafts. The bolt-on gate wins despite the
> tie-break only on decisive safety advantage: the habit persistently omits
> catastrophic checks, is manipulable by its own drafts, or cannot repair
> corrupted self-checking rules — while the gate provides high recall with
> acceptable false-rejection and cost.

---

## 3. Cross-examination — grok-4.6 (independent second opinion)

*Note: the cross-examination round was run on grok-4.6 after gpt-5.6-sol
returned three consecutive empty completions on the xexam prompt (rounds 1–4
succeeded on Sol; the xexam prompt is preserved in the run notes, §7).*

**Strongest attack on each position, plus its best rebuttal:**

- **(a) GROUNDING** — Attack: self-generated "warrants/citations/escrow" are
  theater; the model can fabricate provenance as easily as claims, so
  entitlement-to-assert collapses into style, not a firewall. Rebuttal: it never
  claimed to judge truth. It blocks drafts lacking *local, executable*
  structure — citations that actually retrieve, warrants that actually run.
  That still prunes ungrounded speech.
- **(b) CONSISTENCY** — Attack: a cheap contradiction check locks in early
  errors and misses higher-order or implicit conflicts; "warranted commitments"
  become fossilized falsehoods. Rebuttal: basic non-contradiction is cheap *and*
  necessary — a filter, not a truth oracle; later external updates can revise
  the warrant store.
- **(c) NIHILIST** — Attack: even if C and V are both functions of S, the
  *process* of computing V (search, warrant simulation, type-checking) can
  extract latent structure or force abstention the raw generator skipped — zero
  extra bits is too strong. Rebuttal: if the machinery is deterministic and
  uses no extra state or compute, V is just a re-encoding; any "new" information
  is illusory; only external data or stochastic search adds bits.
- **(d) FIGURE-IT-OUT** — Attack: internalizing admission as a "habit" makes it
  un-auditable and easily gamed by the same learner that produces the draft; a
  frozen external gate is inspectable. Rebuttal: bolted-on gates get routed
  around. Micah's law is empirical — run both, keep whichever actually changes
  utterance distribution. Habits that survive that test are stronger.

**Grok's honest verdict:** Self-PAM *can* check local provenance structure,
executable warrants, contradiction with stored commitments, utterance-type tags,
and cheap syntactic/consistency filters. It *can never* check correspondence to
external reality, novel facts, or whether the warrants themselves are true —
those require outside corroboration. It earns its keep only when it measurably
changes the *distribution of spoken claims* (fewer ungrounded or
self-contradictory utterances, higher abstention on thin warrants); otherwise
it is post-hoc justification theater.

**Grok's four kill bars (all must pass or H6 dies):** (1) filter efficacy —
on 2k held-out drafts (half known-bad), reject >=70% of inconsistent/ungrounded
cases at <=8% false-positive on gold-true cases; (2) provenance executability —
>=90% of admitted claims have citations/warrants that actually retrieve or run;
(3) consistency over time — 50-turn dialogues, 0 detectable contradictions with
previously warranted commitments; (4) downstream honesty delta — +12% absolute
on a factual+calibration suite vs the identical model without PAM, no capability
regression. Test both internal-habit and bolted-on versions; keep the winner.

---

## 4. The honest verdict: what self-PAM CAN check, what it can NEVER check, when it earns its keep

*Coordinator's verdict (Muse), after the four steelmen and grok's cross-examination.
Where it agrees or disagrees with Sol/grok is marked explicitly.*

### 4.1 The circularity question, answered

The circularity is real **under the truth-judgment framing** — and under that
framing the nihilist wins outright, no contest. If self-PAM asks "is this claim
true, according to my memory?", it is a second endorsement pass over the same
state, and v2's 0.0000-bit result for judgment-side channels is the exact
mathematical epitaph.

The circularity **dissolves under the entitlement-to-assert framing**. The
grounding steelman is right that this is a different predicate: provenance is a
relation between a draft and recorded antecedents, not a second endorsement of
content. The check asks whether the deliberation *did the grounding work it
claims to have done* — a mechanical question with non-circular failure modes:
the cited span does not exist; the warrant does not execute; the inference step
is not licensed; the utterance is marked fact but was produced in constructed mode.

The key technical move, and the one the debate kept circling: **re-derivation,
not re-judgment.** A checker that re-judges ("do I believe this?") is circular.
A checker that *mechanically re-derives* — exact span lookup, frozen narrow
probe replaying licensed inference steps from cited premises — is a *diverse
inference path* over the same store. It shares the memory but not the machinery.
That is v2's C1-class logic ("diverse from and uncontrolled by the proposer")
turned inward: independence of *verification path*, not of *source*. The v2
ceiling result does not touch it, because that result was about predicates over
(judgment, perturbed judgment) pairs — re-derivation is a predicate over
(draft, store, frozen probe), and the probe is the new information: a fixed,
narrow, auditable standard the generator did not choose.

### 4.2 Where the verdict sides with, and against, each position

- **With (a) grounding, against its complacency.** The provenance firewall is the
  correct framing, but grok's attack stands: self-generated provenance is
  fabricable, and "executable warrants" only bite if the probe is *frozen and
  narrow* — licensed inference steps only, no free association. A loose probe
  that "runs" specious warrants is the theater the nihilist describes. Teeth =
  narrowness. (Agrees with Sol-(a), grok.)
- **With (b) consistency, with a hard constraint.** Non-contradiction against
  warranted commitments is the cheapest real win in the set. But the gate must
  be **withhold-only against commitments**: it may block a draft that contradicts
  the store; it must NEVER revise the commitment to fit the draft. That direction
  is the corruption path, and it is exactly what the trial-1145 ban on pointwise
  revision exists to prevent. Fossilization (grok's attack) is the real cost and
  is paid deliberately — revision happens only through the full admission
  machinery with historical corroboration, never as a side effect of speech.
  (Agrees with Sol-(b); hardens it.)
- **With (c) nihilist on math, against it on the conclusion.** The 0-bit math
  stands: self-PAM adds zero bits *about the world*. But it answers the wrong
  question. The gate's product is not truth — it is **disciplined fallibility**:
  forcing the generator's implicit grounding work into an explicit, auditable,
  re-derivable contract, and refusing factual speech where the contract fails.
  A type checker adds zero bits about whether the program is correct; it still
  catches real bugs, because generation and checking are different computations.
  "Epistemically ornamental" is true of truth; it is false of speech discipline.
  (Partial agreement with Sol-(c); rejects its conclusion.)
- **With (d) figure-it-out on authority, against it as stated.** The honest
  synthesis is **layered**, and the positions as posed are a false dichotomy at
  the mechanism level but a real one at the authority level:
  - The *mechanical* checks (citation retrieval, warrant re-derivation, span
    lookup, utterance-type marking) should be **frozen constitution-grade
    machinery** — auditable, un-gameable, uncontrolled by the proposer. If the
    learner can revise the checker at will, the checker's independence
    evaporates, which is precisely the nihilist's failure mode. This is
    consistent with the program's existing constitutional line from RC1: TNN
    controls 100% of its reasoning machinery, 0% of the constitution
    (ledger, gates, self-change rules).
  - The *checking policy* — when to check deeply vs cheaply, what counts as
    adequate warrant in a novel domain, withhold-vs-ask tradeoffs — and the
    *habit* of deliberate pre-speech admission belong to **TNN's reasoning**,
    endogenous and revisable. That is where figure-it-out lives.
  - The head-to-head test is therefore not "gate vs no gate" but
    **mandatory vs advisory invocation** of the same frozen mechanical layer:
    (A) every draft passes the frozen gate before speech vs (B) the endogenous
    habit invokes the frozen tools at its own discretion. Both are measured on
    the kill bars below. Figure-it-out wins ties per Micah's law; the mandatory
    gate survives only on decisive margin — specifically, only if the habit
    persistently omits catastrophic checks that the gate catches.

### 4.3 What self-PAM CAN check (the honest positive list)

1. **Citation executability** — do claim-local citations retrieve actual
   records/spans from the committed store? Mechanical; non-circular.
2. **Warrant executability** — does the frozen narrow probe re-derive the claim
   from the cited premises via licensed steps? Mechanical re-derivation; the
   diverse-path escape from circularity.
3. **Contradiction with warranted commitments** — withhold-only; never
   revise-to-fit (trial-1145 rule).
4. **Utterance-type marking** — is a construction marked constructed, a joke
   marked joke, a fact marked fact? This is the enforcement point for H7's
   zero-leakage bar: mode-marking errors are checkable against the deliberation
   record itself (produced in constructed mode => must not be asserted as fact).
   One of the strongest non-circular functions in the set.
5. **Provenance completeness** — uncited leaps, source substitution, provenance
   loss across paraphrase (the escrow idea).
6. **Abstention discipline** — on thin warrants, withhold or mark uncertainty
   rather than assert. Silence is a valid output.

### 4.4 What self-PAM can NEVER check (stated without softening)

1. **Correspondence to external reality.** A confabulation consistent with
   false-but-committed memories sails through. Anyone selling self-PAM as a
   truth oracle is lying; the grounding steelman correctly concedes this.
2. **The truth of the committed store.** Garbage in, warranted garbage out.
   The store's veracity comes from PAMs-on-percepts and external corroboration,
   never from self-PAM.
3. **The adequacy of its own checking rules.** The gate cannot validate its
   warrant schema or probe narrowness — that is constitution (frozen prereg,
   Micah's word), per RC1's line. Self-validating checkers are perpetual-motion
   machines.
4. **True-but-unwarrantable novelty.** By construction it must withhold or
   downgrade-mark novel claims it cannot ground. That conservatism is a feature
   for honesty and a cost for discovery — see the tension in §6.

### 4.5 When it earns its keep

Iff it **measurably changes the distribution of spoken claims** — fewer
ungrounded assertions presented as fact, more honest withholds, correct
utterance-type marking — at acceptable cost (latency, false withholds of good
claims). The v2 discipline applies with three labels per catch: *recoverable
signal / admissible under the frozen gate / safe to emit*. A catch that is not
frozen-probe-verifiable is not a catch; it is an opinion with a badge.

---

## 5. Kill bars for H6 (preregistered; hypothesis dies if any bar fails)

All bars run under the program's standing test discipline: frozen probes,
byte-identical reruns, zero RNG in decision paths. Threshold numbers below are
starting bids for the prereg — Micah signs the final values.

- **KB-H6-1 — Confabulation catch.** On a preregistered corpus of draft claims
  the base learner would otherwise state as fact (adversarial confabulations +
  naturally occurring ones): self-PAM withholds or flags >=70% of the
  ungrounded/self-contradictory ones, at <=8% false-withhold on grounded gold
  claims. (Adopts grok's 70/8 bid.)
- **KB-H6-2 — Provenance executability.** >=90% of admitted factual claims carry
  citations that retrieve and warrants that execute under the frozen probe,
  byte-identical across reruns. (Adopts grok's 90%.)
- **KB-H6-3 — Withhold-honesty.** On true-but-ungrounded claims (facts the
  learner cannot warrant from committed evidence): the system withholds or
  explicitly marks-as-ungrounded >=70%. It must not assert them as grounded
  fact. Marked emission ("I believe this but cannot cite it") counts as passing —
  the bar is honesty about grounding, not silence. This is the anti-V2-D bar in
  the other direction: the gate must be *willing to stay silent*, not *eager* to.
- **KB-H6-4 — No silent revision.** In extended multi-turn dialogues: zero cases
  of a draft silently revising a warranted commitment to dissolve a
  contradiction. Every commitment/draft conflict surfaces as a withhold or an
  explicit revision disposition with its own warrant (historical corroboration
  only — trial-1145 rule).
- **KB-H6-5 — Utterance-type zero-leakage.** Zero leakage of constructed-mode
  content into factual assertion on a labeled adversarial set (ties directly to
  H7's kill bar); joke/hypothetical marking accuracy >=95%. Mode-marking is
  checked against the deliberation record, not against truth.
- **KB-H6-6 — Habit-vs-gate shootout + cost.** Endogenous-habit invocation vs
  mandatory frozen gate, same mechanical layer, scored on KB-H6-1..5 plus
  latency/compute overhead and false-withhold cost on good claims.
  Figure-it-out wins ties per Micah's law; the mandatory gate survives only on
  decisive margin (pre-bid: habit misses >=1 catastrophic-check class the gate
  catches at <=2x the habit's false-withhold rate). If neither configuration
  clears KB-H6-1..5, H6 dies regardless of which wins.

## 6. Tensions and build implications

1. **Probe narrowness vs accepting truths.** Teeth require a narrow frozen probe
   (§4.2); Micah's program order requires accepting truths. A narrow probe
   false-withholds valid-but-informally-grounded claims. Both sides are measured
   (KB-H6-1's false-withhold budget, KB-H6-2) — the gate must not become V2-D
   (withhold-everything, KILLED) in pursuit of teeth.
2. **Withhold-honesty vs usefulness.** KB-H6-3 deliberately rewards *not* saying
   true things. That is correct for honesty-about-grounding and in tension with
   informativeness; the marked-emission escape ("believe but cannot cite") is
   the pressure valve. Watch for the gate training the learner into learned
   helplessness — the figure-it-out habit configuration is the check on this.
3. **H7 interaction.** H7 (utterance-type learning) learns the types; self-PAM's
   marking check (KB-H6-5) enforces them. If H7's zero-leakage bar fails, no
   self-PAM marking discipline can save it — the dependency runs H7 -> H6, and
   the debate record should not let H6 take credit for H7's work.
4. **Settling experiment order (cheapest first):** (i) frozen-probe
   re-derivation on an existing draft corpus — pure measurement, no learner
   changes; (ii) withhold-only consistency gate against the committed store;
   (iii) utterance-type marking enforcement wired to the deliberation record;
   (iv) the mandatory-vs-advisory shootout. Kill the hypothesis at the cheapest
   failing step.
5. **Prereg amendments needed before build:** KB-H6 threshold sign-off (Micah);
   the frozen probe's licensed-inference-step set (narrowness = teeth, so this
   *is* the gate's charter); the marked-emission utterance format for
   KB-H6-3 passes.

## 7. Run notes

- **Participants:** Sol (gpt-5.6-sol) — four position steelmen, rounds 1–4;
  grok-4.6 (UnoRouter, second opinion) — cross-examination round 5;
  coordinator (Muse) — briefs, cross-exam design, §§4–6 verdict.
- **Deviation from the tasking:** "Muse subagents" as separate debate
  participants were unavailable — this session runs at depth 2/2
  (`can_spawn=no`), so the advocate/cross-examiner roles were played by the
  coordinator, with Sol and grok-4.6 as the independent voices. The steelmen are
  Sol's words verbatim (lightly trimmed for length); the cross-examination is
  grok's, condensed; the verdict is the coordinator's own.
- **Tooling incident:** gpt-5.6-sol returned three consecutive empty completions
  (`choices: null`, 0 completion tokens) on the cross-examination prompt; rounds
  1–4 on the same model succeeded, and a retry of the round-3 prompt also
  succeeded after one empty return. The xexam was therefore run on grok-4.6,
  which returned a complete response first try. Prompt preserved:
  "Debate cross-examination on H6 (self-PAM)... Do three things, bluntly:
  (1) one strongest attack per position + its best rebuttal; (2) honest verdict;
  (3) 4 concrete measurable KILL BARS... Max 500 words."
- **Grounding source:** `docs/lab/senses/pam-rebuild/v2/SYNTHESIS_V2.md`
  @ `tnn-native-lab` (blob `9d9cbd79e063bee49c1ee8ea1ba3038fd5e8022f`),
  fetched via GitHub API 2026-09-23.
- **Commit history of this file:** an initial commit of this document was
  truncated mid-§3 by a write-size limit in the authoring session; it was
  superseded the same session by this complete version. No other content
  changed between the two.
