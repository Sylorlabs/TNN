# PREREG H-INTENT: Procedure-Intent Retrieval

## Hypothesis

When the continuing learner receives a procedure query, it can infer which
stored procedure the querier intends, instead of applying all slots and
reporting each. Intent is inferred from query context available to the
learner: training-length match, learning recency, and bridge-condition
firing. On genuinely ambiguous queries the learner withholds instead of
guessing silently.

## Background

H-ROUTER (canonical 1.6) boundary: "Slot selection out of scope: procedure
queries apply all stored procedures and report each (slot, output). Intent
retrieval is future work."

H-UNIFIED (canonical 1.7) boundary: "Procedure queries report all
slots/rules; intent selection out of scope."

This hypothesis closes that documented gap. It is bounded L2 integration
infrastructure, not L3 evidence: no representational invention is involved.

## Mechanism (frozen)

Intent store: per proc slot and per bridge rule, record (learn_seq,
train_len). learn_seq is a global monotonic counter incremented at each
successful learning event. train_len is the uniform training input length,
or -1 if training lengths varied.

At query time for input q:

1. Candidates: every proc slot and bridge rule that applies successfully
   to q.
2. Score per candidate c:
   score(c) = cond_fire(c,q) * 20000 + len_match(c,q) * 10000 + learn_seq(c)
   where cond_fire = 1 if c is a bridge rule whose condition fires on q
   (0 otherwise), len_match = 1 if train_len(c) == q.len (0 otherwise).
3. Decision:
   - 0 candidates: WITHHOLD (no procedure applies).
   - 1 candidate: return it.
   - 2 or more: let g = score(top) - score(second). If g >= 2, return top
     and list the rest as alternatives. If g < 2, WITHHOLD with AMBIGUOUS
     flag.
4. Emit an inspectable trace: per candidate (kind, slot, len_match,
   learn_seq, cond_fire, score) and the decision.

Rationale for the gap threshold: learn_seq values are distinct integers,
so g < 2 with equal cond_fire and len_match means the top two were learned
in immediately adjacent events with no other distinguishing signal. That is
genuinely ambiguous; recency alone is too weak to guess on silently.

## Frozen Kill Bars

- K-I1: On unambiguous queries, returns ONLY the intended procedure's
  output. The output bytes must equal the intended procedure's semantics
  on the query. The trace must show the winning score components.
- K-I2: On ambiguous queries (top two within gap < 2), WITHHOLDS with the
  AMBIGUOUS flag. It must not emit any candidate's output as the answer.
- K-I3: The intent trace is inspectable: for every candidate the trace
  emits kind, slot, len_match, learn_seq, cond_fire, and score, plus the
  final decision and gap.
- K-I4: Deterministic. Three runs produce byte-identical output (md5).

## Test Design (frozen)

Pure Zag. Pinned znc 2026.07.0-dev. No Python anywhere.

T1 (K-I1a, length disambiguation):
- Learn reverse on n=4 pairs: "dcba>abcd;wxyz>zyxw".
- Learn broadcast-last on n=5 pairs: "abcde>eeeee;fghij>jjjjj".
- Query "hello" (n=5): expect ONLY "ooooo" (broadcast-last). Slot for
  n=5 must win on len_match.
- Query "abcd" (n=4): expect ONLY "dcba" (reverse). Slot for n=4 must win
  on len_match.

T2 (K-I1b, bridge condition intent):
- Learn bridge: "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"
  (IF input[0]==120 THEN broadcast-first ELSE broadcast-last).
- Query "xqz" (n=3, starts with x): expect ONLY "xxx". The firing bridge
  rule must win on cond_fire.
- Query "qrs" (n=3, no x): bridge ELSE branch applies; reverse/broadcast
  slots from T1 may also apply. Expect the decision trace to resolve by
  score; the test asserts the returned output equals the top scorer's
  output and the trace is inspectable (no fixed winner asserted here
  beyond score-consistency, since T1 slots interfere by design).

T3 (K-I2, ambiguity):
- Fresh state. Learn reverse on n=5: "abcde>edcba;vwxyz>zyxwv".
- Learn broadcast-last on n=5: "abcde>eeeee;fghij>jjjjj".
- Query "world" (n=5): both apply, both len_match, adjacent learn_seq,
  gap = 1 < 2. Expect WITHHOLD with AMBIGUOUS flag and no answer output.

T4 (K-I4): run the full test binary three times, md5 of outputs identical.

## What does NOT count

- Returning all slots (the old handle_proc_query_unified behavior).
- Silently emitting one candidate's output on an ambiguous query.
- Any authored intent label or per-query hint supplied by the researcher.
- Python in generators, verifiers, analysis, or scratch tooling.

## Commit order

This prereg commit strictly precedes the implementation commit.
Implementation must not be committed before this file.
