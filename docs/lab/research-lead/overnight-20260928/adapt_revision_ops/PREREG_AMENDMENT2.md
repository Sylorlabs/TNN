# PREREG Amendment 2: shortcut withdrawal and T1/T2 edge-count bar

Status: pre-implementation (no implementation committed yet; the
trial run below used uncommitted scratch sources only). This
amendment changes only driver instrumentation and two kill-bar
clauses. It does not change the operators, the revision predicate,
the battery structure, or the expected answers.

## Finding 1: the training shortcut pollutes SPECIALIZE

The trial run (T1-FAIL, S1-FAIL; T2/S2/S3-PASS) showed that
SPECIALIZE-ONE creates a spurious [71] MAP in phase 2. Cause: the
phase-1 training query (11,71,14) teaches the shortcut fact
(11,71,14) via promote_graph, and SPECIALIZE-ONE (which scans every
link for alternative relations) treats it as a live alternative at
link 0. A cached query answer is not a world regularity and must
not license a specialization.

Fix (driver only): ts_train_x now withdraws (11,71,14) immediately
after training. MAP_X is unaffected (the MAP persists; only the
shortcut fact is retired). This matches the Amendment-2 spirit of
the prior work: withdraw cached consequences that confound the
adaptation signal.

## Finding 2: the phase-4 fallback adapts MAP_Z

In T1 phase 4, after adapt_revise2 correctly creates nothing (Xt
not stale), the fresh-adaptation fallback scanned the native
MAP_Z (the phase-2 composition result, relseq [1,1], no type-16)
and created [1,1,9] (extend via the new (13,9,40) fact) and [1]
(truncate). This is correct learner behavior (the pipeline failed;
the learner tries to adapt), but it changes the type-16 edge count,
failing the preregistered "edge count unchanged" clause in K-T1
(and K-T2 has the same exposure).

Fix (kill bars only): K-T1 and K-T2 drop the strict edge-count
equality clause. The essential "no revision" check is retained and
is direct: no type-16 edge targets Xt (p4), and Xt stays live (p3).
The fallback creating unrelated adaptations from MAP_Z is not a
revision of the TRUNCATE adaptation and does not touch Xt.

## Revised kill bars (frozen)

- K-T1: phase-2 ans = 13; phase-4 ans = -2; Xt live; no type-16
  edge with target Xt; cc_satisfy(X,11) != 3. (Edge-count clause
  removed.)
- K-T2: phase-2 ans = 13; phase-4 ans = -2; Xt live (not retired);
  no type-16 edge with target Xt. (Edge-count clause removed.)
- K-S1, K-S2, K-S3, K-D, K-H1, K-H2: unchanged.

## Unchanged

- Operators (ts_patch.zag), revision predicate, kind dispatch.
- Battery arms, queries, expected answers.
- The TRUNCATE theorem.
- Commit order: this amendment is committed alone before the
  implementation.
