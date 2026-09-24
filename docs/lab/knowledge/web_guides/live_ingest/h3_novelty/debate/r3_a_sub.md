SUBSTITUTE VOICE for position (a) (Sol unavailable; voiced by a stand-in model from Sol's Round 1 + all Round 2s).

**1. Strongest point made against position (a)**

The strongest point made against position (a) is that Rival D's objection, which states that "deterministic uncertainty" is operationally incoherent in a zero-RNG substrate, has a valid point. In a system without randomness, the concept of uncertainty as a degree of belief becomes incoherent, and attempting to implement it risks collapsing into "not yet computed" or relying on arbitrary heuristics. This objection highlights a potential flaw in the operationalization of position (a)'s definition of novelty.

**2. Proposed operational definition of novelty for position (a)**

To operationalize novelty for position (a), I propose the following definition:

- **Frozen parts:**
  - TNN's current knowledge state (ledger)
  - Normalization rules (lowercase, synonym collapse, quantifier expansion)
- **Heuristic parts:**
  - Semantic matching algorithm (with conservative and deterministic settings)
  - G4's byte-identical >=2-source rule
- **Inputs:**
  - Extracted claims from the corpus
  - TNN's world-model
- **Mechanism:**
  1. Normalize the extracted claim using the frozen normalization rules.
  2. Check if the normalized claim matches any installed fact in the ledger byte-identically. If a match is found, mark the claim as non-novel.
  3. If no match is found, use the semantic matching algorithm to determine if the claim is semantically similar to any installed fact. If a match is found, mark the claim as non-novel.
  4. If the claim is not marked as non-novel, apply G4's byte-identical >=2-source rule to determine if it can be installed. If the rule is satisfied, mark the claim as novel and installable.

**3. Confidence (0-100%):** 80%

**4. What is left open:**

1. The exact implementation of the semantic matching algorithm and its conservative and deterministic settings.
2. The handling of borderline cases where the semantic matching algorithm is unsure about whether a claim matches an installed fact.
3. The potential for adversarial attacks that exploit the use of semantic matching to bypass the byte-identity rule.
