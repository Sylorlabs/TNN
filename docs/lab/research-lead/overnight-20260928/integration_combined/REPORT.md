# INTEGRATION-COMBINED REPORT (non-ledger)

**Verdict: BUILD-PASS. All 13 kill bars green, all 6 falsification
probes behaved as designed.**

The three mechanisms (self-triggered revision, the plan-invalidation
hook, the integrated B1/B2 contracts) work together with **zero
interference**: Act 1 (S1A-S10F) reruns byte-identical to
INTEGRATION-SELFTRIG with the hook fully dormant, and Act 2 (S11)
demonstrates the hook invalidating and rebuilding a stale plan in the
live query path after a B1 tag-shape collision, with no clear_plans
anywhere in the S11 path.

## What was built

Lane: `docs/lab/research-lead/overnight-20260928/integration_combined/`,
file prefix `cb_`. Pure Zag, safebin-only, pinned znc
`znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev).

**Architecture (additive over C455/C461; u_* bodies untouched,
byte-copy verified):**

- **M1 self-triggered revision** (from INTEGRATION-SELFTRIG): trigger A
  (spec refusal inside execute_plan), trigger B (learner-vs-oracle
  disagreement in the do_query retry loop, max 3 attempts). Unchanged.
- **M2 integrated B1/B2 contracts**: B1 binding contracts (bind via
  u_check, invalidate via u_invalidate, revise via u_revise); B2
  coverage contracts (induct, route via bind_fam for spec queries,
  self-trigger invalidation on disagreement). Unchanged.
- **M3 plan-invalidation hook (new)**: lazy plan-version validation in
  compose's plan-table hit path. Every cached fam is re-validated
  against the live binding contract via bind_fam (read-only:
  u_check mutates nothing) before the plan loads. On the first
  mismatch the plan slot is zeroed, telemetry is stashed at
  L+13276 (fire count), L+13280..13296 (gtag, need, tag, oldfam,
  newfam), and the miss path rebuilds. do_query emits the HOOK line
  when it observes the fire count increase across the compose call
  (compose returns only the st code, so the cursor cannot thread
  through it). The hook is read-only toward contracts and writes only
  the stale plan slot plus telemetry: it cannot perturb B1 or B2
  state (I-2). It keys on B1 fams only, so a B2 revision can never
  trip it (I-1). At most one fire per binding change (I-6): the
  first stale plan invalidates, and the rebuild writes live fams.

**Experiment (two acts in one binary):**

- **Act 1 (K1-K3):** S1A-S10F verbatim from INTEGRATION-SELFTRIG,
  including the post-drift B2 revision and S10 recovery. No B1
  revision occurs in S1-S10, so the hook must be dormant.
- **Act 2 (K4-K10):** S11 on post-S10F L2/S2 state, world stays A2.
  S11A re-arms counters (C_Q=500); S11B runs a VERIFY-shaped stale
  query (goal 818, reuses RETRIEVE-bound tagC=801) through the live
  do_query path; S11C stages the B1 tag-shape collision (real
  try_family trials, 3x u_invalidate, fresh judgment table from trial
  outcomes, u_revise; C_Q re-armed to 500 as disclosed apparatus);
  S11D runs the live recovery query with NO clear_plans anywhere in
  the S11 path. SUMMARY-COLLISION reports cumulative stats.

## Kill bars (all green)

- **K1 (self-trigger preserved):** PASS. S10D's E1 trigger-B
  revision fires exactly as in INTEGRATION-SELFTRIG (lines 1-87
  byte-identical, including the S10 ISD/REVISE lines).
- **K2 (B2 contract preserved):** PASS. S10 drift and recovery are
  byte-identical; B2 coverage contracts induct, route, and revise
  exactly as in C455.
- **K3 (hook dormant, no B1 revision):** PASS. Lines 1-87 are
  byte-identical to st_run1.txt; zero HOOK lines in lines 1-87
  (grep count 0; the single HOOK line in the run is in S11).
- **K4 (S11B stale query misroutes end-to-end):** PASS. Frozen line
  reproduced exactly:
  `Q id=QD0 goal=818 st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56`
- **K5 (S11C staged B1 revision):** PASS. Frozen lines reproduced
  exactly:
  `ISD-REV tag=801 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1
  nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0`
  `ISD-CNT total=3 correct=0 revcount=1 first=500 olderr=2 fiterr=0`
- **K6 (no manual clear_plans in S11):** PASS. grep shows the only
  clear_plans call is S8's (cb_main.zag:967, pre-existing C455
  code); the S11 path (lines 1122-1262) contains no call. The
  stale plan is invalidated by the hook.
- **K7 (hook fires exactly once with correct telemetry):** PASS.
  Exactly one line: `HOOK gtag=818 need=0 tag=801 oldfam=0
  newfam=1`. L+13276 = 1 in SUMMARY-COLLISION.
- **K8 (QD1 agrees after hook rebuild):** PASS. Frozen line
  reproduced exactly:
  `Q id=QD1 goal=818 st=2 vers=3 ans=2:1,1 agree=1 cs=16 cg=56`
- **K9 (SUMMARY-COLLISION exact):** PASS.
  `SUMMARY-COLLISION agree=7 plans_built=4 plans_loaded=6 trials=9
  declines=0 cs=984 cg=2464 hook=1 covdc=0,0,0`
- **K10 (3/3 byte-identical):** PASS.
  sha256(cb_run1/2/3.txt) = 7374989a...f124 (3 identical); stderr
  empty on all three runs; exit code 0.
- **K11 (toolchain guard):** PASS. Step 0 executed at startup:
  PATH=$HOME/safebin, `which python3`/`which python` empty,
  pinned znc used for all builds. Zero forbidden invocations.
  Prereg committed alone (264d7870c, exactly PREREG.md +
  NAMECHECK.md) strictly before any implementation commit.
- **K12 (hygiene):** PASS. Zero em/en dash bytes in all sources,
  build script, and docs. 70+ world literals scanned (superset of
  the 17 canonical identifiers) with word-boundary grep: zero hits
  in cb_learn.zag/cb_main.zag. The 3 byte-copy modules were
  cmp-verified identical to st_*.
- **K13 (wiring audit):** PASS. u_invalidate sites: cb_learn
  860/883/904/937/977-979 (execute_plan refusals + disagree, all
  pre-existing), cb_main 639-641 (S9A demo), 734-738 (S9B demo),
  1157-1159 (S11C). u_revise sites: cb_learn 637 (cov_induct retire
  rule), cb_main 656 (S9A), 812 (S9B), 1174 (S11C). All per prereg.

## Falsification probes (F1-F6)

- **F1 (hook fires in Act 1):** would have produced a HOOK line in
  lines 1-87 or broken byte-identity. Absent. Mechanism: no B1
  revision occurs before S9A's demo (which never calls compose),
  so no plan can go stale.
- **F2 (hook misfires on B2 revision):** S10's post-drift
  B2 revision changes spec routing, not bound fams; plans_loaded
  continues normally and no HOOK line appears in lines 1-87.
- **F3 (hook needs more than one fire per binding change):** only
  one fire; the rebuilt plan binds live fams and revalidates
  clean.
- **F4 (self-trigger retry cannot attribute binding-caused vs
  coverage-caused disagreement):** confirmed as a real gap (I-4).
  It did not fire in this run (QD1 agreed first-try via the hook
  rebuild), but the gap is disclosed, bounded, and self-healing:
  a misattributed retry still converges within 3 attempts or
  terminates as disagree. Proposed follow-up: a learner-owned
  disagreement-attribution probe. This is the one known
  imperfection; it does not weaken any kill bar.
- **F5 (B2 revise-on-retire + B1 latch race on 901):** no race;
  the two revise paths sequence (S9B demo, S10 trigger-B, S11C)
  and sg(S2,901) stays 0/1/retire-latched correctly.
- **F6 (hook cost on plan-load hot path):** bounded by plan size
  (here 1-2 needs, 1 bind_fam each); L2/32k state unchanged.
  plans_loaded=6 matches INTEGRATION-SELFTRIG exactly.

## Design notes

- The **lazy hook** (validate in compose's hit path) won over the
  eager hook (on u_revise) because every execution goes through
  compose->plan_find, and eager would over-fire on B2 revises that
  change routing rather than fams, or require contract-kind
  discrimination. Frozen per PREREG.md.
- Two implementation slips were caught and fixed before the first
  green run: `b[c]=44` written where main's buffer is `B` (5
  sites), and `relC` renamed to `relC2` in S11 to avoid shadowing
  oracle_812's local. Both are byte-irrelevant now; the record is
  here for the audit trail.

## Artifacts

- Sources: cb_base.zag, cb_world.zag, cb_module.zag (byte-copies
  of st_*, cmp-verified), cb_learn.zag (st_learn + first_subj port
  + M3 hook), cb_main.zag (st_main + oracle_1ret/oracle_1vfy,
  zero_counters, okind 2/3, HOOK emit, S11A-S11D,
  SUMMARY-COLLISION), cb_build.sh.
- Runs: cb_run1.txt (97 lines, sha256
  7374989ac41dfc7975d737521c606dbe2c076c3acce0003c89849bcc783fc124),
  cb_run2.txt, cb_run3.txt (byte-identical), empty stderr logs.
- Binary: cb_bin (sha256
  03534d2d80ad5f97be0d3e9fef309d42afa6d3752717cd544c15b30a752fb70e).
- Design: PREREG.md (frozen), NAMECHECK.md (Step 0 + scope).

## What remains / recommended follow-ups

1. **Trigger-B attribution (I-4):** the disclosed gap. A
   follow-up battery could give the do_query retry loop a
   learner-owned attribution probe (binding-caused vs
   coverage-caused disagreement) and test whether it ever
   misattributes on purpose-built collision worlds.
2. **Ledger minting is paused for this task** (non-ledger); if
   claim minting resumes, the natural claims are the three
   non-interference results (hook dormancy, B2-revision
   transparency to the hook, single-fire invalidation).
3. The combined binary is a candidate substrate for the L2
   adaptive-reuse frontier: binding revision + plan
   invalidation + self-triggered recovery now coexist in one
   live query path, so reuse-across-revision experiments can
   build on it without re-integration.
