# Fable Round-2 Architecture E (verbatim from Fable 5.1 deep batched call, 2026-09-24)

## ARCHITECTURE E: NEGATION-FIRST ELIMINATION ENGINE (NFEE)

**1. Name and essence.**

Negation-First Elimination Engine. Instead of deriving what IS true (forward chaining from positive premises), NFEE first derives what CANNOT be true — building an elimination set — and then derives positive conclusions only from claims that survive elimination. The core insight: round 1's fragility came from engines that couldn't distinguish "derivable but false" from "derivable and true". NFEE sidesteps this by inverting the problem: first, use the knowledge store to derive everything that's provably impossible; anything not eliminated is a candidate for positive conclusions. This is structurally different from all round-1 and round-2-slot engines because it treats negation as the PRIMARY engine and affirmation as the secondary step.

**2. Core operation.**

The primitive is **contrapositive firing**: given a rule "if A₁∧A₂∧...∧Aₙ then C", the contrapositive is "if NOT-C then NOT-A₁∨NOT-A₂∨...∨NOT-Aₙ". NFEE works backward from negated goals: to determine whether NOT-H is derivable, it fires contrapositives of rules whose consequent is H (or whose consequent can lead to H). This differs from match-and-bind:

- Match-and-bind is forward: antecedent → consequent. Contrapositive firing is backward: NOT-consequent → NOT-antecedent (disjunctive).
- Match-and-bind produces single conclusions. Contrapositive firing produces disjunctive constraints (NOT-A₁ OR NOT-A₂ OR ...).
- Match-and-bind accumulates positive claims. Contrapositive firing accumulates *elimination constraints* — sets of claims that CANNOT all be simultaneously true.

The elimination set is then used to "filter" forward derivations: a forward derivation is valid only if none of its premises have been eliminated.

**3. Data structures.**

Three arenas:

`ELIM_ARENA` (elimination constraints):
```
constraint_0: [type:u8=0][disj_count:u8][claim_idx:u8, claim_idx:u8, ...]  // "at least one of these claims is false"
```

`FORWARD_ARENA` (positive derivations, same format as CLAIM_ARENA in PCFS but without proof objects — instead, each forward claim carries an `elim_check_index:u16` referencing the point in ELIM_ARENA that was checked before asserting it).

`STATUS_ARENA` (per-claim status, parallel array to claim indices):
```
status[claim_idx]: [eliminated:u8][eliminated_by:u16]  // if eliminated, which constraint did it
```

Audit chains for NFEE are two-phase: (1) show why a claim was NOT eliminated (traverse elimination constraints applied to it and show each was satisfiable), and (2) show the forward derivation that produced it.

Arena sizing: ELIM_ARENA 64KB (up to 4096 constraints × 16 bytes), FORWARD_ARENA 128KB, STATUS_ARENA 8KB. Well within 2^25 limit.

**4. Search/control strategy.**

Phase 1 — Elimination pass (backward):
- Start from negated query: derive NOT-H by contrapositive firing.
- For each rule whose consequent matches H (or matches something that can derive H), fire contrapositive: produce disjunctive constraint on antecedent negations.
- Propagate: for each negated antecedent NOT-Aᵢ, check if Aᵢ is itself the consequent of another rule; if so, fire that rule's contrapositive too.
- Continue until depth bound (8 primary, 16 scaled) or no new elimination constraints.
- Result: ELIM_ARENA filled with disjunctive constraints.

Phase 2 — Forward pass (filtered):
- Standard forward chaining (match-and-bind) from initial positive claims.
- Before asserting any new claim C, check: for each elimination constraint in ELIM_ARENA, is C one of the disjuncts? If C would violate an elimination constraint, C is marked eliminated and NOT asserted.
- Continue until goal H is asserted (H survives elimination) or depth bound reached.

Termination: H asserted and surviving elimination → "H derivable". H derivable but eliminated → "H contested" (NOT-H has stronger support). H not derivable → "H unsupported".

**5. Contradiction handling.**

Under false-rule injection: a false rule F: "if TRUE then NOT-H" fires in Phase 1, producing a direct elimination constraint: [NOT-H]. In Phase 2, H cannot be asserted because the elimination constraint kills it. But NFEE doesn't halt — it continues deriving all other claims, and can report that H is "contested by constraint from rule F".

This is the KEY advantage: NFEE can identify SPECIFICALLY which rules contribute to H's elimination. ONE cannot do this (it halts globally). DUAL can score evidence but cannot pinpoint the source. PCFS can quarantine but must detect contradiction first. NFEE detects elimination *as a first-class operation* and can attribute it.

Under multiple false rules with contradictory implications: NFEE produces multiple elimination constraints. If constraint₁ eliminates claim X and constraint₂ eliminates claim Y, but X and Y are independent, both eliminations proceed independently. If constraint₁ and constraint₂ jointly eliminate ALL claims (the knowledge store is entirely suspect), NFEE reports this clearly: "all derivations contested, elimination constraints cover all claims".

Weakness: contrapositive firing produces disjunctive constraints, which are harder to reason about than conjunctive derivation. In a knowledge store with many rules, the number of elimination constraints can grow faster than the number of positive derivations (worst case: exponential in rule count). However, depth bounds limit this growth, and in practice, most rules have small antecedents (2-4 literals), keeping disjunct size manageable.

**6. Pure-Zag determinism plan.**

- Phase 1 and Phase 2 are strictly sequential (no interleaving — deterministic ordering).
- Within each phase, iteration follows committed rule order and claim-address order (same as PCFS).
- Contrapositive firing: for rule R with consequent C and antecedents A₁...Aₙ, the contrapositive constraint is computed by iterating antecedents in index order (deterministic).
- Elimination checking in Phase 2: iterate ELIM_ARENA in order, check each constraint against the candidate claim using `_zag_strcmp` (inverted — returns 1 on equality, so check for match and negate).
- Append-only arenas, no deallocation, no RNG. 3x byte-identical reruns guaranteed by construction.

**7. Falsifiable prediction vs round-1 engines.**

Prediction: **On a battery of problems where NOT-H is derivable from 2 false rules and H is derivable from 5+ legitimate rules (KB5-style), NFEE will produce exactly 0 incorrect positive conclusions AND will produce an attribution string identifying the specific false rules responsible for H's elimination, where ONE produces 60/60 withholds (0 attributions) and DUAL produces 0 incorrect but no rule-level attribution.**

The measurable claim: NFEE's Phase 1 will produce ≤5 elimination constraints that specifically block H, and Phase 2 will successfully derive all other claims (untainted by the false rules' elimination constraints, provided those constraints don't intersect with the legitimate derivation paths).

Kill-bar falsification: if NFEE produces >3 incorrect positive conclusions on this battery, the Phase 2 filtering is incomplete (elimination constraints are being missed). If NFEE's Phase 1 produces >20 elimination constraints for a problem where ONE halts within 5 derivations, the contrapositive expansion is excessive (suggesting the approach doesn't scale to deeper knowledge stores).

Additional prediction: **NFEE will show the largest performance gap vs ONE on problems where the knowledge store contains many rules with shared antecedents** (because contrapositive firing on shared antecedents produces constraints that eliminate many claims simultaneously — a leverage effect that forward chaining lacks).

---

