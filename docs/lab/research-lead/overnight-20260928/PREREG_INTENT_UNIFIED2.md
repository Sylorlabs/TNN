# PREREG H-INTENT-UNIFIED2: Repair of the IU4-ADV Red-Team Downgrade

## Hypothesis

The two successful IU4-ADV attacks (X-IU1 recency bypass, X-IU2
condition dominance) and the X-IU3 len_match boundary can be repaired
by (a) recording training inputs per slot/rule and adding an
exact-match specificity term that dominates condition firing,
(b) removing learn_seq from the decision score so the ambiguity guard
uses only query-informative signals, and (c) scoping len_match as the
explicitly weakest signal with a documented boundary. All 20/20 frozen
H-INTENT-UNIFIED checks keep passing.

## Background

- H-INTENT-UNIFIED DOWNGRADED by IU4-ADV (report IU4_ADV_RESULT.md):
  X-IU1 SUCCESS (recency bypass of the ambiguity guard), X-IU2 SUCCESS
  (cond_fire dominance over verbatim training evidence), X-IU3 BOUNDARY
  (len_match dominance, informational), X-IU4 PASS (port faithful).
- The 20/20 frozen checks still pass; classification stays bounded L2
  with narrowed reliability. This repair addresses the narrowed claims.
- The flaw is inherited from H-INTENT, so the repair is applied
  identically to intent_learn.zag (standalone) and unified_learn.zag
  (port), preserving X-IU4 faithfulness.

## Root causes (from the red team)

1. X-IU1: learn_seq is query-irrelevant but breaks ambiguity ties. Two
   unrelated interleaved learns flip an identical query from WITHHOLD
   to a confident pick. The builder's own gap rationale
   (PREREG_INTENT_AMEND1) is unsatisfiable while seq pollutes the score.
2. X-IU2: the scoring has no exact-match or specificity signal. A single
   coincidentally-firing byte condition (20000 points) defeats the
   learner's own verbatim training evidence for that exact input.
3. X-IU3: len_match has no causal link to procedure competence (the
   procedures are length-general per K-U1) but dominates selection.

## Mechanism (frozen)

### 1. Extended intent record

Per proc slot and per bridge rule, record
(learn_seq, train_len, in_count, in_list_off):

- in_count: number of training inputs recorded for this slot/rule.
- in_list_off: offset into the persistent string area of in_count
  (in_off, in_len) i32 pairs. The input bytes stay where
  handle_proc_learn_unified staged them; the string area is
  append-only, so the offsets remain valid.
- Cap: 16 inputs per record (documented boundary; every frozen
  battery uses at most 5).
- Layout: IBASE=1560. 16 proc slots x 16 bytes = 1560..1816.
  4 bridge rules x 16 bytes = 1816..1880. SEQADDR=1880.
  Verified free: causal store ends at 1552, WORK starts at 2048.
- Bridge sub-procedures still receive no records
  (PREREG_INTENT_AMEND1): they stay excluded from candidacy.

### 2. New scoring: query-informative signals only

- em(c,q) = 1 if q equals any recorded training input of c, else 0.
  NEW. Specificity principle: stored exact evidence dominates
  generalization heuristics.
- cf(c,q) = 1 if c is a bridge rule whose condition fires on q.
  Unchanged.
- lm(c,q) = 1 if train_len(c) >= 0 and equals q.len. Unchanged.
- qscore(c,q) = em*40000 + cf*20000 + lm*10000.
- learn_seq is still recorded and shown in the white-box trace for
  provenance, but is EXCLUDED from the decision score. Rationale:
  seq carries zero information about the querier's intent (X-IU1).

### 3. New ambiguity rule

- 0 candidates: WITHHOLD (kind -1). Unchanged.
- 1 candidate: return it. Unchanged.
- 2 or more: WITHHOLD AMBIGUOUS (kind -2) whenever the top two
  candidates tie on qscore (equal em, cf, lm), regardless of
  learn_seq. Otherwise return the top scorer.
- This implements the red team's principled rule verbatim:
  "withhold whenever the top two candidates tie on all
  query-informative signals, regardless of seq gap."

### 4. X-IU3 scoping (len_match)

- len_match is RETAINED, not removed. Reason: the frozen T1a/T1b
  checks require it. "hello" is not verbatim in the broadcast
  training ("abcde>eeeee;fghij>jjjjj"), so without lm both
  candidates tie at qscore 0 and the battery would withhold.
  Removing lm would break frozen checks; that is not a repair.
- It is now explicitly the weakest signal, dominated by exact-match
  and condition-firing, and its boundary is documented in the result:
  len_match reflects training-length coincidence, not procedure
  competence, and can misroute when training lengths are incidental.
  The X-IU3 swapped-lengths scenario is asserted as a documented
  boundary with unchanged behavior.

### 5. Faithful port

Identical repair in intent_learn.zag and unified_learn.zag.
stress_learn.zag, genbias_test.zag, and unified_adversary/ulib.zag
are separate frozen experiments and are not modified.

## Frozen Kill Bars

- K-IU2-1 (X-IU1 closed): the red-team interleaved attack workspace
  (broadcast n=5, reverse n=3, reverse n=4, reverse n=5 learned in
  that order) queried with "hello" WITHHOLDS AMBIGUOUS (kind -2).
  The adjacent-learn baseline also withholds (kind -2).
- K-IU2-2 (X-IU2 closed): D trained "xqw>wqx;xab>bax" plus the bridge
  rule (condition input[0]==120). Query "xqw" returns kind 0
  (proc slot D) and the answer is "wqx". Verbatim training evidence
  beats the firing bridge condition.
- K-IU2-2b (no overcorrection): query "xzz" (fires the bridge
  condition, verbatim in NO training set) still selects the bridge
  rule (kind 1) and answers "xxx". The em term must not break
  legitimate condition routing.
- K-IU2-3 (no regressions): repaired intent_learn.zag main() scores
  10/10 PASS; repaired unified_learn.zag main() scores 20/20 PASS.
  Rationale for safety: em never fires on any frozen-battery query
  (no query is verbatim in its workspace's training inputs; verified
  by inspection before freezing), and every frozen withhold/pick
  verdict is preserved under qscore ties (shown per-check in the
  result doc).
- K-IU2-4 (determinism): three consecutive runs of each binary
  (intent_learn, unified_learn, iu2_fix) produce byte-identical
  output (md5).
- K-IU2-5 (X-IU3 boundary documented): swapped-lengths workspace
  (reverse n=5 "abcde>edcba;vwxyz>zyxwv", broadcast n=4
  "abcd>dddd;wxyz>zzzz"), query "abcd" still routes to broadcast via
  len_match and answers "dddd" (behavior unchanged); the result doc
  records this as the declared len_match boundary.

## Test Design (frozen)

Pure Zag. Pinned znc 2026.07.0-dev (edition 2026). No Python anywhere:
no generators, no verifiers, no analysis scripts, no scratch tooling.

- iu2_fix.zag: byte-copy of the repaired unified_learn.zag with
  main() replaced by F1 (X-IU1 baseline + interleaved attack,
  scenarios replicated exactly from iu4_adv.zag), F2 (X-IU2 repair),
  F2b (no overcorrection), F3 (X-IU3 boundary). Asserts the K-IU2-1,
  K-IU2-2, K-IU2-2b, K-IU2-5 verdicts above.
- Regression: the repaired intent_learn.zag and unified_learn.zag
  mains run unmodified (K-IU2-3).
- Raw outputs committed: IU2_FIX_RAW.txt (authoritative for F1..F3),
  plus regression raws. md5 over three runs per binary (K-IU2-4).
- Only repair-owned files staged and committed. No other agent's
  files touched.

## What does NOT count

- Keeping learn_seq in the decision score in any form or weight.
- Changing any frozen 20/20 scenario to dodge a new withhold verdict.
- Recording intent for bridge sub-procedures.
- An em implementation that consults anything beyond the slot/rule's
  own recorded training inputs.
- Python in any form.

## Commit order

This prereg commit strictly precedes the implementation commit.
