# PREREG: Adapt Revision for TRUNCATE and SPECIALIZE Operators

Frozen 2026-10-02. This preregistration strictly precedes
implementation. This prereg commit contains ONLY this PREREG.md. No
kill bar below may be weakened or reinterpreted after results are
seen.

Worker: Adapt Revision Operators Worker. Branch: tnn-native-lab,
local only, nothing pushed.

## Objective

ADAPT-REVISION-COMPLETE showed the learner can revise an EXTEND-ONE
adaptation (re-extend with a new frontier parameter, or retract).
Open question: does adapt_revise work for TRUNCATE and SPECIALIZE
adaptations? This test builds TRUNCATE-ONE and SPECIALIZE-ONE
adaptation operators (the L2 family named but never built), creates
both adaptation kinds, breaks them with world changes, and checks
whether the learner revises each with the correct operator and
parameter.

## Substrate facts fixed by prior work (frozen premises, not claims)

- Chain execution is value-based; licensing facts are provenance
  only, except that cc_relseq requires each link's licensing fact to
  be live (a dead licensing fact makes the MAP unreadable, which
  counts as broken).
- A world change retires the old fact node (field 36 = 0); the
  learner is never told. Detection is purely experiential.
- alloc_node recycles the lowest dead node id, so world changes use
  teach-then-kill: the replacement fact lands in a fresh slot and
  the adaptation's licensing is genuinely broken, not silently
  rewritten (adapt_revision Amendment 2).
- Cached shortcut facts from pre-change queries are withdrawn with
  the world change in arms expecting -2, so redundant trial paths do
  not confound the signal (adapt_revision Amendment 2).
- A retired MAP slot may be recycled; "retired" observably means
  "no longer a live MAP (tag 20 with field 36 = 1)".

## The TRUNCATE theorem (honest boundary, preregistered)

Claim: a pure-prefix TRUNCATE adaptation cannot go stale while its
source is live and intact. Proof sketch: let src have relseq length
L, let a be its prefix truncation of length k < L (same relations).
Source intact means cc_relseq(src) = L and cc_satisfy(src, s) = L.
The satisfying assignment gives values v_0..v_L with live facts for
each link. The first k links satisfy a from s, so cc_satisfy(a, s)
= k. For a to be broken while src holds, cc_relseq(a) must be -1
(some prefix licensing fact dead). But a's prefix licensing facts
are the first-live facts at truncation time, and src's prefix
licensing facts are the first-live facts at training time; src is
readable (else not intact), so its prefix licensing is live, and
first-live is deterministic, so a's prefix licensing facts are the
same live nodes. Contradiction. The only escape is pathological
slot-recycling with duplicate facts, which no arm constructs.

Consequence, preregistered: adapt_revise must NEVER fire for a
TRUNCATE adaptation. The TRUNCATE arms therefore test correct
NON-revision (discrimination), not revision. If a TRUNCATE revision
ever fired, K-T1/K-T2 would fail and the theorem would be falsified,
which is itself an informative result.

## Operator specification (frozen)

New file ts_patch.zag (unfrozen). Frozen copies (read-only, sha256
verified): cc_base.zag from ../composition_C/cc_base.zag,
un_patch.zag and adapt_patch.zag from ../composition_adapt/,
revise_patch.zag from ../adapt_revision/.

TRUNCATE-ONE (adapt_truncate): after the standard pipeline fails,
for each live native MAP m (tag 20, live, no outgoing type-16),
relseq R length L with 2 <= L < 7, fully satisfied from s
(cc_satisfy == L): build the prefix R[0..L-2] (truncate by one)
from the prefix values and facts; dedup (skip if any live MAP
already carries exactly that relseq); t2_asm_chain; t2_try_verify
to the prefix terminal; adapt_promote (teaches NO fact, per the
frozen adapt_patch rationale); type-16 edge new -> m. Returns the
count created. Names no relation, MAP, length, or query.

SPECIALIZE-ONE (adapt_specialize): after the standard pipeline
fails, for each live native MAP m, relseq R length L with
1 <= L < 7, fully satisfied from s: for each link j, for each live
non-superseded fact (v_j, r_alt, v_new) with r_alt != R[j]
(an alternative relation the world offers at that link): build the
candidate relseq R[0..j-1] ++ [r_alt], then greedily extend with
R[j+1..] from v_new as far as t2_lu_first succeeds; dedup on the
exact candidate relseq; t2_asm_chain; t2_try_verify to the
candidate terminal; adapt_promote (no fact); type-16 edge new -> m.
Returns the count created. This specializes the procedure by
committing to the world's offered alternative at one link. Names no
relation, MAP, length, query, or expected value.

Kind inference (ts_kind): from the relseqs of src and a (both
readable, else kind 3):
- kind 1 (EXTEND) iff len(a) == len(src)+1 and a[0..len(src)-1]
  equals src.
- kind 2 (TRUNCATE) iff len(a) < len(src) and a[0..len(a)-1]
  equals src[0..len(a)-1].
- kind 3 (SPECIALIZE) otherwise.
No new stored state; the kind is inferred from structure at
revision time.

adapt_revise2: the frozen adapt_revise staleness predicate verbatim
(src live; src intact: cc_relseq(src) >= 1 and cc_satisfy(src, s)
== len(src); adaptation not intact), reusing rev_is_adapted,
rev_src, and rev_extend_src from the frozen revise_patch.zag. On
STALE, dispatch by ts_kind(src, a): kind 1 -> rev_extend_src
(frozen); kind 2 -> rev_truncate_src (re-truncate src, type-16 new
-> a; expected never to fire, per the theorem); kind 3 ->
rev_specialize_src (re-run the SPECIALIZE-ONE inner loop for src
against the current world, type-16 new -> a). Retire a (field 36 =
0) AFTER construction (Amendment 2 ordering). If the re-run finds
nothing applicable, the stale adaptation stays retired: revision by
retraction. Returns total created.

ev_query_revise2: ev_query_revise verbatim except the adapt bracket
calls adapt_revise2, and the frozen fallback (when revision created
nothing) runs adapt_extend + adapt_truncate + adapt_specialize
(all three fresh operators, deterministic node-id order), then
re-runs compose_try once if anything was created.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X by
ev_teach (11,1,12),(12,1,13),(13,1,14) then query (11,71,14) -> 14
via ev_query_revise2 (trial promotes MAP_X, relseq [1,1,1]), then 10
distractor teaches (subjects 5000+, relations 60-69). Fact node ids
captured from ev_teach returns. The learner never observes world
changes except through query outcomes.

- T1 TRUNCATE-TAIL-BREAK: phase 2 query (11,72,13) -> 13.
  TRUNCATE-ONE creates Xt = [1,1] (type-16 Xt -> X); compose
  answers via Xt. World change: teach (13,9,40), kill (13,1,14)
  (teach-then-kill), withdraw shortcut (11,72,13). X broken
  (licensing dead); Xt intact. Phase 4 query (11,73,99) -> -2
  (forces the bracket; nothing reaches 99).
  Expect: ans = -2; Xt live; no type-16 edge targets Xt (no
  revision fired); type-16 edge count unchanged from post-phase-2;
  X not intact (cc_satisfy(X,11) != 3).
- T2 TRUNCATE-PREFIX-BREAK (contract break): phase 2 as T1
  (Xt = [1,1], ans = 13). World change: teach (12,5,20), kill
  (12,1,13), withdraw shortcut (11,72,13). X broken and Xt broken
  (prefix link dead). Phase 4 query (11,73,13) -> -2.
  Expect: ans = -2; Xt still LIVE (not retired: the break is in
  the contract, not the adaptation); no type-16 edge targets Xt;
  edge count unchanged.
- S1 SPECIALIZE-REVISE: phase 1 also teaches (12,2,99) (the
  alternative; captured). Phase 2 query (11,72,99) -> 99.
  TRUNCATE-ONE creates Tt = [1,1]; SPECIALIZE-ONE creates Xs =
  [1,2] via (12,2,99); compose answers 99 via Xs. World change:
  teach (12,3,98), kill (12,2,99) (teach-then-kill), withdraw
  shortcut (11,72,99). Xs broken (link and licensing dead); X
  intact. Phase 4 query (11,73,98) -> 98.
  Expect: ans = 98; exactly one live SPECIALIZE-kind revision
  Xs2 with relseq [1,3] and type-16 Xs2 -> Xs; Xs retired (not a
  live MAP); type-16 Xs -> X persists (chain Xs2 -> Xs -> X);
  MAP_X live and intact; Tt live with no type-16 edge targeting
  it (the TRUNCATE adaptation correctly untouched).
- S2 SPECIALIZE-RETRACT: phase 1 and 2 as S1 (Xs = [1,2],
  ans = 99). World change: kill (12,2,99), teach nothing (dead
  end), withdraw shortcut (11,72,99). Xs broken; X intact. Phase
  4 query (11,73,99) -> -2.
  Expect: ans = -2; Xs retired; type-16 Xs -> X persists; no new
  type-16 edges (count unchanged from post-phase-2); X live and
  intact; Tt live.
- S3 SPECIALIZE-NOCHANGE: phase 1 and 2 as S1 (Xs = [1,2],
  ans = 99). No world change. Phase 4 query (11,73,99) -> 99 via
  Xs directly (bracket does not fire).
  Expect: ans = 99; Xs live; no type-16 edge targets Xs; edge
  count unchanged.

## Kill bars (frozen)

- K-T1: T1 all assertions pass: phase-2 ans = 13; phase-4
  ans = -2; Xt live; no type-16 edge with target Xt; type-16 edge
  count equals post-phase-2 count; cc_satisfy(X,11) != 3.
- K-T2: T2 all assertions pass: phase-2 ans = 13; phase-4
  ans = -2; Xt live (not retired); no type-16 edge with target
  Xt; edge count unchanged.
- K-S1: S1 all assertions pass: phase-2 ans = 99; phase-4
  ans = 98; Xs2 live with relseq [1,3]; type-16 Xs2 -> Xs; Xs not
  a live MAP; type-16 Xs -> X present; MAP_X live;
  cc_satisfy(X,11) == 3; Tt live; no type-16 edge with target Tt.
- K-S2: S2 all assertions pass: phase-2 ans = 99; phase-4
  ans = -2; Xs not a live MAP; type-16 Xs -> X present; edge
  count unchanged from post-phase-2; MAP_X live;
  cc_satisfy(X,11) == 3.
- K-S3: S3 all assertions pass: phase-2 ans = 99; phase-4
  ans = 99; Xs live; no type-16 edge with target Xs; edge count
  unchanged.
- K-D: 3/3 runs byte-identical (sha256 equal, cmp pairwise).
- K-H1: zero em/en dashes in all deliverables (byte-verified).
- K-H2: cc_base.zag, un_patch.zag, adapt_patch.zag,
  revise_patch.zag copies sha256-identical to their frozen
  sources; the frozen sources unmodified.

Verdict ADAPT-REVISION-OPS-COMPLETE iff K-T1, K-T2, K-S1, K-S2,
K-S3, K-D, K-H1, K-H2 all pass.

## Implementation plan (after prereg commit)

1. Copy the four frozen sources; sha256-verify against originals.
2. Write ts_patch.zag (ts_relseq_present, adapt_truncate,
   adapt_specialize, ts_kind, rev_truncate_src,
   rev_specialize_src, adapt_revise2, ev_query_revise2). No
   changes to frozen files.
3. Write ts_driver.zag (arms T1, T2, S1, S2, S3).
4. Build: cat cc_base.zag un_patch.zag adapt_patch.zag
   revise_patch.zag ts_patch.zag ts_driver.zag > ts_full.zag.
   Compile with the pinned znc in safebin PATH. Run 3x; verify
   byte-identical; check kill bars.
5. Write REPORT.md; fill in NAMECHECK.md build records. Commit
   with explicit pathspecs.

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh).
Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
new MAP or edge types (type-16 adapted-from reused for revision
links; retirement is field 36 = 0). Kind is inferred from relseqs,
not stored. The operators name no relation, MAP, length, query, or
expected value. Output via the existing emit/e64 helpers; every
binary's stdout bytes verified 3/3 byte-identical. State reads use
ng/eg/get32; no as *i32 slice construction (per AGENTS.md).

## Known boundaries (not flaws in the claim)

- The world changes are researcher-imposed; the learner is not told.
  Detection is purely experiential.
- The adaptation operator classes (TRUNCATE-ONE, SPECIALIZE-ONE)
  are researcher-supplied machinery; the revision content (which
  MAP is stale, which kind, which alternative fact) is computed from
  the learner's own workspace state. Not an L3 invention claim.
- Single adaptation per kind per arm; one world change per arm.
  Chained revisions (Xs2 going stale later) are out of scope.
- Toy scale; mechanism demonstration with frozen bars, not a
  generality or SURVIVES claim.
- The TRUNCATE theorem is proved for the substrate's satisfaction
  semantics; the pathological slot-recycling escape is documented
  but not constructed.
