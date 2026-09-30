# Integration Step B: BLOCKED

Date: 2026-09-30.
Worker: Integration Step B Worker.
Task: Port the full causal machinery (split/merge/contest, 14/14 validated) into unified_learn.zag.

## Verdict: STEP-B-BLOCKED

The port cannot be completed as specified. The architectures are fundamentally incompatible.

## The incompatibility

### unified_learn.zag (target)
- Variables: 2 (s0, s1)
- Causal store: 16 flat rules, 28 bytes each (7 i32s: used, cond_var, cond_val, action, effect_var, effect_val, status)
- Location: CBASE=1104, 448 bytes total
- Interface: `clearn(W, base, s0, s1, act, ns0, ns1)`, `cpredict(W, base, s0, s1, act, out[2])`
- No episodes, no ambiguity, no contests. Simple match-and-fire.

### causal_learn.zag (source)
- Variables: 3 (v0, v1, v2)
- Data structures: episodes (state[3], action, next_state[3]), entities (per-action, with masks, condition values, effects, ambiguity flags, parent pointers, episode lists), contests (for resolving ambiguity)
- Workspace: 8940 bytes with complex layout (O_EP_S, O_EN_A, O_CT_EN, etc.)
- Interface: batch processing (`causal_learn <obs.txt> <probe.txt>`), not per-episode learn/predict
- Full split/merge/contest machinery: split_candidate, apply_split, split_attempt, find_contest, new_contest, contest_feed, merge_pass

### Why "just port it" fails

1. **Variable count mismatch (2 vs 3).** The causal logic in causal_learn.zag is written for 3 variables. The unified learner's entire causal subsystem (rules, tests, router) assumes 2 variables. Changing to 3 would break all existing unified tests (K-U3, K-U4, K-U5).

2. **Data structure incompatibility.** The split/merge/contest functions operate on episodes, entities, and contests. These do not exist in unified_learn.zag. The functions cannot be copied without also copying the entire 8940-byte workspace layout and all supporting functions.

3. **Interface mismatch.** Unified uses per-episode `clearn`/`cpredict`. Causal_learn uses batch file processing with episode accumulation, then query. The 14/14 validation was on the batch interface with 3-variable problems.

4. **Workspace layout conflict.** Unified's workspace is 65536 bytes with fixed layout (PBASE=0, BBASE=1024, CBASE=1104, WORK=2048, etc.). Causal_learn needs 8940 bytes at specific offsets. There is no free 8940-byte region that doesn't conflict with existing unified structures.

## What "porting" would actually require

Option A: Extend unified to 3 variables.
- Change clearn/cpredict signatures, rule structure, all tests, router.
- Breaks backward compatibility. Requires re-validation of entire unified test suite.
- This is a redesign, not a port.

Option B: Backport split/merge/contest to 2 variables.
- Rewrite the causal logic for 2-variable episodes.
- The 14/14 validation no longer applies (different variable count, different problems).
- This changes the causal logic, violating the "do NOT change" constraint.

Option C: Shim/adapter layer.
- Keep unified's 2-var interface, internally translate to 3-var causal_learn.
- Pad with zeros, store episodes separately, translate queries.
- The "14/14 validated behavior" is not preserved (different input distribution).
- Adds complexity without clear benefit.

## Recommendation

Gap G2 cannot be closed by simple porting. The Integration Scout's Step B assumes architectural compatibility that does not exist.

Three paths forward:

1. **Accept the simplified causal store.** The unified learner's 2-variable flat rules may be sufficient for its 2-variable domain. The "full machinery" was validated on 3-variable problems that unified never encounters. G2 may be a false gap.

2. **Redesign unified for 3 variables.** A major breaking change requiring full re-validation. Only justified if 2 variables are proven insufficient for the target curriculum.

3. **Keep causal_learn.zag as a standalone component.** Use it for 3-variable problems, unified for 2-variable problems. Document the split. This is honest about the architectural boundary.

## No code changed

This worker did not modify unified_learn.zag or causal_learn.zag. No port was attempted because the prerequisites for a correct port do not exist.

## Compliance

No em dashes. No Python. Analysis only. Owned path only.
