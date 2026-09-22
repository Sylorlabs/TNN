# Q2 — Knowledge Audit: did the TNN ever have bug knowledge?

**Scope:** `curriculum.json`, `CURRICULUM_REPORT.md`, `learner.zag` (2050 lines, src/),
`driver.py`, `run_full.py`, `manual.md`, `PREREG.md`, `CODING_REPORT.md`.
**Method:** source grep + line-level read of every repair/generation path.
**Auditor:** BUG-BLINDNESS WORKER B, 2026-09-21.

## Q2(a) — Every pattern ID installed via `teach` (11/11 enumerated)

The install set is the `ALL_PATTERNS` CSV, defined identically in
`driver.py:12` and `run_full.py:13`:

```
p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill
```

**Count: 11.** All 11 are passed to the learner's `gen` mode as the
`installed` CSV (`do_gen`: `_zag_arg(3)`, learner.zag:1971) and consumed only
by `installed_has()` gate checks in `gen_t1` (1915–1941), `gen_t2` (1943–1967),
and `gen_t4` (1841–1890): if the needed ID is absent the emitter refuses with
`UNTAUGHT:<id>`. Two facts matter:

1. **`teach` mode is never invoked by either driver.** `grep` for
   `run_learner('teach'`/`"teach"` across `driver.py` and `run_full.py`
   returns zero hits. The 11 IDs are injected straight into `gen`; the only
   mentions of `teach` are in prose docs (`PREREG.md`, `CODING_REPORT.md`).
2. **`teach` installs nothing even when run.** `do_teach`
   (learner.zag:1306–1320) prints an `AUDIT op=INSTALL pid=…` line and exits.
   There is no store, no table, no file write; learner processes are
   stateless across invocations. Verified empirically: shipped `src/learner`
   binary is behavior-identical to a fresh build from this source
   (sha256 of `repair` and `teach` outputs match).

**Classification — all 11 are correct-pattern, 0 are bug-knowledge:**

| # | Pattern ID | Emitter in learner.zag | Generates | Bug knowledge? |
|---|---|---|---|---|
| 1 | p_math | `emit_t2_math` (622) | correct MATH programs | no |
| 2 | p_search | `emit_t2_search` (536) | correct SEARCH programs | no |
| 3 | p_slice | `emit_t1_slice` (289) | correct SLICE programs | no |
| 4 | p_strrev | `emit_t2_strrev` (582) | correct STR programs | no |
| 5 | p_func | `emit_t1_func` (216) | correct FUNC programs | no |
| 6 | p_loop | `emit_t1_loop` (335) | correct LOOP programs | no |
| 7 | p_struct | `emit_t1_struct` (383) | correct STRUCT programs | no |
| 8 | p_sort | `emit_t2_sort` (480) | correct SORT programs | no |
| 9 | p_argv | `emit_t1_argv` (410), `t4_argvsum` (1033) | correct ARGV programs | no |
| 10 | p_strcnt | `emit_t1_str` (350) | correct STR-count programs | no |
| 11 | p_slicefill | `emit_t2_squares` (694) | correct SLICE-fill programs | no |

Every pattern table entry maps a spec class to a **correct-code emitter**.
There is no table of faults, no bug-pattern list, no error→fix mapping
reachable from any `teach`-installed ID. `grep -i "bug"` in `learner.zag`
returns **zero hits**. The reference card `manual.md` ("CARD: errors") documents
the 5 error classes as human reference only — headed "REFERENCE ONLY, never
installed" — and is never read by the learner at runtime.

**Verdict (a): 11/11 IDs enumerated; 11 correct-pattern, 0 bug-knowledge.**

## Q2(b) — Every repair rule: authored vs taught

All 8 repair functions are **authored-in-learner** (baked into `learner.zag`
at learner-build time; the dispatch in `do_repair`, learner.zag:2006–2039, is
a hardcoded `if`-chain on the eclass string). **Zero were taught** — there is
no taught-repair store and `do_repair` reads no pattern table.

| # | Function | Line | Eclass | Rule (mechanism) | Authored? | Called by dispatch? |
|---|---|---|---|---|---|---|
| 1 | `patch_ret_word` | 1442 | E0203 | `return "word";` → `return <N>;` via 21-word `word_to_num` dict (1400) | yes | **yes** (1st) |
| 2 | `patch_arg_unquote` | 1463 | E0203 | strip quotes off first quoted-int literal anywhere in source | yes | **yes** (2nd) |
| 3 | `patch_del_badassign` | 1490 | E0203 | delete a line `V="…";` (exact `="` match, no spaces) when `let V:i32/i64` declared | yes | **yes** (3rd) |
| 4 | `patch_type_a` | 1184 | E0203 | rewrite `let V:i32/i64="lit"` decl type → `[]u8` | yes | **NO — dead code**, never called |
| 5 | `patch_unknownfn` | 1155 | UNKNOWNFN | rename unknown call to nearest defined/intrinsic name under `similar()` (≤2 char diffs, length diff ≤2; intrinsics `_zag_print`, `_zag_i64_to_str`, `_zag_arg`) | yes | **yes** |
| 6 | `patch_arity` | 1596 | ARITY | too many args → drop extras; too few → pad by incrementing parsed digits of last arg (`lv+1…`) | yes | **yes** |
| 7 | `patch_brace` | 1733 | PARSE | close open blocks before a new `fn` line; append `}`×depth at EOF | yes | **yes** |
| 8 | `patch_dupfn` | 1784 | DUPFN | delete the **second** `fn <name>(` definition wholesale (brace-matched span) | yes | **yes** |

Notes:
- The E0203 dispatch order is fixed: `patch_ret_word` → `patch_arg_unquote`
  → `patch_del_badassign` (first applicable wins; learner.zag:2013–2017).
- `patch_type_a` (1184–1240) carries its own A/B/C shape comments but is
  **dead code** — `do_repair` never calls it. Its shape-A (`let V:i32="lit"`)
  therefore has **no live handler**.
- `similar` (1107–1125), `rewrite_call` (1127–1153), `find_fn_defs`
  (1054–1081), `count_args` (1580–1593), `match_brace` (1388–1398),
  `word_to_num` (1400–1425), `is_quoted_int` (1426–1440) are authored helpers.
- **Latent defect (found during Q3b, see RESULTS-Q3.md):** `patch_brace`
  writes its re-emitted copy into `cx` even when it returns 0; `do_repair`'s
  `if(done==0){e_raw(cx,src);}` (2034–2036) then appends the original source,
  doubling the program. Trigger: eclass=PARSE on a brace-balanced source.
- `gen`'s "self-review" (prereg: "slots filled? all called fns defined?") is
  implemented as **brace-balance counting + auto-close only**
  (learner.zag:1989–2001). `review_braces` (1291) is dead code, never called.
  The slots-called-fns check does not exist.

**Verdict (b): 8/8 repair rules authored-in-learner; 0/8 taught; 1 authored
rule (`patch_type_a`) is dead code.**

## Q2(c) — Where error classification happens

**In the driver, not the learner.** `eclass_of` (driver.py:19–26;
duplicated run_full.py:31–37) regex-classifies znc stderr:

| Eclass | Regex / substring | `details_of` (driver.py:28–38) |
|---|---|---|
| E0203 | `'E0203' in err` | — (empty) |
| UNKNOWNFN | `'unknown function' in err` | name from ``unknown function `([^`]+)` `` |
| ARITY | `'passes' in err and 'argument(s)' in err` | `name:given:expected` from `call to '(\w+)' passes (\d+) argument\(s\), expected (\d+)` |
| PARSE | `'E0001' in err` | — (empty) |
| DUPFN | `'duplicate fn' in err` | name from `duplicate fn definition '(\w+)'` |
| UNKNOWN | fallthrough | — |

The learner's `repair` mode receives only `(eclass, details, src)`
(`do_repair`: `_zag_arg(2..4)`, learner.zag:2007–2009). **The TNN never sees
raw compiler output.** Per the PREREG.md §3 claim "driver.py (thin
deterministic plumbing, no decisions)": the driver makes one load-bearing
decision — the error class — and the learner's entire repair behavior is
dispatched on that label.

**Verdict (c): classification = driver.py `eclass_of`/`details_of` (Python).
The learner classifies nothing.**

## Q2(d) — T3 error-class coverage: compile-time vs logic/runtime

All 10 T3 items (`curriculum.json` `t3[]`) with their znc error text:

| # | ID | Class | znc error text (verbatim) | Compile-time? |
|---|---|---|---|---|
| 1 | m-type-let | E0203 | `error[E0203]: expected i32, found []u8 in function main` | yes |
| 2 | m-unknown-call | UNKNOWNFN | `znc: error in main (line 4): native: call to unknown function \`ad2\`` | yes |
| 3 | m-arity-few | ARITY | `znc: error: call to 'add' passes 1 argument(s), expected 2 (in fn '…` | yes |
| 4 | m-brace | PARSE | `E0001: unexpected end of input while parsing source` | yes |
| 5 | m-dup-fn | DUPFN | `znc: error: duplicate fn definition 'dbl'` | yes |
| 6 | m-type-return | E0203 | `error[E0203]: expected i32, found []u8 in function label` | yes |
| 7 | m-unknown-intrinsic | UNKNOWNFN | `znc: error in main (line 1): native: call to unknown function \`_zag…` | yes |
| 8 | m-arity-many | ARITY | `znc: error: call to 'add' passes 3 argument(s), expected 2 (in fn '…` | yes |
| 9 | m-type-arg | E0203 | `error[E0203]: expected i32, found []u8 in call to add` | yes |
| 10 | m-brace2 | PARSE | `E0001: unexpected end of input while parsing source` | yes |

Class counts: E0203 ×3, UNKNOWNFN ×2, ARITY ×2, PARSE ×2, DUPFN ×1.

**Verdict (d): compile-time 10/10; logic/runtime 0/10.** No T3 item compiles
and then misbehaves; every fault is a compiler rejection.

## Q2(e) — Any debugging procedure (fault-finding sequence)?

**No.** Evidence:
- `grep -rni "debug\|diagnos\|fault.find\|troubleshoot\|procedure"` over
  `learner.zag`, `driver.py`, `run_full.py`, `manual.md` → zero hits
  (excluding "deliberation").
- The repair loop is: compile → driver regex-classifies stderr → learner
  applies one authored textual patch → recompile (≤6 attempts). There is no
  localize → hypothesize → test sequence, no reading of the program to find
  the fault, no symptom analysis.
- Test failures are explicitly **not** diagnosed: `driver.py` `gen_task`
  (~line 66): "test failure isn't a compiler error; can't repair via
  compiler evidence … test failures end the loop." `run_full.py` `eval_t3`
  likewise `break`s on test failure.
- The `delib` mode is a frozen bank of 12 transitive-inference logic puzzles
  (`delib_row`, learner.zag:1340+; entities alice/bob/…, middle-term
  unification) — unrelated to code debugging and never invoked by the
  drivers (zero `run_learner('delib'` hits).

**Verdict (e): no debugging procedure exists anywhere in the system.**

## Q2 overall verdict

- (a) 11/11 teach-installed IDs enumerated: **11 correct-pattern, 0 bug-knowledge**
- (b) 8/8 repair rules **authored-in-learner** (1 dead: `patch_type_a`);
  **0 taught**
- (c) error classification lives in **driver.py** (`eclass_of`/`details_of`);
  the learner never sees compiler output
- (d) T3: **10/10 compile-time**, 0/10 logic/runtime
- (e) **no debugging procedure** anywhere

**Gap-classification input:** no bug knowledge was ever installed through a
deliberative/teaching path (teach is an audit emitter; the 11 IDs are
correct-code idioms; all repair rules were authored at build time). The
REARCHITECT trigger's first condition is **not** met; the primary verdict is
**curriculum gap**, with trial-architecture findings (stateless loop,
driver-owned classification, dead `patch_type_a`, brace-only "self-review")
as required fixes distinct from the trigger.
