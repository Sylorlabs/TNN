# Wave-6 Investigation 2: formula-test — REPORT

**Verdict: POSITIVE** — a viable `wrong(m,v)` replacement exists, fully
characterized, with one minor benign catch stated below. This investigation
changes nothing in the prereg; adopting the formula still needs Micah's
ruling + a dated amendment (PREREG §9/§10). Defects 2, 3 and C1 from the
BLOCKED report are untouched — the trial stays BLOCKED until all are ruled.

**Evidence:** `analyze.py` (this directory) — pure arithmetic over
m = 0..499, v ∈ {0,1,2}. No trial simulation, no RNG. All yields below are
exact counts, verified by double computation (determinism holds trivially
for closed forms; confirmed anyway).

## The one finding that matters most

The WBS rigidity test only works if wrong memories actually *become strong*.
Strength reaches a memory through exactly two paths: the trainer-declared
path (empty — Defect 2) and the learner's STRENGTHEN-on-importance-revelation
path (fires only when `imp(m,v) = 1`). A wrong memory with `imp = 0` enters
with weak features, gets declared strength ~10, and is revised with a single
evidence record — no friction, no rigidity test. So the operative question
for any candidate is not just "~20% yield" but **what fraction of wrong
memories are also important** — that fraction is the R_wbs denominator.

## Results table (per variant, H = 500)

| candidate | formula | yield v0/v1/v2 | wrong&important (R_wbs denom) v0/v1/v2 | right&important (F_wbs denom) | period | pressure-ep hits | implant-ep hits |
|---|---|---|---|---|---|---|---|
| blocked (ref) | `(5m+11v+7)%10<2` | 0 / 0 / 0 | — | — | — | — | — |
| (a) report's suggestion | `(3m+7v+1)%10<2` | 100 / 100 / 100 | **0 / 0 / 0** | 150 / 150 / 150 | 10 | v0: all four | v0: {83,250,333} |
| **(b) recommended** | **`(3m+7v+9)%10<2`** | 100 / 100 / 100 | **100 / 100 / 100** | 50 / 50 / 50 | 10 | none | v2: {166,416} |
| (c) simplicity foil | `(4m+9v+2)%10<2` | 100 / 100 / 100 | 50 / 50 / **0** | 100 / 100 / 150 | **5** | v1,v2: all four | v1,v2: {250} |

Residue uniformity: (a) and (b) raw mod-10 values hit exactly 50× each per
variant (slopes 3 coprime to 10); (c) likewise on its 5-cycle.

## Per-candidate catch analysis

### (a) `(3m+7v+1)%10<2` — FATAL catch: the rigidity test would be vacuous
- **P(important | wrong) = 0.000 in every variant.** The wrong residues
  ({0,3},{1,4},{2,5} mod 10) are disjoint from the importance residues
  ({1,4,7},{2,5,8},{3,6,9}) — an accident of the chosen offsets, but the
  effect is total: not one wrong memory in any variant would ever be
  strengthened. R_wbs = 0/0 in all variants; arm A's kill criterion
  ("fail to revise its own strong mistakes and A dies") cannot be evaluated.
  This is the same *class* of failure as the blocked formula — zero
  *testable* wrong memories instead of zero wrong memories — and it would
  have passed a naive "~20% yield" check. Yield alone is not a validity check.
- **Variant asymmetry:** in v=0 every pressure episode (100,200,300,400) and
  3 of 5 implant episodes are wrong=1; in v=1/v=2 none are. So v=0's
  wrong-pattern is entangled with the pressure/implant schedules while the
  other variants' aren't — asymmetric blinding hygiene across variants.
- Predictability: period 10, a clean "m mod 10 ∈ {two residues}" rule — moot,
  given the fatal catch.

### (b) `(3m+7v+9)%10<2` — RECOMMENDED. Catch: two cosmetic index coincidences in v=2
- **Nested in importance: P(important | wrong) = 1.00 in every variant.**
  Wrong residues {4,7}/{5,8}/{6,9} sit inside importance residues
  {1,4,7}/{2,5,8}/{3,6,9}. Every wrong memory honestly looks important early
  (matches TEST_PLAN §7b's "early features honestly indicate importance —
  no trap"), gets strengthened to 80–90 by the learner's own rule, then
  receives contradictions at m+25k. R_wbs denominator = 100/variant;
  F_wbs denominator = 50/variant; perfectly symmetric across variants.
- **THE CATCH, plainly:** in variant 2 only, episodes 166 and 416 are both
  wrong-memory episodes (WBS cell) and implant episodes (JI cell). What this
  means for the trial: nothing measurable. The three curricula run as
  *separate cells* — the JI cell never evaluates the wrong-formula, the WBS
  cell never consults the implant list — and the learner is a fixed policy
  that carries no knowledge across cells. There is no causal path by which
  the coincidence can affect any metric in any arm. It is a cosmetic wart,
  not a confound. It is also the *minimum* achievable: exhaustive search over
  the whole mod-10/threshold-2 family (all coprime slopes, all offsets) found
  exactly 4 nesting solutions; the others have 2–4 such coincidences, (b)
  has the fewest (2). The mod-20 family has zero nesting solutions at all.
- Predictability: period 10, "m mod 10 ∈ {two residues}". This is *exactly
  as predictable as the importance signal itself* (also a mod-10 residue
  rule revealed 25 late) — parity, not a new leak. A learner would need ~2
  full cycles of contradiction revelations to infer it, and the preregistered
  learner does no such inference (fixed policy).
- Price of nesting (not a catch, a design consequence): P(wrong|important) =
  2/3 — two-thirds of important memories turn out wrong, so the rigidity test
  is harsh: the learner must revise 100 strong mistakes per variant inside
  W=150. That harshness is the point of WBS ("fail to revise its own strong
  mistakes beyond the registered bound and A dies").

### (c) `(4m+9v+2)%10<2` — REJECTED. Catches: leakiest pattern + dead variant
- **Period 5** ("wrong iff m mod 5 == r", variant-specific r). Strictly more
  predictable than the importance signal — a handful of contradiction
  revelations would let even a simple pattern-learner anticipate wrongness
  *before* the 25-episode-late revelation. Of the three, this is the leakiest
  against the blinding requirement.
- **Variant asymmetry, fatal in v=2:** P(important|wrong) = 0.5 in v=0 and
  v=1 but **0.0 in v=2** — R_wbs denominator 0 in v=2, so the "every
  variant" promotion criterion (PREREG §5.1) could not be evaluated there.
- Pressure-episode entanglement in v=1 and v=2 (all four pressure episodes
  are wrong=1) but not v=0 — asymmetric again.

## Cross-pattern alignment summary (all candidates)
- **Pressure episodes** {100,200,300,400} and **implant episodes**
  {83,166,250,333,416} (500 out of range per Defect 3) live in the VUP and
  JI curricula respectively; `wrong(m,v)` is consulted only in WBS. All
  reported overlaps are therefore cross-cell regularities with no causal
  path into any cell's dynamics under the preregistered fixed learner
  policy. They are recorded as blinding hygiene, not validity threats —
  except where they create *variant asymmetry*, which is flagged per
  candidate above. (b) is the only candidate with no pressure overlap in
  any variant and no variant-asymmetric behavior anywhere.

## Recommendation
Adopt **`wrong(m,v) = 1` iff `(3m + 7v + 9) mod 10 < 2`** as the Defect-1
fix, via dated amendment + Micah's re-approval. It is the minimal edit of
the BLOCKED report's suggestion (offset 1 → 9), yields exactly 20% per
variant with uniform residues, nests inside importance in every variant
(maximum WBS power, faithful to "early features honestly indicate
importance"), is symmetric across variants, matches the importance
signal's predictability class, and has the fewest cosmetic index
coincidences of any nesting solution in the family (2, benign, v=2 only).

## Next step
1. Micah rules on the Defect-1 amendment (recommended text above). This
   investigation is analysis only — nothing was written to the prereg.
2. Defects 2 (VUP designated subset empty), 3 (implant episode 500 out of
   range), and C1 (static-check scope) still await rulings. The trial
   remains BLOCKED until all are ruled and amended.
3. Suggested amendment note to file alongside: "yield alone does not
   validate a curriculum formula — any replacement must also report
   P(important|wrong) per variant (the R_wbs denominator), or the rigidity
   test can be silently vacuous," with this report as evidence.
