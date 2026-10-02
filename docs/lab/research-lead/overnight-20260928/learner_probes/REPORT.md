# REPORT: Learner-Chosen Probe Inputs (LPROBE)

Verdict: **LEARNER-PROBE-COMPLETE**. All 8 frozen kill bars pass,
3/3 deterministic runs byte identical. Pure Zag, zero forbidden
executables. Local only, never pushed.

## What was built

A learner that not only decides WHEN to probe its typed contract
(PROACTIVE-PROBE-COMPLETE) but now CHOOSES WHICH inputs to probe from
an open pool. The driver supplies the world: 10 candidate probe inputs
(input bytes only; outcome labels stay with the world). The learner
scores every candidate from its own state and selects 3:

- Contract: CONTRACT_TY=7 with (C_SLOT, C_THRESH). Promise: the world
  yields success when acting on (s[C_SLOT] >= C_THRESH).
- x_score (learner side, new): score = (3 - |s[C_SLOT]-C_THRESH|) * 10
  + minHamming(candidate, taught episodes in [0, XN)). Boundary
  proximity to the held contract dominates; novelty against the
  learner's own experience breaks ties. No labels consulted.
- x_choose_probes (learner side, new): selects PROBE_BUDGET=3 pool
  indices, score descending, pool index ascending tiebreak; writes
  C_CHOICE0..2 (offsets 585, 589, 593) and C_CHOSEN_N (offset 583).
  The driver only READS these to learn which inputs to present.
- Everything else (x_teach, x_fit_contract, c_verify, x_probe_begin,
  x_probe_end, x_maybe_revise, c_commit) is unchanged from PPROBE.
- No modes, no bridges, no handlers. CHOICE_ENABLED is a driver set
  experimental parameter for the fixed-probe control arm, same
  standing as PROBE_ENABLED in PPROBE.

## Build

`cat learner.zag world.zag driver.zag > lp_full.zag` (26958 bytes),
then `znc lp_full.zag -o lp_bin`. Build exit 0; only the benign zagd
unavailable warning. 3 runs, sha256
`aa170b854142d52f5a86803c160d8624d3b0fbc36715f92ef1582c27824081bc`
identical across all three (KB7).

One compiler defect was hit and worked around during the build: seven
deep nested `if`s combining `!=`/`<=` with a call in the innermost
condition produced a spurious E0204 on the following `let`
(bisected; each construct compiles alone). Fixed by hoisting
sub-conditions into flag lets and keeping nesting at 3. Recorded in
~/AGENTS.md as the third pinned-znc defect. No kill bar or frozen
value was touched by the workaround.

## Evidence (from lp_run1.txt, verified stdout bytes)

Arm A (learner-chosen, threshold drift 2->3):
- Initial fit: slot=2 t=2 err=0 revptr=4 (matches PREREG hand
  derivation).
- Round 1 (world 0): probeneed=1, learner chooses [2,0,1] with scores
  32/31/31 (exactly the frozen hand derivation), 3 probes pass,
  hsok=1, rev=0, unprobed=0.
- Round 2 (world 1): probeneed=1; learner chooses [2,0,1] again (same
  experience, same stale contract); all 3 fail (pred=1 act=0, run
  1/2/3, req latches, firstq=2). Driver observes req=1 BEFORE
  x_maybe_revise.
- Revision: slot=2 t=3, revcount=1, fiterr=0, olderr=1 (old contract
  errs once on the new window, so the fit used only post change data).
- High-stakes commitment after revision: pred=0 act=0 ok, hsfails=0.
- Event order: seq=3/4/5, so C_PROBE_SEQ < C_REVISE_SEQ <
  C_COMMIT_SEQ. C_UNPROBED=0. Every failure happened at probe stakes.

Arm B (learner-chosen, no drift control): fit (2,2); 3 rounds, each
with probeneed=1 and the identical learner choice [2,0,1] from
identical state. Totals: probes=9, pfails=0, rev=0, hs=3, hsfails=0,
unprobed=0, firstq=-1, req=0. Choice is stable and bounded: exactly
one 3-probe round per commitment, nothing triggered when stable.

Arm C (fixed interior probes {P4,P6,P8}, drift, choice disabled):
probeneed=1 both rounds; all fixed probes pass in world 1 (pred=0
act=0, the drift is missed); req=0, no revision; HS2 under the stale
(2,2) contract: pred=1 act=0 FAIL, hsfails=1. Final contract stays
(2,2). Same budget, same proactive timing as arm A; the only
difference is WHO chose the probes. The learner's boundary probes
catch the drift; the fixed interior probes do not.

## Kill bars (frozen in PREREG.md, commit 247e85cb4)

- KB1 learner chooses: arm A C_CHOICE == [2,0,1], C_CHOSEN_N==3,
  matching the frozen hand-derived expectation. PASS.
- KB2 chosen probes informative: arm A round 2 probefails==3,
  req==1 before revision, firstq==2, 3<4<5 ordering, unprobed==0,
  arm A hsfails==0. PASS.
- KB3 uninformative avoided: chosen set exactly {2,0,1}: no
  duplicates, budget exactly 3, all six interior distractors (pool
  indices 4..9) unchosen; every chosen probe has boundary distance
  |s2-2|==0 and minHamming>=1 (nothing already experienced). PASS.
- KB4 value of choice: arm A round 2 hsok==1; arm C probefails==0,
  req==0, final contract (2,2), hsok2==0 (hsfails==1). PASS.
- KB5 bounded budget when stable: arm B probes==9, pfails==0, rev==0,
  hs==3, hsfails==0, unprobed==0, choice [2,0,1] all 3 rounds. PASS.
- KB6 contract values: arm A (2,2) then (2,3); arm C final (2,2);
  arm B final (2,2). PASS.
- KB7 determinism: 3/3 byte identical stdout, sha256 equal (shell
  verified). PASS.
- KB8 revision window purity and no false triggers: arm A fiterr==0,
  olderr==1 (>=1); arm B firstq==-1, final req==0. PASS.

Binary verdict line: `VERDICT LEARNER-PROBE-COMPLETE`.

## Governance

- Toolchain guard executed at worker startup; `which python3 python`
  returned nothing; PATH=$HOME/safebin for all work. No forbidden
  executable invoked at any point. One near miss, disclosed: while
  composing a shell line during compiler bisection I typed a `python3`
  token; it did not resolve under the safebin PATH (verified with
  `command -v`: empty), so no Python process was ever spawned. No
  wave logic, analysis, or output involved Python in any form.
- PREREG.md committed alone (commit 247e85cb4) before any
  implementation file existed. No kill bar moved after results.
- Static audit: driver.zag contains no assignment to st[505]
  (C_REV_REQ), st[562] (PROBE_FRESH), st[583] (C_CHOSEN_N), or
  st[585]/st[589]/st[593] (C_CHOICE0..2); all are learner written
  (c_verify latch, x_probe_end / x_maybe_revise / c_commit freshness,
  x_choose_probes selection). The driver reads the choice offsets
  only to learn which pool inputs to present.
- World 0 training reuses the CDRIFT/PPROBE frozen episodes. World 1
  is new in this wave (threshold drift s2>=2 to s2>=3), re-frozen in
  this wave's PREREG.md section 2; the tested mechanism
  (learner-chosen probe inputs) is new.
- Honest boundary (from the prereg): the driver still schedules
  teaching, the world change, pool presentation (inputs only), and
  query presentation. Not claimed: learner-invented pools,
  experience-set probe budgets, or learner-set probe timing beyond
  x_probe_begin.
- Nothing pushed; commits local on tnn-native-lab only.
