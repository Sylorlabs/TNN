# Q3 — Repair diagnosis: results (2026-09-21)

Battery: `q3_run.py` (imports `eclass_of`/`details_of`/`run_learner`/
`compile_src`/`run_tests` from `driver.py`; the repair loop is an exact
replica of `driver.repair_task`). Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze`.
Expectations were sealed in `SEALED_EXPECTATIONS.md` before the scored runs.

"Repaired" = full pipeline (classify → ≤6 repair iters → compile → test
vectors) ends with compile rc=0 AND the item's test vector passing —
`repair_task`'s own success criterion.

## Q3a — same-class novel shapes: 5/10 repaired → KB-R1 FAIL

All 10 pre-verified to fail compilation with the claimed class (see log).
5 reps each; all 5/5 byte-identical per item (sha256 digests in
`logs/q3_report.json`).

| ID | Class | Novel shape | Result (5 reps) | Iters | Sealed prediction | Match? |
|---|---|---|---|---|---|---|
| e1 | E0203 | `return "forty-two";` — word outside the 21-word `word_to_num` dict | 0/5 | 6,6,6,6,6 | FAIL | ✓ |
| e2 | E0203 | `x = "oops";` — spaces around `=` defeat the exact `="` match | 0/5 | 6,6,6,6,6 | FAIL | ✓ |
| u1 | UNKNOWNFN | `prnit(...)` — edit distance >2 from every def/intrinsic | 0/5 | 6,6,6,6,6 | FAIL | ✓ |
| u2 | UNKNOWNFN | `ad(...)` nested as call arg, renamed to `add` | 5/5 → `6` | 2 | PASS | ✓ |
| a1 | ARITY | 2 args missing: `add3(7)` → filled `, 8, 9` | 5/5 → `24` | 2 | PASS | ✓ |
| a2 | ARITY | non-numeric last arg: `cat2("x")` → filled `, 1` | 5/5 → `7` | 2 | FAIL | ✗ |
| p1 | PARSE | missing final `}` of main (EOF deletion site) | 5/5 → `hi` | 2 | PASS | ✓ |
| p2 | PARSE | missing `}` closed at wrong site → f(3)=3 vs expected 6 | 0/5 (test fail) | 2 | FAIL | ✓ |
| d1 | DUPFN | non-identical bodies, test expects second (`return 2;`) | 0/5 (test fail) | 2 | FAIL | ✓ |
| d2 | DUPFN | same semantics, different param names (`n` vs `x`) | 5/5 → `42` | 2 | PASS | ✓ |

**KB-R1: 5/10 < 7/10 → FAIL. Matching is brittle even within class.**

Notes:
- **a2 surprise (sealed prediction wrong, 9/10 predictions correct):** I
  predicted the fill heuristic's `, 1` would produce E0203
  (`cat2("x", 1)` with `b:[]u8`). Empirically znc **accepted** the integer
  literal where `[]u8` was expected (no E0203 — the typed check is
  asymmetric: `"3"`→`i32` param errors, but `1`→`[]u8` param does not), and
  `cat2` ignores its args, so the test passed. The repair is real by the
  pipeline's criterion, but the mechanism is luck, not diagnosis: the
  heuristic emitted a type-incorrect call that happened to compile.
- e1/e2/u1 each burned all 6 iterations with the source returned unchanged
  every time (dispatch found no applicable patch; `done==0` → echo).
- p2 and d1 are the instructive failures: the pipeline "fixed" the compile
  error but produced the wrong program (blind brace-closing swallowed
  `return r;`; delete-second kept the wrong definition). Compile-error
  disappearance ≠ bug fixed.

## Q3b — mislabel probe: 0/5 recover → KB-R2 CONFIRMED

`src/learner repair <wrong-eclass> <wrong-details> <src>` directly, single
shot, then compile+test the output:

| ID | True fault | Wrong label | Output | Recovers? |
|---|---|---|---|---|
| b1 | ARITY (m-arity-few) | E0203 | UNCHANGED | no |
| b2 | E0203 (m-type-let) | ARITY/`x:1:2` | UNCHANGED | no |
| b3 | PARSE (m-brace) | DUPFN/`main` | UNCHANGED | no |
| b4 | DUPFN (m-dup-fn) | PARSE | CHANGED (source doubled — see defect note) | no |
| b5 | UNKNOWNFN (m-unknown-call) | E0203 | UNCHANGED | no |

**KB-R2: 0/5 → CONFIRMED. No independent diagnosis exists; the driver's
label is fully load-bearing.** With the wrong label the learner either
echoes the source or corrupts it; it never re-diagnoses from the code.

**Latent defect found (b4):** `patch_brace` (learner.zag:1733) writes its
re-emitted copy into `cx` even when it returns 0 (no change). `do_repair`
then appends the original source (`if(done==0){e_raw(cx,src);}`,
learner.zag:2034–2036), **doubling the program** (148→295 bytes, 2→4
`fn dbl` occurrences, measured). Trigger: eclass=PARSE on an already
brace-balanced source. Never fires in the T3 battery (both PARSE items are
genuinely unbalanced), but any mislabeled-PARSE input gets corrupted
instead of echoed. (`patch_unknownfn` is safe here — it returns before
`rewrite_call` when nothing matches.)

## Q3c — novel-class probe: 0/4 recovery

All four verified `eclass_of(...) == UNKNOWN` before the runs:

| ID | Fault | znc error text | Result |
|---|---|---|---|
| c1 | read of undeclared `y` | `native: unknown identifier in expression: y` | 6 iters, all UNKNOWN, not repaired |
| c2 | unknown struct field `p.z` | `native: unknown struct field` | 6 iters, all UNKNOWN, not repaired |
| c3 | no `main` function | `native: no main function found` | 6 iters, all UNKNOWN, not repaired |
| c4 | duplicate struct `P` | `duplicate type definition 'P'` | 6 iters, all UNKNOWN, not repaired |

**Recovery rate 0/4**, as expected: the driver dispatches nothing for
UNKNOWN and the learner echoes the source each attempt.

## Artifacts

- `q3_run.py` — battery runner (deterministic; imports driver.py)
- `SEALED_EXPECTATIONS.md` — predictions sealed pre-run (9/10 correct)
- `logs/q3_run.log` — full run log
- `logs/q3_report.json` — machine-readable results + digests

## Q3 bottom line

| Bar | Result |
|---|---|
| KB-R1 (≥7/10 same-class novel shapes repaired) | **FAIL** — 5/10 |
| KB-R2 (mislabel: 0/5 → no independent diagnosis) | **CONFIRMED** — 0/5 |
| Q3c novel-class recovery | 0/4 |
