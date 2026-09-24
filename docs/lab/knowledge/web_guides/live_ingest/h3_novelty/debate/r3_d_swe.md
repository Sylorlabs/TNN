**1. Strongest Accepted Objection**
I accept Step’s objection that pure learner uncertainty conflates "not yet derived" with "unknown." This changes position (d) by adding a prerequisite: novelty requires uncertainty *specifically regarding entailment*. If the world-model *could* derive the claim (even if the specific path hasn't been traversed), it is not novel. This prevents the system from flagging redundant logical consequences as new information.

**2. Operational Definition for H3**
**Definition:** Novelty = Logical Openness.
**Computation:**
1.  **Entailment Check (Frozen):** Run deterministic forward-chaining on the KB closure $M$ using the claim $C$ as input. If $C$ is entailed, output **Not Novel**.
2.  **Epistemic State Check (Frozen):** If $C$ is not entailed, inspect the learner's structural graph. If the node for $C$ exists and is settled (True/False), output **Not Novel**. If the node is absent or marked Undecided, output **Novel**.
This distinguishes "corpus had nothing new" (entailed or settled) from "I failed to learn" (entailment failed + node open).

**3. Confidence**
85% — It strictly separates implicit knowledge from actual gaps while remaining deterministic.

**4. Left Open**
1. Computational tractability of exhaustive entailment checks on large KBs.
2. Handling of non-symbolic (probabilistic) entailment in the learner.
3. Whether a "Novel" flag triggers an immediate install or merely a prioritized learning query.
