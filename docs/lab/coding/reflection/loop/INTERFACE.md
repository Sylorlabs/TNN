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

Spec formats (frozen, from the prior trial):
- `T1|FUNC|name=..|args=..|ret=..|op=..`, `T1|SLICE|...`, `T1|LOOP|...`,
  `T1|STR|...`, `T1|STRUCT|...`, `T1|ARGV|...`
- `T2|SORT|...`, `T2|SEARCH|...`, `T2|STR|...`, `T2|MATH|...`, `T2|SLICE|...`
- `T4|GOAL|<english goal>` — novel write-from-spec.

### `diagnose <spec> <src> <evtype> <evidence> [installed] [demo] [card]`
The deliberative core. Inputs: the spec, the current source, the evidence
type (`COMPILE`, `TEST`, `GEN`), and the evidence envelope (below).
Output:

```
DIAG class=<CLASS> strategy=<STRAT> score=<n> trace=<contributions>
@@SRC@@
<revised source, verbatim>
@@END@@
```

**Deliberation, not first-match.** Every candidate class is scored against
*all* the evidence plus cross-checks against the *source* (brace balance,
is the named identifier actually defined, duplicate-definition counts,
similar-name search). Winner by argmax; ties break in the fixed priority
order `SYNTAX > DUPFN > NAME > ARITY > TYPE > UNKNOWN`. The trace logs every
scored contribution, including rejected hypotheses
(e.g. `NAME+0:named-is-defined-conflict` — the NAME hypothesis was
considered and refuted by the source cross-check). The trace never contains
raw evidence bytes, only fixed reason strings — it is one line.

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
4. Run `znc <src> -o <bin> --no-analyze --no-zagd`; capture rc + raw stderr.
5. Run each test vector (`<bin> <args...>`, 10s timeout); byte-compare
   stdout and rc against expectations.
6. Build the envelope, call `diagnose`, parse the DIAG line + `@@SRC@@` block.
7. Enforce the budget; stop on `halt-*` or byte-identical revision.
8. Log everything.

The test comparison (step 5) is the test harness itself, not a coding
decision. The budget (max iterations) is set by the caller, not chosen
per-task by the driver.

## Logging

Per item: `id`, `mode`, `budget`, `outcome`
(`pass` | `halt-*` | `stall-guard-halt` | `diag-unparseable` | `budget-exhausted`),
`iters_used`, per-iteration records
(`n`, `evtype`, `class`, `strategy`, `score`, `trace`, `src_sha256`,
`new_src_sha256`, `evidence_sha256`, phase timings), `time_s`.
The canonical form (for determinism digests) drops all wall-clock timings.

## Determinism contract

Same battery + same learner binary + same znc → byte-identical canonical log.
Verified by `measure.py`: 3 full runs at budget 6, sha256 of the canonical
log must match. No RNG anywhere; no timestamps in the canonical log; dict
order fixed by sorted keys.

## Limits (documented, not hidden)

- argv transport: spec + source + evidence travel on the command line
  (~2MB ARG_MAX in practice; battery items are <2KB).
- Revised sources must not contain a line exactly `@@END@@`.
- The patch set is mechanical; novel logic defects outside the learner's
  generation concepts halt rather than loop forever. That halt is the
  measured behavior (see RESULTS.md), not a gap in the loop.
