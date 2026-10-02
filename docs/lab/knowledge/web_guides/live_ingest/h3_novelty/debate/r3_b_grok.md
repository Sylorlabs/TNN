**1. Strongest conceded point against (b)**  
The A9 colluding-hosts vulnerability: byte-identical sentences can be forced through the >=2 gate by coordinated adversaries, labeling misinformation as “non-novel” while genuine signals remain withheld. This is valid; it exposes that the gate checks only surface corroboration, not content integrity. My position is unchanged—novelty remains the withhold trigger—but the definition must be paired with an explicit post-gate integrity filter (e.g., cross-source semantic hash) to block the attack surface.

**2. Operational definition for H3**  
Hand to mechanism crew:  
- **Input**: stream of byte-identical normalized sentences S (lowercase, punctuation-removed, deduplicated per source).  
- **Frozen parts**: normalization function N (deterministic, zero-RNG) and source-ID extractor (IP + timestamp + host hash).  
- **Heuristic part**: G4 gate G(S) = 2 if ≥2 independent sources produce identical N(S), else 1.  
- **Computation**: for each arriving S, compute G(S); if G(S)<2 then withhold and tag “novel”; else install and tag “corroborated”. Ledger stores only (N(S), source-list, install-flag).  
- **Distinguishes**: “corpus had nothing new” (G<2, withhold) vs “failed to learn” (G=2 but content later rejected by integrity check).  

<=180 words.

**3. Confidence: 82%**  
The gate is the only deterministic, zero-RNG primitive that survives the LI-1 pilot and A2/BUGFIX-1 red-teams.

**4. Leave open**  
- How to compute “independent source” under partial network partitions.  
- Edge case of semantically synonymous but not byte-identical paraphrases from different hosts.  
- Long-term ledger bloat from repeated withhold tags.
