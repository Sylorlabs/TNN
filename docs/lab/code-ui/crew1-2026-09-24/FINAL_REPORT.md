# CODEUI-1 Crew 1 — final report: T1 guided learning, B1 battery, T2 websites

Date: 2026-09-24. Frozen prereg: `~/workspace/code-ui/PREREG.md`
(2026-09-24 ~09:50 PDT). Teach order: types → functions → interfaces →
classes → generics → DOM APIs → async → modules.

## T1 — Guided learning (TypeScript)

**Teaching result: 8/8 practice tasks passed**, manual-free after the
single logged consultation per unit.

| Unit | Consult bytes | FNV | Practice | Revisions | Fix |
|------|---------------|-----|----------|-----------|-----|
| U1-types | 1351 | a226fa91f5a850e3 | p1 | 0 | — |
| U2-functions | 1486 | d735d8dbc5271db8 | p2 | 0 | — |
| U3-interfaces | 1522 | 9cf8eafa536c4ee5 | p3 | 0 | — |
| U4-classes | 2020 | a9de9e75800b7c94 | p4 | 1 | TS2564 → `fieldbang=!` learned |
| U5-generics | 1910 | 93da99bed526788c | p5 | 0 | — |
| U6-dom | 1892 | 81c8b22e90fdd510 | p6 | 1 | TS18047 → `nonnull=!` learned |
| U7-async | 1677 | 2cd72d482dca610e | p7 | 0 | — |
| U8-modules | 1640 | 2c009dc3442281ea | p8 | 0 | — |

The two revisions are textbook deliberate revision: the compiler
diagnosed a strict-mode violation (TS2564 definite assignment on
`title`; TS18047 possibly-null `app`), and the mechanism installed a
general correction (`fieldbang=!`, `nonnull=!`) that then applied to all
later tasks. This is the coding-manuals proposal working as designed:
reference consulted once, installed as procedural schema, then
manual-free.

Learned card state (frozen for B1):
- `cards/U4-classes.card`: `fieldbang=!`
- `cards/U6-dom.card`: `nonnull=!`

Sources manifest: `corpus/SOURCES.md` (8 public references with URLs,
byte counts, digests; teaching-only rules).

## B1 — preregistered battery (26 tasks, frozen 2026-09-24 ~10:40 PDT)

Bar: ≥85% pass `tsc --strict` + correct runtime output, manual-free,
median ≤5 compiler-driven revisions.

| Run | Pass | Median rev | Notes |
|-----|------|-----------|-------|
| b1a | 25/26 (96.2%) | 0 | t06 failed on a task-data typo (A1), not a knowledge gap |
| b1b | 26/26 (100%) | 0 | corrected rerun |
| b1c | 26/26 (100%) | 0 | corrected rerun, independent process |
| b1d | 26/26 (100%) | 0 | new pure binary (findcard in Zag); decisions byte-identical to b1b/b1c |
| b1e | 26/26 (100%) | 0 | new pure binary (findcard in Zag); decisions byte-identical to b1b/b1c/b1d |

- Transfer task t04 (U1 task composed from the U3 `ifacefn` template)
  passed in every corrected run.
- Sole amendment A1 (`battery/AMENDMENTS.md`): t06's PARAMS body used
  meta-key names `p1`/`p2` instead of the declared identifiers
  `name`/`title`. Intent-preserving data fix; frozen semantics, tests,
  and expected output unchanged.
- Failure diagnosis: the single failure across all runs was a task-data
  typo (machinery correctly reported CARD-level NOFIX — no MISTAKES rule
  covers a typo, and inventing one would be wrong). Zero knowledge-gap
  failures: every learned pattern the battery probed was recalled and
  applied correctly, manual-free.

**B4 determinism:** normalized decision evidence (card selection,
transfer flag, revisions, fixes, errors, outcome per task) is
byte-identical across b1b, b1c, AND b1d —
sha256 `10e352cf559b641bacb339999a6e6088b81d4d34e97c6067ffad48cb9349b2ae`.
b1d/b1e ran on the rebuilt pure binary (findcard moved into Zag),
proving the purity remediation changed nothing behaviorally. Four
independent runs, one shared decision hash. Cards verified
frozen during B1 (no writes; driver ran frozen=True).

**B5 purity:** all teaching/authoring/revision decisions in pure Zag
(`bin/learn`: teach/compose/revise/findcard). Audit in `PURITY.md`.
During the audit, template retrieval was moved from Python into Zag as
the `findcard` mode; equivalence proven 26/26 + old/new binary
byte-identical on compose (t01/t04/t13/t26) and teach.

**Teaching determinism:** the full teach phase was run TWICE from
identical pristine card snapshots (driver/teach_det.py). Byte-identical
results: consult.log (sha256
`52f259caaf4a9a699574ee9c2f4020fe2d6377856cb40154abbf1d1b556926e6`),
results.json (sha256
`c4f7efcf12be14ccefa4abf98f42bb076e9ba833f3106adf27b46fbccf9a5c2b`),
and final card states. Both runs independently re-derived the same two
deliberate revisions (TS2564→fieldbang, TS18047→nonnull). Learned cards
restored afterward; restoration verified byte-identical to the
pre-experiment snapshot.

## T2 — website ladder (4 sites)

| # | Site | Rung | Builds to working | Compiler revs | Defects (pre-judgment) |
|---|------|------|-------------------|---------------|------------------------|
| 1 | dawn | static landing | 1 | 0 | 0 |
| 2 | gadget | interactive components | 1 | 0 | 0 |
| 3 | grid | layout challenge | 1 | 0 | 0 |
| 4 | selene | self-designed | 2 | 0 | 1 authoring (spec slip: unbound `{id}` → `getElementById("")`; caught by output inspection, fixed) |

All four compile under `tsc --strict` with zero errors. gadget's four
interactive components verified against a stub DOM (counter, tabs,
todo, accordion, year). No manuals consulted during site builds.
selene's structure came from the deterministic default-design procedure
(`sites/selene/DESIGN.md`) from the topic string alone.

v1 of all four sites is in
`ui-judgment/NEEDS_JUDGMENT/{dawn,gadget,grid,selene}/` per the frozen
judgment protocol. **Awaiting Crew 2's ≥3 named defects per site** for
the v2 iteration loop. Micah's eyes are the final oracle.

Authorship accounting (PURITY.md scope note + SITES_REPORT.md): HTML/TS
pieces composed by the mechanism from crew-authored scaffold written in
the learned idioms; CSS and site briefs are the crew's; selene's
concept is procedure-designed.

## Metrics summary (prereg bars)

- B1: 100% pass (bar 85%), median 0 revisions (bar ≤5). PASS.
- Manual-free testing: held (zero corpus consultations during B1;
  production consultations logged separately).
- First-working-build iterations: 1,1,1,2 across the ladder.
- Retention: B1 is the retention test (learned knowledge applied
  manual-free days after teaching) — 26/26. Site rebuilds are
  deterministic from specs.

## Open items / recommended follow-ups

1. Crew-2 judgment → v2 builds for all four sites (blocked on Crew 2;
   v1 dropped in NEEDS_JUDGMENT per protocol §5).
2. Final evidence commit to the lab repo (staged at
   `~/workspace/tnn-lab/code-ui/crew1-2026-09-24/`, to commit with
   `commit_racefree.py`; binaries and `.zag-cache` excluded).
3. Coding-manuals-law compliance audit: DONE — verdict COMPLIANT
   (MANUALS_AUDIT.md). Cards hold only generative templates,
   diagnostic→correction rules, and compiler-evidence-derived learned
   entries; no handbook prose installed.
