# H-INTENT RESULT: Procedure-Intent Retrieval

## Verdict: H-INTENT SURVIVES (10/10 checks, 4/4 kill bars)

## What was built

`intent_learn.zag`: procedure-intent retrieval for the continuing learner.
Closes the documented H-ROUTER/H-UNIFIED gap ("procedure queries apply all
stored procedures and report each; intent retrieval is future work").

Mechanism:
- Intent store: per proc slot and per bridge rule, (learn_seq, train_len).
  learn_seq is a global monotonic counter bumped at each successful
  learning event. train_len is the uniform training input length, or -1
  if training lengths varied.
- learn_seq initializes to -1 for all slots. Only slots with learn_seq >= 0
  are intent candidates. Bridge sub-procedures never receive intent
  records, so they are correctly excluded from direct candidacy (they are
  reachable only via their bridge rule).
- Score per candidate: cond_fire * 20000 + len_match * 10000 + learn_seq.
  cond_fire = 1 when a bridge rule's condition fires on the query.
  len_match = 1 when train_len equals the query length.
- Decision: 0 candidates -> WITHHOLD; 1 candidate -> return it; 2+ ->
  return top iff gap >= 2, else WITHHOLD AMBIGUOUS. A gap below 2 with
  equal cond_fire/len_match means adjacent learning events with no other
  distinguishing signal: genuinely ambiguous, so the learner does not
  guess silently.
- Every query emits a white-box trace: per candidate (kind, slot,
  len_match, train_len, seq, cond_fire, score) plus the decision and gap.

## Frozen bars and results

- K-I1 (unambiguous queries return only the intended output): PASS.
  T1a: "hello" (n=5) -> "ooooo" via the n=5 broadcast slot (len_match
  decides, gap=10001). T1b: "abcd" (n=4) -> "dcba" via the n=4 reverse
  slot (gap=9999). T2a: "xqz" -> "xxx" via the firing bridge rule
  (cond_fire=1, score=20000). T2b: "qrs" -> "sss" via the bridge ELSE
  branch (sole candidate).
- K-I2 (ambiguous queries withhold): PASS. T3: reverse and broadcast-last
  both trained on n=5 in adjacent events; query "world" (n=5) gives
  scores 10000 vs 10001, gap=1 < 2 -> WITHHOLD AMBIGUOUS, no answer
  emitted. T3c: empty store -> WITHHOLD (no candidate).
- K-I3 (inspectable trace): PASS. Raw output shows per-candidate
  kind/slot/len_match/train_len/seq/cond_fire/score and the decision for
  every query.
- K-I4 (determinism): PASS. Three runs byte-identical
  (md5 93da10d04a5b9888e4f1db4cb0b41298).

## Evidence

- Prereg: PREREG_INTENT.md (commit 39638a053), frozen before implementation.
- Amendment: PREREG_INTENT_AMEND1.md (commit dbe804b3b), transparent,
  pre-implementation. Excluded bridge sub-procedures from candidacy and
  moved T2 to a fresh W.
- Implementation: intent_learn.zag.
- Raw output: INTENT_RAW_OUTPUT.txt (authoritative, md5 above).

## Classification

Bounded L2 integration infrastructure. It composes validated mechanisms
(procedure store, bridge rules, discovery) with a ranking rule. No
representational invention involved. Not L3.

## Boundaries

- Intent signals are training-length match, recency, and condition firing.
  Richer signals (query semantic content, multi-turn dialogue state) are
  out of scope.
- The gap<2 ambiguity threshold is a fixed rule, not learned.
- train_len is -1 for varied-length training; such procedures never get
  the length bonus.
- Not yet ported into unified_learn.zag's query handler; intent_learn.zag
  is a standalone validation. Porting is future work.
