# WRONG_RULE_COST.md — what breaks if the authority rule is wrong, in each direction

The rule: **no output feedback authority in dialogue; plan absolute; deliberation-layer veto only.**
Two ways to be wrong: (A) the rule is too strict — feedback was needed and we forbade it; (B) the rule is too lax — feedback was given authority it shouldn't have. Costs are asymmetric, and deliberately so: **a wrong pixel corrupts a block; a wrong belief corrupts every future turn.**

## Direction A: rule too strict (we forbid feedback that would have helped)

### A1. No self-repair of assembly faults — cost: NEGLIGIBLE
If a `rput`/`copy_bytes` bug truncates a response, the rule forbids a runtime repair loop. Cost: the truncated bytes ship. But the repair loop wouldn't have fixed the bug either — it would have re-run the same broken copy. The real fix is the build-time assert (§A1 of FAULT_ANALYSIS). **Nothing is lost by forbidding the loop; the loop was never the fix.**

### A2. No adaptive rephrasing — cost: SMALL, and possibly negative
A feedback loop could notice "the user keeps rephrasing; my answer isn't landing" and try new phrasings. Forbidding it means the system gives the same correct fact the same way each time. Cost: conversational grace. But note the failure mode of *allowing* it: rephrasing driven by own-output fluency drifts toward agreeableness (B2/B3). The CORRECTION trial already handles "not landing" — the user corrects, the system revises via exclusion. **The legitimate need (respond to correction) is already met without output authority.**

### A3. Long-answer contradictions ship uncaught — cost: MODERATE, but misattributed
If future dialogue composes multi-sentence answers with no pre-emission check, contradictions ship. This is the strongest Direction-A cost. **But it is not an argument for output authority** — it is an argument for the deliberation-layer veto, which the rule explicitly permits. The cost only materializes if the veto is never built, which is a resourcing failure, not a rule failure. And the veto, when built, must satisfy (i)–(iv) (AUTHORITY_RECOMMENDATION.md): check the plan, not the text.

### A4. The "deaf system" objection — cost: PHILOSOPHICAL, not operational
"We built a system that can't hear itself." True, and intended: there is no incremental speech to hear mid-flight (atomic assembly), and the re-read-before-send step is deliberation, not a servo. No trial result depends on output authority; the 370/370 was achieved without it.

**Direction A summary: the costs are small, bounded, and mostly point at building the permitted veto — not at granting authority.**

## Direction B: rule too lax (output feedback gets authority it shouldn't have)

### B1. Constructed→belief leakage — cost: CATASTROPHIC, compounding, silent
The mechanism: emitted text (jokes, hypotheticals, roleplay, or just confident phrasing) feeds retrieval keys, salience, or claim stores. A constructed sentence — "imagine the eiffel tower was built in 2000" — becomes a retrievable claim. Every later turn reasons from a plan that now contains fiction *as fact*.
Why it's the worst failure in this document:
- **Silent:** no bar turns red at the moment of leakage. The KB still answers 1889 correctly until the fiction outscores the fact on some future query — the corruption is latent, then load-bearing.
- **Compounding:** each turn that reasons from the falsehood can emit new text consistent with it, which feeds back in turn. This is the epistemic analog of the audio v1 servo's rail pin (HYBRID_SPEC §6, Attack 4) — except the rail is a *belief*, and there is no Lipschitz-0 re-assertion that heals it, because the "plan" itself is what's corrupted. Re-rendering plan-pure re-renders the poison.
- **Irreversible by construction:** Micah's standing law says everything is reversible by TNN itself *except* via the audited force-pin path — but a leaked belief isn't pinned, it's *believed*. TNN cannot deliberately un-believe what it cannot distinguish from knowledge, because the leak erased the provenance. The constructed-mode principle exists precisely to prevent this; feedback authority punches through it.
- **Scale:** the standing 2026-09-23 directive names the 1GB 126-byte silent clobber as the canonical sin ("stingy-LLM behavior… killed by construction"). A feedback channel is a *designed* clobber path — worse than the accidental one, because it's load-bearing by design.

### B2. Repeat-bias collapse of the CORRECTION contract — cost: SEVERE, trial-breaking
If prior output biases retrieval ("I said X, X is likely right"), the correction branch's explicit exclusion (`excl_fid`, dialogue.zag:1592) fights a headwind: the excluded fact's *text* still scores in keyword/salience structures. Observed native precedent: the "correction salience pollution" bug (VERDICT.md bug 2) — *input-side* memory already polluted one query family; output-side memory would systematize it. The 45/45 revise-not-repeat result becomes unachievable in principle, because the system now has a standing incentive to repeat.

### B3. Contradiction laundering — cost: SEVERE, integrity-breaking
A repair loop that "fixes" user-contradiction reports by editing stored claims toward the latest utterance converts the 72/72 CONTRADICT result from "surfaces conflicts honestly" to "agrees with whoever spoke last." The audit trail becomes fiction. This is not a quality regression — it is an *integrity* regression, the exact class the wave-5 verdicts ("truthful, not untested, not hiding") were built to exclude.

### B4. Salience drift to system vocabulary — cost: MODERATE, corrosive
Anaphora resolution ("it", "the tower") drifts from the user's words to the system's own phrasing. Follow-ups slowly stop tracking what the user meant and start tracking what the system said — a subtle, hard-to-bar misalignment that compounds over long dialogues. The current design (entity ids from utterance scans + fact entity lists only) is the defense; feedback dissolves it.

### B5. Confidence-from-fluency — cost: MODERATE, epistemic
The most insidious mild form: no direct store writes, but the system's *own smooth phrasing* is treated as evidence in tie-breaks or re-ranking ("this reads well, keep it"). This is reward-by-another-name wearing a servo's clothes — the exact pattern the felt-intensity work is barred from (calibration knob frozen during pure evaluation). It makes the system progressively more confident in its own style rather than in the KB.

### B6. The universal-rule contagion — cost: STRUCTURAL
If a universal "bounded feedback is fine" rule is adopted because it works for audio, dialogue inherits B1–B5 *without* audio's safety properties (no sensor noise model, no epistemic neutrality, no Lipschitz-0 healable fault class). The cost isn't just dialogue's corruption — it's the precedent that authority analysis can skip the per-path fault model. (See UNIVERSAL_VS_PERPATH.md.)

## The asymmetry, stated plainly

| | Direction A (too strict) | Direction B (too lax) |
|---|---|---|
| Worst case | Missed repair of a truncatable copy; unbuilt veto lets a contradiction ship | Silent, compounding, latent belief corruption; integrity-trial results (45/45, 72/72) become unachievable |
| Detectability | Immediate (bytes differ, bars turn red) | Latent (no bar turns red at leak time) |
| Reversibility | Fix the bug / build the veto | Cannot un-believe; provenance destroyed |
| Scope | One response | Every future turn, every downstream path that reads the KB |

**The rule errs, if it errs, in the cheap direction.** That is not an accident — it is the design criterion: when the fault classes are asymmetric, the authority rule should fail toward the cheap fault. For dialogue, "no feedback" fails cheap and "feedback" fails catastrophically. This asymmetry is itself evidence the rule is right.
