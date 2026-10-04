# Prereg: H-UNIFIED (End-to-End Unlabeled Learn-Route-Revise Loop)

**Date:** 2026-09-29
**Status:** FROZEN before implementation
**Hypothesis:** H-UNIFIED

## Hypothesis

A single pure-Zag continuing learner can process an unlabeled item stream
containing simple procedure tasks, conditional procedure tasks, causal tasks,
and queries, by:

1. Inferring task type from input structure (H-ROUTER machinery, committed as
   05a00279d).
2. Attempting direct procedure discovery on PROC_LEARN items; on failure,
   automatically triggering conditional induction via the revision bridge
   (H-BRIDGE machinery with the B-A6b fix, committed as 974a9ca13).
3. Routing causal items to causal induction (H-CAUSAL machinery).
4. Answering queries from the appropriate store, including bridge-rule
   dispatch for conditional procedures.

No P/C/Q prefixes. No process reset. One stream, one process.

## What Is New

H-ROUTER routed PROC_LEARN items only through direct discovery; the bridge
was a separate executable. This unifies them: a PROC_LEARN item that fails
direct discovery automatically attempts bridge induction within the same
process and the same item-handling path.

## Design (pre-implementation)

- Workspace layout: proc store (16 slots) at pbase, bridge rule store
  (4 rules) at bbase, causal store (16 rules) at cbase, plus work, pair,
  string, and seq-staging areas.
- `handle_proc_learn_unified`: parse line into str>str pairs, stage them
  into W, call `bridge_learn` (direct-first, then bridge). Returns slot,
  1000+bslot, or -1.
- `handle_proc_query_unified`: apply every stored procedure AND every stored
  bridge rule (via bridge_apply), reporting each. Bridge rules reference
  proc slots, so conditional capability is exercised at query time.
- Router, causal learn/query, and WITHHOLD behavior copied from the
  committed `route_learn.zag` unchanged.
- Bridge machinery (`bridge_learn`, `bridge_apply`, `pdiscover_dry`,
  `br_store`) copied from the committed `bridge_learn.zag` unchanged.

## Kill Bars (frozen)

- **K-U1 (simple procedure):** Unlabeled `"abc>cba;xy>yx"` routes PROC_LEARN,
  direct discovery stores a program, and query `"hello"` applied at that
  slot yields `"olleh"`.
- **K-U2 (conditional procedure):** Unlabeled conditional item
  (`"xab>xxx;abc>ccc;def>fff;xcd>xxx"`) routes PROC_LEARN, direct discovery
  fails, bridge induces `IF input[0]==120 THEN <first> ELSE <last>`, and
  query dispatch yields `"xqw"->"xxx"` and `"zzz"->"zzz"`.
- **K-U3 (causal):** Unlabeled causal episodes route CAUS_LEARN, rules are
  learned, and a causal query predicts correctly.
- **K-U4 (queries):** Unlabeled queries route to the correct store and
  produce correct answers, including at least one answer that exercises a
  bridge rule.
- **K-U5 (no interference):** After all learning, the reverse program from
  K-U1 still applies correctly, and the causal prediction from K-U3 still
  fires correctly.

## Verdict Rule

H-UNIFIED SURVIVES iff K-U1..K-U5 all PASS on a deterministic run
(byte-identical across 3 runs). Any FAIL kills H-UNIFIED.

## Honest Limitations (declared before running)

1. Routing predicates are authored structure checks, not meta-learned
   (inherited from H-ROUTER).
2. Bridge conditions are single (pos,val) equality only (inherited from
   H-BRIDGE).
3. Procedure-query reports all slots and rules; slot/intent selection is
   out of scope (inherited from H-ROUTER).
4. This is integration infrastructure, not L3 evidence. The components
   were each independently validated and red-teamed; this tests their
   composition.
5. The conditional training item uses researcher-arranged pairs (same shape
   as the H-BRIDGE Task A); the bridge genuinely searches the condition
   from the data (verified by the H-BRIDGE red team, B-A1 PASS).

## Commit Order

This prereg is committed BEFORE any implementation file. The implementation
commit follows and must not modify this file except to mark it superseded
if the bars are later revised (a new prereg would be required).
