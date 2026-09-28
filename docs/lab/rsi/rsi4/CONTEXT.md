# RSI-4 Instrument Context (frozen with PREREG4.md — smuggling-audit target)

## Mechanism inventory (descriptive only — what exists, not how to fix)

- M-TEACH: installs (key, val, seq) facts. Set-processing: no.
- M-KEY: constructs the lookup key from a fact's key field. Set-processing: no.
- M-RETRIEVE: gathers all facts with a matching key into a candidate set.
  Set-processing: yes. Readable fields: key, val, seq.
- M-ARBITRATE: selects one fact from a candidate set. Set-processing: yes.
  Readable fields: key, val, seq. Baseline behavior: first-taught wins.
- M-PROBE-SEM: poses current(k) queries against the store. Set-processing: no.
- M-LEDGER: audit trail. Constitution-protected (C1/C4).

Conflict path (computed from set-processing flags, pipeline order):
M-RETRIEVE → M-ARBITRATE.

## Field inventory

Fields: key, val, seq. Present at M-TEACH; readable at M-RETRIEVE and
M-ARBITRATE.

## Computable set-statistics (derived by fixed rule from the field inventory)

For each readable field f: DISTINCT(f), MODE(f). Positional: FIRST, LAST.
Set-level: SIZE.

- DISTINCT(f): the number of distinct f-values in the set.
- MODE(f): the f-value with the greatest count in the set; undefined on tie.
- FIRST: the first-taught element of the set.
- LAST: the last-taught element of the set.
- SIZE: the number of elements in the set.

These are general set operations. No statement here connects any statistic
to any repair.

## Composition operators (general program-construction pieces)

- PREFER-EXTREMAL(stat, dir): at a decision stage, select the element whose
  statistic key is extremal in direction dir; ties fall back to baseline.
- FILTER-EXTREMAL(stat, dir): at a gathering stage, keep the elements whose
  statistic key is extremal in direction dir.
- ANNOTATE(stat): record the statistic in the stage record; the decision
  is unchanged.

## Failure-signature vocabulary (computed mismatch types)

POSITIONAL: a positional rule predicts the probe outcomes.
DIRECTIONAL: a field-direction rule predicts the probe outcomes.
SET-STATISTICAL: only a set-statistic predicts the probe outcomes.
NONE: no tested statistic predicts the probe outcomes.

## Constitution

C1 ledger append-only · C2 gates authoritative · C3 self-change requires
verification+rollback · C4 audit complete (no silent skips) · C5 verification
bars frozen (only Micah amends).
Protected set: {(M-LEDGER,*)} ∪ {(M-ARBITRATE,bar_threshold),
(M-SELFCHANGE,verify_gate)}.
