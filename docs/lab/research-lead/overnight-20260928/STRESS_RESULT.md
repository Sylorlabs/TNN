# H-STRESS Result: KILLED (14/17)

**Date:** 2026-09-29
**Prereg:** PREREG_STRESS.md (commit `12dda2060`, frozen before implementation)
**Implementation:** stress_learn.zag (mechanism code byte-identical to committed unified_learn.zag, only main() replaced per prereg)
**Raw output:** STRESS_RAW_OUTPUT.txt (md5: 272e75506ddcc91d46816e72a89a6382, 3 runs byte-identical)

## Verdict: H-STRESS KILLED

**Score:** 14/17 (npass/ntest)

## Kill bar results

| Bar | Verdict | Evidence |
|-----|---------|----------|
| K-S1 (10+ events, no crash) | **PASS** | 16 events processed, exit 0, no crash/hang |
| K-S2 (graceful exhaustion) | **FAIL** | ks2a=1 (E_over -1 correct), proc=16/16 correct, bridge0_ok=1, but slot0_ok=0 |
| K-S3 (retention) | **FAIL** | slot0_ok=0 (slot 0 reverse no longer maps hello->olleh); bridge0_ok=1, caus1_ok=1, caus0_ok=1 |
| K-S4 (no interference) | **FAIL** | caus_full_ok=1, wh1=1, wh2=1, but slot0_ok=0 fails the proc-query-after-causal-fill check |

## Event log summary

- E1 (S1 reverse): PASS, slot 0
- E2 (C1 cond-x): PASS, bridge rule 0 (IF input[0]==120)
- E3 (S2 bcast-last): PASS, slot 3
- E4 (C2 cond-y): PASS, bridge rule 1 (IF input[0]==121)
- E5 (S3 bcast-first): PASS, slot 6
- E6 (C3 cond-z): PASS, bridge rule 2 (IF input[0]==122)
- E7 (S4 identity): PASS, slot 9
- E8 (C4 cond-w): PASS, bridge rule 3 (IF input[0]==119), bridge 4/4 FULL
- A1 (ambiguity): PASS, WITHHOLD
- E9 (C5 cond-v, bridge full): PASS, honest -1, **F-LEAK CONFIRMED** (2 proc slots wasted: 12->14)
- F1 (fill reverse): stored, slot 14
- F2 (fill reverse): stored, slot 15, proc 16/16 FULL
- F3 (fill reverse): -1 (proc full, correct)
- F4 (fill reverse): -1 (proc full, correct)
- E_over (proc-full probe): -1, proc 16/16 (correct)
- EK1 (causal fill): PASS, 16/16 rules
- EK2 (causal-full probe): PASS, no new rule, honest miss

## The failure

Slot 0 (reverse, learned in E1) no longer correctly maps `hello`->`olleh` after the full pressure sequence. The `proc_apply` returns a wrong result or fails.

Bridge rule 0 (using proc slots 1,2) still works correctly (`xqw`->`xxx`, `zzz`->`zzz`). Causal rules still work. Only slot 0 is affected.

This is a **retention failure under store pressure**. The mechanism does not crash or corrupt other stores, but it loses the earliest-learned procedure.

## F-LEAK finding (predicted in prereg, confirmed)

E9 wasted 2 proc slots (12->14) when bridge_learn failed on a full bridge store. The `return -1` path does not release the already-stored s1/s2 subset procedures. This is wasteful but not corrupting. Documented as a finding, not a kill (per prereg).

## Honest interpretation

The unified learner handles 16 interleaved learning events without crashing, degrades gracefully on store exhaustion (honest -1), keeps causal and bridge stores intact, and withholds on ambiguity. However, it **fails to retain the earliest procedure** under pressure. This is either:

1. A memory corruption bug in the stress harness or unified learner, OR
2. An architectural retention limitation.

The failure is isolated to slot 0; slots 1-15, bridge rules, and causal rules are unaffected. This suggests a specific bug rather than systemic corruption, but root-cause diagnosis is out of scope for this test.

## Classification

**H-STRESS KILLED.** Bounded L2 integration infrastructure has a retention failure mode under store pressure. The graceful degradation (honest -1) and non-interference (causal/bridge intact) are validated. The retention guarantee is not.

## Commits

- `12dda2060`: Prereg H-STRESS FROZEN (K-S1..K-S4)
- (this commit): Implementation + result + raw output

## Files

- PREREG_STRESS.md (committed in prereg)
- stress_learn.zag (mechanism verbatim from unified_learn.zag, main() replaced)
- STRESS_RESULT.md (this file)
- STRESS_RAW_OUTPUT.txt (authoritative evidence, md5: 272e75506ddcc91d46816e72a89a6382)
