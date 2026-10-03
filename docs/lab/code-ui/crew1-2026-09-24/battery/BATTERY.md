# B1 BATTERY — preregistered 2026-09-24 ~10:40 PDT, BEFORE any teaching/testing run

Bar (frozen PREREG): >=85% of tasks pass `tsc --strict` compile + run correctly,
manual-free (zero corpus consultations during testing), median <=5
compiler-error-driven revision iterations per task.
Kill: <85% pass or median >5 revisions -> diagnose knowledge gap vs machinery ceiling.

## Battery: 26 tasks, basics -> DOM -> interactive

| ID | Unit | Task |
|----|------|------|
| t01 | U1-types | typed variable + arithmetic |
| t02 | U1-types | union param with typeof narrowing |
| t03 | U1-types | sum number[] |
| t04 | U1-types | optional property + ?? fallback |
| t05 | U2-functions | annotated function add |
| t06 | U2-functions | optional parameter |
| t07 | U2-functions | arrow + contextual typing in .map |
| t08 | U2-functions | function-type alias as parameter |
| t09 | U3-interfaces | interface + two-arg function (manhattan) |
| t10 | U3-interfaces | readonly + optional props |
| t11 | U3-interfaces | interface extends |
| t12 | U3-interfaces | index-signature dictionary sum |
| t13 | U4-classes | class with constructor + method |
| t14 | U4-classes | class implements interface |
| t15 | U4-classes | class extends + super |
| t16 | U5-generics | generic identity |
| t17 | U5-generics | generic first<T> with T\|undefined |
| t18 | U5-generics | constrained generic longest |
| t19 | U6-dom | getElementById + textContent (null discipline) |
| t20 | U6-dom | createElement + appendChild |
| t21 | U6-dom | querySelectorAll + forEach |
| t22 | U7-async | async/await promise |
| t23 | U7-async | Promise.all concurrency |
| t24 | U8-modules | named export/import |
| t25 | U8-modules | default export + named import mix |
| t26 | U8-modules | import type |

## Method (frozen before run)

- TEACHING phase: curriculum order U1..U8; per unit exactly ONE corpus
  consultation (logged with byte count + FNV-1a); card installed to knowledge/;
  one practice task (p1..p8) run through compose -> tsc --strict -> revise loop
  (max 5 revisions). LEARN lines from revise are appended to the card's LEARNED
  section (knowledge growth from compiler evidence).
- TESTING phase (B1): knowledge/ frozen; consultations forbidden (compose exits
  2 on missing card -> task FAIL; consultations.log line count must not grow).
  Per task: compose -> tsc --strict -> node run -> stdout diff vs EXPECT.
  Revision loop max 5 compiler-error-driven iterations; LEARN ignored.
- Runtime harness: node; DOM tasks run under domshim.js (test double for the
  DOM runtime; TYPE-level strictness is real tsc against lib.dom).
- Metrics: pass rate, per-task iterations, median iterations, fix-code histogram,
  consultation count (teaching only), practice-vs-battery iterations (transfer),
  determinism: two full B1 runs byte-identical (excluding wall-clock).

## Expected learning events (teaching; not scored, recorded as evidence)

- p4: TS2564 on uninitialized class field -> revise inserts `!` -> LEARN fieldbang=!
- p6: TS18048 on getElementById result -> revise inserts `!` -> LEARN nonnull=!
  (t19/t20 then benefit in B1: transfer without re-consultation)
