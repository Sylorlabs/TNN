# BUG-BLINDNESS — Final Verdict

**Crew:** bug-blindness (Micah order 2026-09-21)
**Prereg:** `70807baa8f3f` (frozen), amended by **Micah 2026-09-21 direct order**:
"TNN MUST catch everything the compiler catches, by reading, no compiler"
— Q1 expanded to the full 12-class compiler catalog; new headline bar KB-D1C.
**Date:** 2026-09-22

## Headline

**Micah's bar is MET: 24/24 compiler parity by reading, no compiler.**
The TNN — given a program encoded as facts and its deliberative inference
machinery — catches everything the compiler catches, plus bug classes the
compiler itself is blind to. It does not merely match the compiler; on the
tested battery it exceeds it.

## Q1 — Detection without the compiler: YES

Instrument: `inspect.zag` (pure Zag, zero RNG). An authored parser encodes
program text into integer fact tables (DEF/CALL/ARITY/DECL/ASSIGN/USE/LOOP/
COND/STRUCT/BRACE + spec intent); deliberative checks then run genuine
inference over the tables (middle-term unification in the style of the
learner's `delib`: every CALL callee unified against every DEF row, every USE
against dominating ASSIGN rows, etc.). **Declared boundary:** text→facts is
authored parsing; the checks are general inference, not source-text regexes —
the same check code handles all 38 programs.

Battery: 38 FRESH programs (not T3 items), answer key sealed before scoring
(`2bccc18e…`), 5/5 byte-identical reps. Compiler catalog enumerated by direct
probing of the pinned toolchain (12 classes).

| Bar | Score | Rule | Verdict |
|---|---|---|---|
| KB-D1C compiler parity (24 items, 12×2) | **24/24 = 1.0000** | ≥ 0.85 | **PASS** |
| KB-D1 detection (30 buggy) | 30/30 = 1.0000 | ≥ 0.70 | PASS |
| KB-D1 false alarms (8 clean) | 0/8 = 0.0000 | ≤ 0.25 | PASS |
| KB-D2 class+line precision | 30/30 = 1.0000 | ≥ 0.60 | PASS |

Per-class parity — all 12 classes 2/2, **zero gaps**: E0001, E0002, E0010,
E0203 (all 5 shapes: let-assign, return, call-arg, return-in-void,
void-as-value), UNKNOWN-IDENT (incl. unparenthesized conditions),
UNKNOWN-FN, ARITY, DUP-FN, DUP-TYPE, UNKNOWN-FIELD, NO-MAIN, BAD-INDEX.

Stretch (beyond-compiler, reported separately): UNINIT-VAR 2/2, OFF-BY-ONE
2/2, WRONG-COMPARISON 2/2. Compiler blind spots (undeclared `x=5`,
struct-field type mismatch, `let` redeclaration — all compile) correctly
reported CLEAN: 0 false alarms, as required.

No close-the-gap prescriptions needed: there are no gaps. What made it work
is worth recording: the paren-requirement (curriculum idiom #1) as a CHECK
catches the whole `unknown identifier in expression: >` family; unification
of CALL against DEF catches unknown-fn/arity/dup-fn as one mechanism, not
three.

## Q2 — Knowledge audit: it never HAD bug knowledge (AUDIT.md)

- (a) **Teach-installed IDs: 11/11 enumerated, 11 correct-pattern, 0
  bug-knowledge** (`p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,
  p_sort,p_argv,p_strcnt,p_slicefill`). Passed straight to `gen`; `teach`
  mode is **never invoked** by either driver; `do_teach`
  (learner.zag:1306–1320) is an audit-line emitter that installs nothing.
  `grep -i bug` in learner.zag: zero hits.
- (b) **Repair rules: 8/8 authored-in-learner, 0/8 taught**
  (`patch_ret_word`:1442, `patch_arg_unquote`:1463,
  `patch_del_badassign`:1490, `patch_unknownfn`:1155, `patch_arity`:1596,
  `patch_brace`:1733, `patch_dupfn`:1784; plus `patch_type_a`:1184 which is
  **dead code** — never called).
- (c) **Classification lives in the Python driver** (`eclass_of`/
  `details_of`, driver.py:19–38). The learner's `repair` mode receives only
  `(eclass, details, src)` and never sees compiler output.
- (d) **T3: 10/10 compile-time, 0/10 logic/runtime.**
- (e) **No debugging procedure exists anywhere.** Test failures explicitly
  end the loop undiagnosed (driver.py:~66); `delib` is 12 frozen puzzles,
  never invoked by drivers. The prereg's "self-review" is brace-counting +
  auto-close only; the claimed "called fns defined?" check doesn't exist
  (`review_braces`:1291 is dead code).

**Gap-classification input:** no bug knowledge was ever installed through a
deliberative/teaching path → the rearchitect trigger's first condition is
NOT met → **curriculum gap** is the primary verdict.

## Q3 — Repair diagnosis: pattern matching, confirmed (RESULTS-Q3.md)

- (a) Same-class novel shapes: **5/10 → KB-R1 FAIL** (<7/10). All 10
  pre-verified to fail with the claimed class; 5/5 reps byte-identical.
  Survived: near-miss rename, 2-arg fill, EOF brace, dup-fn param variant,
  one arity (znc accepted ill-typed `cat2("x",1)` — luck, not diagnosis).
  Failed: word outside the 21-word dict, spaces around `=`, edit distance
  >2, blind brace-close that changed semantics (compiled, wrong output),
  delete-second that kept the wrong body.
- (b) Mislabel probe: **0/5 → KB-R2 CONFIRMED.** Wrong eclass → source
  echoed unchanged; zero independent diagnosis; the driver's label is fully
  load-bearing.
- (c) Novel classes: **0/4.** `eclass_of`→UNKNOWN, driver attempts nothing.

**Latent defect (new):** `patch_brace` writes its re-emitted copy into `cx`
even when returning 0; the `if(done==0){e_raw(cx,src);}` fallback then
**doubles the program** (measured 148→295 bytes on mislabeled-PARSE input).
Never fires on the T3 battery; corrupts any mislabeled-PARSE input. Must fix.

## Q4 — Learning from the compiler talking back: the loop is a crutch (q4/TRANSFER_REPORT.md)

**Architectural proof** (learner.zag, exact): ll.10–12 pure functions of
inputs; ll.1306–1319 `do_teach` prints audit only; ll.2006–2039 `do_repair`
argv→patches→stdout with no persistence; **zero `_zag_raw_syscall`** (no
file writes possible); ll.2041–2050 fresh dispatch per mode; driver.py:42–45
fresh subprocess per call. Learner binary unchanged across the repair
experience (sha256 `ac7f6e3b…`). **Transfer is architecturally impossible —
statelessness, not the ceiling, is the binding constraint.** The compiler's
feedback is consumed by Python regexes; the TNN never sees an error.

**Empirical:** 6/6 ARITY repairs with compiler feedback (logged); inspector
on 8 fresh ARITY + 8 fresh UNINIT (control) probes before vs after:

| Probe set | PRE | POST | Δ |
|---|---|---:|---:|
| ARITY | 8/8 | 8/8 | 0pp |
| UNINIT control | 8/8 | 8/8 | 0pp |

**KB-T1: FAIL** (mechanical — no +30pp gain; transfer unmeasurable at
ceiling, and impossible by construction).

**Generation bound (honest, sealed):** first-attempt `gen` on 6 fresh specs
with unseen ops: **1/6** (sealed bar ≥5/6 not met; prediction wrong,
reported). The learner emits correct bodies only for authored ops
(`sum,max,fact,is_even,count_pos,gcd,is_prime,fib`); unseen ops get empty
bodies the repair loop cannot fix. The "beautiful code" claim is bounded by
the authored op inventory. (Sequencing note: labeled pre-equivalent replay
from the unchanged stateless executable, not a chronological PRE — flagged
openly in TRANSFER_REPORT.md.)

## Gap classification (frozen rule applied)

- **Primary: curriculum gap.** The TNN was never taught bug knowledge; the
  repair machinery was authored around it, not learned by it.
- **Rearchitect trigger: DOES NOT FIRE.** Its first condition (knowledge was
  installed) is not met.
- **Trial-architecture gaps (required fixes, distinct from the trigger):**
  stateless repair loop, driver-owned classification, dead code
  (`patch_type_a`, `review_braces`), brace-only "self-review",
  `patch_brace` doubling defect.

## Recommendation (no TNN rearchitect — a teaching rearchitect)

Nothing about the TNN's machinery failed: with knowledge-shaped input (the
fact encoding) its deliberative inference hits 24/24 parity plus
beyond-compiler classes. What failed is everything around it. To make
"learning from the compiler talking back" real:

1. **Teach bug knowledge deliberately** — fault classes, the paren
   principle, assign-before-use dataflow, spec-vs-bound checking — through
   the teach/deliberative path, not baked patches. Q1 proves the machinery
   can use it once it has it.
2. **Move classification into the TNN** — compiler stderr enters as an
   untrusted observation the TNN reads and diagnoses with its
   Q1-demonstrated reading ability; delete the Python regexes.
3. **Give the loop memory** — repair episodes must be able to install
   knowledge (repair `do_teach` from no-op to real; add a persistent store).
   Until then the transfer question is untestable by construction.
4. **Fix `patch_brace`** doubling on mislabeled-PARSE input.
5. **Generation:** extend the op inventory or teach op-composition — 1/6 on
   unseen ops bounds current generation to authored ops.

## Artifacts

- `PREREG-BB.md` (frozen `70807baa8f3f`, amended by Micah 2026-09-21 order)
- `inspect.zag` + `battery/parity/` (38 items, sealed key `2bccc18e…`)
- `AUDIT.md`, `SEALED_EXPECTATIONS.md`, `RESULTS-Q3.md`, `q3_run.py`
- `q4/` (16 probes, sealed keys, `TRANSFER_REPORT.md`, gen specs)
- `run_bb1_parity.py`, `run_bb1_q4_gen.py`, `run_bb1_repairs.py`,
  `verify_bb.py`, `MANIFEST_A.sha`, `logs/`
- Commit: this verdict (below). Night-run log updated.
