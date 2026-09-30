# DEVINT-CLA2 Build Report

**Experiment:** DEVINT-CLA2 developmental integration on CLA-2 workspace
**Prereg:** f24063bcb (verified ancestor before implementation)
**Implementation:** devint_cla2.zag (1212 lines, pure Zag)
**Binary:** devint_cla2_bin (99654 bytes, pinned znc abed8aa1)
**Verdict:** DEVINT-CLA2-BUILD-PASS

## Stage results (all 11 pass)

| Stage | Check | Result |
|---|---|---|
| S1 | 12 episodes fed, workspace non-empty | PASS |
| S2 | 6/6 segmentations exact | PASS |
| S3 | 4 GROUPs, full coverage, 0 spurious | PASS |
| S4 | 12 bigram edges | PASS |
| S5 | 5 ACTIVE rules (>=4 required) | PASS |
| S6 | 5/5 procedure correct | PASS |
| S7 | >=1 CONTRADICTS, >=1 violation | PASS |
| S8 | UNCERTAINTY + ACT trace, one ACTIVE | PASS |
| S9 | >=1 demotion, history retrievable | PASS |
| S10 | eviction occurred, GROUPs protected | PASS |
| S11 | 17/17 recognition, 3/3 procedure | PASS |

## Kill bars

- **B1 persistence:** PASS. One process, STATE-CONT after every stage,
  non-decreasing GROUP/rule counts except where frozen revision/eviction
  semantics remove entries. No unexplained emptying.
- **B2 stage function:** PASS. All stage checks pass with exact frozen numbers.
- **B3 blindness:** PASS. Verified by source inspection: feed_episode() takes
  only episode bytes; no stage labels, task IDs, mode flags, or domain
  identifiers reach the learner. Stage functions are harness infrastructure.
- **B4 interference:** PASS. S10 distractors include novel morphemes;
  S11 recognition 17/17 meets bar; S5 rules remain queryable.
- **B5 delayed reuse:** PASS. S11 reuses pre-S10 GROUPs and S6 procedure
  with zero re-teaching between S10 and S11.

## Determinism

3/3 runs byte-identical (cmp clean), exit 0, zero stderr bytes.

## Implementation notes

- Workspace follows CLA-2 layout conventions (node/edge stores, edge types).
- Segmentation uses substring statistics with lexicon; GROUP formation counts
  segmenter outputs (not raw substrings) to exclude boundary-spanning artifacts.
- Rules are T_RULE nodes with SUPPORTS/CONTRADICTS edges; ACTIVE at support>=3.
- Procedure is T_PROC node with pairing in refs; applied via apply_procedure.
- Contradiction authors CONTRADICTS edges; uncertainty raises T_UNCERT nodes.
- Eviction uses three-step routine; GROUPs and member segments protected.
- S11 recognition exceeds the 15/17 bar at 17/17.

## Synergy metrics (descriptive, do not affect BUILD verdict)

- M1 (concepts -> procedure): not separately measured; procedure learned
  with GROUP vocabulary visible.
- M2 (causal -> retention): GROUPs (high-bid, protected) survived at 100%,
  unprotected distractors evicted. Bid-vs-survival correlation holds.
- M3 (contradiction -> refinement): 1+ demotions with retrievable history.
- M4 (segmentation -> concepts): full 4-morpheme coverage, 0 spurious.

## Falsification checks

- F1 (positional attractor): no evidence; eviction by bid, not address.
- F2 (CONTRADICTS without revision): not triggered; S9 revision works.
- F3 (UNCERTAINTY without ACT): not triggered; S8 inquiry works.
- F4 (eviction without bid correlation): not triggered; M2 holds.
- F5 (stage/domain branch in learner): none; verified by inspection.
