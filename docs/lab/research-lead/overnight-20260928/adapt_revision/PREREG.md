# PREREG: Adapted Structure Revision (revise the adaptation, not the contract)

Frozen 2026-10-02. This preregistration strictly precedes implementation.
This prereg commit contains ONLY this PREREG.md. No kill bar below may be
weakened or reinterpreted after results are seen.

Worker: Adapted Structure Revision Worker. Branch: tnn-native-lab, local
only, nothing pushed.

## Objective

Contract revision is done (value-keyed, rule-level, sequential:
sequential_revision). L2 adaptation is done (EXTEND-ONE creates derived
MAPs with type-16 adapted-from provenance: composition_adapt). Open
question: when an ADAPTED MAP proves wrong, can the learner revise the
ADAPTATION itself, rather than revising the underlying contract or
re-teaching the base MAP?

This test builds exactly that situation: the learner adapts X via
EXTEND-ONE; the adapted X' works; the world changes so that X' breaks
while X's contract still holds; the learner must revise the adaptation
(a new parameter in R1, retraction of the adaptation decision in R2).
A contract-break control (R4) proves the learner does NOT touch the
adaptation when the break is in the contract instead.

## Substrate facts fixed by prior work (frozen premises, not claims)

- Chain execution is value-based: t2_asm_chain guards on literal
  values, licensing facts are provenance only. A relation-only world
  change is behaviorally invisible, so the world change must move
  values.
- t2_lu_first and t2_gather do not honor type-3 supersede edges, so a
  world change retires the old fact node (field 36 = 0), which every
  lookup path honors. The learner is never told; detection is purely
  experiential (the post-change query fails through the normal
  pipeline).
- rebind_try is value-path based (t2_gather, cycle rejecting). A
  frontier fact that points back into the existing path (a cycle)
  defeats rebind and the contract fallback while cc_satisfy
  (relation-indexed, cycle tolerant) still admits the revised
  extension. This is what makes adaptation revision, rather than
  rebind, the operative mechanism in R1.
- TRUNCATE adaptations cannot break independently of their base (a
  truncated MAP's facts are a prefix of the base's), so EXTEND-ONE is
  the adaptation operator under test. Its vulnerable part is the
  frontier link; the base contract is the prefix.

## Operator specification (frozen)

New file revise_patch.zag (unfrozen). Frozen copies (read-only, sha256
verified): cc_base.zag from ../composition_C/cc_base.zag,
un_patch.zag and adapt_patch.zag from ../composition_adapt/.

adapt_revise(W, s, masked): revision phase, one pass, node-id order.
For each live adapted MAP a (tag 20, field 36 = 1, outgoing type-16
edge), let src be the type-16 target; skip unless src is live:

1. lsrc = cc_relseq(src) length; ls = cc_satisfy(src, s).
   Source contract intact iff lsrc >= 1 and ls == lsrc.
2. la = cc_satisfy(a, s); lalen = cc_relseq(a) length.
   Adaptation intact iff la >= 1 and la == lalen. (la == -1 with
   lalen == -1 counts as broken: an unreadable adaptation is stale.)
3. STALE iff source intact and adaptation not intact. This is the
   discrimination the experiment exists to test: the adaptation broke
   while the contract holds.
4. On STALE: emit REVISE-STALE; retire a (field 36 = 0; its edges,
   including type-16 a -> src, persist for provenance); re-extend src
   against the CURRENT world with rev_extend_src (the adapt_extend
   inner loop for one source MAP, parameterized so the new MAP's
   type-16 edge points to a, the revised adaptation, not to src).
   Emit REVISE-MK per created MAP. Returns total created.

If the re-extension finds no live frontier fact (dead end), the stale
adaptation stays retired and nothing replaces it: revision by
retraction (the EXTEND decision itself is withdrawn).

ev_query_revise: ev_query_adapt verbatim except the adapt bracket
calls adapt_revise first and adapt_extend (frozen) only as fallback
when revision created nothing:

  emit ADAPT-TRY; nmk = adapt_revise(W, s, masked);
  if (nmk == 0) { nmk = adapt_extend(W, s, masked); }
  emit ADAPT-CREATED; if (nmk > 0) re-run compose_try.

The operator names no relation, no MAP, no length, no query, and no
expected value: the revision parameter (frontier fact) is read from
the fact store, and staleness is computed from satisfiability only.

## Battery (frozen)

All arms use fresh workspaces (z_alloc + tnn2_init), train X by
ev_teach (11,1,12),(12,1,13),(13,1,14) then query (11,71,14) -> 14 via
ev_query_revise (trial promotes MAP_X, relseq [1,1,1]), then 10
distractor teaches (subjects 5000+, relations 60-69), then the phase-2
adaptation: ev_teach (14,1,15), query (11,71,15) -> 15. The adapt
bracket fires (no adapted MAPs yet, so the frozen adapt_extend
fallback creates X' = [1,1,1,1] with type-16 X' -> X), compose
re-run promotes MAP_Z. Fact node ids are captured from ev_teach
returns; the world change kills fact nodes (field 36 = 0) and teaches
replacements. The learner never observes the change except through
query outcomes.

- R1 PARAM-REVISE: world change kills (14,1,15), teaches (14,3,12)
  (frontier now cycles back to 12: rebind and the contract fallback
  cannot see any length-5 path from 11, but cc_satisfy still admits
  the revised extension). Query (11,71,12).
  Expect: ans = 12; exactly one live adapted MAP X'' exists with
  relseq [1,1,1,3] and type-16 X'' -> X'; X' retired (field 36 = 0);
  type-16 X' -> X edge persists, so provenance reads X'' -> X' -> X
  (the revision chain); MAP_X live; control query (11,71,14) -> 14
  (the contract was never touched).
- R2 RETRACT-ON-DEAD-END: world change kills (14,1,15), teaches
  nothing (frontier 14 is a dead end). Query (11,71,15).
  Expect: ans = -2; X' retired; zero live adapted MAPs; the type-16
  X' -> X edge persists (provenance of the retraction). The learner
  revised the adaptation decision to nothing rather than clinging to
  a stale structure or hallucinating a replacement.
- R3 NO-CHANGE-CONTROL: no world change. Query (11,71,15).
  Expect: ans = 15; X' live; exactly one live adapted MAP; no type-16
  edge targets X' (nothing revised it); type-16 edge count unchanged
  from pre-query. Revision is driven by the world change, not by
  re-querying.
- R4 CONTRACT-BREAK-CONTROL: world change kills (12,1,13) (inside
  the base contract), teaches (12,1,93). Query (11,71,15).
  Expect: ans = -2; X' still LIVE (the learner correctly does not
  revise or retire the adaptation when the break is in the contract);
  exactly one live adapted MAP; type-16 edge count unchanged. This is
  the mirror discrimination: adaptation revision fires if and only if
  the adaptation, not the contract, broke.

## Kill bars (frozen)

- K1: R1 all assertions pass: ans = 12; X'' live with relseq
  [1,1,1,3]; type-16 X'' -> X'; X' field 36 = 0; type-16 X' -> X
  present; MAP_X live; control query (11,71,14) ans = 14.
- K2: R2 all assertions pass: ans = -2; X' field 36 = 0; zero live
  adapted MAPs; type-16 X' -> X present.
- K3: R3 all assertions pass: ans = 15; X' live; one live adapted
  MAP; no type-16 edge with target X'; edge count unchanged.
- K4: R4 all assertions pass: ans = -2; X' still live; one live
  adapted MAP; type-16 edge count unchanged (no revision fired on a
  contract break).
- K5: 3/3 runs byte-identical (sha256 equal, cmp pairwise).
- K6: zero em/en dashes in all deliverables (byte-verified).
- K7: cc_base.zag, un_patch.zag, adapt_patch.zag copies sha256
  identical to their frozen sources; the frozen sources unmodified.

Verdict ADAPT-REVISION-COMPLETE iff K1-K7 all pass.

## Implementation plan (after prereg commit)

1. Copy the three frozen sources; sha256-verify against originals.
2. Write revise_patch.zag (rev_is_adapted, rev_src, rev_extend_src,
   adapt_revise, ev_query_revise). No changes to frozen files.
3. Write rv_driver.zag (arms R1-R4).
4. Build: cat cc_base.zag un_patch.zag adapt_patch.zag
   revise_patch.zag rv_driver.zag > rv_full.zag. Compile with the
   pinned znc in safebin PATH. Run 3x; verify byte-identical; check
   kill bars.
5. Write NAMECHECK.md (Step 0 guard, commit-order self-check, build
   records) and REPORT.md. Commit with explicit pathspecs.

## Architecture accounting (frozen constraints)

Pure Zag, safebin PATH, no Python (guard re-verified in build.sh).
Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
new MAP or edge types (type-16 adapted-from is reused for the
revision link; retirement is field 36 = 0, the existing kill idiom).
The revision operator is learner-state machinery: no conditional
dispatch on task labels anywhere (grep for mode/bridge/handler
returns 0). Output via the existing emit/e64 helpers exactly as the
frozen base does; every binary's stdout bytes verified 3/3
byte-identical before trusting them. State reads use ng/eg/get32;
no as *i32 slice construction.

## Known boundaries (not flaws in the claim)

- The world change itself is researcher-imposed, as any lab world
  change must be; the learner is not told. Detection is purely
  experiential (the post-change query fails through the normal
  pipeline, then the staleness check fires inside the adapt bracket).
- The adaptation operator class (EXTEND-ONE) is researcher-supplied
  machinery; the revision content (which frontier fact, which MAP is
  stale) is computed from the learner's own workspace state. The
  claim is learner-driven revision of an adapted structure, not
  open-ended invention (not L3).
- Single adaptation chain per arm; one world change per arm. Chained
  revisions (X'' going stale later) are out of scope; the operator is
  written generically (it skips non-live sources) but not tested
  there.
- Toy scale; mechanism demonstration with frozen bars, not a
  generality or SURVIVES claim.
