# DIAGNOSIS: Why TNN's Round-4 "Reasoning Traces" Read as Debug Codes

**Date:** 2026-09-26
**Sources:** `~/workspace/trace_trial/docs/lab/dialogue/round4/dialogue_trace.zag` (3233 lines),
`dialogue.zag` (3190 lines), `add_hooks.py`, `ROUND4_REPORT.md`, `trace_output.txt`,
`kb.txt`. Extracted from repo commit `4f782c40d766377c8842127fa2e6ba344c4fc58f`, branch `tnn-native-lab`.
**Method:** read-only source analysis. Every claim below cites a line number in `dialogue_trace.zag`
unless noted.

---

## 0. TL;DR

The TR tags are **printf-debugging of a crew-authored deterministic chatbot**, inserted after the
fact by a Python script (`add_hooks.py`). No part of the binary deliberates; there is nothing
resembling TNN-native reasoning (no hypothesis elimination, no deliberation ledger, no
alternatives ever considered) because the entire decision procedure is a fixed priority cascade
of `if` statements written by the crew. The traces log the *outputs* of already-completed
deterministic computations — often *after* the answer was rendered — and one whole tag family
(`TR method=`) logs a lookup whose result is **never used by any decision**. They read as audit
codes because that is exactly what they are: a dispatch log plus a variable dump.

---

## 1. Per-tag inventory: emitter, logged state, what you learn, what's omitted

Emitter helpers (all defined `dialogue_trace.zag` lines 84–107):
- `tr()` — raw `write(2, …)` to stderr, so TR lines never touch stdout/answers (line 85).
- `trn()` — prints an i64 as decimal (lines 88–93).
- `trt(t)` — prints `TR turn=<t> ` prefix (lines 95–98).
- `tre(eid,…)` — resolves an entity id to its name via the gazetteer (`ge` rows: name offset/len at `8+eid*16`; lines 99–107). Prints `?` for negative ids.

The five "note" functions live at lines 2440–2457. In the control binary (`dialogue.zag`
lines 2412–2424) they are **no-op stubs** (`return;` only) — e.g. `dialogue.zag` contains **zero**
`TR ` emissions (verified by grep). `add_hooks.py` turns them into printers via whole-function
replacement (lines 65–84 of `add_hooks.py`) and inserts every other TR line after unique anchor
lines (the `HOOKS` list). So the entire trace layer is a crew-authored post-processing
instrumentation of a copy of the source — TNN did not emit any of it.

| # | Tag as seen in output | Emitting function / line | Variables logged | What a human learns | What is omitted (the actual reasoning) |
|---|---|---|---|---|---|
| 1 | `TR turn=N ut=K` | `do_turn`, hook at **2663** (inserted after `let ut:i32=utter_type(…)` at 2662) | `turn_no` (loop counter), `ut` = return code of `utter_type()` | Turn index; a numeric utterance-type code. Codes are defined in `utter_type` (1562–1570): **0** = ordinary (falls through to retrieval), **1** = joke request (`tok_has` "joke"/"jokes"), **2** = memory/history question (`is_mem_q`), **3** = forget instruction (`tok_has` "forget"/"forgot"/"forgotten") | The code meanings (opaque without source); which tokens matched; the priority order — "forget" is checked *before* "joke" (1563 vs 1566), so a turn containing both always classifies as forget |
| 2 | `TR turn=N branch=<name>` | `do_turn`, hooks at **2665** (utter-type), **2694** (correction), **2796** (resume), **2819** (compose), **2838** (challenge), **2857** (provenance), **2888** (assertion) | The literal branch name — i.e., which `if` condition matched | Which of the 8 fixed cascade sections fired (sections listed at 2659/2689/2794/2817/2832/2851/2879/2913) | **Every branch not taken and why.** The cascade is strictly first-match-wins; once a section matches it `return`s. The trace never records rejected alternatives or the priority order. Note `branch=compose` (2819) fires *after* `do_compose()` already returned 1 **and wrote the full answer into `resp`** — it is a post-hoc label on a completed action, not a decision trace |
| 3 | `branch=default fid=F withhold=W` | `do_turn`, hook at **3003** | `fid3` = fact-table row index returned by `retrieve()` (fact rows are 40 bytes: `8+fid*40`, cf. 2405); `wd` = 0/1 output of `withhold_check()` | Which KB row won retrieval; whether the withhold gate fired | The fact *text* (only the row index); the scores of runner-up facts (`retrieve` at 1028 picks best Jaccard-ish match — the losers are never logged); *which* withhold sub-gate fired — G1 entity-aboutness, G2 relation-demand, G3 demand-focus (all inside `withhold_check`, 2140+) |
| 4 | `TR compare e1=… v1=… e2=… v2=… tall=T dmin=D` | `do_compare`, hook at **1845** | Entity ids + names (`tre`), their values from `year_of()`, `tall` (1 = height-dimension compare, 0 = time-marker compare), `dmin` (0 = max/taller/last, 1 = min/shorter/first) | The two compared entities and their looked-up values, and the comparison mode | **The actual decision — which entity won — is NOT logged.** The trace fires *before* the winner is chosen: `let win:i32=e1; … if(dmin==0 && v2>v1){ win=e2; …}` happens at ~1855, after the emission. Also omitted: how `year_of` resolved the value, entity-scan tie-breaking |
| 5a | `TR f3 ddim=… d1=… v1=… d2=… v2=… diff=…` | `do_compose`, hook at **2272** | `ddim` (1 = height, 2 = years, from `diff_dim` at 2199), entity ids/names/values, `df` = absolute difference | Dimension code, the pair (either explicit in the question or carried one turn via `pv` slots 48/52/60 — see 2290–2296), live KB values, computed difference | Whether the pair came from the utterance or the carry; the carry's one-turn expiry rule (`cturn+1!=turn_no` → fail, 2251) |
| 5b | `TR f3 unit=meters\|years` | `do_compose`, hook at **2282** | The unit string the code itself appends (`if(ddim==1){ rput(resp," meters"…` at 2280) | Nothing beyond what the answer already says | This tag is an **echo of the code's own render step** — it logs a string the program just wrote. Zero information about any decision |
| 6 | `TR method=N` | `tr_method_note`, called at **2471** (joke), **2731** (correction), **2898** (contradiction), **3014** (clarification) | `mfid` = return of `method_fact()` = lowest fact-table row whose lowercased text contains a **crew-hardcoded keyword**: `"joke"`→43, `"corrected"`→46, `"action"`→45, `"contradicts"`→47 | Which KB row contains the keyword the crew hardcoded at that call site | **Everything that would make this a "method consultation": the result is never used.** Verified: all four `mfid_*` variables appear *only* as the argument to `tr_method_note` — zero uses in any branch condition, zero influence on any answer. The behavior (joke template, correction entity-swap, clarification) is implemented directly in crew code and would be byte-identical if facts 43–47 did not exist (a miss would print `TR method=-1`). The tag documents a decorative lookup, not a decision input |
| 7 | `TR pred-mismatch=0/1` | `tr_predmm_note`, default path **3011** | `pm` = return of `pred_mismatch()` (2546): 1 if some relation-keyword in the question is absent from the retrieved fact while an entity matched | Whether the withhold was "entity matched, predicate never taught" (→ clarification) vs "entity unknown" (→ plain "I don't know.") | *Which* predicate word mismatched; which fact it was tested against |
| 8 | `TR correct-shaped=0/1` | `tr_correct_shape_note`, correction path **2753** | `shaped` = 1 if the entity-swap into the previous question succeeded (2737–2750), 0 if it fell back to the bare remainder (`ql2=cql`, 2752) | Whether shape-preservation worked | The actual reconstructed question text; why the swap failed (no `find_sub` hit) |
| 9 | `TR correct-withhold=0/1` | `tr_withhold_note`, correction path **2776** | `wh_c` = withhold gate result on the re-asked question | Same as tag 3's `withhold=`, but for the correction path | Same omissions as tag 3. Note: the default path never emits `TR correct-withhold=`; the correction path never emits `TR pred-mismatch=` — the tags are path-local, not a uniform schema |
| 10 | `TR joke pair se=… te=… sv=… tv=…` | `tr_joke_note`, inside `compose_joke` **2471** (scan at 2472–2485) | `se`/`sv` = shortest entity id/value, `te`/`tv` = tallest entity id/value (via `year_of(…,"tall")`) | The min/max height entities the riddle is built on | The tie-break rule ("lowest eid wins ties", comment at 2468); that the pair is *always* (global min, global max) — no selection deliberation; the riddle template and the "look up to" double-meaning logic that makes it a joke |
| 11 | `branch=assertion subj=… rel=R val=V conf=C` | `do_turn`, hook at **2888** | `subj` (name via `tre`), `rel` = 1..6 relation code from `extract_assert` (1109), `val` = raw number via `trn` (**not** name-resolved — an entity id prints as digits), `conf` = return of `uclaim_check()` (0 = new claim → "NOTED.", 1 = contradicts a ledger row → challenge) | The extracted triple and the ledger's new/contradiction verdict | Relation-code meanings (1..6); the ledger row it contradicted (which turn, what old value — the code *has* `coval`/`cturn` buffers at 2885–2886 but the trace doesn't print them); `val=17` requires the reader to look up entity 17 (= paris) manually |
| 12 | `TR challenge cfid=… conf=…` | `do_turn`, hook at **2845** | `cfid` = previous answer's fact id, `conf` = digit-conflict code | Which fact is being defended, whether the challenge contained a conflicting digit | Emitted **after** `do_defense(resp,…)` already ran (2844) — post-hoc again |

Two non-TR lines for completeness: `NOVEL=1` is emitted by the binary itself (3186) when
`novelty_ok()` flags the response as novel vs KB+history; the `T R4-0N … PASS/FAIL`, `A …`,
`X …`, `D …`, `SECTION …` lines are the battery harness, not the binary.

### Timing summary: when each tag fires relative to its decision

| Tag | Decision status at emission |
|---|---|
| `ut=` | After classification, **before** branch dispatch |
| `branch=utter-type / correction / resume / challenge / provenance` | After the `if` condition matched, **before** the branch body executes |
| `branch=assertion` | After `uclaim_check` returned `conf`, before response render |
| `branch=default fid= withhold=` | **After** both `retrieve()` and `withhold_check()` completed, before response render |
| `TR compare` | After value lookup, **before** the winner is selected |
| `TR f3 … diff=` / `TR f3 unit=` | After arithmetic, during/after render |
| `TR method=` / `pred-mismatch=` / `correct-shaped=` / `correct-withhold=` / `joke pair` | After the flagged value was computed; **the values play no further role** (pure epilogue) |
| `branch=compose` / `TR challenge cfid=` | **After the answer was fully rendered** — strictly post-hoc |

**Not one tag fires *during* a decision, because there are no decisions being deliberated.**
Every emission point sits after a deterministic function returned, and the emitted value is that
function's output (or a decorative extra lookup). The trace is a *log of computed results*,
never a *record of a choice being made*.

---

## 2. Mechanism-level cause of the weirdness

### Who authors the traces: the crew harness, three layers deep

1. **The behavior is crew-authored.** `do_turn` (2657) is a fixed priority cascade —
   utterance-type → correction → resume → compose → challenge → provenance → assertion →
   default retrieval (section comments at 2659, 2689, 2794, 2817, 2832, 2851, 2879, 2913).
   Every leaf (`do_compare` at 1752, `do_compose` at 2228, `withhold_check` at 2140,
   `retrieve` at 1028, `compose_joke` at 2461, `clarify_predicate` at 2559,
   `render_claim` at 2483) is a deterministic crew-written function: keyword scans
   (`find_sub`, `tok_has`), gazetteer lookups, integer arithmetic, first-match-wins
   returns. There is no randomness and no judgment anywhere in the pipeline.

2. **The trace hooks are crew-authored.** `add_hooks.py` (a Python script, not part of the
   binary) string-inserts `tr(…)` calls into a *copy* of `dialogue.zag` to produce
   `dialogue_trace.zag`, and replaces the five no-op `tr_*_note` stubs with printing bodies.
   The control binary contains zero TR emissions. The ROUND4_REPORT's "trace fidelity" check
   (control vs trace binary, answers byte-identical) confirms the traces are observational
   instrumentation bolted on the outside.

3. **Even the "method consultation" is crew-authored theater.** The comment at 2417–2420
   claims method facts 45/46/47 "are taught through the normal intake path; the code consults
   them before acting, and the trace records which method fact was consulted." Mechanistically:
   `method_fact()` (2426) is a substring search for a keyword the crew hardcoded at each call
   site; its return value is passed *only* to `tr_method_note()` and never gates, steers, or
   informs any behavior. The code does not "consult before acting" in any causal sense — the
   action is fully determined by crew code paths that never read `mfid`.

### Is TNN's own deliberation represented? No — none exists in this binary.

Searched for deliberation machinery: the only hits for `deliberat|hypothes|eliminat|ponder`
are the English word "deliberately" in a code comment (578) and the string "i doubt" inside
the challenge detector (1413). There is:

- **No hypothesis set.** `retrieve()` returns a single best fact id; runner-ups are discarded,
  never logged, never compared.
- **No deliberation ledger.** The only ledger present is the **uclaim ledger** (1279: 16-byte
  rows `subj@0 rel@4 val@8 turn@12`) recording *user* assertions for contradiction detection —
  a lookup table, not a reasoning workspace.
- **No alternatives, no weighing, no uncertainty.** Every decision point is a boolean or an
  argmin; the trace logs the winning value, never the consideration.

### Why they *read* weird — the three precise causes

1. **They log machine addresses, not thoughts.** `fid=41`, `ut=1`, `se=14`, `rel=6`,
   `ddim=1`, `val=17` are row indices, enum codes, and dimension flags meaningful only with
   the source open. A reasoning trace is written for a *reader*; these were written for a
   *debugger* — `tre()` name-resolution exists only for entity ids, while `fid`, `rel`,
   `val`, `ut`, `ddim`, `dmin` print raw numbers.
2. **They are emitted after the fact.** Most tags fire once the deterministic computation is
   over (and two — `branch=compose`, `TR challenge cfid=` — after the answer itself is
   rendered). A trace that only ever reports completed results cannot show reasoning *happening*.
3. **They mistake instrumentation for introspection.** Logging that `withhold_check`
   returned 1 is not the system "deciding to withhold" in any deliberative sense — it is a
   printout of a pure function's return value. The `TR method=` tags go further: they present
   a decorative KB lookup as if the system had *consulted a principle*, when the principle
   played no causal role.

---

## 3. What a genuine reasoning trace would carry that these don't

For each decision point in the battery, a genuine trace would show:

| Missing element | Concrete example from this battery |
|---|---|
| **Alternatives considered** | Turn 1: which candidate facts did `retrieve()` score, what were their scores, why did fid 0 beat fid 4? The trace shows only the winner. |
| **Why the winner won, in followable terms** | Turn 3: the trace logs `v1=96 v2=93` but never states "big ben is taller because 96 > 93" — the `win=` selection (post-trace) is invisible. |
| **Rejected branches and why** | Turn 9: the cascade tried utter-type → correction → resume → compose → challenge → provenance before reaching assertion/default. None of the rejections are recorded; a reader can't tell the system even *considered* them. |
| **Evidence weighed, not just looked up** | Turn 13: `conf=1` says the ledger flagged a contradiction, but not *which* earlier turn's claim, what the old value was (the code holds `coval`/`cturn` — untraced), or what would have counted as resolving it. |
| **Uncertainty and its resolution** | There is none anywhere: no confidence, no tie-breaking rationale (the joke's "lowest eid wins ties" rule is a comment, never traced), no case where two readings were genuinely close. |
| **The principle actually doing work** | `TR method=46` *looks* like "I applied the correction principle," but the principle did no work — the entity-swap code did. A genuine trace would show the principle constraining the outcome, not decorating it. |
| **Human-readable referents** | `fid=41`, `rel=6`, `val=17`, `ddim=1`, `dmin=0`, `ut=1` — a genuine trace would name the fact, the relation, the entity, the dimension, the direction. The one helper that does this (`tre`, entity names) proves the authors knew how; they just didn't do it for anything else. |

Note the asymmetry the report's own verification exposes: the "trace fidelity" gate
("control vs trace binary → all 29 answers identical, TR lines excluded") is presented as a
*strength*. It is actually the diagnosis in one line: **the traces can be deleted without
changing a single answer, because they never participated in producing any.**

---

## 4. Verdict

These are not reasoning traces in any meaningful sense. **They are execution traces — a
debug log of a deterministic rule engine** — specifically:

> A crew-authored dispatch log (which `if` fired) plus a variable dump (what the pure
> functions returned), instrumented post-hoc by `add_hooks.py` into a copy of the source,
> printed to stderr so as not to disturb the byte-identical answers.

What makes the verdict sharp rather than merely deflationary:

- **Nothing in the binary deliberates.** The decision procedure is a fixed 8-section
  first-match-wins cascade of deterministic functions. Logging its intermediate values is
  like calling a stack trace "the program's thoughts."
- **The most reasoning-like tags are the most misleading.** `TR method=45/46/47/43` wears
  the costume of principle-guided behavior ("the system consulted its taught method"), but
  the lookup result is causally inert — used only as a print argument. This is not a trace
  of reasoning; it is a trace of a *reenactment* of reasoning.
- **The one real decision in the pipeline isn't traced.** `do_compare`'s winner selection
  (`win=e1/e2`) happens *after* `TR compare` is emitted. The trace shows the evidence and
  hides the verdict.

Micah's instinct is exactly right: he "could never imagine them as reasoning traces" because
no reasoning occurred at the traced points — only computation. A genuine TNN reasoning trace
would require TNN-native machinery that *considers and eliminates* (hypotheses, readings,
candidate facts) and the trace would show the elimination. This binary has no such machinery
to trace. The honest label for the artifact is **"deterministic dialogue router with
instrumented internals,"** and the honest label for the TR lines is **"crew debug output."**

### Recommended follow-ups (for the coordinator)

1. If the goal is traces *of TNN reasoning*, the prerequisite is TNN-native deliberation
   machinery in the binary (hypothesis set + elimination + a deliberation ledger) — tracing
   has to come after the thing being traced exists. Instrumenting the current router further
   will only produce more detailed debug codes.
2. If the goal is human-readable audit output from the current router, the cheap fixes are:
   resolve all codes to names (`fid`→fact text, `rel`→relation name, `val`→entity name,
   `ut`/`ddim`/`dmin`→words), log rejected branches with their failing conditions, and move
   the `TR compare` emission after winner selection. But this yields a readable *log*, still
   not a reasoning trace — don't label it as one.
3. The `TR method=` pattern should be retired or repaired: either make method facts
   causally load-bearing (behavior changes when the fact is absent — currently it doesn't)
   or stop presenting the lookup as consultation. As it stands it is the single most
   misleading element in the trace set.
