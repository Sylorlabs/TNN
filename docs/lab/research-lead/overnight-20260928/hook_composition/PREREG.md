# PREREG: HOOK-COMPOSITION (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/hook_composition/`, file
prefix `hc_`. Branch `tnn-native-lab`, commits local only, never pushed.

## 1. Task

Merge the generalized hook from INTEGRATION-HOOK-GENERALIZE
(multi-need interior invalidation, lazy-suffices, coverage needs no
hook, retirement decline=1) into the INTEGRATION-COMBINED binary
(self-triggered revision M1 + B1/B2 contracts M2 + plan-invalidation
hook M3). Additive only: build on both predecessors, redesign nothing.

## 2. Design answers (frozen before implementation)

**Q1: What breaks when you add multi-need support to the combined
binary?** Five findings, all verified by source inspection before
this prereg:

(a) The hook loop itself does NOT break. The combined binary's inline
hook already scans every plan position (`while(hp<nn2)`) and records
the first stale need; it is functionally identical to hook_gen's
`plan_stale_need`/`plan_invalidate` (bind_fam is read-only, so the
continued scan after the first stale hit has no side effects). It was
however NEVER exercised with nn>1 in the combined binary (S11 used a
1-need goal). Act 3 is its first multi-need exercise.

(b) Telemetry cell collision. hook_gen's fire counter lives at
L+13288; the combined binary's hook tag lives at L+13288. A blind
merge collides. Resolution (frozen): keep the COMBINED layout
(L+13276 fire count; L+13280..13296 gtag, need, tag, oldfam, newfam)
and translate hook_gen's IHH-INV lines into the combined HOOK line
format. Act 1/2 regression depends on the combined layout.

(c) Plan-table capacity. The table has 4 slots. Post-S11 it holds
813, 808, 818. Act 3 needs 820 and 821: 5 distinct goals > 4 slots.
Without intervention plan_new returns -1 and execute_plan reads out
of bounds. Resolution (frozen, disclosed apparatus): ONE clear_plans
at S12A setup. Growing the table would be an unprincipled
benchmark-specific patch; the 4-slot cap is recorded as a follow-up
(eviction policy experiment), not patched here.

(d) Binding directory capacity. 8 slots; post-S11 holds 801, 802,
807, 811; Act 3 needs 803, 804, 805, 806: exactly 8, zero headroom.
Resolution (frozen, disclosed apparatus): clear_bindings at S12A.
Stale clause bodies are fully overwritten by u_induct/u_write_clause
(active=1, dc=0 reset) on slot reuse, so predictions are unaffected.

(e) World state. S10C drifted the world to A2. Resolution (frozen,
disclosed apparatus): S12A re-runs setup_worldA, which is
byte-identical in both lanes and starts with set32(A,0,0) (full
reset), restoring world A exactly.

**Q2: Does the retirement finding (decline=1) interact with
self-trigger?** No, by construction of do_query: on compose st==0 it
prints `decline=1` and returns BEFORE the oracle/agree/trigger-B
logic. The hook fires first (newfam=-1), then the miss path declines
via learn_bindings' abstention path, which calls no u_invalidate, so
S+900/901 are untouched and no RETRY line is emitted. Kill bar HK-G3
proves it: decline=1 with zero RETRY lines anywhere in Act 3. Known
caveat (not triggered here, recorded as follow-up): if a future
change made decline retry, trigger-B would misattribute a
binding-retirement cause to coverage contracts (extends the disclosed
I-4 attribution gap).

**Mechanism delta: none.** The generalized hook mechanism is already
latent in the combined binary; hook_gen's three findings (lazy
suffices, multi-need interior handled, coverage needs no hook) are
architectural properties that transfer without code change. The merge
work is the integration BATTERY (Act 3, stages S12A-S12J) porting
hook_gen's G1/G2/G3 scenarios into the combined binary. The only
learn-file-adjacent change is one additive branch in do_query
(`okind==4` dispatches the ported oracle_rvr); Act 1/2 use okind
0-3, so the regression is untouched.

## 3. Implementation (additive deltas over cb_*, frozen)

- hc_base.zag, hc_module.zag, hc_world.zag: byte-copies of cb_*.
- hc_learn.zag: byte-copy of cb_learn.zag (hook loop unchanged).
- hc_main.zag: cb_main.zag plus (1) `if(okind==4){ oracle_rvr(...); }`
  in do_query; (2) ported from gen_main.zag, verbatim logic:
  oracle_rvr, mk_g1need, mk_gchain, mk_g1, tag_cb,
  stage_g1_prebind, stage_g1_revision, stage_g2_covrev,
  stage_g3_retire, stage_g3_restore; (3) Act 3 stages S12A-S12J before
  o_flush. NOFIRE lines read L2+13276 (combined layout), named
  S12-NOFIRE.
- S12A HOOKGEN-SETUP (disclosed apparatus, in order): read tagC from
  the live binding directory (pre-clear, runtime-derived, no
  literals); setup_worldA(A); re-specialize ret/vfy/cnt on the
  restored world A (specialize_ret/vfy/cnt; the L-state spec indexes
  are world-relative and S10E built them on A2; no new episodes, rel
  logs intact; amendment N1); clear_plans(L2); clear_bindings(L2,S2);
  zero_counters(S2); zero L2+13276..13296 (hook telemetry re-arm, per
  the S11A precedent); derive t1..t4 = tagC+2..+5, rels/objs from
  vocab_scan/first_obj/first_subj, gtG1/gtG2 = 813+7/+8, build G1/G2.
- hc_build.sh: assemble hc_full.zag from the five parts, compile with
  the pinned znc. Pure shell + znc.

## 4. Frozen expected output

### 4a. Regression (must hold exactly)

- Lines 1-87 of hc_run1.txt byte-identical to cb_run1.txt lines 1-87
  (Act 1: self-trigger + B1/B2, hook dormant).
- Lines 88-97 byte-identical to cb_run1.txt lines 88-97 (S11: the
  single-need hook collision, exactly one HOOK line).

### 4b. Act 3 (frozen; translated from hook_gen's G-stages into the
combined HOOK format; HOOK lines are emitted by do_query BEFORE the
Q line, unlike hook_gen's trailing IHH-INV)

```
STAGE S12A HOOKGEN-SETUP
S12-RESET clear_plans=1 clear_bindings=1 world=A
STAGE S12B G1-PREBIND
G1-PREBIND tag=804 fam=0
STAGE S12C G1-BUILD
Q id=G1Q0 goal=820 st=2 vers=0,0,0 ans=5:1,631,0,1,611 agree=0 cs=168 cg=224
STAGE S12D G1-REVISION
G1-REV tag=804 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1 nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0
STAGE S12E G2-BUILD
Q id=G2Q0 goal=821 st=2 vers=2 ans=2:1,611 agree=1 cs=16 cg=56
STAGE S12F G2-COVREV
G2-COVREV dc=2 active=0 req=1 olderr=1 revcount=1 route601=0 route602=1
STAGE S12G G2-QUERY
Q id=G2Q1 goal=821 st=1 vers=0 ans=2:1,611 agree=1 cs=56 cg=56
S12-NOFIRE hook=0
STAGE S12H G1-DELAYED
HOOK gtag=820 need=1 tag=804 oldfam=0 newfam=1
Q id=G1Q1 goal=820 st=2 vers=0,1,0 ans=6:1,631,1,1,1,611 agree=1 cs=224 cg=224
Q id=G1Q1R goal=820 st=1 vers=0,1,0 ans=6:1,631,1,1,1,611 agree=1 cs=224 cg=224
S12-NOFIRE hook=1
STAGE S12I G3-RETIRE
G3-RET tag=806 dc=2 active=0 req=0
Q id=G1Q1R2 goal=820 st=1 vers=0,1,0 ans=6:1,631,1,1,1,611 agree=1 cs=224 cg=224
HOOK gtag=821 need=0 tag=806 oldfam=0 newfam=-1
Q id=G2Q1R goal=821 decline=1
STAGE S12J G3-RESTORE
G3-REV tag=806 dc=0 active=1 req=1 olderr=0 revcount=1 route0=1 route1=0 route2=0
Q id=G2Q2 goal=821 st=2 vers=0 ans=2:1,611 agree=1 cs=56 cg=56
PLAN goal=820 n=3 [2:805:0] [1:804:1] [0:803:0]
PLAN goal=821 n=1 [0:806:0]
SUMMARY-HOOKGEN agree=13 plans_built=8 plans_loaded=9 trials=21 declines=1 cs=1952 cg=3528 hook=2 covdc=2,0,0
```

Prediction basis (frozen): setup_worldA is byte-identical across
lanes, so rels/objs/tags/goals derive identically
(601/602/603/607, tags 803-806, goals 820/821). Coverage-contract
state at Act 3 (post-S10E: RET admits {601,602}) yields the same
version vectors as hook_gen's induct state (RET {601,602}):
G1 vers=0,0,0; G2Q0 vers=2; G2Q1/G2Q2 vers=0. u_invalidate's dc
saturates at 2 on retirement regardless of starting dc, so G1-REV
and G2-COVREV reproduce exactly; olderr follows from the admit sets
({804->0} on the flipped table = 2; old RET {601,602} on the
602-only table = 1; retired 806 clause body intact for u_check_all
= 0). G2Q1R's decline path calls no u_invalidate, so S+900 stays 2
through G3-RESTORE and req latches to 1 there. Cumulative counters:
trials 9+12=21 (learn_bindings only: 3+6+3); declines 0+1=1; agree
7+6=13 (G1Q0 disagree, G2Q1R no accumulation); cs 984+968=1952; cg
2464+1064=3528; hook re-armed to 0 at S12A, fires at G1Q1 and
G2Q1R = 2; covdc 2,0,0 (3000 retired by G2-COVREV).

## 5. Kill bars (all must be green; each discriminates)

- HK-R1 (Act 1 regression): hc_run1.txt lines 1-87 byte-identical to
  cb_run1.txt lines 1-87. Fails if M1/M2 or hook dormancy regressed.
- HK-R2 (S11 regression): lines 88-97 byte-identical to cb_run1.txt.
  Fails if the 1-need hook path changed.
- HK-G1 (multi-need interior): exactly one line
  `HOOK gtag=820 need=1 tag=804 oldfam=0 newfam=1`, and the following
  G1Q1 line has st=2 agree=1. Fails if the inline hook loop
  mishandles nn=3 or misses interior positions.
- HK-G2 (coverage needs no hook): `S12-NOFIRE hook=0` after G2Q1, and
  grep -c `^HOOK` over the whole run == 3 (S11, G1Q1, G2Q1R only).
  Fails if a coverage-contract revision trips the hook.
- HK-G3 (retirement x self-trigger): the G2Q1R block is exactly
  `HOOK gtag=821 need=0 tag=806 oldfam=0 newfam=-1` followed by
  `Q id=G2Q1R goal=821 decline=1`, and grep -c `^RETRY` over lines
  98+ == 0. Fails if decline triggers (or corrupts) self-trigger.
- HK-G4 (restore): G2Q2 line has st=2 agree=1; final PLAN dump is
  exactly the two frozen lines. Fails if retirement is sticky.
- HK-G5 (lazy, no eager sweep): the only clear_plans call sites in
  hc_main.zag are S8's pre-existing one and S12A's disclosed one;
  the S12B-S12J path contains no clear_plans call. Fails if an eager
  sweep is added.
- HK-G6 (determinism): 3/3 runs byte-identical, stderr empty, exit 0.
- HK-G7 (toolchain): Step 0 guard clean; prereg+namecheck committed
  alone before any implementation commit; pure Zag.
- HK-G8 (hygiene): zero em/en dash bytes in lane sources, build
  script, docs; no world literals in new code (all values
  runtime-derived).

## 6. Falsification probes

- F1: hook loop mis-scan for nn=3 (caught by HK-G1's exact need=1).
- F2: trigger-B firing on G1Q0's agree=0 (specused==0 guard; caught
  by HK-G3's zero-RETRY grep over Act 3).
- F3: G2-COVREV olderr divergence from the S10E clause form (caught
  by the frozen G2-COVREV line).
- F4: plan_new -1 path (5th concurrent goal) is NOT exercised: the
  disclosed S12A clear_plans keeps the table at <=2 rows. Deliberate;
  the capacity limit is a recorded follow-up, not a crash test.

## 7. Build/run protocol

Assemble hc_full.zag, compile with the pinned znc, run 3x to
hc_run1/2/3.txt with empty stderr logs. Verify HK-R1..HK-G8.
Then write REPORT.md. Commits: prereg (alone, this commit),
implementation, artifacts, report. All local, never pushed,
explicit pathspecs.

## 8. Amendment N1 (committed alone before the corrected build)

Cause: the first build's Act 3 run broke the frozen G2Q0 line. G2Q0
did not agree first-try; instead trigger-B fired twice (RETRY att=1,
att=2), retired the RET coverage contract, and the query agreed on
generic fallback. Root cause: a design miss in the S12A apparatus,
not a mechanism failure. The L-state spec-procedure indexes
(ret/vfy/cnt fact indexes at L+68/L+132 etc.) are WORLD-RELATIVE:
they store fact indices into the live world. S10E re-specialized
them on the drifted world A2 (specialize_ret/vfy/cnt at cb_main
1078/1086/1094). S12A restored world A WITHOUT re-specializing, so
ret_spec read A2 fact positions against world-A facts and returned 0
subjects for (601,621); the S-contract still routed 601 to spec
(vers=2), hence the disagreement. Notably, self-trigger handled the
stale index exactly as designed: two bounded retries, coverage
contract retired, generic fallback, agree.

Correction (frozen): S12A now re-specializes on the restored world
A (specialize_ret/vfy/cnt on L2/S2, no new episodes; the rel logs
are intact and deduped), following the S10E precedent
("re-specialize after a world change"). At S12A all three coverage
contracts are active, so cov_induct takes the u_induct path (fresh
induct, no revcount bump, no req latch); admit sets are unchanged
(RET {601,602}, VFY {601,602,603}, CNT {601,602,603}), so all
section-4 predictions stand UNCHANGED, including G2-COVREV's
olderr=1 (dc saturates at 2 from the re-inducted dc=0) and the
SUMMARY-HOOKGEN counts. The broken run's artifacts are discarded
(run files overwritten by the corrected runs); the observed RETRY
sequence is recorded here as evidence, not adopted.

Kill bars HK-R1..HK-G8 are unchanged. F4 is extended: the stale
spec-index episode is recorded as a real integration finding
(world-relative learner indexes must be re-specialized after a
world restore), with the trigger-B recovery as the safety net.
