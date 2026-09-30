# STEP-D RESULT: Merged DEVINT1 and DEVINT2 Curricula

**Verdict: STEP-D-COMPLETE.** All 6 kill bars PASS.

## What Was Built

**File:** `merged_curriculum.zag` (1572 lines)

Single binary containing:
- DEVINT1 curriculum (11 stages: S1-S11, morpheme stream learner)
- DEVINT2 curriculum (7 stages: S1-S7, rule store learner)
- Single main() calls devint1_run() then devint2_run()
- No process reset between curricula
- Single process, persistent execution

**Merge method:** Mechanical composition.
- DEVINT1's main renamed to devint1_run()
- DEVINT2's main renamed to devint2_run()
- Duplicate helpers (z_alloc, emit, i32s, get32, set32) deduplicated
- i64s kept (unique to DEVINT2)
- New main() emits headers and calls both sequentially

## Kill Bar Results

**K-D1 (compiles):** PASS. znc compiled with warnings only (19 in DEVINT1 section, 2 in DEVINT2 section, all pre-existing). Binary 200900 bytes.

**K-D2 (DEVINT1 identical):** PASS. Merged DEVINT1 section matches standalone baseline byte-for-byte. Diff exit 0.

**K-D3 (DEVINT2 identical):** PASS. Merged DEVINT2 section matches standalone baseline byte-for-byte. Diff exit 0.

**K-D4 (single binary):** PASS. One main() function. No exec/fork. Verified by inspection.

**K-D5 (pure Zag):** PASS. Zero Python. Zero em-dash bytes (verified via od).

**K-D6 (determinism):** PASS. 3/3 runs byte-identical. md5 3ca746e8b381ae455ef46e4ed938a7c1.

## Test Output Summary

**DEVINT1:** BUILD-PASS
- S1-S11 all complete
- Final: SYNERGY pack=505, BUILD-PASS

**DEVINT2:** BUILD-PASS
- S1-S7 all complete
- All 6 bars PASS (K-D2-1 through K-D2-6)
- Final: DEVINT2 BUILD-PASS

## Gap Closure

**G1 functionally closed:** There is now a single binary that runs the full developmental curriculum (both DEVINT1 and DEVINT2 trajectories).

**Caveat:** This is functional composition, not architectural unification. The two learners use different state representations (morpheme stream vs integer-coded rules) and different W buffer layouts. True unification on the unified backbone remains future work (blocked by Step B architectural incompatibility).

## Files

- `PREREG_STEPD.md` (frozen prereg)
- `merged_curriculum.zag` (implementation)
- `STEPD_RESULT.md` (this file)
- `devint1_part.zag`, `devint2_part.zag` (intermediates, can be deleted)

## Governance

- Prereg 2757df508 strictly precedes implementation
- Pure Zag, no Python
- No em dashes
- Owned path only
- Commits local
