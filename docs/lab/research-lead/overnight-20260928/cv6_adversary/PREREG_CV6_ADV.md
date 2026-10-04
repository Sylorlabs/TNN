# Preregistration: H-CAUSALV6 Red Team (CV6-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any attack fixture is built or run)
**Researcher:** H-CAUSALV6 Red Team (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV6 SURVIVES (commit 807d13042), R6 repair
  (R6a refutation floor, R6b graded re-confirmation, R6c masking check).
**Assumption:** the H-CAUSALV6 claim is false. Attacks below try to kill or
  downgrade it.

## Method

- Attacker uses ONLY the committed `causalv6.zag` blob from 807d13042
  (md5 7d579163a5299c2054e2080df3c3d198, verified byte-identical to the
  working tree file before this prereg). No mechanism edits.
- Attack fixtures are plain `T` observation files + probe files, run with a
  binary compiled from the committed blob. Pure Zag. No Python at any stage.
- Every attack run 3/3; determinism checked by cmp/md5.
- Verdicts: KILL (claim false), DOWNGRADE (claim narrowed), HOLD (attack
  fails, boundary confirmed).

## X-CV6-1: Support-bar vs diversity (R6b drops the R4 guard)

**Theory.** R6b replaces the R4 cause-context diversity check with a pure
support bar (`support > dl_rf`) for re-confirmation of refuted rules. Under
CV5, a refuted rule re-confirming went through the R4 diversity path (no
dl_rf existed), so a positioned confounder repeating in an identical
background state could never re-confirm. R6b re-admits exactly that shape:
a refuted rule re-confirms by repetition alone, with zero context novelty.

**Design.**
- Phase 0: rule R0=(a4,d=2,s2,1) created (dl_cs=(0,0,0)), confirmed via one
  diverse support (R4). R0 ACTIVE, support=2, dl_rf=0.
- Phase 1: adversary refutes R0 with a genuine counter-episode
  (dl_rf=2, support=1, PROVISIONAL).
- Phase 2: two honest re-demonstrations of (a4,d=2,s2,1), BOTH with cause
  context exactly (0,0,0) == dl_cs (no diversity).
- Control fixture (separate): a fresh rule receiving two identical-context
  supports (rf=0 path) must show the frozen R4 behavior:
  `# ... NOT CONFIRMED ... cause context identical to creation; remains
  PROVISIONAL`.

**Kill criteria.**
- DOWNGRADE if: Phase 2 re-confirms R0 (`# delay rule R0 CONFIRMED`,
  final `st=ACT`) on identical-context supports AND the control shows R4
  blocking the same shape (PROVISIONAL). This demonstrates R6b strictly
  weakens the frozen R4 positioned-confounder guard for re-confirmation.
- HOLD if: R6b does not re-confirm, or the control does not show the R4
  block.

## X-CV6-2: Delayed-law intervener (R6c masks immediate laws only)

**Theory.** R6c withholds refutation only when the CURRENT episode action's
learned ACTIVE *immediate* law predicts the observation (`dl_masked` scans
ST_ACT immediate entries). A *delayed* law of another action that fully
explains the observation does not mask. This is the X-CV5-2 failure class
(falsification vs masking) recurring for delayed interveners.

**Design.**
- Phase A: R1=(a4,d=2,s2,1) genuine, ACTIVE (support=2).
- Phase B: R2=(a2,d=1,s2,2) genuine, ACTIVE (support=2, diverse).
- Phase C (trap): a4 at t, a2 at t+1, a1 at t+2 with s2 0->2 (R2's delayed
  effect fires). a1 has no learned law (fresh action), so R6c cannot mask.
- At the trap: R1's refutation check sees cause a4 at t, expects s2=1,
  observes 2. R2 (ACTIVE) fully explains s2=2 via its own learned delayed
  law.

**Kill criteria.**
- DOWNGRADE if: R1 is `# ... REFUTED` at the trap while R2 is ACTIVE in
  the final dump (observation explained by the learner's own delayed law,
  refutation not withheld). C-R6c narrowed to immediate-law interveners.
- HOLD if: R1 is not refuted, or R2 is not ACTIVE at the trap.

Note: the disclosed ST_AMB non-masking boundary is verified by code
inspection (`dl_masked` requires `en_st==ST_ACT`); no fixture is spent on
it in this wave.

## X-CV6-3: Multi-refutation floor escalation (persistent adversary)

**Theory.** R6a sets `dl_rf` to the pre-refutation support on every
refutation, and R6b clears it only on promotion. A persistent adversary
injecting one counter-episode per cycle refutes at the current peak
support, so the floor ratchets up every cycle while the adversary's
per-cycle cost stays 1. Honest recovery cost grows without bound.

**Design.** Repeating cycle after R0=(a4,d=2,s2,1) is ACTIVE (support=2):
- Adversary block (4 eps): X(a3), C_adv(a4, clean cause), G(a3),
  CTR(a1, s2 stays 0) -> REFUTED, floor = peak support.
- Honest recovery: k honest [C,G,E,R,X] blocks until support > floor ->
  CONFIRMED, floor cleared.
- Run 4 cycles; stop after the 4th refutation (leave PROVISIONAL).

**Kill criteria.**
- DOWNGRADE if: floors escalate 2->3->4->5 across the 4 cycles, honest
  re-confirmation costs grow (2,3,4 honest effect episodes), adversary pays
  1 counter-episode per cycle, and R0 spends a growing fraction of time
  PROVISIONAL/inert. C-R6b narrowed: the X-CV5-1 ratchet is closed for
  one-shot adversaries only; a persistent 1-episode-per-cycle adversary
  wins the cost race.
- HOLD if: floors do not escalate or recovery cost stays flat.

## X-CV6-4: Regression (verify all builder bars, no silent changes)

**Design.**
- Rebuild the binary from the committed 807d13042 blob (already verified
  md5 7d579163a5299c2054e2080df3c3d198).
- Rerun K-CV6-1c (cv6_trunc21), K-CV6-2 (cv5_adv_mask), K-CV6-3
  (cv5_adv_rearm) fixtures; cmp against committed CV6_*_RUN.txt.
- Rerun all 12 regression fixtures; cmp against committed CV6_REG_*.txt.
- Verify `git diff` causalv5.zag -> causalv6.zag is exactly the R6 change
  set (no other mechanism edits).
- 3/3 determinism on every run.

**Kill criteria.**
- KILL (of the regression claim) if any output differs byte-wise from its
  committed raw, any run is non-deterministic, or the v5->v6 diff contains
  non-R6 mechanism changes.
- HOLD (regression claim stands) if all outputs are byte-identical.

## Governance

- Pure Zag only. No Python at any stage (fixtures via shell heredocs/loops,
  analysis via grep/cmp/md5, all committed).
- This prereg is committed ALONE before any attack fixture, build, or run.
- Only CV6-ADV-owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/cv6_adversary/).
- No em dashes in loop documentation (byte-verified before commit).
- Commits stay local; no push.
