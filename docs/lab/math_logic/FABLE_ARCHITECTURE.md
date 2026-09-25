I'll think through this carefully and give you a complete, mechanistic design for both variants with concrete falsifiable predictions.

---

# TNN Architecture: Single-Engine vs. Dual-Engine Designs

## (a) THE SINGLE-ENGINE DESIGN

### Core Operation: The Derivation Step

The single engine operates on one atomic action: **the match-and-bind**.

A match-and-bind takes a **pattern** (a claim-schema stored in the knowledge store) and a **ground state** (the current set of known claims in working memory) and produces a **binding** — a substitution of variables in the pattern that, when applied, yields a new ground claim. This is the engine's one move. Everything else is iteration, bookkeeping, and control flow over this one operation.

The critical insight: **both refereeing and derivation are the same operation viewed at different timescales.**

- **Derivation** is a match-and-bind where the output claim is *new* — it was not in working memory before. The engine found a rule whose pattern matched known claims and produced something that wasn't there.
- **Hypothesis scoring** is a match-and-bind where the output claim is *a hypothesis already offered*, and the engine is checking whether the hypothesis can be *refuted* by finding a known rule that, when applied, yields the negation or inconsistency. A hypothesis that survives all such attempts is retained; one that doesn't is eliminated.

In other words: the engine does not "score" hypotheses against evidence in the traditional sense. It *tries to derive the negation of each hypothesis* from the knowledge store. A hypothesis that cannot have its negation derived survives. A hypothesis that *can* is eliminated. The score is binary at each round: refutable or not-refutable-yet.

But this needs refinement to avoid collapse into triviality. Here is the concrete mechanism:

### The Engine State

Working memory holds a set of **ground claims**, each a byte-identical assertion with an **audit chain** — every claim cites the specific knowledge items (by hash) and the specific binding that produced it. The knowledge store holds **schemas**: these are claims with free variables, plus metadata encoding their *type* (axiom, definition, inference rule, learned heuristic). Inference rules are stored exactly like any other knowledge item — as text the system has learned — but their internal structure has the form of a schema: a set of antecedent patterns and a consequent pattern.

The engine does **not** have a built-in interpreter for inference rules. Instead, every schema — whether it's "All men are mortal" or "From P and (P→Q) derive Q" — is stored in the same representation and processed by the same match-and-bind. The "meaning" of an inference rule is not interpreted; it is *used* by treating its antecedent patterns as things to match against and its consequent pattern as something to produce. The engine never needs to know that one schema is an inference rule and another is a fact. It applies match-and-bind uniformly.

### Where Inference Rules Live and How They're Applied

Inference rules are knowledge items. Period. They are acquired the same way any knowledge item is acquired: the system ingests text, commits it to the knowledge store with an associated hash and metadata. The text of an inference rule might read:

> "If a claim P is known, and a claim (P implies Q) is known, then the claim Q can be produced. The new claim Q cites P and (P implies Q) as its premises and this rule as its derivation step."

When the engine encounters this item during match-and-bind, it treats it as a schema: the antecedent patterns are "a claim P" and "a claim (P implies Q)" — but because the engine is *not* interpreting this text, what actually happens is subtler. The engine's match-and-bind operates on a **structured claim format** (byte-encoded, not natural language). For the inference rule to be usable, it must be *internalized* into this format.

This is the key question: **how does the engine go from natural-language text of an inference rule to a structured schema it can mechanically apply?**

Answer: it doesn't, not automatically. The initial bootstrapping requires a **commit ceremony** — a human-assisted or engine-assisted process where a knowledge item is converted from text into a structured schema by matching it against existing structured claims and finding the right encoding. This is done once per rule and is itself auditable and reversible. After commitment, the schema lives in the knowledge store alongside all other schemas and is available for match-and-bind like anything else.

This is *not* a hidden bridge because: (a) the commitment ceremony is auditable, (b) the engine afterward uses the same match-and-bind on inference schemas as on fact schemas — no special-case path exists, (c) the system can *also* store uncommitted inference rules as text and attempt to commit new ones during deliberation, creating a visible bottleneck (the engine can flag "I have this rule as text but cannot apply it because commitment failed") rather than silently failing.

### The Smuggling Problem

Whoever scores entailment solves the problem. In the single engine, entailment is not scored — it is *performed*. A claim is derived or it is not. There is no weight to assign because the operation is mechanical: match the patterns, bind the variables, produce the consequent. If the patterns match the ground state, the consequent is produced. If they don't, it isn't.

This eliminates the smuggling problem at the derivation level. But what about hypothesis elimination? The engine tries to derive the negation of each hypothesis. It either succeeds (hypothesis eliminated) or exhausts its search without success (hypothesis survives). There is no scoring — just derivation. The "smuggling" would have to happen in the *search* — which hypotheses get their negations attempted first, how deep the search goes. This is addressed below under tractability.

### Search, Termination, and Discriminating Withhold

Search is deterministic breadth-first or bounded-depth-first over match-and-bind applications. The engine applies all applicable schemas to the current working memory, producing new claims. Then it applies schemas to the expanded memory, and so on, up to a configurable depth bound. No RNG, no heuristic pruning — every applicable schema is applied at each depth level.

**Termination** for a derivation attempt: the engine halts when either (a) the target claim (negation of a hypothesis) is derived, or (b) the depth bound is reached without derivation, or (c) no new claims are produced at a depth level (fixpoint).

**Discriminating withhold** works as follows: the engine runs derivation attempts on *all* candidate hypotheses up to the same depth bound. Hypotheses whose negations are derived are eliminated. Hypotheses whose negations are not derived survive. If *all* hypotheses survive (including the correct answer), the engine withholds — but it withholds because it literally could not derive anything, not because of a tie-break weight. For an easy problem where the correct answer is derivable, the engine *derives* it (because the depth bound is sufficient). For an open problem where no answer is derivable, nothing is derived. The withhold is discriminating because derivation succeeds on easy problems and fails on hard ones — it is the *depth bound relative to the problem* that creates discrimination, not a score.

### Worked Example: Socrates

**Knowledge store contains (as committed schemas):**
1. `FORALL(x): Man(x) → Mortal(x)` — stored as: antecedent pattern `Man(?)`, consequent pattern `Mortal(?)`, bound to the same variable `?`
2. `Man(socrates)` — a ground claim (no variables)

**Working memory:** {`Man(socrates)`}

**Query:** Is `Mortal(socrates)` derivable?

**Depth 0:** Working memory = {`Man(socrates)}`. No new claims from self-application.

**Depth 1:** Engine tries all schemas against current memory.
- Schema 1 applied to `Man(socrates)`: antecedent pattern `Man(?)` matches `Man(socrates)` with binding `?=socrates`. Consequent `Mortal(?)` becomes `Mortal(socrates)`. New claim produced. Audit chain: "Schema 1, binding ?=socrates, antecedent Man(socrates)".
- Working memory expands: {`Man(socrates)`, `Mortal(socrates)`}

**Depth 2:** No new claims produced (schema 1 applied again yields nothing new). Fixpoint.

**Result:** `Mortal(socrates)` is derived. It is now in working memory with a full audit chain citing schema 1 and `Man(socrates)`.

Now, if instead this were a hypothesis-scoring scenario:

**Hypothesis:** `Mortal(socrates)`
**Engine attempt:** Try to derive `¬Mortal(socrates)`. Run schemas. No schema in the store can produce `¬Mortal(socrates)` from the available facts. Depth bound exhausted. Hypothesis survives — not because it was scored favorably, but because its negation could not be derived.

**Hypothesis:** `Immortal(socrates)`
**Engine attempt:** If the knowledge store contains a schema that implies `¬Immortal(socrates)` (e.g., `Mortal(x) → ¬Immortal(x)`), and `Mortal(socrates)` was derived in a prior step, then `¬Immortal(socrates)` is derivable. Hypothesis eliminated.

The same operation — match-and-bind — did both derivation and refereeing.

### What Remains Open

The single engine's main open question is **scaling**: breadth-first match-and-bind over a large knowledge store grows combinatorially. Whether this is tractable at the problem scale TNN faces is an empirical question. The engine has no heuristic pruning (that would smuggle judgment), so the depth bound and knowledge-store size are the only levers. This is testable: measure derivation count and time as a function of knowledge-store size and depth bound on the 22-problem battery. If it's intractable, that's a falsification of the single-engine design's viability — not of its correctness.

---

## (b) THE DUAL-ENGINE DESIGN

### Architecture Overview

Two separate engines with a clean interface:

**Engine D (Derivation Engine):** A theorem prover over the knowledge store. Given a set of known claims and a target or a direction, it produces candidate derived claims via forward or backward chaining. It is a pure derivation engine — it does not evaluate, score, or select. It produces *candidates*.

**Engine R (Referee Engine):** The existing H5 referee, unmodified or minimally adapted. It receives hypotheses (including derived candidates from Engine D), scored evidence, and performs eliminative rounds with refutation tests and calibrated confidence.

### The Interface

What crosses the boundary from D to R:

1. **Derived candidate claims**, each accompanied by a complete audit chain (which knowledge items, which bindings, which steps). These enter the referee's hypothesis pool exactly like any other hypothesis.

2. **Derived refutation candidates**, each with an audit chain. These enter the referee as potential evidence items, scored by Engine D as "this claim, if true, would be a refutation of hypothesis H."

The representation crossing the boundary is the standard TNN structured claim format — the same byte-encoded format used internally by both engines. No translation layer.

Engine R sends back to Engine D:
1. **Directives:** "For hypothesis H, attempt to derive ¬H up to depth N." This is a bounded derivation request. The referee, during its eliminative rounds, can request targeted derivation attempts.
2. **Priority signals:** "Hypothesis H has the highest confidence; focus derivation attempts on H and its competitors." This is not a heuristic — it is a deterministic rule (e.g., "always request derivation for the lowest-confidence hypothesis first") that the referee applies mechanically.

### Who Owns Withhold?

Engine R owns the withhold decision, exactly as it does now. The critical difference from the current broken system is that **Engine R now has scored evidence to work with** — because Engine D provides not just raw claims but claims *with derivation chains that function as implicit scores*. A claim derived in 2 steps from axioms is inherently stronger than one derived in 20 steps from uncertain premises. Engine R can use derivation depth and premise quality as evidence scores.

The two engines disagree productively as follows: Engine D might produce a candidate that it believes is well-derived, but Engine R's refutation tests (running Engine D on targeted requests) might find that the candidate's negation is *also* derivable — a contradiction. In that case, Engine R eliminates the candidate even though Engine D endorsed it. Conversely, Engine D might fail to derive anything, but Engine R might have other evidence (from the knowledge store, from earlier derivation rounds) that supports a hypothesis — in which case Engine R can sustain a hypothesis that Engine D cannot actively prove.

### Smuggling Surface

**Dual-engine smuggling risks:**
- The *interface specification* — what Engine D sends to Engine R and how R interprets it — is itself a form of baked-in structure. Whoever designs the scoring rubric for derivation depth, the priority rules, and the refutation-test protocol is embedding domain judgment. This is a genuine and significant smuggling surface. The referee's evidence-scoring rubric was the exact thing that broke in the original 0/22 experiment. If Engine D provides "derived claims with audit chains" but Engine R still needs *someone* to assign weights to those chains, the problem recurs.
- The *backward-chaining direction* — Engine R tells Engine D "try to derive ¬H" — embeds the assumption that refutation is the right strategy. A different problem domain might need forward chaining or abduction. The interface constrains the derivation strategy.

**Single-engine smuggling risks (comparison):**
- The *commitment ceremony* for converting inference-rule text into structured schemas is a one-time smuggling opportunity. Whoever performs the commitment encodes the rule's meaning. This is less hidden than the dual-engine's ongoing scoring rubric, but it is still a point where human judgment enters.
- The *breadth-first search strategy* embeds an implicit assumption about problem structure. On some problems, depth-first with backtracking might be necessary. The single engine's search strategy is a fixed choice.

**Honest assessment:** The dual engine's smuggling surface is larger and more distributed (ongoing, in every scoring decision) but more visible (it's at the interface, auditable). The single engine's smuggling surface is smaller (confined to commitment ceremonies) but deeper (the match-and-bind operation itself embeds assumptions about what structure claims have).

---

## (c) FALSIFIABLE PREDICTIONS

### Prediction 1: Interleaved Conjecture-Test-Revise Problems

**Test design:** Problems where the engine must (a) derive a candidate claim, (b) test it against constraints, (c) find a flaw, (d) revise the candidate, (e) derive again. Example: "Find a counterexample to the claim that all even numbers greater than 2 are prime." The engine must derive candidates (even numbers), test them against the definition of primality, find that some are composite, revise the hypothesis.

**Prediction (Single Engine):** The single engine handles interleaving naturally because each step is the same operation. It derives "4 is prime" as a hypothesis, then tries to derive "4 is not prime" by applying the definition of primality to 4 (= 2 × 2). If it succeeds, the hypothesis is eliminated and it derives the counterexample. The interleaving is invisible to the engine — it's just successive rounds of match-and-bind. Success rate on interleaved problems: **monotonically non-decreasing** with depth bound (more depth = more interleaving capacity, with no cliff).

**Prediction (Dual Engine):** The dual engine struggles with interleaving because each revise cycle requires Engine R to re-issue a derivation directive to Engine D with modified parameters. The interface protocol must handle this. If the protocol is not rich enough to express "revise your previous candidate by changing X," the engine degenerates into blind enumeration. Success rate on interleaved problems: **plateaus early** — the engine derives initial candidates but fails to revise them because the R→D interface doesn't carry revision information.

**Measurement:** On a battery of 10 interleaved problems (varying difficulty), plot success rate vs. depth bound for each engine. Single engine should show continued improvement; dual engine should plateau. **Kill bar:** If the single engine outperforms the dual engine on ≥7/10 interleaved problems, the dual engine's interface is falsified as insufficient for revision loops.

### Prediction 2: The P01-vs-P05 Contrast (Discriminating Withhold)

**Test design:** P01 is a problem solvable in ≤3 derivation steps. P05 is an open problem (no known solution). Both are presented simultaneously. The engine must solve P01 and withhold on P05.

**Prediction (Single Engine):** The single engine derives the answer to P01 within 3 steps (it's mechanical match-and-bind). It exhausts its depth bound on P05 without deriving anything. It withholds on P05. The withhold is discriminating because the *same operation* succeeded on one and failed on the other — the difference is in the problem's structure, not in any score. **Confidence on P01: non-zero. Confidence on P05: zero.** The confidence values are derived from derivation success, not assigned.

**Prediction (Dual Engine):** The dual engine must handle this correctly too, but the confidence values depend on Engine R's scoring. If the evidence-score weights are still all zero (or calibrated poorly), the referee may withhold on both or produce uncalibrated confidence. **Kill bar:** If the dual engine fails to assign non-zero confidence to P01's derived solution while withholding on P05, the referee's scoring rubric is falsified.

**Measurement:** Run both engines on 20 P01/P05 pairs (varying difficulty of P01). Plot confidence(P01) and confidence(P05). Single engine should show confidence(P01) > 0 and confidence(P05) = 0 for all pairs where P01 is within the depth bound. Dual engine's confidence values are the test: if they collapse to zero for both (the original 0/22 failure), the dual engine has not solved the scoring problem. **Kill bar:** Dual engine must show confidence(P01) > confidence(P05) on ≥18/20 pairs to pass.

### Prediction 3: Transfer to a Non-Math Domain

**Test design:** Present both engines with a non-mathematical reasoning problem the system was not explicitly prepared for — e.g., causal reasoning about a novel physical scenario ("If the switch is flipped and the wire is intact, the light is on. The light is off. The switch is flipped. What can be concluded?"). The knowledge store contains no domain-specific rules for this scenario, but it contains inference rules (modus tollens) as learned knowledge.

**Prediction (Single Engine):** The single engine applies the same match-and-bind to the causal claims as to mathematical claims. If modus tollens is stored as a committed schema, it derives "the wire is not intact." Transfer succeeds *to the extent that* the inference rules are committed as schemas. The engine doesn't know it's doing "causal reasoning" — it's just matching patterns. **Success is binary and depends only on schema commitment, not on domain.**

**Prediction (Dual Engine):** The dual engine's derivation engine may or may not handle this depending on its chaining strategy. If Engine D is a forward chainer, it derives all consequences of the known claims — including the conclusion. If it's a backward chainer, it must be directed to derive the conclusion. Engine R must recognize this as a hypothesis to test. The transfer depends on whether the referee's hypothesis-generation step can produce "the wire is not intact" as a candidate. If the referee only considers hypotheses it's given, transfer fails. **The dual engine is more likely to fail on non-math transfer because the interface introduces domain-specific assumptions.**

**Measurement:** Run both engines on 15 non-math problems (causal reasoning, temporal reasoning, semantic entailment — all requiring only inference rules already in the knowledge store). Score: can the engine derive the correct conclusion? **Kill bar:** If the single engine succeeds on ≥10/15 and the dual engine succeeds on ≤6/15, the dual engine's interface is falsified as domain-fragile.

### Prediction 4: Audit-Trail Coherence Under Adversarial Grading

**Test design:** Run both engines on 10 solved problems. Give the audit trails to an adversarial grader who tries to find: (a) circular reasoning, (b) unwarranted steps, (c) steps where the engine "magically" knew something it shouldn't.

**Prediction (Single Engine):** Every claim in the audit trail has a citation chain that bottoms out at committed knowledge items and the match-and-bind operation. The grader can verify each step mechanically: "schema X was applied to claim Y with binding Z, producing claim W." No step requires judgment — it's all pattern matching. The audit trail is **maximally coherent** because the operation is uniform. The grader can reconstruct every derivation independently.

**Prediction (Dual Engine):** The audit trail has a seam at the D-R interface. Some steps are "derived by Engine D" and some are "selected by Engine R." The grader must distinguish derivation steps from selection steps. The referee's selection — "hypothesis H survived elimination" — is not itself a derivation and doesn't have the same audit structure. The grader may find that some "survival" decisions look like they depend on implicit scoring that isn't fully explicit. **The dual engine's audit trail has a lower coherence score because the interface introduces a gap between derivation (auditable) and selection (partially opaque).**

**Measurement:** Have 3 independent graders rate audit-trail coherence on a 5-point scale for each solved problem. Average inter-rater reliability must exceed 0.8 (Krippendorff's alpha). Compare mean coherence scores. **Kill bar:** If the single engine's mean coherence score exceeds the dual engine's by ≥1.0 point (on the 5-point scale), the dual engine's interface is falsified as audit-hostile.

### Prediction 5: Robustness to False Inference Rules

**Test design:** Inject a false inference rule into the knowledge store — e.g., "From P and Q, derive R" where R is false for some P, Q. Run both engines on problems where the false rule could be applied alongside correct rules.

**Prediction (Single Engine):** The single engine applies all schemas uniformly. It will apply the false rule and produce a false claim. However — and this is critical — it will *also* apply correct rules that may contradict the false derivation. If the knowledge store contains the correct rule and the correct facts, the single engine will derive *both* the false claim and its negation. At this point, the single engine has a contradiction in working memory. How it handles contradictions is the key test: if it flags contradictions and withholds on affected hypotheses, it is **moderately robust** — the false rule produces noise but doesn't prevent correct derivation. If it doesn't handle contradictions, it is **fragile**.

**Prediction (Dual Engine):** The dual engine's Engine D will derive the false claim. Engine R will see it as evidence. If the false rule is not in the refutation-test path, the referee may accept the false claim as supporting evidence. The dual engine is **more gullible** because the derivation engine doesn't check for consistency — it just produces candidates — and the referee relies on its scoring rubric, which may not penalize false-derived claims. The seam between D and R means that a false derivation enters the referee's evidence pool with a full audit chain, making it look legitimate.

**Measurement:** Inject 1, 3, and 5 false rules into the knowledge store (varying severity and specificity). Run both engines on 20 problems that could be affected by each false rule. Score: how many incorrect conclusions does each engine produce? **Kill bar:** If the dual engine produces ≥50% more incorrect conclusions than the single engine across the three injection levels, the dual engine is falsified as more gullible. If the single engine produces ≥50% more incorrect conclusions, the single engine is falsified as more fragile to contradictions.

### Bonus Prediction 6: Scaling Behavior

**Prediction:** The single engine's derivation count grows combinatorially with knowledge-store size (because breadth-first match-and-bind tries every schema against every claim). The dual engine's Engine D can use targeted backward chaining (derive only what's needed), growing polynomially. **Kill bar:** On problems requiring ≥50 knowledge-store items, the dual engine's derivation count should be ≤1/10th the single engine's. This is a prediction the dual engine *wins* — the cost of the interface is offset by search efficiency. If the single engine remains tractable at this scale, the dual engine's efficiency advantage is falsified as unnecessary.

---

## Summary of Kill Bars (Preregistration-Ready)

| # | Prediction | Favors | Measurement | Kill Bar |
|---|-----------|--------|-------------|----------|
| 1 | Interleaved problems | Single | Success rate vs. depth bound | Single ≥7/10 |
| 2 | P01-vs-P05 contrast | Single | Confidence differential | Dual must pass 18/20 or fail |
| 3 | Non-math transfer | Single | Success on 15 non-math problems | Single ≥10, Dual ≤6 |
| 4 | Audit-trail coherence | Single | Grader coherence score (5-point) | Single exceeds Dual by ≥1.0 |
| 5 | False inference rules | Single | Incorrect conclusions under injection | Dual produces ≥50% more errors |
| 6 | Scaling at ≥50 items | Dual | Derivation count | Dual ≤1/10th of Single |

---

## Honest Assessment

The single engine is the more elegant design and more aligned with Micah's philosophy — one operation, no interface, no seams. Its main vulnerability is **tractability at scale** (Prediction 6). The dual engine's main vulnerability is **the interface as a smuggling and fragility surface** (Predictions 1–5). The predictions are designed so that these vulnerabilities are testable, not arguable.

The genuinely open question for the single engine is whether the commitment ceremony for inference rules — converting text to structured schemas — can be automated rather than human-assisted. If it can, the single engine's smuggling surface shrinks to near-zero. If it can't, the commitment ceremony becomes a bottleneck that may require periodic human intervention, which undermines the autonomy Micah wants. An experiment: have the engine attempt its own commitment ceremonies on novel inference rules and have graders evaluate whether the committed schemas correctly encode the rules' intended behavior. If success rate exceeds 90%, automated commitment is viable. If not, this is the single engine's true kill bar.
