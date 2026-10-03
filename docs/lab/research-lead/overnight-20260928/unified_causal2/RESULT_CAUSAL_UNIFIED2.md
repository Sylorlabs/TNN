# Result: H-CAUSAL-UNIFIED2 SURVIVES (5/5)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED2 (repair of H-CAUSAL-UNIFIED)
**Prereg:** PREREG_CAUSAL_UNIFIED2.md (committed 3a19b47c7, frozen before
  implementation; commit-order satisfied)
**Implementation:** unified_causal2.zag (copy of unified_causal.zag at
  ba065e172 plus exactly the four frozen repairs R1-R4;
  unified_causal.zag untouched)
**Parent verdict repaired:** H-CAUSAL-UNIFIED DOWNGRADED
  (ADV_CAUSAL_UNIFIED_RESULT.md, prereg ae0c3e0d0)
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python. Determinism via cmp/md5sum (shell).

## Verdict: SURVIVES (5/5), bounded L2 integration repair

All four red-team findings are repaired. All five frozen kill bars pass.

## Repairs (frozen in prereg, implemented as specified)

**R1 (X-CU1 provenance):** `fu_hist_count` now counts ENTRIES with
`ST_SUPER()` over `nent(W)` instead of EPISODES with `EP_SUP()` over
`nep(W)`. The CAUSHIST count agrees with the hypotheses listing it just
emitted. Doc comment corrected.

**R2 (X-CU2 flood):** `new_contest` emits an explicit error on the -1 path
naming the state. `learn_episode` marks the entry `ST_CONFL()` and emits an
entry-level note, then returns. `predict` withholds on ST_CONFL entries
(and `find_entry` skips them), so queries on the flooded state withhold
instead of predicting confidently. The K-CU5 guarantee is now: explicit
contest plus withhold when a slot exists; explicit error plus withhold
when capacity is exhausted. No silent evidence loss in either case.

**R3 (X-CU3 entry/episode caps):** `new_entry` emits an explicit error on
the -1 path. `apply_split` saves `nent(W)` before creating children and
restores it on any child-allocation failure (transactional rollback; the
partial children are referenced only via the nent count). `fu_learn_ep`
emits an explicit error on the 128-episode cap. `merge_pass`'s `if(m>=0)`
guard and `learn_episode`'s `if(i<0){return;}` now follow already-emitted
errors, so no -1 path remains silent.

**R4 (X-CU4 doc):** 126 shared machinery functions, not 127 (129 in
causal_learn.zag minus i64s, load_obs, parse_int). Port faithful; only the
count claim was wrong.

**Non-goals (as preregistered):** Capacities stay 8/32/128. No eviction
policy invented; exhaustion is explicit, not silent.

## Frozen bar results

**K-CU2-1 (provenance consistency): PASS.** After the frozen phase-C2
stream, the hypotheses listing shows 4 SUPERSEDED entries (H2, H6, H7, H8)
and CAUSHIST reports superseded=4. Listing and count agree (was 2 vs 4).

**K-CU2-2 (flood withhold): PASS.** 10 contradictions at 10 distinct states
(adversary pattern). The 9th and 10th emit
`ERROR: contest capacity (8) exhausted; contradiction at state (...) has
no contest slot; contradiction UNTRACKED` plus
`ENTRY action 2 [any] CONFLICTED: contradiction untracked (contest cap)`.
nct stays 8. Query Q(2,0,0,2) on the 9th-contradiction state returns r=0
(WITHHOLD). No confident prediction on untracked evidence.

**K-CU2-3 (regression): PASS.** Repaired binary on the frozen main: 28
PASS markers (all present in unified_causal/run_a.txt), 0 FAIL. Diff vs
run_a.txt is exactly one line: `C-HIST caus_hist routes, superseded=2`
-> `superseded=4`. No other behavioral change; no error emissions in the
frozen run (caps not reached).

**K-CU2-4 (determinism): PASS.** Main 3/3 byte-identical via cmp
(md5 87f8edc29825802327029f46f045dbe3). Flood test 3/3 byte-identical via
cmp (md5 c79afcf78a1cea546ddccedd2805b5b8).

**K-CU2-5 (entry-cap audit): PASS.** Unit driver drives new_entry to the
32-entry cap: explicit `ERROR: entry capacity (32) exhausted` observed,
-1 returned at nent=32. Unit driver drives fu_learn_ep to the 128-episode
cap: explicit `ERROR: episode capacity (128) exhausted` observed, -1
returned at nep=128. Source audit of all new_entry call sites (fu_init,
learn_episode, apply_split with nent rollback, merge_pass guarded) and the
new_contest call site (learn_episode, ST_CONFL marking): no silent -1 path
remains.

## Classification

Bounded L2 integration repair, not L3. Composes the validated H-CAUSAL
machinery with explicit failure semantics. No representational invention.

## Honest boundaries

- Contest capacity is still 8; under sustained contradiction flood the
  learner withholds rather than adjudicates. Adjudication under flood
  (eviction/merging policy) is future work.
- Entry capacity is still 32; a split that cannot allocate is aborted,
  not partially applied.
- The per-entry 64-episode list bound and u8 episode-index storage are
  pre-existing workspace limits, unchanged by this repair.

## Files

- unified_causal2.zag (repaired implementation)
- unified_causal2/RESULT_CAUSAL_UNIFIED2.md (this file)
- unified_causal2/CU2_RAW_MAIN.txt (frozen main, md5 87f8edc29825802327029f46f045dbe3)
- unified_causal2/CU2_RAW_FLOOD.txt (flood test, md5 c79afcf78a1cea546ddccedd2805b5b8)
- unified_causal2/CU2_RAW_ENTRYCAP.txt (entry-cap and episode-cap unit drivers)

No binaries committed. Test harnesses in /tmp only.
