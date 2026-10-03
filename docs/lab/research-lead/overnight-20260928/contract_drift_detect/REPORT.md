# REPORT: Contract Drift Detection (CDRIFT)

Verdict: **CONTRACT-DRIFT-DETECT-COMPLETE**. All 9 frozen kill bars pass,
3/3 deterministic runs byte identical. Pure Zag, zero forbidden
executables. Local only, never pushed.

## What was built

A learner that holds a TYPED CONTRACT it commits to and acts on, detects
contract staleness from its own verification failures, and triggers
contract revision autonomously.

- Contract: CONTRACT_TY=7 with (C_SLOT, C_THRESH). Promise: the world
  yields success when acting on (s[C_SLOT] >= C_THRESH).
- Monitor (inside c_verify, learner side): each unlabeled query produces
  a commitment (c_act) and an observed world consequence. Mismatch =
  verification failure. 3 consecutive failures latch CONTRACT_REVISE_REQ
  (offset 505). Threshold 3 is a frozen generic parameter.
- Revision: x_maybe_revise (standing driver heartbeat) revises iff the
  learner latched the request and the experimental parameter
  REVISION_ENABLED=1. Revision re runs the same generic first fit over
  the learner state window [REV_PTR, XN), so only post change data is
  used. No new semantic cases, no modes, no bridges, no handlers.
- Contract vs mask (the tested distinction): a mask is a passive input
  selection filter (ADETECT). A contract is a promise the learner ACTS
  on, with a verifier comparing commitment vs consequence. The world
  change here moves the outcome law from slot 2 to slot 4 while the
  surface stream is unchanged; detection uses verification failures,
  not score distribution surprise.

## Build

`cat learner.zag world.zag driver.zag > cd_full.zag` (17533 bytes),
then `znc cd_full.zag -o cd_bin`. Build exit 0; only the zagd
unavailable warning. 3 runs, sha256
`2c7fbb4c28f18c54ae83910b660bbafbae326266dd7eceb39bb3e8871fb33683`
identical across all three (KB7).

## Evidence (from cd_run1.txt, verified stdout bytes)

Arm A (drift, revision enabled):
- Initial fit: slot=2 t=2 err=0 revptr=4 (matches PREREG hand derivation).
- Phase 1 (world 0): correct=8/8, req=0.
- Phase 2 queries 1..3 under the stale contract: pred/act mismatches
  (1/0, 0/1, 0/1), fail run 1,2,3, req latches at q=3, firstq=3.
- Revision: slot=4 t=2, revcount=1, fiterr=0, olderr=2 (old contract has
  2 errors on the new window, so the fit used only post change data).
- Phase 2 remainder: 9/9 correct under the new contract (phase total 9/12).
- Phase 3 (fresh world 1 queries): correct=8/8, req=0.

Arm B (no drift control): fit (2,2); 20/20 correct; req=0; revcount=0;
contract unchanged.

Arm C (drift, revision disabled): phase 1 8/8; phase 2 correct=3/12 with
the req latched at q=3 and held (revcount=0, contract stays (2,2)).

## Kill bars (frozen in PREREG.md, commit da2d1b51d)

- KB1 contract works pre change: arm A phase 1 8/8, req=0. PASS.
- KB2 drift breaks the stale contract: arm C phase 2 3/12, bar <= 5/12. PASS.
- KB3 detection via verification failures: req latched after post change
  query 3, C_FIRST_DETECT_Q=3. PASS.
- KB4 autonomous trigger: revcount A=1, B=0, C=0; driver.zag has no code
  write to offset 505 (only a read in d_req and a comment); the latch
  (learner.zag:143) and the clear after revision (learner.zag:174) are
  the only writes. The driver heartbeat x_maybe_revise is a no op when
  the learner did not request. PASS.
- KB5 revised contract works: arm A phase 3 8/8. PASS.
- KB6 no false triggers: arm B req=0 with 20/20; arm A req=0 after
  phase 3. PASS.
- KB7 determinism: 3/3 byte identical stdout (sha256 above). PASS.
- KB8 contract values: pre change (2,2), post revision (4,2), arm C
  final (2,2). PASS.
- KB9 revision window purity: fiterr=0 on the new window, olderr=2 >= 1.
  PASS.

## Disclosed boundaries (not claimed)

The driver schedules teaching episodes, the initial fit, the world
change timing, and the x_maybe_revise heartbeat after each batch. The
learner does not choose when to teach or when baselines are recorded,
and a change that leaves verification outcomes unchanged is out of
scope. The revision decision, the detection latency, and the revised
contract values are the learner's.

## Toolchain guard

Step 0 executed before any work: PATH=$HOME/safebin, `which python3
python` returned nothing. No forbidden executable invoked at any point.
Shell used only for safebin setup, concatenation, znc, binary runs,
sha256sum, greps, and git. All research logic in pure Zag via the pinned
znc, following the AGENTS.md miscompile workarounds (u8 backed state
with get32/set32, single buffer emit with ob helpers, one raw syscall
flush, no `as *i32` slice construction in functions).

## Files

`docs/lab/research-lead/overnight-20260928/contract_drift_detect/`:
NAMECHECK.md, PREREG.md, REPORT.md, learner.zag, world.zag, driver.zag,
cd_full.zag, cd_bin, cd_compile.txt, cd_run1.txt, cd_run2.txt,
cd_run3.txt.

## Follow ups worth recording

- The monitor threshold (3 consecutive) is a frozen generic parameter,
  but a k of n variant would be more robust to intermittent noise; a
  future worker could test detection under noisy consequences.
- Detection here is reactive (3 failures must occur). Proactive
  contract verification (the learner probing its own contract before
  committing) is the natural next frontier.
- The contract type is minimal (slot, threshold). Richer typed
  contracts (H1 style, between mechanisms) with the same
  verify then revise loop would test compositional contract drift.
