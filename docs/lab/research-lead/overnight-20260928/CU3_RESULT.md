# H-CAUSAL-UNIFIED3 Result: SURVIVES (6/6 + 28/28)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED3 (repair of the H-CAUSAL-UNIFIED2 X-CU2-1 downgrade)
**Prereg:** PREREG_CAUSAL_UNIFIED3.md (commit 613886ade), frozen before any implementation.
**Amendment:** PREREG_CAUSAL_UNIFIED3_AMEND1.md (commit 7d7336f3f), transparent re-freeze before the corrected implementation. The frozen R1 absorb was over-broad (a mask-0 conflicted entry swallowed genuinely new states, breaking post-flood normal learning); AMEND1 scopes the absorb to conflicted entries holding live evidence at the exact state.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python at any stage (implementation, drivers, analysis, file ops).

## The repair

`unified_causal3.zag` is copied byte-identical from committed `unified_causal2.zag`
at 6ec2609da, plus exactly two additions (diff verified; `unified_causal2.zag`
untouched; `main()` byte-identical):

**R1 (X-CU2-1, as amended): durable conflict marking.** New pure query
`find_conflicted` returns the most specific ST_CONFL() entry covering
(action, state) that holds a live (non-superseded) episode at the exact
state; -1 otherwise. In `learn_episode`, when `find_entry` returns -1, the
episode is absorbed into that conflicted entry (`entry_add_ep`, status stays
ST_CONFL) with an explicit `CONFLICTED-ABSORB` note, instead of creating a
fresh ACTIVE entry that would silently forget the contradiction. Queries keep
withholding through the existing no-entry path. A 64-episode per-entry guard
emits an explicit error and refuses rather than overflowing the episode
region. Episodes at genuinely new states still take the pre-existing
fresh-entry path (v2 behavior preserved).

Design note: absorbing (rather than creating fresh conflicted entries) keeps
all evidence for the conflicted (action, state) in one entry, so a future
contest-eviction policy can adjudicate from complete evidence.

## Kill bar results

**K-CU3-1 (durable withhold): 6/6 PASS.** Exact X-CU2-1 replication:
- K-CU3-1a: flood of 10 contradictions; nct=8, 8 contests open. PASS
- K-CU3-1b: immediate post-flood query Q(2,0,0,2) returns r=0. PASS
- K-CU3-1c: bypass episode at (2,0,0) emits CONFLICTED-ABSORB; nent unchanged (no fresh entry). PASS
- K-CU3-1d: post-bypass query Q(2,0,0,2) still returns r=0. The X-CU2-1 bypass is closed. PASS
- K-CU3-1e: second bypass episode; withhold durable, nent stable. PASS
- K-CU3-1f: fresh state (3,3,3) learns normally and predicts via exact-episode (r=1). Post-flood liveness intact (AMEND1 guard). PASS

Observed flood detail: the 9th contradiction marks its entry ST_CONFL at
seq 18; the 10th contradiction's first episode takes the fresh-entry path
(no live (2,0,1) episode in the conflicted entry yet), then hits contest-cap
exhaustion and is marked ST_CONFL at seq 20, exactly as the amendment
predicted. nct stays 8 throughout.

**K-CU3-2 (regression): PASS.** Repaired main output is byte-identical to the
committed unified_causal2 main output (md5 87f8edc29825802327029f46f045dbe3):
28 PASS markers, 0 FAIL. The new path never triggers in the frozen run
(caps not reached), as required.

**K-CU3-3 (determinism): PASS.** 3/3 byte-identical main runs
(md5 87f8edc29825802327029f46f045dbe3); 3/3 byte-identical bypass-driver runs
(md5 760dcc9890a72ff35bbc393dfeb519ee).

**K-CU3-4 (explicitness audit): PASS.**
(a) The absorb path always emits its CONFLICTED-ABSORB note (2/2 observed).
(b) The 64-overflow path always emits its ERROR (code-reviewed; not triggered
in tests, which stay far below the cap).
(c) `find_conflicted` is a pure query: reads only en_st/en_a/cond_matches/
ep_st/ep_s; no store mutation.
(d) No new silent -1 or silent-drop path: every new return follows an
explicit emit. The only behavior change vs v2 is the exact repair target
(same-state re-learning after conflict).

## Verdict

**H-CAUSAL-UNIFIED3 SURVIVES.** The X-CU2-1 conflict-bypass is closed: the
withhold after contest-capacity exhaustion is now durable across continued
learning at the contradicted state, while normal learning on new states is
preserved.

## Classification

Bounded L2 causal integration with durable explicit conflict marking. Not L3
(unchanged): no new representation is invented; the repair makes an existing
guarantee hold under continued learning.

## Honest limits

- Conflicted entries never become ACTIVE again in this repair; un-conflicting
  (e.g., after new adjudicating evidence) is future work.
- Contest eviction/merging remains an explicit non-goal; capacity is still
  8/32/128 with refuse-and-warn semantics.
- The dead `en_st(W,i)==ST_CONFL()` branch in `predict` (unreachable via
  `find_entry`) was left untouched to keep the diff minimal.
- The 64-episode per-entry bound (pre-existing, disclosed in H-CAUSAL-UNIFIED2)
  is unchanged on the normal path; the new path guards it explicitly.

## Commits (branch `tnn-native-lab`, local only)

- 613886ade: PREREG H-CAUSAL-UNIFIED3 FROZEN
- 7d7336f3f: AMEND1 FROZEN (exact-state scoping)
- (this commit): unified_causal3.zag + CU3_RESULT.md + CU3_RAW_MAIN.txt + CU3_RAW_BYPASS.txt

## Raw evidence

- CU3_RAW_MAIN.txt: md5 87f8edc29825802327029f46f045dbe3 (3 runs)
- CU3_RAW_BYPASS.txt: md5 760dcc9890a72ff35bbc393dfeb519ee (3 runs)

## Governance

- Prereg strictly precedes implementation (613886ade is an ancestor of the
  implementation commit); amendment strictly precedes the corrected code.
- Only owned files staged; concurrent agents' files untouched.
- No binaries committed (builds in /tmp only). No em dashes in new files.
