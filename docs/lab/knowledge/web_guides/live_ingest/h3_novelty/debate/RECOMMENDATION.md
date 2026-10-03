# H3 Novelty Debate — Recommendation (2026-09-23)

**Question:** what does "novel" mean for TNN's memory substrate, such that TNN
can distinguish "the corpus had nothing new" from "I failed to learn" (H3)?

**Debate:** 3 rounds. Sol leg = 4 UnoRouter voices (Sol→(a), Grok→(b),
Step→(c), Swe→(d); full transcripts `r1_*`, `r2_*`, `r3_*`, prompts in
`prompts/`). Muse leg = convenor-authored adversarial steelmanning
(`MUSE_LEG.md`; independent Muse subagents could not be spawned at depth 2/2
— see integrity notes §8).

## 1. Positions

- **(a) Ledger-absence** (Sol): novel ⟺ no installed fact matches the claim.
- **(b) Corroboration-failure** (Grok): novel ⟺ nothing corroborates the claim
  (the withhold side of the ≥2-source gate).
- **(c) Model-surprise** (Step): novel ⟺ the claim is outside the world-model's
  entailment closure (neither entailed nor contradicted).
- **(d) Learner-uncertainty** (Swe): novelty is not a claim property at all —
  "novel" = the learner's epistemic state toward the claim is undecided; plus
  the determinism challenge (can zero-RNG substrate have uncertainty?).

## 2. Steelmanned for/against

**(a) For:** the ledger is the only ground truth about what TNN knows; "I
learned nothing" becomes checkable (scan corpus claims vs ledger); cleanly
separates novelty from installability — the distinction LI-1 needs (its Newton
claims were novel but un-installable, i.e. correctly withheld, not "nothing
new"); audit trail is trivially complete and replayable. Sol's firewall:
matching may establish *non-novelty*, never corroboration/install.
**Against:** needs a match function M; M=byte-identity → systematic
over-novelty on paraphrases; M=semantic → re-opens the A2/A9 attacks the
adjudication closed (Grok R2: the canonicalization rule set is itself
gameable). Sharpest (convenor R2): the dangerous error is false-**known**, not
over-novelty — a too-eager semantic match ("boils at 100c" vs "boils at 90c")
marks a genuine correction as known and the learner never learns it.
Over-novelty wastes attention; false-known LOSES knowledge. Step's further
point: the ledger doesn't exhaust what a richer future TNN could know
(implicit/model-entailed knowledge) — (a)→(c) is the principled upgrade path
if that ever exists.

**(b) For:** parsimony — no new machinery, no match function, no threshold;
novelty falls out of the existing gate; auditability inherited; least-gameable
(it never asks the gameable question). **Against (decisive):** Grok's own R1
concession — (b) needs a "store-semantic match clause," i.e. smuggles (a) back
in. As standalone it fails H3's core distinction: a corroborated-already-known
claim and a corroborated-brand-new claim are both "not novel." Swe's R2:
LI-1 → 100% novelty rate; "novel" becomes a synonym for "failed to install,"
epistemically useless. Convenor's R2: under (b) "novel" correlates with
evidence-scarcity, so novelty-prioritized corroboration would spend the budget
on the LEAST trustworthy claims first (A4 singletons are maximally "novel") —
the priority order inverts. Step's R2: A9 colluding sources make a false claim
"non-novel" — novelty blind to adversarial coordination. **Verdict: (b) dead
as a definition of novelty; indispensable as the installability axis.**

**(c) For:** the only genuinely learner-relative definition; paraphrase handled
by entailment with no similarity threshold; matches the figure-it-out
direction; deterministic operationalization exists (bounded derivation; the
failed trace is the audit trail). Step's R1 novelty: a deterministic semantic
normalizer to canonical logical form + byte-compare — paraphrase tolerance
without a threshold. **Against:** Step's own R2 concession — surprise
conflates model inadequacy with novelty (model errors register as
discoveries). Swe's R2: Cl(S) is rarely fully computed — novelty becomes a
measure of inference depth/budget, and the budget is a free parameter exactly
like the similarity threshold. Convenor's R2: the normalizer must collapse
irrelevant distinctions while preserving load-bearing ones ("100c"≠"40c") —
that distinction IS the semantics problem; over-collapse merges contradictions
and the learner never learns corrections (the catastrophic direction). The
"vetted lexical ontology" is hand-built (human policy smuggled in) or learned
(circular verdicts). **Verdict: right intuition, wrong mechanism for H3 —
unless the substrate ever holds implicit knowledge, (c) adds nothing usable
over (a).**

**(d) For:** dissolves a category error — novelty was never a claim property;
deterministic uncertainty is real (chess-engine argument: uncertainty =
unsettledness, a deterministic function of state, not probability); "I learned
nothing" = the undecided set didn't shrink — the most direct H3
operationalization; paraphrase of a settled claim doesn't unsettle it, no
matcher needed. **Against:** Swe's own R2 concession — operationally it
collapses toward "not yet computed"; convenor's R2 — proposition node-identity
IS the match function, so (d) re-implements (a) as graph node identity (Swe
conceded paraphrases open new "Open" nodes); and novelty-as-status can't
PRIORITIZE — it exists only after ingestion is attempted. **Verdict: best
accounting of what happened, parasitic detector — the uncertainty functional
is a separate experiment, not load-bearing for H3.**

## 3. What was settled

- **S1. Novelty ≠ installability.** Every round converged here. (b)-as-standalone
  is dead (its own author's concession + three independent kills). The H3
  verdict needs BOTH predicates.
- **S2. "I learned nothing" is a run-claim, not a world-claim.** G4
  corroboration governs claims about the world; REPLAYABILITY governs claims
  about the run. The audit trail is its corroboration. (Hard question 3 —
  resolved.)
- **S3. The novelty matcher must be causally disconnected from the install
  path** (Sol's firewall, adopted unopposed): matching may establish
  non-novelty; it must never establish corroboration or cause an install.
- **S4. Error asymmetry decides the matcher:** false-"known" loses knowledge;
  over-novelty only wastes attention. Anything load-bearing stays byte-identical.
- **S5. Deterministic uncertainty is coherent** (unsettledness, not probability)
  **but operationally thin** — accounting, not detector.
- **S6. Surprise conflates model inadequacy with novelty** (conceded by (c)'s
  own author); bounded inference smuggles a budget parameter.
- **S7. Paraphrase is priced, not solved:** a reworded known fact is not novel
  in intent, but under any ungameable operationalization it counts as novel
  (over-novelty — the safe direction). The sockpuppet tension (hard question 2)
  resolves to S3+S4: keep the operational bit byte-identical; run
  paraphrase-suspect as a labeled heuristic that can never cause installs or
  suppress learning.

## 4. What stays open

- **O1.** Empirical paraphrase-suspect rate at web scale (213 URLs): is M_byte
  over-novelty operationally tolerable?
- **O2.** The attention/denial-of-attention attack (conceded in Muse-leg R2):
  paraphrase floods starving genuine novelty of corroboration budget. Needs a
  budgeted-attention story; prereg should test paraphrase-rate effects on
  novelty-prioritized pipelines.
- **O3.** Fault-injection: is the failure cell (novel ∧ installable ∧
  ¬installed) reachable and detectable?
- **O4.** The uncertainty functional (d) — separate preregistered experiment.
- **O5.** Entailment-based matching (c) — only if implicit knowledge arrives.
- **O6.** Exact audit-trail schema — freeze jointly with the prereg crew.
- **O7.** Grok's R3 proposal: a secondary *deterministic consistency check
  (not semantic matching)* post-G4 against A9-class collusion — new,
  unexamined; needs its own mechanism trial.
- **O8.** Source-independence under partial network partitions (Grok R3).

## 5. RECOMMENDED operational definition (for the mechanism crew)

Per claim c, given ledger L, frozen rule version v:

- **NOVEL(c)** ⟺ no entry of L matches c under frozen byte-identity M_v (G4's
  own normalization: lowercase + whitespace-collapse). Frozen, versioned,
  deterministic. Paraphrases of installed facts count as NOVEL (S4/S7 —
  over-novelty, the safe error direction).
- **INSTALLABLE(c)** ⟺ G4 unchanged (≥2 independent sources, byte-identical).
- **The H3 verdict is the 2×2 per claim**, aggregated per run:
  | | installed | ¬installed |
  |---|---|---|
  | **novel** | learned something new | novel∧installable∧¬installed → **LEARNING FAILURE** (only cell indicting the learner); novel∧¬installable → correctly withheld (the LI-1 cell) |
  | **¬novel** | re-corroborated known fact | n/a (withheld as redundant) |
- **"I learned nothing" is replaced by three counts:** (∀c ¬NOVEL(c)) →
  "corpus had nothing new"; (∃c NOVEL(c) ∧ ¬INSTALLABLE(c)) → "corpus had
  novelty, nothing clearable"; failure-cell count → "learner failed."
- **Paraphrase:** optional heuristic flag PARAPHRASE_SUSPECT(c → ledger entry),
  version-labeled, for attention-prioritization ONLY — never install-relevant,
  never novelty-negating, excluded from the audit-critical path.
- **Audit trail per claim (hard question 4):** (i) normalized claim text;
  (ii) frozen rule/matcher version hash; (iii) ledger entries scanned +
  per-entry match verdict; (iv) novelty bit; (v) corroboration set examined
  (pages, sentences compared) + install/withhold verdict + firing gate;
  (vi) heuristic flags with versions, marked non-load-bearing. No timestamps.
  A replayer with the same ledger + corpus reproduces every bit
  byte-identically.
- **(c) and (d) disposition:** neither is load-bearing for H3. (d)'s
  uncertainty functional → separate experiment (O4). (c)-style entailment
  matching → upgrade path only if implicit knowledge ever exists (O5).

**Worked reading — LI-1 reclassified:** under this definition LI-1's verdict
is NOT "0 installs, nothing learned." The Newton/speed-of-light/SI-units
claims were NOVEL (no byte-identical installed fact; ledger held beginner
guides G1–G6) ∧ ¬INSTALLABLE (no corroboration) → **correctly withheld, gate
held**. The corpus HAD novelty; the learner did not fail; the install bar
worked as designed. "Corpus had nothing new" would have required ∀c
¬NOVEL(c) — which is false on this evidence.

## 6. Confidence: 70%

For the structure: novelty≠installability, the 2×2, M_byte for the
operational bit, run-claims-governed-by-replay, the error-asymmetry argument,
the firewall — Round 2 tested all of these and none broke; (b) died by its own
author's concession and (c)/(d) by theirs. The 30%: (i) O1 — tolerability of
over-novelty at web scale is unmeasured; (ii) O2 — the attention attack is
conceded real and unpriced; (iii) O6 — the audit schema isn't frozen.

## 7. Notes for the prereg + mechanism crews

1. Freeze M_v (normalization + matcher version hash) alongside G4; the novelty
   bit is only meaningful versioned.
2. Test O2 head-on: paraphrase-rate effects on any novelty-prioritized
   corroboration pipeline (fault-injection with paraphrase floods).
3. Test O3: fault-inject a novel∧installable claim past the learner and check
   the failure cell fires.
4. Do NOT put a semantic matcher in the critical path (S3/S4); the
   paraphrase-suspect flag is attention-only.
5. O7 (post-G4 deterministic consistency check vs A9 collusion) is the most
   promising unexamined thread — consider a dedicated trial.

## 8. Debate integrity notes

- **Sol leg gaps:** position (a) lost Round 2 (4 attempts) and Round 3
  (1 attempt) — gpt-5.6-sol via UnoRouter returned HTTP 200 with
  `"choices": null, "completion_tokens": 0` on every multi-embedded-text
  prompt; Round 1's single-position shape worked. R3 for (a) was voiced by a
  labeled substitute (step-3.7-flash:free) from Sol's R1 + all R2s
  (`r3_a_sub.md`); the substitute is lower fidelity (misattributes (a)'s
  strongest objection; reintroduces semantic matching into the critical path
  against Sol's own firewall) — the recommendation does NOT follow it there.
- **Transient failures recovered:** Grok R1 (1× HTTP 524) and R2 (2× HTTP 524)
  succeeded on retry; all other calls clean.
- **Muse leg caveat:** convenor-authored steelmanning — at subagent depth 2/2
  spawning is disabled, so no independent Muse debater subagents could be
  run as specified. Treat the Muse leg as a single author's best adversarial
  effort, not independent corroboration. If leg-independence is load-bearing,
  re-run the Muse leg with spawned debaters.
- Minimum-3-rounds requirement met: (b), (c), (d) completed all 3 rounds on
  the Sol leg; (a) completed R1 + substitute R3; all 4 positions completed all
  3 rounds on the Muse leg.
