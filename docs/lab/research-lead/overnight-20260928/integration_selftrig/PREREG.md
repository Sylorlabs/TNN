# PREREG: INTEGRATION-SELFTRIG (self-triggered revision in the live query path)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/integration_selftrig/` only.
Worker: INTEGRATION-SELFTRIG worker (subagent, 2026-10-03).
Parent mandate: INTEGRATION-B1B2 (C455) follow-up, open thread 1.
C455 demonstrated that the C443 B1/B2 contracts integrate at the
COGOPS composer's binding layer, but its revision (S9A/S9B) was
researcher-staged: the driver called u_invalidate/u_revise with
hand-chosen judgment/consequence pairs. This experiment wires
u_invalidate into the live query path so revision fires during
live operation, triggered by what the composer itself observes.

Commit order: this prereg (plus NAMECHECK.md Step 0) strictly
precedes all implementation. No implementation file exists in
this lane at this commit.

## 1. Question and predicted outcome

Question: can the C455 integrated composer revise its own
bindings during live operation, with u_invalidate fired by live
query outcomes (spec refusal or oracle disagreement) rather than
by a staged demo, and u_revise fired by the latched request at
the next specialize?

PREDICTED OUTCOME (frozen): SELF-TRIGGERED REVISION
DEMONSTRATED. A drift injected between queries (world facts
rearranged; relation vocabulary unchanged) makes the learner's
positional procedure indexes stale. The next live queries
disagree with the independent all-generic oracles; the query
path itself invalidates the spec-routing coverage contracts
(judgment=1, consequence=0); after two disagreeing attempts all
three coverage clauses retire and the third attempt falls back
to generic routing with full agreement; a subsequent
re-specialize (the natural composer operation) sees the latched
revision request and revises each retired contract from fresh
evidence (revcount 1,2,3); spec routing is restored and the
goals pass. The C455 S1A-S9 battery runs unchanged first and
its output is byte-identical to C455's frozen run.

## 2. The self-trigger design (frozen)

### 2.1 What "self-triggered" means here

The researcher injects the drift (rewrites the world fact
array between queries; this is the environment changing, as in
C455 S5). Everything else is composer-driven: the invalidate
calls fire inside the per-query path (do_query /
execute_plan), the revision-request latch is set by those
invalidates, and u_revise fires inside specialize (via
cov_induct) because the request is latched. No demo stage
chooses which contract to invalidate, which judgment or
consequence to report, or when to revise. The S9 demos remain
in the battery unchanged (they are C455's staged evidence);
S10 is the new live-path battery.

### 2.2 Trigger A: spec refusal (internal; execute_plan)

In execute_plan, each spec-procedure call site checks for the
refusal return (-1):
- ret_spec -> -1: u_invalidate(S,3000,1,0), then fall back to
  ret_gen for that need.
- vfy_spec -> -1 (both the src<0 and src>=0 sites):
  u_invalidate(S,3100,1,0), then fall back to vfy_gen.
- cnt_spec -> -1: u_invalidate(S,3200,1,0), then fall back to
  cnt_gen.
Judgment=1 is the coverage contract's standing admission;
consequence=0 is the procedure's observed refusal. The
fallback keeps the query live (the answer is still produced).
FROZEN PREDICTION: this wiring is dormant in S10 (no
working-set/contract divergence occurs in the battery; the
contracts and working sets are inducted together and the drift
preserves the vocabulary, so no -1 can arise). It is wired and
source-audited (K10), disclosed as not fired.

### 2.3 Trigger B: oracle disagreement (live; do_query)

do_query is the live per-query path. After the oracle
comparison, on ans_eq=0 with at least one spec version in
vbuf, the composer function note_answer_disagree invalidates
each family that routed spec, once per family per attempt:
u_invalidate(S,3000,1,0) if any need vers=2;
u_invalidate(S,3100,1,0) if any need vers=3;
u_invalidate(S,3200,1,0) if any need vers=5.
Judgment=1: the composer's spec routing was sound;
consequence=0: the joint answer disagreed with the
independent oracle. Rationale (frozen): the composer cannot
attribute a joint-answer disagreement to one family from the
answer record alone; the conservative learner response is to
distrust every spec commitment that contributed. do_query then
retries the query (bounded self-correction, max 3 attempts);
each disagreeing attempt re-invalidates. A RETRY line is
emitted per invalidate round. On agree, or on disagree with no
spec versions, or after attempt 3, do_query returns.
FROZEN PREDICTION: on a first-try agree the retry path emits
nothing, so S1A-S9 output is byte-identical to C455.

### 2.4 Revision via the latched request (cov_induct)

cov_induct (called by specialize_ret/vfy/cnt) currently calls
u_induct unconditionally. New rule (frozen): after loading the
fresh judgment table, if the contract was previously committed
(CONTRACT_SET=1) and no clause is active (all retired), this
is a REVISION, not a fresh induct: the composer ensures the
revision request is latched (ss(S,901,1) if 901==0; the
request originates from the live-path failures) and calls
u_revise(S,cbase,1), which scores the old clause on the new
table (olderr), re-inducts, and bumps revcount. Otherwise
u_induct as before. FROZEN PREDICTION: in C455's S1A-S9 this
case never occurs (contracts are fresh or healthy), so S1A-S9
output is byte-identical.

### 2.5 The drift (frozen)

setup_worldA2 (new, in st_world.zag): the same 56 facts as
world A (same relation vocabulary 601,602,603,607,609, same
multiset), rewritten in a different order: 603 facts at slots
0-15, 602 facts at slots 16-31, 601 facts at slots 32-47,
distractors at 48-55. The learner's bucket indexes (positional,
built by specialize on world A) go stale: spec procedures
scan the old positions and miss. The contracts still admit the
rels (correctly; the rels are present), so version selection
still routes spec. Generic procedures (and the oracles) scan
the current array and stay correct. Consequence: genuine
oracle disagreement on spec-routed queries, observed live.

### 2.6 Opaque identifiers

No world literals in st_learn.zag or st_main.zag (same 17
identifiers as C455 K3a, verified by the same word-boundary
grep). setup_worldA2 lives in st_world.zag with the other
environment definitions. All S10 values are runtime-derived.

## 3. Frozen predictions: S1A-S9 (C455 regression)

The battery runs C455's S1A, S1B, S1C, S2, S3, S4, S5, S6, S7,
S8, S9A, S9B unchanged (same code paths; do_query's retry is
silent on first-try agree; the C_Q tick in do_query is output-
invisible since S[7] is never printed and S9 overwrites it).
PREDICTION: the S1A-through-SUMMARY-DIAMOND output, and the
S9A/S9B lines, are BYTE-IDENTICAL to C455's ib_run1.txt.
Verified by diff, not by re-derivation.

## 4. Frozen predictions: S10 (self-triggered revision battery)

S10 runs on fresh composer state (L2, S2; 16384 bytes each,
zeroed) so S9's state changes do not pollute it. The shared
world array A is reset with setup_worldA at S10A start. C_Q
(S2 slot 7) ticks once per do_query call.

### S10A LEARN (world A; mirrors C455 S1, no per-episode lines)

4 RET episodes (pattern ids 0-3) + specialize_ret; 4 VFY
episodes (chain ids 0-3) + specialize_vfy; 4 CNT episodes
(pattern ids 0-3) + specialize_cnt. Working sets {601,602},
{601,602,603}, {601,602,603}; coverage clauses RET
(0,identity,[601,602]), VFY (0,identity,[601,603]), CNT
(0,identity,[601,603]).

### S10B BASELINE (C_Q=1,2)

- E0 (mk_goal813_E0): st=2 vers=2,3,3,5
  ans=7:1,611,0,1,611,1,2 agree=1 cs=96 cg=336.
  (C455 S2 frozen values; plan built, plans_built=1, trials=9.)
- R0 (mk_goal808_A0): st=2 vers=2,3,5
  ans=6:1,613,1,613,1,2 agree=1 cs=64 cg=224.
  (C455 S4 frozen values; plans_built=2, trials still 9.)
- BCONTRACT dump (from L2/S2):
  801 induct=1 clause=(1,0,0,0) active=1 dc=0;
  802 induct=1 clause=(1,0,1,1) active=1 dc=0;
  807 induct=1 clause=(1,0,2,2) active=1 dc=0.

### S10C DRIFT-INJECT

setup_worldA2(A). DRIFT line emitted. No clearing, no
re-specialize: this is the drift.

### S10D DRIFT-QUERIES (C_Q=3,4)

E0 on the drifted world (plan loaded, st=1):
- Attempt 1: vers=2,3,3,5. need0 spec scans stale 601-bucket
  (old indexes {0,1,6,7,12,13,18,19,24,25,30,31,36,37,42,43}
  now hold 603/602/601 facts whose objects never equal 621)
  -> OUTS[0]=[0]; oracle ret_gen finds (611,601,621) ->
  [1,611]. need1/need2 verify over empty subjects -> [0]
  both sides. need3 count over empty -> [1,0] both sides.
  ans=5:0,0,0,1,0 vs oracle 6:1,611,0,0,1,0 -> agree=0.
  note_answer_disagree: RET/VFY/CNT invalidated once each
  (judgment=1, consequence=0). RETRY att=1 dc=1,1,1
  active=1,1,1 req=1 first=3. (Fail run 900 hits 3 on the
  third invalidate, latching 901 with first_detect=C_Q=3.)
- Attempt 2: clauses still active (dc=1). vers=2,3,3,5,
  same stale answers -> agree=0. Three more invalidates:
  dc=2,2,2 -> all three clauses RETIRE (active=0). RETRY
  att=2 dc=2,2,2 active=0,0,0 req=1 first=3.
- Attempt 3: u_check=0 on all three (no active clause) ->
  vers=0,1,1,4 (all generic). Generic procedures scan the
  current array -> ans=7:1,611,0,1,611,1,2 agree=1.
  The composer self-healed by retiring stale commitments.
R0 on the drifted world (clauses retired; C_Q=4): vers=0,1,1,4
  on attempt 1 -> ans=6:1,613,1,613,1,2 agree=1. No
  invalidates (agree on first try).

### S10E REVISE

2 episodes per family on A2 (re-log; working sets unchanged),
then specialize_ret/vfy/cnt. Each cov_induct finds its
contract committed-but-retired with the request latched (or
re-asserts it) and calls u_revise:
- REVISE fam=ret olderr=0 revcount=1
  nclause=(0,0,601,602) active=1.
  (Old [601,602] errs 0 on the new table: accepts 601,602
  admitted, rejects 603,607,609 refused; re-induct gives the
  same clause; buckets rebuilt from the A2 array.)
- REVISE fam=vfy olderr=0 revcount=2
  nclause=(0,0,601,603) active=1.
- REVISE fam=cnt olderr=0 revcount=3
  nclause=(0,0,601,603) active=1.
The revision re-derives each binding from fresh evidence; the
clause is unchanged because the drift preserved the relation
vocabulary (frozen expectation, not a failure: the stale part
was the positional index, which specialize rebuilds).

### S10F RECOVER (C_Q=5,6)

- E0: vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1 cs=96
  cg=336. (Fresh buckets; spec routing restored.)
- R0: vers=2,3,5 ans=6:1,613,1,613,1,2 agree=1 cs=64
  cg=224.
SUMMARY-DRIFT: agree=6 (8 attempts, 6 agreeing),
plans_built=2 plans_loaded=6 trials=9 declines=0; cs/cg
totals observed from run 1 and byte-identical in runs 2/3
(not hand-derived).

## 5. Kill bars (frozen)

- K1 BASE INTACT: S1A-through-SUMMARY-DIAMOND and S9A/S9B
  output byte-identical to C455's ib_run1.txt (diff clean).
- K2 BASELINE: S10B E0/R0 lines exactly as frozen in 4/S10B
  (st, vers, ans, agree, cs, cg).
- K3 SELF-TRIGGER: S10D E0 attempts 1-2 agree=0 with
  vers=2,3,3,5; RETRY lines exactly dc=1,1,1/active=1,1,1
  then dc=2,2,2/active=0,0,0, req=1 first=3 both times.
  (Revision fired during live queries: u_invalidate called
  from do_query, not from a demo stage.)
- K4 SELF-HEAL: S10D E0 attempt 3 agree=1 vers=0,1,1,4
  ans=7:1,611,0,1,611,1,2; R0 agree=1 vers=0,1,1,4
  ans=6:1,613,1,613,1,2.
- K5 REVISE-VIA-LATCH: S10E REVISE lines exactly as frozen
  in 4/S10E (olderr=0 revcount=1,2,3; clauses as listed;
  active=1).
- K6 RECOVERY: S10F E0/R0 lines exactly as frozen in 4/S10F.
- K7 DETERMINISM: 3/3 byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin every command; `which python3` and
  `which python` return nothing; zero forbidden invocations;
  pure Zag via the pinned znc; shell only for
  znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified); word-boundary grep over the 17 identifiers
  empty in st_learn.zag and st_main.zag.
- K10 LIVE-PATH WIRING: source audit shows u_invalidate is
  called (a) in execute_plan at the three spec-refusal
  fallback sites, (b) in note_answer_disagree (called only
  from do_query's live retry path); u_revise is called only
  from cov_induct under the retired-with-latch rule; no
  S9-style staged invalidate/revise calls exist for S10.

## 6. Falsification criteria (frozen)

- F1: S1A-S9 output differs from C455's ib_run1.txt ->
  the self-trigger wiring broke the base; diagnose, do not
  amend.
- F2: S10D E0 attempt 1 agrees -> the drift does not produce
  disagreement; the trigger design is wrong.
- F3: S10D E0 attempt 3 disagrees -> retirement/fallback
  failed; diagnose.
- F4: S10E REVISE lines differ (revcount, olderr, clauses) ->
  the revise did not fire via the latched request.
- F5: audit finds an S10 invalidate/revise call outside the
  live query path or the latch rule -> the self-trigger
  claim is VOID.

## 7. Verdict mapping (frozen)

- K1-K10 PASS: SELF-TRIGGERED REVISION DEMONSTRATED. The
  composer revises its own bindings during live operation:
  drift -> live disagreement -> self-fired invalidates ->
  clause retirement -> generic fallback (goals pass) ->
  latch-driven revise at re-specialize -> spec routing
  restored (goals pass). No staged demo chooses the
  contract, the evidence, or the timing.
- K1 PASS, K3/K5 FAIL: STAGED-ONLY. Composition preserved
  but revision did not self-trigger; the wiring is
  behavior-neutral plumbing.
- K1 FAIL: BASE BROKEN. The wiring changed composition
  behavior; diagnose before any further claim.
- K4/K6 FAIL with K3/K5 PASS: revision fires but goals do
  not survive it; the fallback/revise path is incorrect.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 8. Build and run plan (post prereg)

Files (prefix `st_`), all pure Zag, in
`docs/lab/research-lead/overnight-20260928/integration_selftrig/`:
- `st_base.zag`: byte-copy of
  integration_b1b2/ib_base.zag (cmp-verified).
- `st_world.zag`: ib_world.zag content + setup_worldA2
  appended (ib_world part cmp-verified against the source).
- `st_module.zag`: byte-copy of
  integration_b1b2/ib_module.zag (cmp-verified; u_* bodies
  untouched).
- `st_learn.zag`: ib_learn.zag + (a) spec-refusal fallback
  with u_invalidate at the three spec call sites in
  execute_plan, (b) note_answer_disagree (per-family
  invalidate on live disagreement + RETRY line), (c)
  revise-on-retire rule in cov_induct. No other logic
  changes.
- `st_main.zag`: ib_main.zag + (a) do_query retry loop
  (max 3 attempts; silent on first-try agree) and C_Q tick,
  (b) S10A-S10F stages on fresh L2/S2, (c) emit_revise
  helper, (d) SUMMARY-DRIFT. S1A-S9 code unchanged.
- `st_full.zag`: concatenation (exactly one `fn main`).
- `st_build.sh`: assemble + compile with the pinned safebin
  znc (`$HOME/workspace/tnn-rsi/src/tools/toolchain/
  znc_linux_x86_64_abed8aa1`).
- Run 3x (`st_run1/2/3.txt` + `.err`), sha256sum compare,
  stderr empty. Byte-verify: st_base/st_module vs ib
  sources; st_world head vs ib_world; zero em/en dash bytes
  in docs; zero of the 17 identifiers in st_learn.zag/
  st_main.zag; diff S1A-SUMMARY-DIAMOND + S9A/S9B sections
  vs C455 ib_run1.txt. Write REPORT.md.

Commits (explicit pathspecs, /usr/bin/git, local only, never
pushed): (1) this prereg + NAMECHECK.md alone; (2)
implementation; (3) build artifacts + runs; (4) REPORT.md.
