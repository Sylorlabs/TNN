# B3 VERDICT — CODEUI-1 iteration crew (v1 → v2)

**Date:** 2026-09-24. **Frozen authorities:** `code-ui/PREREG.md` (B3),
`code-ui/ui-judgment/JUDGMENT_PROTOCOL.md`, frozen judge v1, blind proxy
rubric `b3-iteration/PROXY_RUBRIC.md` (preregistered BEFORE any judging).

## Per-site results

| site | v1 score (a/b) | v2 score (a/b) | (a) judge v2>v1 | (b) proxy majority | B3 |
|---|---|---|---|---|---|
| dawn | 830 / 830 | 830 / 830 | tie — NO | 1/3 — NO | **FAIL** |
| gadget | 830 / 830 | 960 / 960 | YES (+130, defect cleared) | 2/3 — YES | **PASS** |
| grid | 830 / 830 | 704 / 704 | regression — NO | 1/3 — NO | **FAIL** |
| selene | 704 / 704 | 704 / 704 | tie — NO | 1/3 — NO | **FAIL** |

**B3 outcome: 1/4 sites pass (gadget).** The bar is per-site; there is no
aggregate pass.

## What the numbers mean

- **gadget PASS.** The judge's HIERARCHY_FLAT cleared on both
  representations (830→960); the blind proxy improved on 2 of 3 named
  defects (hero_ratio 0.43→0.69, align_modes 2→1). Iteration-from-own-
  judgment worked here.
- **dawn FAIL (tie).** The enlarged hero fragmented into more bands under
  the judge's band detector (hero_ratio 430→406) — the judge's number moved
  opposite to the visible change. Proxy confirms the hero did get
  relatively larger (size_ratio 3.71→4.00).
- **grid FAIL (regression).** Acting on the judgment backfired: reshuffling
  type sizes created a 5th rendered band-height class, firing a NEW
  TYPOGRAPHY_INCONSISTENT (830→704). The v1 remains the better artifact by
  the frozen judgment.
- **selene FAIL (tie).** Hierarchy improved on both instruments (judge
  hero_ratio 575→740, proxy 0.37→0.49) but not enough to clear the bar;
  typography stuck at 5 modes; spacing worsened on both instruments.

## Structural finding: HIERARCHY_FLAT is nearly unwinnable for full pages

All five references are near-single-band hero crops (apple2: m_bands=1,
hero_ratio=1000); the envelope floor for hero_ratio is 952‰. No
multi-section page (7–16 bands) can put 95% of its ink mass in one band, so
the defect fires on every full page and no reasonable hero enlargement
clears it (selene: 575→740 still fires; dawn: 430→406). This is a judging-bar
issue, not an acting issue — flagged as an observation for the judge-repair
crew (their work untouched). It does not invalidate the gadget pass: there
the defect cleared because hero_ratio crossed into a sub-threshold
severity, and the proxy independently confirmed the hierarchy gain.

## Honest mechanism-vs-scaffold accounting

**TNN's own machinery did:**
- Defect naming + scoring + verdict: the frozen pure-Zag `judge` binary
  (both representations, byte-identical reruns verified).
- All HTML/TS authoring: every fragment composed by `bin/learn compose`
  (pure Zag: template selection + slot binding), assembled by the
  deterministic builder, compiled `tsc --strict` clean. v2 HTML/TS are
  **byte-identical to v1** (verified per file) — the design delta is
  CSS-only, so no code drift was possible.
- The selene v1 default-design procedure (Crew 1, deterministic).

**The crew (me) scaffolded:**
- The v2 design deltas: translating the judge's named defects into concrete
  CSS values (e.g. "HIERARCHY_FLAT → h1 56→72px"). The judge names defects,
  not pixel values; the design decisions are mine. Documented per defect in
  each site's V2 CSS header comment.
- The render pipeline: WeasyPrint 70 + pdftoppm → 1280×800 RGB24 .img
  (deterministic harness, zero aesthetic logic). Chromium on this VM is
  broken (verified: hangs/writes nothing); the playwright chromium download
  fails through the egress proxy. WeasyPrint renders CSS grid correctly but
  has flex quirks (e.g. gadget's counter buttons render stretched — a
  renderer artifact, NOT a design defect, and NOT named as one). Same
  renderer for v1 and v2, so the comparison is fair; absolute scores are
  renderer-conditioned.
- The blind proxy rubric: preregistered before any judging, implemented
  independently of the judge; one genuine bug fixed after preregistration
  (dark-theme ink polarity — selene measured zero bands; fixed, all sites
  re-scored, documented in the rubric's run log). Blinding via SHA-256
  filename mapping, measurements recorded before unsealing.
- JUDGMENT.md prose: the mechanism's verdict is quoted verbatim; the
  protocol's "≥3 specific defects" bar was met by supplementing the
  mechanism's 1–2 named defects with crew-observed specifics, each labeled
  as crew-observed and each a rubric-valid name with a concrete ref
  comparison. The mechanism alone named fewer than 3 — reported as-is.

**Zero RNG:** every decision path (learn compose, judge, builder, rubric,
render) is deterministic; judge reruns byte-identical (verified 2x).

## Deliverables

- v2 sites: `code-ui/sites/<name>/v2/` and `code-ui/ui-judgment/NEEDS_JUDGMENT/<name>/v2/`
- `JUDGMENT.md` + `V2_JUDGMENT.md` per site in `NEEDS_JUDGMENT/<name>/`
- Traces: `code-ui/ui-judgment/traces/b3iter/<site>_{v1,v2}_{a,b}.{txt,out}`
- Workdir: `code-ui/b3-iteration/` (render.py, build_v2.py, proxy_rubric.py,
  PROXY_RUBRIC.md, v2css/, blind/, *_v1.img, *_v2.img)
- Mirror: `tnn-lab/code-ui/b3-iteration/`

## Open / recommended follow-ups (for parent)

1. Micah's eyes are ground truth on the final sites (per prereg) — the v2
   sites are openable for his verdict, labeled NEW.
2. Judge-repair crew: consider the HIERARCHY_FLAT envelope finding (952‰
   floor vs multi-band pages) — observation only.
3. grid v2 regressed by the frozen judgment: recommend reverting grid to v1
   as the shipped artifact unless Micah's eyes prefer v2.
