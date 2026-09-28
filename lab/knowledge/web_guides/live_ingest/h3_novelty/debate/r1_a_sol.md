1. **Novelty is relative to the installed ledger, not to wording.** The relevant question is whether the corpus contributes a fact absent from TNN’s current knowledge state. A byte-identical sentence is too narrow: ordinary sources routinely express the same fact differently. Lexical and semantic matching lets TNN recognize that “the Earth orbits the Sun” does not become novel merely because it is phrased as “Earth travels around the Sun.”

2. **This directly operationalizes H3.** For each extracted claim, TNN can produce a deterministic disposition:  
   - matched to an installed fact → not novel;  
   - no match, but fails G4 → potentially novel but withheld for integrity;  
   - no match and passes G4 → novel and installable.  
   Thus “I learned nothing” means the corpus contained no unmatched, installable knowledge—not merely that the extractor happened to produce zero installs.

3. **Novelty and installation are different predicates.** G4 governs whether a claim may enter the ledger; matching governs whether a claim is already represented there. A claim can be semantically familiar yet withheld because its current evidence is insufficient, or genuinely absent yet withheld because it lacks corroboration. Keeping those outcomes separate preserves both safety and diagnostic value.

4. **The definition is deterministic and auditable.** Given the same ledger, normalization, matcher, and thresholds, every run returns the same novelty result. The result can cite the exact installed fact and matching rationale, rather than hiding failure behind a count of zero installs.

**Hard question: the sockpuppet tension.** A paraphrase-tolerant matcher appears to reintroduce the very attack that byte-identity was chosen to prevent: colluding sources can paraphrase a false claim and evade a literal-equality defense. My partial answer is to keep matching strictly downstream of trust: semantic similarity may establish *non-novelty relative to an already installed fact*, but it must never establish corroboration or authorize installation. New claims still require G4’s independent, byte-identical support. Matching should also be conservative and deterministic, with borderline cases reported as “unknown” rather than treated as matches. This does not solve the A9 integrity boundary; it prevents novelty detection from weakening G4 while still distinguishing “already known” from “not safely learned.”
