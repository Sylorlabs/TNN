# REPORT: COGOPS-OSCILLATORY (follow-up to COGOPS-CYCLES C442)

Date: 2026-10-03. Worker: COGOPS-OSCILLATORY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_oscillatory/`
Prereg: commit d683e1ae6 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed), plus transparent
pre-implementation correction 9c46ce2c7 (rs/vs 50/63 to 43/53;
no implementation existed). No amendments after implementation
began; errata below are post-execution corrections, not prereg
changes. Implementation commit follows this report.

## Verdict: INFORMATIVE-FAIL (mechanism). The C442 generalization handles convergence only; oscillation is not composed.

The experiment ran two period-2 oscillatory goals through the
byte-identical C442 composer (change-driven iterated execution
to quiescence, frozen 16-pass cap), executed by the
learner-owned spec procedures (id 2 / id 3) that the learner
built from oscillation-workload episodes. What happened:

- Both oscillatory goals terminated: the 16-pass cap fired
  (passes=16 on both). No hang, no crash, no divergence to
  infinity. Totality holds; the cap is real totality
  insurance, and this is the first battery where it actually
  fires.
- Quiescence was never reached. A period-2 cycle changes every
  need's output record every pass, so the change-driven
  iteration cannot halt by its own halting criterion. The
  halting vocabulary (output-stability) is blind to
  oscillation.
- The emitted answers are deterministic phase artifacts of
  the cap parity, not composed answers. The self-loop goal
  emitted the even phase ([1,662]); the 2-node goal emitted
  records that DISAGREE across the cycle edge (need1
  [1,661] verified while need2 [1,662] already produced):
  the 1-step lag signature of a mid-oscillation capture. No
  converged semantics can produce that.
- The stability probe proves the captured phases are not
  fixpoints: RETRIEVE [606,662] = [661] and
  RETRIEVE [606,661] = [662] (period2=1). Whatever phase the
  cap captures is unstable under one more application.
- The convergent control in the same binary (goal 816, world
  C) reproduces C442 exactly: passes=9, quiescence, fixpoint
  618, stable=1 under re-application. Same composer, same
  learner-owned procedures, same bindings: convergence is
  handled, oscillation is not. The variable is the workload
  dynamics, not the machinery.

The composer cannot recognize or report oscillation: the
capped answer is emitted in the normal format (st=2, records,
versions) with no oscillation flag, indistinguishable in form
from a converged answer. A downstream consumer reading
ans=6:1,662,1,662,1,611 would have no way to know it is a
phase artifact. That is the honest boundary: change-driven
iteration to quiescence composes convergent cycles; for
oscillatory cycles it terminates without composing.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3 passes=16 and S4 passes=16 (cap fires; quiescence unreachable) | O0 passes=16; O1 passes=16 | PASS |
| K2 | O0 ans=6:1,662,1,662,1,611; O1 ans=8:1,611,1,661,1,662,1,661 (phase artifacts incl. 1-step lag) | exact match on both | PASS |
| K3 | S5 period2=1 (661->662->661); S8 stable=1 (618->618) | PROBE osc s1=661 s2=662 s3=661 period2=1; PROBE fixpoint fix=618 next=618 stable=1 | PASS |
| K4 | c6_learn.zag / c6_base.zag byte-identical to c5 files; no new composer functions | cmp identical on both | PASS |
| K5 | zero literals in c6_learn.zag, c6_main.zag (7 ids); spec versions execute the oscillation; BIND 801->0, 802->1 | word-boundary grep empty in both (2 comment violations caught and fixed pre-build); vers 2,3,2 and 2,3,2,3; BIND as predicted | PASS |
| K6 | S7 reproduces C442 C0: passes=9, ans=6:1,618,1,618,1,611, agree=1, cs=136, cg=720 | exact match | PASS |
| K7 | 3/3 byte-identical stdout, stderr empty | sha256 a7f107bf x3; .err 0 bytes | PASS |
| K8 | safebin, no python, pure Zag | verified; one near-miss disclosed below, zero executions | PASS |
| K9 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Per-query detail (frozen predictions in PREREG Section 7):
- O0: st=2, vers=2,3,2, ans=6:1,662,1,662,1,611, agree=1
  (vacuous parity, preregistered), cs=96, cg=1098, passes=16
- O1: st=2, vers=2,3,2,3, ans=8:1,611,1,661,1,662,1,661,
  agree=0 (predicted), cs=124, cg=1220, passes=16
- C0: st=2, vers=2,3,2, ans=6:1,618,1,618,1,611, agree=1,
  cs=136, cg=720, passes=9
- SUMMARY-OSC: agree=2 plans_built=3 plans_loaded=0 trials=6
  declines=0 cs=232 cg=1818 rs=43 rg=0 vs=55 vg=0
  (vs=55 vs the predicted 53: see erratum E1; every other
  number exact)

Learner-state evidence (all six LSTATE lines exact):
- S1A: LSTATE-RET nrel=2 ids=601,602 cnts=16,16
  prov=0,0,3,56 rev=1
- S1B: LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16
  prov=1,4,7,56 rev=1
- S2 ret: LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3
  prov=0,8,11,61 rev=2
- S2 vfy: LSTATE-VFY nrel=4 ids=601,602,603,608
  cnts=16,16,16,2 prov=1,12,12,61 rev=2
- S6 ret: LSTATE-RET nrel=4 ids=601,602,606,604
  cnts=16,16,0,8 prov=0,13,15,72 rev=3
- S6 vfy: LSTATE-VFY nrel=5 ids=601,602,603,608,605
  cnts=16,16,16,0,8 prov=1,16,16,72 rev=3
- BIND after S3: 801->fam0 (ok0=1,f1=1,f2=1),
  802->fam1 (f0=1,ok1=1,f2=1); trials=6
- TOPO probes: 818 placed=3/3 stall=0; 819 placed=1/4
  stall=1 (fallback [0,1,2,3]); 816 placed=3/3 stall=0

## Errata (transparent; prereg NOT silently amended)

E1 (counter semantics, caught by testing): the frozen
prediction said vs=53; observed vs=55. Hand-trace says 53
vfy_spec INVOCATIONS (O0: 16; O1: 15+15; C0: 7). A scratch
debug binary (throwaway copy in /tmp, lane files untouched)
with per-need invocation counters confirmed exactly
16 / (15,15) / 7 invocations. The +2 is the inherited
counter semantics, byte-identical from C442: the vs counter
increments on version SELECTION (ver==3), which also fires
on O1's two pass-0 empty fan-in execs (need1, need3), where
nsub=0 means vfy_spec is never invoked. cs (the
check counter, the efficiency-relevant one) is unaffected
and matched exactly (96/124/136). This is the direct analog
of C442's erratum E3: a hand-computation gap in a counter,
behavior as designed. The kill bars do not involve vs.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin exported
per invocation; setup_safebin.sh run at startup,
SAFEBIN-READY, 36 tools, no python); `which python3` /
`which python` return nothing before and after; znc
2026.07.0-dev (pinned
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). All
computation pure Zag; shell only for znc/binary/git/
assembly/byte-verification.

Near-miss (zero execution): during the vs investigation the
worker reflexively typed `python3 -c` in a shell command;
python3 does not resolve in the safebin PATH, so nothing
executed (verified: no output, and the subsequent echo
confirmed). No forbidden executable was invoked at any
point. K8 PASS.

One debug detour used a throwaway scratch binary in /tmp
(since removed from the lane; never committed); no Python
was involved at any point.

## Evidence detail

Oscillation, not convergence (K1/K2): O0's self-loop plan
[1:801:0] [2:802:1] [0:801:0] iterated RETRIEVE 16 times
(661->662->661...), VERIFY tracking each phase, and halted
only because pass reached 16. O1's 2-node plan
[0:801:0] [1:802:1] [2:801:0] [3:802:1] (TOPO placed=1/4,
stall=1, fallback order) oscillated from pass 1 after a
pass-0 startup transient (need2's first output made need1
and need3 emit [0], correctly treated as unchanged from the
empty record by out_eq_snap, so no spurious dirtying). The
final records disagree across the cycle edge (need1
[1,661] vs need2 [1,662]): the fingerprint of a
mid-oscillation capture, impossible under converged
semantics.

Not a fixpoint (K3): the S5 probe chains three generic
RETRIEVEs from the goal record's [rel,obj] with no literals:
661->662->661, period2=1. The S8 control chains the
convergent walk to its fixpoint and re-applies once:
618->618, stable=1.

Oracle (dis)agreement, preregistered: O0's agree=1 is
cap-parity correspondence (the 16-guarded all-generic walk
lands on the same even phase), explicitly vacuous per the
prereg. O1's agree=0 is predicted: the oracle's guarded
walk reads need1 at the guard-final phase [1,662] while the
executor's need1 lags one step ([1,661]). The divergence
documents that no "intended answer" exists for oscillation.

Learner-not-researcher (K5): the 7 new identifiers occur
only in c6_world.zag (environment) and as runtime values in
output. The oscillation executes under learner-owned spec
versions selected from episode-built coverage (vers lines
2,3,2 and 2,3,2,3; rg=0, vg=0: no generic fallback took a
single composed step). Trial bindings 801->RETRIEVE,
802->VERIFY serve the oscillatory self-loop, the
oscillatory 2-cycle, and the convergent self-loop alike.

Composer identity (K4): the file the oscillation ran on is
byte-identical to the file that converged in C442. The
boundary probed here is a property of C442's generalization,
not of new code.

## What this establishes (and does not)

Establishes: C442's change-driven iteration handles
convergence only. On a period-2 oscillatory cycle of
learner-owned procedures it preserves totality (the
16-pass cap fires; first battery where the cap actually
fires) but does not compose the oscillation into a
meaningful answer: quiescence is unreachable, the emitted
records are deterministic phase artifacts (with a 1-step
lag across the 2-node cycle), and the captured phase is
provably not a fixpoint. The same composer converges
(passes=9) where a fixpoint exists, isolating workload
dynamics as the variable. The capped answer is emitted in
the normal format with no oscillation flag: the composer
cannot recognize or report oscillation.

Does not establish: divergent (growing, non-periodic)
cycles; 3+ node oscillatory cycles; a repaired halting
vocabulary (no redesign attempted); whether the learner
could learn to detect oscillation (the probes are
researcher instruments, not learner-owned); scaling beyond
the tested sizes; behavior under a different cap parity
(the cap is frozen at 16 by design).

## Toolchain

- safebin active for every command (PATH=$HOME/safebin
  exported per invocation; setup_safebin.sh run at startup,
  SAFEBIN-READY, no python); `which python3` / `which
  python` return nothing; znc 2026.07.0-dev (pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- All computation pure Zag; shell only for znc/binary/git/
  assembly/byte-verification.
- Git writes via /usr/bin/git absolute path (safebin git
  symlink has the known EPERM-on-write defect). Explicit
  pathspecs on every add/commit; no other lane touched;
  nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_oscillatory/`:
PREREG.md (frozen, commits d683e1ae6 + 9c46ce2c7),
NAMECHECK.md (Step 0), c6_base.zag (= c5_base.zag,
cmp-verified), c6_learn.zag (= c5_learn.zag, cmp-verified),
c6_world.zag, c6_main.zag, c6_build.sh, c6_full.zag
(assembled; exactly one `fn main`), c6_bin,
c6_compile.txt, c6_run1/2/3.txt (sha256
a7f107bfa4f8450f495c5f1fc0ea49cba9c02ef28b11c8164738b9db86764641)
+ .err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Halting vocabulary beyond output-stability: the
   mechanism needs a way to recognize non-convergence
   (period detection, oscillation flag) in learner-owned
   state before oscillatory composition can be claimed.
   The S5 probe pattern (chained re-application) is a
   candidate instrument, but it must be learner-owned to
   count.
2. Halt-on-verifier-failure: C442's other open boundary.
   O1's pass-0 transient ([0] records treated as unchanged)
   is adjacent territory worth a dedicated test.
3. 3+ node oscillatory cycles and divergent (growing)
   cycles: untested.
4. The vs counter semantics (E1): consider documenting the
   version-selection vs invocation distinction in the
   shared composer notes, since it now confused two
   consecutive workers' hand computations.
