# DEBATE RECORD — Source-Trust Forks (K / L / S)

**Status:** FROZEN 2026-09-23. Fork crews must read and address the must-address items in §9 before claiming verdicts.
**Program:** SOURCE-TRUST FORKS PROGRAM — debate crew (Sol + Muse).
**Tasking:** Structured debate, FOR and AGAINST each design. No building, no testing — debate and record only.

## 0. Provenance of this record

- **The question:** How should TNN represent TRUST IN INFORMATION SOURCES?
- **Micah's original idea:** TNN carries trust per source as a scalar 0→1 (e.g. 0.36), hand-settable.
- **Micah's self-correction (standing directive):** SCRAP THE KNOB — "as a human I don't have knobs, I just learned myself." Trust must be learned by TNN, part of TNN, not a hand-set dial.
- **The three forks** (built and tested head-to-head by separate crews under a separate frozen prereg):
  - **Fork K (knob):** explicit scalar trust per source (0→1), hand-set initial value + mechanical update rule. The baseline to beat.
  - **Fork L (learned):** no hand-set value; trust EMERGES from a per-source track record TNN builds from its own experience. Learned, not dialed.
  - **Fork S (structural):** no scalar at all; trust as structure — provenance graph + corroboration history. Admission reads the record directly, never a collapsed number.
- **Debate participants:**
  - Two Sol-model opinions via UnoRouter (`gpt-5.6-sol`) were tasked: Sol-A argued as devil's advocate FOR Fork K / AGAINST the no-knob designs (full opinion recorded, §5); Sol-B was tasked to steelman Fork L but **could not be retrieved** — six attempts over ~25 min all returned empty provider completions (`choices: null`); documented in §6 with a coordinator re-attempt action. The Muse role-separated rounds (§3a/§3b) cover Sol-B's brief in substance.
  - Muse positions: a single agent ran explicit role-separated rounds — a genuine FOR case and a genuine AGAINST case for each fork, each steelmanned as if argued by a separate disciplined Muse instance (§2–§4). No strawmanning: each AGAINST case attacks the fork's actual best arguments, and the synthesis (§7) records where the debate genuinely resolved vs. where it deadlocked into testable predictions.

---

## 1. Definitions the debate settled on

Before arguing, the rounds fixed terminology, because half the disagreement was semantic:

1. **A "knob"** is not a number. A knob is a parameter whose value embodies *a human's theory of how trust should work*, placed where TNN cannot change it. The scalar is innocent; the hand is guilty. (Anti-knob criterion, full form in §7 Q2.)
2. **"The number"** in Q1 means a *persistently stored, per-source collapsed scalar* used at decision time — not a transient quantity computed mid-deliberation. All three forks compute transient quantities; they differ on what is *stored*.
3. **Trust vs. truth:** trust-in-source is a heuristic for allocating *verification effort*, not a verdict on claims. Any design that lets source-distrust veto corroborated truth, or source-trust auto-admit uncorroborated claims, has a bug regardless of fork. (Candidate law, §7 Q5.)
4. **Representation × learning are orthogonal axes.** K = scalar + hand-set. L = scalar + learned. S = structure + deliberative/learned. The unbuilt fourth corner (structure + hand-set rules) is named only to keep the debate honest: nobody is building a hand-written provenance rule engine, but "structural" alone does not imply "learned."

---

## 2. Fork K — the scalar knob (baseline)

### 2a. FOR K (Muse, steelman)

**Decision-making needs the number.** Every real decision under uncertainty is a bet, and bets need odds. Consider what breaks concretely when you delete the stored scalar:

- **Bet sizing:** Source A predicts a component will fail. TNN must decide whether to spend trivial or serious mitigation resources. A provenance record is not a stake. Sizing the bet needs something equivalent to P(claim correct | source, context) × consequence — a scalar, even if computed transiently.
- **Arbitration:** A says the drug interaction is dangerous; B says it is safe. TNN must recommend, not admire the nuance forever. Comparing sources requires commensurable weights.
- **Resource allocation:** ten sources generate leads; TNN can verify two. This is a bandit problem. Ranking needs scalar indices — expected information gain or expected correctness per unit cost.
- **Gating/triage:** admit-without-review vs. review vs. reject is a cutoff decision, and a cutoff needs a number. "Admit when graph pattern X holds" is a categorical threshold over hand-selected structural features — a knob with poorer resolution.

**Humans have the dial too.** Micah's "I don't have knobs" is introspectively wrong at the mechanism level: "I trust her" *is* a cached per-person summary, and it is scalar-like. The honest reading of the directive is not "no scalar in the head" but "no hand on the dial." K's sin is who turns it, not that it turns.

**K is the load-bearing baseline.** If a fancy design cannot beat a hand-tuned scalar on the scoreboard, it is worse than a spreadsheet. The mechanical update rule is auditable, deterministic, O(1) at decision time, and its failures are obvious and testable — a badly tuned K fails loudly, while a muddled S fails inscrutably.

**The anti-knob critique proves too much.** Every learning system has hyperparameters; "zero knobs" as an absolute is incoherent — even the substrate has constants. K is at least honest about its knobs. L hides them one level down in the "emergent" machinery and calls the hiding learning.

**Scale is not optional.** At ingestion throughput (cf. the 1GB line), per-admission deliberation over a provenance graph is computationally infeasible. K pays the reasoning cost once, caches the sufficient statistic, and acts in constant time.

### 2b. AGAINST K (Muse, steelman)

**The knob is a frozen folk theory.** The update rule's constants — learning rate, betrayal penalty, recovery rate, recency decay — encode *someone's* folk psychology of trust, not TNN's learned judgment. This is exactly what Micah's law forbids, and no amount of scoreboard performance legitimizes it: a faster wrong thing is still the wrong thing.

**A single scalar cannot express what trust needs to express:**
- *Malice vs. error:* a skilled liar and an honest novice can both be right 60% of the time and must be handled oppositely (the liar fails strategically at high stakes; the novice improves with feedback). One number conflates them by construction.
- *Domain-specificity:* trusted on physics, worthless on gossip — the per-source scalar is blind to claim class.
- *The shape of history:* 500-honest-then-betrayal compresses to "0.998… now 0.4." The long-con *pattern* — the most decision-relevant fact — is erased by the collapse. The scalar remembers the average and forgets the story.

**Trust-vs-truth: the scalar becomes a veto.** Gate-on-scalar designs in practice reject corroborated truth from distrusted sources — the map vetoing the territory. K's defense ("the scalar is only an input") concedes the point: wherever the scalar isn't doing the work, the corroboration logic is, and the debate is about what does the work.

**The reformed source exposes the rigidity.** Mechanical recovery is either too fast (forgives the sleeper's handler on schedule) or too slow (punishes the genuinely reformed forever) — because the rate is a constant, not a judgment. Humans forgive on evidence *and* on theory of the person; K has the evidence channel only.

**Sybil-trivial.** The table floods with fresh identities. The default-trust for unknown sources is itself a knob that mints trust from nothing (optimistic) or DOSes attention (pessimistic) — and the attacker chooses which failure you get by choosing how many identities to mint.

**K doesn't learn; it accumulates.** There is no understanding in the number. It is a thermometer with no path to becoming a thermostat — and this program is building minds, not instruments.

---

## 3. Fork L — learned trust (the directive's heir)

### 3a. FOR L (Muse, steelman)

**L is the faithful reading of the directive.** No hand-set dial, but no pretense that decisions don't need aggregates. The value is learned from TNN's own experience: source-symmetric start, no designer theory of trust dynamics in the update path, dynamics revisable by TNN itself (the RC1 pattern — TNN controls 100% of its reasoning machinery, 0% of the constitution).

**It captures what humans actually do.** Cached trust-per-person, updated by experience, with the update *policy* itself subject to revision from experience. "I trust her again, but not completely" is a learned scalar with asymmetric recovery — L's natural output, K's hand-tuned imitation.

**It beats K where it matters and S on cost.** The dynamics adapt to the actual source ecology instead of executing frozen folk theory (beats K); the learned value is O(1) at decision time — memoized judgment, not per-case deliberation (beats S on throughput).

**The scalar is a readout, not the whole story.** L's track record *behind* the value can hold verdicts (malice-vs-error judgments from the FL2/lie-detection line), domain tags, recency structure. The number is the cache; the record is the memory. This answers the collapse objection: L collapses for action but retains for deliberation.

**Sybil: L is the only fork whose natural extension survives cheap identities** — *if* the learning is at the feature level, not the identity level. A learned trust *function* over behavioral features (burst patterns, claim-copying, stake behavior) generalizes to never-before-seen identities; a per-source table cannot. L-as-table is as Sybil-fragile as K; L-as-learned-function is the Sybil-resistant design. The fork crew must build the latter.

### 3b. AGAINST L (Muse, steelman)

**"Emergent" is doing unexamined work.** Every accumulator has an update rule; every update rule has constants; someone chose the episode boundaries, the verdict taxonomy, the aggregation function, the recency weighting. L risks being K with the knobs moved one level down and labeled "learning." The debate forces L's crew to name *every* constant in the update path and defend each as substrate-general (arithmetic of memory) rather than trust-specific (theory of trust). Any constant that encodes "how much betrayal should hurt" is a knob, whatever it is called.

**The collapse objection survives.** If the record behind the scalar does the real work in hard cases (sleeper, reformation, malice-vs-error), then the scalar is theater in exactly the cases that decide the debate — and L is S with extra steps and a misleading cache. If instead the scalar does the real work, L has conceded Q1 to K and the only remaining question is who sets the update constants.

**Circularity of the training signal.** What is the ground truth for trust updates? "Source was right/wrong" requires verdicts — which require the very judgment machinery that trust is supposed to serve. Trust learns from verdicts; verdicts lean on trust. K has this problem too, but K doesn't claim to have dissolved it; L's "learned" framing obscures a bootstrap problem the crew must solve explicitly (which verdicts are trust-independent enough to train on?).

**The sleeper needs a tripwire, not a gradient.** Learned accumulators are smooth by construction; the human response to betrayal-after-500-honest is discontinuous — "wait, WHAT?" — a regime change in the *theory of the source*, not a gradient step in a tally. L needs a deliberative surprise-handler, which is S's machinery wearing L's badge.

**Cold start is a designer theory too.** Source-symmetric initial state ("treat all strangers alike") is Laplace's indifference smuggled in as neutrality. Indifference is a choice, and under Sybil it is an exploitable one: the attacker's 500 sockpuppets each get the same fresh start as a genuine newcomer.

---

## 4. Fork S — structural trust (no scalar)

### 4a. FOR S (Muse, steelman)

**The scalar answers the wrong question.** The question is never "do I trust source X?" in the abstract — it is "do I admit *this claim*?" Trust is a function of (source, claim, context). Collapsing to a per-source scalar is premature abstraction: it throws away claim-level and context-level information before the decision that needs it. S answers the actual question directly from the record.

**Only structure preserves the shape of history** — and the human-like judgments live in the shape:
- the long con (500 honest, then betrayal) reads as a *pattern*, interpretable as "capable of sustained deception";
- the reformation arc reads as a trajectory, not a recovery constant;
- the Sybil burst reads as a star in the graph, invisible in a table;
- domain-specificity is native (the record is per-claim; no separate domain machinery needed).

Scalars erase shape; structure keeps it. Every hard case in Q3 is a shape-reading problem, which is why S owns Q3.

**Trust-vs-truth dissolves.** There is no source-level number, so there is no source-level veto to override. Corroboration is *in the record*; the true-but-distrusted claim is admitted on the corroboration naturally. S cannot commit K's characteristic sin.

**Retroactive re-valuation.** When the sleeper's betrayal lands at episode 501, the right response is not just "distrust future claims" — it is "re-examine everything already admitted from this source." Only a provenance graph supports walking back from the source to everything it touched. Scalars and tallies have no reach-back; their past admits are frozen. This is S's most underrated advantage and the fork crews for K and L have no answer to it within their representations.

**Most figure-it-out.** Zero designer theory of trust baked in. TNN reads the record and judges each case — the closest any fork comes to "I just learned myself."

### 4b. AGAINST S (Muse, steelman)

**"Admission reads the record directly" is a slogan, not a mechanism.** How does admission read a graph with 10⁶ edges per decision, at ingestion throughput? S either memoizes its reads — and becomes L with extra steps and a misleading origin story — or it doesn't run at production scale. The fork crew must specify the read procedure with computational complexity, or S is a promissory note.

**Every concrete read procedure reintroduces the number.** Graph queries that actually decide things — corroboration counts, centrality, recency weights, burst detectors — are scalar aggregates computed on the fly. S doesn't delete the number; it *recomputes* it per decision at 1000× the cost and with less testing per aggregate than K's single explicit value. "No stored scalar" is an implementation detail about caching, not a cognitive achievement.

**Inconsistency.** The same record read under different deliberative contexts can yield different verdicts. Cached scalars give stable, auditable, deterministic trust states. Determinism cuts both ways here: the mind can't be dice, but neither should it be moody — and per-decision re-derivation is moodiness with extra steps.

**Triage still needs cutoffs.** Admit / review / reject is a threshold decision. Thresholds need numbers. S pays for its purity in deliberation budget on every admission, including the 99% of routine cases where the graph read will reproduce what a cached scalar already knew.

**S's knobs are in the schema, where they're hardest to see.** What counts as an edge? What counts as corroboration vs. copying? How is provenance recorded when sources cite each other? These designer choices shape every downstream judgment, and unlike K's exposed constants they are nearly impossible for TNN to revise — they're load-bearing architecture, not parameters. S may be *less* revisable than K, not more.

---

## 5. Sol-A opinion (devil's advocate FOR K, AGAINST the no-knob designs)

*Via UnoRouter, model `gpt-5.6-sol`. Prompt tasked it to defend the scalar and attack L and S at their strongest. Recorded 2026-09-23; lightly formatted, content verbatim in spirit.*

> **Deleting the number does not delete trust policy; it merely hides the policy inside a slower, less inspectable computation.** Any system that must bet, choose, allocate, or gate eventually needs a decision-relevant compression of evidence. In most operational settings, that compression is a scalar: expected reliability, expected loss, posterior odds, or marginal value. Fork K makes that fact explicit. Forks L and S either recreate the number downstream or avoid making crisp decisions.
>
> **What breaks without a collapsed value** — four ordinary decisions: (1) *Bet sizing:* a provenance record is not a stake; sizing needs P(claim correct | source, context, record) × consequence — a scalar even if temporary. (2) *Conflicting sources:* A says dangerous, B says safe; TNN must recommend administer, withhold, or investigate — comparing sources needs commensurable weights, and S's traversal implements an implicit, worse-tested scoring function. (3) *Resource allocation:* ten leads, two verification slots — a bandit problem needing scalar indices; "read the whole history" is wasteful and unstable. (4) *Gating:* "admit when graph pattern X holds" is a categorical threshold over hand-selected features — a knob with poorer resolution. S's failure mode is latency and inconsistency: every decision a fresh miniature trial, different prompts yielding different verdicts from the same record. K reasons once, caches the sufficient statistic, acts in constant time. A scalar is lossy — but action itself is lossy. A robot cannot both turn left and right merely because the evidence remains nuanced.
>
> **Fork L is a knob with extra steps.** It must answer: how much evidence is enough? How are old and recent episodes weighted? Does one severe lie outweigh twenty trivial truths? What happens before the first observation? How does performance transfer across domains? Any accumulator needs an effective prior, learning rate, decay schedule, loss function, treatment of missing outcomes. Setting displayed trust to "nothing" moves the prior into behavior — if an unseen source is admitted 30% of the time, that *is* its initial trust policy. Even a fully learned model inherits priors from architecture, training distribution, objective, regularization. Not absence of knobs — less legible knobs distributed across millions of parameters. The clean line: **evidence acquisition may be learned, but action requires a decision statistic.** For a source used across many downstream decisions, repeatedly reconstructing that value is inefficient and harder to audit. K stores the reusable summary openly. L's best argument — a fixed rule may encode the wrong inductive bias — is true, but the remedy is to *learn or calibrate K's update parameters*, not to pretend the posterior reliability is philosophically illegitimate.
>
> **Hard cases.** *Reformed source:* humans say "I trust her again, but not completely" — a scalar-like summary with asymmetric recovery. K represents this honestly: sharp penalties for high-confidence deception, gradual recovery through independently verified successes, recency decay. *Honest-but-wrong:* here a single scalar genuinely fails if asked to represent both reliability and intent — a well-meaning novice and a skilled liar at 60% each must be handled differently. K should define its scalar narrowly as **predictive reliability for the relevant claim class**, with intent, competence, calibration, domain kept as separate features. The lesson is "don't make one scalar carry every concept," not "never collapse." *Sleeper:* a naïve average barely moves — catastrophic. K needs surprise-sensitive updates: severe authenticated betrayal triggers a large multiplicative penalty, change-point hypothesis, or quarantine floor. Mechanical, fast, uniform, on the critical path without rereading 500 episodes. S retains forensic detail, but traversal is not a reaction policy — it must still decide how much one betrayal outweighs history.
>
> **Sybil:** No design survives cheap identities without identity continuity, authentication, stake, behavioral linkage, or provenance-level clustering. K degrades predictably with a pessimistic prior, limited privileges, capped influence for unknowns. L is especially exploitable if its learning grants newcomers optimistic exploration. S has the strongest potential advantage when its graph exposes shared infrastructure or coordinated corroboration — but that advantage comes from identity/relationship evidence, not from refusing a scalar. Feed those signals into K as initialization or caps. Without identity linkage, all three fail; with linkage, S is a valuable evidence substrate but not a complete admission policy.
>
> **Ranking** by figure-it-out flexibility: 1. L, 2. S, 3. K. By likely near-term empirical scoreboard: 1. K, 2. L, 3. S. K wins on calibration, latency, sample efficiency, reproducibility, decisive behavior. L may eventually beat it with enough experience and strong meta-learning — but it will still learn an implicit scalar decision statistic. S shines in forensics and adversarial provenance, yet struggles as the sole real-time control mechanism. **The boring scalar probably wins — not because cognition is one-dimensional, but because decisions require compression. Keep the provenance graph. Learn the update rule where possible. Track intent and competence separately. But cache an explicit, calibrated trust value. Refusing to name the number does not make TNN more human; it makes its number harder to find.**

## 6. Sol-B opinion (steelman FOR L)

*Via UnoRouter, model `gpt-5.6-sol`. Prompt tasked it to steelman Fork L (defend learned trust; attack K and S at their strongest). **Retrieval failed at the provider layer:** six attempts over ~25 minutes (2× long structured prompt via sol.py, 1× HTTP 524 gateway timeout, 2× inline-script retries, 1× short plain prompt via unorouter.py chat) all returned empty completions (`choices: null`, `completion_tokens: 0`). Only `gpt-5.6-sol` is listed on the connector, so no alternate Sol model was available. The single successful Sol call in this session was Sol-A (§5), suggesting transient provider-side degradation of this model at retrieval time.*
*Substance note: the pro-L steelman Sol-B was meant to supply is fully present in the Muse role-separated rounds (§3a FOR L / §3b AGAINST L), which were written to the same brief — defend L at its strongest, attack K and S at theirs, no strawmanning. The debate record is therefore complete in substance. The coordinator may re-run the Sol-B call when the provider recovers and append the opinion here; it should be checked against §3a for agreement/disagreement and any delta recorded.*

**Coordinator action:** re-attempt Sol-B retrieval post-recovery; append verbatim opinion + delta-vs-§3a note. Do not treat this section as closed until then, but do not hold fork-crew work on it — §3a/§3b stand as the L positions.

---

## 7. The six questions — settled or sharpened

### Q1. Is the collapsed scalar the wrong abstraction? What breaks when you delete the number?

**Sharpened, not settled — the debate split on stored vs. computed.** Both Sol-A and the Muse FOR-K case establish that *decision-time* collapse is unavoidable: bets, arbitration, bandits, and triage cutoffs need commensurable quantities. The Muse FOR-S case establishes that *stored* collapse is premature: the question is per-claim, and per-source scalars destroy claim-level and context-level information.
**Testable form:** the fork crews are not debating "number vs. no number" but **cached scalar (K/L) vs. per-decision computed aggregate (S)**. S's crew must specify the read procedure and its complexity; if the procedure memoizes, S must say what distinguishes its memo from L's learned value. K/L crews must show a case where the stored scalar outperforms per-decision recomputation *other than* on compute cost — otherwise S wins on information and loses only on budget, which is an engineering trade, not a cognitive verdict.

### Q2. Can L's "emergent" value avoid being a knob in disguise? The anti-knob criterion.

**Settled as a definition; L's compliance is the empirical question.** The debate converged on this criterion — a parameter is a knob iff it embodies *a human's theory of how trust should work* in a place TNN cannot revise. Concretely, L is not-a-knob iff:
1. **Source-symmetric initial state** — no designer ranking of sources; every source starts identically (indifference is itself a choice, but a symmetric one, and the only non-ranking choice).
2. **No trust-theory constants in the update path** — every constant must be defensible as substrate-general (arithmetic of memory, deliberation budget) rather than trust-specific. "How much betrayal should hurt" may not appear as a constant; if it appears at all, it must be a *learned* quantity revisable by TNN's own deliberate self-change (RC1 pattern).
3. **Revisability by TNN** — the update dynamics themselves are within TNN's deliberate control (it can inspect and revise how it learns trust), not frozen designer code. The only frozen trust value permitted is an audited human/trainer force-pin (standing law: the only true lock is human, audited, visible).
4. **No hidden priors in behavior** (Sol-A's challenge, accepted): if unseen sources are admitted X% of the time, X *is* the initial trust policy and must be declared and defended, not smuggled inside "no initial value."

**The line the debate drew:** a per-source accumulator is NOT a knob in disguise iff its update rule is TNN's own general learning machinery applied to source experience — no trust-specific formula. It IS a knob iff any step computes "trust" via a designer-authored function of experience. L's crew must publish the full constant inventory of their update path with each constant classified per (2). This is a must-address item (§9).

### Q3. The hard cases.

**(a) Reformed source.** Agreement: re-earned trust must be *slower and more conditional* than initial trust — severity of the breach, number of post-reform observations, independence of verification, and opportunity-to-deceive all matter. K mechanizes this with a recovery constant (rigid: too fast for the con artist, too slow for the genuinely reformed). L learns the recovery dynamics from experience (better, *if* the training regime contains reformations to learn from — cold-start problem for the dynamics themselves). S reads the reformation arc as a trajectory (richest, most expensive). **Testable:** the battery must include reformation episodes with *varying* genuineness; the fork that forgives the truly reformed fastest while staying cold to the performing reformer wins. No fork may be scored on recovery speed alone — recovery *discrimination* is the metric.

**(b) Honest-but-wrong (malice vs. error).** Settled: **no single scalar can express this; any fork that tries fails.** A skilled liar and an honest novice at equal accuracy must be handled oppositely, and the difference (strategic failure at high stakes vs. improvability with feedback) is invisible to accuracy tallies. Consequence: K must split its scalar (reliability vs. intent vs. competence — Sol-A conceded this) or lose adversarial cases; L's track record must store *verdicts about intent* (from the FL2/lie-detection line), not just outcomes, or its "learning" learns the wrong lesson; S's graph must have edge types distinguishing "wrong" from "deceptive," or its shape-reading reads noise. **The representation must be rich enough to hold the judgments TNN can actually make** — this is a constraint on all three crews, and the battery must test malice-vs-error discrimination directly.

**(c) Sleeper (500 honest, then betrayal).** Settled on the principle, open on the mechanism: the right response is **discontinuous** — a regime change in the *theory of the source* ("capable of long cons"), not a gradient step; and it is **retroactive** — everything previously admitted from the source goes under re-examination. A smooth accumulator under-reacts by construction; only a deliberative surprise-handler gets this right. K's answer (multiplicative shock / quarantine floor) is fast but mechanical — it reacts without understanding, and its shock magnitude is a knob. S's answer (re-read the shape, walk the provenance graph backward) is correct but slow and needs a specified trigger. L's answer must include the tripwire or it is K-smooth. **Testable:** the battery must include sleepers where the betrayal is (i) a one-off error, (ii) a changed circumstance, (iii) a revealed long con — the fork that responds identically to all three fails; the fork that discriminates fastest *with reasons* wins.

### Q4. Sybil resistance.

**Settled: no fork survives cheap identities on its trust representation alone.** The 1GB finding stands — origin counting is defeated by design (500/500). The debate's findings:
- Trust representation ≠ identity. Sybil resistance comes from **(a)** identity cost/authentication underneath, and/or **(b)** coordination/burst detection over provenance structure. The prereg must state which the battery assumes; a battery with costless identities and no burst detection tests nothing about trust — it tests identity, and all forks fail identically.
- **Graceful degradation ranking:** S degrades most gracefully *as an evidence substrate* — the sockpuppet burst is visible in the graph (star pattern, copied claims, shared infrastructure) and invisible in a scalar table. K degrades most *predictably* — pessimistic priors and capped influence for unknowns bound the damage arithmetically. L-as-per-source-table degrades like K; **L-as-learned-function-over-behavioral-features** is the only variant with a path to actual resistance (it generalizes to unseen identities) — but that is a stronger claim than "per-source track record" and the crew must build it to claim it.
- Without (a) or (b), the honest result is "all forks fail; the failure is out of scope for the trust representation." The debate records this so the battery doesn't misattribute an identity failure to a trust design.

### Q5. Trust vs. truth (distrusted source, true + corroborated claim).

**Settled as candidate law:** *Trust in sources is a heuristic for allocating verification effort, not a verdict on claims.* A distrusted source's claim gets more scrutiny, not automatic rejection; a trusted source's claim gets less scrutiny, not automatic acceptance. What SHOULD happen: the claim is admitted on the strength of the corroboration; the source's distrust is untouched (or updated slightly — corroborated truth from a distrusted source is weak evidence of reform, not strong).
- K's failure mode: scalar-as-veto rejects it. K's repair: the scalar gates *scrutiny*, never *admission* — corroboration bypasses the source score. (If the scalar never gates admission, K's crew must say what work the scalar does.)
- L's failure mode: the learned value overgeneralizes "distrusted → reject." L's repair: the training regime must include distrusted-source-truth cases, or the learned policy learns a prejudice.
- S's non-failure: no source number means no source veto; the corroboration is in the record. This is S's cleanest win and the debate records it as such.
- **Testable:** the battery must include distrusted-source-says-truth-with-corroboration cases; any fork that rejects them fails the item regardless of its aggregate score.

### Q6. Figure-it-out ranking — and does it predict the scoreboard?

**Ranking by figure-it-out (least designer theory of trust baked in):**
1. **S** — no trust theory stored at all; per-case deliberative judgment over the record. (Sol-A ranked L first here; the Muse rounds rank S first. The disagreement is recorded: Sol-A counts L's adaptive dynamics as more figure-it-out than S's deliberation-because-S's read procedure may itself embed theory. Both readings are defensible; the battery decides which kind of flexibility pays.)
2. **L** — the value is learned, but the update machinery (episode boundaries, verdict taxonomy, aggregation) still embeds designer choices. The most figure-it-out *scalar* design.
3. **K** — the designer wrote the update rule; TNN executes it. Most rigid-policy.

**Does the ranking predict the empirical outcome? The debate says: not necessarily, and this must be stated plainly.** "Figure-it-out wins ties" is Micah's tie-break rule, not a law of nature. The boring scalar may win the scoreboard if the battery rewards fast, consistent, cheap, well-calibrated decisions — because figure-it-out costs deliberation budget and risks inconsistency, and S's flexibility is worthless if the read procedure is the real theory. Sol-A's blunt prediction (K > L > S on the near-term scoreboard) is recorded as the prediction to beat. The debate's contribution is the **win-conditions analysis** each crew must address:
- K wins if: decisions are frequent and time-pressured, sources are stable, the battery measures calibration and cost. K loses if: the battery is adversarial (sleepers, reformations, Sybils) or tests malice-vs-error.
- L wins if: the horizon is long enough for learned dynamics to beat frozen rules, and the regime contains the hard cases to learn from. L loses if: the battery is short-horizon (no time to learn) or the update path smuggles knobs (then it's K with worse legibility).
- S wins if: the battery weights adversarial/forensic cases heavily and deliberation budget is ample. S loses if: throughput or consistency dominate the scoring, or the read procedure turns out to be the hidden theory.

**A directive caveat the debate insists on recording:** Micah's "scrap the knob" prejudges K's loss. K is the baseline to beat — a baseline that *cannot* win is a strawman baseline, and beating a strawman proves nothing. If K wins empirically despite the directive, that is data *about the directive*, and the program must report it, not bury it.

---

## 8. Placement: PAM admission layer, memory substrate, or own organ?

**Recommendation: its own organ — a source-model capacity — serving both, owning retroactive re-valuation.** Reasons, argued from the debate:

1. **Not PAM-only.** PAMs are the senses/gates; the admission/install gate is where trust *acts* (scrutiny allocation, triage). But trust *judgments* need memory (the track record / provenance graph lives in the substrate) and deliberation (malice-vs-error, sleeper tripwires). A pure PAM gate is too thin — it becomes a mechanical filter, i.e., K in a trench coat. The PAM v2 synthesis already lists provenance/ledger as a hard mechanism (M9) and the gate as an admission/coverage system; trust-as-scrutiny-advice plugs into that gate naturally, but the *model of the source* cannot live in the gate.
2. **Not substrate-only.** MA4's signed memory values already carry valence, and source-trust should be *one input* to the signing deliberation. But memories are about claims and trust is about sources; collapsing source-models into per-memory signs loses the per-source aggregation L wants to learn and the per-source graph S wants to walk. Worse, neither a gate nor a static sign supports **retroactive re-valuation**: when the sleeper betrays at episode 501, everything admitted from that source must go under re-examination. Only a standing source-model with reach into the substrate can do that.
3. **Own organ fits the architecture.** The post-toy architecture has five organs (deliberate memory substrate, eliminative hypothesis logic, deliberate consolidation/promotion, symbolic recall and trace composition, native structural revision). A source-trust organ sits alongside as a sixth capacity: it maintains *theories of sources* (reliable, biased, honest-but-wrong, adversarial, reformed, sleeper-suspect…), answers queries from PAM admission ("how much scrutiny for this claim from this source?"), writes into substrate signing deliberations, and owns the backward walk — on source-theory change, find everything the source touched and flag it for re-verdict. S's provenance graph is this organ's natural memory; L's learned dynamics its natural update; K's scalar its natural *cache* (memoized readout, explicitly labeled as cache, never as truth).

**What each fork crew owes the placement question:** K must say where its table lives and what triggers retroactive re-scoring on betrayal (a table with no backward walk fails the sleeper). L must say where the track record lives and which organ revises the update dynamics. S must say which organ runs the read procedure and at what budget. If the program later merges forks, the organ is the merge point.

---

## 9. Must-address items per fork crew

**Fork K crew:**
1. Publish every constant in the update rule (initial value, learning rates, betrayal penalty, recovery rate, decay). For each: what human judgment does it encode, and why is that judgment not TNN's to make?
2. Split the scalar or lose adversarial cases: state how the design represents malice-vs-error and domain-specificity, or concede it doesn't and bound the damage.
3. State the scalar's exact role in admission: if it can veto a corroborated claim, the design violates the trust-vs-truth law (§7 Q5) — repair or defend.
4. Specify the sleeper response mechanically (shock magnitude? quarantine floor? change-point trigger?) and the retroactive re-valuation procedure — what happens to the 500 previously admitted memories?
5. If K wins the scoreboard, the crew must argue explicitly whether the win vindicates hand-set trust or merely well-calibrated compression — the directive question doesn't dissolve with a high score.

**Fork L crew:**
1. Publish the full constant inventory of the update path, each classified substrate-general vs. trust-specific per the anti-knob criterion (§7 Q2). Any trust-specific constant is a knob — rename or remove.
2. Declare the behavioral initial policy (the "no initial value" claim): unseen sources are admitted X% of the time under conditions Y — X and Y *are* the initial trust policy. Defend them.
3. Solve the bootstrap explicitly: which verdicts are trust-independent enough to train the trust dynamics? Name them.
4. Build the sleeper tripwire: show the mechanism by which betrayal-after-long-honesty produces a *discontinuous* source-theory change, not a gradient step.
5. State whether L is per-source-table or learned-function-over-features. Only the latter may claim Sybil resistance; the former must accept K's Sybil analysis.
6. If the scalar is a readout over a record that does the real work, say what distinguishes L from S-with-a-cache.

**Fork S crew:**
1. Specify the read procedure: the exact query/algorithm admission runs over the provenance graph, with computational complexity per decision and behavior at ingestion scale. "Deliberation figures it out" is not a specification.
2. Name the schema knobs: what counts as an edge, as corroboration vs. copying, as a source identity? Argue why these are revisable by TNN and not frozen designer theory.
3. Show the triage cutoffs: admit/review/reject needs thresholds — where are they, who sets them, are they learned?
4. Specify the sleeper trigger (what pattern of graph evidence fires the regime change) and the retroactive walk (algorithm + cost for re-examining everything a betrayed source touched).
5. Demonstrate consistency: same record, same query, same verdict — across deliberative contexts and across reruns. If the read is deliberative, bound the variance.
6. If the read procedure memoizes, state the invalidation policy — a memo with no invalidation is a stale scalar, the worst of both designs.

**All crews:** the battery must contain (i) reformation episodes of varying genuineness, (ii) sleepers of all three kinds (one-off error / changed circumstance / revealed long con), (iii) honest-but-wrong vs. malicious sources at matched accuracy, (iv) distrusted-source-truth-with-corroboration, (v) a Sybil leg *with a stated identity assumption* (costless identities + no burst detection ⇒ all forks fail identically; that leg tests identity, not trust — label it as such).

---

## 10. Debate verdict ranking (debate crew's own)

The tasking asks for the debate crew's ranking with the single strongest argument for and against each. This ranking is a *debate* verdict — a prediction and a judgment about the designs — not the empirical outcome, which belongs to the fork crews and the frozen battery.

**1. Fork L (learned) — the directive's heir and the best bet.** *Strongest for:* it is the only design that takes Micah's directive seriously without pretending decisions don't need aggregates — learned values, source-symmetric start, revisable dynamics; the human pattern ("I trust her again, but not completely") falls out of experience rather than being hand-tuned in. *Strongest against:* "emergent" may be K with the knobs moved one level down — the crew must survive the constant-inventory audit (§9), or L is the least honest of the three designs, not the most.

**2. Fork S (structural) — the most right about the hard cases, the least proven as a mechanism.** *Strongest for:* the hard cases are shape-reading problems and only structure preserves shape — the sleeper's long con, the reformation arc, the Sybil burst, retroactive re-valuation; and trust-vs-truth dissolves because there is no source veto. *Strongest against:* "admission reads the record directly" is currently a slogan — without a specified, budgeted, consistent read procedure, S is a promissory note that recomputes K's number per decision at 1000× the cost.

**3. Fork K (knob) — the baseline that might embarrass everyone.** *Strongest for:* decisions require compression and K is the honest, auditable, O(1), deterministic form of it; Sol-A's challenge stands — deleting the number hides the policy inside a slower, less inspectable computation, and the near-term scoreboard likely favors the boring scalar. *Strongest against:* the update constants are frozen folk psychology — exactly what the directive forbids — and no score can legitimize a design whose core is a human theory TNN cannot revise; also it has no representation for malice-vs-error and no reach-back for the sleeper.

**The synthesis the debate kept returning to:** representation and learning are orthogonal, and the winning system is probably L+S with K as cache — learned source-models (theories of sources, revisable) over a structural provenance record (shape preserved, retroactive walk supported), with memoized scalars as explicitly-labeled cache for O(1) decisions, all housed in a source-trust organ serving PAM admission and substrate signing. The forks are worth building separately because each one stress-tests a different load-bearing claim — but the crews should know the likely endgame is a merge, and the prereg should say what would count as each fork *losing* rather than merely scoring second.

---

*End of frozen debate record. Fork crews: address §9 before claiming verdicts. Coordinator: commit discipline is yours.*
