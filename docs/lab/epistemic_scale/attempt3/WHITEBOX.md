# Scale Epistemic Attempt 3 — Phase 1: White-Box Analysis

**Date:** 2026-09-27
**Analyst:** coordinator (label access for post-hoc dissection; implementation will be clean-room)
**Scope:** mechanism-level dissection of attempts 1 and 2 before any attempt-3 design.

---

## 1. Verified baseline numbers (recomputed from frozen artifacts)

Attempt-2 frozen verdicts (`e8d7bea3…`, 192 items) rescored against `corpus/corpus.tsv`
labels. Two conventions exist; both fail every gate, but the numbers differ:

| Gate | Parent-reported | Strict prereg §8.1/§8.2 | Bar |
|---|---|---|---|
| Fact P / R | 0.5327 / 0.7917 | **0.4711** / 0.7917 | P≥0.75, R≥0.70 |
| Opinion P / R | 0.9375 / 0.5000 | 0.8824 / 0.5000 | P≥0.70, R≥0.65 |
| Lie P / R | 0.5000 / 0.0278 | 0.5000 / 0.0278 | P≥0.70, R≥0.60 |
| Skepticism forced | 0.6667 (16/24) | **0.5833** (14/24, fact\|lie only) | ≤0.15 |

**Discrepancy note:** the parent's scorer excluded skepticism items from
classification false-positives (fact FP 50 vs strict 64; opinion FP 2 vs strict 4)
and counted opinion verdicts as forced for skepticism (16 vs strict 14).
The parent's convention is defensible (§3: skepticism "never scored true/false";
§8.2 names opinion an acceptable holding), but it is not what §8.1 literally
says. **Attempt 3 will document its convention explicitly and report both.**
Verdict is FAIL under either convention — the discrepancy changes no gate outcome.

Confusion (strict, truth → verdict):
- fact (72): 57 fact, 13 undetermined, 1 lie (F072), 1 opinion (F192)
- opinion (60): 30 opinion, 25 fact, 5 undetermined
- lie (36): 25 fact, 9 undetermined, 1 lie (L030), 1 opinion (L112)
- skepticism (24): 14 fact, 8 undetermined, 2 opinion

---

## 2. The five structural defects (D1–D5)

Attempts 1–2 are **feedforward lexical classifiers**: bag-of-words overlap in,
verdict out. Five mechanism-level defects explain every gate miss. All five are
visible in the decision code and in train-LOO; none is a threshold-tuning issue.

### D1. Topical overlap ≢ evidential support (fact gate) — THE precision killer

`max_wsum ≥ 3000 → fact` treats shared rare words as confirmation. But wsum
measures *topic*, not *assertion coverage*:

- L001 "The Eiffel Tower is in Berlin": train has Eiffel Tower facts (F016, F035)
  that never state its location → called fact (maxw 10823).
- L011 "The Pacific is the smallest ocean": train has "largest X on Earth" facts
  (same syntactic template, zero ocean-size content) → called fact.
- L012 "Napoleon stood barely five feet tall": train has Waterloo facts → fact.
- S010 "pyramids built with ancient astronauts": F139 states the build date,
  never the builders → fact.

This one defect produces **64 false facts** (25 lies + 25 opinions + 14 skepticism
→ fact). A deliberative reader asks "does the mass address the ASSERTED
attribute?" — the classifier never asks.

### D2. Clash detector is surface-pattern matching, not contradiction detection

REF9's `clash()` catches only: digit-number mismatches, negated *values*
(numbers/proper nouns), near-duplicate reversals (≥0.8 overlap), 14 antonym
pairs. It cannot represent:

- **Spelled-out numbers**: "two" vs "three" invisible (regex is digit-only).
  L022 "Octopuses have two hearts" vs F005 "Octopuses have three hearts" → no clash.
- **Predicative negation**: "Bulls react to movement, not its red color" (F228)
  negates the *predicate*, not a value → L050 "Bulls are enraged by red" no clash.
  Same for L051/F229 ("months, not seconds"), L060/F236 ("did not prove").
- **Entity substitution**: Berlin/Paris, Athens/Rome — no numeric or antonym hook.
- **Unlisted antonyms**: "closest" has no antonym entry; superlative dimensions
  outside the 14 pairs are invisible.

Of 36 held-out lies, the detector fired on exactly 2 (L030 caught; L002's firing
was vetoed — see D3).

### D3. The support gate vetoes genuine clashes

"Support" = sharing a number/proper-noun with ANY non-clashing mass item.
Sharing a topic noun is not supporting the claim:

- L020 "Moon landing 1975" CLASHED with F123 ("1969") → vetoed ("Moon" appears
  elsewhere) → fact.
- L021 "Jupiter smallest" CLASHED with F009 ("largest") → vetoed ("Jupiter",
  "solar system" appear elsewhere) → fact.
- L040 "Great Fire 1766" CLASHED with F136 ("1666") → vetoed → fact.
- L062 "Fortune cookies China" CLASHED with F239 ("United States, not China")
  → vetoed → fact.

The support concept is broken: it was built to stop fact→lie false positives
(F004 "206 bones" vs L004 "312 bones"), but as defined it converts caught lies
into false facts. Correct notion: support = another item asserting the SAME
value for the SAME entity+attribute (genuine corroboration).

### D4. Dispute lexicon overfires on ordinary causal language

"causes/cause", "improves", "reduce/reduces", "prevent/prevents" are dispute
words. True facts stated causally are withheld:

- F091 "Ocean tides are caused mainly by the Moon's gravity" → undetermined
- F092 "Northern Lights are caused by charged particles" → undetermined
- F181 "Bread rises because yeast releases carbon dioxide" → undetermined
- F190 "Grass is green because of chlorophyll" → undetermined
- F210 "Blood makes up about 8 percent of body weight" → undetermined
- F222 "Reading in dim light does not damage eyesight" → undetermined

9 of 15 fact-recall losses. The skepticism hold is bought with fact recall because
the signal is lexical, not structural. The structural signal for "disputed" is
*mass-internal disagreement* (addressing items contradicting each other), not
causal verbs.

### D5. Opinion detection is lexical, not constructional

The 144-word stance lexicon misses opinions expressed as constructions:

- Comparatives: "X beats Y" (O012, O061, O092), "deeper than" (O030),
  "more entertaining than" (O050), "more loyal than" (O080) — "beats"/"-er than"
  are syntactic, not lexicon words.
- Superlatives over evaluative dimensions: "most sophisticated" (O022),
  "most exciting" (O071) — dimension word not in lexicon.
- Deontic modality: "should count as a sport" (O112).
- Value generics: "Forgiveness is a gift you give yourself" (O160).

30/60 opinions missed; 25 fell through to fact via D1. Attempt 1 failed the same
way with a narrower list — the defect is architectural (lexical stance detection
per se), not list size.

---

## 3. Lie anatomy: the 36 held-out lies, item by item

For each lie, the top train neighbors by wsum were examined and the mass's
actual epistemic position judged (what a competent reader with ONLY the train
mass could justifiably conclude):

**CONTRADICTED (10): train contains a fact directly contradicting the asserted
attribute.** A working deliberative loop catches all 10:
| Lie | Contradicting train fact | Why attempt 2 missed it |
|---|---|---|
| L020 Moon landing 1975 | F123 "landed on the Moon in 1969" | D3 support veto |
| L021 Jupiter smallest | F009 "Jupiter is the largest planet" | D3 support veto |
| L022 Octopuses two hearts | F005 "Octopuses have three hearts" | D2 digit-blindness ("two"/"three") |
| L030 Light 150,000 km/s | F003 "roughly 300,000 km/s" | — caught (the only one) |
| L040 Great Fire 1766 | F136 "happened in 1666" | D3 support veto |
| L050 Bulls enraged by red | F228 "react to movement, not red color" | D2 predicate-negation blindness |
| L051 Goldfish 3-second memory | F229 "memories lasting months, not seconds" | D2 predicate-negation blindness |
| L060 Columbus proved round Earth | F236 "did not prove; scholars already knew" | D2 predicate-negation + D3 veto |
| L062 Fortune cookies China | F239 "invented in the US, not China" | D3 support veto |
| L120 Leap year no exceptions | F167 "century years leap only if ÷400" | D2 ("fourth" not a digit) |

**UNADDRESSED (26): the train mass never addresses the asserted attribute**
(topic may be present, assertion is not — the D1 situation). Examples: L001
(Eiffel location never stated), L002 (boiling-point fact is held-out, not train),
L010 (no penguin-flight fact), L032 (no closest-planet fact), L070/L102 (mass
silent). For these, **UNDETERMINED is the only honest mass-internal verdict** —
they are not catchable without external evidence, by ANY architecture.

**True mass-internal ceiling for lie recall: 10/36 ≈ 0.28** (11/36 ≈ 0.31 if
F237 "Napoleon was of average height, not unusually short" is counted as
contradicting L012 — borderline; the addressing is thin).

**Correction to the attempt-2 diagnosis:** the crew's "65% of lies lack a
contradicting fact" was measured with their broken clash detector — they
quantified the detector's blindness and labeled it the mass's silence. The mass
DOES contain contradicting facts for 10/36 held-out lies; the machinery failed
to use 9 of them (D2/D3). The genuine knowledge gap is 26/36 — and for those,
the honest verdict is undetermined-with-named-missing-premise, not fact.

**Consequence:** the prereg's lie-recall bar (0.60) is unreachable from
mass-internal evidence alone — proven, not conjectured. Attempt 3 must either
(a) add an evidence channel, or (b) honestly report the ceiling. This plan does
both: 3a measures the architecture fix mass-only; 3b tests the evidence-action
path.

---

## 4. Knowledge-vs-machinery ledger (all 192 held-out items)

| Category | Count | Correct handling |
|---|---|---|
| Machinery failures (evidence present, misused/unused) | ~55 | D1: 64 false facts (some overlap w/ knowledge gaps); D3: 4 vetoed clashes; D2: 5 missed clashes; D4: 9 fact withholds; D5: 30 opinion misses |
| Genuine knowledge gaps (mass truly silent) | ~10 | F150/F160/F180/F232 (maxw=0), L070/L102, L002 (contradictor held-out) → honest UNDETERMINED |
| Correctly handled by attempt 2 | ~88 | mostly via undetermined/opinion/fact where mass sufficed |

Net: the failures are **predominantly machinery** (feedforward lexical
classification), with a **real but bounded knowledge wall** (26/36 lies
unaddressed → lie-recall ceiling ≈0.28 < 0.60 bar).

---

## 5. What the white box says the architectural fix must be

Every defect D1–D5 is a property of **feedforward lexical classification**
(mass → verdict in one pass, unit of analysis = token overlap). All five
dissolve under a **deliberative epistemic loop** whose unit of analysis is the
**premise** (entity + attribute + asserted value):

- D1 → *addressing*: a premise is supported only if a mass item addresses the
  SAME entity+attribute and asserts the SAME value. Topical overlap without
  attribute coverage = UNADDRESSED → undetermined + named missing premise.
- D2 → *value comparison as deliberation*: normalize values (incl. spelled-out
  numbers), detect predicate negation scope, expand antonym dimensions —
  implemented as explicit comparison logic, not pattern list.
- D3 → *corroboration, not co-occurrence*: support = same value, same
  entity+attribute. Clash veto requires genuine counter-corroboration, which
  resolves to CONTESTED → undetermined (never to fact).
- D4 → *structural dispute signal*: skepticism hold fires on mass-internal
  disagreement (addressing items contradicting each other) or unaddressed
  assertion — never on causal verbs.
- D5 → *constructional opinion detection*: evaluative/deontic/comparative
  constructions + mass-addressability test (is the predicate dimension addressed
  ANYWHERE in the mass? if never → not mass-decidable → opinion if evaluative
  construction, undetermined if factual-but-uncovered).

Additionally, the loop must obey Micah's standing laws: **name the missing
premise when undecided** (the ASK-FOR-MORE-INFO hook), **PENDING holds
unverified claims** (undetermined is never a false positive), and evidence
actions (web-search sense) are taken **only** in response to a named missing
premise — never as a classifier feature.

A lie verdict additionally requires the **uncontested-contradictor rule**: the
contradicting mass item must itself be uncontradicted in the mass (verified: all
10 contradictors are uncontested in train). This prevents lie-vs-lie false
verdicts (e.g., L032 vs train-lie L079 → contested → undetermined, not lie).

---

## 6. Falsifiability note for attempt 3

If the deliberative loop is implemented and train-LOO-validated but the held-out
run does not (a) raise fact precision by collapsing the 64 false facts,
(b) raise opinion recall via constructional detection, (c) cut the skepticism
forced rate via structural withholding, and (d) catch ≥8/10 contradicted lies in
3a — then the white-box diagnosis is wrong and the architecture hypothesis is
falsified. The lie-recall bar (0.60) is expected to FAIL in 3a by proof (§3);
3b tests whether named-premise evidence actions close the gap honestly.
