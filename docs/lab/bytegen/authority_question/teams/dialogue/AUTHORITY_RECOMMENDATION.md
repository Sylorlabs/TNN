# AUTHORITY_RECOMMENDATION.md — recommended authority rule for dialogue

## Recommended rule

> **No output feedback authority in dialogue. The plan is absolute. The only legitimate output-side mechanism is a deliberation-layer veto whose correction is plan-pure re-composition — and the checked text is the defendant, never the witness.**
>
> Concretely:
> 1. No emitted byte may ever enter a retrieval key, a salience/topic structure, the user-claim store, the KB, or any tie-break, weight, or score used by generation. (The existing `last_fid` exact-tie preference is grandfathered: it is a plan-side integer id, tie-only, and the correction branch's explicit exclusion of the previous answer is retained.)
> 2. KB remains write-once at install. User assertions remain in the turn-labeled claim store, never promoted without a deliberate, audited act.
> 3. Any future pre-emission self-consistency check may *veto* a composed response and force plan-pure re-composition. It may not edit, smooth, or arbitrate using the response's own content. Its correction map must be constant in the checked text.
> 4. `novelty_ok`-style post-hoc measurements stay measurement-only: flags, never steering.

## The steelman for the opposition (feedback SHOULD have bounded authority in dialogue)

The strongest honest case for giving output feedback *some* authority:

1. **The audio precedent is real.** The hybrid v2 spec proved that a bounded exception path (detect fault → re-render plan-pure) heals real corruption with zero authority creep, because the correction map is constant (Lipschitz 0). Dialogue could have the analogous path: detect a corrupted/contradictory composed response, re-compose plan-pure. If it works for waveforms, the *shape* should transfer.
2. **Long answers will need self-monitoring.** Today's dialogue emits one fact or one template sentence; it scores 370/370 partly because the task is small. A future TNN that holds real conversations will compose multi-sentence answers, and *some* mechanism must catch "sentence 2 contradicts sentence 1" before the user sees it. Reading the composed response is the natural sensor for that. Refusing all output-side checks on principle risks shipping contradictions the plan "knew" were wrong.
3. **Continuity is already feedback-shaped.** The `last_fid` tie-break and the salience stack are prior-turn memory steering current generation, and the trials *pass because of them* (follow-ups, ellipsis, anaphora: 45/45, 60/60). A purist "no memory of prior output" rule would break the dialogue's best results. If some prior-output influence is already legitimate, the line is quantitative (how much), not categorical (none).
4. **Humans self-monitor.** People hear themselves talk and mid-course-correct. A system that cannot hear itself at all is missing a capability the target (human-like dialogue) observably uses.

## Why the steelman fails (rebuttal)

1. **The audio shape transfers, but the audio *authority* doesn't — because the audio sensor measures signal, not propositions.** The exception path's safety proof (HYBRID_SPEC §2) rests on the output being epistemically neutral: a waveform carries no beliefs, so a false positive is a no-op. Dialogue's output is propositional: "the eiffel tower was built in 2000" is a *claim*. The safety proof does not survive the transfer — a false positive in a dialogue loop doesn't re-render silence, it installs or reinforces a claim. The shape (detect → plan-pure re-compose) is worth keeping; the *authority* (output steering anything) is not.
2. **Self-monitoring of long answers is deliberation, and deliberation already has a legitimate form that needs no output authority.** The checker compares the *proposed response against the plan* (KB + committed claims). The response is the artifact under test. This is exactly the current `novelty_ok` architecture (measurement without steering) plus a veto. Nothing in "catch sentence-2-contradicts-sentence-1" requires sentence 1's *text* to have authority — it requires sentence 1's *plan content* (the fact ids it was composed from) to be in the checker's input. Check the plan, not the text. The text is a lossy projection of the plan; checking the projection instead of the source is strictly worse engineering.
3. **The existing memory is input-side, not output-side — the line IS categorical.** `last_fid` is a fact id (plan content), not emitted text. The salience stack holds entity ids scanned from *utterances* and *fact entity lists* (plan content). `uc` holds *user* claims. None of them is the system's generated text feeding back. The trials pass because the system remembers the *conversation*, not because it reads its own *output*. Conflating "memory of what was said" with "output feedback authority" is the exact category error the opposition needs; the native code keeps them separate, and the rule should too.
4. **Humans self-monitor *speech*, but TNN's dialogue has no speech act to monitor mid-flight.** There is no incremental word loop to correct — the response is atomic. The human analogy that actually fits is not "hearing yourself talk" but "re-reading the email before sending": a deliberate, plan-side review step (deliberation layer), not a servo. And when humans re-read, the authority stays with what they *meant* (the plan), not with the draft's typos.

## The deliberation-layer carve-out, stated precisely

Self-consistency work is legitimate in dialogue **iff all four hold**:

- (i) The checker reads the *plan* (KB facts, committed claim ids, discourse state) as ground truth and the composed text only as the artifact under test.
- (ii) The checker's only power is **veto → plan-pure re-composition**. It may not edit text, blend, or "resolve" using the text's content.
- (iii) The correction map is constant in the checked text (the dialogue analog of Lipschitz 0): same plan fault → same re-composition, regardless of how the text happened to phrase it.
- (iv) Constructed-mode text (jokes, hypotheticals, roleplay — per H7 utterance-type labels) is **never eligible** as checker input against the belief store, and never written to any store the checker reads. The constructed→belief boundary is air-gapped from the veto path.

Under (i)–(iv), the "feedback" is not feedback at all in the authority sense: the output earns nothing. That is the point.

## What this rules out, explicitly

- Any "read my last answer to decide this answer" mechanism beyond the existing integer-id tie-break.
- Any repair loop that edits a response toward consistency *with itself* (B3 contradiction laundering).
- Any learning-from-own-output: emitted text entering vocab weights, keyword scores, salience, or claim stores (B1, B4).
- Any "confidence from fluency": the system must never treat its own smooth phrasing as evidence (the B2 repeat-bias family).

## Bottom line for Micah

Dialogue is the path where the authority question is *easiest*, because the answer is structural: there is no sensor, no noise, and no plan-independent fault class — and the output is the one thing in the whole lab that can poison the belief store. **Plan absolute, no feedback authority, deliberation-layer veto only.** The audio rules stay on the audio path (see UNIVERSAL_VS_PERPATH.md).
