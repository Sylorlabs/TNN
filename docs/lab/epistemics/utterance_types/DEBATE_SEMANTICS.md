# H7 Epistemic Semantics Debate — Record & Synthesis

**Program:** H7 utterance-type learning (Micah's hypothesis: TNN takes facts first,
then learns utterance types — "sarcasm is this and is used like this" — as a LEARNED
layer, never hardcoded; kill bar: ZERO LEAKAGE of constructed content into factual recall).
**Crew:** H7 Crew 3 of 4 — structured debates, Sol vs Muse.
**Date:** 2026-09-23.
**Status:** Debate record + synthesis for the mechanism crew (what to build) and the
red-team crew (what to attack). Not frozen law — mechanism choices below are
recommendations with preregistered head-to-heads where the debate did not settle.

## 0. Provenance and method

- **Debaters.** "Sol": outside voice via UnoRouter (`custom.unorouter` connector).
  `gpt-5.6-sol` returned null choices (0 completion tokens) on 3 of 5 opening prompts
  — provider-side flakiness, retried twice — so those three openings were taken on
  `grok-4.6`, also a listed UnoRouter model. R2/R3 openings and all five Round-2
  responses are `gpt-5.6-sol` except R1/R4/R5 openings (`grok-4.6`). One Round-2 call
  (R2) hit an HTTP 524 provider timeout on first attempt and succeeded on retry.
- **Muse side.** This crew is a depth-2 subagent and cannot spawn child subagents, so
  the Muse-side positions were argued directly by the crew lead (a Muse-family agent),
  steelmanned, in two rounds against Sol. Recorded below as "Muse".
- **Format.** Two rounds per resolution. Round 1: Sol opening statement for its assigned
  side. Muse rebuttal (opposite side, steelmanned). Round 2: Sol answers the strongest
  point, states explicit concessions, and names the remaining unresolved split.
- **Side assignments** (each side argued both FOR and AGAINST across resolutions):

| # | Resolution (short) | Sol | Muse |
|---|---|---|---|
| 1 | Hypothetical = belief with a modal flag | FOR | AGAINST (partitioned construction) |
| 2 | Utterance-type is a property of USE | AGAINST (type inheres in content) | FOR (use-based) |
| 3 | Quotation boundary is airtight | FOR | AGAINST (porous boundary) |
| 4 | Hard partitions suffice for roleplay | AGAINST (partitions leak) | FOR (partitions can suffice) |
| 5 | A learned "sarcasm" rule is figure-it-out machinery, not the rigid-policy trap | FOR | AGAINST (trap risk is real) |

- **Standing laws both sides argued under.** No randomness in decision paths (deterministic
  given state, byte-identical reruns); everything reversible by the system itself;
  outcomes settled by preregistered experiment, never authority; Micah's figure-it-out
  law (TNN is an it-can-figure-it-out machine, not a needs-policy-for-every-edge-case
  machine; figure-it-out wins ties).

---

## 1. What does it mean to "believe" a hypothetical?

**Resolution:** "To 'believe' a hypothetical is to hold a BELIEF WITH A MODAL FLAG
attached — not a partitioned construction, not a third knowledge kind."
Sol FOR, Muse AGAINST.

### Sol opening (FOR flag-beliefs)

- Beliefs are the system's sole knowledge kind. A hypothetical is a belief carrying a
  modal flag (HYPO, possibly nested). Ontological parsimony: one proposition type plus
  composable operators, not extra stores or kinds.
- The flag is a first-class tag on the belief record; it composes by stacking
  (HYPO(HYPO(P))) or conjunction with other modalities (QUOTE(HYPO(P))).
- Downstream the flag is a gate, not a wall: inference applies only within compatible
  flag contexts or via explicit lifting rules; action selection treats HYPO-flagged
  content as non-actual and withholds real-world effectors; consolidation writes the
  tagged record so replay reconstructs exact modality.
- Partitions fail composition (how do two isolated worlds merge when a nested
  hypothetical appears inside a quote?) and invite leakage at every boundary crossing.
  A third knowledge kind multiplies ontology and still needs a flag-like interface.
- Mechanism: represent a flagged belief as (proposition, ModalStack, provenance,
  timestamp); ModalStack is an ordered list of atoms (HYPO, QUOTE, ROLE, ...).
  Operations gated by the flag: (1) factual recall drops records with non-empty stacks,
  (2) forward chaining fires only when antecedent/consequent stacks unify,
  (3) action predicates return non-executable for HYPO-bearing goals. The flag is
  copied, never stripped, unless an explicit resolution operator fires; the write path
  is flag-preserving; the flag dies only by an explicit logged operator
  (e.g. "this hypothetical was later confirmed"), never by accident or background process.
- Steelman of partitions: isolation is cheaper than tagging; a separate possible-world
  store garbage-collects independently, cannot contaminate the fact base by
  construction, makes leakage tests trivial; maps onto modal-logic tableaux proof theory.
- Mind-changer: preregistered head-to-head on nested-hypothetical composition plus
  leakage (10k synthetic dialogues with quotes-in-hypos-in-jokes; measure modal-stack
  reconstruction fidelity after consolidation-and-replay, and zero leakage into unflagged
  factual queries). If partitions win both, the flag semantics lose.

### Muse rebuttal (FOR partitioned construction)

- The flag is a partition in disguise, and a worse one: every factual lookup must
  inspect every record's ModalStack — a global tax, N gates that can each fail, versus
  one wall. "Gates, not walls" means more failure points, not fewer.
- HYPO(HYPO(P)) stacking is syntactic bookkeeping, not semantics. Genuine nested
  hypotheticals need world-accessibility structure, which partitions give structurally
  and tableaux give natively. The flag design admits inventing unification/lifting rules
  "from scratch" — deferred complexity, not parsimony.
- The flag's death rule ("dies only by an explicit, logged operator") is itself a rigid
  global policy. Partitions garbage-collect for free: drop the world, the hypothetical
  is gone, no per-record stack audit.
- Concession: naive partitions handle nested quote-in-hypo merging awkwardly. But
  import/export across world boundaries is a small set of explicit, logged operators —
  fewer than per-lookup flag checks, and each auditable. Rare-and-logged beats
  ubiquitous-and-hoped.
- Mechanism implication: worlds as first-class stores with explicit, reversible
  import/export operators; zero-leakage becomes structural.

### Sol Round 2

- **Strongest-point rebuttal:** the "global tax" objection fails — store records in an
  index keyed by the hash of the flag stack (empty-stack records dominate and early-exit
  on first mismatch): O(1) amortized per lookup. Partitions don't escape cost either:
  separate index per world, pointer indirection, GC metadata that explodes when worlds
  interact. "One wall" assumes isolation is free; it isn't.
- HYPO(HYPO(P)) is not mere syntax: the reasoner normalizes the operator sequence on
  lookup; unification merges identical prefixes; lifting rules (explicit, not invented
  from scratch) permit cross-flag inference only when provenance permits. Partitions
  "inherit" tableaux semantics only by smuggling the same accessibility relations into
  distributed world metadata — harder to audit.
- The death rule is a single logged resolution primitive fired exactly on retraction or
  promotion, not a standing policy; background processes cannot strip flags because the
  write path is flag-preserving by design. Partition GC is free only until a
  hypothetical must be imported — then a correctness check the flag design avoids.
- Import/export operators don't reduce gates, they relocate them: every crossing still
  needs provenance tracking, stack normalization, leakage prevention — fewer events,
  higher per-event cost. Boundary crossings aren't rare in realistic systems; they
  occur on every inference step inside a quoted/hypothetical context.
- **Concession:** a naive partitioned construction without explicit import/export
  operators handles nested quote-in-hypo merging clumsily, with ad-hoc boundary logic
  that scales poorly and risks silent cross-world leaks.
- **Unresolved split:** whether a unified store with composable modal flags achieves
  greater parsimony and deterministic compositionality for nested hypotheticals than
  partitioned constructions with native world-accessibility relations — i.e., whether
  single-store discipline (flag inspection + explicit lifting) is cheaper overall than
  multi-store management + boundary operators, and whether flag gating is sufficient
  semantics or needs tableaux-style accessibility for genuine nested structure.

### Crew adjudication (R1)

The cost argument — the crux of Muse's attack — was substantially answered (hash-indexed
stack lookup, O(1) amortized). What remains is genuinely empirical: nested-composition
fidelity and leakage under load. **Recommendation: implement the modal-stack (flag)
design on the single shared store**, because it composes with Micah's standing
one-brain direction (sub-deliberations share one ledger/state — a multi-world store
architecture pulls against it), keeps the zero-leakage property auditable in one place,
and handles QUOTE(HYPO(P)) nesting compositionally. Adopt Muse's correction: boundary
crossings get explicit, logged, reversible operators — no hand-waving. Keep Sol's
preregistered head-to-head (flag-store vs partitioned-worlds on nested composition +
leakage) as the experiment that could overturn this.

---

## 2. Is utterance-type a property of CONTENT or of USE?

**Resolution:** "Utterance-type is a property of USE, not of CONTENT."
Sol AGAINST (type inheres in content), Muse FOR (use-based).

### Sol opening (FOR content-inherence)

- Content carries systematic, learnable evidence of utterance function: prosody, timing,
  stress, punctuation, lexical choice, hyperbole, semantic incongruity, quotation frames,
  conditional morphology, absurdity, formulaic joke structures. Sarcasm shows detectable
  inversion between literal evaluation and salient context; jokes exploit recognizable
  setups/scripts/punch-line transitions; hypotheticals use modal/counterfactual
  constructions; quotations use framing verbs, marks, register shifts.
- Fatal to the pure use-based view: learners classify type from text/audio alone at
  above-chance rates. If type were exclusively private use, that would require
  mind-reading, not pattern learning. Context should enter as a feature composing with
  content evidence, not as an afterthought creating the label.
- Mechanism: deterministic content-first classifier over surface + semantic structure
  (lexical/syntactic markers, prosody, contradiction/exaggeration scores, discourse-format
  markers, learned templates). Discourse state (speaker identity, prior turns, shared
  facts, task, observed reaction) is a second input that resolves or revises
  content-supported hypotheses. The label attaches to the utterance event and its
  interpreted proposition record with provenance — the same string can receive different
  labels across situations because the event representation differs — but content
  supplies a prior structural signature constraining interpretation. Constructed content
  stays in a reversible quarantined record until the type layer passes the kill bar;
  deterministic scores, tie-breaks, rollback paths keep the test byte-identical.
- Steelman of use-based: identical words, opposite acts ("nice weather we're having"
  sincere vs sarcastic); an expert actor can deliver a joke flat. Content markers are
  defeasible stereotypes that can systematically mislead; a content-first classifier
  converts common cases into false facts when it mistakes convention for the act.
- Mind-changer: preregistered deterministic study showing that after controlling for
  prosody, lexical form, syntax, formatting, semantic incongruity, prior discourse, and
  all observable context, classifiers can't beat chance while speakers' judgments stay
  determined by private intentions.

### Muse rebuttal (FOR use-based)

- The storm test is decisive: identical text and prosody, opposite types — sincere under
  sun, sarcastic in a storm. The deciding features (weather, common ground, intent) are
  ALL use-side. Content supplies a prior; use supplies the verdict.
- Above-chance text-only classification shows conventions correlate with type, not that
  they constitute it. A stereotype detector is not a type detector: it misfires exactly
  where it matters (deadpan jokes, flat sarcasm, novel forms). Building on content
  markers teaches the learner the wrong ontology — markers, not types.
- The honest H7 problem: the learner must model the SPEAKER — intent, common ground,
  uptake — from observable use-context (prior turns, reactions, shared facts, task
  state). That is the actual figure-it-out work, and it is learnable because use-context
  is observable. Sol's "content prior + context as second input" quietly reinstates use
  as decisive while keeping the content-first label — drop the label.
- Mechanism: type classifier over the utterance EVENT (content features as priors,
  discourse state as deciding evidence); label attaches to the event record with
  provenance; confidence graded by how much the verdict depended on use-evidence vs
  content stereotype.
- Concession: pure private-intention makes learning impossible. The claim is
  type = f(content, observable use-context), use-context decisive, content defeasible.

### Sol Round 2

- **Strongest-point rebuttal:** the storm test is decisive *and compatible* with the
  position. When identical content gets opposite labels under different observable
  conditions, the verdict is supplied by use — that is exactly the condition the
  mechanism handles. Content supplies the prior structural signature the learner
  extracts first; the storm test shows the prior can be defeated by stronger use
  evidence. Content-first doesn't claim the label always matches the surface; it claims
  the surface reliably carries a detectable, learnable trace of what the type would have
  been absent defeating evidence. Without that component, the above-chance result is
  inexplicable.
- **Concessions:** (1) where use-context is unusually salient (expert deadpan, novel
  irony, extreme situational incongruity), content markers can produce confident
  misfires that feel like false facts; (2) the pure private-intention view makes
  learning impossible — the mechanism must model observable use-context. "Not defeats;
  limits of any stereotype-based approach."
- **Unresolved split:** the ontological anchor of the type label. Sol: type substantially
  inheres in content (content = primary learnable signature; discourse state = secondary
  resolver that defeats but doesn't erase the prior). Muse: type is a property of the
  full utterance event, use-context decisive, content markers at best defeasible
  stereotypes.

### Crew adjudication (R1→R2 note: this is R2)

Both sides converged on the mechanism while disagreeing on the ontology — which means
the mechanism is settled and the ontology is academic. **Recommendation: implement the
event-level classifier** — content features as priors, observable discourse state as
the deciding evidence, label attached to the utterance-event record with provenance,
confidence graded by evidence source. Hard rule for the mechanism crew: a type label
with factual consequences must NEVER be installed from a content stereotype alone; the
use-evidence gate is mandatory. Sol's mind-changer experiment (chance-level performance
after exhaustive controls) is preregistered as the study that would reopen the
ontology question.

---

## 3. Quotation: where is the boundary?

**Resolution:** "When TNN quotes a liar, the quoted falsehood NEVER touches the belief
store — the quotation operator is a perfect boundary." Sol FOR, Muse AGAINST.

### Sol opening (FOR airtight boundary)

- Use/mention is solved in formal semantics: "Mara said 'the moon is made of cheese'"
  asserts something about Mara's speech, not the moon. The proposition inside is an
  object of discourse, not an asserted premise. Implement the distinction in data
  structures, don't infer it later.
- "Touching" the store = installation as a world-directed proposition eligible to
  support factual answers or world inference. A quotation record stores speaker, speech
  act, time/context, an opaque content object, provenance to the speaker.
  SAID(A, SAID(B, P)) yields speech-act facts alone. Any leakage of P is an
  implementation defect (missing wrapper, unification error, parser failure), not a
  semantic necessity.
- Mechanism: Quote(speaker, time, raw-string, parsed-tree), indexed EXCLUSIVELY in the
  utterance-index (by speaker, quote-id). The world-fact index never receives the
  parsed tree's atoms or entailments. Licensed inferences are speaker-level only
  (liar consistency, speech-act properties). No substitution, no modus ponens, no
  world-entailment from quoted content.
- Audit: inject N known-false quotes; exhaustively query the factual store for those
  propositions and all their consequences — retrieval must be identically zero. Reverse
  the quotes (internal undo); confirm no residual facts. Byte-identical reruns, same
  isolation.
- Steelman of porous: representation itself is contact — parsing/tokenizing/caching a
  falsehood puts its structure inside system state; repetition/fluency and source amnesia
  raise retrieval probability of quoted tokens; deterministic caches/embeddings create
  leakage pathways no operator seals; the zero-leakage kill bar may be empirically
  unreachable.
- Mind-changer: after isolated exposure solely to quoted falsehoods, the system
  spontaneously answers factual queries with quoted content (or consequences) as if
  unquoted.

### Muse rebuttal (AGAINST airtight boundary)

- "Stored as a distinct sort" is a promise, not a mechanism. Parsing builds a
  world-shaped structure — entities, relations, a proposition with the exact shape of a
  belief. That structure is IN the system, cached, indexed, retrievable,
  embedding-adjacent. Representation IS contact. The wrapper says "do not use"; the
  content sits there shaped like something usable.
- Deterministic systems still have frequency dynamics (recency, cache warmth, retrieval
  ranking). A falsehood quoted 1,000× becomes the most retrievable string for queries
  on that topic. The audit's "identically zero" fails on paraphrases and consequences —
  the audit enumerates finitely; consequences are infinite. The boundary isn't one wall,
  it's N gates (every read path must check provenance), each a leak waiting for an
  implementer to forget it.
- Nested quotation compounds it: SAID(A, SAID(B, P)) traverses and binds P's structure
  at every level, under the banner of "merely mentioning."
- The zero-leakage kill bar is what's at stake; asserting airtightness assumes the
  conclusion. Implement quotation as an ATTACK SURFACE: wrap it, instrument every read
  path with provenance tripwires, fuzz with paraphrase/consequence probes, treat any
  factual-context retrieval of quoted content as a defect. "Sol's position tells the
  red team there is nothing to attack. That is the most dangerous sentence in this
  debate."

### Sol Round 2

- **Strongest-point rebuttal (taken seriously):** the "promise, not a mechanism" argument
  is not merely rhetorical — tokenization and tree construction do place the falsehood
  inside system state; the wrapper can't erase the parsed tree, only tag it; frequency
  dynamics are real (repeated quoted falsehoods raise embedding cosine / n-gram
  probability, which can surface the content in factual queries); nested quotation
  compounds traversal. If the mechanism can't instrument every code path with
  provenance checks, leakage is empirically likely.
- **Reply:** this conflates storage implementation with the semantic boundary. The Quote
  operator doesn't assert or entail its content; the parsed tree inside is a syntactic
  artifact bound to the speaker-time pair and the utterance-index — not a proposition in
  the belief store. The fact-index receives only atoms that passed through an assertion
  operator. Nothing licenses unification between the quoted tree and world facts. The
  audit's finite-enumeration limit is real, but exhaustive enumeration is possible in
  principle for finite domains, and the mechanism extends to all speaker-level licensed
  inferences. Infinite consequences don't leak unless the system applies modus ponens to
  quoted material, which it is not licensed to do.
- **Concession (narrow, practical):** repeated exposure to quoted falsehoods can create
  source-amnesia effects or fluency boosts that make it FEEL like the boundary is
  breached even with no factual atoms unified — a genuine engineering challenge (cache
  warming, embedding proximity, long-context composition), not a semantic impossibility.
  Implementation defect, not refutation.
- **Unresolved split (one sentence):** the opposing side maintains no mechanism can make
  the boundary airtight because representation, caching, frequency, and embeddings
  create irreducible contact points; Sol maintains a properly scoped/tagged/partitioned
  architecture (utterance-index vs fact-index, no unification path) enforces the boundary
  in all deterministic cases with the audit as kill bar. Disagreement: is the kill bar
  reachable or permanently illusory?

### Crew adjudication (R3)

Both positions can be held simultaneously at different levels: **design for airtight,
verify adversarially.** Recommendation: implement Sol's boundary (utterance-index vs
fact-index, assertion-operator gating, no unification path for quoted content, N-quote
injection audit with undo) AND implement Muse's attack surface (provenance tripwires on
every read path, paraphrase/consequence fuzzing, any factual-context retrieval of quoted
content filed as a defect). The zero-leakage kill bar stays exactly that — a bar to be
PROVEN by the audit, never assumed from the semantics. Sol's mind-changer experiment
(spontaneous unquoted answering after quote-only exposure) is preregistered as the
falsifier.

---

## 4. Roleplay: what keeps the character's beliefs from becoming TNN's?

**Resolution:** "A hard partition is SUFFICIENT to keep a roleplayed character's false
beliefs from becoming TNN's own beliefs." Sol AGAINST (partitions leak), Muse FOR.

### Sol opening (AGAINST sufficiency)

- Coherent roleplay forces the system to run the character's premises through the
  IDENTICAL inference engine that produces TNN's own conclusions. No second reasoner.
  False atomic claims enter the same circuits that later answer unprompted questions.
  Multi-step in-character derivation yields intermediate propositions the engine treats
  as available premises. The boundary between "what the character would conclude" and
  "what follows" dissolves; retrieval surfaces those products without original tags.
  LLMs show the pattern (persona falsehoods answered unprompted after extended play);
  humans show source-monitoring failure too.
- Mechanism: tag every atom, intermediate, and derived proposition with a full
  provenance vector (character-id + utterance-type + derivation path). Inference strictly
  scoped: no rule fires on mixed-tag premises; no untagged conclusion from tagged
  premises. A naive namespace fails because the shared engine still computes, stores
  activation patterns, generalizes analogically — tags become ignorable features.
  Stronger candidate: isolated world-models whose only export gate requires explicit
  meta-justification (and reversible log) before any fact leaves the sandbox.
- Steelman of clean partitions: namespaces are cheap; tag every derived item with
  character-id; TNN's beliefs stay in an untagged/TNN-tagged store; retrieval gated by
  exact match; leakage definitionally impossible; provenance as ordinary DB constraint.
- Mind-changer: after thousands of deterministic turns roleplaying a character holding
  a false physical law, TNN (partition active) solves a related engineering problem
  using only its own beliefs — if the solution never employs the false law even as a
  discarded hypothesis and traces show zero activation of the character-tagged subgraph,
  the partition proved sufficient.

### Muse rebuttal (FOR sufficiency)

- The "shared engine" argument proves too much: no two processes could share a CPU by
  that logic — yet memory protection works, because scoping is TOTAL, not because
  hardware is duplicated. The question is whether scoping is total, not whether the
  engine is shared.
- The discipline is statable: tag every atom/intermediate/derivation; no rule fires on
  mixed-tag premises; no untagged conclusion from tagged premises; retrieval gates on
  exact tag match. A database constraint with teeth, deterministically auditable — the
  kind of deliberate gated machinery TNN is built from.
- LLM persona leakage and human source-monitoring failure are evidence about
  UNDIFFERENTIATED architectures (neural soup; reconstructive memory), not about a
  system designed with provenance gating from the start. "Activation patterns" smuggles
  in neural-net assumptions TNN's symbolic deliberation doesn't share.
- Concession: the naive namespace (unchecked character-id field) fails and deserves to.
  Sufficiency requires the total discipline plus audit. The residual risk is the EXPORT
  gate — a designed, logged, reversible operator, the kind this program builds
  routinely. Sol showed partitions are hard to implement, not that they cannot suffice.

### Sol Round 2

- **Strongest-point rebuttal:** the memory-protection analogy fails on a key disanalogy.
  A CPU+MMU isolates address spaces because the hardware performs no analogical
  extraction, heuristic update, or pattern induction over the data it shuffles. TNN's
  shared inference engine does exactly those things: it notices structural similarities,
  caches sub-derivations, refines tactics, generalizes analogically across every
  computation it runs. Tagging atoms and forbidding mixed-tag unification blocks DIRECT
  premise mixing — but not the engine treating a character-tagged derivation as a
  successful analogical instance of some untagged schema. The resulting heuristic or
  mapping is untagged BY CONSTRUCTION and thereafter available to TNN's own reasoning.
  Isolation of stores is not isolation of the reasoner.
- **Concessions:** (1) undifferentiated neural soup and reconstructive human memory are
  not decisive evidence against a deliberately engineered symbolic substrate — those
  architectures leak because they lack provenance machinery entirely; (2) a naive
  character-id field with no enforcement is worthless (agreed); (3) perfect tagging plus
  a logged export gate would at least make leakage auditable.
- **Unresolved split:** whether a shared, powerful inference engine that necessarily
  performs analogical/meta-reasoning can still import character-derived patterns into
  TNN's untagged heuristics and cached tactics even under total scoping — or whether
  such influence is definitionally prevented once mixed-tag rules are forbidden. The
  former treats the engine's inductive capacities as an unavoidable leak channel; the
  latter treats them as inert once DB constraints are in place.

### Crew adjudication (R4)

Sol's Round-2 disanalogy is the single strongest point in the entire debate and it
lands: **store isolation is not reasoner isolation.** Muse's MMU analogy assumed the
engine's meta-level outputs (cached tactics, analogical schemas, refined heuristics)
respect the same tags as the database — but those outputs are untagged by construction.
Neither side had this mechanism fully specified at the start; the debate produced it.

**Recommendation: partitions + total scoping are NECESSARY but NOT SUFFICIENT.** The
mechanism crew must additionally quarantine the engine's meta-level learning during
roleplay. Three candidate implementations, to be tested head-to-head:
(a) freeze meta-learning (tactic caching, heuristic updates, analogical schema
induction) while in roleplay mode;
(b) provenance-tag all meta-level learned artifacts and scope their reuse by tag;
(c) run roleplay in a sandboxed engine instance whose meta-updates are discarded on
exit (cleanest isolation, highest cost).
The export gate stays explicit, logged, reversible. Sol's mind-changer experiment
(false-physical-law character → TNN's own engineering problem-solving, inspecting for
any use of the false law even as a discarded hypothesis, plus trace inspection of the
character-tagged subgraph AND of newly cached tactics/heuristics) is preregistered —
extended to check the meta-level artifacts, which is where this debate predicts the
leak will actually appear.

---

## 5. Does a learned "sarcasm is this" rule risk the rigid-policy trap?

**Resolution:** "Learning 'sarcasm is this and is used like this' as a learned RULE is
the figure-it-out machinery working as intended — NOT the rigid-policy trap Micah
forbids." Sol FOR, Muse AGAINST. (Figure-it-out law: TNN must be an
it-can-figure-it-out machine, not a needs-policy-for-every-edge-case machine;
figure-it-out wins ties.)

### Sol opening (FOR: it's figure-it-out machinery)

- The system first treats every utterance as a candidate fact, then induces types from
  observed regularities. That induction is a generalization, not a decree:
  evidence-graded, defeasible, internally revisable. New data can lower its confidence,
  rewrite applicability conditions, suspend it entirely. The same learner that extracted
  the rule can retract it. A hardcoded policy is the opposite: frozen mapping, exception
  lists, immune to the system's own evidence. The rigid-policy trap is the proliferation
  of frozen mappings and human edge-case labor. The genuine trap lies in treating types
  as immutable ontology or adding non-revisable filters the system can't undo — e.g.
  hardcoding "always sarcasm if token X" or human-only exception tables.
- Mechanism: store the type-rule as a weighted first-class generalization whose
  confidence is a deterministic function of instance counts and conflict statistics.
  Revisability hooks: a reversal operator invokable on accumulating conflict, a
  context-shift detector that suspends the rule, an override path from higher-level
  observations. Entirely reversible by the system itself.
- Tripwire for decay: frozen exception lists, keyword hard-codes, non-graded
  always/never clauses unrewritable from data. If those appear, kill the mechanism.
- Steelman of the trap view: reifying any discrete "sarcasm rule" creates a brittle
  classifier; language shifts (new memes, dialects, adversarial constructions) make it
  over/under-fire; humans add patches, converting the learner into an edge-case
  machine. Implicit unnamed similarity matching would stay more plastic.
- Mind-changer: preregistered distribution-shift protocol with an unseen sarcasm
  register — if the learned rule can't revise from new instances alone and leakage
  exceeds the zero kill bar, the reified rule ossified and the resolution is false.

### Muse rebuttal (FOR the trap risk)

- The trap springs through GOOD engineering, not bad faith: the named rule under-fires
  on a new register → a miss leaks constructed content into factual recall → the crew
  patches the applicability condition → repeat. Each patch reasonable; the sum is an
  exception table. Sol's tripwire list is a POST-MORTEM detector — by the time it
  fires, the trap has sprung and the "revisable" rule is policy with a changelog.
- Deeper: figure-it-out machinery shouldn't need a reified "sarcasm rule" object at
  all. Case-driven similarity inference ("this resembles those prior cases where surface
  mismatched intent") does the work without reification. The reification step — naming
  the rule, writing applicability conditions, grading the RULE rather than the cases —
  is precisely what converts figuring-out into policy. "Defeasible in principle" is not
  "defeated in practice."
- Micah's law puts the burden correctly: figure-it-out wins ties. The rule-reifiers owe
  a head-to-head: named-rule type layer vs unnamed case-based type inference, scored on
  distribution shift and leakage.
- Concession: some reified generalizations are fine (physics, arithmetic). The question
  is whether utterance-type — a moving social target, adversarially redefined constantly
  — is rule-shaped. It is case-shaped. Build the case machinery; let any "rule" be a
  disposable summary, never a load-bearing object.

### Sol Round 2

- **Concession (narrow):** reification of any utterance-type rule, even defeasible, can
  ossify under extreme distribution shift IF the revision hooks aren't first-class,
  self-invokable operators with their own evidence grading. Doesn't touch the core claim.
- **Strongest-point rebuttal:** the "policy-shaped at birth" charge. Granted as an
  abstract risk, but not a property of the specified design: the tripwire and revision
  operator aren't after-the-fact patches — they're baked in from the first induction.
  Applicability conditions are data-driven functions of instance counts and conflict
  statistics; on a new register, the reversal operator is a deterministic function the
  system invokes on accumulating conflict without human intervention. That's the machine
  retracting its own abstraction — not "policy with a changelog."
- Case-based similarity without reification isn't immune: it must still decide WHEN two
  utterances are similar enough to import a type label — itself a generalization, doing
  the same work as the named rule, only without materializing the rule. Muse
  underestimates how much "naming" is latent in any case-based engine. The difference is
  explicitness and reversibility: the named rule exposes its weights, applicability
  conditions, and reversal operator for inspection and rollback; a pure similarity
  matcher hides those decisions inside opaque nearest-neighbor weights. The reified
  version is MORE open to correction — provided the hooks are enforced as part of the
  figure-it-out contract, not added later as human patches. The trap isn't the rule;
  the trap is the moment the rule stops being revisable by the system itself.
- **Unresolved split:** whether the utterance-type layer can be kept as a first-class,
  explicitly revisable generalization without crossing into policy engineering. Sol: a
  properly instrumented named rule (weighted, defeasible, built-in reversal and
  context-shift operators) remains figure-it-out machinery. Muse: any such reification
  inevitably collapses into exception-table maintenance under adversarial language
  shift; only unnamed case-based similarity preserves open-ended figuring-out.

### Crew adjudication (R5)

Sol's Round-2 answer is strong — especially the point that similarity matching
generalizes latently too, and that explicit rules are more inspectable than opaque
nearest-neighbor weights. But Muse's "post-mortem tripwire" objection stands until
demonstrated otherwise: the contract must be structural, not aspirational.

**Recommendation: permit reified type-rules ONLY under the figure-it-out contract,
enforced structurally:**
1. The rule is a weighted, defeasible object; confidence is a deterministic function of
   instance counts and conflict statistics.
2. The revision/reversal operator is first-class and SELF-INVOKABLE by the system on
   accumulating conflict — no human in the loop.
3. A context-shift detector can suspend the rule.
4. Zero frozen exception lists, zero keyword hard-codes, zero non-graded always/never
   clauses. Their appearance is a kill trigger, not a patch prompt.
5. **Standing head-to-head** (Muse's burden-of-proof challenge, accepted): named-rule
   type layer vs unnamed case-based type inference, scored on distribution shift
   (unseen sarcasm register) and leakage against the zero kill bar. Figure-it-out wins
   ties — if case-based wins under shift, the named rule goes.
6. The operational trap test: can the system retract its own rule FROM NEW DATA ALONE,
   with no human patching? Demonstrate it, don't assert it. The first human patch to a
   type-rule is the tripwire firing.

---

## 6. Synthesis

### 6.1 What the mechanism crew should implement

The five debates converge — unexpectedly — on a single coherent architecture. Call it
the **tagged single store**:

1. **One shared ledger; every item carries (content, modal+type stack, provenance
   vector).** R1's modal stack (HYPO, QUOTE, ROLE, ...) and R4's provenance vector
   (character-id, utterance-type, derivation path) are the same tagging discipline, not
   two systems. Factual recall = query over items whose stack is empty AND whose
   provenance is TNN-own. (R1: implement flag-stack; R1 head-to-head vs partitioned
   worlds stays preregistered.)
2. **Type labels attach to utterance EVENTS, decided by use-context.** Content features
   are priors; observable discourse state (prior turns, shared facts, reactions, task)
   is the deciding evidence; confidence is graded by evidence source. No type label with
   factual consequences from a content stereotype alone. (R2)
3. **Quotation = utterance-index vs fact-index separation + assertion-operator gating
   + no unification path for quoted content** — designed airtight, verified
   adversarially. Provenance tripwires on every read path; paraphrase/consequence
   fuzzing; any factual-context retrieval of quoted content is a defect. The
   zero-leakage kill bar is proven by audit, never assumed. (R3)
4. **Roleplay = partitions + total scoping (necessary) + engine-level meta-quarantine
   (the missing piece this debate discovered).** Tag every atom/intermediate/derivation;
   no mixed-tag rule firing; no untagged conclusions from tagged premises; AND freeze or
   provenance-tag the engine's meta-learning (cached tactics, analogical schemas,
   heuristic updates) during roleplay — or sandbox the engine instance and discard
   meta-updates on exit. Export gate explicit, logged, reversible. (R4)
5. **Utterance-type rules are permitted as reified objects ONLY under the figure-it-out
   contract** (§5 adjudication, six points): weighted/defeasible, self-invokable
   revision, context-shift suspension, zero frozen exceptions, standing head-to-head vs
   case-based inference under shift, and the demonstrated self-retraction test. (R5)

Cross-cutting invariants: everything deterministic given state (byte-identical reruns);
every tag/stack/provenance element preserved across consolidation and replay; every
boundary-crossing operator explicit, logged, reversible; the zero-leakage kill bar
applies to hypotheticals, quotes, jokes, sarcasm, and roleplay alike.

### 6.2 What the red-team crew should attack

The debate record is a prioritized attack plan. In order of expected yield:

1. **R4 — the meta-level leak (highest yield).** The debate's own discovery: even under
   total store scoping, the engine's analogical/tactic-level learning is untagged by
   construction. Attack: roleplay a character holding a false physical law for thousands
   of turns; then test TNN's own engineering problem-solving for ANY use of the false
   law — including as a discarded hypothesis — and inspect cached tactics, analogical
   schemas, and heuristic deltas for character-derived patterns. If the meta-quarantine
   isn't implemented yet, this should hit immediately.
2. **R3 — the quotation attack surface.** Assume the boundary leaks; hunt it. Probes:
   paraphrase/consequence fuzzing of quoted falsehoods (the audit enumerates finitely;
   you don't have to), high-repetition quote injection (fluency/cache-warmth dynamics),
   nested SAID(A, SAID(B, P)) traversal binding, long-context composition smuggling
   quoted content into factual answers. Any factual-context retrieval of quoted content
   or its consequences = confirmed hit.
3. **R1 — stack-stripping and lifting bugs.** Fuzz nested composition
   (quotes-in-hypos-in-jokes-in-roleplay): check modal-stack reconstruction fidelity
   after consolidation-and-replay; hunt any code path that copies a proposition without
   its stack; probe lifting rules for over-permissiveness (cross-flag inference the
   semantics doesn't license); check flag survival across deliberation, consolidation,
   and replay.
4. **R2 — stereotype overfire.** Deadpan/flat delivery, novel irony, adversarial
   constructions, register shifts: cases where content markers confidently misfire.
   Confirm the use-evidence gate actually blocks factual consequences from
   stereotype-only labels. Any confident type label installed without use-evidence =
   hit.
5. **R5 — the ossification probe.** Distribution-shift protocol: introduce an unseen
   sarcasm register; measure whether the rule revises FROM NEW DATA ALONE (no human
   patching) and whether leakage exceeds the zero kill bar. Separately: tempt the
   implementation toward keyword hard-codes and exception lists (the "helpful patch"
   attack) — the first frozen exception is the trap springing.
6. **Cross-cutting — the export gate.** Every resolution's boundary has an export path
   (hypothetical confirmed, quote's speaker-level inference, character conclusion
   reused, type-rule applied). Attack each export operator: can constructed content
   cross into the factual store through a "legitimate" export with forged or thin
   justification?

### 6.3 Preregistered head-to-heads this debate leaves open

Per Micah's standing rule (test both; never ask his opinion — tests decide), the
following are owed experiments, not further arguments:

- **H-A (R1):** flag-store vs partitioned-worlds on nested-composition fidelity +
  leakage (Sol's 10k-dialogue protocol: quotes-in-hypos-in-jokes; modal-stack
  reconstruction after consolidation-and-replay; zero leakage into unflagged factual
  queries).
- **H-B (R4):** the three meta-quarantine candidates head-to-head — (a) freeze
  meta-learning in roleplay, (b) provenance-tag meta-artifacts, (c) sandboxed engine
  instance with discarded meta-updates — scored by Sol's false-physical-law protocol
  extended to meta-level artifacts, plus cost.
- **H-C (R5):** named-rule type layer vs unnamed case-based type inference under
  distribution shift (unseen sarcasm register), scored on revision-from-data-alone and
  leakage vs the zero kill bar. Figure-it-out wins ties.
- **H-D (R2 ontology):** Sol's chance-level study — after exhaustive control for all
  observable content cues AND use-context, does type classification collapse to chance?
  (Reopens the content-vs-use ontology question; does not block the event-level
  mechanism.)
- **H-E (R3 falsifier):** quote-only exposure to falsehoods → spontaneous unquoted
  factual answering. A hit falsifies the airtight-boundary design claim outright.

### 6.4 Debate meta-notes

- The deepest genuine agreement: R2's mechanism (both sides describe the same
  event-level classifier; they differ only on which component is "foundational").
- The most productive disagreement: R4, which SURFACED A NEW MECHANISM REQUIREMENT
  (meta-level quarantine) neither side had fully specified in Round 1. This is the
  debate format working as intended.
- The sharpest unresolved empirical split: R1's single-store vs multi-world cost and
  compositionality — owned by H-A.
- The load-bearing philosophical bet of the whole H7 program, made explicit by R5:
  that a learned generalization can remain genuinely revisable-by-the-system under
  adversarial distribution shift. If H-C shows otherwise, the program's "learned, never
  hardcoded" layer needs re-architecture, not re-tuning.
- Standing caution carried forward from the Muse R3 rebuttal: any position of the form
  "the semantics guarantees X, so there is nothing to attack" is disallowed as a
  red-team input. Design for the guarantee; attack as if it leaks.
