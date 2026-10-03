# WB-LEARN optimizations (2026-09-27) — broad native mechanisms

Companion to WORKBUDDY.md. Every mechanism below is a general Zag-level
capability, never a per-item patch, content allowlist, frozen choice menu,
bridge, or prompt shaping. The chat wrapper is pure I/O and stays dumb by
design.

## Mechanism 1 — Interactive chat mode (main, `argv[1]=="chat"`)

One process stays alive across turns, preserving TNN's native salience,
history, assertions, and in-memory facts. A 4KB line buffer is filled by
the `stdin_line` helper (raw fd-0 reads); each line is lowercased and fed
to the unchanged `do_turn`. One process = one session: everything
evaporates on exit. Batch mode (battery.txt) is untouched — verified
byte-identical on the S1 battery.

Broad because: it changes *process lifetime*, not any behavior. No
content, no prompts, no task logic.

## Mechanism 2 — Session teaching (4b hook in do_turn §4 + `session_teach`)

A declarative user turn that the assertion path cannot parse (unknown
entity or relation shape) is taught as a **session fact** through the same
ingestion KB facts get: `proc_sentence` → `gaz_scan` → `extract_unit` →
40-byte `fm` record. Session facts live after the KB facts with fids
100000+. Retrieval, G6, negation, yes/no, and provenance consult them with
zero changes — they cannot tell a session fact from a KB fact, which is
exactly the point.

Capacity is principled, not tuned: the three arena-bound checks
(`fm` 8192, `ftx` 8192, `fea` 4096) are the physical arena sizes. Full
arenas answer `My session notes are full.` No persistence: a new process
starts from `kb.txt` alone.

Broad because: any declarative sentence in the language is teachable, not
a fixed set of templates or nightly names. The ingestion is shared code,
not a parallel path.

## Mechanism 3 — Declarative-shape gate (`is_teach_shape`)

Teaches only grammatical declaratives. Excludes interrogatives (the
wh-word list plus the `cmp_yesno` auxiliary-inversion class) and leading
imperatives (tell/give/show/list/explain/describe/summarize/draft/write/
name/review/check/audit/verify/find/identify/compare/analyze/assess/
evaluate/critique/edit/fix/create/make/generate/produce/provide/suggest/
recommend/outline/plan).

Broad because: grammatical *mood*, never content. A request stays a
request regardless of topic; a statement stays teachable regardless of
topic. (Caught live: `review this work order…` was briefly swallowed as a
teaching before the imperative list covered it — the failure mode was
silent memory corruption, the fix was widening the grammatical class.)

## Mechanism 4 — Content-word memory selection (`mem_answer`)

The old `mem_answer` blindly quoted the latest user turn, so `what did i
tell you about FI1?` quoted the *question*. The new selection:

1. Ordinal/first/last/previous/latest handling unchanged.
2. Otherwise, scans the question's non-scaffolding **content words**
   (stopwords and memory-discourse verbs — tell/told/ask/say/said/
   remember/recall/about/my/question/mention — excluded by closed
   grammatical class in `is_mem_scaffold`) and selects the most recent
   prior user turn containing one as a token.
3. Tell/say-shaped requests prefer stored *teachings*; ask-shaped requests
   prefer stored *questions* (pass 1 = shape-matched, pass 2 = any).

Broad because: token-level content matching with a grammatical scaffold
class — no entity lists, no nightly names, no per-question rules.

## Mechanism 5 — `tok_in_span`, `is_mem_scaffold` (helpers)

Small, general: token-exact substring search and the scaffold-word
predicate. No content knowledge.

## What was deliberately NOT done

- No KB file writes, no strength changes, no consolidation — prereg
  `6e15c93144` territory.
- No answer shaping or prompt engineering anywhere (the relay is pure I/O;
  the binary has no task templates).
- No morphology patch for the `expos`/`expose` asymmetry — frozen
  morphology, routed as a work order instead.
- No comparison/correction/summarization engines — those are the v2 work
  orders below, each a real native mechanism to design, not a patch.

## v2 work orders (from tonight's honest failures)

| WO | Failure | Mechanism needed |
|---|---|---|
| WO-WB-1 | `which destroyed more runs, fi1 or fi3?` → withhold | Comparison over session facts: extract quantities from taught facts, order them. General numeric-relation composition, not FI-specific. |
| WO-WB-2 | `those two probes: which destroyed more?` → withhold | Anaphoric plural resolution over taught entities + WO-WB-1. |
| WO-WB-3 | Correction appends instead of superseding; `was fi4 absorbed or a failure?` → withhold | Retraction/supersede: a correction-shaped turn marks the earlier session fact superseded. Needs a native session-fact lifecycle. |
| WO-WB-4 | `draft three morning-brief bullets…` → unrelated fact | Task-shaped generation: compose from retrieved facts into a requested shape. Largest gap. |
| WO-WB-5 | `summarize the caveats…` → entity drift | Abstractive composition over multiple facts. |
| WO-WB-6 | `what did X expose/classify?` → withhold on present facts | Morphology: restore-e on `-ed` strip (exposed→expose), owned by the morphology line. |

## Toolchain finding (new 2026-09-27)

**znc silently miscompiles forward function references.** A call to a
function defined later in the source compiles clean but yields a globally
corrupt binary (bus error before the first output — even untouched paths
crash). Fix: define callees before callers (the final source orders
`is_teach_shape` → `mem_answer` → `do_turn` → chat branch). Recorded in
`~/AGENTS.md`. The compiler should reject forward references; until it
does, audit call direction in every native edit.
