# PREREG: INTEGRATION-HOOK-GENERALIZE

Date: 2026-10-03. Worker: INTEGRATION-HOOK-GENERALIZE.
Lane: `docs/lab/research-lead/overnight-20260928/integration_hook_gen/`
Follows up on INTEGRATION-HOOK (HOOK WORKS, K1-K6 PASS).

## Background

INTEGRATION-HOOK demonstrated a general plan-version check inside
`compose` that subsumes the manual `clear_plans` for the binding layer:
before a cached plan loads, every cached (tag, fam) pair is re-checked
against the live binding contract, and any mismatch invalidates only
that plan row. Its report lists three open limitations, which this
experiment closes:

1. Multi-need stale-interior-need untested. The hook scans needs in
   plan order and reports the first stale need, but only single-need
   staleness was exercised.
2. Coverage-contract staleness untested. The hook checks the binding
   contract only. Coverage contracts drive per-need version selection
   live at execute time, so the predicted behavior is that the hook
   correctly stays silent on coverage revision while execution adapts.
   This must be demonstrated, not asserted.
3. Eager vs lazy undecided. The hook is lazy (query-time). The report
   asks whether an eager revise-time sweep is needed. Decisive tests:
   (a) a stale row sitting unloaded across intervening stages must be
   harmless and caught at load; (b) retirement-without-revision
   (bind_fam abstains, returns -1) must be handled, which a revise-time
   eager hook cannot cover because u_revise never runs there.

## Hypothesis

The lazy plan-version check generalizes without redesign: it detects a
stale interior need of a multi-need plan (need-indexed, targeted); it
correctly discriminates binding-contract staleness (fires) from
coverage-contract staleness (silent, execution self-corrects through
live version selection); and lazy strictly dominates eager because the
check precedes every plan load (compose is the sole plan_find /
execute_plan caller, grep-verified) while also covering
retirement-without-revision, which no revise-time hook can see.

## Design (frozen before implementation)

Build on INTEGRATION-HOOK, not a redesign:

- `gen_base.zag`, `gen_world.zag`, `gen_module.zag`: byte-copies of
  INTEGRATION-HOOK's `ih_base.zag`, `ih_world.zag`, `ih_module.zag`
  (cmp-verified). `u_revise` untouched. No eager sweep added.
- `gen_learn.zag`: byte-copy of `ih_learn.zag` plus ONE evidence
  extension: `plan_invalidate` records the stale need index p
  (0-based, plan order) at L+13304 (verified free), alongside the
  existing [goal tag, cached fam, current fam] at
  L+13292/13296/13300. `plan_stale_need`, `compose`, and the check
  logic are UNCHANGED. Diff vs ih_learn.zag is the evidence slot plus
  comment only.
- `gen_main.zag`: extended driver. New tags and goal tags are
  runtime-derived (tagC+2/+3/+4/+5 from the live binding table,
  g_tag+7/+1); rels/objs from vocab_scan and first_subj/first_obj.
  New oracle `oracle_rvr` for the 3-need G1 goal (generic ret_gen /
  vfy_gen, plan order [2,1,0] documented; okind=4). A `tag_cb` helper
  locates a tag's clause block by scanning the binding table
  (2000+bi*100), no literals.

### Stage plan (all state carries forward; L/S persist)

1. IH-SETUP: replicate INTEGRATION-HOOK setup (world A, 12 episodes,
   3 specializes, E0 build, E0 re-query). Regression anchor.
2. IH-COLLISION: replicate demo_collision_hook (QD0, trials, 3x
   u_invalidate on tag 801's block, u_revise, QD1, QD1 re-query).
   IHH-INV line gains `need=` from the new evidence slot.
3. G1-PREBIND: build a 1-need goal (T2=804, RET shape (601,621)) and
   call learn_bindings directly (no plan row): T2 inducts to fam 0.
   Print `G1-PREBIND tag=804 fam=0`.
4. G1-BUILD: query goal 820, 3 needs, no links:
   need0 (T1=803, RET (603,620)); need1 (T2=804, chain
   [(631,607,641),(631,607,641)]); need2 (T3=805, RET (607,641)).
   topo order for link-free goals is [2,1,0], so the plan row is
   p=0:(T3,0), p=1:(T2,0), p=2:(T1,0). The chain need executes under
   the stale fam 0 pre-revision (ret_gen on rel 2: empty, safe).
5. G1-REVISION: trials on T2's chain shape (tr0=0,tr1=1,tr2=0), 3x
   u_invalidate on T2's block (2300), judgment acc=[(804,1)]
   rej=[(804,0),(804,2)], u_revise. T2 flips 0->1. The G1 row is now
   stale at interior p=1. It is NOT re-queried yet.
6. G2-BUILD: query goal 821, 1 need (T4=806, RET (601,621)). T4
   inducts to fam 0. Plan [T4:0].
7. G2-COVREV: 3x u_invalidate on the RET coverage block (3000),
   jt_load_cov acc=[602] rej=[601] (nf=1), u_revise. RET coverage now
   admits 602 only. Binding contracts untouched.
8. G2-QUERY: re-query goal 821. Predicted: hook silent (bind_fam(806)
   still 0), plan LOADS (st=1), vers drops 2->0 via live
   ret_version, answers still agree.
9. G1-DELAYED: re-query goal 820 (its row sat stale through stages
   6-8). Predicted: hook fires at interior p=1 (sp=2), rebuilds,
   agree=1. Then re-query (st=1, silent).
10. G3-RETIRE: 2x u_invalidate on T4's block (2600): dc=2, active=0,
    req=0 (pure retirement, no revision latch). Intervening re-query
    of goal 820 (st=1, silent). Then query goal 821: predicted hook
    fires with cur=-1, row invalidated, build declines (bind_fam
    abstains) instead of misrouting.
11. G3-RESTORE: 3rd u_invalidate (req latches), judgment
    acc=[(806,0)] rej=[(806,1),(806,2)], u_revise restores T4->0.
    Query goal 821: rebuilds, agree=1.
12. Final dump_plans and SUMMARY (plan loads at L+13228, stale
    invalidations at L+13288).

Why these stages answer the three questions:

- Multi-need interior: G1's stale need is p=1 of 3 (fresh p=0 and
  p=2 bracket it). `need=1` in IHH-INV proves the scan passed a fresh
  need to find the stale interior one. Targeted: no other plan row is
  touched.
- Coverage: G2-QUERY is the discrimination test. The plan cache holds
  (tag, fam); versions are recomputed from live coverage contracts in
  execute_plan. The hook firing on coverage change would be spurious;
  staying silent while vers adapts 2->0 with agree=1 proves the
  hook's predicate is exactly the plan's cached contract surface.
- Eager vs lazy: G1-DELAYED proves a stale row is harmless until
  load and caught at load (lazy airtight; compose is the only load
  path). G3-RETIRE proves lazy covers retirement-without-revision
  (cur=-1 -> clean decline), a transition no revise-time eager hook
  can observe. Cost: the check is nn plan-row scans x <=3 u_checks
  each (E0: <=12 u_checks per load) against a full plan execution;
  an eager sweep would repeat the same work speculatively at revise
  time for rows that may never load, and still miss retirement.

## Frozen predictions

Regression (adopted from INTEGRATION-HOOK P1-P7; IHH-INV format
extended with need=):

- R1: `Q id=E0 goal=813 st=2 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1 cs=96 cg=336`
- R2: E0R `st=1 agree=1`; `IHH-NOFIRE stale=0`.
- R3: `Q id=QD0 goal=818 st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56`
- R4: `ISD-REV tag=801 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1 nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0`
- R5: `IHH-INV goal=818 cached=0 cur=1 need=0 stale=1`
- R6: `Q id=QD1 goal=818 st=2 vers=3 ans=2:1,1 agree=1 cs=16 cg=56`
- R7: QD1R `st=1 agree=1`; stale counter stays 1.

New (cs=/cg= recorded, not frozen; nclause tuple on G1-REV recorded):

- N1: `G1-PREBIND tag=804 fam=0`
- N2: `Q id=G1Q0 goal=820 st=2 vers=0,0,0 ans=5:1,631,0,1,611 agree=0`
  (plan order [2,1,0]; chain need under stale fam 0 yields empty)
- N3: `G1-REV tag=804 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1 route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0`
- N4: `Q id=G2Q0 goal=821 st=2 vers=2 ans=2:1,611 agree=1`
- N5: `G2-COVREV dc=2 active=0 req=1 olderr=1 revcount=1 route601=0 route602=1`
- N6: `Q id=G2Q1 goal=821 st=1 vers=0 ans=2:1,611 agree=1`; `G2-NOFIRE stale=1`
- N7: `Q id=G1Q1 goal=820 st=2 vers=0,1,0 ans=6:1,631,1,1,1,611 agree=1`;
  `IHH-INV goal=820 cached=0 cur=1 need=1 stale=2`
- N8: G1Q1R `st=1 agree=1`; stale stays 2.
- N9: `G3-RET tag=806 dc=2 active=0 req=0`
- N10: G1Q1R2 `st=1 agree=1`; stale stays 2.
- N11: `Q id=G2Q1R goal=821 decline=1`;
  `IHH-INV goal=821 cached=0 cur=-1 need=0 stale=3`
- N12: `G3-REV tag=806 dc=0 active=1 req=1 olderr=0 revcount=1 route0=1 route1=0 route2=0`
  AMENDMENT 2026-10-03 (committed before implementation): the original
  freeze predicted dc=2 active=0, assuming dc/active were captured before
  u_revise (the ISD-REV pattern). stage_g3_restore reads them inline
  AFTER u_revise, and u_revise restores active=1, dc=0. Observed dc=0
  active=1 is the correct restored-clause state (route0=1 confirms).
  Telemetry read-timing miss in the prediction, not a mechanism or
  kill-bar failure; the driver is NOT changed to chase the prediction.
- N13: `Q id=G2Q2 goal=821 st=2 vers=0 ans=2:1,611 agree=1`

Derivation notes (no run preceded this prereg): vers values from the
coverage contracts (RET admits {601,602} until G2-COVREV, then {602};
VFY admits {601,602,603}; 607/603/rel-2 are unadmitted, so gen
procedures run and the generic oracles agree by construction).
olderr counts judgment-table rows the pre-revision clause set
misclassifies under u_check_all. ans values from world A facts
((611,603,620), (631,607,641), (611,603,630), (611,601,621)).

## Kill bars

- K1-K6 (regression): R1-R7 observed exactly (R5 in the extended
  format); 3/3 byte-identical; stderr empty; safebin/pinned znc/pure
  Zag; hook diff vs ih_learn.zag is the L+13304 slot + comment only;
  zero numeric identifiers in hook functions; zero clear_plans calls.
  FAIL (K4/K5: PROCESS-FAIL) otherwise.
- GK1 (multi-need interior): N7 observed exactly: IHH-INV with
  need=1 (sp=2, interior p=1), stale 1->2, G1Q1 st=2 agree=1.
- GK2 (no spurious fire): N2, N6, N8, N10 show no IHH-INV; every
  re-query is st=1.
- GK3 (coverage discrimination): N6 observed exactly: st=1 (loaded,
  not rebuilt), vers 2->0, agree=1, stale counter unchanged.
- GK4 (retirement): N11 observed exactly: cur=-1, decline=1 (no wrong
  answer), stale 2->3; N13 rebuilds with agree=1 after restore.
- GK5 (determinism): 3/3 byte-identical runs, sha256 recorded,
  stderr empty on all runs. PROCESS-FAIL otherwise.
- GK6 (toolchain/generality): safebin from first command, pinned
  znc, pure Zag, no python. PROCESS-FAIL on any violation.

## Falsification criteria

- F1: IHH-INV on G1Q1 missing, or need!=1 (hook did not find the
  interior need).
- F2: any IHH-INV on G1Q0, G2Q1, G1Q1R, G1Q1R2 (spurious fire).
- F3: G2Q1 shows st=2 (rebuilt) or vers!=0 or agree=0 (coverage
  mishandled).
- F4: G2Q1R shows st=1/2 with an answer instead of decline=1, or
  cur!=-1 (retirement misrouted or missed).
- F5: any R1-R7 value differs (regression broken).
- F6: runs not byte-identical, stderr non-empty, toolchain violation.

## Deliverables and commit order

1. This PREREG.md + NAMECHECK.md (Step 0), committed ALONE.
2. Implementation: gen_base/gen_world/gen_module.zag (byte-copies),
   gen_learn.zag (evidence slot), gen_main.zag (extended driver),
   gen_build.sh, gen_full.zag.
3. Artifacts: gen_bin, gen_compile.txt, gen_run1/2/3.txt (+ .err),
   sha256.
4. REPORT.md with verdict.

No em/en dashes in any lane file (byte audit). No domain language in
code or docs: fams/tags/rels are opaque integers throughout.
