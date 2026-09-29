# RESULT: H-FDCR-UNIFIED2 Repair — SURVIVES (5/5 kill bars, 23/23 preserved)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED2 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED DOWNGRADED (red team: FDCR_UNIFIED_ADV_RESULT.md)
**Prereg:** `PREREG_FDCR_UNIFIED2.md` (frozen; content committed in
  d926eb0f6 before implementation; see Governance Note 1)
**Verdict:** SURVIVES. All 5 frozen kill bars pass. All 23/23 original
  tests still pass. Deterministic 3/3.

## Repairs Implemented

All four repairs from the prereg were implemented in
`unified_fdcr2.zag` (copy of `unified_fdcr.zag`; original unmodified).

### R1: Majority-vote concept association (X-FU1)

`handle_proc_learn_unified` no longer uses only the first training
input. It now:

- Computes the concept for every training input via
  `con_find_member_str`.
- For each distinct concept, counts how many inputs are members.
- Selects the concept with the highest count.
- Requires strict majority: `count * 2 > nseg`. Otherwise -1.
- Ties: first-seen wins (disclosed).

Evidence (K-FU2-1):
```
ULEARN: direct discovery -> proc slot 0 (intent seq recorded, train_len=3, concept=-1)
K-FU2-1a P1 (1/2 members) train_con=-1 PASS
ULEARN: direct discovery -> proc slot 1 (intent seq recorded, train_len=3, concept=0)
K-FU2-1b P2 (2/2 members) train_con=0 PASS
```

P1 trained on `cat>tac;bat>tab` (only 1/2 inputs are concept members)
now correctly receives no association. The coarse first-input-only
behavior is closed.

### R2: Feature accumulation (X-FU2)

`handle_concept_learn` restructured to two passes:

- Pass 1 parses all facts into (subject, feature) pairs (max 16 per
  batch, disclosed).
- Pass 2 groups by subject, accumulates each subject's full feature
  set (deduplicated, max 8), then either:
  - Extends the subject's existing concept (cross-batch, via
    `con_find_member_str`), or
  - Calls `con_form` once with the full set (nfeat may exceed 1).

The call site now passes nfeat>1. The "multi-feature FORM" claim is
now true of the integration, not just the infrastructure.

Evidence (K-FU2-2):
```
ULEARN concept: subject [cat] nfeat=1 -> concept 0 (total nfeat=2)
K-FU2-2a cross-batch: 1 concept, nfeat=2 PASS
ULEARN concept: subject [bird] nfeat=2 -> concept 0 (total nfeat=2)
K-FU2-2b within-batch: 1 concept, nfeat=2 PASS
```

Two facts for `cat` in separate calls now produce one concept with
two features, not two fragmented concepts.

Disclosed limitation: extending a concept's feature set does not
re-evaluate other existing members against the enlarged set. This is
a v2 simplification, not full FDCR revision.

### R3: Trace consistency (X-FU4b)

`intent_trace_emit` now computes `qcon`, `pcon`, and `cb` for proc
candidates (as `intent_winner` does) and displays `concept_boost=`
plus the full score `lm*10000+cb*5000+seq`. Bridge candidates display
the boost and `cf*20000+lm*10000+cb*5000+seq`.

Evidence (K-FU2-3):
```
INTENT query [dog] qlen=3
  cand kind=proc slot=0 len_match=1 train_len=3 seq=0 concept_boost=1 cond_fire=0 score=15000
  cand kind=proc slot=1 len_match=1 train_len=3 seq=1 concept_boost=0 cond_fire=0 score=10001
K-FU2-3 winner=P1 (concept boost) PASS
```

The trace now explains the actual winner. A user reading the trace
sees P1 at 15000 beating P2 at 10001, matching `intent_winner`'s
decision. The white-box violation is closed.

### R4: Bridge concept support (X-FU3 boundary)

- New `intent_record_br_con` records concept association for bridges.
- `handle_proc_learn_unified` uses majority-vote (R1) for bridge
  concept association.
- `intent_winner` bridge scoring: `cf*20000+lm*10000+cb*5000+seq`.
- `intent_trace_emit` shows bridge concept boost.

The X-FU3 boundary is closed by extension: concepts now inform bridge
selection as well as procedure selection. The existing
`intent_record_br` (concept=-1) is retained but unused by the unified
handler.

## Kill Bar Results

- **K-FU2-1:** PASS (2/2). Majority vote works: 1/2 yields -1, 2/2
  yields concept 0.
- **K-FU2-2:** PASS (2/2). Cross-batch and within-batch accumulation
  both produce single multi-feature concepts.
- **K-FU2-3:** PASS (1/1). Trace shows `concept_boost=1` and
  `score=15000`; winner matches.
- **K-FU2-4:** PASS (23/23). Full original suite preserved. See
  `FDCR_UNIFIED2_RAW.txt`.
- **K-FU2-5:** PASS. Three runs byte-identical.
  - 23/23 suite: md5 `4dac4dd34d657364fa4f85d93858839b`
  - Kill bars: md5 `b1908ba8bcf0588ffbc9021cc4851554`

## Classification

Bounded L2 integration repair. The downgrades are addressed. No L3
claimed. The mechanism remains white-box and causally traceable.

## Governance Notes

1. **Prereg sweep:** The prereg file `PREREG_FDCR_UNIFIED2.md` was
   committed as part of `d926eb0f6` (another agent's H-MEM2 prereg
   commit) via a concurrent-agent sweep. The content is byte-identical
   to the frozen prereg (md5 verified). The prereg strictly precedes
   the implementation commit. The commit message is incorrect (says
   H-MEM2), which is a hygiene issue documented here, not a
   prereg-order violation.

2. **Pure Zag:** No Python used in implementation, tests, or
   analysis. All edits via file tools and shell (cp, sed, head,
   tail). Compilation via `znc`. Test execution via compiled binaries.

3. **No mechanism hardcoding:** The repairs use only generic logic
   (majority vote, feature accumulation, score display). No fixture
   literals in mechanism code.

4. **Original preserved:** `unified_fdcr.zag` unmodified. All repairs
   in `unified_fdcr2.zag`.

## Files

- `PREREG_FDCR_UNIFIED2.md` (frozen prereg)
- `unified_fdcr2.zag` (repaired implementation)
- `fdcr_unified2_kbtest.zag` (kill bar test harness)
- `FDCR_UNIFIED2_RAW.txt` (23/23 suite output, run 1)
- `FDCR_UNIFIED2_KB_RAW.txt` (kill bar output, run 1)
- `FDCR_UNIFIED2_RESULT.md` (this file)
