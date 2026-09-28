# Ruling 3 — Evidence summary (does NOT make Micah's ruling)

Prereg: `PREREG_R3.md` (frozen; commit `81d683776bb9`). Positions:
(1) shift to `{0,83,166,250,333,416}`; (2) fully 1-index curriculum, implants
`{83,166,250,333,416,500}`; (3) drop to five implants `{83,166,250,333,416}`.

Raw evidence: `evidence/r3_t123.log` (T1–T3, byte-identical ×2),
`evidence/cell_s{N}_{B,C}_JI_{0,1,2}_r{1,2}.log` (T4, byte-identical ×2,
checker clean: `ST_INVALID 0` in every cell), `evidence/r3_t2d_sites.txt`
(T2d), `evidence/r3_t5_edge.txt` (T5).

## T1 — range validity

| scheme | H=500 | H=5000 |
|---|---|---|
| 1 (shift) | 6/6 in range | 6/6 |
| 2 (1-index) | 6/6 | 6/6 |
| 3 (drop-5) | 5/5 | 5/5 |

All three schemes pass range validity at both horizons.

## T2 — collisions / cost of 1-indexing

- Pressure collisions: scheme 1: 0; **scheme 2: 1** (implant episode 500
  collides with the 1-indexed pressure episode 500); scheme 3: 0.
- Designation collisions: 0 for all. Implant/revelation overlaps: 0 for all.
- T2d static audit (`r3_t2d_sites.txt`): 39 sites where closed forms are
  evaluated at episode numbers (`lr_imp`/`lr_wrong`/`lr_vj`/`lr_designated`
  all take `r3_m(t)` = t+1 under scheme 2), plus qualifiers and offset code
  that had to change from `t%100==0` to `t>=0 && t%100==99` and `t==99`
  style guards. The 1-index conversion is mechanical but touches every
  closed form — the largest code-churn of the three options, for no
  behavioral gain.

## T3 — spacing, rate, coverage

- Scheme 1: gaps 83/84 (mean 83.20), rate 12/1000, entrenchment coverage 78.
- Scheme 2: gaps 83/84 (mean 83.40), rate 12/1000, coverage 66 (the final
  implant at episode 500 has a **zero-episode observation window** —
  right-censored, exactly the defect the WBS late-horizon censored rule
  exists to handle).
- Scheme 3: gaps 83/84 (mean 83.25), rate 10/1000, coverage 65.

## T4 — real S1 JI cells (arm bias) — the decisive test

`ST_METRIC 3` = implants rejected / implants admitted (frozen 95% bar),
variants 0–2:

| scheme | Arm B (uniform) | Arm C (graded) |
|---|---|---|
| 1 (shift) | **6/6 = 100%** all variants (passes 95% bar) | **1/1 = 100%** (the ep-0 implant is admitted pre-freeze and rejected — measurable) |
| 2 (1-index) | **5/6 = 83.3%** all variants — **flips B across the 95% bar** | 0/0 (frozen by ep 82 — unmeasurable) |
| 3 (drop-5) | 5/5 = 100% (passes) | 0/0 (first implant at 83 — unmeasurable) |

Why scheme 2 fails B: its last implant sits on the final episode (500);
contradictions for it would arrive at episodes 525+ — outside the run — so
it is never observed, never rejected, and stays entrenched at end
(`ST_METRIC 5` = 1/6 vs 0/6 for the others). Scheme 2 makes one implant
structurally untestable. Excluding it from the denominator post-hoc would be
a metric change — and would concede scheme 2 is scheme 3 plus a decorative
implant. Drops: C loses one fewer memory under scheme 1 (469 vs 470)
because the ep-0 implant is admitted instead of dropped.

## T5 — episode-0 edge

Dynamic evidence: scheme-1 arm-B cells show 6/6 admitted and 6/6 rejected —
the ep-0 implant is admitted, contradicted (t=25, 50), and killed with no
special-casing (`if(p==0){return 0;}` guard verified live in the audit;
closed forms evaluate at `r3_m(0)=1`, no divide-by-zero, no negative
index). Static audit in `r3_t5_edge.txt`.

## Which position the evidence favors

**Scheme 1 (shift to `{0,83,166,250,333,416}`) on every frozen criterion:**
(1) all-in-range at both horizons; (2) zero collisions and no code churn
(scheme 2 collides with pressure ep 500 and requires 39-site 1-index
conversion); (3) preserves six evenly spaced implants at 12/1000 with the
best entrenchment coverage (78 vs 66/65); (4) the only scheme that does not
distort arm comparisons — B stays at 100% rejected/admitted (scheme 2
flips B to 83.3%, below the frozen 95% bar) and C keeps a measurable
denominator (1/1 vs 0/0 for schemes 2 and 3).

Build note (not a metric change): `ST_METRIC 5` (entrenched implants) still
uses the frozen denominator 6 for scheme 3; the observed value is 0
(0/6 = 0/5), so no conclusion is affected. Flagged for the next build.

This states which position the evidence favors. The final ruling is Micah's.
