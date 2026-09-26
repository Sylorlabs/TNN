# N5 Fork A — Verdict

## Genuine-substitution verdict: CONFIRMED

Fork A implements genuine L12 term rewriting with capture-variable binding.
The trace explicitly shows:
- **Schema capture**: L12 proposals cite p3=<schema> where the schema
  contains literal `$A`/`$B` capture variables (e.g., `p=[1,-2,2]`,
  `schema=S2`).
- **Equality binding**: `BIND via S<e> A="<A>" B="<B>"` logs the exact
  bytes bound from the equality premise.
- **Equality consumption**: `SUBST-REV via S<e> + S<tt> schema=S<sch>`
  consumes the equality to establish the original goal bytes.

## Minimal tests (all byte-identical across 2 runs)

| Test | Verdict | Chain |
|------|---------|-------|
| SUBST_MIN1 (n=2k → n⁴=16k⁴) | DERIVED | GOAL-SUBST (BIND n→2k) → pow-dist → num-pow → juxt → SUBST-REV |
| SUBST_NOVEL1 (m=5j → m³=125j³) | DERIVED | Same pattern, novel vars/consts/exp |
| SUBST_NOVEL2 (q=3r → q²=9r²) | DERIVED | Same pattern |
| SUBST_NOVEL3 (a=2b → a⁶=64b⁶) | DERIVED | Higher exponent |
| SUBST_NOVEL4 (t=4s → 8∣t³) | DERIVED | Divisibility witness |
| SUBST_NEST1 (x=a+b → (x+1)²=((a+b)+1)²) | DERIVED | Nested: direct X=X → SUBST-REV |
| SUBST_NEG1 (schema, no equality) | WITHHELD | Correct: no L12 without equality |
| SUBST_NEG2 (unrelated equality) | WITHHELD | Correct: no binding |

## Battery scores (sealed keys, byte-identical reruns)

- **PB1**: 8/24 (bar: ≥12/24) — NOT MET
  - 8 correct WITHHELD (R3N_04,05,10,12,15,17,21,24)
  - 2 numeric (R3N_09,11) correctly WITHHELD per task requirement
    (sealed key says DERIVED, but task mandates WITHHOLD with reason)
  - 14 DERIVED problems not derived (require K005/general reasoning
    beyond Fork A's substitution scope)
- **PB4**: 1/20 (bar: ≥12/20) — NOT MET
  - CHAIN_NL_12 DERIVED via sound L5 modus-ponens chain
  - 19 others WITHHELD (require diverse reasoning: geometry, puzzles, etc.)
- **Parser crashes**: 0 (bar: zero) — MET
  - All 88 runs (44 problems × 2) completed with rc=0
  - All reruns byte-identical

## Why the bars are not met

Fork A is a **specialized substitution magnifier**, not a general reasoner.
The L12/L13/L14 machinery proves substitution theorems genuinely, but PB1/PB4
test broad reasoning (K005 modus ponens chains, universal instantiation,
geometry, logic puzzles) that requires the full N5 L0–L11 stack working at
scale. The inherited machinery derives some (CHAIN_NL_12 via L5) but not
most.

The task's primary requirement — genuine L12 with schema + equality +
binding trace — is fully met. The battery bars assume a general reasoner;
Fork A delivers the substitution component.

## Open issues

1. **PB1/PB4 coverage**: Fork A needs the full N5 reasoning stack (or a
   general-reasoning fork) to meet the 12/24 and 12/20 bars. The substitution
   machinery is sound but narrow.
2. **Numeric problems**: Task requires WITHHOLD (done), but sealed keys
   mark R3N_09/R3N_11 as DERIVED. This is a task-vs-key tension, not a bug.
3. **Universal instantiation**: Problems like R3N_01 ("every even integer")
   need UI from definitions (K107) to get `n=2k` before L12 can fire.
   Not implemented in Fork A.

## Artifacts
- `n5a.zag`: implementation (see FORK_A_DESIGN.md)
- `tests/`: 8 minimal fixtures
- `runs/`: 8 minimal × 2 + 44 battery × 2 outputs, RUNLOG.txt
- Binary SHA-256: `4592d39ab760d78b211a01b8139ae31194497d9e8a90ed626f39ebb3971`
