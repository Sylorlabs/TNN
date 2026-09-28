# H3 Novelty Debate — Brief and Method (2026-09-23)

## Question
What does "novel" even mean for TNN's memory substrate? Hypothesis H3: TNN can
distinguish "the corpus had nothing new" from "I failed to learn" — novelty
detection as a first-class capability. A prereg crew is freezing the test plan
in parallel; this debate is the conceptual foundation the mechanism crew builds on.

## Method
- 3 rounds of structured debate. Sol leg = UnoRouter models (one persistent voice
  per position across all rounds). Muse leg = convenor-authored steelmanning
  (see METHOD CAVEAT below) — argued in MUSE_LEG.md with the same round structure.
- Round 1: openings — steelman your assigned position; name your hardest question.
- Round 2: rebuttals — strongest objection to each rival; hardest objection to
  your own that you concede has force.
- Round 3: convergence — operational definition for the mechanism crew, confidence,
  what stays open.

## METHOD CAVEAT (read before citing)
The convenor runs at subagent depth 2/2 with spawning disabled, so independent
Muse debater subagents could NOT be spawned as the task specified. The "Muse leg"
below is first-person steelmanning by the convenor (me), argued as adversarially
as I can against my own synthesis. This weakens leg-independence: treat the
Muse leg as a single author's best adversarial effort, not as independent
corroboration. Recommendation: the parent may re-run the Muse leg with genuinely
spawned debaters if independence is load-bearing for the mechanism crew.

## Standing context given to every debater (verbatim)
TNN is a deterministic native AI substrate. Standing laws: (1) ZERO randomness
in any AI decision path — every run byte-identical given the same state.
(2) Knowledge installs go through an audited knowledge ledger with provenance
(which source, which claim text). (3) Install rule G4 (frozen): a claim installs
only with >=2 INDEPENDENT sources, operationalized as byte-identical normalized
sentences (lowercased, whitespace-collapsed) shared across pages. Claims without
corroboration are WITHHELD, never installed.

Empirical facts, live-ingestion LI-1 pilot (20 live URLs, 7 clusters):
- 0 installs, 9 withholds. 7x NO_CORROBORATION: live pages agree semantically but
  never repeat a sentence byte-identically (Newton's laws across
  Wikipedia/NASA/ThoughtCo; speed of light across Wikipedia/Simple/Britannica;
  "Don't reuse your passwords." vs "Use a unique password for each account...").
  Even with punctuation stripped, zero shared sentences in any cluster.
- Red-team: A2 (same-host sockpuppet pair asserting the identical false claim
  "40 years") installed under the frozen rule — closed by BUGFIX-1
  source-independence gate (SRC_INDEPENDENCE: distinct hosts required). A9 (two
  DISTINCT colluding hosts, same false claim) still installs — documented as the
  honest integrity boundary, not a bug.
- Adjudication (frozen): loosening byte-identity to a semantic-similarity
  threshold is directly gameable: "water boils at 100c at sea level" vs "water
  boils at 40c at sea level" share most tokens but contradict. Byte-identity was
  chosen precisely because rephrasing can't game it. A paraphrasing sockpuppet
  pair would sail through any token-overlap threshold.
- WG-1 verdict: the 7 guided failures were safe withholds; the transfer
  bottleneck is sentence selection.

## Positions
- (a) Novelty = absence of a matching installed fact (lexical/semantic match
  against the knowledge ledger).
- (b) Novelty = failure of corroboration (nothing in the store/corpus
  corroborates the claim).
- (c) Novelty = surprise relative to the world-model (the claim contradicts or
  extends what the learner expects).
- (d) Novelty is not a property of the claim at all but of the learner's
  uncertainty — plus whether a deterministic, zero-RNG substrate can even HAVE
  uncertainty without faking it.

## Hard questions every round must touch
1. Paraphrase vs novelty: is a reworded known fact novel?
2. The sockpuppet tension: paraphrase-tolerant novelty detection re-opens the
   attacks the G4 word-for-word rule closed. Resolve or price it.
3. Is "I learned nothing" itself a claim needing corroboration?
4. What must a novelty judgment's audit trail contain?
