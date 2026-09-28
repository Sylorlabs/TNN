**Steelman Position (d):**

1.  **Internal Locus:** Novelty is strictly an epistemic status of the learner, not a feature of the external text. A claim is novel only if the TNN's current state lacks a derivation path to a boolean (True/False) value for that proposition. "Known" claims are already settled in the graph; "unknown" claims are simply open slots waiting for evidence.
2.  **Enabling H3:** This definition operationalizes H3 perfectly. "Corpus had nothing new" is simply a report that the ingestion cycle found zero open-state nodes to populate. "Failed to learn" is a process error (crash, deadlock). The distinction reduces to checking if the state changed, rather than guessing external intent.
3.  **Deterministic Uncertainty:** Uncertainty is not probability; it is the absence of a proof. A deterministic substrate maintains "uncertainty" as a structural property—e.g., a node marked "Open" because no derivation chain exists yet. This is a genuine lack of information, functionally distinct from "settled," without requiring a random number generator to simulate doubt.

**Struggle:**
(1) Paraphrase vs novelty — is a reworded known fact novel?

**Partial Answer:**
If the learner lacks a robust normalization layer that maps "A = B" to "B equals A," a paraphrase registers as novel. The system must treat semantic variation as structural novelty until logic resolves it. The risk is a state bloated with "novel" synonyms that represent no new information, requiring a rigorous canonicalization pipeline to filter true novelty from mere rephrasing.
