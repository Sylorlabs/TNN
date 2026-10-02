# PREREG: Contract Drift Detection (CDRIFT)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/contract_drift_detect/` only.
Worker: Contract Drift Detection Worker (subagent, 2026-10-02).
Parent mandate: test autonomous detection of CONTRACT drift (not mask drift).

## 1. What is being tested

AUTONOMOUS-DETECT-COMPLETE showed a learner can detect MASK drift via
surprise in its own decision score stream. A mask is a passive input
selection filter. A CONTRACT is different: a typed promise the learner
commits to and acts on. Here the contract has type CONTRACT_TY with
fields (SLOT_INDEX, THRESHOLD, OUTCOME_LAW): "if I act on
(s[slot] >= T), the world yields success". The learner uses the contract
to make commitments; the world returns consequences (success or
failure). The world change makes the promised relation FALSE (the
outcome law moves from slot 2 to slot 4) while the surface stream is
unchanged. The learner has no labels in deployment, so it cannot measure
accuracy. What it CAN observe is verification outcomes: its committed
prediction vs the observed world consequence. Persistent verification
failures latch a learner written revision request; a standing driver
heartbeat calls x_maybe_revise; the learner revises the contract from its
new experience window using the same generic fit machinery.

Disclosed boundary of "autonomous": the driver still supplies the
standing opportunity (it calls x_maybe_revise after each batch, like a
heartbeat), schedules teaching episodes (labeled), calls the initial
x_fit_contract, and schedules the world change. The DECISION to revise
(CONTRACT_REVISE_REQ written ONLY by the monitor inside c_verify, never
by the driver) and the revised contract VALUES (first fit over the
learner state window [REV_PTR, XN)) are the learner's. What this build
does NOT claim: the learner choosing when to record baselines or when
to teach, detecting a change that leaves its verification outcomes
unchanged, or the world change being hidden from the driver.

## 2. Frozen learner machinery (disclosed)

- State: one u8 buffer, 1024 bytes, zeroed at arm start.
  0: XN (episode count, max 32)
  1: REV_PTR (first not yet consolidated episode index)
  2: REVISION_ENABLED (driver set experimental parameter; 1 arm A/B, 0 arm C)
  7: C_Q (queries this phase; driver resets at phase start, disclosed scheduling)
  8 + n*8: episode n: id, s0..s5, label (8 bytes each; 8..263)
  500: CONTRACT_TY (7 when a contract is held)
  501: C_SLOT (informative slot index 0..5)
  502: C_THRESH (threshold 1..3)
  503: CONTRACT_SET (1 = contract established)
  504: C_FAIL_RUN (consecutive verification failures)
  505: C_REV_REQ (1 = learner requests revision; written ONLY by c_verify)
  506..509: C_REV_COUNT i32 (revisions performed)
  510..513: C_FIRST_DETECT_Q i32 (phase query index of first latch, -1 init)
  514..517: C_CORRECT i32
  518..521: C_TOTAL i32
  522..525: C_FIT_ERR i32 (fit errors of current contract on its fit window)
  530..533: C_OLDERR_ON_NEW i32 (old contract errors on the new window, traced at revision)
- x_teach(st, id, s0..s5, label): append episode.
- x_fit_contract(st): first fit over episodes [REV_PTR, XN). Candidate
  scan order frozen: slot 0..5, threshold 1..3. Errors = count of
  episodes where (s[slot] >= T) != label. Keep the first candidate with
  strictly fewer errors (scan order tiebreak). On a fit: set
  CONTRACT_TY=7, C_SLOT, C_THRESH, CONTRACT_SET=1, C_FIT_ERR=best errors,
  REV_PTR=XN. Empty window: no change.
- c_act(st, s0..s5): if CONTRACT_SET: (s[C_SLOT] >= C_THRESH) else 0.
- c_verify(st, s0..s5, actual): the monitor. C_Q++; pred=c_act;
  ok=(pred==actual); C_TOTAL++; if ok C_CORRECT++. If CONTRACT_SET:
  ok resets C_FAIL_RUN to 0, else C_FAIL_RUN++; if C_FAIL_RUN >= 3 then
  C_REV_REQ=1 (latch; if C_FIRST_DETECT_Q<0 record C_Q). Threshold 3 is
  a frozen generic parameter, not tuned to any world. Returns ok.
- x_maybe_revise(st): iff C_REV_REQ==1 and REVISION_ENABLED==1:
  compute old contract errors on [REV_PTR, XN) into C_OLDERR_ON_NEW,
  call x_fit_contract (fits the NEW window only), C_REV_COUNT++,
  C_REV_REQ=0, C_FAIL_RUN=0. Otherwise no op.
- c_phase_reset(st): C_Q=0, C_FAIL_RUN=0 (driver called at phase start).

## 3. Frozen world data

World 0 outcome law (driver side, learner never sees): label = (s2 >= 2).
World 1 outcome law: label = (s4 >= 2).

Training episodes, world 0 (id, s0..s5, label):
E1: (1, 0,0,3,0,0,0, 1)
E2: (2, 1,1,0,1,0,0, 0)
E3: (3, 0,0,2,0,1,0, 1)
E4: (4, 2,3,1,0,0,1, 0)
Frozen fit result: (C_SLOT, C_THRESH) = (2,2), 0 errors. Hand verified:
slot 0 fails at E1 for all T; slot 1 T=1 fails at E2, T=2 fails at E4,
T=3 fails at E4; slot 2 T=1 fails at E4; slot 2 T=2 fits all four with
0 errors; scan order stops tiebreaks at the first zero error holder.
The binary trace must print fit (2,2).

Training episodes, world 1:
E1p: (11, 0,0,0,0,3,0, 1)
E2p: (12, 1,0,1,1,0,1, 0)
E3p: (13, 0,0,0,0,2,0, 1)
E4p: (14, 0,3,0,0,1,0, 0)
Frozen fit result: (4,2), 0 errors. Hand verified: slot 0 fails at E1p;
slot 1 T=1 fails at E2p, T=2 fails at E4p, T=3 fails at E4p; slot 2 fails
at E3p; slot 3 fails at E3p; slot 4 T=1 fails at E4p; slot 4 T=2 fits all
four with 0 errors. Old contract (2,2) has >= 1 error on this window
(E1p: s2=0 predicts 0, label 1).

Phase 1 queries, world 0, 8 queries (label = s2>=2), all correct under (2,2):
P1 (0,0,0,0,0,0) P2 (1,1,2,0,0,0) P3 (0,0,3,1,2,0) P4 (2,1,1,0,3,1)
P5 (0,2,2,0,0,0) P6 (3,0,0,0,1,0) P7 (1,1,3,0,0,2) P8 (0,0,1,2,0,0)

Arm A phase 2 queries, world 1, 12 queries. Q1..Q3 under stale (2,2):
Q1 (0,0,3,0,0,0) pred 1 act 0 FAIL (run 1)
Q2 (1,1,0,0,3,0) pred 0 act 1 FAIL (run 2)
Q3 (0,0,1,0,2,1) pred 0 act 1 FAIL (run 3, REQ latches)
Revision happens here (teach E1p..E4p, x_maybe_revise). Q4..Q12 under (4,2):
Q4 (2,0,3,1,0,0) pred 0 act 0 ok
Q5 (0,1,2,0,1,0) pred 0 act 0 ok
Q6 (1,0,0,0,2,0) pred 1 act 1 ok
Q7 (0,0,3,0,3,1) pred 1 act 1 ok
Q8 (2,2,1,1,0,0) pred 0 act 0 ok
Q9 (0,0,2,0,0,2) pred 0 act 0 ok
Q10 (1,3,0,2,1,0) pred 0 act 0 ok
Q11 (0,0,3,0,1,0) pred 0 act 0 ok
Q12 (0,1,1,1,3,0) pred 1 act 1 ok

Arm A phase 3 queries, world 1, 8 queries, all correct under (4,2):
R1 (1,0,0,0,3,0) R2 (0,2,1,0,0,1) R3 (0,0,2,1,2,0) R4 (2,0,0,0,1,0)
R5 (0,3,3,0,0,0) R6 (1,1,1,1,3,1) R7 (0,0,0,0,2,2) R8 (3,2,2,0,0,0)

Arm C phase 2 queries, world 1, 12 queries, all under stale (2,2):
Q1..Q3 as in arm A. Then:
Q4 (2,0,3,1,0,0) pred 1 act 0 FAIL
Q5 (0,1,2,0,1,0) pred 1 act 0 FAIL
Q6 (1,0,0,0,2,0) pred 0 act 1 FAIL
Q7 (0,0,3,0,3,1) pred 1 act 1 ok
Q8 (2,2,1,1,0,0) pred 0 act 0 ok
Q9 (0,0,2,0,0,2) pred 1 act 0 FAIL
Q10 (1,3,0,2,1,0) pred 0 act 0 ok
Q11 (0,0,3,0,1,0) pred 1 act 0 FAIL
Q12 (0,1,1,1,3,0) pred 0 act 1 FAIL
Correct: 3/12. REQ latches at Q3; revision disabled so the contract stays (2,2).

Arm B queries, world 0, 20 queries (label = s2>=2), all correct under (2,2):
B1 (0,0,0,0,0,0) B2 (1,1,2,0,0,0) B3 (0,0,3,1,2,0) B4 (2,1,1,0,3,1)
B5 (0,2,2,0,0,0) B6 (3,0,0,0,1,0) B7 (1,1,3,0,0,2) B8 (0,0,1,2,0,0)
B9 (0,0,2,0,1,1) B10 (1,0,0,3,0,0) B11 (2,2,3,0,0,0) B12 (0,1,1,1,2,0)
B13 (3,3,2,0,0,1) B14 (0,0,0,0,3,0) B15 (1,2,3,2,1,0) B16 (0,0,1,0,0,3)
B17 (2,0,2,1,1,0) B18 (0,3,0,0,2,1) B19 (1,1,2,3,0,0) B20 (0,0,0,1,0,2)

## 4. Arms

Arm A (drift, revision enabled): teach E1..E4, x_fit_contract, 8x phase 1
queries, world change, phase reset, 3x phase 2 queries (detection),
teach E1p..E4p, x_maybe_revise (revision), 9x phase 2 queries, 8x phase 3
queries. x_maybe_revise also called after every batch as a standing
heartbeat (no op when REQ=0).
Arm B (no drift control): teach E1..E4, x_fit_contract, 20x queries world 0,
x_maybe_revise heartbeats. No world change.
Arm C (drift, revision disabled): like arm A through phase 1, world change,
12x phase 2 queries (stale contract), heartbeats (no op; disabled).
No re teach in arm C.

## 5. Frozen kill bars

KB1 contract works pre change: arm A phase 1 correct == 8 of 8, and
C_REV_REQ == 0 after phase 1.
KB2 drift breaks the stale contract: arm C phase 2 correct <= 5 of 12.
KB3 detection via verification failures: arm A CONTRACT_REVISE_REQ == 1
latched after phase 2 query 3, and C_FIRST_DETECT_Q == 3.
KB4 autonomous trigger: arm A C_REV_COUNT == 1; arm B C_REV_COUNT == 0;
arm C C_REV_COUNT == 0; driver.zag contains no write to offset 505
(static grep audit), so the request is learner written.
KB5 revised contract works: arm A phase 3 correct == 8 of 8.
KB6 no false triggers: arm B C_REV_REQ == 0 after 20 queries with 20 of 20
correct; arm A C_REV_REQ == 0 after phase 3.
KB7 determinism: 3 full binary runs produce byte identical stdout
(sha256 equal, shell verified).
KB8 contract values: arm A pre change (C_SLOT, C_THRESH) == (2,2);
post revision == (4,2); arm C final == (2,2).
KB9 revision window purity: arm A C_FIT_ERR == 0 after revision and
C_OLDERR_ON_NEW >= 1 (old contract errors on the new window, so the fit
used only post change data).

Verdict rule: KB1..KB9 all pass gives CONTRACT-DRIFT-DETECT-COMPLETE.
Any bar fails: verdict names the failed bar, no completion claim. A
forbidden interpreter invocation at any point is PROCESS-FAIL and the
wave result stays exploratory.

## 6. Build and run plan (post prereg)

Files: learner.zag (state, x_teach, x_fit_contract, c_act, c_verify,
x_maybe_revise, c_phase_reset, ob helpers, z_alloc, get32/set32),
world.zag (frozen data above), driver.zag (arms, bars, single raw syscall
flush). Build: `cat learner.zag world.zag driver.zag > cd_full.zag`,
then `znc cd_full.zag -o cd_bin`. Run 3x, sha256sum compare. Write
REPORT.md. Commit with explicit pathspecs.
