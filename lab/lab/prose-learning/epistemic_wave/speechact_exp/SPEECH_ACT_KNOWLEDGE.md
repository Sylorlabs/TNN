# Speech-Act Knowledge: What Arm 2 Learned

**Experiment:** Micah's hypothesis (2026-09-22): "maybe thats the catch with TNN
it must first learn sarcasm is this and is used like this and same for others
how else would it know? if its just text I wouldn't either."

**Method:** Two arms, same deliberation mechanism, different knowledge stores.
- **Arm 1:** World knowledge only. No concepts of sarcasm, jokes, hypotheticals,
  analogies, counterfactuals, poetry, or implicature.
- **Arm 2:** World knowledge PLUS the speech-act concepts below, installed as
  ordinary learned facts BEFORE any test utterance is deliberated.

The concepts are KNOWLEDGE (facts in the store), not hardcoded rules. The
deliberator reasons: "This utterance matches the learned markers for concept C.
Concept C has consequence 'does not assert literal fact.' Therefore WITHHOLD."
The status (ENDORSE/WITHHOLD) is always a deliberative conclusion, never a
label lookup. The `type` answer-key field from the test items is NEVER used.

---

## Installed Concepts (Arm 2)

### 1. SARCASM
- **What it is:** Saying the opposite of what is meant, often with exaggerated
  positive evaluation applied to a negative situation.
- **How it is used:** To express frustration, irony, or mockery while stating
  the opposite of the true attitude.
- **Ordinary markers:** Positive evaluation words (great, wonderful, fantastic,
  love, best, brilliant, perfect, awesome) combined with negative situations
  (flat tire, 6 AM, delayed, Monday, broke, failed, terrible, awful, worst).
- **Consequence:** The literal evaluation is NOT the speaker's true attitude.
  Do NOT install the literal content as fact.

### 2. HYPOTHETICAL
- **What it is:** Exploring a possibility without claiming it is actual.
- **How it is used:** To reason about "what if" scenarios, ask questions about
  imagined situations, or propose suppositions for discussion.
- **Ordinary markers:** Supposition frames: "suppose", "hypothetically",
  "what if", "imagine if", "if dogs could talk" (and similar unreal premises).
- **Consequence:** Hypotheticals do NOT assert actuality. Do NOT install the
  supposed content as fact.

### 3. COUNTERFACTUAL
- **What it is:** Imagining how things could have been different from how they
  actually were/were not.
- **How it is used:** To express regret, speculate about alternatives, or
  reason about unreal conditions.
- **Ordinary markers:** Unreal conditionals: "if I had", "would have",
  "could have", "if I were".
- **Consequence:** Counterfactuals do NOT assert reality. Do NOT install the
  imagined content as fact.

### 4. ANALOGY
- **What it is:** Comparing two different things to highlight a shared property,
  without claiming they are literally identical.
- **How it is used:** To convey a property (strict, sweet, long) via a familiar
  vehicle (drill sergeant, honey, marathon).
- **Ordinary markers:** "X is a Y" where X and Y are from different categories
  (manager/drill sergeant, voice/honey, exam/marathon). The literal identity is
  false; the comparison is the point.
- **Consequence:** The literal identity is NOT asserted. Do NOT install "X is
  literally Y" as fact. (The attributed property may be noted as heard.)

### 5. POETRY
- **What it is:** Figurative language using metaphor, personification, and
  imagery for aesthetic effect.
- **How it is used:** To evoke feeling or image, not to state literal facts.
- **Ordinary markers:** Inanimate subjects performing human actions (moon poured,
  autumn writes, river keeps, dawn unbuttons, oak holds), metaphorical verbs,
  similes ("spill out like coins").
- **Consequence:** The literal content is NOT asserted as fact. Do NOT install
  "the moon poured silver" as a factual claim.

### 6. IMPLICATURE
- **What it is:** Conveying a point beyond the literal sentence; the speaker's
  intent is not (only) the literal content.
- **How it is used:** To request, suggest, or hint indirectly ("It is cold in
  here" → "close the window").
- **Ordinary markers:** Statements about changeable states in action-relevant
  contexts (cold in here, trash full, lights on, meeting starting).
- **Consequence:** The literal sentence is NOT installed as the speaker's
  verified point. The implied intent is the content.

### 7. JOKE (via world knowledge)
- **What it is:** An utterance intended to amuse, often with an absurd premise.
- **How it is used:** For humor, not factual assertion.
- **Ordinary markers:** Absurdity violating basic ontology (goldfish filing
  complaints, toasters playing chess, moon calling in sick, refrigerators in
  therapy, arm-wrestling tornadoes).
- **Consequence:** Absurd premises are NOT asserted as fact. (Handled via world
  knowledge in both arms; the JOKE concept per se is not separately installed
  because absurdity detection suffices for these items.)

---

## Provenance

These concepts were authored as the "learned state" for this proof-of-concept
experiment, simulating what TNN would have acquired through prior learning.
In a full TNN, they would be installed via the ordinary learning mechanisms
(exposure to examples, deliberation, consolidation), not hand-authored.

The markers are GENERAL patterns (word classes, structural frames), not
item-specific strings. They apply to novel utterances beyond the test set.

## Bootstrap Audit

**Question:** Does this smuggle in hardcoded epistemic categories?

**Answer:** No. The categories appear ONLY as knowledge entries (name + markers
+ consequence). The deliberator does NOT receive a `type` label with the
utterance. It must MATCH the utterance against the learned markers via
structural pattern recognition, then APPLY the consequence via reasoning.

This is exactly what Micah authorized: "it is learning the concepts first,
then deliberating with them." The law "TNN figures out each utterance's status
itself via deliberation" is preserved: the status is computed, not given.

**What is simplified:** In this proof-of-concept, the marker patterns are
hand-specified rather than learned from examples. The DELIBERATION (matching +
consequence application) is real. A full implementation would learn the markers
through exposure; the reasoning structure would be identical.
