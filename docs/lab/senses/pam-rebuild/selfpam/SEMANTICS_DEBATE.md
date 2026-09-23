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
succeeded on Sol; the xexam prompt is preserved in the run notes below).*

**Strongest attack on each position, plus its best rebuttal:**

- **(a) GROUNDING** — Attack: self-generated "warrants/citations/escrow" are
  theater; the model can fabricate provenance as easily as claims, so
  entitlement-to-assert collaps
...[truncated 9426 chars]