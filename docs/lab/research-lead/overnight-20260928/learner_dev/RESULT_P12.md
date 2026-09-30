# RESULT_P12: Developmental-language episode inside the continuing learner (FROZEN EXECUTION)

Date: 2026-09-30 UTC. Worker: Learner Developmental-Language Integration.
Implementation: docs/lab/research-lead/overnight-20260928/learner_dev/dev_learn.zag
Prereg: PREREG_P12.md (commit 980981716, committed alone before implementation).
Kill bar K1: prereg 980981716 is a strict ancestor of the implementation
commit (verified by git merge-base --is-ancestor at commit time).

## Verdict: LEARNER-DEV-PASS

All five frozen prediction groups match 3/3, P1-P11 is byte-identical,
and the positional scope restriction is honored.

## Frozen predictions vs observed (3/3 byte-identical runs, exit 0, zero stderr)

P12-A (installation): installed_now=1 at seen=40 only; 0 at
seen=20,30,50,60,70,80,90,100. OBSERVED: exactly as predicted.
Final OPREC: k=0 trig=1 scope=0 sig=0 sup=12 created=40 active=1,
all other slots inactive. The seen=40 diagnostic shows the DELETION
candidate (w=1, sup=12, mtch=12, div=2, cs=40, cb=28, gate=1).

P12-B (frozen test): TEST_ACC 20/20. F1=1. F2=1. F4=1 (t1_full=3,
t1_abl=0, acc_abl=17/20, negdrop=3). F5=1 (acc>=16, size 3/3).
OBSERVED: exactly as predicted.

P12-C (no regression): lines 1-237 of RUN1.txt (all output through
"STATEHASH P11") are byte-identical to RUN1.txt at dc20745db.
OBSERVED: cmp clean. The only new output is the P12 region
(lines 238-382).

P12-D (persistence): after the 20-item pressure wave, P12_DEV 3/3,
P12_FOUNDATION 8/8, P12_CORR 2/2. OBSERVED: exactly as predicted.
The P12 facts were earned 3x immediately to importance 31 (P9/P11
discipline) and survived the wave; the wave's 125 EVICT lines hit
only low-importance items.

P12-E (determinism): 3/3 byte-identical runs, exit 0, zero stderr.
OBSERVED: sha256 356e2ea769614df4f67294c2d980a3cd284a02ccb6512721f52af10374c28672
all three.

F3 source audit (shell): the OpScope learner section of dev_learn.zag
contains zero string literals, hence zero word literals. The gate
routes on OPREC.trigger_form, a runtime-bound value, unchanged.

Frozen adversary check (regression guard): the R1R4 battery inside the
lifetime installed exactly one operator (trig=1), replicating the
frozen white-box result. No confound installed in the R1R4 battery.

## Positional scope restriction (honored)

The "not" unit in the R1R4 battery always occurs at utterance position
1. Per OPSCOPE-DISPLACEMENT-LOAD-BEARING, the gate's positional
assumption is load-bearing. This result claims ONLY position-contingent
operator installation, not position-general negation learning.

## Family A confound (out of scope, documented)

The Family A mid-utterance confound installs as a DELETION operator
under the verbatim R1R4 gate (GATE-STRESS-FAIL, sealed ebd62fe5). P12
integrates the gate verbatim and does not repair it. Gate repair is the
job of the behavioral-validation redesign (opscope_behav lane). The
Family A battery was not re-run in P12: its outcome is frozen and
sealed, and the gate code is verbatim, so a re-run would add no
information.

## ONE-SYSTEM RULE accounting (new standing directive, recorded per result)

- Cognition source lines added: 1168 (dev_learn.zag 2380 lines vs
  revert_learn.zag 1212 lines). Breakdown: OpScope learner 421 lines
  (verbatim), OpScope world 503 lines (verbatim, minus 5 identical
  utils), P12 helpers 44 lines, P12 episode inline in main ~195 lines,
  provenance comments ~5 lines.
- New hardcoded semantic cases: 0. The gate is verbatim; no new
  semantic case was added to the learner.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 1 episode driver (the P12 block in
  main(); a developmental episode, not a permanent mode).
- Learner-state structures created: the 8400-byte OpScope state slice
  W[2048..10448], a separate subsystem state format inside the one
  32768-byte state. Plus 3 earned facts (920,2,1), (921,2,0),
  (922,2,20) in the stress store.

Capability-source delta: the developmental-language capability
(operator discovery for the R1R4 negation battery) required 1168 new
source lines. This is a LARGE capability-source delta, and it is
architectural debt under the ONE-SYSTEM RULE: P12 achieves integration
(one lifetime, one binary, no resets, no recompilation) by COMPOSITION
of a second subsystem, not by the general architecture learning the
behavior. The standing question "Why can the existing general
architecture not learn this behavior?" is NOT answered by P12; it is
deferred to the compression step.

Honest ceiling: bounded L2. The candidate graphs, the gate, and the
episode driver are researcher-supplied. The "one continuing learner"
goal is approached (one state, one lifetime, developmental episode
persisted as learner state), not claimed.

## Reproduction

Build: src/tools/toolchain/znc_linux_x86_64_abed8aa1 build
dev_learn.zag -o dev_learn_bin (exit 0; warnings are pre-existing
classes in copied code: A0102 in earn_guarded, E0101 in gen_direct /
gen_neg). Run: ./dev_learn_bin > RUN.txt. Expect the sha256 above and
P1-P11 byte-identical to dc20745db RUN1.txt lines 1-237.

## Recommendation: next integration target

The next developmental episode should be chosen for ARCHITECTURAL
COMPRESSION, not for capability breadth. Concretely: the operator
discovery currently living in the 8400-byte OpScope subsystem slice
should be re-expressed in the learner-owned structural workspace
(the stress/DDEs structures), eliminating the independent subsystem
state format. Until that compression happens, each new P-episode adds
~1000 lines and a new state format, which is the subsystem sprawl the
ONE-SYSTEM RULE forbids. The opscope_behav redesign (cross-context
behavioral validation as the admission criterion) should be scored on
whether it moves toward learner-owned structure, not just on whether
it repairs the gate.
