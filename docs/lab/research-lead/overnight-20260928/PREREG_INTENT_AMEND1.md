# PREREG H-INTENT AMENDMENT 1 (transparent, pre-implementation)

## Reason

Design review before implementation found two issues in the frozen T2:

1. Bridge sub-procedures: when bridge_learn creates a bridge rule, it stores
   two sub-procedures in proc slots. These are only meaningful via the
   bridge rule, not as standalone query candidates. The frozen mechanism did
   not exclude them. Fix: intent store learn_seq is initialized to -1 for
   all slots; only slots with learn_seq >= 0 (i.e., recorded by an explicit
   learning event) are intent candidates. Bridge sub-procedures never
   receive intent records, so they are correctly excluded.

2. T2 interference vagueness: the frozen T2 ran on the T1 workspace, making
   the "qrs" expectation depend on cross-test interference ("no fixed
   winner asserted"). This is weak. Fix: T2 runs on a fresh W containing
   only the bridge rule. Both queries then have deterministic expected
   outcomes.

## Amended T2 (replaces frozen T2)

T2 (K-I1b, bridge condition intent), fresh W:
- Learn bridge: "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"
  (IF input[0]==120 THEN broadcast-first ELSE broadcast-last).
- Query "xqz" (n=3, starts with x): the bridge rule is the sole candidate;
  its condition fires (cond_fire=1). Expect ONLY "xxx". Trace must show
  cond_fire=1 and the winning score.
- Query "qrs" (n=3, no x): the bridge rule is the sole candidate; condition
  does not fire, ELSE branch applies. Expect ONLY "sss". Trace must show
  cond_fire=0 and single-candidate decision.

## Amended mechanism (replaces frozen step 1)

1. Candidates: every proc slot with proc_used==1 AND intent learn_seq >= 0
   that applies successfully to q, plus every used bridge rule that applies
   successfully to q. (Bridge sub-procedures are excluded by the
   learn_seq >= 0 requirement.)

Steps 2-4 unchanged. Kill bars K-I1..K-I4 unchanged. T1, T3, T4 unchanged.

## Commit order

This amendment is committed before any implementation commit.
