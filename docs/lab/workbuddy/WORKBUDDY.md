# TNN Workbuddy — overnight report (2026-09-27)

Micah's order: *"run chat tests and try working with TNN itself, make it
optimized as your workbuddy to help you — broad fixes, no bridges, no rigid
architecture."* Refined: *"TNN works with you and learns off you and sub
agents work too — try that, and it tries to help."*

This document records what was tried, what worked, what failed, and the
morning verdict. All exchanges below are verbatim.

## Scope and boundaries

- The dialogue system under test is the round-4 build
  (`docs/lab/dialogue/round4/dialogue.zag`, adoption commits `75267f9df7`,
  `fb4961d96`, pinned compiler
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- **Session learning only.** Persistent KB writes, strength changes, and
  consolidation belong to frozen grow-with-me prereg `6e15c93144`, which
  Micah has not approved. Nothing in this line touches them: session facts
  live in process memory and evaporate when the process exits.
- All repairs are broad native Zag mechanisms. No per-item patches, no
  frozen choice menus, no bridges, no prompt engineering, no answer shaping.
- The chat wrapper (`wb_chat2.py`) is a pure I/O relay: it spawns the
  binary, forwards stdin lines unchanged, and returns only the final `A `
  response line. It does no thinking, preprocessing, or shaping.

## Method

1. Baseline: frozen round-4 binary, batch mode, 18-turn real-conversation
   battery — two runs byte-identical at the response-stream level
   (`5a585449…6903fc9`).
2. Session-learning probe against the frozen binary: teach FI1/FI3
   findings, then ask back. Result: `I don't know.` everywhere —
   conversation history was not session fact learning.
3. Built the WB-LEARN variant (see OPTIMIZATIONS.md): interactive chat
   mode + session teaching + content-aware memory recall, all in native Zag.
4. Re-ran every probe verbatim against the new binary; verified the frozen
   batch answer stream is byte-identical under the new binary
   (`3d60c4e3…418f` on the S1 battery, both binaries).

## Baseline verdict (frozen round 4, before repair)

| Area | Result |
|---|---|
| Exact fact-shaped retrieval (known vocabulary) | Good |
| Honest withholding ("I don't know") | Often worked |
| Arbitrary comparisons, counting, aggregation | Failed |
| Summaries, morning-brief drafting | Failed |
| Arbitrary nightly terminology | Failed |
| Referent binding under challenge | Dangerous case seen: `are you sure the video composer was blind?` defended the azupscale fact instead of the video-composer entity |

Provisional blocker at baseline: no learn → retain → compose → use path
for arbitrary session knowledge.

## What the repair changed (WB-LEARN)

Teachings are installed as session facts through the *same* ingestion as KB
facts (same `proc_sentence` + `gaz_scan` + `extract_unit` + 40-byte record).
Session fact IDs start at 100000. Retrieval, G6, negation, and yes/no all
consult them with zero changes to those paths.

### Verbatim: session teaching and retrieval (s4 battery)

| # | Input | Response |
|---|---|---|
| 1 | `integrity probe FI1 destroyed 38 of 44 runs.` | `Noted.` |
| 2 | `integrity probe FI3 destroyed 40 of 44 runs.` | `Noted.` |
| 3 | `what did fi1 destroy?` | `integrity probe fi1 destroyed 38 of 44 runs.` |
| 4 | `how many runs did fi3 destroy?` | `integrity probe fi3 destroyed 40 of 44 runs.` |
| 5 | `which destroyed more runs, fi1 or fi3?` | `I don't know.` |
| 6 | `fi4 was silently absorbed.` | `Noted.` |
| 7 | `was fi4 absorbed?` | `fi4 was silently absorbed.` |
| 8 | `no, fi4 was a failure.` | `I don't know.` |
| 9 | `was fi4 a failure?` | `I don't know.` |
| 10 | `what did i tell you about fi1?` | `You asked: integrity probe fi1 destroyed 38 of 44 runs.` |
| 11 | `who wrote the martian?` | `Andy Weir wrote The Martian.` |

Run twice: byte-identical (`a9ebec32…e32d598`). Teaching → exact
retrieval → yes/no → memory recall → KB retrieval all work in one session.

### Verbatim: memory regressions (still passing)

| Input | Response |
|---|---|
| `do you remember what my first question was?` | `You asked: who wrote the martian?` |
| `what was my second question?` | `You asked: when was he born?` |
| `what did i ask?` | `You asked: what was my second question?` (default-last preserved) |

The old failure — `what did i tell you about FI1?` quoting the *question*
instead of the *teaching* — is fixed by the tell/say shape preference
(row 10 above quotes the teaching).

### Verbatim: real night findings fed as teachings

| Input | Response |
|---|---|
| `the decoration audit exposed multiple decorative and unwired mechanisms.` | `Noted.` |
| `the see-its-result audit classified the audio planner as closed.` | `Noted.` |
| `the see-its-result audit classified the upscale line as blind.` | `Noted.` |
| `input fidelity passed image png byte-identical.` | `Noted.` |
| `did input fidelity pass png?` | `input fidelity passed image png byte-identical.` |
| `what did i tell you about the upscale line?` | `You asked: the see-its-result audit classified the upscale line as blind.` |
| `what did the decoration audit expose?` | `I don't know.` |
| `what did the see-its-result audit classify as blind?` | `I don't know.` |

Yes/no and memory recall work on real findings. The two `what did X
verb?` failures trace to a **morphology asymmetry** (see below) plus the
G6 untaught-predicate gate — an honest, characterized limitation, not a
silent wrong answer.

### Verbatim: anaphora, comparison, correction

| Input | Response |
|---|---|
| `those two probes: which destroyed more?` | `I don't know.` |
| `no, fi4 was a failure after all.` (after teaching `fi4 was silently absorbed.`) | `Noted.` (appended as a second session fact — no supersede) |
| `so was fi4 absorbed or a failure?` | `I don't know.` (cannot adjudicate between its own two session facts) |

### Verbatim: genuine work tasks (help tasks)

| Input | Response | Judgment |
|---|---|---|
| `review this work order for holes: WO-2 routes the fix to the owner.` | `Herman Melville wrote the novel Moby Dick.` | Task-generation failure: retrieved an unrelated fact instead of reviewing |
| `draft three morning-brief bullets about disk space.` | `Herman Melville wrote the novel Moby Dick.` | Task-generation failure |
| `summarize the caveats of the see-its-result verdict.` | `I don't know that one. What I know about moby dick: ...` | Summary failure (entity drift to moby dick) |

An earlier build swallowed `review ...` as a teaching (`Noted.`);
the imperative-verb exclusion list now routes all tested task verbs to the
normal pipeline, where they fail *honestly* as wrong-shape answers rather
than silently corrupting session memory.

## Failure taxonomy (planned categories)

| Category | Observed |
|---|---|
| Correct retrieval | Yes — taught facts, KB facts, memory quotes |
| Correct composition | Not observed |
| Honest withhold | Yes — frequent and correct |
| Missing relation/composition | Yes — comparisons (`which destroyed more`), `those two probes` anaphora |
| Wrong-shape answer | Yes — task verbs return unrelated facts |
| Summary failure | Yes — `summarize the caveats…` |
| Task-generation failure | Yes — `draft three bullets…`, `review this work order…` |
| Entity/gazetteer miss | Not separately isolated tonight |
| Referent-binding error | Baseline case recorded; batch re-probes on the briefing KB show frozen and new binaries byte-identical (both answer `was the video composer blind?` correctly, both withhold on `are you sure…`) |
| Unsupported request correctly withheld | Yes |

## New findings for other lines

1. **znc forward-reference miscompile (NEW, 2026-09-27).** Calling a
   function defined *later* in the source compiles without error but
   produces a globally corrupt binary (bus error before the first banner
   print — even untouched code paths crash). Moving the callee above the
   caller fixed it. Lesson recorded in `~/AGENTS.md`: keep every call
   backward; the compiler must reject forward references.
2. **Stemmer asymmetry (frozen morphology, characterized not fixed).**
   `stem_inplace` strips `-ed` naively: `exposed`→`expos` but
   `expose`→`expose`; `classified`→`classifi` but `classify`→`classify`.
   Fact keys and question keys diverge for e-final verbs, so `what did X
   expose/classify?` withholds even when the fact is present. The two
   paths share one stemmer (symmetric by construction), so this is a
   stemmer-quality gap, routed as a work order to the morphology owner —
   not patched here.
3. **Corrections append, never supersede.** `fi4 was silently absorbed`
   followed by `no, fi4 was a failure after all` stores two session facts;
   `was fi4 absorbed or a failure?` withholds. No retraction mechanism
   exists — work order for the memory line.
4. **Disk.** The home disk hit 100% twice overnight (64K free); a VM
   reboot at ~09:00 PDT cleared it to ~200M. Heavy batteries must check
   `df -h ~` first. This line's builds moved to `/tmp` during the crisis.

## Morning verdict: usability as a workbuddy

**Better than baseline, not yet a workbuddy.** Session teaching is real:
direct declarative findings enter native memory and are exactly retrievable,
yes/no-answerable, and quotable by the memory path for the life of the
session, with frozen batch behavior provably untouched. Anaphora over
taught entities (`what did i tell you about FI1?`) now resolves to the
teaching, not the question.

**Biggest blocker (updated):** session facts can *enter* and be
*retrieved*, but TNN still cannot *compose* over them — no comparison
(`which destroyed more`), no anaphoric aggregation (`those two probes`),
no correction adjudication, no summarization, no task-shaped generation
(`draft bullets`, `review this work order`). The missing piece is no
longer intake; it is relation composition and generation over session
knowledge. That is the v2 work-order list in OPTIMIZATIONS.md.

**Where persistent learning would have helped:** multi-session carryover
of tonight's findings (decoration audit, FI1/FI3/FI4, see-its-result,
input fidelity) — explicitly out of scope; belongs to grow-with-me
prereg `6e15c93144`, not implemented here.

## Reproducibility

- Final source: `docs/lab/workbuddy/wb_dialogue.zag` (this commit),
  SHA-256 `8ab44a883076bdea3730b110d4f09eceb2e2a2d2270aa414ed12d2e14da26422`.
- Rebuild: `apply_edits.py` (in `~/workspace/workbuddy/`) regenerates it
  byte-identically from frozen
  `docs/lab/dialogue/round4/dialogue.zag`; compile with the pinned
  toolchain; batch answer stream must equal
  `3d60c4e33c0259b12fd7d27363aed6e8eca095a75bbc8a4daadcc2b6bbcf418f`.
- Interactive harness: `~/workspace/workbuddy/wb_chat2.py` (pure I/O
  relay; `BINARY` env overrides the binary path; run with the binary's
  directory as cwd so it finds `kb.txt`/`gaz.txt`).
