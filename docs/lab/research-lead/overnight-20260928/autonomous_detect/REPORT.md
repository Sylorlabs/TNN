# REPORT: Autonomous Change Detection (ADETECT)

Worker: Autonomous Change Detection Worker (subagent, 2026-10-02).
Prereg: `autonomous_detect/PREREG.md` (frozen at 75ddab9be, committed
alone before any implementation existed; no amendments).
Build: `cat learner.zag world.zag driver.zag > ad_full.zag`
(1210 lines), then `znc ad_full.zag -o ad_bin`. Build exit 0. Only
diagnostics: the benign zagd-unavailable notice, three A0101
off-by-one heuristic warnings in x_revise_masks/x_recall (analyzer
cannot prove the bounds; indices provably in range, same as the
spec_mask_revision build), no errors.

## Verdict: AUTONOMOUS-DETECT-COMPLETE (7/7 kill bars PASS, 3/3 deterministic)

## Bar results (from ad_run1/2/3.txt, byte-identical)

- K-AD-1 baseline-recorded: set=1 mean=9 spread=4 req=0. PASS.
- K-AD-2 stable-no-trigger: Z-STABLE 4/4, req=0, revs=0, k1=48,
  k2=12. PASS. The stable world (phase-5 batch, ids 41..44) produced
  zero surprising decisions and the standing x_maybe_revise call was
  a no-op. No false trigger.
- K-AD-3 change-detected: Z-TRAIN-EVAL 4/8 (external performance
  drop from 4/4 to the always-skip baseline), DET_REVISE_REQ=1 set
  by the learner at the 3rd surprising decision (id 23), masks still
  48/12, revs=0, Z-NOREVISE 2/4. PASS.
- K-AD-4 autonomous-revision: revs=1, req=0, k1=12, k2=48,
  revptr=24. PASS. The driver called x_maybe_revise; the learner
  decided to revise and ran the generic re-consolidation itself.
- K-AD-5 recovery: Z-CHANGE 4/4 with M1 reused (n=1, t=6,
  prog=1,0,1,0,...); every Z-CHANGE line shows a 2-reading replayed
  sequence (5,8 / 3,2 / 7,6 / 2,3) with surp=0. PASS.
- K-AD-6 provenance: phase-1 consolidation left masks 48/12
  (stability), ADAPT-STAT spec=360 in ARM-CHANGE, grep audit on
  learner.zag zero hits on all 14 frozen patterns. PASS.
- K-AD-7 determinism: ad_run1/2/3.txt sha256 identical:
  33a7b29f15194c2d8a031642f7e80276c15d4ccc38968c51a69cecdf92a055c6.
  PASS.

No falsifier fired (F-NO-BASE, F-FALSE-TRIGGER, F-NO-DROP,
F-NO-DETECT, F-NO-REVISE, F-NO-RECOVER, F-CONTROL-BROKEN,
F-SPURIOUS, F-OP-EXPAND, F-AUDIT, F-NONDET, F-PYTHON all silent).

## What the trace shows

ARM-STABLE: baseline froze at mean=9 spread=4 from phase-1 test
scores [13,5,13,5]. Phase-5 decisions (s=13,5,13,5) each deviate
exactly 4, never strictly exceeding spread=4: run stays 0, req stays
0, x_maybe_revise returns 0 twice. Z-STABLE 4/4.

ARM-CHANGE: phase-2 train evaluation with stale masks replays (0,0)
on all 8 episodes; every score s=0 deviates 9 > 4 (surprising); at
the 3rd consecutive surprise the learner sets DET_REVISE_REQ=1
(visible on the ZT id=23 line: surp=1 req=1). The driver never
writes offset 420. x_maybe_revise then revises autonomously: masks
swap 48<->12 to 12/48, REV_PTR 16->24, revs=1, req cleared.
Phase-2 test: Z-CHANGE 4/4, post-revision scores back in baseline
range (no second trigger, run=0).

ARM-NOREVISE: identical detection (req=1, run=12 by end of test),
but the driver withholds x_maybe_revise: masks stay 48/12, revs=0,
Z-NOREVISE 2/4. Causal control: detection without the revision
action does not recover performance, so the recovery in ARM-CHANGE
is attributable to the learner-triggered revision.

## Disclosed boundary of "autonomous"

The driver supplies the standing opportunity (calls x_maybe_revise
after each batch, like a heartbeat) and schedules baseline
recording. The DETECTION (DET_REVISE_REQ written only by learner
monitor logic in decide()) and the REVISION (x_revise_masks on
learner state) are the learner's. In spec_mask_revision the trigger
was driver-scheduled consolidation; here the driver only offers the
call and the learner decides. A world change that leaves the
learner's score distribution unchanged would not be detected; the
monitor is distributional surprise in exec(M) scores, the
learner-observable proxy for a world change (the learner has no
labels in phase 2). The driver measures the true accuracy drop
(4/4 -> 4/8) externally.

## Residual footprint

Researcher-supplied generic machinery, frozen in prereg: op basis
{CPY,ADD,SUB,MAX,MIN}, 2-register machine, greedy construction,
variance mask criterion, consolidation pointer, SPECIALIZE standing
rule, driver-scheduled consolidation timing, driver-scheduled
baseline recording, the standing x_maybe_revise heartbeat, and the
trigger threshold 3. 0 modes, 0 bridges, 0 handlers, 0 new semantic
cases. Pure Zag; zero Python invocations.

## Non-claims

- One world family (kind-tagged aggregation with a slot move). No
  generality claim beyond the three demonstrated arms.
- The hidden world rules were builder-designed, not
  adversary-designed. Sealed-adversary generality is open future
  work.
- Does not claim Micah's full 12-criterion L3 bar.
- Paper untouched. Nothing pushed. Commits local on tnn-native-lab.

## Artifacts

`docs/lab/research-lead/overnight-20260928/autonomous_detect/`:
NAMECHECK.md, PREREG.md, REPORT.md (this file), learner.zag,
world.zag, driver.zag, ad_full.zag, ad_bin, ad_compile.txt,
ad_run1.txt, ad_run2.txt, ad_run3.txt.
