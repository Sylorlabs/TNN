# FROZEN JUDGMENT PROTOCOL — CODEUI-1 Crew 2 (T4/B2/B3)

**Frozen:** 2026-09-24 ~10:30 PDT (preregistered BEFORE the B2 held-out test).
**Governs:** the conscious visual-judgment mechanism, B2 held-out test, B3 iteration.
**Parent law:** `~/workspace/code-ui/PREREG.md` (frozen a3746a90). Nothing here weakens it.

## 1. The mechanism

`judge` — one pure-Zag binary (`src/judge.zag`), zero RNG, deterministic.
It consumes the frozen image-sense binaries as perceptual evidence and performs
its own deliberate visual analysis from RGB24 pixels.

CLI:
```
judge metrics <img>                                   # metric vector only
judge judge <judged.img> <refs_profile.txt> <sense_evidence.txt>
```

- `<img>`: fixture format — u32 LE width, u32 LE height, W*H*3 RGB24.
- `refs_profile.txt`: 5 reference blocks (order: apple2, apple3, linear1,
  stripe1, vercel1). Each block: `ref=<name>` then 14 `m_<metric>=<int>` lines.
- `sense_evidence.txt`: `representation=a|b`, then 5 `colordisc=<SAME|DIFFERENT>`
  lines in the same reference order, then `shapetrans=<value>`. Produced by a
  deterministic driver that runs the FROZEN sense binaries
  (`~/workspace/senses-rebuild/a_raw/sense`,
  `~/workspace/senses-rebuild/b_percept/sense`) — colordisc on a
  judged|reference pair fixture, shapetrans on the judged hero.

**Purity split (B5):** all aesthetic logic — metrics, scoring, defect naming,
verdict — lives in `judge.zag`. The driver is a deterministic harness with NO
aesthetic logic: it assembles fixtures, runs frozen binaries, invokes `judge`
once, and archives outputs.

**Sense consumption:** the judge reads the sense binaries' verdicts as
perceptual evidence lines in its trace. `sense_bonus` = +30 (cap 1000) when
≥3 of the 5 colordisc evidence lines are SAME — small, documented,
deterministic.

## 2. Metrics (all integers; per-mille where noted)

| metric | meaning |
|---|---|
| m_bg_lum | background luminance estimate (0..255) |
| m_ink_lum | mean ink-pixel luminance (0..255) |
| m_contrast | (max+10)*1000/(min+10) of bg vs ink luminance (cap 30000) |
| m_ink_total | per-mille of all pixels classified as ink |
| m_bands | count of contiguous text-band rows groups |
| m_gap_cv | per-mille CV of inter-band gaps |
| m_margin_ink | per-mille ink inside the outer 10% top/bottom rows |
| m_guides | count of strong vertical-edge columns (cap 40) |
| m_align_conc | per-mille of vertical-edge energy in the top-4 guides |
| m_type_modes | distinct band-height classes (cap 12) |
| m_hues | dominant saturated-hue bins (0..12) |
| m_hero_ratio | per-mille mass share of the largest content band |
| m_rows | image height (normalizer, not scored) |
| m_satcov | per-mille of all pixels with saturation > 48 |

Tolerances (tol) and weights (w) — preregistered, applied identically to both
representations:

| metric | tol | w | defect fired when dev>=450 |
|---|---|---|---|
| m_bg_lum | 60 | 0 | — (context only) |
| m_ink_lum | 60 | 0 | — (context only) |
| m_contrast | 1000 | 2 | CONTRAST_POOR |
| m_ink_total | 60 | 1 | DENSITY_CLUTTER |
| m_bands | — | 0 | — (context only) |
| m_gap_cv | 300 | 1 | SPACING_IRREGULAR |
| m_margin_ink | 40 | 1 | MARGIN_CROWDED |
| m_guides | 4 | 1 | ALIGNMENT_WEAK |
| m_align_conc | 150 | 1 | ALIGNMENT_WEAK |
| m_type_modes | 2 | 1 | TYPOGRAPHY_INCONSISTENT |
| m_hues | 2 | 1 | COLOR_UNRESTRAINED |
| m_hero_ratio | 150 | 1 | HIERARCHY_FLAT |
| m_satcov | 150 | 1 | COLOR_UNRESTRAINED |

dev_m (AMENDED 2026-09-24 ~11:00 PDT, before B2 — rationale: two-sided
deviation punished superior UIs for being *cleaner* than the reference in the
good direction, e.g. margin_ink=2 vs ref 134): one-sided envelope deviation.
The 5 reference vectors define a per-metric envelope [lo,hi]; dev=0 while the
judged value is inside the envelope or on its good side; past the envelope
edge in the BAD direction, dev=(dist)*1000/tol (cap 1000). Bad directions:
high = ink_total, gap_cv, margin_ink, guides, type_modes, hues, satcov; low =
contrast, align_conc, hero_ratio. m_bands is context only (not a rubric
defect). sense_bonus=+30 when ≥3 of 5 colordisc evidence lines are SAME.
score = 1000 − Σ(w_m · dev_m)/Σw_m − 80·(number of fired defects)
        + sense_bonus, clamped 0..1000.
(AMENDED 2026-09-24 ~12:00 PDT: per-defect penalty added — rationale: a page
with multiple rubric defects must score clearly below a page with one mild
excursion; dev-weighted mean alone under-penalized multi-defect pages.
Tolerances tightened to the "clearly bad" distance so the in-envelope
superiors keep dev=0.)
No per-reference best-match in scoring; nearest reference reported in trace.
verdict = GOOD if score ≥ 600 else BAD.
confidence = min(1000, |score − 600| * 1000 / 400).

## 3. Named defects — the valid-reason rubric

A reason is rubric-valid iff it is one of these 8 named defects, each mapped
to a prereg category:

- typography: **TYPOGRAPHY_INCONSISTENT**, **CONTRAST_POOR**
- spacing: **SPACING_IRREGULAR**, **MARGIN_CROWDED**, **DENSITY_CLUTTER**
- hierarchy: **HIERARCHY_FLAT**
- color restraint: **COLOR_UNRESTRAINED**
- alignment: **ALIGNMENT_WEAK**

≥3 specific defects named per Crew-1 site judgment (B3 step 3).

## 4. B2 held-out test (frozen before the test)

- 10 pairs: (b2superior[i], bad[i]), i = 0..9. **Independence requirement
  (prereg B2): the bad[i] fixtures MUST be built by an independent party that
  did not train the judge and never shown during judgment development.**
  A self-built set (`b2/quarantine/`, generator `b2/gen_bad.py`) exists but is
  INELIGIBLE — it was produced by this judgment crew, so the frozen prereg
  forbids its use as B2 evidence. It is retained only as quarantined
  development material, clearly labeled non-evidence. Official B2 awaits an
  independently produced bad set (parent to arrange); the pair mapping will be
  frozen on arrival.
- Same frozen protocol, same pairs, run separately per representation
  (a_raw, b_percept). Byte-identical reruns verified (3x).
- Preference = higher score wins. Tie = not-preferred.
- **Bar: ≥8/10 preference for the superior side per representation, AND ≥1
  rubric-valid reason fired on the bad side of every won pair.**
- Kill (per prereg B2): ≤6/10, or reasons fail the rubric → report which
  representation and which reason classes failed.

## 5. B3 iteration protocol (frozen)

1. Crew 1 drops v1 into NEEDS_JUDGMENT/<name>/ (index.html + assets).
2. Crew 2 renders headless LOCALLY (local files only — never external
   navigation), screenshots at fixed viewport, converts to .img.
3. Judge v1 through the frozen protocol vs the 5 references; names ≥3
   specific defects vs T3 examples; writes iteration request to
   NEEDS_JUDGMENT/<name>/JUDGMENT.md.
4. Crew 1 ships v2 addressing them.
5. Crew 2 re-judges v2 FROM PIXELS ONLY with the frozen protocol.
6. Pass: (a) score(v2) > score(v1) by the frozen judgment, AND (b) the blind
   human-proxy rubric (spacing/typography/alignment sub-scores recomputed
   from v2's pixels) improves on a majority of the named defects.
   Micah's eyes are ground truth on the final sites when available.

## 6. Labeling

Every delivered artifact labeled NEW / PREVIOUSLY SHOWN / REFERENCE.
T3 examples are REFERENCE. Traces go to ui-judgment/traces/.

## 7. Determinism & purity bars (B4/B5)

- 3 runs of judge on the same inputs → byte-identical stdout (B4).
- Judgment logic in pure Zag only (B5). No binaries or .zagd in commits.
