# PREREG: H-INTENT-UNIFIED9 Red Team (IU9-ADV) (FROZEN)

## Target claim under test

H-INTENT-UNIFIED9 SURVIVES (4/4, bounded L2 integration test):
R10's kind dispatch (proc_apply vs bridge_apply) on a mixed
bridge/proc pair beyond the top two is correct, and R10 does not
over-withhold on agreeing answers with different internal slots.

The IU9 builder closed the IU8 red team's named gap (X-IU8-2) with a
(proc,bridge) pair where the bridge was the second member, and
audited precision on proc/proc agreement.

## Adversary stance

Assume the IU9 claim is false. Attack the dispatch combinations and
precision dimensions the builder did not test:

1. The candidate list is built procs-first, bridges-second, so R10's
   pair loop can produce (proc,proc), (proc,bridge), and
   (bridge,bridge) pairs, but never (bridge,proc). The builder
   tested (proc,proc) via IU8 and (proc,bridge) via IU9 K-IU9-1.
   (bridge,bridge) is empirically untested: the only dispatch
   combination no frozen run has ever exercised.
2. Precision was audited only for proc/proc agreement. Bridge winners
   (kind=1) and truncated candidates agreeing with procs are
   untested.
3. B2 (em=1 vs em=0 non-truncated beyond the top two) and B3
   (POSSIBLE-diagnostic precision cost) are disclosed as untouched.
   This red team characterizes them empirically instead of taking
   the disclosure on faith.

## Frozen attacks

Setup-validity rule (frozen): every bar first checks its learn
preconditions via the `iu8_show` helper (prints kind, slot, em,
true npairs, applied answer) plus direct byte checks of applied
answers. If any learn fails, or kind/em/answer differs from the
frozen expectation, the bar reports SETUP-FAIL: no conclusion, NOT
counted as a pass. Post-hoc fixture tuning is forbidden.
Diagnostic counting is scoped to lines between the
`>>> SEC <id> BEGIN` and `>>> SEC <id> END` markers (the decide
section of each attack). Learn-phase emissions are out of scope.

Exact diagnostic texts (from the committed source):
- R10-NEW: `INTENT VERBATIM-CONFLICT: verbatim candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
- IU3-OLD: `INTENT VERBATIM-CONFLICT: top two candidates both have exact_match=1 but disagree; WITHHOLD AMBIGUOUS`
- IU4A: `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`
- IU4B: `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`
- R8: `INTENT TRUNCATED-CONFLICT-POSSIBLE: truncated candidates disagree beyond top two; WITHHOLD AMBIGUOUS`
- R9: `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer beyond top two; WITHHOLD AMBIGUOUS`

### X-IU9-1: bridge/bridge kind dispatch

Fresh W. Learn order (query `xab`, qlen=3), three bridges, no procs:
- B_a: `aab>aab;abb>abb;acb>acb;abcde>abcde;xab>xxx;xcb>xxx;xdb>xxx`
  (expected: rc>=1000, kind=1, em=1, cf=0, lm=0, score 40000,
  applied answer `xxx`)
- B_b: `aad>aad;aae>aae;aaf>aaf;aabcd>aabcd;xab>xxx;xeb>xxx;xfb>xxx`
  (expected: rc>=1000, kind=1, em=1, applied answer `xxx`;
  observed in validation: cf=1, score 60000; pinned as setup)
- B_c: `aab>baa;abb>bba;acb>bca;abcde>edcba;xab>bax;xcb>bcx;xdb>bdx`
  (expected: rc>=1000, kind=1, em=1, cf=0, lm=0, score 40000,
  applied answer `bax`)

Expected arrangement: top=B_b (60000, `xxx`), second=B_a (40000,
`xxx`); the top two agree, so IU3 does not fire. R10's pair loop
runs in candidate-index order (bridges only): (B_a,B_b) agrees on
`xxx`; (B_a,B_c) disagrees (`xxx` vs `bax`) and must trigger
bridge_apply vs bridge_apply.

Why this attacks: the dispatch reads ka/kb per candidate, but no
frozen run has ever executed the (1,1) combination. A latent
kind/slot confusion that only manifests when both sides take the
else branch would break exactly here.

PASS iff: kind=-2 AND the decide section contains R10-NEW exactly
once AND none of IU3-OLD, IU4A, IU4B, R8, R9 appears.
KILL iff: kind>=0 (both-verbatim bridge/bridge disagreement
silently resolved), or any panic.
DOWNGRADE iff: kind=-2 but a different guard's text fires, or
R10-NEW is absent.
SETUP-FAIL iff: any rc<1000, any em!=1, or any applied answer
differs from `xxx`/`xxx`/`bax`.

### X-IU9-2a: precision, bridge winner agreeing with procs

Fresh W. Learn order (query `xab`):
- Bw: `aab>aab;abb>abb;acb>acb;xab>xxx;xcb>xxx;xdb>xxx`
  (expected: rc>=1000, kind=1, em=1, cf=0, lm=1, score 50000,
  applied answer `xxx`)
- V1: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (expected: rc>=0, kind=0, em=1, score 40000, `xxx`)
- V2: `xabcd>xxx;xefgh>xxx;xab>xxx`
  (expected: rc>=0, kind=0, em=1, score 40000, `xxx`)

All three agree on `xxx`; the bridge wins outright (50000 vs
40000). R10 must not fire and the kind=1 winner must be returned
intact.

Why this attacks: the builder's precision audit used a proc
winner. A bridge winner takes a different return path
(res kind=1, bridge slot); an over-withhold or winner-selection
defect specific to kind=1 would break exactly here.

PASS iff: kind==1 AND zero `WITHHOLD AMBIGUOUS` occurrences in
the decide section.
KILL iff: kind==-2 (R10 over-withholds on agreement: precision
defect), or any panic.
DOWNGRADE iff: kind>=0 but kind!=1 (wrong winner returned).
SETUP-FAIL iff: setup invalid.

### X-IU9-2b: precision, truncated bridge agreeing with procs

Fresh W. Learn order (query `xab`):
- Tt: `xab>xxx;abc>xxx;def>xxx;ghi>xxx;jkl>xxx;mno>xxx;pqr>xxx;stu>xxx;vwx>xxx;yza>xxx;bcd>xxx;efg>xxx;hij>xxx;klm>xxx;nop>xxx;opq>xxx;qrs>xxx`
  (17 pairs; expected: rc>=1000, kind=1, em=1, true npairs=17
  (truncated), applied answer `xxx`; observed in validation:
  cf=1, score 70000; pinned as setup)
- V1: `xab>xxx;xbc>xxx;xde>xxx`
  (expected: rc>=0, kind=0, em=1, score 50000, `xxx`)
- V2: `xab>xxx;xfg>xxx;xhi>xxx`
  (expected: rc>=0, kind=0, em=1, score 50000, `xxx`)

All three agree on `xxx`. The truncated bridge wins (70000). R10
must not fire on a truncated agreeing member, and no truncated
guard may fire on agreement either.

Why this attacks: X-IU8-4 showed a truncated em=1 DISSENTER is
claimed by R10; the agreeing mirror (truncated member, kind=1,
winning) was never tested for over-withholding.

PASS iff: kind==1 AND zero `WITHHOLD AMBIGUOUS` occurrences in
the decide section.
KILL iff: kind==-2 (over-withhold on agreement), or any panic.
DOWNGRADE iff: kind>=0 but kind!=1.
SETUP-FAIL iff: setup invalid (including true npairs<=16).

### X-IU9-3: regression (production mains byte-identical, mechanism frozen)

Extract the COMMITTED `unified_learn.zag` and `intent_learn.zag`
at HEAD via git show, cmp-verified against the worktree, compile
each main once to /tmp with the pinned toolchain, run each binary
3 times directly. Additionally verify the mechanism region (lines
1-1579) is byte-identical between the IU8 result commit
`e948219c6` and HEAD (IU9 made no mechanism change).

PASS iff: unified output md5 = 904de9f83a2873c7a8862b71804a9065
and intent output md5 = 98315faec8faea24e75533892c0b240d on all
3 runs each, exit 0, zero stderr bytes, and the mechanism region
is byte-identical across the two commits.
KILL iff: any md5 differs, any run is not byte-identical, or the
mechanism region differs (silent behavior change).

### X-IU9-4a: boundary B2 characterization (em=1 vs em=0 non-truncated)

Fresh W. Learn order (query `xab`):
- V1: `xab>xxx;xbc>xxx;xde>xxx`
  (expected: rc>=0, kind=0, em=1, score 50000, `xxx`)
- V2: `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (expected: rc>=0, kind=0, em=1, score 40000, `xxx`)
- R3: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm`
  (expected: rc>=0, kind=0, em=0, true npairs=5 (not truncated),
  applied answer `bax`, score 10000)

The (V1,R3) and (V2,R3) pairs are the disclosed B2 class: em=1 vs
em=0 non-truncated. No guard claims them (R8 needs em=0 both, R9
needs the em=0 side truncated, R10 needs em=1 both). Expected:
silent resolution by score, kind=0, zero withhold diagnostics.

This bar characterizes the boundary; B2 is outside the IU9 claim
scope, so it cannot kill. PASS iff the observation matches the
disclosed boundary (kind==0, zero `WITHHOLD AMBIGUOUS`).
BOUNDARY-DEVIATION (reported, coordinator adjudicates, not a
kill) iff kind==-2 or any diagnostic appears (the boundary as
disclosed would be wrong).
SETUP-FAIL iff: setup invalid.

### X-IU9-4b: boundary B3 context, R9 positive control

Fresh W. Learn order (query `xab`):
- V0: `xab>xxx;xbc>xxx;xde>xxx`
  (expected: rc>=0, kind=0, em=1, score 50000, `xxx`)
- V1: `xab>xxx;xfg>xxx;xhi>xxx`
  (expected: rc>=0, kind=0, em=1, score 50000, `xxx`)
- T2: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;opq>qpo;qrs>srq;rst>tsr`
  (18 pairs, query unrecorded; expected: rc>=0, kind=0, em=0,
  true npairs=17 (truncated), applied answer `bax`, score 10000)

The top two (V0,V1) agree on `xxx`. R9 must claim the (V0,T2)
verbatim-vs-truncated disagreement with its POSSIBLE diagnostic.
This is the guard whose precision cost B3 is about; the control
confirms the guard works as specified before the cost is
discussed.

PASS iff: kind=-2 AND the decide section contains the R9 text
(`verbatim candidate meets truncated record with different
answer beyond top two`) exactly once AND none of IU3-OLD, IU4A,
IU4B, R8, R10-NEW appears.
KILL iff: kind>=0 (R9's pair class silently resolved: genuine
guard defect), or any panic.
DOWNGRADE iff: kind=-2 but a different guard's text fires, or
the R9 text is absent.
SETUP-FAIL iff: setup invalid.

## Frozen verdict rules

- Any KILL trigger: H-INTENT-UNIFIED9 is KILLED.
- Any DOWNGRADE trigger (no KILL): H-INTENT-UNIFIED9 is
  DOWNGRADED (survives with a named defect).
- All bars PASS with no SETUP-FAIL and no BOUNDARY-DEVIATION:
  H-INTENT-UNIFIED9 SURVIVES the red team.
- SETUP-FAIL on a bar: reported as no-conclusion for that bar,
  never as a pass; a second distinct fixture is forbidden.
- BOUNDARY-DEVIATION on X-IU9-4a: reported as a characterization
  result for coordinator adjudication, not a kill.

## Frozen methodology

1. This prereg is committed ALONE before any adversary harness
   build, compile, or run. Commit order verified by
   `git merge-base --is-ancestor`.
2. Adversary harness `iu9_adv.zag` = mechanism region of the
   COMMITTED `unified_learn.zag` at HEAD (lines 1-1579,
   everything before `fn main`), extracted via `git show`,
   cmp-verified byte-identical against the working-tree region;
   plus t_learn, t_decide, iu4_init, iu8_show carried verbatim
   from the committed `iu8_verify.zag` (lines 1580-1698); plus
   a new X-IU9-1/2a/2b/4a/4b attack main. No mechanism byte is
   altered.
3. Evidence method: compile once to /tmp with the pinned
   toolchain (binaries never committed); execute the binary
   directly 3 times for clean raws (exit 0, zero stderr).
   Raw evidence: `IU9_ADV_RAW.txt` (md5 recorded, 3/3
   byte-identical via cmp).
4. Pure Zag throughout: prereg, harness, builds, runs, greps,
   md5, cmp. No Python at any stage.
5. Toolchain: znc 2026.07.0-dev (edition 2026), pinned at
   /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc.
6. Only researcher-owned paths staged (pathspec-restricted).
   Concurrent workers' files untouched.
7. No em dashes in loop documentation (byte-verified).
