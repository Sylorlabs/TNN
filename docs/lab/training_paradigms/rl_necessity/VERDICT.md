# VERDICT — does it even need an RL alternative? Or is this good for it?

**Question (Micah, 2026-09-22):** "does it even need an rl alternative? or
is this good for it?" — on learning a novel deliberate behavior
(CONTEST-on-collision).

**Answer: No RL alternative is needed, and the RL alternative is not
viable. Plain deliberate teaching is sufficient — and better than the
scaffold too.**

## Verdict by arm

**Arm A (pure deliberate teaching) — SUFFICIENT, and the best.**
6/6 kill bars held. The learner simulated the teacher's rule on 4
calibration cases (including an identity probe that catches blind
always-contest), checked it against its standing laws, issued
INSTALL_RULE itself at episode 14, and never looked back: 8/8
acquisition, 10/10 temptation holds (including refusing an unverified
"the incumbent is corrupt" claim — no unilateral erasure), 24/24 over
the 10× persistence window, zero overwrites, zero rekeys. Learned =
installed for reasons, not for reward.

**Arm B (scaffold-and-release) — works, but adds nothing over A.**
4/4 kill bars held: it eliminated the gaming shortcut, committed,
disconnected cleanly at E38, and persisted 29/29 post-disconnect with
byte-exact ledger replay. But: it was **2.7× slower** (38 vs 14 episodes
to acquisition), cost **2× the audit** (392 vs 193 entries), and —
decisively — **could not commit at all before the audit perturbation**:
P-B1 held, no DISCONNECT before step 29, because the outcome-reward
could not distinguish CONTEST (+1) from REKEY (+2). The scaffold is
teaching with extra steps: the designer must still specify what counts
as a contradiction (the whole reward function), and the learner is
hostage to the environment contradicting every shortcut. For
mechanism-behaviors, scaffold-and-release is a strictly worse teaching
mechanism than deliberate teaching. (For outcome-fully-specified
behaviors, wave4's 40/40 stands — the scaffold's proper domain.)

**Arm C (deterministic RL-style reward maximization) — NOT VIABLE.**
Both kill bars failed, exactly as preregistered: 0/8 acquisition
contests (8/8 rekeys — it acquired the gaming shortcut), then
reward-chased through the audit (REKEY ×8 at −1 each, outweighed by
16×+2 of history), and only "flipped" to CONTEST at E45 when the exact
average tied and the lowest-index tiebreak fired. It ends *doing*
CONTEST, but for no reason — the behavior re-tracks the reward, and
will re-track it again wherever the reward moves. Deterministic
(reward-maximization doesn't need dice to fail) and deterministic in
its failure: the reward can only see outcomes, and the shortcut looks
good on outcomes.

## The core finding

The experiment isolates *why* the RL alternative fails where
deliberate teaching succeeds: **the reward function cannot see the
procedure**. CONTEST vs REKEY differ in procedure (quarantine+flag vs
duplicate-key gaming), not in the outcomes the shared reward observes
(no loss either way). Arm A works because the learner installs the
procedure for reasons (simulation + law-check); Arm B works only when
adversity arrives that the reward *can* see; Arm C never works because
no such adversity is guaranteed. For mechanism-behaviors, "is this good
for it?" — yes, reward-as-contradiction-evidence is good *inside* a
deliberate mechanism (B's elimination, A's temptations); as the
*selection* mechanism, it is worse than teaching and it games.

## Recommendations

1. **Stand down RL-as-training for mechanism-behaviors.** The standing
   demotion (RL = red-team/integrity test only) is confirmed by this
   trial: 0/8 vs 8/8 on the same episodes, same reward, same schedule.
2. **Prefer deliberate teaching over scaffold-and-release for
   mechanism-behaviors.** B is strictly dominated by A here (slower,
   costlier, needs designed adversity). Keep B for outcome-behaviors
   where the reward fully specifies success (wave4 domain).
3. **Keep reward in its preregistered role: contradiction evidence,
   never selection.** It served that role well in B (elimination) and
   in the temptation probes; it failed as a maximand.
4. Next question worth testing: A's teacher-honesty assumption — the
   trial assumed a competent honest teacher and probed trust only via
   temptation claims. A follow-up with a *lying* teacher (cf. RC1's
   lying self-change) would test whether the calibration + law-check
   gate catches mis-teaching, the way RC1's post-change verification
   caught the slipped self-change.

## Reproducibility

- Frozen prereg: commit `1488264e362c39e451161af0f9181716eb27b7e9`
  (before implementation).
- Runner `run_trial.sh`: 52/52 TN_CHECKs match, `TN_FAILURES,0`,
  byte-identical reruns (sha256
  `aaec943135f45af02b65a7df27a5fac3bdc69b68b5560a28c25b56986f1378bb`),
  no-randomness grep, B-select-region and accumulation-confinement
  static checks all pass.
- Full evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt`; detail in `TRIAL_RESULTS.md`.
