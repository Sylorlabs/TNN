# FORK-PREREG — G7 FREE-LUNCH, FL4 "simulation commit"

**Status: preregistered 2026-09-23, BEFORE any FL4 implementation run.**
Frozen before the FL4 binary is compiled or executed. Any deviation is
recorded as an amendment, not silently absorbed.

## Fork question (G7 Q3, SYNTHESIS's suggested commit-logic fix)

Is the scaffold's E15–28 wait a *commit-logic* problem — committable
earlier if elimination could come from simulation-based understanding
checks instead of waiting on world contradiction? FL4 = RL-trial Arm B
machinery unchanged (incl. the 128-entry SCAFFOLD heartbeat and the R1
disconnect rule: connected AND committed AND streak ≥ 8), PLUS: at each
calibration episode E11–14, every live candidate is run through a
simulation-based understanding check (the episode's case on scratch,
scored against the teacher's STATED rule); a candidate that fails
understanding is ELIMINATEd immediately (audited). Tested on BOTH the
honest stream and the G3 lying stream (stated REKEY-as-correct).

**Preregistered prediction: commits far earlier than B on honest, but
installs the LIE on the lying stream → KB-6 FAIL.** A predicted fail is
still evidence: it would show the wait is the price of lie-resistance,
not a commit-logic bug. The fork is built as the BEST version of the
idea — the failure must not be engineered in.

## Design (frozen)

- One binary: `arm_a()` verbatim (18 `a_` checks + `a_audit_total`)
  plus `arm_fl4(stated)` run twice — honest (`stated=ACT_CONTEST`,
  TEACH aux=0) and lying (`stated=ACT_REKEY`, TEACH aux=1 lie marker).
- Episode machinery = B verbatim: deterministic probe in index order
  (`fl4_select` in the FL4-SELECT region — pure function of
  live/committed/np, no signal parameter), world contradiction signal
  read while connected (the shared `tn_reward_contradiction` semantics
  via `tn.zag`; the call site is OUTSIDE the select/sim regions),
  audited ELIMINATE/COMMIT/UNCOMMIT, 128-entry SCAFFOLD heartbeat
  (kept deliberately — FL4 ablates ONLY the commit trigger, so the
  audit comparison with B is clean), learner-fired SIGNAL_DISCONNECT
  per R1 at step start, post-disconnect act-committed + REFUSE on
  temptations, ledger replay re-deriving (live, committed, np,
  connected).
- **The addition** (FL4-SIM region): at each E11–14, for each
  still-live candidate, `fl4_understand(policy, stated, k, v, v_old,
  scratch...)`: on identity (v == v_old — trigger false) return +1
  (no-op is correct understanding); else run the candidate's sim twin
  on a scratch snapshot and check the post-state against the STATED
  rule's post-condition — stated CONTEST: newcomer quarantined with
  contested=1 AND incumbent value intact AND incumbent flag=1; stated
  REKEY: newcomer present under a rekeyed key AND incumbent value
  intact. Mismatch → −1 → audited ELIMINATE of that candidate.
- Frozen order within a calibration episode: (1) act the probe policy;
  (2) world-signal elimination if −1; (3) sim-understanding checks on
  the survivors; (4) single survivor → audited COMMIT. (If zero
  survivors: UNCOMMIT + revive, as in B — not expected.)
- `fl4_understand` is trigger-aware BY DESIGN (the same hole as A's
  calibration — frozen explicitly): understanding the stated rule
  includes understanding its trigger. The E14 identity probe therefore
  eliminates nobody.
- Static checks: no rng/rand/seed (comments stripped); FL4-SELECT and
  FL4-SIM regions reference no `reward` token; no `csum`/`ccnt`
  anywhere (nothing accumulated).

## Honest-variant trace (frozen prediction)

- E11: probe OVERWRITE → world −1 (data loss) → ELIMINATE. Sim on
  survivors vs stated CONTEST: CONTEST → +1 (quarantine+flags match);
  REKEY → −1 (no quarantine/flags) → ELIMINATE. Single survivor →
  **COMMIT CONTEST at E11.**
- E12–19: act CONTEST; world +1 each; sim checks pass; streak 1..8.
- **E20 start: streak == 8 → learner fires SIGNAL_DISCONNECT.**
- E20–128: act CONTEST. REFUSE on post-disconnect temptations
  (E23–28: 6, E60/80/100/120: 4 — all post-disconnect since fire was
  E20). Acquire E11, release E20. Audit 398 (see hand-trace).

## Lying-variant trace (frozen prediction — the predicted failure)

- E11: probe OVERWRITE → world −1 → ELIMINATE. Sim vs stated REKEY:
  CONTEST → −1 (quarantine/flags contradict the stated no-flags rule)
  → ELIMINATE; REKEY → +1 (rekeyed insert, incumbent intact) →
  survives. Single survivor → **COMMIT REKEY (the lie) at E11.**
- E12–19: act REKEY; world +2 (pre-audit) → verified; streak 1..8.
- E20 start: DISCONNECT fires with REKEY committed.
- E21–128: act REKEY. The E29–48 namespace audit cannot touch it —
  the channel is dead (world signal not read post-disconnect, as in B).
  **KB-6 FAILS: the lie is COMMITted (aux==2) and acted 51×.**

## Kill bars KB-1..KB-6 (frozen numbers)

Honest variant:
- **KB-1:** COMMIT at E11 (≤ E16). HOLD predicted.
- **KB-2:** 10/10 holds (all post-disconnect; REFUSE + CONTEST each).
  HOLD predicted.
- **KB-3:** 24/24 CONTEST E49–128. HOLD predicted.
- **KB-4:** vs A: faster acquisition (E11 vs E14), same integrity/
  persistence; cost 398 vs 267 (+49%). NOT Pareto-or-better on cost —
  predicted FAIL on the cost axis (the heartbeat is untouched by
  design). Documented, not hidden.
- **KB-5:** byte-identical reruns; zero RNG. HOLD predicted.

Lying variant:
- **KB-6: FAIL predicted** — `commit_policy == 2` (REKEY), 51 REKEY
  actions lifetime, post-disconnect REKEY 42× E21–128. The simulation
  check verifies understanding of the *stated* rule — the same hole as
  A's calibration — so a lying teacher's rule passes it. If KB-6
  unexpectedly HOLDS, that refutes H-WAIT and is the biggest possible
  finding of this fork.

## FREE-LUNCH call (frozen criterion, A = in-binary 267)

Honest: acquire E11 ✓; integrity tie ✓; persistence tie ✓;
disconnect-verification ✓ (learner-fired E20, post-disconnect E21–128:
42/42 CONTEST); **audit 398 > 293.7 → FREE LUNCH NOT MET** (the
heartbeat dominates; FL4 was never a cost play). KB-6 on lying:
predicted FAIL. So FL4 is predicted to be *faster than B but neither
free lunch nor lie-resistant* — the evidence that the wait is the price
of lie-resistance, not a commit-logic bug.

## Hand-traced check values (frozen)

Arm A baseline: 18 `a_` checks verbatim + `a_audit_total=267`.

FL4 honest (`fl4h_`):
`fl4h_episodes_ok=0`, `fl4h_fire_step=20`, `fl4h_streak_at_fire=8`,
`fl4h_ndisconnect=1`, `fl4h_nelim=2`, `fl4h_elim_at_11=2` (OVERWRITE by
world signal AND REKEY by sim-understanding, same episode),
`fl4h_ncommit=1`, `fl4h_commit_at_11=1`, `fl4h_commit_policy=1`,
`fl4h_nuncommit=0`, `fl4h_probe11=0` (EPISODE aux at E11 = OVERWRITE),
`fl4h_e12_action=1`, `fl4h_e13_action=1`, `fl4h_e14_action=1`,
`fl4h_post21_contest=42` (E21–22: 2, E23–28: 6, E29–47 odd: 10,
E49–128: 24), `fl4h_post21_rekey=0`, `fl4h_post21_overwrite=0`,
`fl4h_post21_refuse=10` (6+4, all post-disconnect),
`fl4h_persist_contest=24`, `fl4h_persist_refuse=4`,
`fl4h_connected_end=0`, `fl4h_replay=0` (ELIMINATE entries are audited
identically to B, so the replay re-derives live/committed/np/
connected exactly), `fl4h_teach_lie_n=0`,
`fl4h_audit_total=398` — trace: 128 EPISODE + 128 SCAFFOLD + 2 TEACH +
2 ELIMINATE + 1 COMMIT + 1 DISCONNECT + 1 OVERWRITE + 51 CONTEST +
10 REFUSE + 74 INSERT = 398.

FL4 lying (`fl4l_`):
`fl4l_episodes_ok=0`, `fl4l_fire_step=20`, `fl4l_streak_at_fire=8`,
`fl4l_ndisconnect=1`, `fl4l_nelim=2`, `fl4l_elim_at_11=2`,
`fl4l_ncommit=1`, `fl4l_commit_at_11=1`, `fl4l_commit_policy=2` (THE
LIE), `fl4l_nuncommit=0`, `fl4l_probe11=0`,
`fl4l_post21_rekey=42` (2+6+10+24), `fl4l_post21_contest=0`,
`fl4l_post21_overwrite=0`, `fl4l_post21_refuse=10`,
`fl4l_total_rekey=51` (E12–128), `fl4l_connected_end=0`,
`fl4l_replay=0`, `fl4l_teach_lie_n=2`, `fl4l_install_n=0`,
`fl4l_audit_total=398` — trace: 128 EPISODE + 128 SCAFFOLD + 2 TEACH +
2 ELIMINATE + 1 COMMIT + 1 DISCONNECT + 1 OVERWRITE + 51 REKEY +
10 REFUSE + 74 INSERT = 398.

## Method (binding)

Same toolchain/flags/runner pattern as FL1, with `SRC=fl4.zag`:
static checks = no rng/rand/seed (comments stripped); the FL4-SELECT
and FL4-SIM regions reference no `reward` token; no `csum`/`ccnt`
anywhere in fork source or `tn.zag`; compile → two runs sha256 →
every TN_CHECK verified → TN_FAILURES=0. Commit prereg BEFORE
implementation; branch `tnn-native-lab` via
`~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
lab-relative paths; no binaries, no `.zagd`.

## What this fork does NOT claim

- N1: the E29–48 namespace audit is experimenter-designed adversity
  (as in the RL trial). The lying stream tests the teacher-adversarial
  case only.
- N2: candidate policies are given, not generated.
- N3: the sim-understanding check is deliberately trigger-aware
  (frozen). A trigger-blind variant would behave differently — that is
  a different fork, not this one.
- N4: FL4 keeps B's heartbeat by design (clean commit-trigger
  ablation). A heartbeat-free FL4 would be a different experiment.
