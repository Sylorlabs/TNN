# Integration Step C: F-LEAK Repair Status

**Worker:** Integration Step C Worker
**Date:** 2026-09-30
**Verdict:** STEP-C-COMPLETE (fix already applied and verified)

## Finding

The F-LEAK bug (bridge-full slot waste on failed splits) was **already repaired** by H-FLEAKFIX on 2026-09-29. The Integration Scout's Gap G10 listing ("confirmed, unrepaired") was outdated.

## Evidence

### 1. H-FLEAKFIX SURVIVES

- **Prereg:** `PREREG_FLEAKFIX.md` (frozen before implementation)
- **Result:** `FLEAKFIX_RESULT.md` - Verdict: SURVIVES. All four frozen kill bars PASS.
- **Date:** 2026-09-29

### 2. Fix applied to all 4 files

The transactional repair (rollback via `proc_set_used(...,0)` on failure paths) is present in:

1. `bridge_learn.zag` - 2 occurrences of "F-LEAK FIX"
2. `stress_learn.zag` - 2 occurrences of "F-LEAK FIX"
3. `unified_learn.zag` - 2 occurrences of "F-LEAK FIX" (lines 622-630)
4. `genbias_test.zag` - 2 occurrences of "F-LEAK FIX"

Each file has both fix locations:
- Bridge store full: roll back both s1 and s2
- Second proc store failed: roll back s1

### 3. Fix verified working (this worker)

Built `fleaf_test.zag` with znc 2026.07.0-dev and ran it:

```
=== F-LEAK attack tests ===

--- K-F1a: bridge-full attack ---
K-F1a: rc=-1, proc used unchanged (2->2). PASS

--- K-F1b: proc-nearly-full attack ---
K-F1b: rc=-1, proc used unchanged (15->15). PASS

--- K-F3: B-A6b 15-distractor ---
K-F3: bridge rule 0, 2/16 slots, dispatch verified. PASS

=== F-LEAK RESULT: 3/3 ===
```

Zero slots wasted on failure paths. The fix works correctly.

### 4. No regression

Per FLEAKFIX_RESULT.md:
- `unified_learn.zag`: 9/9 PASS (H-UNIFIED SURVIVES)
- `stress_learn.zag`: 17/17 PASS (H-STRESS SURVIVES)
- `genbias_test.zag`: 6/6 PASS (H-GENBIAS SURVIVES)
- `bridge_learn.zag`: 7/7 PASS (H-BRIDGE SURVIVES)

## Why the Scout was wrong

The Integration Scout (2026-09-30) listed G10 as "confirmed, unrepaired" based on CANONICAL_STATE.md, which was last updated before H-FLEAKFIX was applied. The canonical state document was not updated after the fix SURVIVED.

## Action taken

None required. The fix is already in place, tested, and passing. This report documents the verification.

## Recommendation

Update CANONICAL_STATE.md to reflect that F-LEAK is repaired (H-FLEAKFIX SURVIVES). The "unrepaired" language in lines 326, 519, 592 should be corrected.

## Compliance

- Pure Zag: yes (test built and run with znc, no Python)
- No em dashes: verified
- Owned path only: `docs/lab/research-lead/overnight-20260928/integration_step_c/`
- No code changes made (fix already present)
