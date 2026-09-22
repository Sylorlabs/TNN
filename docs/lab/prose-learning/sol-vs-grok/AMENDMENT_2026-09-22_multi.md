# Amendment 2026-09-22 — multi-slice instrument fix (diagnostic-only)

Status: coordinator instrument fix, committed with build-freeze (commit B).
No decision rule, metric, bar, margin, or verdict rule is changed. The primary
metric SG-PARA, eligibility gates, Δ=0.03, and hybrid rules are untouched.

## Defect found during calibration (2026-09-22)

The multi slice was specified as a coreference/composition diagnostic:
two-sentence teaches (`The {Ra} of "{E}" is {V1}. It has a {Rb} of {V2}.`)
with a probe on the second sentence's relation.

Two defects were found when the frozen contender binaries ran on the
calibration battery:

1. **Redundancy with canon.** The second sentence's (relation, entity) pair
   was drawn from the 12 directly-taught families, so every multi probe was
   answerable without the coref sentence. Both contenders scored 24/24 and
   SG-COMP measured nothing beyond canon.

2. **(relation, entity) collisions.** After fixing (1) with novel relations
   cycled `i % 4`, items `i`, `i+8`, `i+16` shared the same (relation,
   entity) pair with different values. Install order then dead-marked the
   first two rows per the frozen contradiction rule and left the third
   live, so probes returned install-order artifacts (Grok multi = 4/24,
   all misses returning the first-installed value of that relation).

## Fix (in `gen/battery.py`, both configs)

- The multi second sentence now asserts a **novel relation** taken from a new
  config list `multi_rels` (4 pairs per config), disjoint by stem from the 12
  relations, the distractor relations, and the other config's vocabulary.
- Item `i` uses `(multi_rels[i % 4], ENT_MAIN[(i // 4) % 8])`: all 24
  (relation, entity) pairs are unique — no install-order collisions.
- Values `V2 = multi_v0 + i * multi_dv` (calib: 500+7i; scored: 700+11i).
- `gen/check_sg.py` §9 now asserts: s2 value frame correct, s2 rel ⊃ probe
  rel by 1–2 residue words, probe rel novel (not in taught relsets), s2
  entity == probe entity (coref threading).

## Effect on calibration (re-measured 2026-09-22, frozen binaries)

| slice | Sol | Grok |
|---|---|---|
| multi (fixed) | 0/24 | 4/24 |

Mechanistic reading (diagnostic-only, does not affect the verdict):
- Sol: the s2 sentence carries residue words (`a`) in its predicate set, so
  exact predicate-set equality never matches the probe → UNKNOWN.
- Grok: the fallback lex is built from the sentence's own words; a
  coref-resolved entity contributes no name to the row lex, so all rows
  sharing a multi relation tie and install order picks the first → the
  first-installed value of that relation regardless of entity.

Neither architecture handles coref-mediated retrieval of a novel relation;
their failure modes are complementary (exactness vs entity-blind tolerance).

## Calibration battery regenerated

`gen/calib/` was regenerated with the fixed generator and re-validated:
frame validation 0 failures, `check_sg.py` passes, zero cross-config stem
or entity collisions. Contender acceptance (5-run byte-identical, canon
96/96) is unaffected — canon/heldout/extra/typo/neg/hedge/contr/distractor
construction is unchanged.
