# Fast-Loop Harness — Interface Contract

`coding/reflection/loop/` — the explicit generate → compile → run → test →
diagnose → revise loop for the coding-reflection workstream. The task crews
(reflection/architecture, synth, OS pieces, coding battery) build on this.

## The law

**Every coding decision lives in the Zag learner. The driver is plumbing.**

- The learner (`learner.zag`) decides: what code to generate (`gen`), how to
  classify a failure and what repair strategy to attempt (`diagnose`), and
  when to stop (`halt-*` strategies).
- The driver (`driver.py`) does NOT: classify errors (no regexes / keyword
  scans on compiler output — verify with
  `grep -nE "E0203|unknown function|argument\(s\)" driver.py`, which must hit
  nothing outside comments), choose repairs, edit code, or interpret test
  failures beyond byte comparison. It invokes binaries, moves bytes, enforces
  the iteration budget, and logs everything.
- This is the correction to the prior trial's attribution gap
  (`coding/CODING_REPORT.md` CORRECTION 2026-09-22): there, the driver's
  `eclass_of`/`details_of` regexes classified errors in Python. Here the
  driver passes compiler stderr and test results **verbatim**; classification
  happens in `learner.zag`'s `diagnose` mode.

## Learner protocol

Binary: `work/learner`, built from `learner.zag` (see `build.sh`).
Pure Zag, zero RNG. All modes are pure functions of argv.

### `gate <spec>`
Refusal check. Prints `ALLOW` or `REFUSE:G<n>`. The driver routes REFUSE to
outcome `gate-refused` before any generation.

### `gen <spec> <installed-csv> <demo> [card]`
Generates a program from spec + installed knowledge. Prints Zag source, or a
**failure sentinel** the driver routes (protocol-level, like a return code —
not diagnosis) to `diagnose` as `evtype=GEN`:
`UNKNOWN_GOAL`, `UNTAUGHT:<pattern>`, `NEED_CARD:<topic>`, `UNKNOWN_TIER`,
`REFUSED:G<n>`.

### `precheck <spec> <src>`
Fail-fast compile precheck (promotion P3, 2026-09-22). The learner predicts
whether `<src>` will compile from the source alone (brace balance,
defined-name check, duplicate-definition check, arity-vs-definition).
Output: `PRECHECK OK`, or `PRECHECK FAIL` followed by reason lines in
znc-diagnostic vocabulary. The driver routes `PRECHECK FAIL` (first output
line only, sentinel-style — like a return code, not diagnosis) straight to
`diagnose` as `evtype=PRECHECK` with the reason text VERBATIM, skipping the
znc invocation; the driver classifies nothing.

Spec formats (frozen, from the prior trial):
- `T1|FUNC|name=..|args=..|ret=..|op=..`, `T1|SLICE|...`, `T1|LOOP|...`,
  `T1|STR|...`, `T1|STRUCT|...`, `T1|ARGV|...`
- `T2|SORT|...`, `T2|SEARCH|...`, `T2|STR|...`, `T2|MATH|...`, `T2|SLICE|...`
- `T4|GOAL|<english goal>` — novel write-from-spec.

### `diagnose <spec> <src> <evtype> <evidence> [installed] [demo] [card] [mask]`
The deliberative core. Inputs: the spec, the current source, the evidence
type (`COMPILE`, `TEST`, `GEN`, `PRECHECK`), and the evidence envelope
(below).
Output:

```
DIAG class=<CLASS> strategy=<STRAT> score=<n> evals=<n> trace=<contributions>
@@SRC@@
<revised source, verbatim>
@@END@@
```

`evals` is the deterministic count of hypothesis-evaluations (promotion P2).

**Deliberation, not first-match.** The COMPILE branch scores candidate
classes against *all* the evidence plus cross-checks against the *source*
(brace balance, is the named identifier actually defined,
duplicate-definition counts, similar-name search). Winner by argmax; ties
break in the fixed priority order
`SYNTAX > DUPFN > NAME > ARITY > TYPE > UNKNOWN`. The trace logs every
scored contribution, including rejected hypotheses
(e.g. `NAME+0:named-is-defined-conflict` — the NAME hypothesis was
considered and refuted by the source cross-check). The trace never contains
raw evidence bytes, only fixed reason strings — it is one line.

**Combo diagnose (default, promotion P2).** `mask` absent or `"ab"`: the
COMPILE branch first prunes provably-dead classes (a class whose every
scoring statement needs an evidence trigger that is absent scores 0 and
logs no trace lines — skipping it is a silent no-op), then runs one-brain
branch-and-bound over the pruned survivor set: classes evaluated in fixed
descending historical win-rate order (TYPE, NAME, ARITY, SYNTAX, DUPFN),
stopping as soon as no unevaluated non-pruned class can take the argmax
(the leader's score strictly exceeds every remaining survivor's theoretical
maximum, or ties it while outranking every remaining survivor that could
tie it on the frozen priority order). Pruned classes emit a
`<CLASS>+0:pruned-no-trigger` trace line; classes skipped by the stop rule
emit no trace lines. Winners are byte-identical to the full evaluation.

**Escape hatch.** `mask="classic"` runs the old full-evaluation path (all
five classes scored in baseline order, no skips) — the control/rollback
path for the promotion regression battery.

Failure classes and strategies:

| class | meaning | strategy |
|---|---|---|
| SYNTAX | parse failure | `patch-brace` — close unbalanced braces |
| NAME | unknown identifier/fn | `patch-unknownfn` — rewrite to similar defined name |
| ARITY | wrong arg count | `patch-arity` — drop/pad call args to the definition |
| TYPE | type mismatch (E0203 et al.) | `patch-type-retword` / `-argunquote` / `-delbadassign` |
| DUPFN | duplicate fn definition | `patch-dupfn` — delete the second definition |
| GEN_FAILURE | gen emitted a sentinel | `halt-genfail` |
| RUNTIME | panic/stderr or rc mismatch | `halt-runtime` |
| OUTPUT_FORMAT | outputs equal modulo trailing whitespace | `patch-add-newline` / `patch-strip-newline` |
| LOGIC_VALUE | integer outputs differ (delta analyzed: off-by-one, sign-flip, value) | `regen-from-spec` — discard broken logic, regenerate via the `gen` path |
| LOGIC_OTHER | non-integer behavioral difference | `halt-unknown` |
| UNKNOWN | nothing scored | `halt-no-patch` / `halt-unknown` |

**Halting is a learner decision.** `halt-*` strategies stop the loop:
`halt-genfail` (nothing to repair — knowledge missing), `halt-runtime`
(cannot map a panic to a source edit from this evidence), `halt-no-patch`
(no applicable patch), `halt-noregen` (spec not generable),
`halt-thrash` (same class twice with no source change),
`halt-cycle` (a previously seen source recurred — A→B→A oscillation).
The driver additionally stops on a byte-identical revision (`stall-guard-halt`)
as belt and braces; the learner is designed never to need it.

**Regeneration vs patching.** For `LOGIC_VALUE` the learner does not guess
edits: it analyzes the numeric delta (trace records off-by-one / sign-flip /
value-delta), then either regenerates from the spec through the normal
generation path or halts if the spec is not generable. Patching is reserved
for mechanical defects; logic defects get re-derivation or an honest halt.

## Evidence envelope (driver → learner)

Built by the driver; compiler/test bytes are verbatim (only the run-specific
source *directory* is folded to the basename for determinism — the filename
and all diagnostic content are preserved).

- `COMPILE`: `"RC <n>\n"` + raw znc stderr, verbatim.
- `PRECHECK`: the learner's `precheck` reason lines, verbatim (znc-diagnostic
  vocabulary, so the same COMPILE scorers apply).
- `TEST`: `"COMPILE_OK\nGOT_RC <n>\nEXP_RC <m>\nGOT_ERR <esc>\nGOT_OUT <esc>\nEXP_OUT <esc>\n"`
  where `<esc>` is lossless backslash escaping (`\`→`\\`, newline→`\n`,
  CR→`\r`). Only the **first failing** test vector is reported.
- `GEN`: `"GENFAIL <sentinel>\n"`.
- Trailer (driver-maintained history, all three always present):
  `"PREV <class>/<strategy>\nSTALLED <0|1>\nCYCLE <0|1>\n"`
  `PREV` is the previous iteration's diagnosis (`none/none` on iteration 1);
  `STALLED` is 1 when the source is byte-identical to the previous iteration;
  `CYCLE` is 1 when the current source hash was seen in an earlier iteration.

## Driver contract (what the driver may do)

1. `gate` check; route REFUSE.
2. `gen` (mode=gen) or take the provided seed (mode=seed).
3. Write source to `<workdir>/<id>_i<iter>.zag` (truncating writes).
4. Fail-fast precheck (always-on unless `--no-precheck`): ask the learner
   `precheck <spec> <src>`; `PRECHECK FAIL` on the first output line routes
   to `diagnose` with `evtype=PRECHECK` (reason text verbatim), skipping znc.
   Sentinel-style routing only — the driver classifies nothing.
5. Run `znc <src> -o <bin> --no-analyze --no-zagd`; capture rc + raw stderr.
6. Run each test vector (`<bin> <args...>`, 10s timeout); byte-compare
   stdout and rc against expectations.
7. Build the envelope, call `diagnose` (mask `"ab"` default, `"classic"`
   escape hatch), parse the DIAG line + `@@SRC@@` block.
8. Enforce the budget (default 4, the Arm 1 knee — promotion P1; overridable
   with `--budget`); stop on `halt-*` or byte-identical revision.
9. Log everything. Every precheck-FAIL source is also appended to
   `<out>.fp_candidates.jsonl` for post-hoc false-positive validation
   (validation compiles are excluded from the loop's znc count).

The test comparison (step 6) is the test harness itself, not a coding
decision. The budget (max iterations) is set by the caller, not chosen
per-task by the driver.

## Logging

Per item: `id`, `mode`, `budget`, `outcome`
(`pass` | `halt-*` | `stall-guard-halt` | `diag-unparseable` | `budget-exhausted`),
`iters_used`, per-iteration records
(`n`, `evtype`, `class`, `strategy`, `score`, `evals`, `trace`, `src_sha256`,
`new_src_sha256`, `evidence_sha256`, `znc`, `precheck`, phase timings),
`time_s`. `znc` is 1 when the iteration invoked znc (0 when a precheck-FAIL
or GEN route skipped it); `precheck` is `ok`/`fail`/`n/a`/`n/a-gen`;
`evals` is the learner-reported hypothesis-evaluation count.
The canonical form (for determinism digests) drops all wall-clock timings.

## Determinism contract

Same battery + same learner binary + same znc → byte-identical canonical log.
Verified by `measure.py`: 3 full runs at budget 4 (the new default),
sha256 of the canonical log must match. No RNG anywhere; no timestamps in
the canonical log; dict order fixed by sorted keys.

## Escape hatches (promotion rollback without code revert)

- `--no-precheck` disables the fail-fast precheck routing (P3).
- `--mask classic` restores the old full-evaluation diagnose path (P2).
- `--budget 6` restores the old iteration budget (P1).
Runtime rollback: `--budget 6 --no-precheck --mask classic`. Code rollback:
`git revert` the promotion commit (the frozen prereg commit stands).

## Limits (documented, not hidden)

- argv transport: spec + source + evidence travel on the command line
  (~2MB ARG_MAX in practice; battery items are <2KB).
- Revised sources must not contain a line exactly `@@END@@`.
- The patch set is mechanical; novel logic defects outside the learner's
  generation concepts halt rather than loop forever. That halt is the
  measured behavior (see RESULTS.md), not a gap in the loop.
