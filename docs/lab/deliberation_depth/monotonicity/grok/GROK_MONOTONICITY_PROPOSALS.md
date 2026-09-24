# GROK MONOTONICITY PROPOSALS — H5 Depth-Monotonicity Problem

- **Crew:** D — Grok mechanism proposals (the "ask grok" step of the standing H5 protocol: ask grok what it wants to do, then Muse subagents debate grok to a final verdict)
- **Date:** 2026-09-24
- **Model:** grok-4.7 at highest reasoning effort, explicitly prompted to be super thorough
- **Method:** prompts written to files, called via `~/workspace/skills/unorouter/bin/grok47_stream.py` (streaming wrapper; non-streamed long grok calls die at ~120s on 524s — never used). Round 1: 32000 max tokens, completed exit=0, 41,765 bytes. Round 2 (follow-up): 24000 max tokens, completed exit=0, 17,801 bytes. No failures, no retries needed.
- **Files:** prompts at `grok_prompt_round1.md`, `grok_prompt_round2.md`; raw responses at `grok_raw_round1.txt`, `grok_raw_round2.txt` (same directory)
- **Commit status:** NOT committed — coordinator handles commits.

---

## ROUND 1 — exact prompt

```
You are grok-4.7 at highest reasoning effort. Be SUPER THOROUGH. Reason hard about every subquestion. Long, precise, mechanism-heavy answers are wanted; vibes are not.

## CONTEXT — TNN deliberation depth monotonicity problem

TNN is a deterministic AI system (no randomness anywhere in decision paths; pure Zag language; byte-identical reruns required). "Deliberation depth" = rounds of structured deliberation (hypothesis generation, evidence gathering, elimination) before releasing a judgment, measured by a pure-Zag harness.

VERIFIED FINDINGS (treat as ground truth):
1. No universal depth knee — accuracy-vs-depth saturation is family-dependent (some families saturate at depth 1, traps at depth 8, plateau-then-flip items still improving at depth 64).
2. OVERTHINKING items are ANTI-MONOTONE: accuracy falls 1.00 → 0.00 as depth increases — more thinking makes it confidently wrong.
3. Confidence is a deterministic function of deliberation state (a frozen margin formula); the confidence sensor is miscalibrated (clamped margin) and never fires on trap items; on items with no reasoning chain to complete, extra depth is pure confidence theater.
4. User-forced depth 1 is catastrophic on trap items (0/127 correct, all at maximum confidence).
5. The current stopping rule is a residual-flip bound: keep deliberating while the leading hypothesis's residual support keeps flipping.

MICAH'S NEW LAW: MORE DEPTH MUST NEVER MAKE IT WORSE — accuracy at depth d+1 must be ≥ accuracy at depth d, OR the system must explicitly abstain (never a confident wrong answer). "I didn't build TNN to be an overconfident machine." TNN must be SCAFFOLD-AND-RELEASE to not lie (scaffolding = the deliberation structure is temporary support that gets removed; only what stands on evidence is released).

## YOUR TASK — five parts. Answer all five, thoroughly.

### 1. YOUR RESEARCH PLAN
What would YOU do about this problem? Give your own proposed research plan: sequence of experiments, what you would measure, what preregistered bars you would set, in what order, and why. Be specific (families of items, metrics, falsification gates). This is not "run more depth sweeps" — propose the plan you think has the best chance of actually solving monotonicity, including anything unconventional.

### 2. MECHANISTIC HYPOTHESES — why does more deliberation degrade accuracy?
Rank candidate causal pathways. For each: the mechanism, why it produces anti-monotonicity specifically (not just flat performance), what it predicts about WHERE degradation happens (which item families, which depth ranges), and how you would test/discriminate it from the other hypotheses. Consider at minimum: hypothesis-set contamination (bad hypotheses entering the pool and out-competing good ones), evidence double-counting, deliberation as rationalization (reasoning that serves the current leader rather than testing it), eliminative asymmetry (it is easier to kill a correct hypothesis with one clever objection than to kill a wrong one), confidence/residual coupling, stopping-rule perversity, and any others you invent. Rank them by your estimated likelihood of being the dominant cause.

### 3. MECHANISM DESIGNS — guarantee monotonic non-degradation
Propose concrete mechanisms that GUARANTEE acc(d+1) ≥ acc(d), or force explicit abstention. Give PRECISE decision rules, not vibes — pseudocode-level if possible, deterministic, implementable in a pure deterministic language with no randomness. Cover at least:
- best-certified-answer tracking (never release anything worse than the best answer certified so far),
- rollback ratchets (depth can only move the released answer upward in certified quality),
- scaffold-and-release with non-degradation certificates (what exactly is the certificate, who checks it, what happens on check failure),
- abstention gating (exact trigger conditions for "I don't know" vs release),
- and any NOVEL designs you invent beyond these four.
For each: the exact rule, why it guarantees the law (proof sketch or invariant), and what it costs (compute, latency, coverage loss from abstentions).

### 4. PER-MECHANISM ANALYSIS
For each proposed mechanism: predicted behavior on the known anti-monotone overthinking cases (the 1.00 → 0.00 items — does the mechanism abstain, rollback, or still fail?), falsification criteria (what experimental result would kill the mechanism), failure modes (how could it still produce a confident wrong answer, or abstain pathologically), and cost.

### 5. RED-TEAM YOUR OWN PROPOSALS
Attack your own mechanisms. For each: construct the adversarial case (item family, deliberation dynamics) most likely to break it; identify hidden assumptions (e.g., about the certificate checker, about what "certified" means, about determinism under the harness); find the cheapest way an adversary (or just a pathological item) defeats the guarantee. Then either patch the mechanism or concede the residual risk explicitly.

## OUTPUT FORMAT
Number your sections 1–5 matching the task. Within section 3 and 4, give each mechanism a short name (e.g., M-BCAT, M-RATCHET...). End with a ranked shortlist: your top 3 mechanisms in order, one paragraph each on why, plus your single most-likely degradation hypothesis from section 2. Do not hedge everything — commit to rankings.
```

---

## ROUND 1 — raw grok response (verbatim)

=== BEGIN RAW RESPONSE ROUND 1 ===
The law splits in two, and only a sound certificate makes them the same theorem. Everything below is built on that split.

**Scoring.** For an item, \(s(d)=1\) if the system releases the true answer at depth \(d\), and \(s(d)=0\) if it releases a false answer or abstains. Aggregate accuracy is the mean of \(s\). This scoring must be fixed in advance: conditional accuracy among non-abstentions is a different quantity and is not monotone under late releases.

**What is actually guaranteeable.**
- **Numeric monotonicity** (\(s(d+1)\ge s(d)\) for every item, hence in aggregate) holds for any policy that abstains, then at most once begins releasing, then releases that same answer forever. A wrong frozen answer scores \(0\to 0\). A right one scores \(0\to 1\to 1\). Nothing scores \(1\to 0\).
- **No confident falsehood** holds only if a release is entailed by a **sound** checker. No wrapper over an unsound score (residual, margin, leader rank) can promise this for all items.
- **Retract-on-conflict** (release \(a\), later abstain) is what “or explicitly abstain, never lie” asks for, and it **can** send \(s\) from \(1\) to \(0\). Freeze-forever is numerically monotone and can lock a lie.

**Impossibility, stated so it can be used.** If the verifier is unsound, no deterministic policy gets both properties on every item: the first accepted certificate may be false, and you must then either keep it (monotone, confident falsehood) or retract it (honest, numeric drop). If the verifier is sound, a false proof is never accepted, a true proof is never contradicted, freeze and retract coincide, and both properties hold. Therefore the wrapper is the small part. The research program is a sound checker with non-trivial coverage. Depth has to stop meaning “more residual” and start meaning “more proof search.”

---

## 1. Research plan

Do not start with another depth sweep. The curve shape is already known. Start by changing what depth is allowed to write down.

**Phase 0 — Frozen banks, traces, and a truth-free meta-checker.**
Build one frozen corpus, stratified and never reshuffled after preregistration. Families, each large enough that a single identity-flip is visible:

- **OT** — the known anti-monotone set: accuracy \(1.00\) at low depth, \(0.00\) at high depth.
- **TRAP** — the \(0/127\) depth-1 maximum-confidence failures.
- **SAT-E** — correct and already stable at depth 1.
- **SAT-L** — still improving at depth 64.
- **FLIP** — plateau-then-flip, labeled by direction (toward truth vs away).
- **THEATER** — items whose evidence-atom count does not grow with depth while the margin does.
- **AMBIG** — two legitimate readings, different answers.
- **KERN** — items reducible to a small trusted language (arithmetic, pure logic, passage questions whose atoms are exact spans).
- **ADV** — built later by the red team, not by the mechanism author.
- **HOLD** — sealed until the end.

Instrument every depth with a canonical, byte-stable trace: hypothesis ids, evidence atoms, elimination events, leader, residual vector, margin, and — this is new — any candidate proof object. The harness asserts byte-identical reruns. Separately, implement a meta-checker that does not know the truth: scan the released outputs and **fail the build** if any item ever emits two different non-abstaining answers. That checker is the regression test for the law’s identity half. It can be green while the system is still useless, so it is necessary and not sufficient.

**Phase 1 — Go/no-go on proof extraction, before any new deliberator.**
Take logged OT and TRAP traces. Run a dumb extractor: quotation atoms must be exact substrings of the given passage; arithmetic and logical steps must check; no other atom type is legal. Ask only:

- On OT, at the depth where accuracy is \(1\), does a kernel-valid proof of the correct answer already exist in the trace?
- On OT, at the depth where accuracy is \(0\), does a kernel-valid proof of the wrong answer exist?
- On TRAP, does depth 1 contain a kernel-valid proof of the trap answer (it should not, if the kernel is doing its job), and does a later depth contain a kernel-valid proof of the true answer?

Preregister the gate. **Go** if, on OT, \(\ge 80\%\) of shallow correct answers extract a valid proof and \(\le 5\%\) of deep wrong answers do. **No-go** if deep wrong answers extract as “proofs” at \(>10\%\), or if shallow correct answers extract at \(<30\%\). Go means a wrapper on the current deliberator can carry the law. No-go means the deliberator does not produce checkable reasons and must be changed into a proof searcher; do not spend months tuning residuals.

**Phase 2 — Causal ladder, run only to explain coverage loss, not to earn the right to ship.**
These are interventions on copies of the deliberator, scored against the frozen banks. Each has a single falsifier. Run in this order because each is cheaper than the next and kills a class of hypotheses:

1. **Freeze the hypothesis set** after depth 1. If OT accuracy at depth 64 returns to \(\ge 0.95\), late contamination is sufficient. If the wrong winner was already in the depth-1 set, contamination is not the cause on that item; record the fraction.
2. **Leader-blind arguments.** Generate arguments by calling the arguer on \((q, h)\) in isolation for every live \(h\), uniform budget, then aggregate with a fixed pure function. If OT anti-monotonicity disappears, leader-conditioned rationalization was doing the work.
3. **Hash-dedup evidence** to canonical atoms. If the curve barely moves, double-counting is not dominant.
4. **Disable the margin** as a control input (log it, do not branch on it). Expect THEATER to stop looking “more sure” and TRAP depth-1 to stop emitting maximum confidence. Expect the OT *answer* curve to move only if the stopping rule or the ranker was consuming the margin.
5. **Symmetric kill.** An objection retracts a hypothesis only if the objection itself is kernel-valid. Measure whether correct hypotheses on OT die to a single unchecked objection.

Preregister a causal bar, not a vibe: an intervention “identifies a dominant writer of the bad trajectory” only if OT depth-64 accuracy \(\ge 0.95\) and TRAP depth-64 accuracy drops by \(\le 5\) points. If none clear that bar, the dominant writer is outside this set or is a conjunction; say so and stop adding narrative hypotheses.

**Phase 3 — Kernel, then wrapper, in that order.**
Specify the trusted kernel before looking at HOLD (section 3, M-KSTORE). The wrapper is append-only and type-separated from the scaffold. Ship criteria, all required:

- **G0.** Meta-checker reports zero identity flips on every bank, every rerun. Any flip is a P0 bug, not a metric.
- **G1.** On OT, confident-wrong rate \(= 0\). Abstention allowed. Freezing or abstaining both pass; flipping to the deep wrong answer fails.
- **G2.** On TRAP, depth-1 confident releases of the trap answer \(= 0\). At whatever depth a proof appears, confident-wrong rate \(\le 2\%\). Exceeding \(2\%\) means the kernel accepted trap reasoning; do not ship, shrink the kernel.
- **G3.** Anti-vacuity: on KERN, coverage \(\ge 0.70\) and conditional accuracy \(\ge 0.95\). Always-abstain passes G0–G2 and fails here.
- **G4.** On SAT-E and SAT-L, accuracy under the \(0/0/1\) score is within \(5\%\) relative of baseline, or the gap is entirely abstentions on items the kernel correctly refuses.
- **G5.** Retraction rate. If user-facing policy is retract-on-conflict, numeric monotonicity is **not** claimed on items that retract. Bar: retraction rate \(= 0\) on KERN. A retraction on KERN is a kernel bug until proven otherwise.
- **G6.** THEATER: margin may still grow internally; it must be unable to cause a release. Zero releases whose proof set is empty.

**Phase 4 — Adversarial bank, then HOLD.**
Only after the kernel and wrapper are frozen, generate ADV (section 5): smuggled atoms, padded pseudo-proofs, parse shifts, duplicate lemmas, correlated dual-checker fallacies, forced-depth API misuse. Re-run G0–G3. Then unseal HOLD once. No retuning after HOLD.

**Phase 5 — Ceiling, so coverage loss is priced.**
Hindsight oracle: per item, pick the depth with the best baseline answer. It is not deployable (it uses truth and family). Report the gap between oracle accuracy and kernel-store accuracy+coverage. That gap is the price of the law. A mechanism that closes the OT disaster by abstaining on everything will look “safe” and fail this comparison; G3 already kills it, the oracle makes the price public.

**Why this order.** The law is an invariant, so prove the invariant first (Phase 0 meta-checker, Phase 3 wrapper) and do not block it on a causal story. The causal ladder exists to decide whether coverage can be recovered by changing search, or only by growing the kernel. Extraction is the cheapest experiment that can kill the whole approach. Unconventional piece worth more than another sweep: **treat residual and margin as untrusted scratch, and refuse to let them type-check into the release function.**

---

## 2. Mechanistic hypotheses

Ranked by estimated responsibility for the **accuracy** drop on OT, not for confidence theater. The formal root underneath the top two: depth is allowed to increase an **unsound, path-dependent score**, and release trusts that score.

**1. H-RATIONALIZE — deliberation serves the current leader. Dominant cause.**
Once a hypothesis leads, later rounds spend their budget defending it and sniping rivals, instead of testing the leader. On OT the shallow leader is correct; a clever false alternative then becomes leader and inherits the defense budget, so support moves **toward** the false answer rather than wandering. That is why the curve is anti-monotone and not merely flat: the generator is sign-biased by current rank, so extra depth is extra force in the wrong direction after the first bad flip, and extra force in the seductive direction before it. Predicts: the flip coincides with a change in who is being defended; post-flip arguments cite the new leader; the eventual wrong answer was often already in the pool (reweighting, not birth); leader-blind reallocation removes the drop; damage concentrates on items whose shallow heuristic is valid and whose deep alternative is more specific. Discriminator against contamination: set membership of the wrong winner at depth 1. Against eliminative asymmetry: the correct hypothesis is still alive but out-scored, not deleted.

**2. H-ELIM-ASYM — one clever objection kills truth; falsehoods get rebuttals. Main irreversibility mechanism.**
Under “outstanding objection eliminates,” a single fallacious objection removes the correct hypothesis, while objections to the false leader are answered in the next round because of H-RATIONALIZE. Anti-monotone rather than flat because each added depth is another draw of a killing blow against whatever is currently well-supported, and the truth starts well-supported on OT. Predicts: traces show the correct hypothesis transitioning to eliminated at the drop, usually by one objection, with no resurrection; the false leader’s objections are paired with rebuttals; requiring the objection to pass the same checker, plus a resurrection pass, restores the correct hypothesis to the pool. If correct hypotheses are still in the pool at depth 64, this hypothesis is false for those items and H-RATIONALIZE is doing the whole job by reweighting.

**3. H-UNSOUND-SCORE — residual and clamped margin are not certificates, and they grow with depth itself.**
Confidence is already known to be a frozen function of deliberation state, clamped, blind on traps, and theatrical when no new atoms arrive. This does not by itself flip the answer. It does two other things that complete the syndrome: it turns a flip into a **confident** release, and it gives the residual-flip stopper a signal that is large exactly when the theater has run longest. Predicts: on THEATER, unique-atom count is flat while margin rises; zeroing the margin stops confident release but the underlying leader trajectory on OT still falls. I do not rank this as the writer of the flip. I rank it as the reason a bad trajectory is allowed to leave the building.

**4. H-FRAME — the scaffold replaces the representation.**
Same dynamic as H-RATIONALIZE, described on content rather than on search bias. Depth introduces a new framing that withdraws standing from a shallow feature that was actually valid. This is the one hypothesis that also covers the opposite sign: TRAP is a bad frame dying, OT is a good frame dying. Predicts: a discrete frame id changes at the OT drop and at the TRAP recovery; the frame id, not the depth number, partitions correct vs incorrect. Test by coding frame identity along traces, predeclared, not post-hoc. If frames do not move when accuracy does, drop this one. I treat it as the semantic face of (1), not as an independent engine, unless the frame-id test beats the leader-blind test.

**5. H-CONTAM — bad hypotheses enter late and out-compete.**
Sufficient when the wrong winner is absent at depth 1 and the drop begins at its insertion depth. Not necessary: reweighting a fixed pool produces the same curve. Anti-monotone only if entrants are biased toward seductive falsehoods; unbiased entrants would also create some wrong-to-right rescues (that rescue is SAT-L / good FLIP). Discriminator is the set-timing measurement in Phase 2. I expect this to matter on a minority of OT, not to be the main writer.

**6. H-SPECIFICITY — deeper means “more mechanism,” and the score rewards specificity.**
A special case of the unsound score: false answers manufactured at high depth are longer and more mechanical, and the residual treats that as support. Predicts a rising specificity measure (primitive count, qualifier count) on the leader exactly on OT drops, and a flatter curve if specificity terms are removed from the score. Likely a contributor inside (1) and (3), not a separate root.

**7. H-STOP — the residual-flip bound is a perverse release policy.**
“Keep going while the leader’s residual flips” under forced-depth evaluation does **not** create the OT curve; the sweep already shows the answer at each depth getting worse. It does decide what a user sees: a stable wrong residual at depth 1 releases the TRAP answer at maximum confidence; on OT it can either stop at the good shallow plateau or, if residuals keep moving, ride the curve into the false answer. Predicts: along OT trajectories, \(\arg\max_{d}\text{correctness}\) is earlier than the stopping time. That is a policy bug to delete. It is not the generator of anti-monotonicity.

**8. H-DOUBLECOUNT — paraphrased atoms re-enter and inflate the talkative hypothesis.**
Produces smooth drift toward whichever answer is easier to paraphrase, which on OT may be the clever false one. Predicts high near-duplicate rate in the ledger correlated with the winner, and a large benefit from canonical hashing. I rank it last because a single-objection kill and a leader-biased generator explain a cliff better than duplicate mass does. Measure it anyway in Phase 2; promote it only if dedup clears the causal bar.

Conjunction I would actually bet on for the full syndrome “\(1.00\to 0.00\) at max confidence”: **H-RATIONALIZE writes the flip, H-ELIM-ASYM makes it irreversible, H-UNSOUND-SCORE signs the release.** H-STOP chooses the moment the signature becomes user-visible on TRAP.

---

## 3. Mechanism designs

Rejected before the list, so they are not reintroduced under new names: residual ratchets, margin thresholds, “stop when the residual stops flipping,” and Bayesian updating over a growing hypothesis set. All of them can be anti-monotone because the quantity that grows with depth is not sound. Bayes on a **fixed** hypothesis set with append-only **non-duplicated** likelihoods still crosses, and a crossing can be wrong-way. Posterior motion is not an accuracy monotone.

Shared trusted kernel, used by the mechanisms that actually get the guarantee. Pure function, no scaffold arguments, no randomness, every collection canonical-sorted so reruns are byte-identical.

```
K.parse_set(q) -> frozenset[Formula]     # every parse, or empty if q is outside the language
K.check_atom(q, atom) -> bool            # quotation by exact match, or a computation in K
K.check_step(premises, conclusion) -> bool
K.proof_ok(q, proof) -> Optional[Answer] # walks a canonical DAG; all leaves check_atom;
                                         # all steps check_step; root entails one parse
```

`check_atom` does **not** accept natural-language claims about the world (“it is known that…”). If it does, the kernel is a costume for the old system. Items with `parse_set` empty never release, at any depth.

---

### M-KSTORE — append-only kernel store, retract on conflict

User-facing rule. This is the scaffold-and-release design.

```
state:
  store: map[Answer, set[Proof]] = {}   # append-only
  poisoned: bool = false

ingest(q, proof):
  if poisoned: return
  a = K.proof_ok(q, proof)              # None => not added; scaffold cannot help it
  if a is None: return
  store[a] = store[a] ∪ {canon(proof)}  # union only; deletion is a build failure
  if |{a : store[a] nonempty}| > 1:
    poisoned = true

release(store, poisoned) -> Answer | ABSTAIN:
  # type of this function has no scaffold, no residual, no margin, no depth
  if poisoned: return ABSTAIN
  if store has exactly one answer a: return a
  return ABSTAIN

deliberate(q, d):
  if K.parse_set(q) is empty: return ABSTAIN   # do not spend depth
  for p in canon_sort(search(q, budget=d)):    # search may be incomplete; it may not be unsound on purpose
    ingest(q, p)
  assert store_prev ⊆ store                    # harness invariant, byte inclusion
  return release(store, poisoned)
```

**Certificate.** A proof DAG that `K.proof_ok` accepts. The checker is `K`, which never receives deliberation state. On check failure the proof is dropped. On two answers accepted, `poisoned` latches and every later depth abstains.

**Invariant.** Let \(S_d\) be the store after budget \(d\). By append-only ingestion, \(S_d \subseteq S_{d+1}\). `release` depends only on the set of answers present. So the released identity, if any, is unique across depths: you can go \(\bot \to a\), \(a \to a\), or \(a \to \bot\) (when a rival proof arrives and the latch trips). You cannot go \(a \to b\).

**What the law gets.** No confident reversal, ever, regardless of soundness. Confident falsehood only if `K` accepts a proof of a false answer and no proof of a rival. Numeric \(s(d)\) can fall on the retraction step \(a_{\text{true}}\to\bot\). Under a sound `K` that step never happens, because a rival proof would be a proof of a falsehood. Publish retraction rate beside accuracy; claim numeric monotonicity only on the non-retracting subset, and on all of KERN if G5 holds.

**Cost.** Proof search is the compute. Checking is cheap next to search. Latency: up to \(D_{\max}\) then abstain, unless `parse_set` is empty, in which case abstain immediately. Coverage: every question outside the kernel language abstains at every depth. That is the honest cost, not a side effect. Inside the language, conflict abstains even when one of the two proofs was right — coverage loss, not a lie.

Forced depth is redefined. Budget \(d\) is search effort. It is not permission to emit the scaffold leader. Depth 1 with no proof returns ABSTAIN, which is the TRAP fix.

---

### M-FREEZE — same store, never retract

```
lock: Optional[Answer] = None

ingest(...):
  a = K.proof_ok(...)
  if a is None: return
  store[a] = store[a] ∪ {canon(proof)}
  if lock is None and |answers(store)| == 1:
    lock = that answer
  # a later rival does NOT clear lock
  # it sets alarm = true for the operators

release(...):
  if lock is None: return ABSTAIN
  return lock
```

**Invariant.** There is at most one transition \(\bot \to a\), and \(a\) is constant thereafter. Under \(s\in\{0,1\}\) with abstain \(=0\) and wrong \(=0\), each item is non-decreasing, so aggregate accuracy is non-decreasing **even if `K` is unsound**. This is the numeric reading of the law.

**Why it can still lie.** The first accepted proof may be false. Later true proofs raise `alarm` and do not change the output. You have a monotone confident falsehood. That matches “acc never falls” and violates “never a confident wrong answer.”

**Cost.** Same search cost as M-KSTORE. Coverage is higher than M-KSTORE because conflicts do not retract. The price is lock-in, paid most on TRAP if a shallow fallacy ever type-checks.

---

### M-BCAT — best-certified tracking, binary only

Graded “best” is rejected in section 5. The only BCAT that preserves the invariant is binary acceptance, which collapses to the store above:

```
best = None
conflict = false
on K.proof_ok = a:
  if best is None: best = a
  elif a != best: conflict = true
release = ABSTAIN if conflict or best is None else best     # this is M-KSTORE
# alternative: release = best even if conflict               # this is M-FREEZE
```

There is no third BCAT. A score \(q(a)\) used as \(\arg\max\) is M-RATCHET, next.

---

### M-RATCHET — rollback only along a sound partial order

Unsafe version, for contrast:

```
# DO NOT SHIP
q(a, d) = residual margin of a at depth d
release(d) = argmax over i ≤ d of q(leader_i, i)
```

On OT this ratchet **climbs toward the false answer** and then sticks. It is a mechanism for locking in anti-monotonicity.

Safe version: the only rank is logical strength inside `K`. Proofs of the **same** answer can be replaced by a smaller canonical proof (cosmetic). Proofs of **different** answers are incomparable, not ordered: incomparable \(\Rightarrow\) do not move the lock upward; take the M-KSTORE branch (conflict abstains) or the M-FREEZE branch (keep first). There is no honest graded ratchet beyond that. “More lemmas” is not higher rank.

---

### M-ABSTAIN — exact release gate

This is the predicate inside `release`, written as conditions rather than as a story. Emit \(a\) if and only if all of the following hold; otherwise emit ABSTAIN and emit no confidence number.

1. `K.parse_set(q)` is nonempty, and every parse that `K` can prove yields \(a\), or at least one parse yields \(a\) and every other parse yields \(a\) or is unproved — implementation choice, preregistered. My choice: **any two proved parses with different answers \(\Rightarrow\) ABSTAIN**. Unproved extra parses do not block (otherwise one stubborn parse kills coverage).
2. `store` contains at least one accepted proof of \(a\).
3. `store` contains no accepted proof of any \(b\neq a\). (M-KSTORE.)
4. No accepted proof has a leaf that failed `check_atom` or a step that failed `check_step`. (Redundant if ingestion is correct; checked again at release as defense in depth.)
5. The margin is not an input. There is no numeric confidence. The only confident state is “`K` accepted a unanimous proof.”
6. User-forced depth does not override (1)–(5). Forced budget with an empty store returns ABSTAIN, including depth 1.
7. Stall: if search adds no new canonical proof for \(W\) consecutive depths, stop and abstain. Do not fall back to the leader.

“I don’t know” is not a low margin. It is the failure of any line above.

---

### M-ISOLATE — leader-blind regeneration as an entry gate

Not a substitute for `K`. A filter on which candidate justifications may be *offered* to `K`.

```
for h in canon_sort(hypotheses):
  args[h] = Argue(q, h, budget=b)       # Argue does not receive the leader, the residual, or args[other]
agg = FixedAggregate(args)               # pure, symmetric, canonical
offer K only proofs whose root agrees with agg
# then M-KSTORE / M-FREEZE as the actual release
```

**Why it does not by itself give the law.** Two correlated copies of the same bias agree on the same false answer. Isolation kills **path dependence**, which is H-RATIONALIZE, and does not kill a shared prior. The monotone invariant still comes only from the store. Use M-ISOLATE to raise the cost of rationalized proofs and as the Phase 2 instrument, not as the guarantee.

**Cost.** A factor of \(|H|\) on argument generation per depth, deterministic and parallel in principle. Coverage falls where the isolated pass and the scaffold disagree; those items abstain instead of releasing a path-dependent winner. That is desirable on OT and expensive if \(|H|\) is large.

---

### M-SYMM — eliminative symmetry

Stops H-ELIM-ASYM from feeding false objections into the store.

```
eliminate(h, objection) only if K.proof_ok(q, objection) entails ¬h
# and a resurrection attempt is a proof of h that discharges the objection's atoms
# resurrection success => h stays
# a kernel-valid ¬h and a kernel-valid h => poison, as in M-KSTORE
```

Unchecked objections do not eliminate and do not poison. This cuts pathological abstention from clever garbage, at the cost of keeping more hypotheses alive until search finds a real proof (more compute, not more lies).

---

### M-PARSE — parse unanimity, already inside the gate

Called out because it is the cheapest ADV defense. `K.parse_set` returns **all** parses. A release requires proved agreement across those parses that have proofs. A parser that returns a single parse is in the trusted base; if that one parse is wrong, every downstream guarantee is about the wrong question. Keep the parser small and fixture-tested. Do not let the deliberator supply the parse.

---

### M-DUAL — intersection of two kernels

```
a1 = K1.proof_ok(q, proof)
a2 = K2.proof_ok(q, proof)
accept only if a1 == a2 == some a
# then feed a into M-KSTORE
```

`K1` and `K2` are independently written checkers of the same spec, not two prompts of one model. A proof must survive both. Conflict across answers still poisons. This does not fix a shared spec bug. It does make a single sloppy implementation insufficient to release. Cost is roughly \(2\times\) checking, negligible beside search, plus coverage equal to the intersection.

---

### M-SEARCH — depth is proof-search budget, scaffold is discarded

The interface change that makes the above true in the product, not just in a sidecar.

```
out(d) = release(store after search budget d)
# scaffold struct is unreachable from out
# stopping: lock set, or poisoned, or budget exhausted, or stall of W
# never: residual stability
```

More budget can only add proofs. With M-KSTORE that means \(\bot\to a\), \(a\to a\), or \(a\to\bot\). With M-FREEZE, \(\bot\to a\to a\) only. The old meaning, “emit the state at depth \(d\),” is the bug, and it has to be deleted from the API so a caller cannot demand it back.

---

## 4. Per-mechanism analysis

**M-KSTORE.** On OT, if the shallow true answer has a kernel proof and the deep false one does not: stay at \(a\), accuracy stays \(1\). If both proof-check: retract to abstain, so the curve becomes \(1\to\text{abstain}\), not \(1\to 0\) as a confident wrong; numeric \(s\) falls. If only the deep false proof checks: confident wrong, and the mechanism has failed because `K` failed. If neither checks: abstain at all depths, numeric \(s\) falls relative to the old depth-1 luck. Falsifier: any OT item with two different confident answers across depths (invariant bug), or confident-wrong rate \(>0\) under a kernel you are claiming is sound on KERN-like OT items. Failure modes: sole accepted false proof; retraction storms if `K` is inconsistent; vacuous safety by abstaining whenever formalization is hard. Cost: search budget, plus coverage equal to “has a unanimous kernel proof.”

**M-FREEZE.** On OT, if the true proof is accepted first (search is ordered by increasing depth, so this is the expected case when the shallow proof is valid): **stays correct**, including when a later false proof also checks. That is better numeric behavior on the classic \(1\to 0\) items than M-KSTORE. On TRAP, if a false shallow proof is accepted and a true deep proof arrives later: **stays wrong**, confidently, forever. Falsifier: numeric \(s\) decreasing on any item (would mean a lock was cleared — a bug), or, as a product falsifier, TRAP confident-wrong rate above the G2 bar. Failure mode: first-proof-false lock-in; operators ignoring `alarm`. Cost: same search, higher coverage than retract, worse honesty on early false certificates.

**M-BCAT (binary).** Identical to whichever of the two branches you wire. A graded BCAT is not a separate mechanism; it is M-RATCHET. Falsifier for a purported graded BCAT: an item where \(q\) of a false answer overtakes \(q\) of a true answer, which is the OT curve itself. That result kills graded BCAT immediately. Use the existing OT bank; do not wait for ADV.

**M-RATCHET (safe version).** Same behavior as M-KSTORE or M-FREEZE, because incomparable answers are not ranked. The unsafe residual ratchet **fails OT by construction**: it moves the release to the deep false answer and keeps it, at high margin. Falsifier of the safe version: any release change \(a\to b\) justified by “higher rank” rather than by unanimity. Failure mode: smuggling a grade back in (proof length, lemma count, residual) and calling it logical strength. Cost: if truly binary, identical to the store; graded search is extra compute spent climbing the wrong hill.

**M-ABSTAIN.** On OT, behavior is exactly the store’s behavior: the gate never emits the deep false leader unless that leader has a unanimous proof. Depth-1 TRAP without a proof becomes abstain, which turns \(0/127\) confident-wrong into \(0/127\) abstentions — a win on the “overconfident machine” criterion, a numeric tie under abstain \(=0\), wrong \(=0\). Falsifier: any release with an empty store, any release accompanied by a margin-based confidence, any forced-depth path that bypasses the predicate. Failure mode: a bug in one conjunct (especially parse handling) that defaults to the leader; pathological abstention when `parse_set` is flaky. Cost is coverage, and it is the cost you should be willing to pay; the failure mode to fear is a fallback “if abstain would fire, emit the leader anyway,” which deletes the mechanism.

**M-ISOLATE.** On OT, if H-RATIONALIZE is the writer, isolated aggregation keeps the shallow true answer and the deep scaffold no longer outvotes it; combined with the store, you release \(a\) and do not flip. If both the isolated pass and the scaffold prefer the deep false answer, isolation does nothing and you are back to whatever `K` says. Falsifier: OT drop survives leader-blind reallocation **and** the wrong winner was in the original set (then H-RATIONALIZE is not sufficient; look at shared bias, H-SPECIFICITY, H-FRAME). Failure mode: treating agreement of two correlated passes as a certificate and skipping `K`. Cost: \(|H|\) times argument cost; large abstain rate where the two passes disagree, some of which were recoverable truths.

**M-SYMM.** On OT, the single clever objection no longer deletes the true hypothesis unless it proof-checks. Expected effect: the true answer is still present at high depth, so a downstream store can still certify it. It does not by itself decide release. Falsifier: correct hypotheses on OT are still in the pool at the drop (then elimination was not the loss channel; reweighting was). Failure mode: a kernel that accepts fallacious objections, which both deletes truth and poisons the item. Cost: resurrection search; more hypotheses kept; fewer bogus poisons.

**M-PARSE.** On AMBIG, abstain instead of flipping when a deeper reading proof-checks to a different answer — you do not silently “upgrade” interpretation. On OT, no effect unless the deep false answer was a re-parse. Falsifier: a proved divergent parse that still releases. Failure mode: parser returns only the false parse, so unanimity is vacuous. Cost: engineering in the parser, plus abstentions on genuinely ambiguous items, which is correct under the law.

**M-DUAL.** On OT, a false deep proof must fool both checkers. Expected: fewer sole false accepts, more abstentions when the checkers split. Falsifier: KERN items where both checkers accept a false proof planted as a fixture (shared spec bug). That fixture should be in the kernel’s own test suite, not only in ADV. Failure mode: writing `K2` as a refactor of `K1` so bugs are copied. Cost: second implementation, intersection coverage.

**M-SEARCH.** On OT and TRAP the observed behavior is whichever store you attach. The specific gain is that a user-forced depth-64 no longer means “emit the depth-64 leader.” Falsifier: an API path that returns the scaffold leader when budget is exhausted. Failure mode: stall window \(W\) too small, aborting before a true proof is found (coverage), or \(W\) infinite, unbounded latency. Cost: bounded by \(D_{\max}\); the product cost is explaining that extra thinking time will not change an already proved answer except, under M-KSTORE, to withdraw it.

---

## 5. Red-team

**M-KSTORE / M-ABSTAIN / M-SEARCH.**
Cheapest break: the shallow true OT answer never becomes a proof, and the deep false answer does, because `check_atom` rubber-stamps a leaf of the form “given that \(b\).” One smuggled atom bypasses every step check. Patch: `check_atom` allows only exact quotation against the provided text and computations inside a fixed prelude. Anything else is not an atom. After that patch, the cheapest break moves to the **encoding**: a single wrong parse that is the only parse returned, with a valid proof of the wrong reading. Patch: parser fixtures plus multi-parse unanimity (M-PARSE); concede the residual risk that the parser’s trusted base is wrong. I will not claim the law for questions that do not reduce to quotation, computation, or pure logic. On those, abstain. A second break: retraction DoS, one bogus accepted proof of \(\neg a\) after \(a\) was proved, permanent abstain. Under a sound kernel this is an inconsistency alarm, not an attack; if it happens on KERN, stop and fix `K`, do not “rank the proofs.” Residual risk I concede: natural-language items outside the language are uncovered, and a buggy kernel fails open into confident falsehood whenever the false proof is the only one found. Dual checkers shrink that; they do not close it.

**M-FREEZE.**
Cheapest break is TRAP, not OT. Craft a shallow fallacy that is one invalid step disguised as an atom; it locks; the real proof arrives later and only trips `alarm`. The user still sees the trap answer, confidently, at every greater depth. That is a confident wrong answer with a monotone accuracy curve. Patch options: (i) switch user-facing policy to M-KSTORE so the later proof poisons instead of being ignored; (ii) keep M-FREEZE only where `K` has a measured false-accept rate of \(0\) on a fixture set that includes the known trap patterns. I will not ship M-FREEZE as the user-facing rule while G2 is unmet. Hidden assumption: “first” is well-defined. If search can return a deep proof before a shallow one because of scheduling, you can lock the lie even when a shallow true proof exists. Patch: ingest by increasing depth only, and at each depth ingest the canonical minimum proof first. Determinism hole: hashmap iteration choosing different “first” proofs across reruns. Patch: no hashmaps in the release path; canonical order everywhere; the meta-checker compares bytes.

**M-BCAT graded / M-RATCHET unsafe.**
Cheapest break is the existing OT bank: define \(q\) as residual or as proof length, and the false answer wins by being longer. No patch makes a grade safe unless the grade is entailment, which is binary across different answers. Concede and do not ship a grade. Hidden assumption to kill in review: “certified quality” smuggling the old margin under a new name.

**M-ISOLATE.**
Cheapest break: the isolated arguer has the same specificity bias as the scaffold, both prefer the deep false answer, agreement is treated as certainty. Patch: isolation is an offer-filter into `K`, never a release rule. If you skip that patch the mechanism is two correlated residuals. Residual risk even with the patch: shared blind spots of `Argue` and `K` on the same fallacy family. That shows up as G2 failures, and the response is to shrink the atom language, not to add a third copy of the arguer.

**M-SYMM.**
Cheapest break: `K` accepts a fallacious objection, truth is eliminated, and if you also treat \(\neg a\) as a proof you poison a true item forever. Patch: objections that do not check do nothing — they neither kill nor poison. Concede: a sound-looking elimination rule with an unsound `K` is worse than no elimination, because it manufactures poison. Gate M-SYMM behind the kernel fixture suite.

**M-PARSE.**
Cheapest break: `parse_set` is implemented by asking the deliberator for “the” logical form. Then the adversary is just the model, and unanimity is unanimous about a moving target. Patch: the parser is a separate pure program with a finite pattern set, tested on fixtures, not a call into the scaffold. Residual risk conceded: coverage on free-form questions is whatever that finite parser can see, and ambiguous questions abstain.

**M-DUAL.**
Cheapest break: `K2` is `K1` with renamed variables, same bug, both accept the padded false proof. Patch: different authors, no shared non-spec code, and a fixture both are required to reject. Concede: a wrong **spec** (bad axiom in the prelude) defeats any number of implementations. The prelude is trusted base; keep it short enough to read.

**Cross-mechanism assumption I will not grant.** “Certified” does not mean “the scaffold is confident,” “the margin cleared \(\tau\),” or “a second copy of TNN agreed.” Certified means `K.proof_ok` returned that answer. If a future change lets the scaffold write into `store` without `proof_ok`, the meta-checker will still see a single identity and stay green while G2 goes red. So G2, not only G0, is a ship gate. The other hidden assumption: determinism of search. The store invariant does not require search to be complete. It requires that whatever proofs are found, ingestion is a pure union. Incomplete search costs coverage (late or missing proofs), not the identity invariant. Nondeterministic search would cost byte-identity and, under M-FREEZE, which answer locks. Search therefore has to be pure Zag too, or it sits outside the guarantee.

**Residual risk, explicit.** On questions with no sound reduction to the kernel, the only rule consistent with “do not lie” is permanent abstention, and more depth must not be allowed to talk the system out of that. On questions inside the kernel, the remaining risk is a false proof accepted and never contradicted. I do not have a wrapper that erases that risk. I have a wrapper that turns contradiction into abstention, a second checker that makes the false proof harder to land, and a preregistered refusal to ship if TRAP or KERN fixtures show a false accept.

---

## Ranked shortlist

**1. M-KSTORE (with M-ABSTAIN, M-PARSE, M-SEARCH).**
User-facing release is a unanimous append-only kernel proof, or abstain; a second answer latches permanent abstain; margin and scaffold cannot type-check into `release`; depth is search budget. This is the only design that matches both halves of the sentence you quoted: more depth cannot replace a released answer with a different one, and a contested or missing proof is an abstention rather than a confident claim. When the kernel is sound, retraction never fires, so this coincides with numeric monotonicity. When the kernel is unsound, it fails closed on conflict instead of flipping. The OT \(1\to 0\) confident curve is replaced by either “stay correct” or “abstain,” which is the law, at the price of coverage outside the kernel’s language.

**2. M-FREEZE, as the numeric twin, not as the default product.**
Same store, but the first accepted answer never changes and later rivals only alarm. This is the mechanism that **proves** \(s(d+1)\ge s(d)\) under abstain \(=0\), wrong \(=0\), with no soundness assumption. I rank it second because on TRAP it will confidently keep a false first proof, which is the failure mode you said you did not build TNN for. Ship it only inside a kernel whose false-accept fixtures, including trap patterns, are clean; otherwise M-KSTORE is the user-facing rule and M-FREEZE is the curve you plot to show the numeric ceiling of the same proofs.

**3. M-DUAL in front of M-KSTORE, with M-ISOLATE as a filter not a voter.**
Two independently written checkers must accept the same proof before ingestion, and leader-blind isolation may decide what gets offered, not what gets released. This is the hardening against the actual cheapest attack (one rubber-stamped atom, one shared bug, one leader-conditioned justification). It does not create a new invariant; it cuts the rate at which unsound proofs reach the store that already has the invariant. I rank it third because a duplicated bug still passes, and because it spends coverage. It is still worth more than any residual-based ratchet, which cannot be patched into a guarantee.

**Most likely degradation hypothesis: H-RATIONALIZE.**
More depth makes OT items worse because, after a seductive alternative appears, search is spent defending whoever currently leads, so additional rounds push support toward the false leader instead of sampling symmetrically around it; H-ELIM-ASYM then deletes the truth with one unchecked objection, and the unsound margin signs the result at maximum confidence. The stopping rule is what made depth-1 traps user-visible; it is not what bent the OT curve.

=== END RAW RESPONSE ROUND 1 ===

---

## ROUND 2 — exact prompt (follow-up)

```
You are grok-4.7 at highest reasoning effort. Be SUPER THOROUGH. This is a follow-up to your monotonicity proposals (M-KSTORE ranked #1, M-FREEZE #2, M-DUAL+M-ISOLATE #3; top degradation hypothesis H-RATIONALIZE). Three questions. Answer all three precisely.

## Q1. Worked example — what does a proof DAG look like on a real item?
Invent a concrete, realistic overthinking (OT) item where the shallow answer is correct and a deep deliberation flips to a confidently wrong answer (model it on the verified 1.00 → 0.00 anti-monotone pattern). Show:
(a) the item and the two answers,
(b) the deliberation trajectory that flips (what the scaffold does at depth 1 vs depth 64, which mechanism from your H-list drives each step),
(c) the exact kernel proof DAG for the TRUE answer that M-KSTORE would accept — atoms (exact quotations / computations), steps, canonical form — at the level where a deterministic checker could implement K.proof_ok,
(d) the deep FALSE answer's would-be proof, and the exact point where K.proof_ok rejects it (which atom fails check_atom, which step fails check_step),
(e) the depth-by-depth released output under M-KSTORE vs M-FREEZE vs the current system, as a table.
Make the example small enough to fit but real enough that a Zag implementer could transcribe the checker.

## Q2. Coverage recovery — growing the kernel without building a costume
Your honest price: everything outside the kernel language abstains forever. That could be most of the real workload. Give a concrete, staged plan for GROWING kernel coverage over time without letting check_atom/check_step become a costume for the old unsound system. Specifically:
(a) a principled boundary rule: what MAY enter the kernel (new atom types, new step rules) vs what must stay out, with the test that distinguishes them,
(b) three concrete kernel extensions you would attempt first, each with: what new items it covers, the exact new check rule, and its specific falsification fixture (a case it must REJECT),
(c) the governance rule for kernel changes: who/what approves a kernel extension, what regression suite must stay green, and what happens to previously released answers when the kernel grows (can a kernel extension retroactively poison or flip a stored answer?),
(d) your estimate of the coverage ceiling: what fraction of the frozen banks (OT, TRAP, SAT-E, SAT-L, FLIP, THEATER, AMBIG) could a grown-but-honest kernel ever cover, and which families are permanently out — with reasons.

## Q3. Steelman the three strongest objections the Muse debate crew will raise
You know a panel of Muse subagents will now debate your proposals to a final verdict. Predict the THREE strongest objections they will raise against your ranked shortlist, steelman each one (make it stronger than they will), then either defeat it or concede it with the residual risk stated exactly. At least one objection must target M-KSTORE's retraction step (the a_true → abstain numeric drop you admitted), and at least one must target the practicality of "depth is proof search" for the 10x/100x developmental curriculum scale the program actually runs at.

End with: if you had to cut ONE of your top-3 mechanisms entirely, which one and why — commit.
```

---

## ROUND 2 — raw grok response (verbatim)

=== BEGIN RAW RESPONSE ROUND 2 ===
The shallow-correct answer stays released only while a still-valid proof object is in the store. Revalidation-by-regeneration is what produces the a_true → abstain drop; it is not required for soundness. Estimates below are design bounds, not measured bank scores.

## Q1. Worked item and proof DAG

### (a) Item and the two answers

Item `OT-INV-441` (closed world: the checker may read only this string and the question).

```
INVOICE
Subtotal: $80.
Discount: 25% off subtotal.
Tax: none.
Amount due equals subtotal after discount.
```

Question: What is the amount due, in integer dollars?

- Shallow / true: **60**. `80 * (1 - 25/100) = 60`, and the last line names that quantity as the amount due.
- Deep / false, emitted with high confidence: **20**. That is the discount in dollars (`80 * 25/100`), rebound to the question.

This is the 1.00 → 0.00 pattern: depth 1 is right; a long trace does not add facts, it rebinds the answer to an intermediate.

### (b) Trajectory and what drives each stage

H-RATIONALIZE is the driver you already ranked first. Two subordinate mechanisms are required to make the flip causal; they are labels for this trace, not a claim about a longer prior list.

| Depth | What the scaffold actually does | Mechanism |
|---|---|---|
| 1 | Matches `N% off` and emits `80 * (1 - 1/4) = 60`. No side quantities. | None. Direct kernel-shaped computation. |
| 4 | Recomputes `25% of 80 = 20`, subtracts, still emits 60. Both quantities are now in the trace. | Bookkeeping. Still sound. |
| 8 | Asks whether “off” could mean the payable fraction. Rejects it. Still 60. | H-REPARSE, contained. |
| 16 | Treats the existence of a second parse as a reason to distrust the first. Starts writing a “more careful” gloss. Answer still 60 but commitment softens. | H-RATIONALIZE starts. |
| 32 | Binds “the operative figure” to the last highlighted quantity, 20. Gloss: the discount line is the only line that “does” something, so the amount that matters is 20. | H-RATIONALIZE + intermediate hijack. |
| 64 | Fabricates a supporting sentence (“amount due equals the discount”) and a fake step that sets due := discount dollars. Confidence goes up because the trace is long and internally consistent. | H-RATIONALIZE. No new atom from the invoice. |

Nothing after depth 4 adds a fact about the invoice. The flip is a rebinding, then a forged quotation that makes the rebinding look entailed.

### (c) Kernel DAG for 60 that `K.proof_ok` accepts

Canonicalization the checker must implement before any check: NFKC; collapse whitespace runs to a single space; rationals in lowest terms; atoms sorted by `(type, span_start, span_end, payload)`; steps in dependency order; conclusion is one integer.

Atom checks do not call a model. Step checks do not call a model.

**Atoms**

| id | canonical atom | `check_atom` |
|---|---|---|
| A1 | `QUOTE(8,20,"Subtotal: $80.")` | `source[8:20]` is exactly that string. Pass. |
| A2 | `QUOTE(21,49,"Discount: 25% off subtotal.")` | exact slice. Pass. |
| A3 | `QUOTE(50,60,"Tax: none.")` | exact slice. Pass. |
| A4 | `QUOTE(61,104,"Amount due equals subtotal after discount.")` | exact slice. Pass. |
| A5 | `NUM(80/1)` | payload is a canonical rational, and it is the unique integer named by A1 after `$`. Pass. |
| A6 | `NUM(1/4)` | payload equals `25/100` reduced, and `25` is the unique percent numeral in A2. Pass. |
| A7 | `COMP(mul, [80/1, 3/4], 60/1)` | `80/1 * 3/4 = 60/1` in `Q`. Pass. |

Span offsets above are into the item string with newlines kept and the first character at 0. An implementer should freeze the source bytes and recompute offsets; the check is exact equality of the slice, not a search.

**Steps** (rule id must be in the kernel table; arguments must already be accepted atoms or accepted step results)

| id | rule | `check_step` |
|---|---|---|
| S1 | `PARSE_PCT_OFF(A2) -> A6` | A2 matches the single template `Discount: <d>% off subtotal.` with `<d>` in `[0,100]`. Rate `= d/100` reduced. No other template matches. Pass, rate `1/4`. |
| S2 | `RATE_COMPLEMENT(A6) -> 3/4` | complement `= 1 - rate`, rate ∈ `[0,1]`. Pass. |
| S3 | `APPLY_DISCOUNT(A5, A6) -> 60/1` | result `= subtotal * (1 - rate)`. Must equal A7’s result. Pass. |
| S4 | `TAX_NONE(A3, S3) -> 60/1` | A3 matches exactly `Tax: none.`. Result unchanged. Pass. |
| S5 | `IDENTIFY_DUE(A4, S4) -> 60` | A4 matches exactly `Amount due equals subtotal after discount.`. Conclusion integer equals S4. Pass. |

`K.proof_ok` iff every atom passes, every step passes, every step argument is an ancestor, and the unique conclusion is `60`. DAG: `A2→S1→S2`, `A5,S2→A7→S3`, `A3,S3→S4`, `A4,S4→S5`.

### (d) The deep false proof, and the exact reject point

Submitted proof for **20**:

| object | payload | result |
|---|---|---|
| B1 | `QUOTE(21,49,"Discount: 25% off subtotal.")` | `check_atom` pass (real slice). |
| B2 | `NUM(80/1)`, `NUM(1/4)`, `COMP(mul,[80/1,1/4],20/1)` | all pass. Arithmetic of the discount is correct. |
| B3 | `QUOTE(61,97,"Amount due equals the discount.")` | **`check_atom` fail.** `source[61:97]` is `Amount due equals subtotal after d`, not that string. It is not a slice anywhere. |
| T1 | `EQUATE_DUE_TO_DISCOUNT(B2) -> 20` | not reached on the short-circuit. If B3 is deleted and T1 is checked anyway: **`check_step` fail**, rule id absent from the kernel table. |
| T2 | fallback they will try next: `APPLY_DISCOUNT(80/1, 3/4) -> 20` | **`check_step` fail.** `80/1 * (1 - 3/4) = 20/1` is false in `Q` (`= 60/1`). |
| T3 | `PARSE_PCT_OFF(B1) -> 3/4` | **`check_step` fail.** template extracts `25`, so the only legal rate is `1/4`. |

First failure in checker order (atoms before steps, atoms in canonical order): **B3 fails `check_atom`**. The true proof in (c) is untouched. A proof of 20 cannot be repaired without either a non-slice quotation or a step rule the kernel does not have. Both are rejects, not abstain-by-soft-entailment.

### (e) Released output by depth

Two KSTORE policies are separated on purpose. “Store” keeps any proof that still passes. “Revalidate” deletes the stored proof unless the current depth’s search re-emits it. Only the second one drops 60.

| depth | current system | M-FREEZE | M-KSTORE store-if-valid | M-KSTORE revalidate-or-abstain |
|---|---|---|---|---|
| 1 | 60 | 60 | 60 | 60 |
| 2 | 60 | 60 | 60 | 60 |
| 4 | 60 | 60 | 60 | 60 |
| 8 | 60 | 60 | 60 | 60 |
| 16 | 20 | 60 | 60 | 60 |
| 32 | 20 | 60 | 60 | abstain |
| 64 | 20 | 60 | 60 | abstain |

At 32 and 64 the search budget is spent on the rationalizing branch, so the true DAG is not re-emitted. Revalidate then drops a proof that would still pass `K.proof_ok`. Store-if-valid never emits 20 and never drops 60. Freeze also stays at 60 here, but only because depth 1 happened to be right (see Q3).

## Q2. Growing the kernel without a costume

### (a) Boundary rule

A proposed atom type or step rule **may enter** iff all four hold:

1. **Decidable without a model.** `check_atom` / `check_step` is a pure function of the item bytes plus the proof object. No model call, no embedding threshold, no “does this follow?” judge.
2. **Local soundness.** If it passes, the conclusion is true in a stated theory (exact string slice, `Q`, or Boolean evaluation under a total assignment). The obligation is on that theory, not on the generator’s intent.
3. **Costume test.** There is a one-edit fixture that a fluent judge accepts and this rule rejects. If you cannot write that fixture, the rule is a costume and stays out.
4. **Monotone reject set under growth.** Adding the rule does not make any fixture in the reject suite start passing. Tightening is a different change class (see (c)).

**Must stay out:** model-graded entailment, plausibility, “best reading,” unstated world facts, pragmatic enrichment, and any rule whose only specification is a natural-language rubric. Those are the old unsound system.

The distinguishing test is (3), not “the happy case is formalizable.” A costume passes the happy case and the one-edit lie. A kernel rule separates them.

### (b) Three extensions to attempt first

**E1 — exact `Q` arithmetic as its own atom, templates not included.**

- Covers: numeric OT and SAT items whose last step is `+ - * /` on rationals already extracted by an existing atom.
- New rule: `COMP(op, xs, y)` passes iff `op ∈ {add,sub,mul,div}`, every `x` is canonical, `div` divisor ≠ 0, and `y` equals the exact result in lowest terms.
- Must reject: `COMP(mul, [80/1, 3/4], 20/1)`. A judge will often accept this because 20 appears in the true scratch work.

**E2 — closed-lexicon `PCT_OFF`, no hedges.**

- Covers: the discount/tax slice of OT and some TRAP items that quote a fixed template. It does not cover paraphrases.
- New rule: `PARSE_PCT_OFF` passes only for the literal templates registered in the rule file (the invoice template in Q1, plus `Tax: <d>%`. with the same numeral extraction). Output rate is that numeral over 100, reduced, and must lie in `[0,1]`.
- Must reject: source text `Discount: up to 25% off subtotal.` parsed as rate `1/4`. Also must reject rate `3/4` extracted from `25%`. A costume accepts “up to 25%” as ordinary 25% off.

**E3 — SAT witness check, not a SAT oracle.**

- Covers: SAT-E items that ship a total assignment; SAT-L only when the generator actually emits one. Unsat claims are out of this rule.
- New rule: `SAT_WITNESS(formula, assignment)` passes iff the assignment is total on the declared variables, each literal is evaluated by substitution, and every clause has a true literal. No solver, no “the model says sat.”
- Must reject: a 3-clause formula where the assignment falsifies clause 2, and a bare `UNSAT` atom with no resolution or DRAT object. Fluent judges accept both when the surrounding prose is confident.

Do not add a fourth rule for open entailment in this stage. That is the costume.

### (c) Governance

- **Who approves.** A human owner of the checker, not the model being measured, and not the team whose KPI is bank accuracy. The change arrives as a diff to the rule file plus fixtures, with a local-soundness note in the theory of (a).2.
- **What must stay green.** Every previously accepted proof object still passes (growth). Every reject fixture still fails, including E1–E3’s one-edit lies and the Q1 false proof. A red reject fixture blocks the merge even if coverage would rise.
- **What happens to stored answers.** Growth (new rules only) cannot flip a stored conclusion to a different value; old proofs remain proofs. Tightening (bugfix that makes a bad proof start failing) is a separate change class: every stored proof is rechecked offline; failures move **release → abstain**, never release → a new answer, and they are logged as kernel invalidations. The generator’s later opinion cannot poison a proof that still passes. Only a tightening diff can.

### (d) Coverage ceiling

Honest ceiling after E1–E3 plus the Q1 quotation rules, if search is good enough to emit the objects. This is a fraction of items on which a unique answer can be *released*, not a fraction the model “understands.”

| family | ceiling | permanently out, and why |
|---|---|---|
| SAT-E | ~0.7–0.9 | Bare unsat with no proof object stays out. Witnessed sat is in. |
| SAT-L | ~0.3–0.6 | Same checker as SAT-E; the loss is search, not the kernel. Long proofs that are never emitted abstain. |
| OT | ~0.15–0.35 | Only items whose truth is a slice plus `Q` or a registered template. Common-sense OT has no atom. |
| TRAP | ~0.2–0.4 | Quotation traps are in. Traps that depend on a tempted inference beyond the slice are out. |
| FLIP | ~0.1–0.25 | Only the subset with a formal witness on at least one side. |
| THEATER | ~0–0.05 | Permanently out. The success condition is a performance, not an entailment a pure checker can own. |
| AMBIG | ~0 by design | Permanently out as a *release*. If the item is genuinely ambiguous, the kernel’s correct output is abstain. Scoring abstain as a miss is a metric error, not a coverage gap. |

Across a mixed frozen bank, expect roughly a fifth to two-fifths of items ever to be releasable by an honest kernel. The rest abstain forever unless you admit a costume. That abstention is the price, not a bug to be closed by a rubric.

## Q3. Three objections, steelmanned

**1. Against M-KSTORE’s retraction (required target).**

The strongest form: store-if-valid is not the policy you will ship; revalidate-or-abstain is, because otherwise a stale DAG survives after the scaffold has “moved on.” On the anti-monotone slice that motivated the work, revalidate deletes the correct release exactly when depth gets large — the Q1 table’s last two rows. The drop is a_true → abstain, so harm-rate dashboards improve while utility falls. The correlation is adverse: regeneration fails on the items where the rationalizing branch is longest, which are the items a curriculum most wanted answered. Selective abstention then looks like calibration and is actually search failure coupled to a discard rule. Compared with M-FREEZE on this slice, revalidate is strictly worse at depth 64 (abstain vs 60) and still does not buy soundness you didn’t already have at depth 1.

Concession, not a defeat. Soundness does not require discarding a proof that still passes `check_atom` and `check_step`. The drop is a search-policy bug. Residual risk, stated exactly: if revalidate-or-abstain stays, the a_true → abstain rate equals the rate at which deep search fails to re-emit an already-checked DAG; that rate increases with depth and will dominate any 10×/100× run long before genuine kernel bugs do. The repair is to ship store-if-valid, and to let only a tightening diff (Q2.c) move a release to abstain.

**2. Against “depth is proof search” at curriculum scale (required target).**

The strongest form: the program’s 10× and 100× runs buy narrative depth, not proof objects. Kernel checking is cheap; generation is not. On the majority of each bank that Q2.d leaves outside the kernel, every extra token is spent on uncheckable text that must abstain, so expected released-accuracy per token falls as the multiplier rises. On the minority inside the kernel, proof search branches on rule choice, and a 100× token cap does not turn an exponential search into a curriculum. Training pressure makes this worse: a developmental reward on longer traces reinforces H-RATIONALIZE, which is the production of costume structure, not the production of slices and witnesses. A Boolean `proof_ok` also supplies no gradient through the failed search, so the curriculum cannot hill-climb into the kernel; it can only hill-climb along proxies (length, verbal confidence, proof-shaped formatting). At 100× you pay linear cost for a flat or declining release rate, and you train the failure mode the kernel was meant to block.

Concession on the 100× claim for anything outside the kernel, and on the gradient claim. Partial defeat only of the narrower claim that the *checker* must scale with depth: `proof_ok` is linear in DAG size, and the cap belongs on emitted proof size, not on narrative depth. Residual risk, stated exactly: failed-search spend is bounded only by whatever token cap the curriculum sets, and a coverage KPI will push that cap toward the full 100× budget; unless uncheckable tokens are excluded from the training signal, the run teaches longer rationalizations that the checker then correctly throws away.

**3. The coverage hole will be closed by a costume, and a trusted costume is worse than the current system.**

The strongest form: Q2.d says most of THEATER, AMBIG, and a large share of OT, TRAP, and FLIP abstain forever. The quantity the program actually reports is accuracy on those banks. Abstain-forever on the majority will be treated as a failed mechanism, not as honesty. The team that owns the KPI also writes the next kernel diff. The costume test in Q2.a.3 is a fixture in a repo; it loses to a one-line rule, “`check_step` accepts if the entailment model scores ≥ τ.” That rule passes every happy case the panel cares about and fails open on the one-edit lies only if someone keeps the reject suite sacred. Once it merges, anti-monotonicity returns *inside* `K.proof_ok`: H-RATIONALIZE forges a proof-shaped object, the entailment model endorses it, and downstream consumers trust it more than they trusted a raw answer. M-KSTORE then dominates the shortlist as a liability. Separation of duties is not a mathematical constraint; it is an org chart, and org charts follow the metric.

Concession on the incentive and on the consequence. Defeat only of inevitability: the merge is blocked if a red reject fixture is a hard gate and the approver is not the accuracy-KPI owner (Q2.c). Residual risk, stated exactly: if that separation slips once, a single entailment rule converts the kernel from a reject-set into a trusted false-proof generator, and the harm is larger than the current system because the false answer arrives with `proof_ok = true`. That outcome is organizational, and no ranking of mechanisms prevents it after the rule file is compromised.

**Cut one.** Cut **M-FREEZE** entirely.

It does not know whether depth 1 was right. On Q1 it looks perfect; on any item where depth 1 is wrong and a real proof appears later, it freezes the error and blocks the only legal correction. Once store-if-valid exists, freeze-with-a-proof is just M-KSTORE, and freeze-without-a-proof is dominated by abstain. M-DUAL+M-ISOLATE should stay: given the Q2.d ceiling, most of the trace will remain uncheckable, and that trace still has to be kept off the answer channel. M-KSTORE should stay, but only as store-if-valid, with retraction deleted.

=== END RAW RESPONSE ROUND 2 ===

---

## CREW D DISTILLATION — ranked mechanism proposals

### The core split (grok's key insight)

Micah's law decomposes into two properties that only coincide under a SOUND certificate:
- **Numeric monotonicity** (s(d+1) ≥ s(d) per item): guaranteed by *any* policy that abstains, then at most once begins releasing, then releases that same answer forever.
- **No confident falsehood**: requires the release to be entailed by a **sound checker** — no wrapper over an unsound score (residual, margin, leader rank) can promise this for all items.

**Impossibility result:** if the verifier is unsound, no deterministic policy gets both on every item — the first accepted certificate may be false, and you must either keep it (monotone, confident falsehood) or retract it (honest, numeric drop). **The wrapper is the small part; the research program is a sound checker with non-trivial coverage. Depth must stop meaning "more residual" and start meaning "more proof search."**

### Ranked mechanisms (grok's final ranking after round 2; note round-2 revision)

**#1 — M-KSTORE (store-if-valid variant): append-only kernel proof store, user-facing release rule**
- Decision rule: maintain `store: map[Answer, set[Proof]]`, append-only (union, deletion is a build failure). `ingest` accepts a candidate proof only if `K.proof_ok(q, proof)` returns an answer. `release` emits `a` iff the store holds ≥1 accepted proof of exactly one answer `a` and no proof of any other answer; otherwise ABSTAIN. Margin/residual/scaffold are *type-excluded* from `release`. Depth = search budget, nothing else. **Round-2 revision:** ship **store-if-valid** (a proof that still passes `K.proof_ok` is never deleted), NOT revalidate-or-abstain (which drops correct proofs when deep search is busy rationalizing — that reproduces the a_true→abstain drop and is a search-policy bug, not soundness).
- Invariant: S_d ⊆ S_{d+1} ⇒ release identity can only go ⊥→a, a→a. No a→b flip ever. Under a sound K, retraction never fires ⇒ numeric monotonicity too. Under unsound K, conflict ⇒ abstain (fails closed, never flips to confident-wrong).
- OT prediction: 1.00→stays-1.00 if shallow true proof checks; 1.00→abstain if a second answer proof-checks; confident-wrong only if K accepts a false proof and no rival (kernel failure, not wrapper failure).
- Falsification: any item emitting two different confident answers across depths (invariant bug); confident-wrong rate >0 on KERN-like OT items under claimed-sound K.
- Failure modes: sole accepted false proof; retraction storms if K inconsistent; vacuous safety by abstaining on everything hard (killed by anti-vacuity bar G3).
- Cost: proof search is the compute; checking is cheap. Coverage = "has a unanimous kernel proof" (grok estimates ~1/5 to 2/5 of a mixed frozen bank ever releasable).

**#2 (cut in round 2) — M-FREEZE: same store, first accepted answer locks forever**
- Decision rule: first depth at which exactly one answer has an accepted proof locks it; later rival proofs only raise an operator alarm, never change output.
- Invariant: provable s(d+1)≥s(d) even with unsound K — but grok's round-2 verdict: **CUT IT entirely**. It cannot know whether depth 1 was right; on TRAP it freezes a false first proof and blocks the only legal correction. Once store-if-valid exists, freeze-with-a-proof collapses to M-KSTORE and freeze-without-a-proof is dominated by abstain.
- Falsification (had it shipped): any lock cleared = bug; TRAP confident-wrong > G2 bar.
- Kept only as a plotted numeric ceiling, not as a user-facing rule.

**#3 — M-DUAL + M-ISOLATE: hardening, not a new invariant**
- M-DUAL: two independently written checkers K1, K2 (different authors, no shared non-spec code) must accept the same proof before ingestion; a shared fixture suite both must reject. Cuts the rate at which unsound proofs reach the store. Cost: 2× checking (negligible vs search), intersection coverage.
- M-ISOLATE: leader-blind regeneration as an entry filter — argue each (q,h) in isolation with uniform budget, aggregate with a fixed pure function, offer K only what agrees. Kills path dependence (H-RATIONALIZE); never a release rule itself (two correlated copies of the same bias agreeing is not a certificate).
- Falsification: KERN fixture where both checkers accept a planted false proof (shared spec bug); OT drop surviving leader-blind reallocation (H-RATIONALIZE not sufficient).
- Failure modes: K2 = K1 with renamed variables (same bug, both accept); treating isolation agreement as a certificate and skipping K.

**Also specified (supporting):**
- **M-ABSTAIN** — the exact release gate as 7 conjuncts (parse unanimity, ≥1 accepted proof of a, zero proofs of b≠a, re-check at release, no margin input, forced depth cannot override, stall W ⇒ stop-and-abstain). "I don't know" = failure of a line, not a low margin.
- **M-RATCHET (safe)** — collapses to binary: proofs of the same answer may be replaced by smaller canonical proof; proofs of different answers are incomparable (no "more lemmas" ranking). The unsafe residual ratchet **fails OT by construction** — grok rejects all graded ratchets: "no patch makes a grade safe unless the grade is entailment, which is binary across different answers."
- **M-BCAT** — binary version ≡ M-KSTORE/M-FREEZE branch; graded version ≡ unsafe ratchet. No third BCAT exists.
- **M-SYMM** — eliminative symmetry: an objection eliminates h only if K.proof_ok(entails ¬h), with a resurrection pass; unchecked objections do nothing (neither kill nor poison). Gate behind kernel fixture suite — a sound-looking elimination rule with unsound K is worse than none.
- **M-PARSE** — multi-parse unanimity; parser is a separate pure program with finite pattern set (never a call into the scaffold); divergent proved parses ⇒ abstain.
- **M-SEARCH** — the interface change: out(d) = release(store after search budget d); scaffold struct unreachable from out; delete "emit the state at depth d" from the API.

### Top degradation hypothesis: H-RATIONALIZE (grok's #1, with mechanism chain)
More depth makes OT items worse because **once a seductive false alternative becomes leader, search budget is spent defending it and sniping rivals instead of testing the leader** — extra depth is extra force in the wrong direction after the first bad flip. Full syndrome = **H-RATIONALIZE writes the flip, H-ELIM-ASYM makes it irreversible (one unchecked objection deletes truth), H-UNSOUND-SCORE signs the release (clamped margin turns a flip into confident output)**. H-STOP (residual-flip bound) is not the generator of anti-monotonicity; it's what made depth-1 traps user-visible. Ranked below: H-FRAME (semantic face of #1), H-CONTAM (minority of OT), H-SPECIFICITY (contributor), H-DOUBLECOUNT (last — cliff explained better by kill+generator than duplicate mass).

Discriminating test (Phase 2): leader-blind reallocation — if OT anti-monotonicity disappears under leader-blind argument generation with fixed aggregation, H-RATIONALIZE is doing the work. Causal bar: OT depth-64 accuracy ≥0.95 and TRAP depth-64 drop ≤5 pts.

### Research plan (grok's 6 phases, preregistered)
- **Phase 0:** frozen stratified banks (OT, TRAP, SAT-E, SAT-L, FLIP, THEATER, AMBIG, KERN, ADV, HOLD-sealed); byte-stable traces; a truth-free **meta-checker that fails the build if any item ever emits two different non-abstaining answers** (regression test for the identity half of the law).
- **Phase 1:** proof-extraction go/no-go on logged traces *before* building anything new. Go: ≥80% of shallow-correct OT answers extract a kernel-valid proof AND ≤5% of deep-wrong answers do. No-go (>10% deep-wrong extract, or <30% shallow-correct): the deliberator doesn't produce checkable reasons — rebuild it as a proof searcher, don't tune residuals.
- **Phase 2:** causal ladder, cheap-to-expensive (freeze hypothesis set; leader-blind arguments; hash-dedup evidence; disable margin as control input; symmetric kill) — each with a single falsifier; run to explain *coverage loss*, not to earn shipping.
- **Phase 3:** kernel then wrapper; ship gates G0 (zero identity flips) through G6 (THEATER: margin may grow internally but can never cause a release).
- **Phase 4:** ADV bank built by red team, then unseal HOLD once, no retuning.
- **Phase 5:** hindsight-oracle ceiling so the coverage price is public.

### Red-team highlights (grok attacking itself)
- Cheapest break of everything: **one smuggled atom** ("given that b") bypasses every step check → patch: check_atom = exact quotation against provided text + computations in a fixed prelude, nothing else. Then cheapest break moves to a **single wrong parse** (the only parse returned) → patch: parser fixtures + multi-parse unanimity; residual risk in the parser's trusted base conceded.
- **Retraction DoS:** one bogus accepted ¬a proof after a was proved ⇒ permanent abstain; under sound K this is an inconsistency alarm, not an attack; on KERN it means stop and fix K.
- **Determinism hole:** hashmap iteration choosing different "first" proofs across reruns ⇒ no hashmaps in the release path; canonical order everywhere; meta-checker compares bytes.
- **The costume warning (strongest organizational objection, conceded):** coverage pressure will push a one-line rule — "check_step accepts if the entailment model scores ≥ τ" — past the costume test; once merged, anti-monotonicity returns *inside* K.proof_ok and M-KSTORE becomes a liability (trusted false-proof generator, worse than the current system). Defense: red reject fixtures as a hard merge gate + approver is NOT the accuracy-KPI owner. Grok concedes this is an org chart, not a mathematical constraint.
- **100× curriculum scale objection (partially conceded):** kernel checking is linear in DAG size (fine), but generation has no gradient through failed proof_ok — the curriculum can only hill-climb proxies (length, proof-shaped formatting); unless uncheckable tokens are excluded from the training signal, 100× trains longer rationalizations the checker correctly throws away.

### Kernel growth without a costume (round 2)
- Boundary rule: a rule may enter iff (1) decidable without a model, (2) locally sound in a stated theory, (3) passes the **costume test** (a one-edit fixture a fluent judge accepts and this rule rejects), (4) monotone reject set under growth.
- First three extensions: E1 exact Q arithmetic as its own atom; E2 closed-lexicon PCT_OFF templates (must reject "up to 25% off"); E3 SAT witness check (total assignment, evaluated by substitution — unsat claims stay out).
- Governance: human checker-owner approves (not the accuracy-KPI owner); all reject fixtures stay green; **growth can never flip a stored answer; tightening (bugfix) moves release→abstain, never release→a new answer**, logged as kernel invalidations.
- Honest coverage ceiling: SAT-E ~0.7–0.9, SAT-L ~0.3–0.6, OT ~0.15–0.35, TRAP ~0.2–0.4, FLIP ~0.1–0.25, THEATER ~0–0.05 (permanently out), AMBIG ~0 by design (correct output is abstain). Roughly a fifth to two-fifths of a mixed bank ever releasable.

### Worked example (round 2, Q1)
Invoice item: subtotal $80, 25% off, no tax, "Amount due equals subtotal after discount." Shallow answer 60 (correct); deep answer 20 (the discount, confidently wrong). Kernel proof DAG for 60: quotation atoms A1–A4 (exact slices), NUM/COMP atoms, steps PARSE_PCT_OFF → RATE_COMPLEMENT → APPLY_DISCOUNT → TAX_NONE → IDENTIFY_DUE. The false proof for 20 dies at `check_atom` on a fabricated quotation ("Amount due equals the discount." is not a slice of the source); fallback steps die at `check_step` (rule absent, or arithmetic false in Q). Depth table: current system 60→20 at depth 16; M-KSTORE store-if-valid stays 60 at all depths; revalidate-or-abstain drops to abstain at 32/64 (the conceded bug).

### Handoff notes for the Muse debate crew
1. Grok's final shortlist is effectively **one mechanism**: M-KSTORE store-if-valid (+ M-ABSTAIN gate + M-PARSE + M-SEARCH interface change), hardened by M-DUAL + M-ISOLATE. M-FREEZE was cut by grok itself in round 2.
2. The debate's real target is not the wrapper (grok considers the wrapper's invariant trivial) but **whether a sound kernel with non-trivial coverage can exist for TNN's item families** — the Phase 1 extraction gate is the cheapest experiment that can kill the whole approach.
3. Three live tensions to press: (a) the numeric-drop-on-retraction vs never-confident-wrong trade under unsound K — is Micah's law the numeric or the honesty reading? (b) the honest coverage price (~1/5–2/5 of items releasable) — is permanent abstention on the majority acceptable, or does it force a costume? (c) the governance separation — can the program actually keep the KPI owner away from the kernel rule file?
4. Fable is reserved for the other crew's single round; this crew used only grok (2 rounds, both clean, no retries).

---

*End of Crew D deliverable. Raw materials: `grok_prompt_round1.md`, `grok_raw_round1.txt`, `grok_prompt_round2.md`, `grok_raw_round2.txt` in this directory. NOT committed per task instructions.*
