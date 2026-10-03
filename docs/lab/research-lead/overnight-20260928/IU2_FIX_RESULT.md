# H-INTENT-UNIFIED2 RESULT: Repair of the IU4-ADV Red-Team Downgrade

## Verdict: H-INTENT-UNIFIED2 SURVIVES (5/5 repair bars, 30/30 total checks)

Both successful IU4-ADV attacks are closed, the X-IU3 boundary is
documented, and all 30 frozen regression checks still pass
(10/10 standalone H-INTENT battery, 20/20 H-INTENT-UNIFIED battery).
Classification remains bounded L2 integration infrastructure.

## What was repaired

### X-IU1: recency bypass of the ambiguity guard (CLOSED)

Root cause: learn_seq is query-irrelevant but broke ambiguity ties, so
two unrelated interleaved learns flipped an identical query from
WITHHOLD to a confident pick.

Repair: learn_seq is still recorded and shown in the white-box trace
for provenance, but is EXCLUDED from the decision score. The ambiguity
guard now uses only query-informative signals: withhold AMBIGUOUS
whenever the top two candidates tie on qscore (equal exact_match,
cond_fire, len_match), regardless of learn_seq. This implements the
red team's principled rule verbatim.

### X-IU2: cond_fire dominance over verbatim training evidence (CLOSED)

Root cause: the scoring had no exact-match or specificity signal, so a
single coincidentally-firing byte condition (20000 points) defeated the
learner's own verbatim training evidence.

Repair: the intent record now persists each slot/rule's training
inputs (in_count plus an (in_off, in_len) list in the persistent
string area; input bytes stay where the learn handler staged them,
string area is append-only; cap 16 inputs per record, documented).
New specificity term: em(c,q) = 1 if the query equals any recorded
training input. qscore = em*40000 + cf*20000 + lm*10000, so verbatim
stored evidence dominates any generalization heuristic.

### X-IU3: len_match dominance (SCOPED as documented boundary)

len_match is RETAINED, not removed: the frozen T1a/T1b checks require
it ("hello" is not verbatim in broadcast training, so without lm both
candidates tie at qscore 0 and the battery would withhold). It is now
explicitly the weakest signal, dominated by exact-match and
condition-firing. Documented boundary: len_match reflects
training-length coincidence, not procedure competence, and can
misroute when training lengths are incidental. The swapped-lengths
scenario keeps its old behavior, now asserted as the declared
boundary rather than a surprise.

## Mechanism (as implemented, identical in both files)

- Intent record layout: IBASE=1560. Per proc slot 16 bytes
  [learn_seq, train_len, in_count, in_list_off]: 16 slots =
  1560..1816. Per bridge rule 16 bytes: 1816..1880. SEQADDR=1880.
  Verified free: causal store ends at 1552, WORK starts at 2048.
- Bridge sub-procedures still receive no records
  (PREREG_INTENT_AMEND1): excluded from candidacy, unchanged.
- intent_winner: qscore = em*40000 + cf*20000 + lm*10000; tie on
  qscore between top two -> WITHHOLD AMBIGUOUS (kind -2).
- intent_trace_emit: now shows exact_match per candidate plus the new
  score; seq still traced for provenance.
- Applied identically to intent_learn.zag (standalone) and
  unified_learn.zag (port, now v3), preserving X-IU4 faithfulness.
  stress_learn.zag, genbias_test.zag, unified_adversary/ulib.zag
  untouched (separate frozen experiments).

## Frozen bars and results

- K-IU2-1 (X-IU1 closed): PASS. Interleaved attack workspace
  (broadcast n=5, reverse n=3, reverse n=4, reverse n=5) queried with
  "hello" WITHHOLDS AMBIGUOUS (kind -2, gap 0). The adjacent-learn
  baseline also withholds. Trace: bcast5 and rev5 tie at qscore 10000
  despite seq 0 vs 3. (IU2_FIX_RAW.txt, F1)
- K-IU2-2 (X-IU2 closed): PASS. D trained "xqw>wqx;xab>bax" plus the
  bridge rule (input[0]==120). Query "xqw": kind 0, proc slot D,
  answer "wqx". Trace: D em=1 lm=1 score=50000 vs bridge em=0 cf=1
  score=20000, gap 30000. (F2)
- K-IU2-2b (no overcorrection): PASS. Query "xzz" (fires the bridge
  condition, verbatim in no training set): kind 1, bridge rule,
  answer "xxx". Trace: D em=0 lm=1 score=10000 vs bridge cf=1
  score=20000. Legitimate condition routing intact. (F2b)
- K-IU2-3 (no regressions): PASS. Repaired intent_learn.zag main():
  10/10 PASS (IU2_INTENT_REG_RAW.txt). Repaired unified_learn.zag
  main(): 20/20 PASS (IU2_UNIFIED_REG_RAW.txt). Safety by
  construction: em never fires on any frozen-battery query (no query
  is verbatim in its workspace's training inputs, verified by
  inspection before freezing), and every frozen withhold/pick verdict
  is preserved under qscore ties.
- K-IU2-4 (determinism): PASS. Three consecutive runs byte-identical
  per binary: iu2_fix md5 e5db4304b184cee4d9f708c0a3347d9f,
  unified_learn md5 904de9f83a2873c7a8862b71804a9065,
  intent_learn md5 98315faec8faea24e75533892c0b240d.
- K-IU2-5 (X-IU3 boundary documented): PASS. Swapped-lengths
  workspace (reverse n=5, broadcast n=4), query "abcd" routes to
  broadcast via len_match, answer "dddd" (behavior unchanged,
  recorded here as the declared len_match boundary). (F3)

Total: 5/5 repair checks + 10/10 + 20/20 = 35/35.

## Evidence

- Prereg: PREREG_INTENT_UNIFIED2.md (commit a6ffebe24), frozen before
  implementation. Commit order: prereg strictly precedes
  implementation.
- Implementation: intent_learn.zag (repaired), unified_learn.zag
  (repaired, v3).
- Repair tests: iu2_fix.zag (byte-copy of repaired unified_learn.zag
  with main() replaced by F1/F2/F2b/F3; attack scenarios replicated
  exactly from iu4_adv.zag).
- Raw outputs (authoritative): IU2_FIX_RAW.txt (md5 above),
  IU2_UNIFIED_REG_RAW.txt, IU2_INTENT_REG_RAW.txt.
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
- Binaries not committed (repo convention); rebuild via
  znc iu2_fix.zag -o iu2_fix (etc.).

## Classification

Bounded L2 integration infrastructure. The repair composes the
validated specificity principle (exact stored evidence dominates
generalization) with the validated query-informative scoring. No
representational invention involved. Not L3.

## Boundaries

- len_match remains a weak heuristic with the documented X-IU3
  boundary: it can misroute when training lengths are incidental.
- The 16-training-input cap per record is a documented boundary.
- The gap<2 rule is replaced by the qscore-tie rule; seq no longer
  influences any decision, only the trace.
- A future red team should probe: em collisions between two slots
  trained on identical inputs, adversarial training sets engineered
  to create em ties, and whether in_count/list integrity survives
  bridge_learn failure paths (records are only written on success).

## Governance

Pure Zag throughout. No Python used at any stage: no generators, no
verifiers, no analysis scripts, no scratch tooling. No em dashes in
new documentation or code. Only repair-owned files staged and
committed; no other agent's files touched. CANONICAL_STATE.md not
edited (dedicated updater owns that file); suggested summary block
is in the handoff report.
