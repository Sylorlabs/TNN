# B5 purity audit — T1 teaching/authoring/revision decisions

Date: 2026-09-24. Mechanism: `bin/learn` (pure Zag, built from
`src/learn.zag` with the pinned znc toolchain). Driver:
`driver/run.py` (orchestration only).

## Bar

Every teaching, authoring, and revision DECISION is made by the pure-Zag
mechanism, deterministically, with zero RNG. The Python driver may only:
invoke processes, move bytes between files, apply decisions the mechanism
already made, and record metrics. It makes no judgment calls.

## Decisions owned by the Zag mechanism

| # | Decision | Zag mode | Notes |
|---|----------|----------|-------|
| 1 | Curriculum sequencing: which unit, in which order | `teach` | Emits CONSULT/INSTALL/PRACTICE lines in curriculum order; one corpus consultation per unit with byte count + FNV digest |
| 2 | Installed-card retrieval: which card holds a requested template | `findcard` | Unit's card first, then remaining installed cards in curriculum order; matches a FULL line `## TPL <tpl>` (line-start and line-end anchored). Prints `<unit>.card`; exits 1 with FINDCARD-MISS when no installed card holds it |
| 3 | Placeholder composition: how `{key}` slots are filled | `compose` | Task PARAMS first, then the card's LEARNED section; UNBOUND keys reported, never guessed |
| 4 | Compiler-diagnostic parsing: what the error means | `revise` | Parses tsc error code, line/col, and identifier from the diagnostics file |
| 5 | Compiler-driven source repair: how to fix it | `revise` | Frozen repair table: TS2564 → definite-assignment `!`; TS18047/TS18048 → non-null `!`; TS7006 → annotate from card hints; TS2339 → correction from installed mistake mappings. Emits FIX lines and LEARN lines |
| 6 | What was learned from a revision | `revise` | Emits `LEARN unit=U k=v`; the driver is only the scribe |

## What the Python driver does (no decisions)

- `parse_task` / `write_blocks` / `norm`: file parsing and byte moving.
- `run_tsc` / `run_node`: invoking the external compiler and runtime.
  Type checking uses real `lib.dom`; DOM unit tests run against `src/domshim.js`.
- Loop control: stop when tsc reports no `error TS`; stop after MAXREV=5
  revisions (frozen prereg parameter, not a judgment call).
- `apply_learn`: appends the mechanism's own LEARN lines to cards during
  teaching (idempotent; skips duplicates). Never invents entries.
- CARD-MISSING: recorded when `findcard` exits 1 — the miss decision is
  the mechanism's; the driver only records it.
- Metrics: pass/fail, revision counts, fix histogram, summaries.
- Phase sequencing: battery order t01–t26 is fixed in the frozen battery.

## Remediation made during this audit (2026-09-24)

Before this audit, template retrieval (which installed card holds a
template) was implemented in Python (`find_card_file`). Although it was
a fixed deterministic rule, it was a retrieval DECISION outside the
mechanism. It has been moved into Zag as the `findcard` mode
(`src/learn.zag`, `findcard_check` + `mode_findcard`), and the driver
now delegates to it.

Equivalence proof:
- `findcard` returns the same card as the old Python rule on all 26
  battery tasks (26/26), and exits 1 with FINDCARD-MISS on unknown
  templates.
- Old vs new `bin/learn`: `compose` byte-identical on t01/t04/t13/t26;
  `teach` byte-identical on the full curriculum.
- Regression runs b1d/b1e (new binary + new driver) are compared
  byte-for-byte against b1b/b1c in the determinism report.

## Scope note — T2 site builder

`sitecom/build.py` routes every HTML fragment and TypeScript piece through
`bin/learn compose` (pure Zag). The site SPEC files (which fragments, in
which order, with what copy) are crew-authored briefs, and the fragment
scaffold (`sitecom/frag.card`) plus TS scaffold (`sitecom/ts.card`) are
crew-authored templates written in the learned T1 idioms. Site-level
design decisions (layout, CSS, copy) are the crew's; piece-level
composition is the mechanism's. Provenance per site is recorded in
`sites/<site>/PROVENANCE.md`. The self-designed site (selene) additionally
records its default-design procedure in `sites/selene/DESIGN.md`.

## Residual non-Zag elements (acknowledged, not decisions)

- The compiler (`tsc`) and runtime (`node`) are external tools; the
  mechanism treats their output as evidence.
- The DOM shim is a test double for `lib.dom` types at runtime only.
- File paths, timeouts, and log locations are operational constants.
