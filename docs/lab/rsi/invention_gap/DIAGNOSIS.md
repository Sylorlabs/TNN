# T1N Invention-Gap Diagnosis — why TNN couldn't invent with principles

**Question (Micah):** "Was the knowledge principles to invent off of, or bad knowledge?"
**Short answer:** Neither. The knowledge was adequate. The composition machinery doesn't exist.
TNN's deliberation is a judge with no hands: it can look at building materials and
say "this beam is rotten, that one is sound" — honestly, with evidence — but there is
no builder. The "builder" is a stencil the crew left behind, and it stamps the same
house no matter what the judge says.

**Status:** diagnosis only. No repair built. Committed on `tnn-native-lab`.

---

## 1. What a human does between a principle and an artifact

Concrete and mechanistic, using the actual domain (inventing a code-generation
architecture from taught knowledge). A human passes through these intermediate
representations — each one is a real thing, not a metaphor:

**H1. Functional decomposition.** Principle: "the system must map goal descriptions
to code emitters and repair code that doesn't compile." The human breaks this into
named jobs with responsibilities: (a) a *selector* that picks an emitter for a goal,
(b) *emitters* that produce code, one per mechanism, (c) a *repairer* that fixes
compile errors. Each job gets a name and a contract. This is a representation the
human holds and revises — "actually, selection and repair should share the trigger
table" is a design edit at this level.

**H2. Interface sketch.** Before any implementation, the human writes signatures:
`select(goal) -> emitter_id`, `emit(emitter_id, goal_params) -> code`,
`repair(code, compiler_error) -> code`. Types and data flow are fixed first. The
compiler later *checks* the plan; it doesn't *make* the plan.

**H3. Mechanism-to-code binding (transliteration).** The human takes an accepted
mechanism — "reverse: read the argv string, loop from n-1 down to 0 printing each
char" — and writes emitter code whose *structure follows the mechanism description*.
The code is a transliteration of a design decision, not a retrieval of a template.

**H4. Parameter-slot filling.** The emitter for "sum" needs bounds. The human decides
*where bounds come from* (the goal's parameters, not the spec's type annotations),
binds them to slots, and the binding has semantics: "N means the count the user
asked for." A distractor integer in the spec must not fill the slot.

**H5. Failure localization → design revision.** Compile error "undefined identifier y":
the human localizes it — *which* emitter, *which* binding — and revises the *design*
("the emitter must bind the loop variable the seed defines"). The fix is at the
design level, not "try random edits until it compiles."

**H6. Provenance tracking.** Every part of the artifact points back: "this emitter
exists because of design decision D3, which came from principle P2, recorded in
episode 24." The human can answer "why is this line here."

The load-bearing observation: **principles and code never touch directly.** Between
them sits a *design* — structured, revisable, made of components, interfaces, and
bindings. Everything humans call "composing" or "inventing" happens in that middle
layer.

---

## 2. What TNN's machinery actually did (mapped step by step, with evidence)

Sources: frozen `t1n_delib.zag` (engine), frozen `trace_frozen.txt` (informed, 99
episodes), frozen `t1n_arch.zag` (composed module), `REVIEW_COORDINATOR.md`.

### The proposer: a token splicer, not a designer

`d_synthesize` (engine line 898) is the "novel synthesis" operator. What it does:

1. Takes a corpus record's prose body, splits it into "sentences."
2. Extracts code-ish tokens from each sentence.
3. Picks the taught base mechanism with the highest keyword overlap.
4. Substitutes identifiers from the record's tokens into the base's lines.
5. Writes the result and compile-tests it.

This is **lexical substitution**, not composition. It has no representation of jobs
(H1 missing), no signatures (H2 missing), no transliteration of a design into code
(H3 missing — it splices tokens, it doesn't translate structure). The trace shows
13 novel proposals (EP0010–EP0022) plus revision rounds; **every one failed to
compile** — "revise produced no candidate" / "revision budget exhausted." A 100%
compile-failure rate is what you expect when the operator has no notion of program
structure (types, scope, control flow). No corpus of principles, however perfect,
can survive this operator.

### The critic: a working judge with no way to order a rebuild

The critic genuinely works. It compile-tested every candidate and **correctly refused
4 taught KB entries** that shipped uncompilable `_zag_raw_syscall` calls (wrong
arity for the pinned toolchain) — real evidence, real refusal. It accepted 4 good
mechanisms (E-STRREV, E-ARRAYSUM, E-SORT, E-HASH).

But its "revision" path is: re-run the same token splicer, up to 3 rounds. There is
no failure localization (H5 missing) — it never says "the failure is in the emitter's
variable binding, revise the binding." It says "try splicing again." When the splicer
can't produce anything, the critic honestly reports "no candidate." The judge is
honest; it just has nobody to give orders to.

### The composer: a fixed stencil, not a composition process

This is the decisive finding. `m_compose` calls `d_emit_module(...)` with six
parameters — the bake episode number and the citation strings, derived from the
deliberation. **All six parameters are dead.** Verified mechanically against the
frozen engine source: zero uses of `t1k, t1t, t2s, t2v, t4k` in the function body
(the single `goal` match is inside a comment string).

The emitted module is ~450 lines of **hardcoded string literals** (`d_cmo("...")`
chunks) authored by the crew. That means:

- The emitter weights (`revers+10`, `sum+10`, `argument+5`, `loop+5`) were never
  deliberated — they're literal text in the template. The trace deliberated
  "use argmax" (EP0024/EP0075); the *weights* came from the stencil.
- `mg_fact` (factorial emitter) has no taught counterpart — stencil content.
- `mg_smart_sum` parses integers out of the spec text — stencil content. This is
  the `4,5,6 → 131` bug: it summed the `32` from the `i32` type annotation. The
  probes' `demo` channel (the actual test inputs, required by prereg Amendment A1)
  is never read, because nothing maps the interface to the implementation
  (H2/H4 missing).
- The phantom citations `EP0100/EP0101/EP0102` are **literal strings in the
  template**, not IDs TNN chose. The traces end at EP0099/EP0058. The review's
  phrasing — "the composer invented citation IDs" — is mechanically imprecise:
  the composer (as a TNN process) made genuine decisions in its COMPARE episodes
  and its bake decision cites the right things; the *emission step* stamped
  hardcoded wrong IDs because no mechanism derives citations from the actual
  episode sequence (H6 severed).

**Zero bits of deliberation flow into the artifact.** The accepted mechanisms
(E-SORT, E-HASH) have no emitter in the module; the module's emitters don't match
the accepted set. The deliberation and the artifact are decoupled by construction.

### Corrected failure attribution

The review says "the composer improvised." The mechanically precise version:

- TNN's deliberation did not improvise. It judged (proposer/critic: real) and it
  decided (composer's COMPARE episodes: real).
- The *emission* is a crew-authored fixed template. The "improvisation" — weights,
  keywords, phantom citations, the spec-text integer parser — was authored by the
  crew when writing the template, and it sailed through because no provenance check
  compares template content against the trace.

TNN didn't cheat at composition. It never got to compose at all.

---

## 3. Answer to Micah's question, with evidence

**"Was the knowledge principles to invent off of, or bad knowledge?"**

It was principles to invent off of — and we can prove the knowledge was never the
binding constraint:

1. **The corpus was inert.** Informed (69 KB entries + 12 prior-art records) and
   scratch (69 KB entries, no corpus) produced **byte-identical modules and
   byte-identical battery logs**. Not a small effect — zero effect. A knowledge
   problem cannot produce a zero effect when the knowledge differs. Only a severed
   pathway can: the 13 novel synthesis attempts all failed to compile, and the
   composer is a fixed stencil, so the manipulated variable had no pathway to the
   outcome.

2. **The critic proved it can judge knowledge.** It refused 4 uncompilable taught
   entries on genuine compile evidence. Bad knowledge *was* present in the KB and
   *was* caught. The judging machinery works on knowledge; the building machinery
   doesn't exist.

3. **Successfully judged knowledge never reached the artifact.** E-SORT and E-HASH
   were accepted and then absent from the module; `mg_fact` is in the module with
   no taught counterpart. The deliberation→artifact link is severed regardless of
   knowledge quality — better knowledge would have been accepted and then ignored
   in exactly the same way.

4. **The synthesis operator is knowledge-proof.** Lexical token-substitution with a
   100% compile-failure rate cannot consume *any* corpus of principles. A human
   given the same 12 records would decompose them into components and interfaces;
   the operator cannot represent structure at all.

**Verdict: broken composition machinery, not bad knowledge.** "Teach knowledge
first" does not buy invention because there is no inventor home — only a judge
and a stencil.

One caveat for the record: the corpus and KB entry *contents* were not in the
committed tree (only their SHA fingerprints in `teach_audit.txt`), so this
diagnosis characterizes the knowledge from the trace's proposal/citation records,
not from reading the corpus text. The conclusion doesn't depend on the corpus
being good — it depends on the operator being unable to use any corpus — but the
corpus text itself is not independently verified here.

---

## 4. The minimal missing mechanism

One mechanism, stated minimally:

> **A composition operator that maps accepted knowledge records to artifact
> content — the deliberation trace must be executable as a build plan.**

Concretely:

- Each accepted mechanism record carries `(triggers, emitter code, slot list)`.
- The composer assembles the module **from those records**: emitters = the accepted
  emitter bodies placed into the module; the selection dispatch = generated from
  the accepted trigger lists; citations = derived from the actual episode sequence.
- No fixed template. The artifact must be a **pure function of (accepted set,
  deliberated rules)**.

This one mechanism covers H3 (binding), H4 (slots), and H6 (provenance). H1/H2
(decomposition, interface sketching) are the deeper, human-full version — future
work. The minimal testable step is the executable-trace link: **if the artifact
isn't a function of the deliberation, nothing downstream — better knowledge,
better judging — can matter.** That's the order of operations: hands before
taste.

---

## 5. What would have to be built (plain language)

1. **Hands**: a composer that reads the accepted mechanisms out of the knowledge
   store and writes their code into the artifact — so changing what TNN accepts
   changes what gets built. (Today: stencil; the accepted set is decorative.)
2. **Slot semantics**: when an emitter needs a parameter, the composer must bind it
   from the goal's parameters with a deliberated rule for *which* value fills
   *which* slot — not "parse all integers out of the spec text." (Today: the
   `i32 → 32` bug is what slot-filling looks like without semantics.)
3. **Eyes on the error**: when a candidate fails to compile, the critic must say
   *which part* failed and revise the *design decision* behind that part — not
   re-run the same splicer. (Today: "revise produced no candidate.")
4. **True provenance**: citations derived from the episode sequence that actually
   ran, so "why is this line here" is always answerable. (Today: hardcoded
   EP0100-102.)

The preregistered test for mechanism #1 — the one that proves the hands exist —
is in `PREREG_COUPLED_COMPOSE.md`.
