# Q4 ADVERSARY SPECIFICATION (SEALED)

## Family: F-PARCOND (Conditional Parity)

**Status:** SEALED. Designed post-freeze by independent adversary. Not revealed to learner designer until evaluation.

**Prereg:** dd2987e83 (committed before this specification)

---

## Hidden Cause

D = IF X1 THEN (X2 XOR X3) ELSE (X2 AND X3)

In words: When X1 is true, D is the parity of X2 and X3. When X1 is false, D is the conjunction of X2 and X3.

### Operator Count (Generic Language)

- A = X2 XOR X3: 1 operator (XOR)
- B = X2 AND X3: 1 operator (AND)
- D = (X1 AND A) OR ((NOT X1) AND B):
  - NOT X1: 1 operator
  - X1 AND A: 1 operator
  - (NOT X1) AND B: 1 operator
  - OR: 1 operator
  - Subtotal: 4 operators
- **Total: 6 operators** (within 7-operator limit)

### Truth Table (X1, X2, X3 -> D)

| X1 | X2 | X3 | D |
|----|----|----|---|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 |

---

## Structural Difference from Existing Families

### Existing Families

**CONJ:** D = AND(X1, X2). Pure conjunction. 1 operator. Shallow, single algebraic structure.

**XOR:** D = XOR(X1, X2). Pure parity. 1 operator. Shallow, single algebraic structure.

**THRESH:** D = majority(X1, X2, X3) = (X1 AND X2) OR (X2 AND X3) OR (X1 AND X3). Symmetric. 5 operators. Mixed AND/OR but uniform structure: all terms are 2-variable conjunctions, combined disjunctively. The symmetry means no variable plays a special role.

**MUX:** D = IF X1 THEN X2 ELSE X3. Conditional. 4 operators. The branches select variables, not computations. Both branches are trivial (single variable).

**NEST:** Hierarchical composition of previously learned fragments. Tests reuse, not novel structure discovery.

### F-PARCOND: Material Difference

1. **Conditional with COMPUTATIONAL branches (not variable selection).** Unlike MUX (which selects X2 vs X3), F-PARCOND selects between two different computations: XOR vs AND. The learner must discover not just "which variable" but "which operation" applies in each condition.

2. **Asymmetric algebraic structure.** Unlike THRESH (symmetric in X1, X2, X3), F-PARCOND assigns X1 a special role (the condition) and X2, X3 symmetric roles within each branch but with different operations per branch. This breaks the symmetry assumption.

3. **Operator heterogeneity within one expression.** THRESH uses only AND and OR. CONJ uses only AND. XOR uses only XOR. F-PARCOND requires AND, OR, NOT, AND XOR in a single 6-operator expression. The discovery mechanism must coordinate across operator types.

4. **Context-dependent operation.** The correct operation on (X2, X3) depends on X1. This is a higher-order pattern than "apply fixed operation to variables." It tests whether the learner can discover conditional computation, not just conditional selection.

### Why This Tests Generalization

The Q4 training families (CONJ, XOR, THRESH) all have:
- Fixed algebraic structure (no conditionals, except MUX which is trivial)
- Symmetric or simple variable roles
- Single operator type per family (except THRESH which is AND/OR)

F-PARCOND requires:
- Discovering a conditional structure where the condition variable (X1) is not part of the branch computations
- Discovering that different branches need different operators
- Coordinating 4 operator types in one expression

A learner that only memorizes "XOR families use XOR" or "THRESH families use AND/OR" will fail. It must genuinely discover the conditional-computational structure.

---

## Evaluation Protocol (Frozen)

### Observables

Six binary variables: X1, X2, X3, X4, X5, X6.

- X1, X2, X3: Causal parents of D (as defined above).
- X4, X5: Distractor variables (correlated with D at 0.6, but not causal).
- X6: Confound (biased in passive samples, dissociated via intervention, as in Q4 design).

### Phase 1: Discovery

**Goal:** Construct and persist explanatory variable D.

**Samples:**
- 8 biased passive samples (X6 confound present).
- 24 adaptive interventions (learner chooses interventions to dissociate X6 and identify structure).

**Success criteria (KB1/KB2 from Q4):**
- True accuracy >= 0.95 on held-out (all 64 combinations of X1-X6, D computed from X1-X3).
- Beats best observable by >= 0.15 margin.
- Growth trace shows incremental construction (not menu selection).
- Operator count <= 7.

### Phase 2: Reuse

**Goal:** Reuse D as terminal in larger expression.

**Target:** C' = D XOR X4.

**Why:** Tests whether the 6-operator D can be treated as atomic. The XOR with X4 is a 1-operator composition over the kept variable.

**Samples:** 8 passive samples (sufficient if D is atomic).

**Success criteria (KB3 from Q4):**
- Reuse interventions to criterion (hit_iv) vs scratch interventions.
- Ratio <= 0.5 (reuse must be at least 2x more efficient).

### Scoring

Same as Q4:
- KB1: Discovery (accuracy, margin over observables).
- KB2: Non-memorization (operator count, growth trace).
- KB3: Reuse (intervention ratio).
- KB4: Purity (Zag only, deterministic, no em dashes).

### Falsifiers

- F1: Discovery fails (accuracy < 0.95 or margin < 0.15).
- F2: Memorization (operator count > 7 or no growth trace).
- F3: Reuse fails (ratio > 0.5).
- F4: Language violation (operators outside {AND, OR, NOT, XOR} or > 7 ops).
- F5: Not better than baseline (learner <= best observable + 0.15).

---

## Governance

- Designed post-freeze by independent adversary (this worker).
- Sealed until evaluation. Learner designer has not seen this specification.
- Design only. No implementation performed.
- Zero Python. Zero em dashes (verified by byte check).
- Commits: prereg dd2987e83 strictly precedes this specification.
