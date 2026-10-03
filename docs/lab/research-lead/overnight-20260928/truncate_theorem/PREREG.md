# PREREG: TRUNCATE Theorem Boundary Conditions

Frozen 2026-10-02. This preregistration strictly precedes
implementation. This prereg commit contains ONLY this PREREG.md. No
kill bar below may be weakened or reinterpreted after results are
seen.

Worker: Truncate Theorem Boundary Worker. Branch: tnn-native-lab,
local only, nothing pushed.

## Objective

ADAPT-REVISION-OPS-COMPLETE proved the TRUNCATE non-staleness
theorem: a pure-prefix TRUNCATE adaptation cannot go stale while its
source is live and intact. Open: what are the exact boundary
conditions? This battery tests three boundaries:

(a) non-prefix TRUNCATE: can it go stale?
(b) TRUNCATE with damaged source: does the pure-prefix protection
    survive when the source is not intact?
(c) TRUNCATE where the world change affects the prefix itself.

Plus a positive control (T): pure-prefix TRUNCATE with an intact
source under a world change.

## Substrate facts fixed by prior work (frozen premises, not claims)

- cc_relseq(m) walks the MAP chain graph; each tag-101 cell names
  its licensing fact through a type-1 edge; a dead licensing fact
  makes the MAP unreadable (returns -1), which counts as broken.
- cc_satisfy(m, s) is value-based: it re-derives the relation
  sequence, then walks live facts from s with t2_lu_first
  (first-live deterministic lookup).
- The revision predicate (adapt_revise2, frozen verbatim): for each
  adapted MAP a (outgoing type-16 to a live src), if src is intact
  (cc_relseq(src) >= 1 and cc_satisfy(src, s) == len(src)) and a is
  not intact, revision fires with kind dispatch on the recorded
  kind (field 12). If src is not intact, the predicate never fires.
- A world change retires the old fact node (field 36 = 0); the
  learner is never told. Detection is purely experiential.
- alloc_node recycles the lowest dead node id, so world changes use
  teach-then-kill: the replacement fact lands in a fresh slot and
  the adaptation licensing is genuinely broken, not silently
  rewritten.
- Cached shortcut facts from pre-change queries are withdrawn with
  the world change in arms expecting -2, so redundant trial paths
  do not confound the signal.
- A retired MAP slot may be recycled; "retired" observably means
  "no longer a live MAP (tag 20 with field 36 = 1)".
- Operational definitions: a MAP is LIVE iff tag 20 and field
  36 = 1. It is INTACT iff cc_relseq >= 1 and cc_satisfy(s) ==
  relseq length. It is STALE iff live but not intact. "Revision
  fired for Xt" means a REVISE2-STALE emission naming Xt, or a new
  type-16 edge targeting Xt.

## The theorem and the boundary hypotheses

Theorem (prior work, restated): let src have relseq length L, let a
be its pure-prefix truncation of length k < L (same relations,
same prefix values, same licensing fact nodes by first-live
determinism). While src is live and intact, a cannot be stale.

Boundary hypotheses under test:

H-A (non-prefix): a TRUNCATE adaptation that is NOT a pure prefix
of its source CAN go stale. Construction: head-drop, the longest
proper non-prefix segment (drop exactly the first link). The
theorem proof relies on prefix licensing sharing; head-drop shares
licensing nodes with the source too, but its root differs, so the
protection is not asserted. Prediction: after a world change that
kills a licensing fact of the head-dropped segment, the adaptation
is stale (detectable), while the frozen predicate still declines
revision because the source is not intact either.

H-B (damaged source, prefix middle): with the source not intact, a
pure-prefix TRUNCATE CAN go stale. Construction: same-relation
replacement of a prefix-interior fact (teach (12,1,98), kill
(12,1,13)). Prediction: Xt licensing dead, so Xt is stale by the
predicate definition; src licensing dead too, so the predicate
gate stays closed and no revision fires. This shows the "source
intact" condition is load-bearing, not decorative.

H-C (damaged source, prefix root): same as H-B with the prefix
root link replaced (teach (11,1,77), kill (11,1,12)). Prediction:
Xt and src both stale; no revision fires.

H-T (positive control): pure-prefix TRUNCATE with an intact source
under a world change that adds a duplicate fact without killing
(teach (13,1,99), no kill). Prediction: Xt and src stay intact
(first-live determinism: the duplicate has a higher node id), no
revision fires, phase-4 re-query answers through Xt.

## Operator specification (frozen)

New file tt_patch.zag (unfrozen). Frozen copies (read-only,
sha256-verified against originals): cc_base.zag, un_patch.zag,
adapt_patch.zag, revise_patch.zag from ../adapt_revision_ops/
(which are themselves verified copies of ../composition_C/,
../composition_adapt/, ../adapt_revision/), plus ts_patch.zag from
../adapt_revision_ops/.

NONPREFIX-ONE (adapt_nonprefix): after the standard pipeline fails,
for each live native MAP m (tag 20, live, no outgoing type-16),
relseq R length L with 3 <= L < 7, fully satisfied from s
(cc_satisfy == L): build the head-drop segment R[1..L-1] (drop
exactly the first link) from values vals[1..L] and facts
fids[1..L-1]; dedup on the exact candidate relseq (skip if any
live MAP already carries it); t2_asm_chain; t2_try_verify from
the segment root (vals[1]) to the segment terminal; adapt_promote
(teaches NO fact, per the frozen adapt_patch rationale); record
kind 2 (TRUNCATE) in field 12; type-16 edge new -> m. Returns the
count created. Names no relation, MAP, length, query, or expected
value. This is a genuine TRUNCATE (it drops source links) that is
not a pure prefix of the source relseq.

ev_query_tt: ev_query_revise2 verbatim, except the fresh-adaptation
fallback runs adapt_extend + adapt_truncate + adapt_nonprefix +
adapt_specialize (in that order), then recomposes once if anything
was created. The order matters: for X = [1,1,1] the prefix
truncation [1,1] is created before the head-drop [1,1], so the
head-drop dedups away and arms B/C/T replicate the prior T1/T2
behavior exactly.

## Arm specifications (frozen)

Each arm runs in a fresh world (z_alloc + tnn2_init). Queries use
ev_query_tt with flags=0, masked=0.

### Arm A: A-NONPREFIX-STALE

1. Teach (31,1,32) = f1, (32,2,33) = f2, (33,1,34) = f3.
2. ph_train = ev_query_tt(31,71,34). Trains Z = [1,2,1].
   Withdraw the (31,71,34) shortcut fact.
3. Gap facts (10 filler teaches, as in prior drivers).
4. ph2 = ev_query_tt(32,72,34). The fallback creates the prefix
   [1,2] (31->32->33) and the head-drop Xt = [2,1] (32->33->34),
   then recomposes. Expect ph2 = 34.
5. Locate Xt: lowest-id live adapted MAP (outgoing type-16) with
   relseq exactly [2,1]. Record kind = ng(Xt,12), src16 target,
   c0 = type-16 edge count.
6. World change: ev_teach(32,5,40) (novel relation, T2 idiom),
   then kill f2. Withdraw the (32,72,34) shortcut fact.
7. ph4 = ev_query_tt(32,73,99). Expect -2.
8. c1 = type-16 edge count.

### Arm B: B-PREFIX-MID-REPLACE

1. Teach (11,1,12) = f1, (12,1,13) = f2, (13,1,14) = f3.
2. ph_train = ev_query_tt(11,71,14). Trains X = [1,1,1].
   Withdraw the (11,71,14) shortcut fact.
3. Gap facts.
4. ph2 = ev_query_tt(11,72,13). The fallback creates the prefix
   Xt = [1,1] (head-drop [1,1] dedups away). Expect ph2 = 13.
5. Locate Xt: lowest-id live adapted MAP with relseq exactly
   [1,1]. Record kind, src16 target, c0.
6. World change: ev_teach(12,1,98) (same-relation replacement),
   then kill f2. Withdraw the (11,72,13) shortcut fact.
7. ph4 = ev_query_tt(11,73,99). Expect -2.
8. c1 = type-16 edge count.

### Arm C: C-PREFIX-ROOT-REPLACE

Identical to arm B, except the world change replaces the prefix
root link: ev_teach(11,1,77), then kill f1.

### Arm T: T-THEOREM-CONTROL

Identical to arm B through step 5, except the world change only
adds a duplicate fact: ev_teach(13,1,99), no kill. Withdraw the
(11,72,13) shortcut fact. ph4 = ev_query_tt(11,73,13).
Expect ph4 = 13.

## Frozen kill bars

Arm A (non-prefix boundary):
- K-A1: ph2 = 34, and Xt exists with relseq [2,1], recorded kind
  ng(Xt,12) = 2, and type-16 Xt -> Z.
- K-A2: post-change Xt is STALE: cc_relseq(Xt) no longer reads
  [2,1]. (The theorem protection does not extend to non-prefix
  TRUNCATE: the violation is correctly detected.)
- K-A3: post-change Z is not intact: cc_relseq(Z) no longer reads
  [1,2,1]. (Documents why the predicate gate stays closed.)
- K-A4: no revision fired for Xt: no type-16 edge targets Xt and
  c1 = c0.
- K-A5: Xt is still live (not retired) and ph4 = -2.

Arm B (damaged source, prefix middle):
- K-B1: ph2 = 13, and Xt exists with relseq [1,1], recorded kind
  2, type-16 Xt -> X.
- K-B2: post-change Xt is STALE: cc_relseq(Xt) no longer reads
  [1,1]. (Pure-prefix protection requires an intact source.)
- K-B3: post-change X is not intact: cc_relseq(X) no longer reads
  [1,1,1].
- K-B4: no revision fired for Xt (no type-16 targets Xt,
  c1 = c0); Xt still live; ph4 = -2.

Arm C (damaged source, prefix root):
- K-C1: ph2 = 13, Xt = [1,1], kind 2, type-16 Xt -> X.
- K-C2: post-change Xt is STALE.
- K-C3: post-change X is not intact.
- K-C4: no revision fired for Xt (no type-16 targets Xt,
  c1 = c0); Xt still live; ph4 = -2.

Arm T (theorem positive control):
- K-T1: ph2 = 13 and Xt = [1,1] created.
- K-T2: post-change X intact (cc_relseq reads [1,1,1] and
  cc_satisfy(X,11) = 3) and Xt intact (cc_relseq reads [1,1] and
  cc_satisfy(Xt,11) = 2).
- K-T3: no revision fired for Xt (no type-16 targets Xt) and
  ph4 = 13.

Harness:
- K-D: 3/3 byte-identical runs (sha256 equal across run1..3,
  cmp clean).
- K-H1: zero em/en dash bytes in PREREG.md, REPORT.md,
  NAMECHECK.md, tt_patch.zag, tt_driver.zag.
- K-H2: the five frozen copies are sha256-identical to their
  originals; grep for mode/bridge/handler in tt_patch.zag and
  tt_driver.zag returns 0; no `as *i32` slice pattern in new
  sources; build.sh enforces the safebin guard (python3/python
  must not resolve); all research logic is pure Zag.

## Verdict rule

ALL kill bars pass: verdict TRUNCATE-THEOREM-COMPLETE. Any kill
bar fails: report the failure honestly with the observed values;
the verdict is not awarded.

## Architecture accounting (preregistered)

- Cognition lines added (unfrozen): tt_patch.zag
  (tt_nonprefix_src, adapt_nonprefix, ev_query_tt) and
  tt_driver.zag (4 arms).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New handlers: 0. New opcodes: 0. New MAP types: 0. New edge
  types: 0 (type-16 adapted-from edge reused; kind 2 recorded in
  MAP field 12 per the frozen Amendment 1 convention).
- The operators name no relation, MAP, length, query, or expected
  value.

## Predicted boundary map

- Pure-prefix + source intact: cannot go stale (arm T).
- Pure-prefix + source not intact: can go stale; predicate
  correctly declines revision (arms B, C).
- Non-prefix + source not intact: can go stale; predicate
  correctly declines revision (arm A).
- Not tested here: non-prefix TRUNCATE with an intact source
  (the substrate shares licensing nodes between a head-drop and
  its source, so any licensing death breaks both; a
  satisfaction-only staleness with intact source is not
  constructible in this substrate and is recorded as an open
  question, not a claim).
