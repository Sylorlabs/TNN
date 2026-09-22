# battery_adaptive_fresh.json — build notes (FROZEN 2026-09-22)

12 items, all new and SHA-disjoint from `work_a1/battery_si.json`
(checked on seed+spec bytes: NONE overlap):
- 8 multi-defect repair seeds (F01–F08), each with 2–3 defects from the
  learner's known classes, piloted at budget 16 with the ORIGINAL
  `work_a1/learner` + `work_a1/driver_si.py` (control learner).
- 3 T4 gen items (G11–G13), each composing ≥2 KB patterns
  (sumprimes/fibsum: p_math+p_loop; selsort: p_sort+p_search),
  new numbers/specs vs the frozen battery.
- 1 unfixable-by-design (X5 undefined accumulator, no similar name →
  `halt-no-patch`).

The reference repair paths below are RECORDED (pilot evidence) and NOT given
to the learner. The driver only reads: id/mode/spec/seed/patterns/demo/card/tests.

## Pilot reference paths (budget 16, control learner, verbatim)

| item | defects | reference path (diagnose classes/strategies) | iters | outcome |
|---|---|---|---|---|
| F01-dupfn-arity | ARITY, DUPFN | ARITY/patch-arity → DUPFN/patch-dupfn | 3 | pass |
| F02-type-format | TYPE, OUTPUT_FORMAT | TYPE/patch-type-argunquote → OUTPUT_FORMAT/patch-add-newline | 3 | pass |
| F03-syntax-dupfn | SYNTAX, DUPFN | SYNTAX/patch-brace → DUPFN/patch-dupfn | 3 | pass |
| F04-name-format | NAME, OUTPUT_FORMAT | NAME/patch-unknownfn (mul2→mul) → OUTPUT_FORMAT/patch-add-newline | 3 | pass |
| F05-dupfn-arity-type | ARITY, DUPFN, TYPE | ARITY/patch-arity → DUPFN/patch-dupfn → TYPE/patch-type-argunquote | 4 | pass |
| F06-syntax-name-format | SYNTAX, NAME, OUTPUT_FORMAT | SYNTAX/patch-brace → NAME/patch-unknownfn (sbu→sub) → OUTPUT_FORMAT/patch-add-newline | 4 | pass |
| F07-type-name | TYPE, NAME | TYPE/patch-type-argunquote → NAME/patch-unknownfn (answr→answer) | 3 | pass |
| F08-name-logic | NAME, LOGIC_VALUE | NAME/patch-unknownfn (fibsm→fibsum) → LOGIC_VALUE/regen-from-spec | 3 | pass |
| G11–G13 | (gen, 2-pattern T4) | first-attempt gen | 1 | pass |
| X5-undefaccum | NAME (unfixable: no similar name) | NAME scores, patch-unknownfn fails | 1 | halt-no-patch |

Defect-class coverage across F01–F08: SYNTAX×2, NAME×4, ARITY×2, TYPE×3,
DUPFN×3, OUTPUT_FORMAT×3, LOGIC_VALUE×1.

## Hardness pilot validation

At budget 2, no repair seed can pass (all need ≥3 iterations). At budget 4,
the six 2-defect seeds pass and the two 3-defect seeds (F05, F06) pass
exactly at the budget edge — same hardness profile as the frozen battery.
Fresh-battery control cost at budget 4: 27 iters / 12 items = 2.25 iters/item.
