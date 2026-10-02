# PREREG Amendment 1: record adaptation kind in MAP field 12

Status: pre-implementation (no implementation committed yet). This
amendment changes only how the adaptation kind is determined at
revision time. It does not change the operators, the battery, the
expected answers, or the frozen kill bars K-T1 through K-H2.

## Issue

The PREREG specifies kind inference from relseqs (ts_kind), falling
back to kind 3 (SPECIALIZE) when the stale adaptation is unreadable
(cc_relseq returns -1 because a licensing fact died). But an
EXTEND-kind adaptation that goes stale via licensing death (the
ADAPT-REVISION R1 pattern: the frontier licensing fact is killed)
is unreadable, so relseq inference would misclassify it as
SPECIALIZE and re-specialize it instead of re-extending it. The
pure-relseq inference is unsound for unreadable adaptations.

## Fix

Record the adaptation kind in MAP field 12 at promotion time.
Field 12 is written as -1 by both promote_graph (cc_base.zag) and
adapt_promote (adapt_patch.zag) and is never read for tag-20 MAP
nodes (verified by grep over all frozen sources). This uses an
existing unused field, not a new MAP type, edge type, opcode, mode,
bridge, or handler.

ts_patch.zag sets ns(W, am, 12, kind) immediately after each
adapt_promote return: kind 2 for TRUNCATE-ONE, kind 3 for
SPECIALIZE-ONE. (Kind 1 is the frozen adapt_extend, which does not
set the field; those MAPs keep field 12 = -1.)

adapt_revise2 determines the kind as: ng(W, a, 12) if it is 1, 2,
or 3; otherwise the PREREG's relseq inference as a best-effort
fallback (covers MAPs from the frozen adapt_extend). The staleness
predicate itself is unchanged (frozen verbatim).

## Unchanged

- Kill bars, battery arms T1/T2/S1/S2/S3, queries, expected
  answers, determinism bar K-D, hygiene bars K-H1/K-H2.
- The TRUNCATE theorem and its consequence (no TRUNCATE revision
  is expected to fire).
- Commit order: this amendment is committed alone before the
  implementation, per the prereg commit-order self-check.
