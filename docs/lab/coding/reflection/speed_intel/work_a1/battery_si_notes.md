# battery_si.json — build notes (FROZEN 2026-09-22)

20 items, all new (no overlap with loop/battery.json v1):
- 12 multi-defect repair seeds (S01–S12), each with 2–3 defects from the
  learner's known classes, piloted at budget 16 with the ORIGINAL
  `loop/learner.zag` (built as `work_a1/learner`) + `driver_si.py`.
- 6 harder T4 gen items (G05–G10), each needing ≥2 KB patterns composed
  (count_occ: p_search+p_slice; sumprimes/fibsum: p_math+p_loop;
  selsort: p_sort+p_search). Single-pattern concepts excluded.
- 2 unfixable-by-design (X3 ungenable spec → `halt-genfail`;
  X4 unrepairable defect → `halt-no-patch`).

The reference repair paths below are RECORDED (pilot evidence) and NOT given
to the learner. The driver only reads: id/mode/spec/seed/patterns/demo/card/tests.

## Pilot reference paths (budget 16, original learner, verbatim)

| item | defects | reference path (diagnose classes/strategies) | iters | outcome |
|---|---|---|---|---|
| S01-syntax-name | SYNTAX, NAME | SYNTAX/patch-brace → NAME/patch-unknownfn (ad2→add) | 3 | pass |
| S02-arity-type | ARITY, TYPE | ARITY/patch-arity (drop extra) → TYPE/patch-type-argunquote | 3 | pass |
| S03-dupfn-name | DUPFN, NAME | DUPFN/patch-dupfn → NAME/patch-unknownfn (dlb→dbl) | 3 | pass |
| S04-syntax-arity | SYNTAX, ARITY | SYNTAX/patch-brace → ARITY/patch-arity (pad 3→3,4) | 3 | pass |
| S05-name-type | NAME, TYPE | TYPE/patch-type-delbadassign → NAME/patch-unknownfn (ad2→add) | 3 | pass |
| S06-syntax-type-name | SYNTAX, TYPE, NAME | SYNTAX → TYPE/delbadassign → NAME/unknownfn | 4 | pass |
| S07-arity-format | ARITY, OUTPUT_FORMAT | ARITY/patch-arity (drop) → OUTPUT_FORMAT/patch-add-newline | 3 | pass |
| S08-name-logic | NAME, LOGIC_VALUE | NAME/patch-unknownfn (pwo2→pow2) → LOGIC_VALUE/regen-from-spec | 3 | pass |
| S09-type-dupfn | TYPE, DUPFN | DUPFN/patch-dupfn → TYPE/patch-type-argunquote | 3 | pass |
| S10-syntax-format | SYNTAX, OUTPUT_FORMAT | SYNTAX/patch-brace → OUTPUT_FORMAT/patch-add-newline | 3 | pass |
| S11-arity-name | ARITY, NAME | NAME/patch-unknownfn (ad2→add) → ARITY/patch-arity (drop) | 3 | pass |
| S12-syntax-type-format | SYNTAX, TYPE, OUTPUT_FORMAT | SYNTAX → TYPE/delbadassign → OUTPUT_FORMAT/add-newline | 4 | pass |
| G05–G10 | (gen, 2-pattern T4) | first-attempt gen | 1 | pass |
| X3-unprovable | — | gen → UNKNOWN_GOAL sentinel → diagnose GEN | 1 | halt-genfail |
| X4-undefloop | NAME (unfixable: no similar name) | NAME scores, patch-unknownfn fails | 1 | halt-no-patch |

Defect-class coverage across S01–S12: SYNTAX×5, NAME×6, ARITY×4, TYPE×5,
DUPFN×2, OUTPUT_FORMAT×3, LOGIC_VALUE×1.

## Hardness pilot validation (§3a)

At budget 2, no repair seed can pass (all need ≥3 iterations): expected
Q_c = 6/18 = 33.3% — well below saturation. At budget 4, the ten 3-iter
seeds pass and the two 4-iter seeds (S06, S12) pass exactly at the budget
edge. Hardness is by construction (iteration floor), not by tricking the
diagnoser.
