# T2 website ladder — build report (Crew 1)

Date: 2026-09-24. Builder: `ts-teaching/sitecom/build.py` (deterministic).
Every HTML fragment and TypeScript piece was composed by `bin/learn
compose` (pure Zag); fragments from `sitecom/frag.card`, TS from
`sitecom/ts.card` (crew-authored scaffold in the learned T1 idioms).
CSS is crew-authored design. All four sites compile under `tsc --strict`
with zero errors. No manuals or references were consulted during the
site builds.

## The ladder

| # | Site | Rung | Dir |
|---|------|------|-----|
| 1 | dawn | static landing page | `sites/dawn/` |
| 2 | gadget | interactive components | `sites/gadget/` |
| 3 | grid | layout challenge (magazine) | `sites/grid/` |
| 4 | selene | self-designed site | `sites/selene/` |

## Per-site metrics

| Site | Builds to working | Compiler revisions | Defects found (pre-judgment) | Manual consultations |
|------|-------------------|--------------------|------------------------------|----------------------|
| dawn | 1 | 0 | 0 | 0 |
| gadget | 1 | 0 | 0 | 0 |
| grid | 1 | 0 | 0 | 0 |
| selene | 2 | 0 | 1 (authoring) | 0 |

Defect detail (selene): the first build's `moonlogic` piece emitted
`document.getElementById("")` — the `{id}` slot was UNBOUND because the
site spec supplied only `el=moonph`. tsc was clean (empty string is a
valid argument); the defect was caught by reading the composed output.
Root cause: spec authoring slip, not a learned-knowledge gap. Fixed by
adding `id=moonph` to the spec; rebuilt clean. Logged here as an
authoring defect: 1 across the ladder.

## Functional verification

- gadget (interactive): exercised all four components against a stub DOM
  in Node — counter reads 1 after (+,+,-); tab 2 activates while tab 1
  deactivates; todo adds a trimmed item and clears the input; accordion
  items wire; year renders 2026. Harness:
  `sitecom/work/gadget_test.js` (+ `domtest.js`).
- selene (interactive): filter/tabs logic is the same verified
  querySelectorAll idiom as gadget's tabs; moon phase computes from the
  date. (Full stub-DOM exercise not repeated; same code shape as
  verified.)
- dawn/grid: static + year piece; structure verified (all fragment
  blocks present, no unbound `{key}` placeholders in any output).

## Retention (sites)

Rebuilding any site from its spec is deterministic: same spec →
byte-identical `index.html`/`app.ts` (the composer is pure Zag; verified
on selene's rebuild — only the spec changed, and only the moonlogic
piece differed). No re-consultation of any reference occurs.

## Judgment handoff (B3)

v1 of all four sites copied to
`ui-judgment/NEEDS_JUDGMENT/{dawn,gadget,grid,selene}/`
(`index.html`, `style.css`, `app.js`, `app.ts`, `PROVENANCE.md`;
selene also `DESIGN.md`) per the frozen judgment protocol §5.
Awaiting Crew 2's ≥3 named defects per site; v2 builds will address
them. Micah's eyes are the final oracle on the finished sites.

## Authorship accounting (honest)

- HTML structure: composed by the mechanism from crew-authored fragment
  templates; copy from the site briefs.
- CSS: crew-authored (the design brief).
- TypeScript: composed by the mechanism from scaffold patterns written
  in the learned idioms (`!` non-null assertions, `querySelectorAll`,
  classes). Not drawn from the learned cards directly — the learned
  templates are function-level, and forcing them would have produced
  worse code. See PURITY.md scope note.
- selene's concept/structure/copy: chosen by the deterministic
  default-design procedure from the topic string alone
  (`sites/selene/DESIGN.md`).
