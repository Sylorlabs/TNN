# PREREG: Composition Integration (H-COMPINTEG-1)

Status: PREREG-FROZEN 2026-10-02. This preregistration strictly
precedes implementation. This commit contains ONLY this PREREG.md.
No kill bar below may be weakened or reinterpreted after results.

Worker: Composition Integration Worker (subagent, 2026-10-02).
Parent mandate: integrate the separately validated pieces C278
(EXTEND/TRUNCATE/SPECIALIZE), C279 (REBIND), C280 (learner-owned
verification), C289 (learner self-wiring), C290/C291 (policy
construction/revision/transfer) and test whether they work TOGETHER
in one learner. Report where integration breaks.

## 1. Objective

Build ONE learner that, in a single query pipeline: (a) applies L2
adaptation operators (EXTEND-ONE, TRUNCATE-ONE, SPECIALIZE-ONE),
(b) verifies exclusively against its own predictions (no harness
expected answers anywhere in the integrated path), and (c) self-wires
the result (learner-written provenance and co-use edges connecting
its own knowledge). Then probe exactly where the integration breaks.

## 2. Frozen design

New file integ_patch.zag (unfrozen). Frozen read-only sources,
copied never edited: cc_base.zag, un_patch.zag (adapt's copy,
sha256 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2),
adapt_patch.zag, revise_patch.zag, ts_patch.zag, lvcomp_patch.zag.

### 2.1 compose_integ(W,s,r,masked,st): the integrated operation

Takes NO researcher expected answer. Flow:

1. lv_setup (C280): learner prediction p for (s,r) into hg(32),
   reliability into hg(36). If no basis: WITHHOLD -3. If
   reliability < 3: WITHHOLD -3. Adaptation NEVER fires when the
   learner withholds: an unreliable learner does not restructure
   its knowledge. This gating is a preregistered integration
   decision; the alternative (adapt first, verify later) is
   rejected because with no prediction there is nothing to verify
   against.
2. Native pass: lv_dfs (C280 learner-terminated DFS) over current
   MAPs. If a chain terminates at p: assemble, lv_verify_chain
   (accept iff execution equals p), promote with self-wiring.
3. Else the L2 bracket: adapt_revise2 (kind-dispatched revision,
   C278) then, only if revision created nothing, the fresh
   operators adapt_extend + adapt_truncate + adapt_specialize
   (same order as ev_query_revise2). Then lv_dfs once over the
   augmented set.
4. Assemble, verify against p, promote. Promotion writes the
   self-wiring: LINK14 from MAP_Z to every segment MAP (provenance),
   type-15 co-use edges between consecutive segments (mechanism B),
   and every adapted MAP carries type-16 adapted-from to its source
   (written by the operators). All edges are written by learner
   promotion code from learner workspace state. No researcher
   wiring exists anywhere in this path.
5. Returns ans (>=0) verified, -2 clean reject, -3 withheld.

### 2.2 KIND-COMPLETION (preregistered integration decision)

The frozen adapt_extend predates Amendment 1 kind-recording, so its
MAPs carry field 12 = -1. ts_kind then misdispatches a STALE extend
adaptation: relseq inference fails on the unreadable relseq and falls
through to kind 3 (specialize). integ_patch records kind 1 in field
12 on every extend adaptation lacking a recorded kind
(integ_tag_extend), completing the Amendment 1 convention.
Truncate/specialize already record 2/3. The latent ts_patch
misdispatch for unrecorded-kind stale MAPs is documented as an
integration finding, not silently patched in the frozen file.

### 2.3 REBIND exclusion (preregistered integration boundary)

rebind_try's signature takes a researcher expected answer and no
learner-verified rebind variant exists. It is EXCLUDED from the
integrated pipeline. This is a preregistered integration break:
an L2 operator whose verification path is researcher-supervised
cannot join a learner-verified learner. Reported as a finding.

### 2.4 Self-wiring interpretation (preregistered)

In the composition substrate, "self-wiring" (C289) is: the learner
connects its own knowledge structures via edges it writes itself:
type-16 adapted-from (adapted MAP to source), LINK14 (composite
MAP_Z to each segment MAP), type-15 co-use (between consecutive
segment MAPs at promotion). The test asserts these edges exist with
the learner-created endpoints, and that no harness code writes
edges in the integrated path.

### 2.5 Explore/exploit split (preregistered)

integ_explore(W,s,r,op,retire,masked): UNGATED experience
gathering, mirroring C280's evidence phase. Runs one adaptation
operator (1=extend, 2=truncate, 3=specialize), executes each
resulting kind-matching adapted MAP from s (t2_exec: a real world
interaction through live facts), observes each outcome with
lv_observe (the learner scores its own prior prediction), and
optionally retires the trial MAPs. It NEVER promotes MAP_Z. The
learner's only persistent gain is the FACT prediction basis and
its reliability score. The 108/13/99/140 values in the battery are
produced by the learner's own adapted executions, never handed by
the harness.

## 3. Battery (frozen)

All arms: fresh workspace (z_alloc + tnn2_init). Train X by ev_teach
(11,1,12),(12,1,13),(13,1,14) then ev_query_adapt(W,11,71,14,0)
(trial promotes MAP_X, relseq [1,1,1]). 30 distractor teaches
(subjects 5000+, relations 60-69). masked=0 throughout.

- I1 INTEGRATE-EXTEND: Z facts (101,1,102),(102,1,103),
  (103,1,104),(104,2,105),(105,2,106),(106,2,107),(107,2,108).
  Explore: 4 cycles integ_explore(W,101,70,op=1,retire=1).
  Query: compose_integ(W,101,70). Hand derivation: explore cycle 1
  creates trial [1,1,1,2], executes to 108, teaches FACT(101,70,108)
  score 0; cycles 2-4 predict 108 and confirm, score reaches 3.
  Query: lv_setup predicts 108 rel 3; native DFS fails (MAP_X ends
  at 104); bracket creates a=[1,1,1,2] (extend) and t2=[1,1]
  (truncate scaffolding); lv_dfs terminates at 108 via a (longest
  first); verify 108==108; promote MAP_Z with LINK14 to a.
  Expect: ans=108; ADAPT-CREATED n=2; live adapted a with type-16
  a->MAP_X, relseq [1,1,1,2], kind 1; MAP_Z LINK14->a; exactly 2
  live adapted MAPs.

- I2 INTEGRATE-TRUNCATE: explore 4 cycles
  integ_explore(W,11,72,op=2,retire=1). Query:
  compose_integ(W,11,72). Hand derivation: explore builds
  FACT(11,72,13) score 3 via trial [1,1] executions. Query:
  predicts 13 rel 3; native fails (MAP_X ends at 14); bracket:
  extend creates nothing (frontier 14 dead end), truncate creates
  t=[1,1], specialize nothing; lv_dfs terminates at 13 via t.
  Expect: ans=13; t type-16->MAP_X, relseq [1,1], kind 2;
  MAP_Z LINK14->t.

- I6 INTEGRATE-SPECIALIZE: teach (12,2,99) after training. Explore
  4 cycles integ_explore(W,11,74,op=3,retire=1). Query:
  compose_integ(W,11,74). Hand derivation: explore builds
  FACT(11,74,99) score 3 via trial [1,2] (link-1 substitution,
  greedy extension stops at 99). Query: predicts 99 rel 3; native
  fails; bracket creates t=[1,1] and xs=[1,2]; lv_dfs tries MAP_X
  (14), t (13), then xs (99==99); verify; promote.
  Expect: ans=99; xs type-16->MAP_X, relseq [1,2], kind 3;
  MAP_Z LINK14->xs.

- I4 INTEGRATE-WITHHOLD: Z facts as I1. NO explore phase. Query:
  compose_integ(W,101,70). Hand derivation: lv_predict finds no
  FACT (101,70,*) and no MAP with field 4 == 70, returns -999999.
  Expect: ans=-3; zero type-16 edges workspace-wide; live MAP
  count == 1 (MAP_X only); the adapt bracket never fires.

- I3 INTEGRATE-STALE-REVISE (the break probe): setup as I1 through
  explore; q1=compose_integ(W,101,70); capture a (the [1,1,1,2]
  MAP) and z1 (MAP_Z). World change: teach (104,2,140), then kill
  (104,2,105) (teach-then-kill; learner not told). q2 =
  compose_integ(W,101,70). Hand derivation: q1 answers 108 with
  MAP_Z LINK14->a. After the change, a is stale (licensing dead,
  cc_relseq -1) while X is intact. q2: lv_setup predicts 108 rel 3
  (FACT(101,70,108) score 3 persists); native DFS: a unreadable
  via cc path (contract fallback may list it ending at 140, never
  at 108), MAP_X ends 104, MAP_Z stale; adapt_revise2: a STALE,
  kind 1 (recorded), rev_extend_src builds a2=[1,1,1,2] via
  (104,2,140) with type-16 a2->a, retires a; lv_dfs: a2 ends at 140
  != 108, nothing terminates at 108. Expect: q1=108; q2=-2; a
  retired (not a live MAP); a2 live with relseq [1,1,1,2] and
  type-16 a2->a; NO LINK14 edge targets a2 (nothing promoted in
  q2); FACT(101,70,108) pred_score still 3 (stale prediction
  persists: the pipeline revises structure but has no
  prediction-revision path on query failure). This arm is the
  preregistered integration breakdown: structure revision and
  learner verification do not close the loop.

- I5 INTEGRATE-RECOVERY (diagnostic, NOT verdict-gating): continue
  I3's workspace. Up to 10 explore cycles integ_explore(W,101,70,
  op=1, retire=0); after each, lv_setup must return 140 with
  rel>=3 to stop. Then q3=compose_integ(W,101,70). Qualitative
  derivation: each cycle predicts 108 from a stale FACT,
  contradicts it by executing a2 to 140, supersedes one stale
  FACT (self type-3 edge) and teaches a 140 FACT; once the 140
  FACT leads, its score climbs to 3. Bounded claim: convergence
  within 10 cycles (exact count observed and reported, depends on
  bid tie-break internals). Expect: cycles<=10; q3=140; MAP_Z2
  LINK14->a2.

## 4. Kill bars (frozen)

- K1: I1 all assertions pass.
- K2: I2 all assertions pass.
- K3: I6 all assertions pass.
- K4: I4 all assertions pass (-3, zero adaptation side effects).
- K5: I3 all assertions pass (q2=-2 with a2 revised and wired
  a2->a, no false accept, stale prediction documented).
- K6: 3/3 runs byte-identical (sha256 equal, pairwise cmp).
- K7: zero em/en dashes in all deliverables (byte-verified); the
  token `expected` appears nowhere in integ_patch.zag (grep audit);
  0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- K8: frozen source copies sha256-identical to their origins;
  origins unmodified.

Verdict COMPOSITION-INTEGRATION-COMPLETE iff K1-K8 all pass.
I5 is reported as a preregistered diagnostic, not gating.

## 5. Architecture accounting (frozen constraints)

Pure Zag via safebin PATH, pinned znc. No Python anywhere. New file:
integ_patch.zag + integ_driver.zag only. No changes to frozen
files. 0 new edge/MAP types (16/14/15 reused). 0 new opcodes.
Cognition lines: counted for integ_patch.zag at report time.
Researcher scaffold (disclosed): the compose_integ pipeline order,
withhold gate, kind-completion tagging, explore/exploit split,
KIND/REBIND boundary decisions. Learner-owned: predictions,
reliability values, which adaptations are created, verification
outcomes, all wiring endpoints.

## 6. Known boundaries (not flaws in the claim)

- Single-segment compositions only; type-15 co-use promotion path
  is present but no arm exercises a 2+ segment composition.
- Toy scale; mechanism integration with frozen bars, not a
  generality or SURVIVES claim.
- REBIND is excluded by signature (section 2.3); a learner-verified
  rebind variant is future work.
- I5's exact convergence tick is observed, not hand-derived.
