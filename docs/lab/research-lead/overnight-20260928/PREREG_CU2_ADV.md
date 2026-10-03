# Preregistration: H-CAUSAL-UNIFIED2 Red Team (X-CU2-1..X-CU2-4)

**Date:** 2026-09-29
**Target:** H-CAUSAL-UNIFIED2 (unified_causal2.zag, commit 6ec2609da)
**Target prereg:** PREREG_CAUSAL_UNIFIED2.md (commit 3a19b47c7)
**Status:** FROZEN (this commit). All attack code and execution follow strictly after.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Background

H-CAUSAL-UNIFIED2 SURVIVES (5/5) per RESULT_CAUSAL_UNIFIED2.md. It repaired:
- R1 (X-CU1): fu_hist_count counts ST_SUPER entries (was EP_SUP episodes).
- R2 (X-CU2): new_contest emits explicit ERROR on -1; learn_episode marks entry ST_CONFL so predict withholds.
- R3 (X-CU3): new_entry emits explicit ERROR on -1; apply_split does transactional nent rollback; fu_learn_ep emits explicit ERROR at 128-episode cap.
- R4 (X-CU4): doc states 126 functions.

This red team assumes the SURVIVES claim is false and attacks the repairs.

## Attack designs (frozen)

### X-CU2-1: Conflict-bypass via continued learning (DOWNGRADE if succeeds)

**Theory:** In learn_episode, when new_contest returns -1 (contest cap exhausted),
the entry is marked ST_CONFL(). But find_entry skips non-ACTIVE/AMBIGUOUS entries.
A subsequent episode at the same (action, state) finds no entry (i<0), creates a
FRESH entry via new_entry, and learns without the contradiction history. Queries
then return confident predictions from the fresh entry, bypassing the conflict.

**Procedure:**
1. Replicate the K-CU2-2 flood: 10 contradictions at 10 distinct states, action 2,
   outcomes (0,0,0) vs (1,1,1). The 9th/10th hit contest cap (8). Entry covering
   state (2,0,0) is marked ST_CONFL.
2. Feed ONE more episode at state (2,0,0), action 2, outcome (0,0,0).
3. Query (2,0,0,2) via fu_predict.
4. Record: does the query return r=1 (confident) or r=0 (withhold)?

**Kill criterion:** If the query returns r=1 with a confident prediction, the
repair's "explicit error plus withhold when capacity is exhausted" guarantee is
bypassed by the very next learning episode. The contradiction evidence is silently
forgotten. This is a DOWNGRADE (the frozen K-CU2-2 bar covers only the immediate
post-flood query, not continued learning; the bar itself is not broken).

**Expected honest outcome:** r=0 (withhold), because the conflict should persist.

### X-CU2-2: Split rollback integrity (KILL if partial state survives)

**Theory:** apply_split saves nent before creating children and restores it on
child-allocation failure. The comment claims "they are referenced only via the
nent count". This attack verifies the claim empirically.

**Procedure:**
1. Fill the entry store to 30 entries (cap is 32) using distinct causal episodes.
2. Trigger a split that requires 3+ children (exceeding remaining capacity).
3. After the rollback, verify: (a) nent is restored to the pre-split value,
   (b) the parent entry is still ACTIVE (not SUPERSEDED), (c) no query returns
   data from a rolled-back child.

**Kill criterion:** If nent is not restored, or the parent is corrupted
(marked SUPERSEDED without valid children, or episodes lost), or a query
reaches a rolled-back child → H-CAUSAL-UNIFIED2 KILLED (the transactional
guarantee is broken).

**Expected honest outcome:** Clean rollback, parent intact, explicit error emitted.

### X-CU2-3: Liveness under sustained contradiction flood (BOUNDARY, informational)

**Theory:** The repair's explicit non-goal: "No contest eviction or merging policy
is invented here; exhaustion is made explicit, not silent." Under sustained flood,
8 contests stay open forever (if never fed resolving episodes). This attack
characterizes the degradation.

**Procedure:**
1. Open 8 contests via contradictions at 8 distinct states.
2. Feed 20 more contradictions at 20 new distinct states (all untracked).
3. Feed normal (non-contradicting) episodes at 5 fresh states.
4. Query the fresh states and the untracked-contradiction states.

**Record:** Do normal episodes still learn? Do untracked states withhold or
predict? Is there any silent data loss (episodes dropped without error)?

**Criterion:** This is INFORMATIONAL. The prereg documents this as a non-goal.
A finding here is a BOUNDARY, not a kill/downgrade, unless episodes are dropped
SILENTLY (no error emitted) — that would be a DOWNGRADE (violates "never silent").

### X-CU2-4: Source audit (PASS/FAIL)

**Procedure:** Manual code inspection of unified_causal2.zag vs the frozen R1-R4
specifications in PREREG_CAUSAL_UNIFIED2.md.

**Checks:**
(a) fu_hist_count iterates nent(W) and counts en_st==ST_SUPER (not nep/EP_SUP).
(b) new_contest emits ERROR on the c>=8 path and returns -1.
(c) learn_episode checks c<0 after new_contest, emits ENTRY CONFLICTED note,
    sets ST_CONFL, and returns (does not proceed to effects/split).
(d) new_entry emits ERROR on i>=32 path and returns -1.
(e) apply_split saves n0=nent(W), restores nent_set(W,n0) on child c<0, emits
    ERROR, returns 0 (parent NOT marked SUPERSEDED on this path).
(f) fu_learn_ep emits ERROR on e>=128 path and returns -1.
(g) No test-answer literals ("cat", "dog", specific expected outputs) in the
    learning path. No hardcoded state/action constants in the repaired functions.
(h) Diff unified_causal2.zag vs unified_causal.zag at ba065e172: changes are
    limited to R1-R4 (plus the new file header). No unrelated modifications.

**Criterion:** Any (a)-(f) mismatch with the prereg → KILL (repair not as
specified). Any (g) hardcoding → KILL. Any (h) unrelated change → DOWNGRADE
(scope creep). All pass → X-CU2-4 PASSES.

## Kill/downgrade summary

- X-CU2-1 succeeds (confident prediction after conflict-bypass) → DOWNGRADED.
- X-CU2-2 finds partial state surviving rollback → KILLED.
- X-CU2-3 finds SILENT episode drop → DOWNGRADED. Otherwise → BOUNDARY (informational).
- X-CU2-4 finds repair not as specified → KILLED. Finds hardcoding → KILLED.

The frozen K-CU2-1..K-CU2-5 bars are NOT retroactively altered by this red team.

## Artifacts (to be committed after execution)

- PREREG_CU2_ADV.md (this file)
- cu2_adv.zag (attack harness; mechanism functions verbatim from unified_causal2.zag, only main() replaced)
- CU2_ADV_RAW.txt (raw output, 3 runs, md5)
- CU2_ADV_RESULT.md (adversary report)

Commit order: prereg (this commit) strictly before attack commit.
Only owned files staged. No binaries committed.
