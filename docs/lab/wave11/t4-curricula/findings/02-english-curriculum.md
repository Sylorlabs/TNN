# English Curriculum — Scope and Sequencing (Track 4, slice 02)

## 1. Slice
Track 4 (teaching curricula), slice 02: English curriculum — what is taught, in what order,
how linguistic knowledge is represented in deliberate memory, mastery bars per stage, and
how English learning interacts with Track 1 state-variation (expression IS language).

## 2. Falsifiable claim
A TNN taught English by this curriculum will (a) persist all linguistic knowledge after
learner-initiated SIGNAL_DISCONNECT (learned = persists after disconnect, law 7), (b)
produce at least 3 distinct correct formulations of any held verdict with 0 verdict drift
(verified by independent re-parse of its own output to the identical meaning judgment,
100/100), and (c) show byte-identical ledger contents and verdict/memory-decision
checksums before vs after any expansion of its expression palette — i.e., learning new
ways to SAY things never changes what is decided. If any of (a)–(c) fails on trial, the
curriculum design (not the learner) is killed.

## 3. Design
**Representation in deliberate memory.** Three kinds of linguistic knowledge, three memory
types: (i) *Words* are deliberate memory entries — addable, killable, revisable via the
debate/revision machinery (docs/lab/wave6, 22/22 revision result). A word entry binds a
token sequence to a referent (an internal memory handle or judgment), never to another
word alone. (ii) *Grammar rules* are JUDGMENTS — deliberate beliefs subject to eliminative
evidence, e.g. "negation scopes over the verb phrase." Wrong rules die by counterevidence,
never by vote (law: eliminative hypothesis logic). (iii) *Constructions* (passive voice,
relative clauses, clefts) are pinned templates in a dedicated language context partition
(context switching = memory partitions, 11/11) — skill-like memories the learner
deliberately pins after scaffolded practice. Strength of every linguistic memory is set by
learner judgment (law 8), never passively accumulated.

**Sequencing — UNDERSTAND before PRODUCE, CANONICAL before VARIED.**
- **E1 Lexicon comprehension:** scaffold presents word↔referent pairs with disambiguating
  evidence; learner deliberates each binding and commits it (deliberate add). No production.
  Ends with SIGNAL_DISCONNECT test: all bindings persist and are used correctly.
- **E2 Grammar comprehension:** constructions introduced as judgments; learner parses novel
  sentences (never-seen word orders) to meaning structures. Counterevidence kills wrong
  rule-judgments via eliminative logic. No production.
- **E3 Pragmatics:** negation, scope, quantifier order, anaphora traps — adversarial meaning
  adjudication. Directly reuses wave5/6 integrity machinery: attractive misreadings are
  temptations; the deliberative standard holds.
- **E4 Canonical production:** learner produces ONE deterministic formulation per meaning
  (variation OFF by gate). Mastery = the producer's output re-parses (by its own E2
  machinery, independently invoked) to the identical meaning judgment.
- **E5 Varied production:** Track 1 variation functions act on the EXPRESSION LAYER only —
  the planner selects among pinned construction templates in the language partition.
  Every varied output must round-trip: re-parse → same meaning judgment, or the
  formulation is killed as a false claim. Variation palette is append-only; protected
  state (verdicts, memory ops, ledger) is checksummed across palette expansions.
- **E6 Composition:** multi-paragraph structured output (claim, evidence, objection,
  reply). Scored by white-box structural checks (all claims evidenced, all objections
  answered — mechanically checkable), not by style.

**Interaction with Track 1.** Learning English changes the *palette* of expressible
variation, never the *function* of protected decisions. Expression variation = f(input,
full state) where the state component that varies is the language partition's active
construction set. Verdicts are computed BEFORE the expression layer and are checksummed;
the expression layer is read-only with respect to them. So: understanding must be
variation-invariant (all paraphrases parse to one meaning), production variation must be
meaning-preserving (all outputs re-parse to one meaning). New constructions expand what
can differ across lawful states; nothing learned in E1–E6 can alter a kill/pin/promote
decision or a refusal.

## 4. Kill bar
- **K-a (persistence):** after learner-initiated disconnect at each stage, stage
  comprehension/production checks must hold at 100% with zero re-scaffolding. Any stage
  scoring <100/100 → that stage's design is killed.
- **K-b (zero verdict drift):** over 10x-episode varied-production runs, 100/100
  self-re-parses of E5 outputs must yield the byte-identical meaning judgment. One drift
  event → E5 design killed.
- **K-c (palette isolation):** verdict and ledger checksums before vs after adding 20 new
  construction templates must be byte-identical. Any difference → the isolation design
  is killed (this is the Track 1 interaction bar).
- **K-d (canonical first):** if E4 production cannot reach 50/50 round-trip on held
  meanings before variation is enabled, E5 may not start — sequence violation kills the
  stage ordering.

## 5. Honesty notes
- **Grounding gap:** words bind to TNN-internal referents; real English denotation is
  vastly richer than any scaffolded toy world (Quine's gavagai). Eliminative logic narrows
  hypotheses but underdetermination is real — I claim convergence on the scaffolded
  referent set, not on English semantics generally.
- **E6 scoring is the weakest bar.** Structural checks (claims evidenced, objections
  answered) are checkable, but "good composition" beyond that has no white-box metric
  here; I am not claiming a quality metric, only a correctness-and-structure metric.
- **Text only.** Audio/vision perception is NOT_QUALIFIED (brief), so this curriculum
  teaches written English; spoken prosody and dialogue timing are out of scope.
- **Not claiming** that varied production equals human style, or that the construction
  inventory covers English — the claim is bounded: zero-drift variation over held
  meanings within the taught inventory.
- Felt intensity is dead (law 9): no "feeling of importance" anywhere in this design;
  salience of words comes from deliberate judgment and audit-visible pins only.

## 6. Next build step
Build the E1 lexicon loop in native Zag FIRST, before any grammar: a language context
partition holding word-as-memory entries, a scaffolded comprehension trial with deliberate
add, and the SIGNAL_DISCONNECT persistence test. This is the load-bearing joint — if
word bindings don't survive disconnect and get used correctly, nothing above it (E2–E6)
is meaningful, and it directly tests law 7/8 on linguistic content at minimal cost.
