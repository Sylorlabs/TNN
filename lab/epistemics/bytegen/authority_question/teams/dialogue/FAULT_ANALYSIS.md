# FAULT_ANALYSIS.md — where output feedback would help vs corrupt in dialogue

Method: for each concrete fault class, ask (i) what the fault is, (ii) whether any output-side measurement could detect it against a plan-derived expectation, (iii) whether the correction could be anything other than plan-pure re-emission, and (iv) what breaks if the output is given authority.

## A. Faults where output feedback would genuinely HELP — audited honestly

### A1. Assembly corruption (buffer overflow, truncated copy, interleaved writes)
- **Fault:** `rput` writes past `resp`'s 1088 bytes, or a `copy_bytes` length bug truncates a fact mid-word. The emitted bytes would not match any plan content.
- **Detection:** possible — compare emitted bytes against the plan-derived expectation (the fact text + template literals). This is a pure `beq` assertion, no sensor involved.
- **Correction:** the only valid correction is re-assembly plan-pure — a constant map in the measured output (Lipschitz 0, one-step). There is nothing to "servo toward": the target is byte-exact, not approximate.
- **Honest assessment:** this collapses to a build-time assertion, not a feedback loop. There is no noise in memcopy; if the assert fails, the binary is broken and no runtime loop fixes that. The audio exception path exists because physical faults (bit flips, dropouts) strike rendered bytes *after* a correct render; in dialogue, render and emission are the same memcopy — there is no "after." **Verdict: feedback adds nothing; a static assert suffices.**

### A2. The `last_fid` continuity tie-break (`retrieve`, dialogue.zag:973)
- **Mechanism (existing, plan-side):** on an exact Jaccard tie, prefer the previously emitted fact. This is the one place prior-turn output-adjacent state biases generation.
- **Where it helps:** "tell me more"-style continuations and repeated topical queries resolve stably instead of flip-flopping between tied facts.
- **Where it could corrupt:** a stuck loop. If the user repeats an identical query, the tie persists and the same fact re-emits forever. Note the bound: it fires **only on exact ties** (`lhs==rhs`), never overrides a strictly better score, and the correction branch *excludes* the previous answer explicitly (`excl_fid`, :1592) — so "no, the other one" always escapes. The stuck-loop scenario is user-driven repetition, and re-answering the same question identically is arguably correct behavior, not a fault.
- **Verdict: this is already the right shape** — plan-side id, tie-only, bounded, and the escape hatch (correction exclusion) is explicit. It needs no change and no text-level feedback.

### A3. Long-answer self-consistency (future, not present)
- **Fault (hypothetical):** a future dialogue that composes multi-sentence answers could emit sentence 2 contradicting sentence 1 (e.g., "X was born in 1819" then "X was born in 1775").
- **Would re-reading own output help?** A checker that reads the composed response and compares it against the KB could *detect* this. But the detection is **plan-derived** (response vs KB), not output-authoritative: the response is the suspect, the KB is the judge. And the correction must be plan-pure re-emission — the output has no authority to resolve which sentence is right; only the plan does.
- **Critical distinction:** this is *deliberation*, a different layer (see below). The check operates on the plan (KB + committed assertions), and the composed text is merely the artifact under test. Giving the *text* authority — "I said 1819 first, so 1819 wins" — is exactly the corruption case (see B2).

## B. Faults where output feedback would CORRUPT — the dangerous cases

### B1. Constructed-mode leakage into the belief store (the load-bearing hazard)
- **Setup:** Micah's constructed-mode principle (standing law): free elaboration happens in an explicitly marked constructed mode, held in partitions, **never committed to the belief store without verification**. H7 (utterance-type learning) makes this concrete: jokes, hypotheticals, sarcasm are learned as *labeled utterance types*, never hardcoded — and never believed.
- **Fault:** any mechanism that feeds emitted (or constructed) text back into retrieval keys, salience, the user-claim store, or the KB. Concrete scenario: TNN answers a hypothetical ("imagine the Eiffel Tower were built in 2000…") — the emitted sentence contains "eiffel tower … built … 2000". If response text feeds the keyword index or `uc`-like memory, a later "when was the eiffel tower built?" retrieval now has a 2000-claim in its candidate set. The fiction outscores or ties the fact. **A wrong belief is now load-bearing in the plan.**
- **Why this is worse than audio:** audio's exception path measures a waveform — epistemically neutral signal; a false positive is a no-op re-render (HYBRID_SPEC §2). Dialogue's output is *propositional content*. A false positive in a dialogue feedback loop doesn't re-render silence — it **installs a falsehood into the plan that all future turns reason from**. Epistemic faults compound across every future turn; a corrupted waveform corrupts one block.
- **Current architecture already defends this correctly:** KB is write-once at install (`kb_install`, :892); user assertions go to `uc` labeled by (subject, relation, value, turn) and are *never promoted to KB*; `novelty_ok` is measurement-only and writes nothing. The constructed→belief boundary is currently enforced by construction. Any feedback authority would have to re-justify punching through it.
- **Verdict: feedback here is not a bounded risk, it is a category violation.** The audio "bounded, revocable" framing does not transfer: you cannot "revoke" a belief the system has already reasoned from for 40 turns.

### B2. Repeat-bias and the CORRECTION contract (45/45 in VERDICT.md)
- **Contract:** on correction, the system must *revise, never repeat*. The mechanism (`:1544–1614`) excludes the previous answer fid and its primary entity from retrieval.
- **Fault if output had authority:** a feedback loop that reads its own prior output as evidence ("I said X last turn, X is probably right") directly fights the exclusion. The WE-09-adjacent "correction salience pollution" bug (VERDICT.md, bug 2 — the no-entity continuation appended the salience head and polluted "tell me about the tower" with "herman melville") is the native demonstration: *input-side* memory already polluted queries once; output-side memory would do it worse, because the system's own confident phrasing would score highly against itself.
- **Verdict: the existing contract is anti-feedback by design.** Output authority would break a 45/45 trial result.

### B3. Contradiction laundering
- **Setup:** the CONTRADICT trial (72/72) works because user claims live in `uc` with turn labels, and the system reports "CONTRADICTION: turn N said X" — it surfaces the conflict, it does not resolve it by fiat.
- **Fault if output had authority:** a self-consistency repair loop that "fixes" contradictions by editing its own prior outputs (or the claim store) to agree with the latest utterance would *launder* the contradiction instead of reporting it. The user asserted X at turn 3 and not-X at turn 9; a feedback loop that rewrites history to not-X makes the system agreeable and the audit trail a lie. The current design's refusal to touch `uc` history is the integrity feature.
- **Verdict: the absence of a repair loop is load-bearing for the 72/72 result.**

### B4. Salience pollution via self-quoting
- **Mechanism:** `sal`/`build_resolved` resolve anaphora ("it", "the tower") from mentioned entities. If emitted text fed salience, the system's own phrasing choices ("the big metal tower") would inject entities the user never mentioned, and follow-up resolution would drift toward the system's vocabulary rather than the user's. The current code pushes only *gazetteer-scanned* entity ids from utterances and fact entity lists — both plan-side.
- **Verdict: keep output out of salience.**

## C. Self-consistency: feedback authority, or deliberation?

The task asks explicitly: does re-reading own output to fix contradictions count as feedback authority, or is that deliberation, a different layer?

**It is deliberation, a different layer — and the distinction is structural, not terminological.**

- **Feedback authority (audio sense):** output bytes are *measured* and the measurement *steers* generation parameters (gain, pitch). The output is a sensor reading about the world.
- **Deliberation (dialogue sense):** a proposed response is *checked* against the plan (KB facts, prior committed claims) before emission. The output is the *defendant*, never the *witness*. The authority stays 100% with the plan; the checker's only power is to veto-and-recompose plan-pure.
- The native code already draws this line: `novelty_ok` (:1500) *measures* the response (novelty flag) but has zero generation authority — it cannot change a byte. `uclaim_check` (:1189) checks *user* claims against *user* history. Neither lets emitted text steer anything.
- If a future deliberation layer pre-emission-checks composed responses for KB-contradiction, that is legitimate **iff** the correction map is constant in the checked text (veto → re-compose from KB, never "edit toward consistency with what I already said"). The moment the text's own content influences the resolution, it has become feedback authority — and B1–B3 apply.

## D. Summary table

| Fault class | Output measurement possible? | Correction shape | Give output authority? |
|---|---|---|---|
| A1 assembly corruption | yes (beq assert) | constant map (re-assemble) | No — assert at build time; no loop needed |
| A2 last_fid tie-break | n/a (plan-side id) | tie-only preference | Already correct; keep bounded as-is |
| A3 long-answer self-contradiction | yes (vs KB) | veto + plan-pure recompose | Only as deliberation-layer veto; text never the judge |
| B1 constructed→belief leak | — | — | **Never.** Category violation; compounds across turns |
| B2 repeat-bias vs CORRECTION | — | — | **Never.** Breaks 45/45 revise-not-repeat |
| B3 contradiction laundering | — | — | **Never.** Breaks 72/72 surface-don't-resolve |
| B4 salience self-pollution | — | — | **Never.** Drifts anaphora to system vocabulary |
