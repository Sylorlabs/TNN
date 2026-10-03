# H-INTENT-UNIFIED RESULT: Intent Retrieval in the Unified Learner

## Verdict: H-INTENT-UNIFIED SURVIVES (20/20 checks, 4/4 kill bars)

## What was built

Ported the H-INTENT procedure-intent retrieval mechanism into
`unified_learn.zag` (now v2). The unified learner's query handler no
longer sprays all stored procedures and bridge rules. It infers which
stored procedure or bridge rule the querier intends and withholds on
genuine ambiguity.

Changes to `unified_learn.zag`:

1. Intent store (IBASE=1560, SEQADDR=1720) and the H-INTENT functions
   ported verbatim: `intent_init`, `intent_record_proc`,
   `intent_record_br`, `intent_winner` (pure decision), 
   `intent_trace_emit` (white-box trace), `handle_proc_query_intent`.
   Address range 1560..1724 verified free (causal store ends at 1552,
   WORK starts at 2048).
2. `handle_proc_learn_unified` now records intent after learning:
   uniform training input length (or -1 if varied) plus the global
   learn_seq. Bridge sub-procedures stored inside `bridge_learn`
   receive no records, so they stay excluded from candidacy
   (per PREREG_INTENT_AMEND1).
3. `handle_proc_query_unified` now delegates to the intent handler.
   Same name and return convention (1 answered, 0 withhold-none,
   -1 withhold-ambiguous).
4. `main()` calls `intent_init(W)` per workspace.

## Frozen bars and results

- K-IU1 (9 unified scenarios still PASS): PASS. K-U1, K-U2a/b/c, K-U3,
  K-U4b, K-U5, K-A assert unchanged behavior. K-U4a adapted as
  preregistered: query "hello" now yields WITHHOLD AMBIGUOUS (proc
  slot 0 score 0 vs bridge rule 0 score 1, gap=1 < 2) while direct
  `bridge_apply` still dispatches "hello"->"ooooo", proving the bridge
  machinery is intact. New K-U4a2: query "xqz" fires the bridge
  condition, intent selects the bridge rule on cond_fire (score 20001
  vs 0) and answers "xxx".
- K-IU2 (10 H-INTENT checks in the unified process): PASS. B-T1 setup,
  B-T1a (hello->ooooo via n=5 slot, len_match), B-T1b (abcd->dcba via
  n=4 slot), B-T2 setup, B-T2a (xqz->xxx via firing bridge),
  B-T2b (qrs->sss via ELSE), B-T3 setup, B-T3 (world WITHHOLD
  AMBIGUOUS gap=1), B-T3b (handler returns -1), B-T3c (empty store
  WITHHOLD). All run through the unified learn/query handlers on
  fresh workspaces.
- K-IU3 (ambiguous queries withhold, no silent guess): PASS. Both the
  unified-stream "hello" and battery "world" withhold with the
  AMBIGUOUS flag and emit no candidate output as the answer.
- K-IU4 (determinism): PASS. Three consecutive runs byte-identical
  (md5 293e908767f70b2136f36730d6682b69).

Total: 20/20 checks PASS.

## Evidence

- Prereg: PREREG_INTENT_UNIFIED.md (commit d959ff51f), frozen before
  implementation. Commit order verified: prereg strictly precedes
  implementation.
- Implementation: unified_learn.zag (v2 header).
- Raw output: INTENT_UNIFIED_RAW.txt (authoritative, md5 above).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned.

## Classification

Bounded L2 integration infrastructure. It composes the validated
H-INTENT ranking rule with the validated unified learn-route-revise
loop. No representational invention involved. Not L3.

## Boundaries

- Intent signals remain training-length match, recency, and condition
  firing (inherited from H-INTENT). Richer signals out of scope.
- The gap<2 ambiguity threshold is a fixed rule, not learned.
- `stress_learn.zag`, `genbias_test.zag`, and
  `unified_adversary/ulib.zag` carry their own standalone copies of
  the old spray handler; they are separate frozen experiments and
  were not modified.
- The em dash in the file header comment (line 1) predates this
  change; the implementation diff adds none.

## Governance

Pure Zag throughout. No Python used at any stage. No em dashes in
new documentation or code.
