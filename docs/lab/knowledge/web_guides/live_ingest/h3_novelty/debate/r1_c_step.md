**Steelman of Position (c): Novelty = model‑relative surprise**

1. **Predictive‑processing grounding** – In a deterministic AI, learning can be viewed as continuously refining a world‑model M that generates expectations E about upcoming propositions. A claim c is *novel* iff M ⊬ c (c is not entailed) and M ⊬ ¬c (c is not contradicted) — i.e., c lies outside the current closure of M and therefore surprises the learner. This directly captures H3’s goal: “I learned nothing” means every incoming c was already predicted (entailed) or ruled out by M, so no surprise occurred.

2. **Separates epistemic failure from genuine redundancy** – If the learner’s model is incomplete, novel claims will appear and drive updates; if the corpus merely repeats what M already knows, the novelty detector stays silent, giving a clean signal that the system has *exhausted* learnable information rather than having *failed* to acquire it.

3. **Deterministic operationalization of “expects”** – Expectations need not be probabilistic. M can be a symbolic knowledge base equipped with a sound, complete inference engine (e.g., forward‑chaining Horn clauses). Given current state S, the engine deterministically computes the deductive closure Cl(S). Expectation E(c) = true iff c∈Cl(S). No randomness is introduced; the outcome is byte‑identical for identical inputs.

4. **Compatibility with G4’s zero‑randomness rule** – Novelty judgments are pure functions of (S, c) and the deterministic inference mechanism. They require no sampling, no stochastic thresholds, and thus preserve byte‑identical runs across identical world states.

5. **Clear audit trail** – A novelty judgment can be logged as: (i) the exact inference steps that failed to derive c or ¬c from S, (ii) the normalized sentence used for comparison, and (iii) the version of M/S at the time. This satisfies the knowledge‑ledger provenance requirement while keeping the judgment itself independent of corroboration counts.

---

**Hard question I wrestle with most:**  
*Paraphrase vs. novelty* – Is a reworded known fact novel?

**Partial answer:**  
Treat a paraphrase as non‑novel only when a deterministic semantic normalizer can prove equivalence to an existing entry in M. The normalizer reduces sentences to a canonical logical form (e.g., predicate‑argument structure with standardized constants) using a fixed rule set (lowercase, collapse whitespace, eliminate synonyms via a vetted lexical ontology, expand quantifiers, etc.). If the canonical forms match byte‑for‑byte, the claim is deemed a known fact; otherwise it is flagged as novel until further corroboration allows its canonical form to be added to M. This preserves the anti‑gameability of byte‑identity (the normalizer itself is deterministic and fixed) while granting limited tolerance for harmless re‑phrasing, thereby addressing the paraphrase tension without re‑opening the sockpuppet loophole.
