# PREREG_AMENDMENT1: mismatch and operator redesign (transparent, pre-implementation)

Frozen 2026-10-02, before any implementation commit. This amendment
re-freezes the mismatch dimension and the adaptation operator. All
kill bars K1-K11 keep their structure; only the frozen expectations
inside A1/A2 change as noted. Nothing in the committed PREREG.md is
edited; this file supersedes the Operator specification and Battery
sections where they conflict.

## What the pilot run proved

A pilot build of the frozen rename design (82 -> 83) was executed
before any implementation commit. Result: the Z query answered 106
with COMP-SEGS n=2 27 40, zero adaptation fired (ADAPT-CREATED n=0).
The unified composition's contract fallback (mechanism A:
un_satisfy -> cx_contract -> t2_gather path of matching plen) applies
MAP_Y's shape along the renamed 83-facts directly; relation identity
is irrelevant to it. The rename mismatch therefore does NOT require
adaptation under the unified pipeline. The frozen claim "exact
composition provably fails" is FALSE for the rename design, so the
rename design is withdrawn. Testing it against a C-only base would
manufacture the need by disabling part of the current architecture;
that is rejected as rigged.

## Amended mismatch (frozen)

LENGTH mismatch (interface arity differs; one of the mandated
mismatch forms). Y (ALLOC) is trained with THREE allocation steps,
relseq [82,82,82]. The Z world needs only TWO allocation steps. X
(SUM) is unchanged: relseq [81,81,81].

This defeats the full unified pipeline:
- C: Y's relseq [82,82,82] is unsatisfiable from the frontier (only
  two r82 facts exist there).
- A: no fact path from the frontier has plen 4 (MAP_Y's contract);
  the longest path there has plen 3.
- B: co-use is an ordering signal only, not an admission criterion.
- Trial: the full s-to-expected path needs 5 links (plen 6); the
  trial chain pass caps at plen 5.

## Amended operator (frozen)

Name: adapt_truncate, the TRUNCATE-TAIL operator (truncate family,
one of the four mandated forms).

Trigger unchanged: fires exactly once per query, only after
activate, rebind_try, and compose_try have all failed.

For each candidate first segment m1 from the unchanged
un_candidates (same admission and ordering as the unified DFS level
0), in order:

1. Satisfy m1 from s with un_satisfy; let v1 be the endpoint value.
   Emit TRUNC-FRONTIER m1= v1=.
2. For each live native MAP m2 (tag 20, no outgoing type-16 edge,
   m2 != m1), in node-id order: read its relation sequence R
   (length L, 1 <= L < 7) with cc_relseq.
3. Try proper prefixes of R from longest to shortest (minimal
   adaptation: the longest prefix licensed by the frontier wins);
   promote at most ONE adapted MAP per m2. For candidate prefix R'
   (length L'): emit TRUNC-TRY m2= L'=; dedup (skip if any live MAP
   already carries exactly R'); satisfiability license (R' fully
   satisfiable from v1 in the fact store); execution check
   (t2_asm_chain + t2_try_verify against its own terminal).
4. Promote with rl_promote (no fact taught: mid-query scaffolding,
   per the EXTEND-ONE invariant). Write type-16 LINK adapted -> m2.
   Emit ADAPT-MK.

After the pass, if at least one adapted MAP was created, re-run the
UNCHANGED compose_try once. Final answer verified against expected
exactly as before.

Generality (frozen claim): the operator names no relation, no MAP,
no length, and no query. The truncation depth is read from the fact
store (longest satisfiable prefix). Arm A2 (Y trained with FOUR
steps, truncated to two) proves no hardcoded truncation depth.

## Amended battery (frozen)

Training: X unchanged (ev_teach (201,81,231),(231,81,261),
(261,81,291); ev_query (201,91,291) -> MAP_X [81,81,81]). Y: ev_teach
(301,82,311),(311,82,321),(321,82,331); ev_query (301,92,331) ->
MAP_Y [82,82,82]. Distractors unchanged (30 teaches, subjects 5000+,
relations 60-69). Queries via ev_query_adapt.

- A1 L2-TREAT: Z facts (101,81,102),(102,81,103),(103,81,104),
  (104,82,105),(105,82,106). Query (101,70,106). Expect: ans=106;
  adapted MAP a with type-16 edge a->MAP_Y and relseq [82,82];
  MAP_Z LINK14 to a and to MAP_X; MAP_Z no LINK14 to MAP_Y; exactly
  one adapted MAP; trace shows TRUNC-TRY m2=MAP_Y L'=2 at v1=104.
- A2 L2-XDEPTH: Y trained with four steps: ev_teach (301,82,311),
  (311,82,321),(321,82,331),(331,82,341); ev_query (301,92,341) ->
  MAP_Y [82,82,82,82]. Z facts as A1. Query (101,70,106). Expect:
  ans=106; adapted MAP a with type-16 edge a->MAP_Y and relseq
  [82,82]; MAP_Z LINK14 to a and to MAP_X, none to MAP_Y.
- A3 L2-IMPOSSIBLE: Z facts (101,81,102),(102,81,103),(103,81,104)
  [dead end]. Query (101,70,106). Expect: ans=-2; zero type-16
  edges workspace-wide.
- A4 L1-REGRESSION: full-length world: Z facts (101,81,102),
  (102,81,103),(103,81,104),(104,82,105),(105,82,106),(106,82,107).
  Query (101,70,107) via ev_query_adapt. Expect: ans=107; zero
  type-16 edges; MAP_Z LINK14 to MAP_X and to MAP_Y.
- A5 NO-ADAPT CONTROL: A1 setup verbatim under the one-line no-adapt
  build (adapt_on()=0). Expect: ans=-2 and zero adapted MAPs.
- A6 ABL-X: A1 setup, MAP_X killed. Expect ans=-2.
- A7 ABL-Y: A1 setup, MAP_Y killed. Expect ans=-2.
- A8 FRESH: no X/Y training. Expect ans=-2.
- A9 REUSE: A1 setup, query (101,70,106) twice. Expect 106, 106;
  adapted count stays 1.

## Kill bars (unchanged in structure)

K1: A1 all assertions pass. K2: A2 all assertions pass (truncation
depth not hardcoded). K3: A3 ans=-2, zero adapted. K4: A4 passes
with zero type-16 edges. K5: A5 ans=-2, zero adapted (exact-reuse
control provably fails the mismatch task). K6: A6, A7, A8 ans=-2.
K7: A9 106/106, adapted count stable at 1. K8: 3/3 byte-identical
runs, sha256 recorded. K9: zero em/en dashes, byte-verified. K10:
un_patch.zag sha256-identical to composition_unified/un_patch.zag
(3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2);
cc_base.zag never modified. K11: 0 new edge/MAP types, 0 new
opcodes, 0 modes, 0 bridges, 0 handlers, 0 semantic cases.

Verdict XDOMAIN-L2-ADAPT-PASS iff K1-K11 all pass.
