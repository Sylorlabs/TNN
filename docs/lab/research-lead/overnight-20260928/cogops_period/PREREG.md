# PREREG: COGOPS-PERIOD (follow-up to COGOPS-OSCILLATORY C451)

Date: 2026-10-03. Worker: COGOPS-PERIOD.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_period/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C451 (INFORMATIVE-FAIL) proved C442's change-driven iteration
handles convergence only: on period-2 oscillatory goals the
16-pass cap fires, quiescence is unreachable, and the emitted
answer is a deterministic phase artifact with no oscillation
flag. Its follow-up #1: a halting vocabulary beyond
output-stability (period detection in learner-owned state)
before oscillatory composition can be claimed.

Key question: can the learner recognize oscillation as a
distinct outcome? That is, can the system halt on a
period-k trajectory with a first-class OSCILLATION outcome
(period + reported orbit), distinct in form from both a
converged answer and a cap-parity capture, rather than
emitting one captured phase as if it were an answer?

Predicted verdict: BUILD-PASS (mechanism). The additive
period-detection halting vocabulary detects period-2 on both
C451 goals (halting at passes 3 and 4, not 16), detects
period-3 on a new 3-cycle goal (pass 4), reports the full
orbit (all phases, never a single captured phase), and the
convergent control reproduces C451 byte-exactly (passes=9,
halt=conv). The detection is not a phase artifact: it fires
iff the deterministic trajectory provably repeats (a
repeated global state in deterministic iteration is a
cycle, by construction), and the report is confirmed by an
independent all-generic attractor computation with
phase-independent orbit-set agreement.

## 2. Design

### 2.1 The halting vocabulary generalization

C442's halting rule is output-stability: halt CONVERGED when
a pass executes no dirty need (equivalently, the global
output state repeats with period 1). The generalization is
exact: halt OSCILLATION when the global output state
repeats with period k > 1. Same machinery class as the
existing quiescence check (generic snapshot equality over
learner-owned procedure outputs), extended from comparing
against pass t-1 to comparing against passes t-2 and
t-3. The 16-pass cap remains as totality insurance for
aperiodic trajectories (halt=CAP).

Detection rule (after each completed pass t, t >= 2):
- period 2 iff sig(t) == sig(t-2) AND sig(t) != sig(t-1)
- period 3 iff sig(t) == sig(t-3) AND sig(t) != sig(t-1)
  AND sig(t) != sig(t-2)

The distinctness guards are load-bearing: a fixpoint
approach (sig(t) == sig(t-1)) can never be misclassified
as oscillation. Because the iteration is deterministic,
sig(t) == sig(t-k) with the guards proves the system is
on a period-k cycle; this is a theorem about the
trajectory, not a parity coincidence. One match suffices;
no voting or windowing.

### 2.2 Learner-owned state

The trajectory history and the outcome record live in the
learner's persistent state L (the same 16384-byte arena as
LSTATE), not in researcher driver variables. New tail
region (after stats at 13224..13276):
- 13276: osc_m (snapshots stored, 0..4)
- 13280: osc_nn (nneeds snapshotted)
- 13284: osc_hist: 4 snapshots x 4 needs x 33 i32
  (2112 bytes, ends 15396). Per need: [n, up to 32 vals].
- 15396: osc_outcome [halt_kind, period, passes] (12 bytes)

The history is a bounded ring (depth 4, shift on overflow);
it is reset per query. The outcome persists in L after
the query as the substrate for future learning.

Boundary statement (frozen): the comparison itself is
generic machinery, the same class as the existing
out_eq_snap quiescence check. The learner did not invent
the detector from experience. What is learner-owned: the
trajectory history, the outcome record, and the
procedures whose outputs oscillate (built by the learner
from episodes). What this establishes: oscillation is now
a first-class outcome the system halts on and reports,
recorded in learner state. What it does not: learner-
invented oscillation detection (explicit future work).

### 2.3 Additive composer delta (no redesign)

`c7_learn.zag` begins with the exact bytes of
`c6_learn.zag` (verified by head -c + cmp); no C442/C451
function is modified. The new section adds only:
- osc_hist_reset / osc_hist_push / osc_hist_eq:
  history management and generic snapshot equality.
- osc_detect: the period 2/3 rule of Section 2.1.
- osc_emit_orbit: orbit report emission.
- execute_plan_iter_pd: the execute_plan_iter loop with
  per-pass snapshot push and the three-way halt
  (quiescence -> halt=0 CONV; detect -> halt=1 OSC;
  cap -> halt=2 CAP). vbuf[20]=passes, vbuf[21]=halt,
  vbuf[22]=period. Answer emission: CONV/CAP -> final
  records in plan order (identical to execute_plan_iter);
  OSC -> [period k, then k phases x nn needs x full
  records in plan order] (the orbit, never one phase).
- compose_iter_pd: compose_iter calling the pd executor.

`c7_base.zag` is a byte-identical copy of `c6_base.zag`
(cp + cmp). `c7_world.zag` extends the environment only:
world E (period-3 workload), retrieve patterns ids 9-12,
verify chain id 7, goal 820. All world literals live
there. The driver reads rel/obj/seed from goal records;
no literals in c7_learn.zag or c7_main.zag.

### 2.4 Agreement: phase-independent orbit confirmation

For OSC goals the oracle does not compare final records
(phase-dependent). Instead, an independent all-generic
attractor walk (oracle_attractor: repeated ret_gen until
a value repeats, bounded 8 steps) finds the cycle and its
length from the goal record's [rel, seed]. Agreement
holds iff: executor halt=OSC, executor period == oracle
cycle length, and the executor's reported driver-need
orbit value SET == the oracle's cycle SET (both
directions). Orbit-set agreement is phase-independent by
construction: it cannot be satisfied by cap parity. The
driver-need plan position (818->0, 819->2, 820->0) is
instrument calibration in the oracle dispatch, the same
class as C451's goal-specific oracles.

### 2.5 World E and goal 820 (period-3; environment; opaque)

World E = world A (56 facts) + 7 workload facts (63 facts,
within the 128 cap), defined in c7_world.zag only:
- rel 612 (4 facts): seed (671,612,670) plus the 3-cycle
  (672,612,671), (673,612,672), (671,612,673): RETRIEVE
  walks 671->672->673->671. No fixpoint exists.
- rel 613 (3 facts): markers (671,613,670),
  (672,613,670), (673,613,670) so VERIFY passes on all
  three phases.

Goal 820: same shape as 818 (oscillatory self-loop):
need0 tag 801 [601,621] carrier; need1 tag 801 [612,670]
with kind-1 SELF-link; need2 tag 802 template [1,(0,613,670)]
with kind-2 link need1->need2. Kahn order [1,2,0].

Predicted iteration: pass 0: need1 -> [1,671]; pass 1:
[1,672]; pass 2: [1,673]; pass 3: [1,671] = sig0.
At t=3: sig3==sig0, sig3!=sig1, sig3!=sig2 -> period 3
fires. Passes used = 4. Orbit (plan order [1,2,0]):
sig1=([1,672],[1,672],[1,611]),
sig2=([1,673],[1,673],[1,611]),
sig3=([1,671],[1,671],[1,611]).
Predicted Q: st=2, vers=2,3,2, halt=osc, period=3,
ans=19:3,1,672,1,672,1,611,1,673,1,673,1,611,1,671,1,671,1,611,
agree=1, cs=44, cg=252, passes=4.

Check counts: cs = need1 4x4 (bucket 612: 4 facts) +
need2 4x3 (bucket 613: 3 facts) + need0 1x16 = 44.
cg = 4 attractor ret_gen calls x 63 facts = 252.
rs = need1 4 + need0 1 = 5; vs = need2 4 = 4.

### 2.6 Predicted period-2 traces (hand-traced)

O0 (818): pass 0: need1 [606,660]->[1,661] (self-link
does not fire, source empty); need2 verifies 661;
need0 -> [1,611]. pass 1: need1 -> [1,662]; need2 ->
[1,662]. pass 2: need1 -> [1,661]; need2 -> [1,661]:
sig2 == sig0, sig2 != sig1 -> period 2 fires at t=2.
Passes = 3. Orbit: sig1=([1,662],[1,662],[1,611]),
sig2=([1,661],[1,661],[1,611]).
Predicted Q: st=2, vers=2,3,2, halt=osc, period=2,
ans=13:2,1,662,1,662,1,611,1,661,1,661,1,611,
agree=1, cs=31, cg=183, passes=3.
cs = 3x3 + 3x2 + 16 = 31. cg = 3x61 = 183.
rs = 3 + 1 = 4; vs = 3.

O1 (819): pass 0 startup transient (need2 -> [1,661];
need1/need3 read empty outputs -> [0], correctly
unchanged). passes 1..3 oscillate with the 1-step lag.
sig1=([1,611],[1,661],[1,662],[1,661]) [need order
0,1,2,3]; sig2=([1,611],[1,662],[1,661],[1,662]);
sig3=([1,611],[1,661],[1,662],[1,661]) == sig1,
sig3 != sig2 -> period 2 fires at t=3. Passes = 4.
Orbit phases sig2, sig3 (the lag signature is preserved
in the orbit: need1 [1,662] while need2 [1,661]).
Predicted Q: st=2, vers=2,3,2,3, halt=osc, period=2,
ans=17:2,1,611,1,662,1,661,1,662,1,611,1,661,1,662,1,661,
agree=1, cs=40, cg=183, passes=4.
cs = 16 + 3x2 + 4x3 + 3x2 = 40. cg = 3x61 = 183.
rs = 4 + 1 = 5; vs selections = 4 + 4 = 8.

C0 (816, convergent control): the walk 611->...->618
has all-distinct global snapshots until the fixpoint;
at t=7 sig7 == sig6 but the k=2 distinctness guard
(sig7 != sig6) fails, so no spurious OSC fire. Pass 8:
no dirty need -> halt=conv. Reproduces C451 exactly:
st=2, vers=2,3,2, halt=conv, period=0,
ans=6:1,618,1,618,1,611, agree=1, cs=136, cg=720,
passes=9.

### 2.7 Orbit-close probes (S8; generic instruments)

For each OSC goal, from the goal record's [rel, seed]:
run oracle_attractor -> cycle; then one fresh ret_gen
on the last cycle value must return the first cycle
value (closure). Predicted: close=1 on all three.
For C0: the C451 fixpoint probe (stable=1). Probe costs
do not accumulate into cs/cg (not queries).

## 3. Kill bars (frozen)

- K1 PERIOD-2 DETECTED AND REPORTED: O0 halts with
  halt=osc, period=2, passes=3; O1 halts with halt=osc,
  period=2, passes=4. Both halt strictly before the cap
  (early halt proves detection, not cap parity), and
  ans carries the full orbit (both phases), never a
  single captured phase.
- K2 NOT A PHASE ARTIFACT: (a) early halt per K1;
  (b) the orbit contains all phases of the cycle;
  (c) agree=1 via phase-independent orbit-set agreement
  with the independent generic attractor;
  (d) S8 closure probes close=1 on all OSC goals.
  The detection fires iff the deterministic trajectory
  provably repeats (Section 2.1).
- K3 PERIOD-3: O2 halts with halt=osc, period=3,
  passes=4; orbit {671,672,673}; agree=1.
- K4 CONVERGENT CONTROL: C0 reproduces C451 byte-exactly
  (halt=conv, period=0, passes=9,
  ans=6:1,618,1,618,1,611, agree=1, cs=136, cg=720).
  No spurious OSC fire during the convergent walk.
- K5 COMPOSER ADDITIVITY: c7_base.zag cmp-identical to
  c6_base.zag; c7_learn.zag begins with the exact bytes
  of c6_learn.zag (head -c + cmp); no existing function
  modified (new functions only); world extensions are
  environment-only.
- K6 LEARNER-NOT-RESEARCHER: word-boundary grep for
  606, 608, 612, 613, 660, 661, 662, 670, 671, 672,
  673, 818, 819, 820 in c7_learn.zag and c7_main.zag
  returns empty; the oscillation executes under
  learner-owned spec versions (vers lines 2,3,..;
  rg=0, vg=0); detection uses only generic snapshot
  equality on learner-owned procedure outputs; history
  and outcome live in L.
- K7 DETERMINISM: 3/3 runs byte-identical stdout;
  stderr empty.
- K8 TOOLCHAIN: safebin active for every command;
  `which python3` and `which python` return nothing;
  zero forbidden-executable invocations; all
  computation pure Zag; shell only for znc/binary/git/
  assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).

## 4. Verdict mapping (frozen)

- K1-K9 PASS: BUILD-PASS (mechanism). The composer has
  a halting vocabulary beyond output-stability:
  oscillation is recognized as a distinct outcome
  (halt=osc, period, reported orbit), period-2 and
  period-3 both detected, convergent control intact.
  This is the follow-up C451 asked for.
- K1 FAIL (cap fires, or halt != osc, on O0/O1):
  MECHANISM-FAIL. The detector does not fire on a
  provably repeating trajectory. Diagnose the trace;
  do not promote.
- K2 FAIL (orbit missing a phase, agree=0, close=0):
  REPORT-FAIL. The report is a phase artifact.
- K3 FAIL (O2 not period-3): PARTIAL. Period-2
  established; the k=3 generalization fails. Characterize.
- K4 FAIL: REGRESSION. The additive delta broke
  convergence. Suspend the oscillation claim until the
  regression is understood.
- K5 FAIL: VOID for the additivity claim.
- K6 FAIL: RESEARCHER CONTAMINATION. VOID.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 5. What this establishes (and does not)

Establishes: whether a period-detection halting
vocabulary in learner-owned state lets the system
recognize oscillation as a distinct outcome. Predicted:
yes for period 2 and 3: early halt with halt=osc,
period, and the full orbit reported; the convergent
control is untouched. The orbit-set agreement gives the
reported oscillation an independent generic
confirmation that cap parity cannot satisfy.

Does not establish: learner-invented oscillation
detection (the detector is generic machinery, Section
2.2 boundary); aperiodic/divergent trajectories (cap
still the only answer); periods > 3 (KMAX=3 frozen);
whether the learner can learn FROM the recorded outcome
(the outcome persists in L; no feedback is attempted);
scaling beyond the tested sizes.

## 6. Build plan

Files (pure Zag), prefix `c7_`, in
`docs/lab/research-lead/overnight-20260928/cogops_period/`:
- `c7_base.zag`: byte-identical copy of c6_base.zag
  (cp + cmp).
- `c7_learn.zag`: c6_learn.zag bytes + additive
  period-detection section (Section 2.3); additivity
  verified by head -c + cmp.
- `c7_world.zag`: c6_world.zag + world E, ret_ep_pat
  ids 9-12, vfy_ep_chain id 7, mk_goal820_E2
  (environment extensions only).
- `c7_main.zag`: driver stages S1A,S1B,S2,S3,S4,S5,S6,
  S7,S8 and SUMMARY-PD; do_query_pd with halt/period
  in the Q line; oracle_attractor; orbit_agree;
  probe_close; dump_osc. No world literals.
- `c7_build.sh`: assemble + compile with the pinned
  safebin znc.

Zag-defect workarounds honored (per AGENTS.md): get32/
set32 only; no _zag_print for dynamic content (single
B buffer + o_ helpers); no `!(A && B)` in while
conditions; if-nesting at most 2 in new code;
_zag_malloc as *u8 threaded via z_alloc; no []u8 as
*u8 casts.

## 7. Stages and frozen predictions

S1A RET-LEARN (world A): eps 0-3 (ids 0,1,2,3);
specialize_ret(0,3).
LSTATE-RET nrel=2 ids=601,602 cnts=16,16
prov=0,0,3,56 rev=1.

S1B VFY-LEARN (world A): eps 4-7 (ids 0,1,2,3);
specialize_vfy(4,7).
LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16
prov=1,4,7,56 rev=1.

S2 OSC-LEARN (world D): eps 8,9,10 (ids 6,7,8),
ep 11 (id 2); specialize_ret(8,11).
LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3
prov=0,8,11,61 rev=2.
vfy ep 12 (id 6); specialize_vfy(12,12).
LSTATE-VFY nrel=4 ids=601,602,603,608 cnts=16,16,16,2
prov=1,12,12,61 rev=2.

S3 OSC-SELFLOOP (world D, period-aware composer):
goal 818. TOPO placed=3/3 stall=0. Plan [1,2,0].
Q id=O0 goal=818 st=2 vers=2,3,2 halt=osc period=2
ans=13:2,1,662,1,662,1,611,1,661,1,661,1,611
agree=1 cs=31 cg=183 passes=3.
OSC-STATE m=3 halt=1 period=2 passes=3.
plans_built=1, trials=6.

S4 OSC-2NODE (world D, period-aware composer):
goal 819. TOPO placed=1/4 stall=1 (fallback [0,1,2,3]).
Q id=O1 goal=819 st=2 vers=2,3,2,3 halt=osc period=2
ans=17:2,1,611,1,662,1,661,1,662,1,611,1,661,1,662,1,661
agree=1 cs=40 cg=183 passes=4.
OSC-STATE m=4 halt=1 period=2 passes=4.
plans_built=2.

S5 OSC3-LEARN (world E): setup_worldE; eps 13,14,15,16
(ids 9,10,11,12), ep 17 (id 2); specialize_ret(13,17).
LSTATE-RET nrel=4 ids=601,602,606,612 cnts=16,16,0,4
prov=0,13,17,63 rev=3.
vfy ep 18 (id 7); specialize_vfy(18,18).
LSTATE-VFY nrel=5 ids=601,602,603,608,613
cnts=16,16,16,0,3 prov=1,18,18,63 rev=3.
Then goal 820. TOPO placed=3/3 stall=0. Plan [1,2,0].
Q id=O2 goal=820 st=2 vers=2,3,2 halt=osc period=3
ans=19:3,1,672,1,672,1,611,1,673,1,673,1,611,1,671,1,671,1,611
agree=1 cs=44 cg=252 passes=4.
OSC-STATE m=4 halt=1 period=3 passes=4.
plans_built=3.

S6 CYCLE-LEARN-C (world C): eps 19,20 (ids 4,5),
ep 21 (id 2); specialize_ret(19,21).
LSTATE-RET nrel=5 ids=601,602,606,612,604
cnts=16,16,0,0,8 prov=0,19,21,72 rev=4.
vfy ep 22 (id 4); specialize_vfy(22,22).
LSTATE-VFY nrel=6 ids=601,602,603,608,613,605
cnts=16,16,16,0,0,8 prov=1,22,22,72 rev=4.

S7 CONV-SELFLOOP (world C, period-aware composer):
goal 816. TOPO placed=3/3 stall=0. Plan [1,2,0].
Q id=C0 goal=816 st=2 vers=2,3,2 halt=conv period=0
ans=6:1,618,1,618,1,611 agree=1 cs=136 cg=720 passes=9.
OSC-STATE m=4 halt=0 period=0 passes=9.
plans_built=4.

S8 PROBES (worlds D/E/C, generic instruments):
PROBE close goal=818 cyc=2:661,662 close=1
PROBE close goal=819 cyc=2:661,662 close=1
PROBE close goal=820 cyc=3:671,672,673 close=1
PROBE fixpoint fix=618 next=618 stable=1

SUMMARY-PD: agree=4 plans_built=4 plans_loaded=0
trials=6 declines=0 cs=251 cg=1338 rs=23 rg=0 vs=22
vg=0 oschalts=3 convhalts=1.

## 8. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md
(Step 0 guard), c7_base.zag (= c6_base.zag,
cmp-verified), c7_learn.zag (c6 bytes + additive
period section, prefix-verified), c7_world.zag,
c7_main.zag, c7_build.sh, c7_full.zag (assembled;
exactly one `fn main`), c7_bin, c7_compile.txt,
c7_run1/2/3.txt (+ .err), REPORT.md.
