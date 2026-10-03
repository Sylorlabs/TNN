# PREREG H-INTENT-UNIFIED: Intent Retrieval in the Unified Learner

## Hypothesis

The H-INTENT procedure-intent retrieval mechanism (scoring
cond_fire*20000 + len_match*10000 + learn_seq, gap >= 2 to select,
otherwise WITHHOLD AMBIGUOUS) can be ported into the unified learner's
query handler without breaking any of the 9 H-UNIFIED scenarios. The
unified learner then infers which stored procedure a query intends
instead of spraying all slots and rules.

## Background

- H-INTENT SURVIVES (10/10, 4/4 bars): standalone `intent_learn.zag`
  implements intent inference with an intent store (learn_seq, train_len)
  per proc slot and per bridge rule. Bridge sub-procedures receive no
  intent records and are excluded from candidacy.
- H-UNIFIED SURVIVES (9/9): `unified_learn.zag` runs routing, direct
  discovery, bridge fallback, and causal learning in one unlabeled stream.
  Its query handler `handle_proc_query_unified` applies EVERY stored
  procedure and bridge rule and reports each. This is the documented gap
  this hypothesis closes.
- Canonical intent store layout (from H-INTENT, frozen): IBASE=1560,
  16 proc slots x 8 bytes then 4 bridge rules x 8 bytes, SEQADDR=1720.
  In `unified_learn.zag` the causal store occupies 1104..1552 and WORK
  starts at 2048, so 1560..1724 is free. Verified by inspection before
  freezing this prereg.

## Mechanism (frozen)

Port into `unified_learn.zag`:

1. Add IBASE()/SEQADDR() constants and the intent functions verbatim
   from `intent_learn.zag`: `intent_init`, `intent_record_proc`,
   `intent_record_br`, `intent_proc_base`, `intent_br_base`,
   `intent_winner` (pure decision), `intent_trace_emit` (white-box trace),
   `handle_proc_query_intent` (full handler; returns 1 answered,
   0 withhold-none, -1 withhold-ambiguous).
2. In `handle_proc_learn_unified`: after `bridge_learn` returns, compute
   the uniform training input length (or -1 if varied) from PAIRBASE and
   call `intent_record_proc` (direct slot) or `intent_record_br`
   (bridge rule). Bridge sub-procedures stored inside `bridge_learn`
   receive no records (per PREREG_INTENT_AMEND1).
3. Replace the body of `handle_proc_query_unified` with the intent
   decision: emit the trace, run `intent_winner`, answer or withhold.
   Keep the function name and return convention (1 answered, 0/−1
   withhold) so callers are unaffected.
4. Call `intent_init(W)` once per workspace (main stream and each fresh
   test workspace).

## Frozen Kill Bars

- K-IU1: All 9 H-UNIFIED scenarios still PASS in the integrated binary.
  Adaptation (declared here, before implementation): the old K-U4a
  asserted the spray behavior (`nq>=2`). Under intent, query "hello"
  (n=5) after learning reverse (train_len=-1, seq 0) and the bridge rule
  (train_len=-1, seq 1, condition not firing) has scores 0 vs 1,
  gap=1 < 2, so the correct intent decision is WITHHOLD AMBIGUOUS.
  The adapted K-U4a asserts: handler returns -1, the trace shows both
  candidates with gap=1, and direct `bridge_apply` still dispatches
  "hello"->"ooooo" (bridge machinery intact). The other 8 scenarios
  (K-U1, K-U2a/b/c, K-U3, K-U4b, K-U5, K-A) assert unchanged behavior.
  Additionally the unified stream queries "xqz" (fires the bridge
  condition): the bridge rule must win on cond_fire and answer "xxx".
- K-IU2: All 10 H-INTENT checks PASS within the unified process, using
  the unified learn/query handlers on fresh workspaces: T1 setup,
  T1a (hello->ooooo via n=5 slot), T1b (abcd->dcba via n=4 slot),
  T2 setup, T2a (xqz->xxx via firing bridge), T2b (qrs->sss via ELSE),
  T3 setup, T3 ambiguity (world WITHHOLD AMBIGUOUS), T3b handler -1,
  T3c empty-store WITHHOLD.
- K-IU3: Ambiguous queries WITHHOLD with the AMBIGUOUS flag and emit no
  candidate output as the answer. Covered by T3/T3b and the adapted K-U4a.
- K-IU4: Deterministic. Three consecutive runs produce byte-identical
  output (md5).

## Test Design (frozen)

Pure Zag. Pinned znc 2026.07.0-dev (edition 2026). No Python anywhere:
no generators, no verifiers, no analysis scripts.

One integrated binary. main() runs Part A (9 adapted unified scenarios,
single stream, one workspace) then Part B (H-INTENT battery on fresh
workspaces). Total checks: 9 + 10 + 1 (xqz selection) = 20, all must
PASS. md5 over three runs for K-IU4.

## What does NOT count

- Keeping the spray handler and adding intent as a side channel.
- Recording intent for bridge sub-procedures (they must stay excluded).
- Changing the H-UNIFIED learning stream to dodge the ambiguous "hello".
- Any authored per-query hint.
- Python in any form.

## Commit order

This prereg commit strictly precedes the implementation commit.
