# PREREG: INTEGRATION-COMBINED (self-trigger + plan-invalidation hook + B1/B2 contracts)

Date: 2026-10-03. Worker: INTEGRATION-COMBINED (follow-up to
INTEGRATION-SELFTRIG). Non-ledger task (claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/integration_combined/`
File prefix `cb_`.

## 1. Parent question

Can the three mechanisms (a) self-triggered revision in the
live query path (INTEGRATION-SELFTRIG, K1-K10 PASS), (b) the
plan-invalidation hook (INTEGRATION-HOOK; motivated by the
INTEGRATION-STRESS IS-D finding that plans cache the bound fam
at build time), and (c) the integrated B1/B2 contract layer
(C455 INTEGRATION-B1B2) work together without interference?

## 2. Combined architecture design

The three mechanisms compose as follows. No redesign of any
foundation; the combination is additive.

**M1 Contracts (C455, unchanged).** B1: one binding contract
per need tag over [tag, fam] at 2000+bi*100. B2: one coverage
contract per procedure family over [rel] at 3000/3100/3200.
`cb_base/cb_world/cb_module.zag` are byte-copies of the
SELFTRIG files (cmp-verified).

**M2 Self-trigger (SELFTRIG, unchanged).** Trigger A: spec
refusal inside execute_plan fires u_invalidate on the
admitting coverage contract (judgment=1, consequence=0) and
falls back to generic. Trigger B: live oracle disagreement
with spec versions used fires one u_invalidate per
spec-routing family from do_query's retry path (max 3
attempts). Revise-on-retire: cov_induct revises (not
fresh-inducts) a committed-but-fully-retired contract under
the latched request 901.

**M3 Plan-invalidation hook (new, this lane).** Design
decision: a LAZY plan-version check in compose's plan-table
hit path, NOT an eager hook on u_revise. Rationale, frozen
before implementation:

- Every plan execution goes through compose -> plan_find, so
  a load-time check covers all staleness. An eager hook on
  u_revise adds nothing except earlier invalidation.
- u_revise is shared by B1 and B2 contracts. A coverage (B2)
  revision must NOT invalidate plans: plans cache only the
  bound fam, and coverage revision changes spec/generic
  routing (read at execute time via u_check), never fams. An
  eager hook would either over-fire (churn on every B2
  revise, including IS-C-style identical-clause restores) or
  need contract-kind discrimination wired into the revision
  path (a new cross-structure coupling).
- The lazy check is read-only toward contracts: bind_fam ->
  u_check mutates nothing (verified in the module source: no
  ss in u_check). Its only writes are the stale plan slot
  (zeroed), its own telemetry cells (L+13276..13296), and the
  HOOK line.

Hook semantics (frozen): on a plan_find hit, for each need,
compare the cached fam against live bind_fam(tag). On the
first mismatch: emit `HOOK gtag=<gt> need=<p> tag=<tag>
oldfam=<cached> newfam=<live>`, zero the plan slot, bump
L+13276, stash fields at L+13280..13296, and take the miss
path (learn_bindings -> topo -> plan_new -> execute_plan).
do_query emits the HOOK line when it observes L+13276
increase across its compose call (compose returns only the
st code; the cursor cannot thread through it).

**Why the three do not interfere (frozen analysis):**

- I-1: B2 self-trigger cycles can never trip the hook. The
  hook keys on bind_fam (B1) mismatch; coverage revision
  changes routing, not fams. Tested by K2 (zero HOOK lines
  across the entire SELFTRIG battery rerun).
- I-2: The hook cannot perturb contract state. Its contract
  reads are read-only; its writes touch only the plan table
  and its own cells. The 901 latch, disconfirmation counts,
  clause activity, and revision counts are untouched by the
  hook. Tested by K8 (coverage dc cells frozen 0,0,0 after
  the B1 revision stage).
- I-3: Self-triggered B2 revision needs no plan handling.
  Retirement changes version selection at execute time under
  the same cached plan (SELFTRIG S10D attempt 3 loads the
  pre-drift plan and routes generic). Preserved by K2.
- I-4 (IDENTIFIED, bounded, disclosed): Trigger B cannot
  attribute a joint-answer disagreement to binding vs
  coverage causes. A wrong binding that routes to a spec
  version and disagrees would make trigger B invalidate an
  innocent coverage contract (2 spurious disconfirmations,
  then retirement, generic fallback, and re-induction of the
  identical clause: bounded, self-healing, but real
  cross-mechanism noise). The hook neither causes nor
  worsens this (it fires only on plan-vs-binding divergence
  after a B1 revision). Follow-up, not tested here:
  attribute before invalidating (trial-check the binding).
- I-5: The 901 revision latch is global across B1/B2.
  Sequencing prevents cross-consumption: S11 asserts the
  latch is clear (zero_counters) before staging B1
  counterevidence, and u_revise clears it after. Pre-existing
  property, not introduced here.
- I-6: At most one hook fire per binding change; after the
  rebuild cached==live, so retries load. No double-build.
  Tested by K6/K8 (exactly one HOOK line; plans_built=4).

Synergy (design argument, not separately tested): after a
B1 revision the hook guarantees the stale plan never
executes, so subsequent live disagreements are attributable
to coverage/world drift rather than a stale cache; the hook
protects the self-trigger's attribution in the
post-revision regime.

## 3. Battery

Act 1 (non-interference): S1A-S10F rerun verbatim on the
combined binary. The hook is present but must be dormant:
every line byte-identical to SELFTRIG's st_run1.txt.

Act 2 (hook guarantee + B1/B2 coexistence): S11A-S11D on
the post-S10F L2/S2 state (world stays A2; no world switch):
- S11A COLLISION-SETUP: zero_counters(S2) (re-arms globals,
  C_Q=500); tagC=801 from the tag directory (runtime);
  relC/subjC/objC from live vocab/fact scans on A2
  (runtime); gtD = g_tag(mk_goal813_E0)+5 = 818 (runtime
  tag arithmetic, as IS-D).
- S11B STALE-QUERY: one VERIFY-shaped need (nf=4,
  [1,subjC,relC,objC]) with tag 801 (bound to RETRIEVE)
  through the LIVE do_query (okind=3, oracle_1vfy ported
  from IS-D). The stale binding misroutes end-to-end.
- S11C BIND-REVISE: staged counterevidence exactly as
  IS-D (real try_family trials -> 3x u_invalidate on
  cb0=2000 -> fresh table from trial outcomes ->
  u_revise). C_Q re-armed to 500 after QD0's live tick
  (apparatus, disclosed) so the frozen first=500 matches
  IS-D exactly.
- S11D HOOK-RECOVERY: live do_query on the rebuilt goal.
  NO clear_plans anywhere in the S11 path (audit): the
  hook must detect the stale plan (cached fam 0 vs live
  fam 1), invalidate it, rebuild, and agree.

## 4. Frozen predictions

Act 1: lines 1-87 of cb_run1.txt byte-identical to
st_run1.txt lines 1-87 (covers S1A through SUMMARY-DRIFT).
Zero HOOK lines in those 87 lines.

Act 2 (exact; all values hand-derived in section 6):

```
STAGE S11A COLLISION-SETUP
STAGE S11B STALE-QUERY
Q id=QD0 goal=818 st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56
STAGE S11C BIND-REVISE
ISD-REV tag=801 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1 nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0
ISD-CNT total=3 correct=0 revcount=1 first=500 olderr=2 fiterr=0
STAGE S11D HOOK-RECOVERY
HOOK gtag=818 need=0 tag=801 oldfam=0 newfam=1
Q id=QD1 goal=818 st=2 vers=3 ans=2:1,1 agree=1 cs=16 cg=56
SUMMARY-COLLISION agree=7 plans_built=4 plans_loaded=6 trials=9 declines=0 cs=984 cg=2464 hook=1 covdc=0,0,0
```

## 5. Kill bars

- K1 CONTRACTS: cb_run1.txt lines 1-56 byte-identical to
  st_run1.txt lines 1-56 (S1A-S9 intact).
- K2 SELF-TRIGGER: cb_run1.txt lines 57-87 byte-identical
  to st_run1.txt lines 57-87 (S10A-SUMMARY-DRIFT intact,
  including all RETRY/REVISE lines).
- K3 HOOK DORMANCY: zero HOOK lines in lines 1-87.
- K4 STALE MISROUTE: the QD0 line exactly as frozen
  (single attempt: vers=0, so trigger B does not fire).
- K5 B1 REVISION: the ISD-REV line exactly as frozen.
- K6 REVISION ACCOUNTING: the ISD-CNT line exactly as
  frozen.
- K7 HOOK FIRES: exactly one HOOK line in the whole run,
  with the frozen fields.
- K8 HOOK RECOVERY: the QD1 line exactly as frozen
  (st=2: rebuilt by the hook; agree=1).
- K9 COMBINED SUMMARY: the SUMMARY-COLLISION line exactly
  as frozen (hook=1; covdc=0,0,0: the B1 revision left
  coverage dc cells untouched).
- K10 DETERMINISM: 3/3 byte-identical runs, stderr empty.
- K11 TOOLCHAIN: safebin only, no python/python3, pure Zag,
  pinned znc 2026.07.0-dev; git via /usr/bin/git, explicit
  pathspecs, local only, never pushed.
- K12 HYGIENE: zero em/en dash bytes in lane docs and
  sources; word-boundary grep over the 17 world-literal
  identifiers empty in cb_learn.zag and cb_main.zag.
- K13 WIRING AUDIT: no clear_plans call in the S11 path;
  u_invalidate appears only at the four execute_plan
  refusal sites, the three note_answer_disagree sites, the
  six S9 demo sites, and the three S11C probe sites;
  u_revise only in cov_induct's retire rule, the two S9
  demo sites, and the one S11C site; the hook's
  bind_fam/u_check calls are the only contract reads in
  compose.

## 6. Derivation notes (why the frozen Act 2 lines are exact)

- QD0: plan miss (goal 818 new) -> bind_fam(801)=0 (stale
  S10A clause (1,0,0,0)) -> plan caches fam 0. Execute
  fam==0 branch: rel=1 (need field 0), obj=subjC;
  ret_version(1)=0 (1 outside [601,602]) -> ret_gen scans
  all 56 A2 facts, none with rel 1 -> OUTS rec [0] ->
  ans=[1,0] -> ans=1:0. cs=56. Oracle_1vfy: chain
  (subjC,603,objC) = A2's first 603-fact (runtime-derived)
  -> vfy_gen 1 step x 56 facts -> [2,1,1], cg=56.
  Disagree; vers=[0] -> trigger B does not fire ->
  single line. st=2 (built).
- ISD-REV: trials are shape-determined: nf=4 -> fam0
  refuses (needs nf=2), fam1 accepts (nf==1+1*3), fam2
  refuses (needs nf=3): (0,1,0). Three u_invalidate(1,0):
  dc 0->1->2 (retire at 2), active 1->0, 900 0->1->2->3
  latches 901, 908 stamps C_Q=500 (re-armed). Fresh table:
  accept (801,1); rejects (801,0),(801,2). u_revise:
  olderr=2 (old clause (1,0,0,0) errs on the accept and on
  reject (801,0)); u_induct single-clause search: field 0
  invalid (tag 801 in all rows), field 1 identity valid
  with width 0, lexicographically first -> clause
  (1,0,1,1); revcount 904: 0->1 (zeroed); route checks
  1,0,0. All world-independent.
- ISD-CNT: 916=3 (three probes, all ok=0), 912=0, 904=1,
  908=500, 924=2, 920=0 (new clause fits the table).
- HOOK: QD1 compose: plan_find(818) hits slot 2; need 0:
  cached fam 0 vs bind_fam(801)=1 (new clause (1,0,1,1))
  -> mismatch -> HOOK line, slot zeroed, L+13276=1,
  miss path -> learn_bindings (committed, no trials) ->
  plan_new caches fam 1 -> execute.
- QD1: fam==1 branch: vfy_version: 603 in [601,603]
  (S10E vfy clause (0,0,601,603)) -> 3. vfy_spec scans
  the 603-bucket (16 A2 entries; multiset identical to
  world A) -> chain hit -> vv=1 -> OUTS rec [1,1] ->
  ans=[2,1,1]. cs=16. Oracle agrees -> agree=1, cg=56.
  st=2 (rebuilt). Single attempt.
- SUMMARY-COLLISION: agree 6+0+1=7; plans_built 2+1+1=4;
  plans_loaded 6+0+0=6; trials 9 (no uncommitted
  bindings; staged trials bypass learn_bindings);
  declines 0; cs 912+56+16=984; cg 2352+56+56=2464;
  hook=1; covdc reads 3010/3110/3210, all 0 (S11C
  invalidates targeted cb0=2000 only).

## 7. Falsification criteria (any one fails the lane)

- F1: any cb_run1.txt line 1-87 differs from st_run1.txt.
- F2: any HOOK line in lines 1-87, or total HOOK count != 1.
- F3: any S11 line differs from the frozen block.
- F4: QD1 st != 2 or agree != 1.
- F5: clear_plans appears anywhere in the S11 code path.
- F6: covdc != 0,0,0 (B1 revision leaked into B2 state).

## 8. Build and run plan (post prereg)

Files (prefix `cb_`), pure Zag, safebin only:
- `cb_base.zag`: byte-copy of st_base.zag (cmp-verified).
- `cb_world.zag`: byte-copy of st_world.zag (cmp-verified).
- `cb_module.zag`: byte-copy of st_module.zag
  (cmp-verified).
- `cb_learn.zag`: st_learn.zag + first_subj (generic port
  from is_learn.zag) + the hook validation in compose's
  hit path (+ hook telemetry cells at L+13276..13296).
- `cb_main.zag`: st_main.zag + oracle_1ret/oracle_1vfy +
  zero_counters (ports from is_main.zag) + okind 2/3 in
  do_query + HOOK-line emit on L+13276 increase + S11A-S11D
  + SUMMARY-COLLISION.
- `cb_build.sh`: assemble (cat base/world/module/learn/
  main), compile with the pinned znc, run 3x, sha256.
- Verify: cmp of copies; diff lines 1-87 vs st_run1.txt;
  frozen S11 block; 3/3 sha256 identical; stderr empty;
  grep audits (clear_plans absent in S11 path;
  u_invalidate/u_revise sites; 17 identifiers absent in
  cb_learn/cb_main; no em/en dash bytes).
- Write REPORT.md.

Commits (explicit pathspecs, /usr/bin/git, local only,
never pushed): (1) this prereg + NAMECHECK.md alone;
(2) implementation; (3) build artifacts + runs;
(4) REPORT.md.
