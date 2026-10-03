# NAMECHECK.md -- IVWC-CASEBIAS-RETRY

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_casebias_retry/` (fresh
  lane; the prior `ivwc_casebias/` lane is untouched).
- Worktree: `~/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3 python` returns nothing (no output, exit nonzero).
- Compiler: pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev`). Pure Zag only. No python, no C, no JS, no Rust
  in implementation, scoring, or analysis.
- Git: `/usr/bin/git` directly (the safebin `git` symlink is known-broken
  for writes per AGENTS.md). Commits local, explicit pathspecs confined to
  `ivwc_casebias_retry/`, never pushed.
- Prereg commit precedes implementation commit (enforced by committing
  PREREG.md + NAMECHECK.md alone first).

## Step 1: What is being built

`src/ivwc_casebias_retry.zag`: verbatim copy of IVWC-CASEBIAS's
world/belief/composer/stepper/verifier/seeds (sealed pairs bit-identical;
K3/K4 anchors verify), plus:

- vv=0 V-UCB anchor (frozen UCB bucket bias, recomputed in-program).
- vv=1 V-SENS (learner): case-level bias = UCB bucket bias + train-fit
  excess residual on a counterfactual-perturbation fragility bin.
  Fragility F(s) = max over leave-one-out recompositions of (P - P_{-i}):
  for each gathered item i, remove it from the belief, re-run
  learner_compose, record preff P_{-i}. Bins: F=0 / 1..25 / >25.
  Residual = mean(d - UCB_b) per bin MINUS global mean residual
  (so a constant-F world reproduces UCB exactly; no degenerate global
  shift). All trained on the 24 train cases only.
- D-ORACLE-BIAS (fenced harness diagnostic in SCORING, never
  learner-visible): harness counts nphantom(s) = number of committed
  planned gathers at cells where the TRUE world has no item.
  B_orc(s) = UCB_b + 40 if nphantom(s) > 0 else UCB_b.
  Verdict = (adjV_orc > TV_orc), TV_orc = mean adjV_orc (same transductive
  mean-bar verdict family as the learner). The +40 is a diagnostic probe
  magnitude, not a proposed learned value; it tests whether ANY
  phantom-conditioned bias can succeed under the mean bar.
- D-ORACLE-SH (fenced shuffled twin): same, but the phantom indicator is
  rotated by 7 cases (nphantom of case (s+7)%12). Tests that D1's effect
  comes from phantom CONTENT, not the procedure.

## Step 2: Diet declaration

24 train cases at wp=15 (seeds verbatim). Sealed: 12 cases each at
wp=15/30/45 (seeds verbatim). Labels ge = (eff >= Tpred) live only in
SCORING. No sealed truth reaches the learner. The word "oracle" appears
only inside the fenced diagnostic block.

## Step 3: Mechanism predictions (preregistered before implementation)

- V-SENS: 11/12 @15 (error {s=3}, same as UCB), 10/12 @45. The fragility
  signal is predicted to carry no phantom information: F reflects random
  spatial layout of non-gathered believed items, not belief wrongness.
  Train bin residuals predicted ≈ 0.
- D-ORACLE-BIAS @15: ≤ 11/12 (does NOT reach 12/12). It fixes s=3 but the
  mean bar drops and flips a boundary true-negative (predicted s=10:
  adjV=9 > dropped TV). Whack-a-mole under the transductive bar.
- D-ORACLE-BIAS @45: ≥ 11/12 (improves on UCB's 10/12 by fixing the
  (1,50)-signature phantoms s=0,s=4). Whether it reaches 12/12 depends on
  how many boundary cases the bar drop breaks; predicted 11/12.
- D-ORACLE-SH: ≤ D-ORACLE-BIAS on both regimes (content matters).

## Step 4: Answers to the task's key questions (preregistered positions)

1. What case-level features distinguish phantoms from genuine positives?
   Predicted: none available to the learner. The phantom is independent
   per-cell belief noise; the belief is the learner's only observation.
2. Can the learner compute distinguishing features from internal state?
   Predicted: the machinery is computable (V-SENS runs), but it carries
   no signal. Computability was never the bottleneck; information is.
3. Does case-level bias generalize or overfit to s=3? Predicted: neither;
   the binding constraint is the (information) x (verdict-structure)
   interaction, not the estimator. Even a perfect signal cannot reach
   12/12 under the mean bar (D1 predicted ≤ 11/12 @15).
