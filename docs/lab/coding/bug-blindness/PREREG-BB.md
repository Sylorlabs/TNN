# BUG-BLINDNESS CREW — Preregistration (frozen 2026-09-21)

**Order:** Micah 2026-09-21 — "TNN at code is amazing and creates beautiful code... but TNN at bugs shits the floor. That's weird and worth investigating."
**Status:** FROZEN. Any change to questions, batteries, bars, or metrics needs a dated amendment.
**Commit rule:** this file is committed alone before any scored run.

## Background findings (from source audit, pre-freeze)

- `learner.zag` `repair` mode = handwritten surgical patches dispatched on an
  error-class string (E0203 shapes A/B/C, UNKNOWNFN, ARITY, PARSE, DUPFN).
- Error classification (`eclass_of`) lives in **Python** (`driver.py` regexes),
  not in the TNN. The TNN never sees raw compiler output.
- `teach` mode is an audit-line emitter; it installs nothing into a live store.
  All patterns and repair rules were baked at learner-build time by `gen_code.py`.
- `gen` "self-review" (prereg claimed "slots filled? all called fns defined?")
  is implemented as brace-balance counting + auto-close only.
- T3's 10 items are all **compile-time** errors. No logic/runtime bug was ever
  in the curriculum.
- These are pre-freeze observations, not verdicts. The four questions below
  test them with numbers.

## Q1 — DETECTION WITHOUT THE COMPILER

Can the TNN find bugs by READING code — no compiler, no execution?

**Instrument:** `inspect.zag` (new pure-Zag binary). An authored parser encodes
the program text into integer fact tables; the TNN's deliberative machinery
then runs genuine inference over the tables (middle-term unification in the
style of the learner's `delib` — e.g., unifying each CALL's callee against
every DEF row). The text→facts encoding is authored parsing and is declared
as the instrument boundary; the CHECKS are deliberative inference, not
source-text regexes.

Fact tables: DEF(name), CALL(caller,callee,line), ARITY_DEF(fn,n),
ARITY_CALL(callee,n,line), DECL(var,type,fn), ASSIGN(var,line,fn),
ASSIGN_LIT(var,litkind,line), USE(var,line,fn), LOOP(fn,line,var,init,op,bound),
SPEC_RANGE(task,lo,hi,inclusive), COND(fn,line,op,lhs_kind), SPEC_COND(task,op),
BRACE_DEPTH(eof_depth).

Deliberative checks (each a scan+unification over tables):
1. UNKNOWN-CALL — CALL callee unifies with no DEF row → BUG
2. ARITY — CALL arg count vs unified ARITY_DEF mismatch → BUG
3. UNINIT-VAR — USE with no ASSIGN row same (var,fn) at earlier line → BUG
4. TYPE-MISMATCH — ASSIGN_LIT kind incompatible with DECL type → BUG
5. OFF-BY-ONE — LOOP (init,op,bound) iteration count vs SPEC_RANGE → BUG
6. WRONG-COMPARISON — COND op inverted vs SPEC_COND → BUG
7. DUP-FN — two DEF rows unify on name → BUG
8. MISSING-BRACE — eof brace depth ≠ 0 → BUG

**Battery:** 24 FRESH programs (not the T3 items): 8 clean, 16 buggy
(8 classes × 2). Output per item: `CLEAN` or `BUG <class> <line>`.

| Bar | Rule |
|---|---|
| KB-D1 detection | buggy-item detection accuracy < 0.70 (i.e. <12/16) OR clean false-alarm > 0.25 (>2/8) → FAIL: cannot detect by reading |
| KB-D2 class precision | of detected bugs, correct fault class < 0.60 → FAIL: finds anomalies, not diagnoses |

Chance baseline for the binary decision is 0.50; class+line chance ≈ 0.06.

## Q2 — KNOWLEDGE AUDIT

Did the TNN ever HAVE bug knowledge? Systematic source audit of
`curriculum.json`, `CURRICULUM_REPORT.md`, `learner.zag`, `driver.py`,
`run_full.py`.

Report exactly:
- (a) every pattern ID installed via `teach`, classified correct-pattern vs bug-knowledge;
- (b) every repair rule: authored-in-learner vs taught;
- (c) where error classification happens (learner vs driver);
- (d) T3 error-class coverage: compile-time vs logic/runtime;
- (e) whether any debugging procedure (a sequence for finding a fault) exists anywhere.

No numeric bar — this is an audit. It must enumerate 100% of teach-installed
IDs. Its verdict feeds the gap-classification rule below.

## Q3 — REPAIR DIAGNOSIS: real diagnosis or error-message pattern matching?

- **(a) Same-class novel shapes:** 10 NEW broken programs with the same 5
  error classes (E0203/UNKNOWNFN/ARITY/PARSE/DUPFN) but surface shapes the
  authored patches never saw (e.g., E0203 via a 4th syntactic shape; PARSE via
  a different deletion site; ARITY via a different call shape). Full pipeline
  (driver classify → learner repair → compile → vectors).
  - KB-R1: < 7/10 repaired → FAIL: matching is brittle even within class.
- **(b) Mislabel probe:** 5 items run through `repair` mode DIRECTLY (bypassing
  the driver) with a WRONG eclass for their true fault.
  - KB-R2: 0/5 recover correctly → CONFIRMED: no independent diagnosis; the
    driver's label is load-bearing. (≥1/5 recovery would indicate some
    diagnosis independent of the label.)
- **(c) Novel-class probe:** 4 items with fault classes outside the 5
  (e.g., a fault producing an error text the driver regexes don't match).
  Report the recovery rate; the driver is expected to return UNKNOWN and
  attempt nothing.

## Q4 — LEARNING FROM THE COMPILER TALKING BACK

After the TNN repairs N bugs of one class WITH compiler feedback, does
first-attempt behavior on FRESH items of that class improve WITHOUT the
compiler — i.e., does a repair episode install durable, transferable knowledge?

- **Architectural fact (prove from source):** does any repair-episode output
  reach any persistent store the learner consults on later invocations?
  (Learner processes are stateless across invocations; teach is an audit
  emitter.) State the fact with file/line evidence.
- **Empirical:** repair experience = 6 ARITY repairs with compiler feedback
  (logged). Probe = Q1 inspector on 8 FRESH ARITY-buggy items + 8 FRESH
  UNINIT-buggy items (control class, never repaired), scored BEFORE vs AFTER
  the repair experience.
  - KB-T1: post-experience ARITY detection < pre + 30pp, or not above the
    UNINIT control → FAIL: repair does not transfer; the loop is a crutch,
    not learning.
- Also record first-attempt `gen` on 6 fresh specs pre/post (expected
  degenerate — gen emitters are correct-by-construction; report as
  unmeasurable headroom if 100%/100%).

## Gap-classification rule (frozen)

- If Q2 finds bug knowledge WAS installed through a deliberative/teaching
  path AND Q1 fails KB-D1 → **REARCHITECT trigger FIRES**: knowledge present
  but undetectable = architecture gap. Escalate explicitly.
- If Q2 finds NO bug knowledge was ever installed → **curriculum gap** is the
  primary verdict. Separately report any trial-architecture findings (e.g.,
  stateless loop, driver-owned classification) as required fixes distinct
  from the trigger.

## Determinism

Zero RNG in any decision path. Q1, Q3a, Q4 batteries: 5 reps byte-identical
(digests). Independent `verify_bb.py` oracle recomputes all metrics from logs.

## Deliverables

`docs/lab/coding/bug-blindness/`: PREREG-BB.md, inspect.zag + batteries,
AUDIT.md, VERDICT-BB.md, SHA256SUMS, run logs, verify_bb.py. Night-run log
updated. Final report: the four answers with numbers, gap classification,
rearchitect recommendation if the trigger fires.
