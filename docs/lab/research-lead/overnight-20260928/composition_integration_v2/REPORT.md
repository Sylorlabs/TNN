# REPORT: H-COMPINTEG-2 (Composition Integration Retry)

Status: VERDICT RUN COMPLETE 2026-10-02.
Verdict: COMPOSITION-INTEGRATION-COMPLETE (K1-K11 all PASS).

Worker: Composition Integration v2 (resumed parked task).
Frozen prereg: commit 2bb9cf9be (PREREG.md + NAMECHECK.md Step 0 only).
Frozen amendment: commit e6595aa89 (PREREG_AMENDMENT1.md, query-relation 79 fix).
Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1.
Pure Zag via safebin PATH; no forbidden executable invoked (Step 0 guard PASS).

## 1. What this wave had to fix (from C295 INCOMPLETE)

Wave 1 (ledger C295) went COMPOSITION-INTEGRATION-INCOMPLETE on four items:

- K1 hand-derivation error: the original prereg claimed EXTEND-ONE creates a
  multi-link trial in one step; EXTEND-ONE extends by exactly one link, so the
  derived terminal 108 was unreachable by the stated construction. Fixed by
  Amendment 1 design (single-link Z-world, link-by-link arithmetic, query
  relation 79): one EXTEND-ONE step from frontier 104 via the live fact
  (104,2,108) creates exactly [70,70,70,2], i.e.
  101 -(70)-> 102 -(70)-> 103 -(70)-> 104 -(2)-> 108. Terminal 108 is
  achievable in one operator step; no multi-link leap is claimed.
- K3 self-referential FACT substitution: the unguarded run built a [74] trial
  licensed by the learner's own prediction FACT. Fixed by GUARD-T1
  (provenance gate: learner-originated facts cannot license
  alternative-relation substitution).
- K5 circular self-verification: the stale prediction could self-verify.
  Fixed by GUARD-T2 (self-license veto) + GUARD-T3 (licensing-liveness veto).
- I5 value-replay gap: recovery after a world change never closed the loop.
  Now exercised as I5/G3 with bounded convergence (<= 10 explore cycles).

Additionally the INTEG-BREAK red team (ledger C305) contributed the three
guards above plus the flagged open item: routing GUARD-T3's INTEG-EXEC-STALE
sentinel (-999999) into the adapt/revise path, which this wave implements as
the integ2 layer (integ2_patch.zag, 145/150 lines).

## 2. Per-bar verdicts

All arms use compose_integ2 (compose_integ with the bracket calling
integ2_revise instead of adapt_revise2). 30 distractor teaches per arm.
masked=0 throughout. Explore uses integ_explore (frozen).

- K1 (I1 INTEGRATE-EXTEND): PASS. Explore x4 on (101,79) op=1 builds
  FACT(101,79,108) score 3 (cycle 1: no basis, pred -999999; cycles 2-4
  confirm). Query ans=108. Fresh bracket creates a=[70,70,70,2] (extend)
  and t=[70,70] (truncate); specialize creates nothing (GUARD-T1 blocks the
  learner-originated FACT). lv_dfs terminates at 108 via a. Verify
  108 == 108 (licensing live; GUARD-T2 silent: licensing facts are
  world-channeled). Promote MAP_Z with LINK14 to a. Assertions: ans=108;
  a type-16->MAP_X, relseq [70,70,70,2], kind 1; MAP_Z LINK14->a; exactly
  2 live adapted MAPs; FACT score 3. All 5/5.
- K2 (I2 INTEGRATE-TRUNCATE): PASS. Explore x4 on (11,72) op=2 builds
  FACT(11,72,13) score 3 via [70,70] trials. Query ans=13. Bracket:
  truncate creates t=[70,70]; extend creates nothing (frontier 14 dead end);
  specialize creates nothing (all alternative candidates learner-originated,
  GUARD-T1 admits none). lv_dfs: t terminates at 13. Assertions 4/4.
- K3 (I6 INTEGRATE-SPECIALIZE): PASS. Setup teaches (12,2,99), retires the
  training FACT (11,71,*). Explore x4 on (11,74) op=3: exactly one trial
  [70,2] per cycle (11 -(70)-> 12 -(2)-> 99); the learner's prediction FACT
  is learner-originated so GUARD-T1 blocks the self-referential [74]
  substitution the unguarded C295 run created. FACT(11,74,99) score 3.
  Query ans=99 via xs=[70,2] (world fact (12,2,99) licensed). Assertions 4/4.
- K4 (I4 INTEGRATE-WITHHOLD): PASS. No explore. Query (101,79): lv_predict
  finds no FACT and no MAP with field 4 == 79; withholds -3. Zero type-16
  edges workspace-wide; live MAP count == 1 (MAP_X only). Assertions 3/3.
- K5 (I3 INTEGRATE-STALE-REVISE): PASS. q1=108 with MAP_Z LINK14->a
  (a=[70,70,70,2], kind 1, type-16->MAP_X). World change: teach (104,2,140),
  kill (104,2,108). q2: lv_setup predicts 108 rel 3 (stale FACT persists);
  native DFS finds nothing at 108; integ2_revise finds a STALE
  (satisfiability disjunct: cc_relseq unreadable, licensing fact dead;
  kind 1), rev_extend_src builds a2=[70,70,70,2] via (104,2,140) with
  type-16 a2->a, retires a; t intact and untouched. lv_dfs: a2 ends at 140.
  q2=-2. Assertions: q1=108 setup ok; q2=-2; a retired; a2 live with
  type-16 a2->a; no LINK14 targets a2; FACT(101,79,108) score still 3
  (stale prediction persists: structure revision and prediction revision
  are still not closed-loop; documented, not hidden). All 6/6.
- K6 (G1 old-K3 regression): PASS. ans=99; FACT(11,74,99) score 3
  (convergence, not starved); ZERO live MAPs with relseq [71] or [74]
  (no self-referential trials); xs=[70,2] live type-16->MAP_X kind 3 with
  MAP_Z LINK14->xs (no guard overreach: world-licensed substitution still
  works and verifies); the blocking trigger was present (prediction FACT
  learner-originated). All 5/5.
- K7 (G2 old-K5 regression): PASS. q1=108; q2=-2; a retired; a2 live,
  relseq [70,70,70,2], type-16 a2->a (stale revision FIRES under the
  guards); total type-14 edge count unchanged across q2 and no LINK14
  targets a2 (no circular self-verification promotion); FACT(101,79,108)
  score 3 (legitimate kind-dispatched revision not blocked). All 6/6.
- K8 (G3 old-I5 regression): PASS. 4 explore cycles (<= 10); q3=140;
  MAP_Z2 LINK14->a2 (consequence converges after the world change under
  guards). All 3/3.
- K9 (determinism): PASS. 3/3 runs byte-identical (pairwise cmp clean).
  sha256 = 857b59e042553ba952ad9626762a146a3fb1d5e4a805c44d0cf27f03335b94ed
  for integ2_run1.txt, integ2_run2.txt, integ2_run3.txt.
- K10 (hygiene): PASS. integ2_patch.zag = 145 lines (cap 150). Token
  `expected` appears 0 times in integ2_patch.zag. Zero em/en dashes
  (byte-verified U+2014/U+2013) in PREREG.md, PREREG_AMENDMENT1.md,
  NAMECHECK.md, integ2_patch.zag, integ2_driver.zag, integ2_build.sh,
  REPORT.md. 0 new edge/MAP types, 0 new opcodes, 0 modes, 0 bridges,
  0 handlers, 0 new semantic cases, 0 new fact fields, 0 new header slots.
  No `while.*!(` negated-conjunction loops; no `as *i32` casts in new code.
- K11 (frozen integrity): PASS. Guarded copies sha256-identical to the
  red-team commits (cc_base_g, ts_patch_g, lvcomp_patch_g); pristine copies
  sha256-identical to C295 values (un_patch, adapt_patch, revise_patch,
  integ_patch); full 64-char compares against NAMECHECK.md Step 3. Origin
  lanes integ_break_redteam and composition_integration: git diff empty.
  Commit-order self-check: 2bb9cf9be holds PREREG.md + NAMECHECK.md only;
  e6595aa89 holds PREREG_AMENDMENT1.md only; both precede every
  implementation artifact.

## 3. Diagnostics (preregistered, NOT verdict-gating)

- I5 INTEGRATE-RECOVERY: PASS. Continued I3's workspace; retired the stale
  Q1 composite; 4 explore cycles to lv_setup(101,79) = 140 rel 4 (<= 10);
  q3=140 with MAP_Z2 LINK14->a2. Exact convergence count observed: 4.
- S1 STALE-ROUTING-UNIT: PASS. Fresh workspace; adapt_extend creates
  a=[70,70,70,2]; supersede (not kill) the licensing fact F108
  (stays live). t2_exec vetoes with -999999 (s1=1). Frozen adapt_revise2
  returns 0 with a still live (s2=1: blind to supersession). integ2_revise
  returns >= 1 via the routed probe (satstale=0, execstale=1); a2 live with
  type-16 a2->a; a retired (s3=1). This isolates the routing's added value:
  without it, the superseded-licensed trial is never revised.

## 4. Implementation note: slot-recycling defect found and fixed

The parked worker's untracked implementation was consistent with the frozen
prereg (rebuilt binary byte-identical to the parked binary) but contained a
latent defect in integ2_revise_one: in the readable case it retired the
stale trial BEFORE kind-dispatch so the frozen duplicate check would pass.
alloc_node recycles dead node slots, so the new trial's own chain cells
reused the retired trial's id (debug: ng(a,36) live again as a 902 frame
node; the type-16 "revises" edge pointed at a recycled cell). In the
unreadable case the deferred retire was still recycled, by the next MAP's
execution-probe frame allocation mid-scan. Observable effect: I3/G2/S1
"a retired" assertions failed (3/3 parked runs).

Fix (integ2_patch.zag only, no prereg change): mask the trial's node type
during dispatch (the frozen duplicate checks adapt_relseq_absent and
ts_relseq_present scan live type-20 MAPs only; cc_relseq walks from
ng(W,m,20) and never reads the MAP's own field 0, so ts_specialize_src's
stale-length limit is unaffected), restore the type, and defer all
retirements past the scan loop via a transient local id list (not learner
state; no new fields or header slots). This restores the prereg's
dispatch-then-retire order, which the frozen adapt_revise documents as
required for exactly this reason.

## 5. Wave-1 defect closure summary

- K1 derivation error: closed by the frozen Amendment 1 design; every arm
  shows the link arithmetic and the runs match it exactly.
- K3 self-reference: closed by GUARD-T1; G1 shows zero self-referential
  trials with convergence intact and no overreach.
- K5 circularity: closed by GUARD-T2/GUARD-T3; G2 shows the stale revision
  firing with no circular promotion.
- I5 replay gap: closed as a bounded diagnostic; I5/G3 converge in 4
  cycles (bound 10).

## 6. Architecture accounting

Cognition lines added: integ2_patch.zag (145) + integ2_driver.zag (harness).
New hardcoded semantic cases: 0. Modes/bridges/handlers: 0. New edge/MAP
types, opcodes, fact fields, header slots: 0. Learner-owned: predictions,
reliability values, which adaptations are created, verification outcomes
(including veto outcomes), all wiring endpoints. Researcher scaffold
(disclosed): pipeline order, withhold gate, kind-completion tagging,
explore/exploit split, stale-sentinel routing design. The three guards are
experimental copies in this lane only; promotion to the frozen base needs
Micah's ruling (prereg boundary, unchanged).

## 7. Known boundaries (unchanged from prereg)

Single-segment compositions only; toy scale; REBIND excluded by signature;
I5/G3 convergence ticks observed not hand-derived; the stale-prediction open
loop (q2=-2 with prediction still at score 3) documented not fixed;
guards live only in this lane's copies.

## 8. Observation (non-gating, for the record)

In the I3 kill case the execution probe does not return INTEG-EXEC-STALE
(execstale=0 in the run log); the satisfiability disjunct carries the stale
verdict (satstale=1, cc_relseq unreadable on the killed licensing fact).
The veto fires in the S1 supersede case (execstale=1), which is the
routing's designed added value over the frozen predicate. No kill bar
depends on which disjunct fires; q2 behavior is identical either way.
