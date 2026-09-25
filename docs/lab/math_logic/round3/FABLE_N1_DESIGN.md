# NATIVE-ENTAIL: A Byte-Level Reasoning Engine Design

This is a deep design document. I will be concrete and honest about what is genuinely hard.

---

## (a) STATE REPRESENTATION

### Working state: the Stack of Text States

The engine maintains a **stack of Text States**. Each Text State is a sequence of bytes. The initial Text State is the raw input problem bytes. Each inference step appends new Text States to the stack (or rewrites existing ones). The entire derivation history is the stack itself.

```
struct TextState {
    id:       u32,           // monotonic, assigned at creation
    bytes:    &[u8],         // raw English text, no encoding assumptions beyond ASCII
    source:   StepSource,    // how this state was produced
    depth:    u32,           // derivation depth (0 = input)
}

enum StepSource {
    Input,                    // depth 0: the original problem
    KnowledgeCite(kid: u32), // cited verbatim from knowledge store
    Inference {
        rule_id:   u32,      // which license fired
        hole_map:  Vec<(HoleId, Span)>, // byte-span bindings for each hole
        premises:  Vec<u32>,  // TextState ids consumed
    },
}
```

### What a "step" transforms

A step consumes one or more existing Text States and produces a new one. The step is the triple:

```
(license_pattern_id, hole_bindings, consumed_state_ids) → new TextState
```

The new TextState's bytes are derived deterministically from the license's output template plus the hole bindings. The stack grows monotonically — steps add, they do not remove (though the referee may mark states as "defeated").

**Example:** Starting state:

```
State 0 (depth 0, Input):
"Prove that the square root of 2 is irrational."
```

After citing K105:

```
State 1 (depth 1, KnowledgeCite(105)):
"Rational: a real number expressible as p/q with integers p, q != 0. Irrational: a real number that is not rational."
```

After citing K005:

```
State 2 (depth 1, KnowledgeCite(005)):
"Rules of inference: modus ponens (from P and P=>Q, infer Q); proof by contradiction (if assuming NOT-P leads to a contradiction, infer P)."
```

### Key design decision: NO shared variable bindings across states

States do not "bind" x=2 or "scope" variables. Each state is an independent text blob. The only connection between states is the license pattern that consumed them and the byte-span holes it matched. This is critical for the anti-bridge argument (section c).

---

## (b) THE INFERENCE LICENSE

### License structure

A license is a **byte-pattern rewrite rule** with named holes. It has:

1. A **premise pattern**: a sequence of literal byte sub-sequences and named holes (`[H1]`, `[H2]`, ...) that must match against Text States.
2. A **consistency constraint**: optional byte-level checks between hole bindings (e.g., "the bytes in [H1] must be identical to the bytes in [H2]").
3. An **output template**: a byte sequence with holes filled by the bindings.

This is more powerful than regex but structured the same way: it is a **pattern over bytes with capture groups and a rewrite output**. No semantic variables, no type system, no quantifier scope.

### License format (pseudocode)

```
struct License {
    id:           u32,
    name:         String,         // human-readable, for citation
    premises:     Vec<Pattern>,   // one Pattern per consumed TextState
    constraints:  Vec<Constraint>, // equality/inequality on hole bindings
    output:       Template,       // bytes with holes
    mode:         InferenceMode,  // Forward | Backward | Refutation
}

struct Pattern {
    segments: Vec<PatternSegment>,
}

enum PatternSegment {
    Literal(Vec<u8>),    // exact byte match
    Hole(HoleId),        // captures a contiguous byte span
    Wildcard,            // matches any bytes (greedy, bounded by surrounding literals)
}

struct Constraint {
    lhs: HoleId,
    op:  EqOp,          // EqBytes | NeqBytes | SubstringOf | BytePrefix
    rhs: HoleId,        // or Literal(Vec<u8>) for constant checks
}

struct Template {
    segments: Vec<TemplateSegment>,
}

enum TemplateSegment {
    Literal(Vec<u8>),
    Hole(HoleId),       // emits the bytes captured by this hole
}
```

### Concretizing K005: Modus Ponens

K005 text: `"Rules of inference: modus ponens (from P and P=>Q, infer Q); proof by contradiction (if assuming NOT-P leads to a contradiction, infer P)."`

The engine must extract the **modus ponens sub-license** from this text. This is itself a byte-level operation: find the substring between `"modus ponens ("` and `"); proof by contradiction"`, yielding:

```
"from P and P=>Q, infer Q"
```

This sub-text becomes the **license template**. The engine interprets the pattern `from [H_PREMISE] and [H_PREMISE"]=>[H_CONCLUSION], infer [H_CONCLUSION]` as a modus ponens license. This interpretation is done by a small, fixed set of **pattern idioms** — not a full parser, but a dictionary of ~20 byte-level idiom recognizers (see below).

#### Pattern Idiom Recognizers (fixed, general, not problem-specific)

The engine has a hardcoded set of ~20 **license shape recognizers** that match structural patterns in the extracted license text. These are NOT domain-specific — they recognize general inferential shapes:

| Idiom | Byte pattern it recognizes | Produces |
|-------|--------------------------|----------|
| `MP-SHAPE` | `from [A] and [A]=>[B], infer [B]` | Modus Ponens license |
| `MP-SHAPE-v2` | `if [A] and [A] implies [B], then [B]` | Modus Ponens license |
| `CONTRA-SHAPE` | `if assuming [A] leads to a contradiction, infer [not-A]` | Proof by contradiction license |
| `UNIV-SHAPE` | `for all [X], if [X] is [KIND], then [PROPERTY]` | Universal instantiation |
| `DEF-SHAPE` | `[TERM] means/is/defined as [DEFINITION]` | Definition expansion |
| `LEMMA-SHAPE` | `if [CONDITION], then [CONSEQUENCE]` | Conditional rule |
| `BICON-SHAPE` | `[A] iff [B]` | Biconditional (bidirectional) |
| ... | ... | ... |

Each recognizer is a fixed byte-pattern matcher with named slots. For MP-SHAPE:

```
fn recognize_mp(bytes: &[u8]) -> Option<License> {
    // Literal: b"from "
    // Hole [A]: until b" and "
    // Literal: b" and "
    // Hole [A再度]: until b"=>", must equal [A] byte-for-byte
    // Literal: b"=>"  
    // Hole [B]: until b", infer "
    // Literal: b", infer "
    // Hole [B再度]: until end, must equal [B] byte-for-byte
    
    let a_start = find_literal(bytes, b"from ")? + 5;
    let a_end = find_literal_from(bytes, b" and ", a_start)?;
    let a = &bytes[a_start..a_end];
    
    let arrow_start = find_literal_from(bytes, b"=>", a_end + 5)?;
    let b_start = arrow_start + 2;
    let b_end = find_literal_from(bytes, b", infer ", b_start)?;
    let b = &bytes[b_start..b_end];
    
    let b_check_start = b_end + 8;
    let b_check = &bytes[b_check_start..];
    
    if a != &bytes[find_literal_from(bytes, b" and ", 0)? + 5..find_literal_from(bytes, b"=>", 0)?]
        || b != b_check {
        return None; // Consistency constraint failed
    }
    
    Some(License {
        premises: vec![
            Pattern { segments: vec![Hole("A")] },           // premise 1: the "P"
            Pattern { segments: vec![Hole("A"), Literal(b" => "), Hole("B")] }, // premise 2: "P => Q"
        ],
        constraints: vec![
            Constraint { lhs: "A1", op: EqBytes, rhs: "A2" },  // premise 1 holes match
            Constraint { lhs: "B1", op: EqBytes, rhs: "B2" },  // conclusion holes match
        ],
        output: Template { segments: vec![Hole("B")] },
        mode: Forward,
    })
}
```

#### Concretizing K202: Euclid's Lemma

K202 text: `"Euclid's lemma: if p is prime and p divides a*b, then p divides a or p divides b."`

Extract sub-text after `"Euclid's lemma: "`: `"if p is prime and p divides a*b, then p divides a or p divides b"`

This matches `LEMMA-SHAPE`:

```
if [H_CONDITIONS], then [H_CONSEQUENCE]
```

But we need to decompose `H_CONDITIONS` further. The engine applies a secondary **conjunction-split** idiom on `H_CONDITIONS = "p is prime and p divides a*b"`:

```
fn split_conjunction(bytes: &[u8]) -> Option<Vec<&[u8]>> {
    // Find " and " not inside nested parentheses
    // Split into conjuncts
}
```

Yields: `["p is prime", "p divides a*b"]`

The license becomes:

```
Premises:
  Pattern 1: Literal("if ") + [H_PRIME_OF] + Literal(" is prime")  →  captures [H_PRIME_OF]
  Pattern 2: Literal("if ") + [H_PRIME_OF] + Literal(" divides ") + [H_PRODUCT] + Literal(", then ") + [H_PRIME_OF] + Literal(" divides ") + [H_FACTOR1] + Literal(" or ") + [H_PRIME_OF] + Literal(" divides ") + [H_FACTOR2]
```

Wait — this is getting complex. Let me restate it more cleanly. The license for Euclid's lemma, as a byte-pattern:

```
Premise P1: [TEXT containing "prime"] — matches a Text State asserting primality of some entity
Premise P2: [TEXT containing "divides" and a product "X*Y"] — matches a Text State asserting divisibility of a product

Constraints:
  - The "prime entity" bytes in P1 must match the "divisor" bytes in P2
  - P2 must contain a product pattern: [DIVISOR] + " divides " + [FACTOR1] + "*" + [FACTOR2]

Output Template: "[PRIME_ENTITY] divides [FACTOR1] or [PRIME_ENTITY] divides [FACTOR2]"
```

#### Worked micro-example on raw bytes

Input state stack:

```
State 0: "Prove that the square root of 2 is irrational."
State 1 (cite K101): "Divisibility: for integers a, b with a != 0, a divides b (a|b) iff there exists an integer c with b = a*c."
State 2 (cite K202): "Euclid's lemma: if p is prime and p divides a*b, then p divides a or p divides b."
State 3 (cite K105): "Rational: a real number expressible as p/q with integers p, q != 0. Irrational: a real number that is not rational."
```

**Step 4:** Apply DEF-SHAPE to State 3. Recognize `"[TERM] means/is/defined as [DEF]"` — but the actual text says `"Rational: a real number expressible as p/q with integers p, q != 0."` This matches a `DEF-SHAPE` variant: `"[TERM]: [DEFINITION]"`. Output:

```
State 4 (Inference, DEF-EXPAND, premises=[3]):
  "Rational means: a real number expressible as p/q with integers p, q != 0."
```

**Step 5:** Apply NEGATION-IDIOM to State 4 + State 3 (which also says `"Irrational: a real number that is not rational."`). The engine applies a pattern that detects `"[X]: a real number that is not [Y]"` where `[Y]` matches the term from a definition of `[X]'s negated form`. Output:

```
State 5 (Inference, DEF-EXPAND, premises=[3]):
  "Irrational means: a real number that is not expressible as p/q with integers p, q != 0."
```

**Step 6:** Now the proof-by-contradiction license from K005 (`CONTRA-SHAPE`) fires. It needs:
- A statement of the form `"assuming [H1] leads to a contradiction"`

The engine constructs the **proof goal** as an assumption. It takes the problem statement and reformulates it as an assumption for contradiction:

```
State 6 (Inference, ASSUME-FOR-CONTRA, premises=[0, 5]):
  "Assume: the square root of 2 is not irrational. 
   By State 5: Irrational means a real number not expressible as p/q with p, q integers, q != 0.
   Therefore: assume the square root of 2 is expressible as p/q with integers p, q, q != 0."
```

**Note on Step 6:** This is the critical step. The engine does NOT perform logical deduction here. It applies a **contradiction-setup pattern**: take the negation of the goal (by finding the word "irrational" in the goal and replacing it with its definition-expanded negation, using the definition in State 5). This is byte-level substitution guided by the CONTRA-SHAPE license's requirements.

---

## (c) THE ANTI-BRIDGE ARGUMENT

### The precise line

**NATIVE-ENTAIL is NOT a disguised formalizer if and only if the following holds:**

At no point does the engine construct a representation that has:
1. **Typed variables** with scope (e.g., `∀x: Prime(x) → ...`)
2. **A well-formedness grammar** that distinguishes formulas from terms
3. **Unification** in the logic-programming sense (creating substitutions)
4. **A domain-independent reasoning procedure** that operates over a formal syntax

NATIVE-ENTAIL operates over **raw bytes with pattern matching**. The "variables" are byte-span holes — they have no type, no scope, no semantics. The "reasoning" is pattern-and-rewrite. The engine never asks "is this well-formed?" — it asks "does this byte sequence match this byte pattern?"

### Three concrete cheating examples

**Cheat 1: "The engine internally converts text to Prolog clauses, then runs resolution."**

This is cheating because Prolog clauses are a formal schema: `divides(P, times(A, B))` is not bytes, it's a term with typed structure. Resolution is a formal procedure over a formal language.

**How my design avoids this:** The engine never builds terms. State 2 is literally the bytes of K202. A license matches those bytes as a pattern. The "conclusion" is built by filling a template with captured byte spans. There is no `divides(P, times(A, B))` — there is only the byte span `"p"` matched in one position and `"a*b"` matched in another.

**Cheat 2: "The engine uses a semantic parser (e.g., SPMRL) to extract a scene graph, reasons over the graph, then regenerates text."**

This is cheating because a scene graph IS a formal schema — entities with typed relations.

**How my design avoids this:** The engine has no semantic parser. It has idiom recognizers (MP-SHAPE, LEMMA-SHAPE, etc.) that match surface byte patterns. These recognizers do not build a graph — they extract holes and fill templates. The "knowledge" about what modus ponens does is encoded in the structure of the MP-SHAPE recognizer: it consumes two text states and produces the conclusion bytes. But this is a hardcoded byte-level operation, not a step through a formal calculus.

**Cheat 3: "The engine maintains a 'working memory' of propositions encoded as (relation, arg1, arg2) tuples, retrieved by keyword matching on the raw text."**

This is cheating because it smuggles in a relational schema through the back door. The keyword matching is a thin disguise over entity-relation extraction.

**How my design avoids this:** There is no working memory of tuples. There is only a stack of Text States, each a byte sequence. "Retrieval" is pattern matching: a license's premise pattern is checked against each state on the stack, byte by byte, looking for a match. No tuples, no relations, no keywords-as-entities. If the bytes `b"prime"` appear in a state, they are just bytes — not a "Prime(entity)" predicate.

### The honest residual risk

The idiom recognizers (MP-SHAPE, LEMMA-SHAPE, etc.) ARE a fixed, small "schema" — they encode the shapes of ~20 common inference patterns. This is a legitimate concern. My defense:

1. These are **surface patterns over bytes**, not abstract schemas. MP-SHAPE recognizes `from [X] and [X]=>[Y], infer [Y]` — it does not recognize `P, P→Q ⊢ Q`. The difference is that the byte-pattern version requires the inference to be **stated in the text** in a recognizable surface form. It cannot reason over unstated implicit logic.

2. The set is **closed and small** (~20). This is comparable to the number of inference patterns a child knows before learning formal logic. The question is whether ~20 surface-pattern recognizers suffice for the test battery — this is empirically testable.

3. If the test battery contains an inference whose surface form is not in the ~20, the engine **withholds** rather than hallucinating. This is honest failure.

---

## (d) CONTRADICTION DETECTION OVER RAW TEXT

### The core mechanism: Claim-Equality Checking

Two Text States **contradict** if they assert opposite things about the same entities. Since we cannot parse semantics, we use a **three-part byte-level contradiction test:**

#### Part 1: Entity Overlap Detection

Two states overlap if they share a **contiguous byte span of length ≥ 4** that is not a common English word. The engine maintains a stop-list of common English words (`the`, `is`, `a`, `that`, `for`, `with`, `and`, `or`, `if`, `then`, `not`, `there`, `exists`, `all`, `every`, `some`, ...) — approximately 300 words. Any shared byte span of ≥4 bytes that is NOT in the stop-list is a potential entity overlap.

```
fn entities_overlap(s1: &[u8], s2: &[u8]) -> Vec<(Span, Span)> {
    // Find all maximal shared substrings of length >= 4
    // Filter out substrings that are entirely common English words
    // Return matched spans
}
```

**Example:** `"p divides a*b"` and `"p divides a"` share `"p divides a"` — the entity overlap is `"p"` and `"a"`. The engine detects this.

#### Part 2: Polarity Assignment

Each state is classified as **affirmative** or **negative** by byte-level pattern matching:

```
fn polarity(bytes: &[u8]) -> Polarity {
    // Check for negative markers at the sentence/clause level:
    //   "not" preceding a verb or adjective
    //   "is not", "does not", "cannot", "no"
    //   "irrational" (contains "ir" prefix + "ational" — but this is for DEFINITION
    //     text, not for claim text; for claims, "not rational" is the form)
    //
    // More robust: detect the "X is not Y" pattern vs "X is Y" pattern
    // around the entity overlap region.
    
    // Returns: Positive | Negative | Neutral
}
```

**Example:** `"sqrt(2) is not rational"` → Negative. `"sqrt(2) is rational"` → Positive.

#### Part 3: Contradiction Rule

Two states **contradict** if and only if:

```
fn contradicts(s1: &TextState, s2: &TextState) -> bool {
    let overlaps = entities_overlap(&s1.bytes, &s2.bytes);
    for (span1, span2) in overlaps {
        let p1 = polarity_around(&s1.bytes, span1);
        let p2 = polarity_around(&s2.bytes, span2);
        if p1 == Positive && p2 == Negative { return true; }
        if p1 == Negative && p2 == Positive { return true; }
    }
    false
}
```

### Hard cases and how they're handled

**"Irrational" vs "not rational":** When State 5 says `"Irrational means: a real number that is not rational"` and a derived state says `"the square root of 2 is rational"`, the engine detects the contradiction because:
- The overlap is `"rational"` (≥4 bytes, not a stop word)
- State 5 has negative polarity around "rational" (`"not rational"`)
- The derived state has positive polarity around "rational" (`"is rational"`)

**"p divides a" vs "p does not divide a":** Direct polarity opposition on overlap `"p ... divide a"`.

**Genuine limitation:** Contradiction detection is **conservative** — it may miss contradictions expressed in very different surface forms (e.g., "2 is the only even prime" vs "3 is also an even prime"). This is acceptable because missing a contradiction leads to under-derivation, which is a lesser failure than false derivation.

---

## (e) SEARCH

### Search discipline: Bounded Iterative Deepening with License-Guided Forward Chaining

```
fn search(input: &[u8], knowledge: &[KnowledgeItem], max_steps: u32) -> Derivation {
    let mut stack: Vec<TextState> = vec![TextState::new_input(input)];
    let mut defeated: HashSet<u32> = HashSet::new(); // IDs of states marked as contradictory
    let mut step_count: u32 = 0;
    
    // Phase 0: Cite all knowledge items
    for ki in knowledge {
        stack.push(TextState::new_cite(ki));
    }
    
    // Phase 1: Iterative deepening on derivation depth
    for depth_limit in 1..=max_steps {
        // At each depth level, try ALL licenses on ALL pairs/groups of states
        let candidates = generate_candidates(&stack, &defeated, depth_limit);
        
        if candidates.is_empty() {
            break; // No more inferences possible
        }
        
        // Deterministic ordering: sort candidates by (license_id, sorted premise_ids)
        candidates.sort();
        
        for candidate in candidates {
            if step_count >= max_steps { break; }
            
            let result = apply_license(candidate, &stack);
            
            if let Some(new_state) = result {
                // Contradiction check
                let mut contradicted = false;
                for existing in &stack {
                    if !defeated.contains(&existing.id) && contradicts(&new_state, existing) {
                        // Mark the LESS-supported one as defeated
                        let loser = referee(&new_state, existing);
                        defeated.insert(loser.id);
                        if loser.id == new_state.id {
                            contradicted = true;
                            break;
                        }
                    }
                }
                
                if !contradicted {
                    new_state.depth = stack[candidate.premise_ids[0]].depth + 1;
                    stack.push(new_state);
                }
                step_count += 1;
            }
        }
        
        if step_count >= max_steps { break; }
    }
    
    // Extract the derivation path from input to goal
    extract_derivation(&stack, &defeated)
}
```

### Candidate generation

```
fn generate_candidates(stack: &[TextState], defeated: &HashSet<u32>, depth_limit: u32) -> Vec<Candidate> {
    let active: Vec<&TextState> = stack.iter()
        .filter(|s| !defeated.contains(&s.id) && s.depth < depth_limit)
        .collect();
    
    let mut candidates = Vec::new();
    
    for (i, s1) in active.iter().enumerate() {
        // Unary licenses (e.g., DEF-EXPAND, NEGATION)
        for license in unary_licenses() {
            if license.premise_pattern.matches(&s1.bytes) {
                candidates.push(Candidate {
                    license_id: license.id,
                    premise_ids: vec![s1.id],
                    priority: license.priority,
                });
            }
        }
        
        // Binary licenses (e.g., MP)
        for (j, s2) in active.iter().enumerate() {
            if i >= j { continue; }
            for license in binary_licenses() {
                if license.premises[0].matches(&s1.bytes) &&
                   license.premises[1].matches(&s2.bytes) {
                    candidates.push(Candidate {
                        license_id: license.id,
                        premise_ids: vec![s1.id, s2.id],
                        priority: license.priority,
                    });
                }
            }
        }
    }
    
    candidates
}
```

### Termination conditions

1. **Step budget exhausted:** max_steps (100) reached.
2. **Fixed point:** No new states generated in a full pass.
3. **Goal found:** A state matches the answer pattern (e.g., contains `"therefore"` + the claim from the problem, or a state is found that contradicts the negation of the goal under proof-by-contradiction mode).

### Determinism guarantee

All ordering is lexicographic on (license_id, sorted_premise_id_tuple). No randomness. Same input → same candidate order → same derivation.

### Open design question: backward vs forward

**The problem:** Forward chaining alone may not efficiently reach the goal. Consider: the engine needs to prove "sqrt(2) is irrational." Forward chaining from definitions and Euclid's lemma will generate many irrelevant divisibility facts before reaching the specific chain about 2 being prime, 2 dividing p², etc.

**Resolution A: Bidirectional with goal skeleton**

Before searching, extract a **goal skeleton** from the problem statement by pattern matching:
- "Prove that [CLAIM]" → goal skeleton is the bytes of [CLAIM]
- The engine also generates the **negation** of the goal (for contradiction): "Assume [CLAIM negated]"

Then search is forward-chaining but with **goal-directed candidate scoring**: candidates whose output template shares byte spans with the goal skeleton are prioritized (lower sort key). This is not a formal heuristic function — it's byte-overlap scoring.

**Trade-off:** This helps focus but can miss non-obvious paths. If the path to the goal requires establishing intermediate facts that share no bytes with the goal, goal-directed scoring is misleading.

**Resolution B: Pure forward with aggressive pruning**

Just forward-chain everything and rely on the bounded depth (100 steps) and contradiction detection to keep the space manageable. With ~20 licenses and ~20 initial states (input + knowledge cites), the branching factor is at most ~400 per step, but most licenses won't match most states, so actual branching is much lower.

**My recommendation:** Resolution A. The goal skeleton extraction is itself a byte-pattern operation ("Prove that [X]" → X is the goal) and doesn't require formalization.

---

## (f) CONTRADICTION-TOLERANT REFEREEING

### When a contradiction is detected

Two states S_new and S_existing contradict. The referee must decide which to **defeat** (mark as unreliable). It does NOT collapse or throw everything out.

### Referee algorithm

```
fn referee(s1: &TextState, s2: &TextState, stack: &[TextState]) -> TextState {
    let q1 = quality_score(s1, stack);
    let q2 = quality_score(s2, stack);
    
    if q1 > q2 { return s2.clone(); }  // defeat s2
    if q2 > q1 { return s1.clone(); }  // defeat s1
    
    // Tie-break: defeat the deeper one (later derivation = less certain)
    if s1.depth > s2.depth { return s1.clone(); }
    if s2.depth > s1.depth { return s2.clone(); }
    
    // Ultimate tie-break: defeat the one with higher ID (later created)
    if s1.id > s2.id { return s1.clone(); }
    s2.clone()
}

fn quality_score(s: &TextState, stack: &[TextState]) -> f64 {
    let mut score: f64 = 0.0;
    
    // Factor 1: Source quality
    match &s.source {
        StepSource::Input => score += 100.0,           // The problem itself is highest quality
        StepSource::KnowledgeCite(kid) => {
            // Knowledge items are scored by the knowledge source
            // In Round 3: all are equal (1.0 confidence)
            // But we can score by whether the item has been "challenged"
            score += 80.0 - 10.0 * times_challenged(kid, stack);
        }
        StepSource::Inference { premises, .. } => {
            // Score is min of premise scores minus depth penalty
            let min_premise_score: f64 = premises.iter()
                .map(|pid| find_state(stack, *pid).quality)
                .fold(f64::INFINITY, f64::min);
            score += min_premise_score - (s.depth as f64 * 2.0);
        }
    }
    
    // Factor 2: Corroboration
    // Count how many independent paths lead to the same conclusion
    // (states with matching output bytes derived from disjoint premise sets)
    let corroboration = count_independent_support(s, stack);
    score += corroboration as f64 * 15.0;
    
    // Factor 3: Specificity
    // More specific claims (more unique bytes) are harder to derive
    // and thus more trustworthy when derived correctly
    let uniqueness = unique_byte_ratio(&s.bytes);
    score += uniqueness * 5.0;
    
    score
}
```

### Key properties

1. **The problem statement always wins** (score 100). This prevents the engine from defeating the problem itself.
2. **Direct knowledge citations always beat derived states** (score 80 vs <80). This means a contradiction between a knowledge cite and a derived state defeats the derived state — exactly right for false-rule injection scenarios.
3. **Corroboration breaks ties.** If the same conclusion is reached via two independent paths (disjoint premise sets), it's likely correct. A state derived from a single potentially-false rule has no corroboration.
4. **Depth penalizes.** Deeply derived states are less trusted than shallow ones, all else equal.

### False-rule injection scenario

Suppose K202* (false) says: `"if p is prime and p divides a*b, then p divides a AND p divides b."`

This is subtle — the "AND" should be "OR". If the engine cites K202* and derives `"p divides a AND p divides b"` for some specific case, and then later (from a different path using correct knowledge) derives `"p does not divide a"` for that same case, the contradiction is detected. The referee:

- K202* citation: quality 80 (knowledge cite, unchallenged)
- Derived contradiction from correct path: quality depends on premise chain

In this case, the engine might not detect the error until much later. This is a genuine limitation — the engine is **not guaranteed to detect false rules proactively**. It detects them only when they produce a contradiction with something else on the stack.

---

## (g) HONESTY: WITHHOLDING

### The withholding rule

```
fn should_withhold(state: &TextState, stack: &[TextState], goal: &[u8]) -> bool {
    // Rule 1: Never derive if no license pattern matches
    // (This is structural — if no idiom recognizes the inference shape, we can't fire it)
    
    // Rule 2: Withhold if the only matching license requires holes that
    // are ambiguous (multiple possible spans in the premise match the hole)
    if has_ambiguous_holes(state) { return true; }
    
    // Rule 3: Withhold if the conclusion would assert something about
    // an entity not present in any premise
    if introduces_unbound_entity(state, stack) { return true; }
    
    // Rule 4: Withhold if the derivation depth exceeds a confidence threshold
    // and no corroboration exists
    if state.depth > 10 && count_independent_support(state, stack) == 0 {
        return true;
    }
    
    false
}
```

### What stops hallucination

1. **Pattern matching is strict.** A license fires only if its byte patterns match. If the bytes don't match, no step is generated. The engine cannot "imagine" a step — it either matches or it doesn't.

2. **Holes must be bound.** Every hole in the output template must be bound to an actual byte span from a premise. The engine cannot output bytes that don't come from somewhere on the stack.

3. **The derivation record is full.** Every step records its license, its hole bindings, and its premise IDs. A grader can verify that the bindings are valid byte spans from the cited states and that the license pattern is valid. There is no room for hallucination in the record — only in the license firing, which is mechanical.

4. **Withholding is the default.** The engine starts from the assumption that it cannot derive anything. A step must be explicitly licensed. No license matches → no step → honest abstention.

---

## (h) WHITE-BOX FAILURE ANALYSIS

### Failure Mode 1: Vocabulary Gap in Pattern Matching

**Symptom:** The engine encounters an inference whose surface form doesn't match any of the ~20 idiom recognizers. For example, a problem that states a fact in an unusual phrasing: `"No integer p exists such that p squared divided by 2 leaves a remainder of 1."` The standard LEMMA-SHAPE expects `"if [X] then [Y]"` but this is phrased as a negated existential.

**Mechanism-level reason:** The MP-SHAPE, LEMMA-SHAPE, etc. are fixed byte-pattern templates. If the knowledge or problem uses a syntactic variant not in the template set, the engine silently fails to recognize the inference opportunity and withholds. The stack reaches a fixed point with no contradiction and no proof.

**Classification:** **Architecture failure.** The idiom set is too small or too rigid. The engine's "vocabulary" of inference shapes is the binding constraint.

**Mitigation (partial):** Expand the idiom set, but this risks approaching a parser (cheating). A principled limit: each idiom must match a **contiguous literal pattern** in the knowledge text — the engine does not rearrange or rephrase. This keeps it byte-level.

### Failure Mode 2: Polarity Detection Failure

**Symptom:** The engine cannot detect a contradiction because the negation is expressed in a form the polarity detector doesn't recognize. For example: `"The square root of 2 is not expressible as a ratio of integers"` vs `"The square root of 2 is the ratio of two integers."` The polarity detector looks for `"not"` adjacent to the overlap, but here the negation is embedded in a complex predicate `"not expressible as"` — the detector might only flag the simple `"not X"` pattern.

**Mechanism-level reason:** The polarity function is a heuristic that looks for `"not"`, `"no"`, `"cannot"` etc. near the overlap region. Complex negation forms (`"fails to"`, `"contradicts"`, `"is impossible that"`) may be missed. When polarity detection fails, contradictions are missed, and the engine may derive contradictory states without detecting the problem.

**Classification:** **Architecture failure.** Polarity detection is fundamentally a natural language understanding task, and doing it byte-level is inherently lossy.

**Mitigation:** A broader set of negative marker patterns (at least 50), but the long tail of English negation makes this incomplete. This is a genuine hard problem.

### Failure Mode 3: Hole Ambiguity Explosion

**Symptom:** A license pattern has a hole that matches multiple non-overlapping spans in a premise. For example, the modus ponens license applied to a state that contains two different `=>` arrows: `"if A then B and if C then D"`. The hole for the antecedent could match `"A"` or `"C"`, and the hole for the consequent could match `"B"` or `"D"`. The engine must try all combinations, but it also must withhold if the correct binding is unclear.

**Mechanism-level reason:** When a hole matches multiple spans, the engine generates **all** bindings (deterministic, since it tries them in byte-offset order). This causes a combinatorial explosion: N possible bindings for M holes produces N^M candidates. For deeply nested patterns, this can exhaust the 100-step budget on useless variants before reaching the productive one.

**Classification:** **Knowledge diet failure.** The knowledge items are too ambiguous in their surface form. Better-written knowledge items (e.g., separating facts clearly with sentence boundaries) would reduce ambiguity. But the engine cannot control how knowledge is written.

**Mitigation:** Limit hole ambiguity to ≤3 bindings per hole. If exceeded, withhold for that license match. This trades coverage for tractability.

---

## (i) KILL BARS

Three falsifiable kill bars for H-NATIVE as tested through NATIVE-ENTAIL:

### Kill Bar 1: The Definition Expansion Test

**Battery:** 10 word problems that require only expanding definitions and applying one inference rule (modus ponens or proof by contradiction), where the definitions and rule are given in the knowledge store.

**Kill bar:** The engine must solve ≥7/10 correctly with zero false derivations. Failure (score < 7 or any false derivation) falsifies the claim that byte-level pattern matching can perform even single-step inference.

**Rationale:** This is the minimal test of the engine. If it cannot expand `"rational means p/q"` and apply modus ponens, native reasoning over bytes is dead.

### Kill Bar 2: The False-Rule Resilience Test

**Battery:** 10 problems, each with one knowledge item silently replaced by a plausible false version (e.g., Euclid's lemma with AND instead of OR).

**Kill bar:** On ≥8/10, the engine must either (a) arrive at the correct answer despite the false rule, or (b) explicitly cite the contradiction and abstain. A false derivation (using the false rule to reach a wrong conclusion) on ≥3/10 falsifies the claim that byte-level contradiction detection can handle adversarial knowledge.

**Rationale:** This tests the core promise of contradiction-tolerant refereeing.

### Kill Bar 3: The Multi-Step Chain Test

**Battery:** 10 word problems requiring 5–15 inference steps (e.g., the standard irrationality of sqrt(2) proof, the pigeonhole principle applied to a concrete scenario, etc.).

**Kill bar:** The engine must solve ≥5/10 within the 100-step budget with a valid derivation (each step verified by the grader). Failure (score < 5) falsifies the claim that byte-level forward chaining with ~20 idiom recognizers can perform genuine multi-step mathematical reasoning.

**Rationale:** This tests the search and the sufficiency of the idiom set for extended reasoning chains.

---

## Summary of the open design questions

1. **Idiom set size and coverage:** ~20 is my estimate for what's needed, but this is a guess. The trade-off is coverage vs. principled restriction. More idioms = more coverage but closer to a parser. Resolution: empirically calibrate on the Round 3 battery.

2. **Backward vs. forward search:** Resolution A (goal-directed scoring via byte overlap) is recommended but may fail on problems where intermediate facts share no bytes with the goal. Resolution B (pure forward) is robust but may be too slow within 100 steps. Resolution: implement A first, fall back to B if A fails within 50 steps.

3. **Contradiction detection sensitivity:** The shared-substring approach is conservative. More aggressive detection (e.g., treating antonyms as implicit contradictions) would catch more but risks false positives. Resolution: start conservative, measure false negatives on the battery, expand only if needed.

The core claim of H-NATIVE is testable: if NATIVE-ENTAIL passes the three kill bars, there is evidence that byte-level native reasoning works for this class of problems. If it fails, the failure mode analysis tells us precisely which aspect of native reasoning is insufficient — whether it's the pattern vocabulary, the contradiction detection, or the search — and that tells us what H-NATIVE must mean (if anything) going forward.
EXIT:0
