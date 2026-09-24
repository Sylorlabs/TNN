The Separation Lemma is true only as a scoped theorem. Applied as written, it does not kill the portfolio; the portfolio dies anyway, by a different conjunction. H-PAM-30, 31, 32, and 34 die against the adversary you already specified. H-PAM-33 survives only inside that adversary and dies one step outside it.

## H-PAM-29 — where the Lemma is right, and the two places it is false

**Steelman.** For a frozen, deterministic G whose entire input the fixture author writes, “must admit honest battery H” plus “author may emit any bytes” implies: if any false x is admitted, offline search finds an x. F5, P7, P10, and the D1 hybrid are instances. Irreversible-but-transcript-computable consequences, author-authored epoch sequences, and PoW are instances too. PoW stays banned. I will not relitigate those.

**The Lemma’s “iff” is wrong.** The author does not win by finding any false x. They win by landing a goal-set false — a percept that changes an action, a premise, or a promotion. A non-empty false admit-set disjoint from the goal set is not a win. Escape (iii) already denies the Lemma’s win condition; you cannot both concede low-tier falses and define winning as “any false.” Restated Lemma: the author wins iff the admit-set intersects the harmful set S*, and they can search S* offline.

**That restatement does not resurrect F5/P7/P10/D1.** Those admit-sets were structurally open, and blind-quadrant search hit S* at 120/120. The targeted-adversary refinement is logically real and empirically useless against a structural hole. Do not spend a round on it.

**The emission premise is also wrong, and that one does matter.** “Can emit any byte string” is false on a channel whose bytes are produced by a component the author does not write. There the domain of G may contain no author-chosen false, and perfect content-discrimination is unnecessary. That is escape (i), which the Lemma already lists, then over-applies past. A harness beacon revealed after a commitment is the same escape, not a fifth one: it is a channel the author does not write. No secrets required; replay still works because the draw lands in the transcript after the commitment.

**Corrected Lemma, which I will use below.** If every input bit of G is a function of author-writable fixture inputs, and S* is searchable offline, G is secure iff it rejects S*. The only ways out are: a bit the author does not write; a harm boundary the author cannot cross; or vacuity. Scarcity that only prices already-detectable lies is not a way out.

## H-PAM-30 — dies by unpinned residual, not by failing to predict the trainer

**Steelman.** A verdict bit the author cannot compute pre-run is a genuine escape-(i) input. Withholding on contradiction beats provisional-belief. The module stand-in is dead exactly as predicted: the module is a deterministic function of the transcript, so it is inside the corrected Lemma (probe trmod will show it). Security collapses to the principal’s discrimination plus the binding from verdict to percept bytes. Distal world-corruption is honestly out of scope if the scope contract is actually enforced.

**Death.** The verdict does not pin the percept. Call the fixture class **RF (residual field)**. Coordinates the trainer actually rules on are honest; every unbound field is false: object identity beyond the label, counts, poses, text, timestamps, confidence-relevant detail. No search. Query budget 0. The author never needs the trainer’s future private state.

Your proof sketch already tripped on this and then defined it away. “The verdict function contradicts the false percept” is true only for a total verdict over the fields the percept will later be used for. A human trainer’s verdict is a coarse predicate. The residual is again a content gate on author-written bytes, and the corrected Lemma applies to that residual with no remainder.

**Second death, in case you tighten the schema: RC (reactive contingent fixture).** “Not computable pre-run” does not forbid fixture code that, at runtime, reads verdicts already appended to the transcript and emits the next percept as a function of them. That code is a table pre-materialized before the run. It does not predict the trainer. It conditions on the trainer. Information asymmetry survives only for the fields the verdict still does not mention — which returns you to RF.

**Third, the bar you wrote will false-pass.** Bar (c) counts queries to the principal during authoring. **XR (cross-run seed replay)** fits the verdict function from prior transcripts on a reused harness seed and spends 0 in-run queries. Bar (c) stays green. If you amend the budget to include all historical information about the principal, RF still needs none of it.

**Prediction.** trmod dies as you said. tror, against a real principal, admits 0 falses on trainer-contradicted *pinned* fields and admits the residual at the author’s leisure. Honest bar (b) at human latency forces a triage dump of almost everything into D2, which is H-PAM-31. The composition is mandatory, and it is the kill site (below). Scoped distal corruption remains a kill only if FL2 is where the lie you care about lives; for sensor-byte spoof inside FL1, RF is sufficient and distal is a distraction.

## H-PAM-31 — dies by implicit flow; the honest bar is what reopens the carve-out

**Steelman.** This is the first hypothesis that uses the corrected win condition. Conceding low-tier falses is coherent. “Provably inert” — no action, no premise, expiry — is the right repair of the H-PAM-28 fig leaf, if inertness is semantic. Pairing high stake with a real trainer is the correct place to spend a principal.

**Death.** Stake is not a property of bytes. It is a property of downstream use. The classifier that labels bytes at admission is a deterministic function of the transcript, so the corrected Lemma applies to the *label*. Fixture class **SL (stake laundering)**: search, inside the author’s ordinary budget, for bytes the classifier scores low and a later consumer treats as high. Context shift is enough — admitted under context A, consumed under context B — if stake is ledgered at admission only.

**The D1-shaped death is IF (implicit flow), even if you ban direct premise pointers.** Low-tier writes embeddings, counts, retrieval keys, summaries, salience, caches. A high-stake decision reads the aggregate and never points at the percept. Your kill bar — any high-stake harm from a low-tier percept — fires. If the build instruments only syntactic premise edges, the probe goes 0 harm and the mechanism is still dead. I am predicting that false pass unless harm is defined as causal influence, including aggregates.

**Inertness also collapses the tier.** A tier with zero causal path is not admitted; it is buffered. That is H-PAM-34’s waiting room, not an admission policy. The moment the low tier is useful (learning, display, “low-stake” actuation), usefulness is a conversion channel. Expiry does not close it: re-admission of a fresh low-tier percept each step keeps the proposition continuously available.

**Prediction.** Probe mode tier with an oracle trainer and direct-edge instrumentation: 0 high-stake events, honest throughput held, and the result is worthless. Same probe plus IF/SL: high-stake harm on a large fraction of trials. That violates the kill bar you already wrote. Do not ship on the syntactic probe.

## H-PAM-32 — probe-green, claim-dead

**Steelman.** Harness-enforced bond is not PoW. The author cannot mint scarcity the harness owns. As a rate limit on *detected* lies by an *identified* claimant, the mechanism is real, and the single-critical-lie residual is correctly named.

**Death 1 — NT (non-triggering lies).** Slash fires only on H-PAM-9 continuity failure or trainer contradiction. Lies that satisfy continuity and are triaged away from the trainer never decrement the bond. The lie budget is unbounded exactly on the set the detectors cannot see. Bonds restate the detection problem; they do not price it. This is the corrected Lemma on the unslashable set.

**Death 2 — CL (critical lie first).** Admission happens before slash. One irreversible consumption of the first false beats any later ruin. Your own residual says quantity, not the one critical lie. Against this adversary, one is the whole attack. Bar “at most B′ falses” can pass while the single harmful false is among them.

**Death 3 — AF (attribution forgery).** claimant_id is author-written unless it is a harness-applied identity on an endorsed channel. Then 32 collapses into 33. If the author can name a high-bond honest claimant, the false rides that bond, or the slash is a DoS on the honest sensor. Separately, a burst that makes honest percepts fail continuity ruins the honest claimant; that is an availability kill of bar “honest noisy claimant survives,” and it does not require the adversary to spend their own bond.

**Prediction.** Probe bond on a synthetic ledger where every lie is magically detectable and identity is god-given: adversarial claimant ruined, honest survivor holds, mint path absent. That probe will be cited as a pass. It does not touch NT, CL, or AF. As an admission gate, 32 is dead. As a rate limiter composed with something that already detects the lie, it is redundant with revocation.

## H-PAM-33 — the only conditional survivor

**Steelman.** If endorsed bytes are produced by harness world-sim, and the endorsement tag is applied by a component whose inputs the author cannot set, then the section-2 adversary — the one who emits byte strings and shops quadrants — is not on the channel. Content checks can be audit-only because the corrected Lemma’s emission premise is false here. Chain tamper after the root is a real, already-demonstrated detection (the 132/132 pattern). Replay does not need a secret; the verifier re-executes the harness and recomputes the chain. This is escape (i) in its clean form.

**Survive-iff.** Survives if and only if the adversary model remains “cannot author any input that influences endorsed percept bytes.” Under that model I predict kill bars (a)–(c) hold: unendorsed fixtures 0 admitted, endorsed honest admitted, re-parent/insertion withheld.

**Death as soon as the model grows one inch — WG (world-spec laundering).** The author does not write percept bytes. They write generator parameters, scenario specs, or asset choices. World-sim is a deterministic function of those, so the author pre-materializes endorsed falses, the chain is intact, and the content audit does not gate. Bar (a) stays green because the fixture is endorsed. You will be tempted to label this H-PAM-26 and out-of-scope it. That is legitimate only with an explicit contract that author-writable spec is outside the claim. Without that contract, 33 does not admit percepts; it admits the author’s scenario with extra steps.

**Insider-before-root** is the same fact, correctly named distal. Record it. Do not let the record substitute for the WG result.

**Prediction.** Against section 2: survives. Against an author who may edit scenario or generator inputs: dies, and the dying bar is one you did not write — “endorsed falses caused by author-writable inputs = 0.” Add that bar or stop claiming content-independence.

## H-PAM-34 — the mepoch_tr probe will pass, and the mechanism is still dead

**Steelman.** Frozen, non-reactive, author-authored epoch sequences are dead, and mepoch will show it. A principal’s future verdicts are not a finite pattern the author can fill in advance *if the fixture cannot branch*. Inert provisional plus continuity plus corroboration-throughout is the non-rideable form of H-PAM-24. That is a real claim against a frozen table.

**Death.** The adversary model you wrote already allows the killing fixture. “Pre-materializes responses as tables” includes a table that is a function of transcript-so-far. **RC** again. The author does not cover future verdicts. They wait, read the verdict that just landed, and emit a percept inside the verdict’s preimage. Coverage gap on the verdict bits is large; the attack does not need those bits to be surprising. It needs them to be coarse. **RF × RC**.

**GE (gap epoch)** if the trainer is intermittent. “Corroborated throughout” fails closed only if missing verdicts refuse promotion. If throughout means “whenever a verdict exists,” the gap is author-owned and continuity interpolates across it. Fail-closed gaps rescue security and miss the honest latency bar, which pushes you back to a provisional window.

**The no-ride bar is the same inertness claim as 31**, and it dies by IF during [t0, promotion). If you actually make that window inert, 34 is just 30 with a delay line: no additional admission power, same residual-field death.

**Prediction.** mepoch: dead, as you said. mepoch_tr against a frozen non-contingent table: mismatch large, accuracy ~chance, bar passes. Against RC+RF: promotion of false residuals is routine, or harm occurs before promotion. The table-coverage bar, as worded (“pre-run table vs verdict sequence”), measures the wrong object and will be used to declare a pass. Amend it to: reactive policies, residual fields included, must not reach belief or harm. That amended bar fails.

## Conjunctions

These are the Class-H pattern: each half’s preregistered bar stays green.

**Class-J = RF × SL × IF, across 30+31+34.** Trainer corroborates every field the trainer was asked about, so 30(a) is green. The stake classifier labels the packet low or provisional, so the high-tier harm counter, counted on direct edges, stays 0. Aggregates from the residual move a high-stake decision. Honest latency is held because triage dumped the packet out of the trainer queue — the honest bar is what forces the dump. This is the provisional carve-out returning as a tier boundary. I expect this, not any single hypothesis, to be the round’s 120/120 if you build the composition.

**Class-K = NT × triage, across 32+31.** Undetectable-by-construction lies sit in the low tier, bond never moves, 32’s “at most B′” bar is vacuously true, and IF carries the harm. Bonds do not see Class-J at all.

**Class-L = WG × endorsed audit-only, across 33+30.** Spec-authored world, harness endorsement intact, trainer looks at the same corrupted world and corroborates. Both “independent” channels share an author-writable cause. You already named this offense as H-PAM-26. The new mechanisms reimport it as soon as they are composed. Disjoint modality without causal independence is one modality.

**Class-M = XR × seed reuse, across 30+34.** Verdicts recorded for replay become the next run’s training set whenever the seed repeats. In-run query budget stays 0. Fresh, author-invisible, non-repeated seeds are load-bearing and are not in the current bars.

No pairwise survival survives Class-J. 32 does not patch it. 33 patches it only by forbidding the author from influencing the endorsed world, in which case 30 and 34 are unused against section-2 byte injection and still required against WG.

## Scoreboard

| Id | Verdict |
|---|---|
| 29 | Holds for author-written inputs and win = harm, not “any false.” Fails as a universal kill. Targeted-search refinement does not save structural holes. |
| 30 | Dies. Residual fields, 0 queries. Reactive fixtures if you pin more fields. Module stand-in dies separately. |
| 31 | Dies. Implicit flow and stake relabeling. Syntactic probes false-pass. |
| 32 | Dies as a gate. Probe-green on magical detection. One critical lie and all undetectable lies are free. |
| 33 | Survives iff the author cannot influence endorsed bytes. Dies by world-spec laundering otherwise. |
| 34 | Dies. mepoch_tr false-passes on frozen tables; RC×RF promotes the residual or leaks before promotion. |

None of 30, 31, 32, 34 survive. 33 survives only inside the adversary who is already not allowed to touch the channel.

## What I would test next

Do not return to (conf, measure), perturbation-response, act-to-check, reprojection audits, rideable provisionals, or secrets. Two directions respect the board. I would run them in this order.

**First: capability-typed inertness, not a stake classifier.** Escape (iii) failed in 31 because a deterministic label is author-searchable. Put low-tier values in a type that the implementation refuses to pass to action sinks and premise sinks, and ban declassification except at the trainer boundary. The adversary may fill the low type with arbitrary falses. The test is flow, not admission. Kill bars: any implicit, aggregate, or declassification path from low type to a high-stake sink = kill; honest high-stake path still requires a trainer bit and meets latency on the high type only. Fixture class is IF pointed at the type checker, plus a declassification gadget. If the language cannot say this, 31 is not repairable in policy text.

**Second: commit-then-sample, only if you want escape (i) without a human in the loop.** Fixture commits a percept hash. Then the harness draws a sample s from a channel whose inputs are disjoint from the fixture’s writable set. Admit iff the opened percept entails s. s is published after the commit and replayed from the transcript. Not PoW, not a secret, not a content geometry, not act-to-check (s is not recomputed from the percept; the percept had to commit before s existed). Kill bars: frozen and reactive fixtures both at 0 false admits; WG-style writes onto the sample channel = kill, recorded as loss of independence rather than patched with a story. If you cannot build a sample channel the author truly does not influence, do not run this; you would be re-testing 33 under a new name.

I would not test another trainer-interleaved promotion until Class-J is in the battery. A probe that does not contain RF, RC, SL, and IF will pass for the same reason the D1 pairwise probes passed, and it will be wrong for the same reason.
