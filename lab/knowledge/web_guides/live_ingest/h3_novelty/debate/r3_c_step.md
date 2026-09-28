**1. Strongest valid objection**  
The clearest critique is that model‑relative entailment is unreliable: the inference engine may be incomplete, and colluding hosts can feed false facts that are never entailed, so “surprise” alone cannot guarantee novelty. I accept this; it forces me to keep the entailment test but to couple it with a deterministic corroboration gate (≥2 independent, byte‑identical sources) so novelty is declared only when the claim is both unentailed and unsupported by sufficient external evidence.

**2. Operational definition for H3**  
- **Input**: candidate claim c and current world‑model M (frozen symbolic KB).  
- **Step 1 (frozen)**: run deterministic forward‑chaining entailment on M to test M ⊢ c? (boolean).  
- **Step 2 (frozen)**: normalize c to a canonical byte string (lower‑case, no whitespace, hash h). Gather all incoming byte‑identical sentences from distinct sources, compute their hashes, and verify that at least two different source identifiers (e.g., host IDs) provide hash h.  
- **Novelty** = (M ⊢ c = false) ∧ (count ≥ 2 independent sources = false).  

The normalization, hashing, and entailment are deterministic and frozen; the independence check uses static source metadata, so no heuristic learning is involved.

**3. Confidence 85%** – the definition is fully specified, deterministic, and directly enforces the withhold‑side G4 rule while preserving model‑relative surprise.

**4. Open items**  
- Handling partially entailed claims or KB sizes that prevent full forward‑chaining.  
- Formal criteria for “independent” sources when colluding hosts may share identical byte strings.  
- Whether to permit dynamic updates to M during the novelty check without breaking determinism.
