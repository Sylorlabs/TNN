# REPORT: Proactive Contract Self-Probing (PPROBE)

Verdict: **PROACTIVE-PROBE-COMPLETE**. All 8 frozen kill bars pass,
3/3 deterministic runs byte identical. Pure Zag, zero forbidden
executables. Local only, never pushed.

## What was built

A learner that holds a TYPED CONTRACT it commits to and acts on, and
PROACTIVELY probes that contract on low-stakes tests BEFORE committing
to high-stakes decisions. This is the follow-on to
CONTRACT-DRIFT-DETECT-COMPLETE, whose disclosed boundary was reactive
detection (failures must occur before revision). Here no high-stakes
failure ever occurs in the proactive arm: drift is caught at probe
stakes, revision happens before the commitment, and the commitment
succeeds.

- Contract: CONTRACT_TY=7 with (C_SLOT, C_THRESH). Promise: the world
  yields success when acting on (s[C_SLOT] >= C_THRESH).
- Proactive decision (x_probe_begin, learner side): probe iff probing
  is enabled, a contract is held, and PROBE_FRESH==0 (contract not
  verified since the last commitment or revision). Records the probe
  event in the learner SEQ counter. A second call without an
  intervening commitment returns 0: no re-probe loops.
- Probe: 3 low-stakes queries per round (frozen PROBES_PER_ROUND=3).
  Verdicts come from the learner's own c_verify against observed world
  consequences. Probe failures feed the consecutive-failure monitor
  with a frozen threshold of 2 (a cheap test warrants a cheap
  trigger; generic parameter, not tuned to any world).
- Revision before commitment: when probes latch C_REV_REQ, the driver
  teaches fresh episodes and calls the standing x_maybe_revise
  heartbeat; the learner revises from its window [REV_PTR, XN) and the
  high-stakes commitment is made only after. SEQ ordering
  (probe < revise < commit) is checkable in learner state, and
  C_UNPROBED counts any commitment made without a fresh probe while
  probing is enabled.
- No modes, no bridges, no handlers. PROBE_ENABLED is a driver set
  experimental parameter for the reactive control arm, same standing
  as REVISION_ENABLED in CDRIFT.

## Build

`cat learner.zag world.zag driver.zag > pp_full.zag` (20985 bytes),
then `znc pp_full.zag -o pp_bin`. Build exit 0; only the benign zagd
unavailable warning. 3 runs, sha256
`d85920ac18c9ee216257b5a128f0fba16b2fc39394aa787550001317a9a34beb`
identical across all three (KB7).

## Evidence (from pp_run1.txt, verified stdout bytes)

Arm A (proactive, drift):
- Initial fit: slot=2 t=2 err=0 revptr=4 (matches PREREG hand derivation).
- Round 1 (world 0): probeneed=1, reprobe=0, 3 probes pass, hsok=1,
  revcount=0, unprobed=0.
- Round 2 (world 1): probeneed=1; probe q1 pred=1 act=0 FAIL (run 1);
  q2 pred=0 act=1 FAIL (run 2, req latches, firstq=2); q3 ok (run
  resets, latch persists). Driver observes req=1 BEFORE x_maybe_revise.
- Revision: slot=4 t=2, revcount=1, fiterr=0, olderr=2 (old contract has
  2 errors on the new window, so the fit used only post change data).
- High-stakes commitment after revision: pred=1 act=1 ok, hsfails=0.
- Event order: seq=3/4/5, so C_PROBE_SEQ < C_REVISE_SEQ <
  C_COMMIT_SEQ. C_UNPROBED=0. Arm A total high-stakes fails=0: every
  failure happened at probe stakes.

Arm B (proactive, no drift control): fit (2,2); 3 rounds, each with
probeneed=1, 3 passing probes, one successful commitment. Totals:
probes=9, pfails=0, revcount=0, hs=3, hsfails=0, unprobed=0,
firstq=-1, req=0. Contract unchanged at (2,2). Probing is bounded
(exactly one probe round per commitment) and triggers nothing when the
world is stable.

Arm C (reactive control, drift, probing disabled): probeneed=0 both
rounds. Round 1 commitment ok. Round 2 commitment under the stale
contract: pred=0 act=1 FAIL, hsfails=1, req=0 (single failure below
threshold, no revision). Final contract stays (2,2). This is the cost
the proactive arm avoided: without probing, the drift causes exactly
the high-stakes failure proactive probing prevented.

## Kill bars (frozen in PREREG.md, commit 06b649a5f)

- KB1 contract works pre change: arm A round 1 probeneed=1, reprobe=0,
  probefails=0, hsok=1, revcount=0. PASS.
- KB2 proactive probe catches drift before high-stakes failure: arm A
  round 2 probeneed=1, probefails=2, req=1 observed before revision,
  firstq=2, arm A high-stakes fails=0. PASS.
- KB3 revision happens before commitment: arm A 3 < 4 < 5 on
  (PROBE_SEQ, REVISE_SEQ, COMMIT_SEQ), unprobed=0. PASS.
- KB4 high-stakes succeeds while the control fails: arm A round 2
  hsok=1; arm C round 2 hsok=0 (hsfails=1). PASS.
- KB5 no unnecessary probes when stable: arm B probes=9, pfails=0,
  rev=0, hs=3, hsfails=0, unprobed=0. PASS.
- KB6 contract values: arm A (2,2) then (4,2); arm C final (2,2). PASS.
- KB7 determinism: 3/3 byte identical stdout, sha256 equal (shell
  verified). PASS.
- KB8 revision window purity and no false triggers: arm A fiterr=0,
  olderr=2; arm B firstq=-1, final req=0. PASS.

Binary verdict line: `VERDICT PROACTIVE-PROBE-COMPLETE`.

## Governance

- Toolchain guard executed at worker startup; `which python3 python`
  returned nothing; PATH=$HOME/safebin for all work. No forbidden
  executable invoked at any point.
- PREREG.md committed alone (commit 06b649a5f) before any
  implementation file existed. No kill bar moved after results.
- Static audit: driver.zag contains no code assignment to st[505]
  (C_REV_REQ) or st[562] (PROBE_FRESH); both are learner written
  (c_verify latch, x_probe_end / x_maybe_revise / c_commit freshness).
- Training episodes reuse the CDRIFT frozen sets, re-frozen in this
  wave's PREREG.md section 3; the tested mechanism is new.
- Honest boundary (from the prereg): the driver still schedules
  teaching, the world change, probe input sets on learner request, and
  query presentation. Not claimed: learner-chosen probe inputs from an
  open world, experience-set probe budgets, or detection of drift that
  leaves every probe outcome unchanged.
- Nothing pushed; commits local on tnn-native-lab only.
