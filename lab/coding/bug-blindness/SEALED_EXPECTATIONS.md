# Q3 — Sealed expectations (written BEFORE any scored run, 2026-09-21)

Predictions derived from line-level reading of the repair dispatch
(`do_repair`, learner.zag:2006–2039) and helpers. The battery is a fair
sample of novel shapes: 4 predicted recoverable, 6 predicted not.

## Q3a — same-class novel shapes (10 items)

"Repaired" = full pipeline (classify → ≤6 repair iters → compile → test
vectors) ends with compile rc=0 AND the test vector passing.

| ID | Class | Novel shape (vs T3) | Predicted znc error (verified pre-run) | Predicted outcome | Why |
|---|---|---|---|---|---|
| e1 | E0203 | `return "forty-two";` — number-word NOT in the 21-word `word_to_num` dict (1400) | `error[E0203]: expected i64, found []u8 in function label` | FAIL | `patch_ret_word`: word_to_num→-1→return 0; `patch_arg_unquote`: not a quoted-int; `patch_del_badassign`: no `="` line |
| e2 | E0203 | bad reassign with spaces: `x = "oops";` (T3 used `x="oops";`) | `error[E0203]: expected i64, found []u8 in function main` | FAIL | `patch_del_badassign` requires the exact `="` substring; spaces defeat it; no quoted-int for arg_unquote |
| u1 | UNKNOWNFN | far name `prnit(...)`, no defs in file | ``call to unknown function `prnit` `` | FAIL | `similar()` needs length-diff ≤2: \|5-10\|=5 vs `_zag_print`; no defs to match |
| u2 | UNKNOWNFN | 2-char unknown `ad(...)` nested as a call argument: `add(ad(1,2),3)` | ``call to unknown function `ad` `` | PASS → `6\n` | `similar("ad","add")`: 1 diff ≤2 → rename all `ad(`→`add(`; arity then fine |
| a1 | ARITY | two args missing: `add3(7)` vs 3 params | `call to 'add3' passes 1 argument(s), expected 3` | PASS → `24\n` | fill branch appends `, 8, 9` (lv=7 → lv+1, lv+2) → `add3(7,8,9)`=24 |
| a2 | ARITY | too few with non-numeric last arg: `cat2("x")` vs 2 `[]u8` params | `call to 'cat2' passes 1 argument(s), expected 2` | FAIL | fill parses digits of `"x"` → lv=0 → emits `, 1` → `cat2("x", 1)` → E0203 on next iter; loop exhausts |
| p1 | PARSE | missing FINAL `}` of main (EOF deletion site; T3 deleted mid-function braces) | `E0001: unexpected end of input while parsing source` | PASS → `hi\n` | `patch_brace` appends `}`×depth at EOF; depth=1 |
| p2 | PARSE | missing `}` before `return r;` — blind close-before-`fn` changes semantics | `E0001: unexpected end of input while parsing source` | FAIL (semantic) | patch closes 2 braces before `fn main`; while swallows `return r;` → f(3)=3, test expects 6 → compiles but test FAILS |
| d1 | DUPFN | non-identical bodies; test expects the SECOND (`return 2;`) | `duplicate fn definition 'val'` | FAIL | `patch_dupfn` always deletes the second def → prints `1`, test expects `2` |
| d2 | DUPFN | identical semantics, different param names (`n` vs `x`) | `duplicate fn definition 'dbl'` | PASS → `42\n` | second def deleted by name match; kept def gives dbl(21)=42 |

**Sealed Q3a tally prediction: 4/10 repaired → KB-R1 FAIL** (bar: ≥7/10 to pass).

## Q3b — mislabel probe (5 items, `repair` mode DIRECT, no driver)

"Recovers" = learner output compiles AND passes the item's tests.

| ID | True fault | Source | Wrong label fed to `repair` | Predicted |
|---|---|---|---|---|
| b1 | ARITY | m-arity-few (`add(3)`) | `("E0203", "")` | no recovery — none of the 3 E0203 patches match |
| b2 | E0203 | m-type-let (`x="oops";`) | `("ARITY", "x:1:2")` | no recovery — no `fn x(` def → nparams<0 → return 0 |
| b3 | PARSE | m-brace | `("DUPFN", "main")` | no recovery — single `fn main(` → second<0 → return 0 |
| b4 | DUPFN | m-dup-fn | `("PARSE", "")` | no recovery — braces balanced → changed=0 → src echoed |
| b5 | UNKNOWNFN | m-unknown-call | `("E0203", "")` | no recovery — no `return "`; no quoted-int; no `="` line |

**Sealed Q3b prediction: 0/5 recover → KB-R2 CONFIRMED** (no independent
diagnosis; driver's label is load-bearing).

## Q3c — novel-class probe (4 items; `eclass_of` verified UNKNOWN pre-run)

| ID | Fault | znc error text (verified) | `eclass_of` | Predicted |
|---|---|---|---|---|
| c1 | read of undeclared `y` | `native: unknown identifier in expression: y` | UNKNOWN | no recovery — driver dispatches nothing for UNKNOWN |
| c2 | unknown struct field `p.z` | `native: unknown struct field` | UNKNOWN | no recovery |
| c3 | no `main` function | `native: no main function found` | UNKNOWN | no recovery |
| c4 | duplicate struct `P` | `duplicate type definition 'P'` | UNKNOWN | no recovery |

**Sealed Q3c prediction: 0/4 recovery rate.**

## Method notes (sealed)

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze`
  (same flags as driver.py).
- Q3a: replicate `driver.repair_task` exactly (import `eclass_of`,
  `details_of`, `run_learner`, `compile_src`, `run_tests` from driver.py),
  6 attempts, 5 reps per item; record sha256 of final source per rep;
  require 5/5 byte-identical.
- Q3b: `src/learner repair <wrong-eclass> <wrong-details> <src>` directly;
  single shot (no driver loop); then compile+test the output.
- Q3c: full `repair_task` pipeline; record eclass per attempt.
- "Repaired"/"recovers" always means compile rc=0 AND the item's test vector
  passes — mirroring `repair_task`'s own success criterion.
