# PREREG: Proactive Contract Self-Probing (PPROBE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/proactive_probe/` only.
Worker: Proactive Probing Worker (subagent, 2026-10-02).
Parent mandate: test PROACTIVE contract self-probing (learner tests
contract BEFORE committing to high-stakes decisions).

## 1. What is being tested

CONTRACT-DRIFT-DETECT-COMPLETE showed a learner can detect contract
drift reactively: verification failures must occur before a revision
request latches. The disclosed boundary there: "Detection here is
reactive (3 failures must occur)". Open question: can the learner
PROACTIVELY probe its contract, testing it on low-stakes inputs BEFORE
committing to a high-stakes decision, and revise before the commitment
when the probe fails?

Here the learner holds the same typed contract as CDRIFT
(CONTRACT_TY=7, (C_SLOT, C_THRESH): outcome == (s[C_SLOT] >= C_THRESH)).
New machinery: a learner-side proactive probe policy. Before any
high-stakes commitment, the learner decides from its own state whether
the contract needs a low-stakes test: x_probe_begin returns 1 iff
probing is enabled, a contract is held, and the contract has not been
verified since the last commitment or revision (PROBE_FRESH==0). The
driver then supplies a small fixed set of low-stakes probe inputs; the
learner verifies each via c_verify. Probe failures feed the same
consecutive-failure monitor, with a frozen probe threshold of 2 (a
cheap test warrants a cheap trigger; threshold 2 is a frozen generic
parameter, not tuned to any world). If the probe latches a revision
request, x_maybe_revise revises the contract from the learner's new
experience window BEFORE the high-stakes commitment is made. A learner
event sequence counter (SEQ) records probe, revision, and commitment
order so the temporal claim is checkable in learner state.

## 2. Frozen learner machinery (disclosed)

State: one u8 buffer, 1024 bytes. Offsets 0..533 as in CDRIFT, plus:
- 3: PROBE_ENABLED (driver set experimental parameter; 1 arms A/B, 0 arm C)
- 534..537: C_PROBES (low-stakes probes run)
- 538..541: C_PROBE_FAILS
- 542..545: C_HS_COMMITS
- 546..549: C_HS_FAILS
- 550..553: C_PROBE_SEQ (SEQ of last probe round begin, -1 init)
- 554..557: C_REVISE_SEQ (SEQ of last revision, -1 init)
- 558..561: C_COMMIT_SEQ (SEQ of last high-stakes commitment, -1 init)
- 562: PROBE_FRESH (1 = contract verified since last commitment/revision)
- 563..566: SEQ (monotonic event counter, never reset)
- 567..570: C_UNPROBED (high-stakes commitments made without a fresh probe while probing is enabled)

Frozen functions:
- x_teach, x_fit_contract, sv, c_act: unchanged from CDRIFT.
  x_fit_contract scans slot 0..5, threshold 1..3; the first candidate
  with strictly fewer errors wins (scan order tiebreak). No semantic cases.
- c_verify(st, s0..s5, actual, is_probe): as CDRIFT plus stake
  accounting. is_probe=1 increments C_PROBES (and C_PROBE_FAILS on a
  mismatch); is_probe=0 increments C_HS_COMMITS (and C_HS_FAILS on a
  mismatch). Monitor: consecutive verification failures (probe or
  commitment) >= 2 latch C_REV_REQ (offset 505), written ONLY here;
  FIRST_DETECT_Q records C_Q at the first latch.
- x_probe_begin(st): the proactive decision. Returns 0 when
  PROBE_ENABLED==0 or CONTRACT_SET==0 or PROBE_FRESH==1. Else SEQ++,
  C_PROBE_SEQ=SEQ, return 1.
- x_probe_end(st, fails): the driver reports the observed probe round
  failures; the learner owns PROBE_FRESH. fails==0 sets PROBE_FRESH=1;
  otherwise freshness stays 0 (the monitor latches a revision request
  instead of starting a re-probe loop).
- x_maybe_revise(st): as CDRIFT, plus on revision: PROBE_FRESH=1 (a
  fresh fit on new data establishes freshness directly), SEQ++,
  C_REVISE_SEQ=SEQ.
- c_commit(st, s0..s5, actual): SEQ++, C_COMMIT_SEQ=SEQ; when
  PROBE_ENABLED==1 and PROBE_FRESH==0, C_UNPROBED++; verify as a
  high-stakes commitment (is_probe=0); set PROBE_FRESH=0 (a commitment
  consumes freshness, so the next commitment re-probes).
- c_phase_reset(st): C_Q=0, C_FAIL_RUN=0. SEQ is never reset.

Disclosed boundary of "proactive": the driver still supplies the
standing opportunity (x_maybe_revise heartbeat), schedules teaching
episodes (labeled), schedules the world change, supplies the fixed
probe input sets when the learner requests a probe, and presents the
high-stakes queries. The DECISION to probe (x_probe_begin from learner
state), the probe verdicts (c_verify), the revision request latch
(monitor at offset 505, never driver written), the revised contract
VALUES (fit over the learner window [REV_PTR, XN)), and the commitment
action (c_act) are the learner's. What this build does NOT claim: the
learner choosing its own probe inputs from an open world, setting its
probe budget from experience, or detecting drift that leaves every
probe outcome unchanged.

## 3. Frozen world data

Training episodes: the CDRIFT frozen sets, re-frozen here (the tested
mechanism is new; the data is a vehicle).
World 0 (label = s2>=2):
E1 (0,0,3,0,0,0, label 1)
E2 (1,1,0,1,0,0, label 0)
E3 (0,0,2,0,1,0, label 1)
E4 (2,3,1,0,0,1, label 0)
Frozen fit: (2,2), 0 errors (hand verified in CDRIFT PREREG.md section 3).
World 1 (label = s4>=2):
E1p (0,0,0,0,3,0, label 1)
E2p (1,0,1,1,0,1, label 0)
E3p (0,0,0,0,2,0, label 1)
E4p (0,3,0,0,1,0, label 0)
Frozen fit: (4,2), 0 errors (hand verified in CDRIFT PREREG.md section
3). Old contract (2,2) has 2 errors on this window: E1p (s2=0 predicts
0 vs label 1) and E3p (s2=0 predicts 0 vs label 1).

World 0 probe set, 3 probes, all pass under (2,2):
P0 (0,0,2,0,0,0): pred 1, label (s2>=2) 1. ok.
P1 (1,0,0,0,0,0): pred 0, label 0. ok.
P2 (0,0,3,1,0,0): pred 1, label 1. ok.

World 1 probe set, 3 probes; Q0 and Q1 fail under stale (2,2), Q2 passes:
Q0 (0,0,3,0,0,0): pred (s2=3>=2) 1, act (s4=0>=2) 0. FAIL (run 1).
Q1 (1,1,0,0,3,0): pred (s2=0) 0, act (s4=3>=2) 1. FAIL (run 2, REQ latches, FIRST_DETECT_Q=2).
Q2 (2,0,0,0,0,0): pred 0, act 0. ok (run resets; the latch persists).

High-stakes queries:
HS1 (world 0): (0,0,3,0,0,0): pred 1, act 1. ok under (2,2).
HS2 (world 1): (0,0,0,0,3,0): under stale (2,2): pred 0, act 1. FAIL.
Under revised (4,2): pred (s4=3>=2) 1, act 1. ok.
HSB0 (world 0): (0,0,3,0,0,0): 1/1. ok.
HSB1 (world 0): (1,1,0,0,0,0): 0/0. ok.
HSB2 (world 0): (0,0,2,1,0,0): 1/1. ok.

Frozen probe policy constants: PROBES_PER_ROUND=3,
PROBE_FAIL_THRESHOLD=2.

## 4. Arms

Arm A (proactive, drift, REVISION_ENABLED=1, PROBE_ENABLED=1): teach
E1..E4, x_fit_contract giving (2,2). Round 1 (world 0):
x_probe_begin=1, 3 probes pass, x_probe_end(0), x_maybe_revise (no-op),
c_commit HS1 (ok). World change (driver scheduled, disclosed). Round 2
(world 1): x_probe_begin=1, 3 probes (2 fail, REQ latches), driver reads
REQ=1 before revision, x_probe_end(2), teach E1p..E4p, x_maybe_revise
(revision to (4,2) BEFORE the commitment), c_commit HS2 (ok).

Arm B (proactive, no drift control, PROBE_ENABLED=1, REVISION_ENABLED=1):
teach E1..E4, fit (2,2), then 3 rounds in world 0. Each round:
x_probe_begin=1, 3 probes pass, x_probe_end(0), x_maybe_revise (no-op),
c_commit HSB0..HSB2 (ok).

Arm C (reactive control, drift, PROBE_ENABLED=0, REVISION_ENABLED=1):
teach E1..E4, fit (2,2). Round 1 (world 0): x_probe_begin=0 (disabled),
c_commit HS1 (ok). World change. Round 2 (world 1): x_probe_begin=0,
c_commit HS2 under stale (2,2) (FAIL). x_maybe_revise heartbeat
(no-op: 1 failure is below threshold). Contract stays (2,2).

## 5. Frozen kill bars

KB1 contract works pre change: arm A round 1 gives probeneed=1,
reprobe=0, probefails=0, hsok=1, revcount=0.
KB2 proactive probe catches drift before high-stakes failure: arm A
round 2 gives probeneed=1, probefails=2, REQ=1 observed before
x_maybe_revise, FIRST_DETECT_Q=2, arm A total high-stakes fails=0.
KB3 revision happens before commitment: arm A C_PROBE_SEQ <
C_REVISE_SEQ < C_COMMIT_SEQ, and C_UNPROBED=0.
KB4 high-stakes succeeds while the control fails: arm A round 2 hsok=1;
arm C round 2 hsok=0 (high-stakes fails=1).
KB5 no unnecessary probes when stable: arm B probes=9, probefails=0,
revcount=0, hscommits=3, hsfails=0, unprobed=0.
KB6 contract values: arm A pre change (2,2), post revision (4,2); arm C
final (2,2).
KB7 determinism: 3 full binary runs produce byte identical stdout
(sha256 equal, shell verified).
KB8 revision window purity and no false triggers: arm A C_FIT_ERR=0 and
C_OLDERR_ON_NEW>=1; arm B FIRST_DETECT_Q=-1 and final REQ=0.

Verdict rule: KB1..KB8 all pass gives PROACTIVE-PROBE-COMPLETE. Any bar
fails: the verdict names the failed bar, no completion claim. A
forbidden interpreter invocation at any point is PROCESS-FAIL and the
wave result stays exploratory.

## 6. Build and run plan (post prereg)

Files: learner.zag (state, x_teach, x_fit_contract, c_act, c_verify,
x_probe_begin, x_probe_end, x_maybe_revise, c_commit, c_phase_reset, ob
helpers, z_alloc, get32/set32), world.zag (frozen data above),
driver.zag (arms, bars, single raw syscall flush). Build:
`cat learner.zag world.zag driver.zag > pp_full.zag`, then
`znc pp_full.zag -o pp_bin`. Run 3x, sha256sum compare. Write
REPORT.md. Commit with explicit pathspecs.
