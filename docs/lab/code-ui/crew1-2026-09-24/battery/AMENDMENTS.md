# B1 battery amendments

The battery table (BATTERY.md) and the 26 task files were frozen 2026-09-24
~10:40 PDT, before any teaching or testing run. Amendments below are
minimal, intent-preserving data fixes discovered during runs. Each records
what was wrong, why the fix preserves the frozen semantics, and which runs
it affects.

## A1 — t06 PARAMS body identifier typo (found during B1 run b1a, 2026-09-24)

- Task: t06 (U2-functions, fnopt template, "optional parameter").
- Bug: the PARAMS `body` referenced the parameter meta-keys `p1`/`p2` as
  identifiers (`return p2 === undefined ? ... p1 ...`), but the fnopt
  template declares the parameters under their VALUES (`name`, `title`).
  Result: `TS2304: Cannot find name 'p2'`, unfixable by the revision
  mechanism (no MISTAKES rule; correct behavior is a task typo, not a
  knowledge gap).
- Fix: body now uses the declared identifiers:
  `return title === undefined ? "Hello, " + name : "Hello, " + title + " " + name + "!";`
- Frozen semantics preserved: ID, unit, title, description, TPL, files,
  TESTS, and EXPECT (`Hello, Al` / `Hello, Dr. Bo!`) are unchanged. The
  task's evident intent (optional title parameter) is what the fixed body
  implements.
- Affects: run b1a (recorded 25/26 with t06 NOFIX) is superseded for the
  headline metric; b1b/b1c reruns use the fixed task.
