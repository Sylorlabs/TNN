# PREREG: COGOPS-OSCILLATORY (follow-up to COGOPS-CYCLES C442)

Date: 2026-10-03. Worker: COGOPS-OSCILLATORY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_oscillatory/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C442 proved cycles join the envelope for learner-owned procedures:
the generalized composer (change-driven iterated execution to
quiescence, frozen 16-pass cap) composes a self-loop walk and a
2-node VERIFY to RETRIEVE cycle to a taught fixpoint. Its honest
boundary: "oscillatory or divergent cycles (the cap is totality
insurance, never fired here)".

Question: does the generalization handle OSCILLATION, or only
convergence? A period-2 cycle never reaches output-stability, so
quiescence can never fire. The experiment runs two oscillatory
goals through the byte-identical C442 composer and characterizes
exactly what happens: does it terminate, does it converge, and is
the emitted answer meaningful?

Predicted verdict: INFORMATIVE-FAIL (mechanism). The composer
preserves totality (the cap fires; no hang, no crash) but has no
vocabulary for oscillation: quiescence-as-halting cannot
distinguish "converged" from "capped mid-oscillation", and the
emitted answer is a deterministic phase artifact of the cap
parity, not a composed answer. A stability probe proves the
emitted value is not a fixpoint, while a convergent control in
the same binary (goal 816, world C) reproduces C442's passes=9
quiescence. Same composer, same learner-owned procedures:
convergence is handled, oscillation is not.

## 2. Design

### 2.1 Composer identity (no redesign)

`c6_base.zag` is a byte-identical copy of C442's `c5_base.zag`
(verified by cmp). `c6_learn.zag` is a byte-identical copy of
C442's `c5_learn.zag` (verified by cmp): the four additive
deltas (topo_g, apply_kind1_g, execute_plan_iter with
quiescence + frozen cap 16, compose_iter) are unchanged, and no
new composer function is added. The oscillation behavior is
therefore a property of the SAME change-driven iteration, not a
new mechanism. New code exists only in `c6_world.zag`
(environment: world D, episode patterns, goal constructors) and
`c6_main.zag` (driver stages, oracles, probes). The banned
identifier list for the learner/driver grep (K5) is the 7 new
world/goal identifiers: 606, 608, 660, 661, 662, 818, 819.

### 2.2 World D and the oscillatory workload (environment-defined; opaque)

World D = world A (56 facts) + 5 workload facts, all opaque
integers, defined in `c6_world.zag` only (61 facts, within the
128 cap):
- rel 606 (3 facts): (661,606,660) [seed: RETRIEVE [606,660]
  returns [661]], (662,606,661), (661,606,662) [the 2-cycle:
  661 <-> 662]. From pass 2 on, RETRIEVE on this relation
  alternates [661], [662], [661], ... : a genuine period-2
  attractor. No fixpoint exists: RETRIEVE [606,661] = [662]
  and RETRIEVE [606,662] = [661], provable by the fact table.
- rel 608 (2 facts): (661,608,660), (662,608,660): markers so
  VERIFY [(s,608,660)] passes for both phases.

The learner is taught the workload by episodes (S2), exactly as
C442 taught the cycle workload: retrieve episodes on
(606,660), (606,661), (606,662) plus the seed pattern
(601,621), then specialize_ret; one verify episode on
[(661,608,660)], then specialize_vfy. The oscillation is
executed by the learner-owned spec versions (id 2 / id 3),
selected from learned coverage, never by a researcher hand
code path.

### 2.3 Goal 818: oscillatory self-loop (mirrors 816)

need0: tag 801, [601, 621] -> [611] (seed/carrier).
need1: tag 801, [606, 660]; kind-1 SELF-link (need1 -> need1:
OUTS slot 0 -> obj field): re-applies RETRIEVE to its own
output subject.
need2: tag 802, template [1, (0,608,660)]; kind-2 link
(need1 -> need2): VERIFY each visited subject.
Kahn order (self-loop ignored by indegree; topo_g takes the
last zero-indegree need): [1,2,0], placed=3/3, stall=0.

Predicted iteration (hand-traced against execute_plan_iter):
pass 0: need1 [606,660] -> [1,661] (self-link does not fire;
source output empty); need2 verifies 661 -> [1,661];
need0 -> [1,611]. Every pass changes need1's record
([1,661] <-> [1,662]) and need2 tracks it, so the self-link
and the kind-2 link re-dirty both needs every pass:
quiescence is unreachable. The cap fires at pass 16.
need1 executes 16 times: odd execs -> [1,661], even -> [1,662];
16th -> [1,662]. need2's 16th exec verifies 662 -> [1,662].
Final records in plan order [1,2,0]: need1 [1,662],
need2 [1,662], need0 [1,611].
Predicted Q line: st=2, vers=2,3,2,
ans=6:1,662,1,662,1,611, agree=1, cs=96, cg=1098, passes=16.

The agree=1 is preregistered as VACUOUS: the independent
all-generic oracle (oracle_osc818) walks the same 16-step
bounded walk (walk_fix with the C442 16-guard) from the same
seed, so oracle and executor share cap parity (both land on
the even phase, 662). Agreement here is cap-parity
correspondence, not semantic composition: no fixpoint exists
for either side to agree on. K3 carries the semantic weight.

Check counts: cs = need1 16x3 (bucket 606: 3 facts) +
need2 16x2 (bucket 608: 2 facts) + need0 1x16 = 96.
cg = seed ret_gen 61 + walk_fix 16x61 + vfy_gen 1x61 = 1098
(world D: 61 facts).

### 2.4 Goal 819: oscillatory 2-node cycle (mirrors 817)

need0: tag 801, [601, 621] -> [611] (carrier; no link to
need2, so need2's constructed obj 660 is the seed).
need1: tag 802, [1, (0,608,660)]; kind-2 (need2 -> need1).
need2: tag 801, [606, 660]; kind-1 (need1 -> need2, OUTS
slot 0 -> obj; the advance, applied every pass once need1
produces).
need3: tag 802, [1, (0,608,660)]; kind-2 (need1 -> need3):
acyclic sink.
Kahn stalls after placing need0 (placed count 1/4); the
fallback appends [1,2,3], plan order [0,1,2,3].

Predicted iteration: pass 0 is a startup transient
(need2 [606,660] -> [1,661]; need1/need3 read the empty
need2 output and emit [0], which out_eq_snap treats as
unchanged from the empty record, so no spurious dirtying).
From pass 1 the 2-node cycle oscillates: need1 verifies
need2's subject ([1,661]/[1,662] alternating), the kind-1
advance link feeds it back as need2's obj, need2 flips
phase. Quiescence unreachable; cap fires at pass 16.
Final (pass 15 end state): need0 [1,611]; need1 [1,661];
need2 [1,662]; need3 [1,661]. Note the 1-step lag signature:
need1 verified 661 while need2 already produced 662. No
converged semantics can produce records that disagree
across the cycle edge; this is the fingerprint of a
mid-oscillation capture.
Predicted Q line: st=2, vers=2,3,2,3,
ans=8:1,611,1,661,1,662,1,661, agree=0, cs=124, cg=1220,
passes=16.

agree=0 is PREDICTED (not a failure): oracle_osc819's
guarded walk lands on the even phase (662) and reads need1
as [1,662], need2 as RETRIEVE [606,662] = [1,661]; the
executor's need1 lags one step behind ([1,661]). The oracle
cannot define correctness for oscillation; the divergence
documents that the "intended answer" is ill-defined.

Check counts: cs = need0 16 + need1 15x2 (pass 0 verifies
nothing) + need2 16x3 + need3 15x2 = 124. cg = 61 + 976 +
61 + 61 + 61 = 1220. cs/cg accumulate over agree=1 queries
only, so O1 contributes neither.

### 2.5 Stability probes (the semantic test)

After the oscillatory queries, on world D, using only the
generic procedures as measurement instruments (no literals in
the driver; rel/obj read from the goal record):
- s1 = RETRIEVE [606,660] -> 661; s2 = RETRIEVE [606,s1] ->
  662; s3 = RETRIEVE [606,s2] -> 661.
- Predicted: s1=661, s2=662, s3=661, period2=1 (s3==s1 and
  s2!=s1). No value in {661,662} is a fixpoint, so whatever
  phase the cap captured (662 on both goals) is provably not
  stable under one more application.
After the convergent control (world C): fix = walk_fix on
need1's [rel,obj] -> 618; next = RETRIEVE [rel,fix] -> 618;
stable=1. The convergent answer IS a fixpoint; the
oscillatory answers are not.

### 2.6 Convergent control (same binary, same composer)

S6 teaches the C442 cycle workload on world C (retrieve
episodes on (604,611), (604,618), seed (601,621);
specialize_ret; verify episode on [(612,605,640)];
specialize_vfy; setup_worldC copied verbatim from c5).
S7 runs goal 816 (mk_goal816_C0 copied verbatim from c5)
through compose_iter. Predicted (C442's observed C0):
st=2, vers=2,3,2, ans=6:1,618,1,618,1,611, agree=1, cs=136,
cg=720, passes=9. Quiescence reached: the same composer
converges where a fixpoint exists.

Need tags 801/802 are REUSED throughout: the same
trial-learned bindings (801 -> RETRIEVE, 802 -> VERIFY) serve
the oscillatory self-loop, the oscillatory 2-cycle, and the
convergent self-loop. No new need tags, no new procedure
ids, no new link kinds.

## 3. What the experiment establishes observably

- K1 OSCILLATION (cap fires): S3 passes=16 AND S4 passes=16.
  Quiescence is not reached on either oscillatory goal; the
  frozen 16-pass cap is the only halting mechanism. The run
  terminates (no hang, no crash): totality holds.
- K2 PHASE ARTIFACT: S3 ans=6:1,662,1,662,1,611 and S4
  ans=8:1,611,1,661,1,662,1,661 exactly as hand-traced: the
  emitted answers are deterministic cap-parity captures,
  including the 1-step lag signature on the 2-node cycle.
- K3 NOT-A-FIXPOINT: S5 probe period2=1 (661->662->661);
  S8 control stable=1 (618->618). The oscillatory answers
  are provably not fixpoints; the convergent answer is.
- K4 COMPOSER IDENTITY: cmp c5_learn.zag c6_learn.zag
  identical; cmp c5_base.zag c6_base.zag identical; no new
  composer functions. The oscillation result is a property
  of the C442 iteration, not a redesign.
- K5 LEARNER-NOT-RESEARCHER: word-boundary grep for
  606,608,660,661,662,818,819 in c6_learn.zag and c6_main.zag
  returns empty; the oscillation executes under spec
  versions (vers lines 2,3,2 and 2,3,2,3); BIND shows
  801->fam0, 802->fam1 from trial (ok0=1 / ok1=1).
- K6 CONVERGENT CONTROL: S7 reproduces C442's C0 exactly
  (passes=9, ans=6:1,618,1,618,1,611, agree=1).
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr
  empty.
- K8 TOOLCHAIN: safebin active for every command;
  `which python3` and `which python` return nothing; zero
  forbidden-executable invocations; all computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).

Frozen summary prediction (agree=1 queries O0 and C0 only):
agree=2, plans_built=3, plans_loaded=0, trials=6,
declines=0, cs=232, cg=1818. Version uses: ret_spec 43,
ret_gen 0, vfy_spec 53, vfy_gen 0 (learner-owned procedures
execute every composed step; generics serve only as oracles
and probe instruments).

Correction C0 (pre-implementation, 2026-10-03): the prereg
as first committed wrote rs=50, vs=63 here and in
Section 3. Re-tracing C442's erratum E3 (the convergent
control's need2 executes 7 times, not 8: on pass 7 need1's
output is unchanged at the fixpoint, so need2 is never
re-dirtied) gives O0 rs=17 vs=16, O1 rs=17 vs=30,
C0 rs=9 vs=7, i.e. rs=43, vs=53. No implementation or
execution existed when this was caught; the corrected
numbers above are the frozen prediction.

Learner-state predictions:
- S1A: LSTATE-RET nrel=2 ids=601,602 cnts=16,16
  prov=0,0,3,56 rev=1.
- S1B: LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16
  prov=1,4,7,56 rev=1.
- S2 ret: LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3
  prov=0,8,11,61 rev=2.
- S2 vfy: LSTATE-VFY nrel=4 ids=601,602,603,608
  cnts=16,16,16,2 prov=1,12,12,61 rev=2.
- S6 ret: LSTATE-RET nrel=4 ids=601,602,606,604
  cnts=16,16,0,8 prov=0,13,15,72 rev=3.
- S6 vfy: LSTATE-VFY nrel=5 ids=601,602,603,608,605
  cnts=16,16,16,0,8 prov=1,16,16,72 rev=3.

## 4. Verdict mapping (frozen)

- K1-K3 as predicted, K4-K9 PASS: INFORMATIVE-FAIL
  (mechanism). The C442 generalization handles convergence
  only. Change-driven iteration to quiescence has no
  vocabulary for oscillation: a period-2 cycle never
  quiesces, the 16-pass cap fires, and the emitted answer is
  a deterministic phase artifact (with a 1-step lag across
  the 2-node cycle), not a composed answer. The stability
  probe proves the captured phase is not a fixpoint, while
  the same composer converges (passes=9) where a fixpoint
  exists. Totality is preserved (no hang, no crash), but the
  composer cannot recognize or report oscillation: the capped
  answer is emitted in the normal format with no
  oscillation flag. Follow-up: a halting vocabulary beyond
  output-stability (e.g. cycle/period detection in
  learner-owned state) is needed before oscillatory
  composition can be claimed.
- K1 FAIL (passes < 16 on an oscillatory goal): the cycle
  converged. Investigate: the workload may not oscillate as
  designed (check the S5 probe first). Do not promote.
- K2 FAIL: phase capture differs from the hand trace.
  Characterize the actual parity/lag; the executor model is
  wrong somewhere. Do not promote.
- K3 FAIL (period2=0 or stable=1 on the oscillatory
  relation): the workload has a fixpoint. Design error;
  the oscillation premise is void.
- K4 FAIL: the composer is not the C442 composer. VOID for
  the boundary claim; the experiment no longer tests C442's
  generalization.
- K5 FAIL: RESEARCHER CONTAMINATION. VOID for the
  learner-execution claim.
- K6 FAIL: REGRESSION. The composer no longer converges
  where C442 did. Suspend the oscillation claim until the
  regression is understood.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 5. What this establishes (and does not)

Establishes: whether C442's change-driven iteration handles
oscillation. Predicted: it terminates via the cap but does
not compose oscillation into a meaningful answer; the
halting vocabulary (output-stability) is blind to period-2
cycles, and the emitted records are phase artifacts. The
convergent control isolates the variable: the same composer,
the same learner-owned procedures, converge where a
fixpoint exists.

Does not establish: divergent (growing) cycles; 3+ node
oscillatory cycles; a repaired halting vocabulary (no
redesign is attempted here); learner invention of
oscillation handling; scaling beyond the tested sizes;
whether a different cap parity would change the emitted
phase (the cap is frozen at 16 by design).

## 6. Build plan (implementation follows this prereg commit)

Files (pure Zag), prefix `c6_`, in
`docs/lab/research-lead/overnight-20260928/cogops_oscillatory/`:
- `c6_base.zag`: byte-identical copy of c5_base.zag
  (cp + cmp).
- `c6_learn.zag`: byte-identical copy of c5_learn.zag
  (cp + cmp).
- `c6_world.zag`: setup_worldA/B (copied), setup_worldD
  (new: A + rel 606 seed+2-cycle + rel 608 markers),
  setup_worldC (copied from c5), ret_ep_pat (+ ids 6,7,8),
  vfy_ep_chain (+ id 6), cnt_ep_pat (copied), w_* helpers
  (copied), mk_goal818_D0 and mk_goal819_D1 (new),
  mk_goal816_C0 (copied from c5). All world literals live
  here.
- `c6_main.zag`: output helpers, run_retep/run_vfyep,
  ans_eq, chain_of, walk_fix (copied); oracle_osc818,
  oracle_osc819 (new; all-generic; 16-guarded walk);
  oracle_cyc816 (copied); do_query (copied + okind 4,5);
  topo_probe (copied); main with stages S1A, S1B, S2, S3,
  S4, S5, S6, S7, S8 and SUMMARY-OSC. No world literals:
  probe rel/obj values are read from the goal record.
- `c6_build.sh`: assemble + compile with the pinned
  safebin znc.

Zag-defect workarounds honored (per AGENTS.md): get32/set32
only; no _zag_print for dynamic content; no `!(A && B)` in
while conditions; if-nesting at most 3; _zag_malloc as *u8
threaded; no []u8 as *u8 casts. (All new code verified
against each.)

## 7. Stages and frozen predictions

S1A RET-LEARN (world A): episodes 0-3 (ids 0,1,2,3);
specialize_ret(0,3). Predicted LSTATE-RET as in Section 3.

S1B VFY-LEARN (world A): episodes 4-7 (ids 0,1,2,3);
specialize_vfy(4,7). Predicted LSTATE-VFY as in Section 3.

S2 OSC-LEARN (world D): setup_worldD; ret episodes 8,9,10
(ids 6,7,8: (606,660)->[661], (606,661)->[662],
(606,662)->[661], each n=1), ep 11 (id 2: seed (601,621));
specialize_ret(8,11); vfy ep 12 (id 6: [(661,608,660)],
v=1); specialize_vfy(12,12). Predicted LSTATE lines as in
Section 3.

S3 OSC-SELFLOOP (world D, generalized): goal 818 D0.
TOPO probe: placed=3/3, stall=0. Plan [1,2,0].
Predicted: st=2, vers=2,3,2, ans=6:1,662,1,662,1,611,
agree=1 (vacuous parity, Section 2.3), cs=96, cg=1098,
passes=16. plans_built=1, trials=6.

S4 OSC-2NODE (world D, generalized): goal 819 D1.
TOPO probe: placed=1/4, stall=1 (fallback [0,1,2,3]).
Predicted: st=2, vers=2,3,2,3,
ans=8:1,611,1,661,1,662,1,661, agree=0 (predicted,
Section 2.4), cs=124, cg=1220, passes=16. plans_built=2.

S5 STABILITY-PROBE (world D): ret_gen probes chained from
the goal record's [rel,obj]: s1=661, s2=662, s3=661,
period2=1. Proves no phase is a fixpoint.

S6 CYCLE-LEARN-C (world C): setup_worldC; ret episodes 13,
14 (ids 4,5), 15 (id 2); specialize_ret(13,15); vfy ep 16
(id 4); specialize_vfy(16,16). Predicted LSTATE lines as
in Section 3.

S7 CONV-SELFLOOP (world C, generalized): goal 816 C0.
TOPO probe: placed=3/3, stall=0. Plan [1,2,0].
Predicted: st=2, vers=2,3,2, ans=6:1,618,1,618,1,611,
agree=1, cs=136, cg=720, passes=9. plans_built=3.

S8 FIXPOINT-PROBE (world C): fix = walk_fix on need1's
[rel,obj] = 618; next = RETRIEVE [rel,fix] = 618;
stable=1. The convergent answer is a fixpoint.

SUMMARY-OSC: agree=2, plans_built=3, plans_loaded=0,
trials=6, declines=0, cs=232, cg=1818 (agree=1 queries
only: O0 and C0), rs=43, rg=0, vs=53, vg=0.

## 8. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0
guard), c6_base.zag, c6_learn.zag, c6_world.zag,
c6_main.zag, c6_build.sh, c6_full.zag (assembled; exactly
one `fn main`), c6_bin, c6_compile.txt, c6_run1/2/3.txt
(+ .err), REPORT.md.
