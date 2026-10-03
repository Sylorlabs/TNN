# REPORT: COGOPS-PERIOD (follow-up to COGOPS-OSCILLATORY C451)

Date: 2026-10-03. Worker: COGOPS-PERIOD.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_period/`
Prereg: commit 012be9fb9 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). No amendments after
implementation began; notes below are post-execution
clarifications, not prereg changes. Implementation commit follows
this report.

## Verdict: BUILD-PASS (mechanism). The composer recognizes oscillation as a distinct outcome.

The additive period-detection halting vocabulary works as
preregistered. On the two C451 period-2 goals the
period-aware composer halts with halt=osc at passes 3 and 4
(not the 16-pass cap), reporting the full orbit; on the new
period-3 goal it halts with halt=osc, period=3, at pass 4;
the convergent control reproduces C451 byte-exactly
(passes=9, halt=conv). Every frozen numeric prediction in
PREREG Section 7 matched exactly: all 8 LSTATE lines, all 4
Q lines, all 4 OSC-STATE lines, all 4 PROBE lines, and the
SUMMARY-PD line.

What changed vs C451: the halting vocabulary is no longer
output-stability-only. The composer now halts three ways:
CONV (quiescence, period-1 repetition), OSC (period-2 or
period-3 repetition of the global output state, with the
orbit reported), CAP (16-pass totality insurance, never
fired here). The capped phase-artifact emission that C451
documented cannot occur for periodic trajectories anymore:
detection fires as soon as the deterministic trajectory
provably repeats, which is strictly before the cap.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | O0 halt=osc period=2 passes=3; O1 halt=osc period=2 passes=4; full orbit in ans | exact on both; ans carries all phases | PASS |
| K2 | early halt; all-phase orbit; agree=1 by orbit-set; close=1 x3 | passes 3/4/4; orbits complete; agree=1 x3; close=1 x3 | PASS |
| K3 | O2 halt=osc period=3 passes=4; orbit of 3; agree=1 | exact | PASS |
| K4 | C0 = C451 byte-exact (halt=conv passes=9 ans=6:1,618,1,618,1,611 agree=1 cs=136 cg=720) | exact | PASS |
| K5 | c7_base = c6_base (cmp); c7_learn starts with c6 bytes (head -c + cmp); new functions only | verified | PASS |
| K6 | word-boundary grep for 14 new ids in c7_learn.zag, c7_main.zag empty; spec versions execute (rg=0, vg=0) | clean; vers 2,3,..; rg=0 vg=0 | PASS |
| K7 | 3/3 byte-identical stdout; stderr empty | sha256 b3714dc7 x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified every command | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Per-query detail (all exactly as preregistered):
- O0: st=2, vers=2,3,2, halt=osc, period=2,
  ans=13:2,1,662,1,662,1,611,1,661,1,661,1,611,
  agree=1, cs=31, cg=183, passes=3
- O1: st=2, vers=2,3,2,3, halt=osc, period=2,
  ans=17:2,1,611,1,662,1,661,1,662,1,611,1,661,1,662,1,661,
  agree=1, cs=40, cg=183, passes=4
- O2: st=2, vers=2,3,2, halt=osc, period=3,
  ans=19:3,1,672,1,672,1,611,1,673,1,673,1,611,1,671,1,671,1,611,
  agree=1, cs=44, cg=252, passes=4
- C0: st=2, vers=2,3,2, halt=conv, period=0,
  ans=6:1,618,1,618,1,611, agree=1, cs=136, cg=720, passes=9
- SUMMARY-PD: agree=4 plans_built=4 plans_loaded=0 trials=6
  declines=0 cs=251 cg=1338 rs=23 rg=0 vs=22 vg=0
  oschalts=3 convhalts=1

Learner-state evidence (all eight LSTATE lines exact; the
bucket rebuilds on each new world behave as designed:
606 empties on world E, 612 empties on world C):
- S1A: LSTATE-RET nrel=2 ids=601,602 cnts=16,16
  prov=0,0,3,56 rev=1
- S1B: LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16
  prov=1,4,7,56 rev=1
- S2 ret: LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3
  prov=0,8,11,61 rev=2
- S2 vfy: LSTATE-VFY nrel=4 ids=601,602,603,608
  cnts=16,16,16,2 prov=1,12,12,61 rev=2
- S5 ret: LSTATE-RET nrel=4 ids=601,602,606,612
  cnts=16,16,0,4 prov=0,13,17,63 rev=3
- S5 vfy: LSTATE-VFY nrel=5 ids=601,602,603,608,613
  cnts=16,16,16,0,3 prov=1,18,18,63 rev=3
- S6 ret: LSTATE-RET nrel=5 ids=601,602,606,612,604
  cnts=16,16,0,0,8 prov=0,19,21,72 rev=4
- S6 vfy: LSTATE-VFY nrel=6 ids=601,602,603,608,613,605
  cnts=16,16,16,0,0,8 prov=1,22,22,72 rev=4
- BIND after S3: 801->fam0 (ok0=1,f1=1,f2=1),
  802->fam1 (f0=1,ok1=1,f2=1); trials=6
- TOPO probes: 818 placed=3/3 stall=0; 819 placed=1/4
  stall=1 (fallback [0,1,2,3]); 820 placed=3/3 stall=0;
  816 placed=3/3 stall=0
- OSC-STATE (learner-owned outcome records): O0 m=3
  halt=1 period=2 passes=3; O1 m=4 halt=1 period=2
  passes=4; O2 m=4 halt=1 period=3 passes=4; C0 m=4
  halt=0 period=0 passes=9

## Evidence detail

Detection, not cap parity (K1/K2): O0's self-loop plan
iterated RETRIEVE 661->662->661; after pass 2 the global
snapshot repeated sig2==sig0 with sig2!=sig1, and the
composer halted at passes=3 with halt=osc, period=2. O1's
two-node plan oscillated from pass 1 (after the pass-0
startup transient); sig3==sig1 with sig3!=sig2 fired at
passes=4. The reported orbits preserve the 1-step lag
signature across the 2-node cycle edge (need1 [1,662]
while need2 [1,661] in one phase): the orbit is the
honest record of the mid-cycle trajectory, not a
smoothed answer. Because the iteration is deterministic,
the first repeated global state proves the cycle; the
distinctness guards (sig(t)!=sig(t-1), sig(t)!=sig(t-2))
are what keep the convergent fixpoint approach in C0
(sig7==sig6) from misfiring: C0 ran the full 9 passes
to quiescence with halt=conv.

Not a phase artifact (K2, four independent legs): (a) the
halts at passes 3/4/4 precede the cap, so no parity
capture is involved; (b) ans contains every phase of the
orbit; (c) the independent all-generic attractor walk
finds the same cycle lengths (2, 2, 3) and the orbit-set
agreement (phase-independent by construction) gives
agree=1 on all three; (d) the S8 closure probes re-verify
with a fresh generic application that each reported
cycle closes (close=1 x3).

Period-3 generalization (K3): the k=3 rule fired exactly
once, on the 3-cycle workload, at the first provable
repeat (t=3). The k=2 rule correctly did not fire on O2
(sig3!=sig1). The detector is a genuine bounded period-k
vocabulary, not a period-2 special case.

Convergent control (K4): C0 is byte-identical to C451's
C0 in every field (the Q line gains only halt=conv and
period=0). The additive delta did not perturb
convergence: same passes, same answer, same costs.

Learner-not-researcher (K6): the 14 new world/goal
identifiers occur only in c7_world.zag (environment) and
as runtime values in output. The oscillation executes
under learner-owned spec versions (vers 2,3,..;
rg=0, vg=0: no generic fallback took a composed step).
The detector compares only generic snapshots of
learner-owned procedure outputs; the history ring and
the outcome record live in L.

## Implementation notes (transparent; prereg not amended)

N1 (vbuf offsets): PREREG Section 2.3 wrote
vbuf[20]=passes, vbuf[21]=halt, vbuf[22]=period as
shorthand. The implementation uses byte offsets 20, 24,
28 (vbuf is byte-addressed, 32 bytes). Behavior is
exactly as predicted; notation only.

N2 (S8 world reload): the close probes each re-load
their goal's world first (D for the period-2 goals, E
for the period-3 goal, C for the fixpoint probe),
because S8 runs after S7 left world C loaded. The
predicted probe lines are unchanged; without the
reload the attractor correctly reported no cycle
(k=0), which is what caught the ordering issue during
testing. Probe costs never accumulate into cs/cg.

## What this establishes (and does not)

Establishes: a period-detection halting vocabulary in
learner-owned state lets the system recognize
oscillation as a distinct outcome. Period-2 and
period-3 trajectories halt early with halt=osc, the
detected period, and the full orbit reported; the
outcome is recorded in the learner's persistent state
(OSC-STATE lines); convergent behavior is untouched.
The orbit-set agreement gives the reported oscillation
an independent generic confirmation that cap parity
cannot satisfy. This is the follow-up C451 asked for.

Does not establish: learner-invented oscillation
detection. The detector is generic machinery of the
same class as the existing quiescence check
(out_eq_snap); the learner built the oscillating
procedures from episodes but did not invent the
period vocabulary. The outcome record now persists in
L as the substrate for future learning; no feedback
from the outcome into later behavior was attempted.
Also not established: aperiodic/divergent trajectories
(the cap remains the only answer there), periods above
the frozen KMAX=3, or scaling beyond the tested sizes.

## Toolchain

- safebin active for every command (PATH=$HOME/safebin
  exported per invocation; setup_safebin.sh run at
  startup, SAFEBIN-READY, no python); `which python3` /
  `which python` return nothing; znc 2026.07.0-dev
  (pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- All computation pure Zag; shell only for znc/binary/
  git/assembly/byte-verification. Zero forbidden-
  executable invocations (no near-misses this lane).
- Git writes via /usr/bin/git absolute path (safebin
  git symlink has the known EPERM-on-write defect).
  Explicit pathspecs on every add/commit; no other
  lane touched; nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_period/`:
PREREG.md (frozen, commit 012be9fb9), NAMECHECK.md
(Step 0), c7_base.zag (= c6_base.zag, cmp-verified),
c7_learn.zag (c6 bytes + additive period section,
prefix-verified), c7_world.zag (environment: world E,
patterns, goal 820), c7_main.zag, c7_build.sh,
c7_full.zag (assembled; exactly one `fn main`),
c7_bin, c7_compile.txt, c7_run1/2/3.txt (sha256
b3714dc762a9032057300d10c85269fe21a56b9013d2114a4f083d53618ddce5)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Learner-invented oscillation handling: the honest
   next step. The OSC outcome now persists in L; a
   natural experiment is whether the learner can learn
   to predict, avoid, or exploit oscillation from that
   record (e.g. a goal that oscillates gets re-planned
   rather than re-executed blindly).
2. Aperiodic trajectories: the cap is still the only
   vocabulary for non-repeating divergence. A growing-
   state detector (e.g. record-size or value drift in
   the history ring) is the adjacent generalization.
3. Periods above KMAX=3 and multi-need phase offsets
   (the O1 lag signature suggests richer attractors):
   untested.
4. The vs counter semantics (C451 E1) now also cover
   the pd composer; consider the shared composer note
   suggested in C451 follow-up #4.
