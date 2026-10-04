# H-CAUSAL-UNIFIED3 Red Team: Adversary Report (CU3_ADV)

**Date:** 2026-09-29
**Target:** H-CAUSAL-UNIFIED3 (unified_causal3.zag) — claimed SURVIVES (6/6 + 28/28)
**Prereg:** PREREG_CU3_ADV.md (commit f92aad7a4, frozen before any attack code)
**Amendment:** PREREG_CU3_ADV_AMEND1.md (swept into affff1aa4; content
byte-identical to intent, prereg strictly ancestral — see Governance)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere (fixtures, harnesses, analysis).

## Verdict: H-CAUSAL-UNIFIED3 SURVIVES this red team

All four preregistered attacks were executed. None fired a kill or
downgrade criterion. One disclosed honest limit was confirmed as a
BOUNDARY. The repair does what it claims, scoped exactly as amended.

## Attack results

### X-CU3-1 (Absorb correctness): HOLDS

**X-CU3-1a (exact X-CU2-1 replay):** Flood of 10 contradictions at action 2
reproduced the committed trace (nct=8, 9th/10th marked ST_CONFL at seq
18/20). Post-flood query r=0. Bypass episode at exact (2,0,0) emitted
CONFLICTED-ABSORB, nent unchanged, post-bypass query r=0. The X-CU2-1
bypass is closed on the repaired binary. No kill criterion fired.

**X-CU3-1b (superseded-evasion):** Code proof: the sole EP_SUP writer is
`contest_feed`, reachable only through the ACTIVE path of `learn_episode`;
`find_entry` never returns ST_CONFL entries; `merge_pass` only merges
ST_ACTIVE entries. Therefore a ST_CONFL entry's episodes can never be
superseded, and the `find_conflicted` exact-state requirement can never be
defeated by supersession. Empirical: runtime invariant scan over all four
attack workspaces (flood, both scope probes, split-failure probe) found 0
superseded episodes inside ST_CONFL entries. F2 confirmed. No kill.

**X-CU3-1c (dead-zone permanence):** 20 consistent episodes at the
contradicted (2,0,0) were all absorbed with explicit notes; queries stayed
r=0; nent stable. The withhold did not flip to confident. This confirms
the DISCLOSED honest limit ("conflicted entries never become ACTIVE
again; un-conflicting is future work") as stated. Classified BOUNDARY, not
a kill: the blackhole is permanent and explicit, exactly as the prereg
discloses. A continuing learner that later receives adjudicating evidence
for a conflicted state has no recovery path in this repair; that remains
future work.

### X-CU3-2 (Scope, AMEND1 exact-state): HOLDS

- **2a:** (2,0,2) after flood (mask-covered, no exact-state episode) took
  the fresh-entry path (nent+1, no absorb note) and learned normally
  (r=1). No over-absorb.
- **2b:** action 3 at (2,0,0) took the fresh-entry path and learned (r=1).
  No cross-action absorb.
- **2c:** (2,0,0) action 2 with third outcome (5,5,5) was absorbed
  (nent unchanged), withhold preserved. Absorb is outcome-agnostic as the
  frozen design requires. No under-absorb.
- **2d (informational):** split-failure ST_CONFL (XOR data, "no single-var
  split resolves" at seq 4) absorbs at its exact state uniformly with the
  contest-cap path. All three ST_CONFL sources are treated identically by
  the repair.

### X-CU3-3 (Regression): HOLDS

Recompiled the committed unified_causal3.zag unmodified: 3/3 runs
byte-identical, md5 87f8edc29825802327029f46f045dbe3, exactly matching the
committed CU3_RAW_MAIN.txt. 28 PASS markers, 0 FAIL. No regression.

### X-CU3-4 (Source audit): HOLDS

- (a) `find_conflicted` contains zero `_set` calls: pure query, no store
  mutation.
- (b) Both returns in the absorb block textually follow an explicit emit
  (ERROR on the 64-guard; CONFLICTED-ABSORB on absorb). No silent path.
- (c) Added-line literals are structural only (0/1 counters, 64 disclosed
  guard, 1/2/4 mask bits). No test-answer literals.
- (d) `main()` byte-identical between unified_causal2.zag and
  unified_causal3.zag.
- (e) `find_conflicted` has exactly one call site (`learn_episode`).

## Determinism

Attack harness: 3/3 byte-identical runs (md5
356f9076af18f5aeeb787ab02ba35c32). Regression binary: 3/3 byte-identical.

## Classification

Bounded L2 causal integration with durable explicit conflict marking,
unchanged. Not L3. The repair closes the X-CU2-1 bypass exactly as
claimed, with the exact-state scope implemented as amended. The permanent
conflict blackhole is the sharpest remaining limitation: it is explicit
and disclosed, not silent, and un-conflicting is acknowledged future work.

## Governance notes

1. Prereg f92aad7a4 strictly precedes all attack execution (verified; no
   attack binary existed before the freeze).
2. AMEND1 was written before any attack code was built, but its commit
   was swept into concurrent worker commit affff1aa4 ("Paper: H-CAUSALV2
   SURVIVES") via broad staging. Committed content verified byte-identical
   to the authored file; prereg f92aad7a4 verified strict ancestor of
   affff1aa4. Ordering (freeze before execution) is preserved. This is the
   same broad-staging pattern previously recorded; only-owned-paths
   staging was followed on this side.
3. Attack harness mechanism lines 1-2328 are byte-verbatim copies of the
   committed unified_causal3.zag (cmp-verified); only `main()` replaced.
4. No Python used at any stage. No em dashes in loop documents. No frozen
   bars altered. No binaries committed (builds in /tmp only).

## Deliverables (this commit, branch tnn-native-lab)

- causal_unified3_adversary/cu3_adv.zag (attack harness)
- causal_unified3_adversary/cu3_adv_main.zag (attack main source)
- causal_unified3_adversary/CU3_ADV_RAW.txt (3/3 identical, md5
  356f9076af18f5aeeb787ab02ba35c32)
- causal_unified3_adversary/CU3_ADV_RESULT.md (this report)

## Suggested follow-up for parent

The natural next step is un-conflicting: a principled adjudication path
that can retire a ST_CONFL entry when later evidence resolves the
contradiction, without reintroducing the X-CU2-1 silent-forget. The
X-CU3-1c fixture (20 absorbed consistent episodes, permanent withhold) is
the regression test for that work.
