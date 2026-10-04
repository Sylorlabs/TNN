# PREREG: Learner-Chosen Probe Inputs (LPROBE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/learner_probes/` only.
Worker: Learner-Chosen Probe Worker (subagent, 2026-10-02).
Parent mandate: test LEARNER-CHOSEN probe inputs from an open world.

## 1. What is being tested

PROACTIVE-PROBE-COMPLETE showed a learner can decide WHEN to probe its
typed contract (x_probe_begin from learner state) before a high-stakes
commitment. Its disclosed boundary: the driver still supplied fixed
probe input sets. Open question: can the LEARNER CHOOSE WHICH inputs
to probe, from an open set, using its own uncertainty, so that the
probes it picks are the informative ones?

Here the driver provides the world: an OPEN POOL of 10 candidate probe
inputs (input bytes only; outcome labels are held by the world and
never shown to the learner before it chooses). The learner holds the
same typed contract as PPROBE (CONTRACT_TY=7, (C_SLOT, C_THRESH):
outcome == (s[C_SLOT] >= C_THRESH)). When x_probe_begin says a probe
round is needed, the learner computes a score for every pool candidate
from its own state and selects PROBE_BUDGET=3 of them.

New frozen learner machinery (disclosed):
- x_score(st, s0..s5): score = (3 - |s[C_SLOT] - C_THRESH|) * 10 +
  minHamming(candidate, taught episodes in [0, XN)). Boundary
  proximity to the held contract dominates; novelty against the
  learner's own experience breaks ties. Computed from learner state
  only. No labels consulted. Returns -9999 if no contract held.
- x_choose_probes(st, pool, n): selects PROBE_BUDGET=3 pool indices,
  score descending, pool index ascending tiebreak. Writes the chosen
  indices into C_CHOICE0..2 (offsets 585, 589, 593, i32) and
  C_CHOSEN_N (offset 583, u8). No-op (returns 0, writes nothing)
  unless CHOICE_ENABLED==1 and CONTRACT_SET==1. The pool is
  driver-supplied world surface (inputs only); the SELECTION is
  learner computed.

State additions (one u8 buffer, 1024 bytes; offsets 0..570 as PPROBE):
- 583: C_CHOSEN_N (u8)
- 584: CHOICE_ENABLED (u8; driver set experimental parameter; 1 arms
  A/B, 0 arm C)
- 585..588: C_CHOICE0 (i32, pool index, -1 init)
- 589..592: C_CHOICE1 (i32, -1 init)
- 593..596: C_CHOICE2 (i32, -1 init)

All other functions (x_teach, x_fit_contract, sv, c_act, c_verify,
x_probe_begin, x_probe_end, x_maybe_revise, c_commit, c_phase_reset,
ob helpers, z_alloc, get32/set32) are UNCHANGED from PPROBE. Novelty
is measured against all taught episodes [0, XN) (what the learner has
experienced); the revision fit window stays [REV_PTR, XN) as in
PPROBE.

Disclosed boundary of "learner-chosen": the driver still schedules
teaching episodes (labeled), schedules the world change, presents the
open pool (inputs only) when the learner requests a probe, and presents
the high-stakes queries. The learner does NOT invent the pool, does not
set its probe budget from experience (frozen PROBE_BUDGET=3), and does
not set probe timing (x_probe_begin from PPROBE). What this build DOES
claim: the learner selects which inputs to probe from the open pool,
the selection is computed from learner state alone, the chosen probes
are informative (catch threshold drift the fixed interior probes miss),
and uninformative probes are avoided.

## 2. Frozen world data

World 0 (label = s2>=2). Training episodes reuse the CDRIFT/PPROBE
frozen set: E1 (0,0,3,0,0,0,1), E2 (1,1,0,1,0,0,0),
E3 (0,0,2,0,1,0,1), E4 (2,3,1,0,0,1,0). Frozen fit: (2,2), 0 errors
(hand verified in CDRIFT PREREG.md section 3).

World 1 (label = s2>=3; THRESHOLD DRIFT, new in this wave). Training:
E1p (0,0,3,0,0,0,1), E2p (1,0,1,1,0,1,0), E3p (0,0,2,0,1,0,0),
E4p (0,3,3,0,0,0,1). Hand fit check (scan slot 0..5, threshold 1..3,
first strictly fewer errors wins): slot 0 values (0,1,0,0) best err 2
(thr 2); slot 1 values (0,0,0,3) best err 1 (thr 1); slot 2 values
(3,1,2,3): thr1 err 2, thr2 err 1, thr3 err 0, first 0-error candidate.
Frozen fit: (2,3), 0 errors. Old contract (2,2) errors on the new
window: exactly 1 (E3p: s2=2>=2 predicts 1 vs label 0).

Open probe pool (10 candidates; driver presents inputs, world holds
labels). preds under stale (2,2); acts under world 0 (s2>=2) and
world 1 (s2>=3):
P0 (0,0,2,0,0,0): pred 1, w0 act 1, w1 act 0. FAIL under stale in w1.
P1 (1,1,2,1,0,0): pred 1, w0 act 1, w1 act 0. FAIL under stale in w1.
P2 (0,3,2,0,1,1): pred 1, w0 act 1, w1 act 0. FAIL under stale in w1.
P3 (1,0,1,0,0,0): pred 0, w0 act 0, w1 act 0. ok.
P4 (0,0,0,0,0,0): pred 0, w0 act 0, w1 act 0. ok.
P5 (2,3,3,0,0,1): pred 1, w0 act 1, w1 act 1. ok.
P6 (1,1,0,1,1,0): pred 0, w0 act 0, w1 act 0. ok.
P7 (0,0,3,1,0,0): pred 1, w0 act 1, w1 act 1. ok.
P8 (3,0,0,0,0,1): pred 0, w0 act 0, w1 act 0. ok.
P9 (1,2,3,0,1,0): pred 1, w0 act 1, w1 act 1. ok.

Hand score check with stale contract (2,2) and experience E1..E4
(min Hamming distances: P0 1, P1 1, P2 2, P3 2, P4 1, P5 1, P6 1,
P7 1, P8 3, P9 3; boundary |s2-2|: P0 0, P1 0, P2 0, P3 1, P4 2,
P5 1, P6 2, P7 1, P8 2, P9 1):
scores: P2 32, P0 31, P1 31, P9 23, P3 22, P5 21, P7 21, P8 13,
P4 11, P6 11. Frozen chosen set (score desc, index asc): [2, 0, 1].
All three are boundary probes (s2=2, distance 0) and all three fail
under the stale contract in world 1. The six interior distractors
(P4..P9, indices 4..9) are all unchosen.

High-stakes queries:
HS1 (world 0): (0,0,3,0,0,0): pred 1, act 1. ok under (2,2).
HS2 (world 1): (0,0,2,0,0,0): under stale (2,2): pred 1, act 0. FAIL.
Under revised (2,3): pred 0, act 0. ok.
HSB0 (world 0): (0,0,3,0,0,0): 1/1. ok.
HSB1 (world 0): (1,1,0,0,0,0): 0/0. ok.
HSB2 (world 0): (0,0,2,1,0,0): 1/1. ok.

Arm C fixed set (driver-supplied, CHOICE_ENABLED=0): {P4, P6, P8}
(all s2=0, interior). All pass under stale (2,2) in world 1
(pred 0, act 0): the drift is missed.

Frozen constants: PROBE_BUDGET=3, PROBE_FAIL_THRESHOLD=2 (from PPROBE,
generic, not tuned to any world).

## 3. Arms

Arm A (learner-chosen, drift, CHOICE_ENABLED=1, PROBE_ENABLED=1,
REVISION_ENABLED=1): teach E1..E4, x_fit_contract giving (2,2).
Round 1 (world 0): x_probe_begin=1, learner chooses [2,0,1], 3 probes
pass, x_probe_end(0), x_maybe_revise (no-op), c_commit HS1 (ok).
World change (driver scheduled, disclosed). Round 2 (world 1):
x_probe_begin=1, learner chooses [2,0,1] (same experience, same stale
contract), 3 probes FAIL (run 1, run 2 latches REQ, FIRST_DETECT_Q=2),
driver reads REQ=1 before revision, x_probe_end(3), teach E1p..E4p,
x_maybe_revise (revision to (2,3) BEFORE the commitment), c_commit
HS2 (ok).

Arm B (learner-chosen, no drift control, CHOICE_ENABLED=1,
PROBE_ENABLED=1, REVISION_ENABLED=1): teach E1..E4, fit (2,2), then
3 rounds in world 0. Each round: x_probe_begin=1, learner chooses
[2,0,1] (identical every round: same experience, same contract),
3 probes pass, x_probe_end(0), x_maybe_revise (no-op), c_commit
HSB0..HSB2 (ok).

Arm C (fixed uninformative probes, drift, CHOICE_ENABLED=0,
PROBE_ENABLED=1, REVISION_ENABLED=1): teach E1..E4, fit (2,2).
Round 1 (world 0): x_probe_begin=1, driver-fixed probes {P4,P6,P8}
pass, x_probe_end(0), c_commit HS1 (ok). World change. Round 2
(world 1): x_probe_begin=1, fixed probes pass (drift missed),
x_probe_end(0), x_maybe_revise (no-op: no failures), c_commit HS2
under stale (2,2) (FAIL). Contract stays (2,2).

## 4. Frozen kill bars

KB1 learner chooses: arm A C_CHOICE0..2 == [2, 0, 1] and C_CHOSEN_N==3
(the frozen hand-derived expectation). The driver never writes the
choice offsets (static audit); the selection is learner computed.
KB2 chosen probes are informative: arm A round 2 probefails==3,
REQ==1 observed before x_maybe_revise, FIRST_DETECT_Q==2,
C_PROBE_SEQ < C_REVISE_SEQ < C_COMMIT_SEQ, C_UNPROBED==0, and arm A
total high-stakes fails==0 (drift caught at probe stakes).
KB3 uninformative probes avoided: arm A chosen set is exactly {2,0,1}:
no duplicates, budget exactly 3, all six interior distractors
(indices 4..9) unchosen, every chosen probe has boundary distance
|s2-2|==0 and minHamming>=1 (nothing already experienced).
KB4 the value of choice: arm A round 2 hsok==1; arm C probefails==0,
req==0, final contract (2,2), hsok2==0 (hsfails==1). Same budget,
same proactive timing; fixed interior probes miss the drift the
learner's boundary probes catch.
KB5 bounded budget when stable: arm B probes==9, probefails==0,
revcount==0, hscommits==3, hsfails==0, unprobed==0, and the learner's
choice is [2,0,1] in all 3 rounds (identical choice from identical
state).
KB6 contract values: arm A pre change (2,2), post revision (2,3);
arm C final (2,2); arm B final (2,2).
KB7 determinism: 3 full binary runs produce byte identical stdout
(sha256 equal, shell verified).
KB8 revision window purity and no false triggers: arm A C_FIT_ERR==0
and C_OLDERR_ON_NEW>=1; arm B FIRST_DETECT_Q==-1 and final REQ==0.

Verdict rule: KB1..KB8 all pass gives LEARNER-PROBE-COMPLETE. Any bar
fails: the verdict names the failed bar, no completion claim. A
forbidden interpreter invocation at any point is PROCESS-FAIL and the
wave result stays exploratory.

## 5. Build and run plan (post prereg)

Files: learner.zag (PPROBE base + x_score, x_choose_probes, new
offsets), world.zag (frozen data above), driver.zag (arms, bars,
single raw syscall flush). Build:
`cat learner.zag world.zag driver.zag > lp_full.zag`, then
`znc lp_full.zag -o lp_bin`. Run 3x, sha256sum compare. Write
REPORT.md. Commit with explicit pathspecs.
