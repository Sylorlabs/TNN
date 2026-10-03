# PREREG: Composition Integration Retry (H-COMPINTEG-2)

Status: PREREG-FROZEN 2026-10-02. This preregistration strictly
precedes implementation. This commit contains ONLY this PREREG.md
and NAMECHECK.md (Step 0). No kill bar below may be weakened or
reinterpreted after results. VOID is terminal.

Worker: Composition Integration v2 (subagent, 2026-10-02).
Parent mandate: retry H-COMPINTEG-1 (ledger C295, verdict
COMPOSITION-INTEGRATION-INCOMPLETE) with the three INTEG-BREAK
red-team guards (ledger C305), and route the INTEG-EXEC-STALE
sentinel into the adapt/revise path (the red team's flagged open
item). One learner, single query pipeline: L2 adaptation operators
(EXTEND-ONE / TRUNCATE-ONE / SPECIALIZE-ONE) + learner-owned
verification (no harness expected answers in the integrated path)
+ self-wiring, built on the GUARDED patch copies.

## 1. The three guards (adopted as experimental copies only)

From the INTEG-BREAK red team (C305, REPORT.md). Each guard is a
copy in this lane; the red-team originals are never edited, and
the guards are NOT promoted to the frozen base. Promotion needs
Micah's ruling; this prereg records that boundary explicitly.

- GUARD-T1 (provenance gate): cc_base_g.zag marks
  learner-internal facts (ev_teach_in) with field 12 = 1;
  ts_patch_g.zag skips learner-originated facts in
  ts_specialize_src's alternative-relation filter. World-channeled
  facts still license substitution.
- GUARD-T2 (self-license veto): lvcomp_patch_g.zag records the
  prediction's source struct id in hg(W,40); lv_verify_chain
  rejects (-2, no promotion) when the verification graph's ET_DEP
  licensing facts are ALL the learner-originated prediction
  source. World-grounded verification still promotes.
- GUARD-T3 (licensing-liveness veto): cc_base_g.zag's t2_exec
  walks the graph's ET_DEP licensing facts (rt_lic_facts); if any
  is dead (field 36 != 1) or superseded, execution returns
  -999999, here named INTEG-EXEC-STALE, instead of replaying
  stale values.

## 2. Frozen design

### 2.1 Stale-sentinel routing (the red team's open item)

GUARD-T3's veto produces INTEG-EXEC-STALE (-999999) in t2_exec,
but the adapt/revise path (adapt_revise2) cannot see it: its
staleness predicate is satisfiability-only (cc_relseq /
cc_satisfy), which does NOT check supersession. A trial whose
licensing fact is superseded-but-live therefore executes stale
(the veto fires) while the revise path judges it intact. This
layer routes the sentinel into the revise decision, minimally
and with zero new learner state:

- integ2_revise_one(W,a,s,masked): per-MAP revision check. The
  staleness predicate is adapt_revise2's predicate OR an
  execution probe: t2_exec(W, ng(W,a,20), s) returning
  INTEG-EXEC-STALE. On stale, kind-dispatch exactly as
  adapt_revise2 (1 -> rev_extend_src, 2 -> ts_truncate_src,
  3 -> ts_specialize_src; all frozen), then retire a. The probe
  interprets the sentinel at the decision point; no mark bit, no
  new field, no registry is recorded anywhere.
- integ2_revise(W,s,masked): adapt_revise2's scan loop calling
  integ2_revise_one per live adapted MAP.
- compose_integ2: compose_integ (integ_patch.zag, frozen) with
  exactly one call swapped: the bracket calls integ2_revise
  instead of adapt_revise2. All other behavior (prediction gate,
  native DFS, fresh operators, kind-completion tagging, assemble,
  verify, promote with self-wiring) is verbatim.

This routing is integration glue, not a fourth guard and not new
substrate machinery: the detection already exists (GUARD-T3);
this layer only makes it visible to the revise decision. Caps
(frozen): integ2_patch.zag <= 150 lines total; 0 new edge/MAP
types; 0 new opcodes; 0 modes/bridges/handlers/semantic cases;
0 new fact fields; 0 new header slots; the token `expected`
appears nowhere in integ2_patch.zag.

### 2.2 Build

cat cc_base_g.zag un_patch.zag adapt_patch.zag revise_patch.zag
ts_patch_g.zag lvcomp_patch_g.zag integ_patch.zag integ2_patch.zag
integ2_driver.zag > integ2_full.zag, compiled with the pinned znc.
Guarded copies are byte-identical to the red-team commits
(sha256 in NAMECHECK.md Step 3). Pristine copies match the C295
values. integ_patch.zag is used frozen (it supplies
compose_integ, integ_explore, integ_tag_extend, integ_assemble).

### 2.3 K1 hand-derivation correction (frozen)

The C295 K1 failure was a hand-derivation error, not a mechanism
failure: the original prereg claimed EXTEND-ONE creates a
multi-link [1,1,1,2] trial in one step, but EXTEND-ONE extends by
exactly ONE link, so the derived terminal 108 was unreachable by
the stated construction. Correction (frozen here): the Z-world is
single-link (Amendment 1 design), and the arithmetic is shown
link by link. Training builds MAP_X with relseq [70,70,70]:

  11 -(70)-> 12 -(70)-> 13 -(70)-> 14   (training facts)

One EXTEND-ONE step from frontier 104 via the live fact
(104,2,108) creates exactly [70,70,70,2]:

  101 -(70)-> 102 -(70)-> 103 -(70)-> 104 -(2)-> 108

Terminal 108 is achievable in ONE operator step; no multi-link
leap is claimed. Every arm below shows this link arithmetic.

## 3. Battery (frozen)

All arms: fresh workspace (z_alloc + tnn2_init) unless noted.
Training (all arms): ev_teach(11,70,12),(12,70,13),(13,70,14),
then ev_query_adapt(W,11,71,14,0). The query relation (71)
differs from the fact relation (70) so no shortcut fires; the
trial promotes MAP_X with relseq [70,70,70], field 4 = 71.
30 distractor teaches (subjects 5000+, relations 60-69).
masked=0 throughout. Queries use compose_integ2; explore uses
integ_explore (frozen).

- I1 INTEGRATE-EXTEND: Z facts (101,70,102),(102,70,103),
  (103,70,104),(104,2,108). Explore: 4 cycles
  integ_explore(W,101,70,op=1,retire=1). Cycle 1: adapt_extend
  creates one trial [70,70,70,2] (frontier 104, fact (104,2,108);
  link arithmetic above), executes to 108, lv_observe teaches
  FACT(101,70,108) score 0 via ev_teach_in (learner-origin).
  Cycles 2-4 predict 108 and confirm; score reaches >= 3.
  Query compose_integ2(W,101,70): lv_setup predicts 108 rel >= 3;
  native DFS fails (MAP_X ends at 104); bracket: integ2_revise
  finds no live adapted MAP (explore retired them); fresh
  operators create a=[70,70,70,2] (extend) and t=[70,70]
  (truncate); specialize creates nothing (every candidate fact
  carries r=70, skipped by the r_alt != R[j] filter);
  integ_tag_extend records kind 1 on a. lv_dfs terminates at 108
  via a. lv_verify_chain: t2_exec returns 108 (licensing live,
  no veto); GUARD-T2 does not fire (licensing facts are
  world-channeled, field 12 = 0, so they cannot all equal the
  learner-originated prediction source); 108 == 108; promote
  MAP_Z with LINK14 to a.
  Expect: ans=108; a live with type-16 a->MAP_X, relseq
  [70,70,70,2], kind 1; MAP_Z LINK14->a; exactly 2 live adapted
  MAPs; explore FACT score >= 3.

- I2 INTEGRATE-TRUNCATE: explore 4 cycles
  integ_explore(W,11,72,op=2,retire=1) builds FACT(11,72,13)
  score >= 3 via trial [70,70] executions (11 -(70)-> 12
  -(70)-> 13). Query compose_integ2(W,11,72): predicts 13
  rel >= 3; native fails (MAP_X ends at 14); bracket: extend
  creates nothing (frontier 14 dead end); truncate creates
  t=[70,70]; specialize creates nothing: the candidate
  alternative facts (training FACT (11,71,14) via mp_run's
  ev_teach_in, explore FACTs (11,72,*) via lv_observe's
  ev_teach_in) are ALL learner-originated, so GUARD-T1's
  provenance gate admits none. (C295's unguarded run created a
  [72,70] trial here; the guard intentionally removes it. The
  arm does not depend on it.) lv_dfs: MAP_X ends 14, t ends 13;
  t terminates at 13. Verify 13 == 13; promote.
  Expect: ans=13; t type-16->MAP_X, relseq [70,70], kind 2;
  MAP_Z LINK14->t; explore FACT score >= 3.

- I6 INTEGRATE-SPECIALIZE: teach (12,2,99) after training;
  retire the training FACT (11,71,*) (harness isolation, same as
  C295 Amendment 3: it is training scaffolding, and it is
  learner-originated so GUARD-T1 would block it anyway).
  Explore 4 cycles integ_explore(W,11,74,op=3,retire=1). Each
  cycle: adapt_specialize sees only the world fact (12,2,99) at
  j=1 (v=12, r=70 -> ralt=2); the learner's prediction FACT
  (11,74,99) is learner-originated, so GUARD-T1 blocks the
  self-referential [74] substitution that C295's unguarded run
  created. Exactly one trial [70,2] per cycle: 11 -(70)-> 12
  -(2)-> 99. Executes to 99; FACT(11,74,99) score reaches >= 3.
  Query compose_integ2(W,11,74): predicts 99 rel >= 3; native
  fails; bracket creates t=[70,70] and xs=[70,2] (via the world
  fact (12,2,99)); lv_dfs tries MAP_X (14), t (13), then xs
  (99 == 99); verify; promote.
  Expect: ans=99; xs type-16->MAP_X, relseq [70,2], kind 3;
  MAP_Z LINK14->xs; explore FACT score >= 3.

- I4 INTEGRATE-WITHHOLD: Z facts as I1. NO explore phase. Query
  compose_integ2(W,101,70): lv_predict finds no FACT (101,70,*)
  and no MAP with field 4 == 70 (MAP_X has field 4 = 71),
  returns -999999. Expect: ans=-3; zero type-16 edges
  workspace-wide; live MAP count == 1 (MAP_X only); the adapt
  bracket never fires.

- I3 INTEGRATE-STALE-REVISE: setup as I1 through explore;
  q1=compose_integ2(W,101,70) -> 108 with MAP_Z LINK14->a
  (a=[70,70,70,2], kind 1, type-16->MAP_X). World change: teach
  (104,2,140), then kill (104,2,108) (teach-then-kill; learner
  not told). q2=compose_integ2(W,101,70): lv_setup predicts 108
  rel 3 (stale FACT persists); native DFS: no candidate
  terminates at 108 (a and MAP_Z re-derive to 140 via the live-
  fact contract path; MAP_X ends 104; t ends 103); bracket:
  integ2_revise finds a STALE (cc_relseq unreadable: licensing
  fact dead; the execution probe agrees: t2_exec vetoes with
  INTEG-EXEC-STALE), kind 1, rev_extend_src builds a2=
  [70,70,70,2] via the live fact (104,2,140): 101 -(70)-> 102
  -(70)-> 103 -(70)-> 104 -(2)-> 140, type-16 a2->a, retires a;
  t is intact (probe executes to 103, no veto) and untouched.
  lv_dfs: a2 ends at 140 != 108; nothing terminates. Expect:
  q1=108; q2=-2; a retired; a2 live with relseq [70,70,70,2]
  and type-16 a2->a; NO LINK14 edge targets a2 (nothing
  promoted in q2); FACT(101,70,108) score still 3 (stale
  prediction persists: structure revision and prediction
  revision are still not closed-loop; documented, not hidden).

- I5 INTEGRATE-RECOVERY (diagnostic, NOT verdict-gating):
  continue I3's workspace. Retire the stale Q1 composite MAP_Z
  (harness isolation, C295 Amendment 3: its contract fallback
  would otherwise reanimate it to terminal 140 and shadow the
  revised a2). Up to 10 explore cycles integ_explore(W,101,70,
  op=1,retire=0); stop when lv_setup returns 140 with rel >= 3.
  Then q3=compose_integ2(W,101,70). Each cycle executes the
  [70,70,70,2] trial to 140 and contradicts the stale 108 FACT,
  superseding it (C181 dynamics). Bounded claim: convergence
  within 10 cycles (exact count observed and reported).
  Expect: cycles <= 10; q3=140; MAP_Z2 LINK14->a2.

### Guard-regression arms (frozen)

- G1 (old K3 scenario: self-referential substitution): fresh
  workspace, I6 setup (train, (12,2,99), retire training FACT,
  4 explore cycles op=3 retire=1 on (11,74), query
  compose_integ2(W,11,74)). Under GUARD-T1 the learner's own
  FACTs cannot license alternative-relation substitution.
  Expect: ans=99; FACT(11,74,99) score >= 3 (convergence, not
  starved); ZERO live MAPs with relseq [71] or [74] (no
  self-referential trials; the [74] trial C295's unguarded run
  created is gone); xs=[70,2] live with type-16->MAP_X, kind 3,
  and MAP_Z LINK14->xs (no guard overreach: the world-licensed
  substitution still works and verifies).

- G2 (old K5 scenario: circular self-verification): fresh
  workspace, I3 setup through the world change. q1=108 as in
  I3. After the change, q2=compose_integ2(W,101,70). Under
  GUARD-T2/GUARD-T3 the stale prediction cannot self-verify:
  any verification graph licensed solely by the learner's own
  reified prediction is vetoed, and stale execution is refused.
  Expect: q1=108; q2=-2; a retired; a2 live, relseq
  [70,70,70,2], type-16 a2->a (the stale revision FIRES under
  the guards); total type-14 edge count unchanged across q2 and
  no LINK14 targets a2 (no circular self-verification
  promotion in q2); FACT(101,70,108) score still 3. (No
  overreach: the legitimate kind-dispatched revision is not
  blocked by the guards.)

- G3 (old I5 scenario: recovery convergence): continue G2's
  workspace. Retire the stale Q1 composite. Up to 10 explore
  cycles as in I5; then q3=compose_integ2(W,101,70).
  Expect: cycles <= 10; q3=140; MAP_Z2 LINK14->a2 (the
  consequence converges after the world change under guards).

### Routing diagnostic (frozen, NOT verdict-gating)

- S1 STALE-ROUTING-UNIT: fresh workspace. Train X; Z facts as
  I1; adapt_extend(W,101,0) + integ_tag_extend(W) creates
  a=[70,70,70,2] (type-16->MAP_X, kind 1). Then supersede the
  licensing fact: F140=ev_teach(W,104,2,140);
  link_edge(W,F108,3,F108,0) (self type-3 = superseded; F108
  stays live). Now a is exec-stale but satisfiability-intact:
  cc_relseq reads [70,70,70,2] (F108 live), cc_satisfy succeeds
  via t2_lu_first (which does not skip superseded facts),
  while t2_exec vetoes (is_superseded check) with
  INTEG-EXEC-STALE.
  Expect: t2_exec(a.root,101) == -999999 (veto fires);
  adapt_revise2(W,101,0) == 0 with a still live (the frozen
  predicate is blind to supersession); integ2_revise(W,101,0)
  >= 1 (the routing makes the veto visible); a2=[70,70,70,2]
  live with type-16 a2->a; a retired. This isolates the
  routing's added value: without it, the superseded-licensed
  trial is never revised.

## 4. Kill bars (frozen)

- K1: I1 all assertions pass.
- K2: I2 all assertions pass.
- K3: I6 all assertions pass.
- K4: I4 all assertions pass (-3, zero adaptation side effects).
- K5: I3 all assertions pass (q2=-2 with a2 revised and wired
  a2->a, no false accept, stale prediction documented).
- K6: G1 all assertions pass (zero self-referential trials,
  FACT convergence, no overreach).
- K7: G2 all assertions pass (stale revision fires, no
  circular promotion).
- K8: G3 all assertions pass (consequence converges).
- K9: 3/3 runs byte-identical (sha256 equal, pairwise cmp).
- K10: zero em/en dashes in all deliverables (byte-verified);
  the token `expected` appears nowhere in integ2_patch.zag
  (grep audit); 0 new machinery beyond the three guards:
  0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases, 0 new fact fields, 0 new
  header slots; integ2_patch.zag <= 150 lines.
- K11: frozen source copies sha256-identical to their origins
  (guarded copies match the red-team commits; pristine copies
  match C295); origins unmodified (git diff empty on both
  lanes); commit-order self-check passes (this prereg committed
  alone before any implementation).

Verdict COMPOSITION-INTEGRATION-COMPLETE iff K1-K11 all pass.
I5 and S1 are reported as preregistered diagnostics, not gating.

## 5. Architecture accounting (frozen constraints)

Pure Zag via safebin PATH, pinned znc. No Python anywhere. New
files: integ2_patch.zag + integ2_driver.zag only. No changes to
frozen or guarded files. 0 new edge/MAP types (14/15/16 reused).
0 new opcodes. The integ2 layer reuses the frozen operators
(rev_is_adapted, rev_src, cc_relseq, cc_satisfy, ts_kind,
rev_extend_src, ts_truncate_src, ts_specialize_src, t2_exec);
it adds no cognitive subsystem. Researcher scaffold (disclosed):
pipeline order, withhold gate, kind-completion tagging,
explore/exploit split, the stale-sentinel routing design above.
Learner-owned: predictions, reliability values, which
adaptations are created, verification outcomes (including veto
outcomes), all wiring endpoints.

## 6. Known boundaries (not flaws in the claim)

- Single-segment compositions only; type-15 co-use promotion
  path is present but no arm exercises a 2+ segment composition.
- Toy scale; mechanism integration with frozen bars, not a
  generality or SURVIVES claim.
- REBIND is excluded by signature (as in C295); a
  learner-verified rebind variant remains future work.
- I5/G3 exact convergence ticks are observed, not hand-derived;
  the bound (<= 10) is what is preregistered.
- The stale-prediction open loop (I3/G2 q2=-2 with the
  prediction still at score 3) is documented, not fixed; fixing
  it is future work (counterexample-driven prediction update).
- The guards live only in this lane's copies; promoting them to
  the frozen base needs Micah's ruling.
