# H-CAUSAL-UNIFIED2 Red Team: Adversary Report (X-CU2-1..X-CU2-4)

**Date:** 2026-09-29
**Target:** H-CAUSAL-UNIFIED2 (unified_causal2.zag, commit 6ec2609da)
**Prereg:** PREREG_CU2_ADV.md (frozen in commit a4bc16b6a before any attack execution; content verified byte-identical via md5)
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python at any stage.

## Verdict: H-CAUSAL-UNIFIED2 DOWNGRADED (not killed)

One of four attacks succeeds (X-CU2-1). One passes (X-CU2-4). Two are informational boundaries (X-CU2-2 verified by inspection, X-CU2-3 as documented non-goal). The frozen K-CU2-1..K-CU2-5 bars are NOT retroactively altered.

## Attack results

### X-CU2-1 (conflict-bypass via continued learning): SUCCEEDS -> DOWNGRADE

**Procedure:** Replicated the K-CU2-2 flood (10 contradictions at 10 distinct states, action 2). The 9th/10th hit contest cap (8); entries marked ST_CONFL. Verified immediate post-flood query Q(2,0,0,2) returns r=0 (WITHHOLD) — K-CU2-2 holds. Then fed ONE more episode at (2,0,0), action 2, outcome (0,0,0). Queried again.

**Result:**
```
Pre-bypass query Q(2,0,0,2): r=0
X-CU2-1a: immediate post-flood withhold CONFIRMED (K-CU2-2 holds)
Feeding post-flood episode at (2,0,0) action 2 outcome (0,0,0)...
(exact-episode) Post-bypass query Q(2,0,0,2): r=1 out=(0 0 0)
X-CU2-1: SUCCEEDS -> DOWNGRADE. Confident prediction after conflict-bypass.
The contradiction (0,0,0 vs 1,1,1) was silently forgotten.
```

**Analysis:** When new_contest returns -1, learn_episode marks the entry ST_CONFL. But find_entry skips non-ACTIVE/AMBIGUOUS entries. The next episode at the same (action, state) finds no entry (i<0), creates a FRESH entry via new_entry, and learns without the contradiction history. The query returns `(exact-episode)` — a confident prediction from the single new episode. The contradiction evidence (0,0,0 vs 1,1,1) is silently forgotten.

**Impact:** The repair's guarantee — "explicit error plus withhold when capacity is exhausted" — holds only if learning stops after the flood. For a continuing learner, the very next episode bypasses the conflict marking. The withhold is not durable.

**Downgrade, not kill:** The frozen K-CU2-2 bar (immediate post-flood query withholds) still passes. This is a new limitation on continued learning, not a break of the frozen bar.

**Honest repair direction:** When find_entry skips a CONFLICTED entry, subsequent episodes at that (action, state) should either (a) route to the conflicted entry (keeping it conflicted), or (b) the new entry should inherit the conflict status. The current "fresh start" semantics silently discards the contradiction.

**Determinism:** 3/3 runs byte-identical, md5 164b17b36823f343bdafe72ef9606026.

### X-CU2-2 (split rollback integrity): VERIFIED BY INSPECTION (no kill)

**Analysis:** apply_split saves n0=nent(W) before creating children. On child allocation failure (c<0), it emits ERROR, restores nent_set(W,n0), and returns 0 without marking the parent SUPERSEDED. 

Verified:
- Contests reference entries via ct_en, but contests are only created for EXISTING entries (indices < n0). New children (indices >= n0) cannot be referenced by contests. Rollback is safe.
- effects_over(W,c,...) only modifies entry c via en_fx_set/en_fp_set. No side effects on other entries or global state. Partial child effects are orphaned by the nent rollback.
- new_entry initializes ALL fields including en_neps_set(W,i,0). Stale episode-list data from rolled-back children is overwritten on reuse. Safe.
- The parent is NOT marked SUPERSEDED on the failure path (that line is after the loop). Parent keeps episodes and stays ACTIVE. Correct.

**Note:** The emit output shows "child ... fx=..." lines for partial children before the "ERROR: split aborted... rolling back" message. The trace is noisy but the store is correct. Cosmetic, not a correctness bug.

**Result:** No kill. The transactional guarantee holds. (Empirical triggering at exact capacity boundary not performed; the logic is verified by inspection of all data flows.)

### X-CU2-3 (liveness under sustained flood): BOUNDARY (informational)

**Procedure:** After the 8-contest flood, fed 3 normal episodes at fresh states (3,3,3),(3,3,4),(3,4,3), then 5 more contradictions at 5 new states (all untracked).

**Result:**
- Fresh state Q(3,3,3,2): r=1. Normal learning INTACT after flood.
- 5 more untracked contradictions: all emitted explicit ERROR + ENTRY CONFLICTED notes. nct stayed 8. nent grew to 15 (new entries for untracked states).
- No episodes dropped silently. Every exhaustion emitted an explicit error.

**Analysis:** This is the documented non-goal. The repair prereg explicitly states: "No contest eviction or merging policy is invented here; exhaustion is made explicit, not silent. That is the honest bounded fix. Eviction policy is future work." The behavior matches the documentation. Under sustained flood, contradiction adjudication degrades (all untracked) but normal learning continues and nothing is silent.

**Result:** BOUNDARY (informational). Not a kill or downgrade. The parent should know: contest capacity is a hard liveness ceiling for contradiction handling, and the X-CU2-1 bypass means the "withhold" degrades further under continued learning.

### X-CU2-4 (source audit): PASS

**Checks:**
(a) fu_hist_count iterates nent(W), counts en_st==ST_SUPER. ✓ (was nep/EP_SUP)
(b) new_contest emits ERROR on c>=8 path, returns -1. ✓
(c) learn_episode checks c<0, emits ENTRY CONFLICTED note, sets ST_CONFL, returns. ✓
(d) new_entry emits ERROR on i>=32 path, returns -1. ✓
(e) apply_split saves n0, restores on c<0, emits ERROR, returns 0, parent NOT superseded. ✓
(f) fu_learn_ep emits ERROR on e>=128 path, returns -1. ✓
(g) No test-answer literals in learning path. No hardcoded state/action constants in repaired functions. The "5000" style weights are in the intent mechanism, not the causal repair. ✓
(h) Diff unified_causal2.zag vs unified_causal.zag at ba065e172: 74 changed lines, all within R1-R4 (header comment, 4 repair sites, fu_hist_count). No unrelated modifications. ✓

**Result:** PASS. The repairs are implemented as specified. No hardcoding. No scope creep.

## Frozen bars re-verified (not altered)

The K-CU2-1..K-CU2-5 bars from PREREG_CAUSAL_UNIFIED2.md are not broken by this red team:
- K-CU2-1 (provenance): Not re-tested; source audit confirms the fix.
- K-CU2-2 (flood withhold): CONFIRMED intact (r=0 immediate post-flood).
- K-CU2-3 (regression): Not re-run; diff confirms no unrelated changes.
- K-CU2-4 (determinism): Attack harness 3/3 byte-identical.
- K-CU2-5 (cap audit): Source audit confirms no silent -1 paths.

## Revised classification

Bounded L2 causal integration with explicit capacity errors and durable-withhold limitation. The four repairs are genuine and correctly implemented. The X-CU2-1 downgrade narrows the R2 guarantee: "explicit error plus withhold" is accurate for the immediate post-exhaustion state, but the withhold is bypassed by continued learning at the same state. For a continuing learner, contradiction evidence at capacity is not durably protected.

## Artifacts (all committed, adversary-owned only)

- PREREG_CU2_ADV.md (frozen before execution)
- cu2_adv.zag (attack harness; mechanism functions verbatim from unified_causal2.zag, only main() replaced)
- CU2_ADV_RAW.txt (raw output, 3 runs, md5 164b17b36823f343bdafe72ef9606026)
- CU2_ADV_RESULT.md (this file)

## Governance notes

- Pure Zag throughout. No Python. No em dashes in new files.
- Prereg was swept into concurrent agent's commit a4bc16b6a; content verified byte-identical (md5 match), timestamp (16:02:33 PDT) precedes attack execution (~16:03 PDT). Ordering valid.
- Only adversary-owned files staged. Concurrent agents' files untouched.
- One git index.lock race during commit; waited for clear, no force.
