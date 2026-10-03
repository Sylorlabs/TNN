# G1 REMATCH — group synthesis (plain language)

**Question:** was the release schedule the load-bearing variable in
RL-trial Arm B's loss? (B: scaffold-and-release with scalar outcome
reward, learner-initiated disconnect — needed 38 episodes vs deliberate
teaching's 14, 2× the audit, because the reward couldn't tell CONTEST
(+1) from REKEY (+2) until the audit perturbation at E29.)

**Answer: No.** Five forks varied only the release schedule — same
reward, same task, same eliminative machinery, same 128 episodes, each
against the same deliberate-teaching baseline. The commit point never
moved: E29 in every fork that committed. The release schedule decides
*when* (and whether) the learner is released onto the committed
behavior — it cannot touch the commit logic, which is where B's loss to
teaching actually lives.

## Per-fork one-paragraph verdicts

- **R1 (learner-initiated disconnect, exact B replication): PASSES.**
  Reproduces the trial's B numbers check-for-check on an independent
  build: commit E29, fire E38 (streak 8), 29/29 post-release, 24/24
  persistence, 392 audit entries. KB-4 fails as preregistered: 38
  episodes and 392 entries vs teaching's 14 and 193.
- **R2 (sudden harness cut at E30): PASSES.** Cutting the 8-episode
  verification wait changed nothing about quality — 33/33 post-release,
  4/4 refuses, 24/24 persistence, identical to R1. Release at 30 vs 38
  saves 8 episodes but the fork is still 2.1× slower than teaching
  (30 vs 14). The verification wait is pure cost with no integrity
  value.
- **R3 (gradual fade of the signal, E30–41): PASSES.** Commit still at
  E29 — the fade doesn't touch elimination — but the thinning signal
  strands the verification-gated release: streak peaks at 5, the learner
  never fires (no disconnect ever, channel stays connected). The
  committed policy still acts CONTEST on all 33 post-commit
  contradictions. Gradual release isn't a slower sudden release: for
  verification-gated machinery it can prevent release entirely, because
  the verification currency is denominated in the fading signal.
- **R4 (late release, streak threshold 24): PASSES.** Fire at E54,
  23/23 post-release, 4/4 refuses, 24/24 persistence — identical quality
  to R1 at 16 more episodes. More verification buys nothing; the policy
  was already correct at E29.
- **R5 (early cut at E20, before any commit): FAILS KB-1–KB-4 as
  preregistered.** Zero commits ever — REKEY is never eliminated without
  the signal — and the learner alternates CONTEST/REKEY (22/21) forever,
  including through the persistence window. The scaffold's pre-commit
  eliminative work is load-bearing: cut before convergence and nothing
  works.

## The pattern

| Fork | Release | Commit | Episodes to release | Audit entries | KB-4 vs teaching |
|---|---|---|---|---|---|
| R1 | E38 (learner) | E29 | 38 | 392 | fail |
| R2 | E30 (sudden) | E29 | 30 | 392 | fail |
| R3 | never (fade strands) | E29 | — | 387 | fail |
| R4 | E54 (late) | E29 | 54 | 392 | fail |
| R5 | E20 (early) | never | — | 396 | fail |
| A (baseline) | n/a (install E14) | — | 14 | 193 | — |

Three regularities, all preregistered and all confirmed:
1. **The commit point is schedule-invariant** (E29 wherever a commit
   happens). The 15-episode gap to teaching's install (E14) comes from
   the eliminative commit logic — the reward's blindness to procedure —
   which no release schedule touches.
2. **Release timing moves cost, not quality.** R2 (−8 eps), R4 (+16
   eps), R1: identical post-release integrity and persistence. Audit
   entries are flat across schedules (387–396).
3. **Release must come after commit, or nothing works** (R5), and a
   fading signal can strand a verification-gated release entirely (R3).

## What this means for H (Micah's hypothesis)

G1 does not save scaffold-and-release on this task: no release schedule
beats plain deliberate teaching here (KB-4 fails 5/5). But it sharpens
the boundary map: the loss is in the *commit* logic (reward can't see
procedure), not the *release* logic. A scaffold that committed
differently — not one that releases differently — is what G2
(richer scaffolds) has to find.

## Reproducibility

- Frozen fork preregs: commit `585602fc` (before any implementation).
- Each fork: `tn.zag` (byte-identical to the trial, sha256
  `0c59e21e…b33b7dc22b05b72b920ca1b9c34`), `g1.zag` (baseline Arm A +
  fork arm), `run_fork.sh` (compile → 2 runs sha256 → static checks →
  all TN_CHECKs → TN_FAILURES,0).
- All five runners: ALL CHECKS PASS (R1 39/39, R2 40/40, R3 43/43, R4
  39/39, R5 39/39); byte-identical reruns; no-RNG grep, select-region
  signal ban, and no-accumulation checks all pass.
- Baseline `a_` evidence lines are byte-identical across all five
  forks and identical to the RL trial's evidence.
- PYTHON SWEEP: no Python anywhere in the fork sources or decision
  paths — learner, world, reward, and harness are 100% native Zag.
  (Python was used once, outside the repo, as a build-time text
  transform deriving the fork harnesses; the runner is bash glue.)
