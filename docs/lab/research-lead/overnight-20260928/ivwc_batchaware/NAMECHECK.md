# NAMECHECK.md -- IVWC-BATCHAWARE

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_batchaware/`
  (fresh lane; all other lanes untouched).
- Worktree: `~/workspace/tnn-rsi` (shared checkout; all commits
  for this lane target `tnn-native-lab` via explicit pathspec
  plumbing that leaves the shared index untouched).
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing (rc=1), `which python` returns
  nothing (rc=1). Pinned znc at `$HOME/safebin/znc`. Pure Zag only.
  No python, no C, no JS, no Rust in implementation, scoring, or
  analysis. Absolutely no python3/python invocation at any step.
  This lane is clean: no toolchain incident, no disclosure needed.
- Git: `/usr/bin/git` directly (the safebin `git` symlink is
  known-broken for writes per AGENTS.md). Commits local, explicit
  pathspecs confined to `ivwc_batchaware/` (via separate
  GIT_INDEX_FILE plumbing; shared index and worktree files
  untouched), targeting `tnn-native-lab`. Pushing to origin is
  AUTHORIZED per Micah's 2026-10-03 authorization (fresh GitHub
  PAT; exclude reproducible cache/build artifacts; push promptly
  as the token will be deleted soon).
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit. No amendments.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_batchaware.zag`: the batch-aware worth-K verdict.
World/belief/composer/stepper/seeds/biases/bars are verbatim from
IVWC-HYBRID-VERDICT / IVWC-APPLIED / IVWC-CONSEQUENCE (K3
re-verifies: ThyA=13/20/6, ThyB=13/20/13, TFIXED=12, CVAL=15,
ThyHKC=15/20/15). What is NEW: a verdict that tracks the batch's
predicted miscalibration instead of the batch's level.

- **V_BAMK (batch-aware miscalibration worth-K, KEY):**
  bar_BAMK(sh) = K + M_pred(sh), K=15. M_pred(sh) is the
  bucket-mix signal: mean over sealed cases of M_train[bkt_s],
  where M_train[b] is the train in-sample miscalibration per
  bucket (mean of adj-eff on train). Reads only bkt (sealed,
  bias-free), M_train (train-fixed), K (world constant). Never
  reads a sealed bias-adjusted score; probe-proof (K1-A10).
- **V_XMG (fenced exact-gap diagnostic):** bar = K + M(sh) with
  the exact batch mean gap, computed fenced after REFERENCE.
  Not a learner verdict; bounds the mean-gap estimand. Zero
  world calls. Named `xmg` (no "oracle" token in source).
- Baselines re-verified verbatim: UCB x V_HA, UCB x V_HKC,
  UCB x V_WK, D1b/D2b x V_BAMK (fenced), execute-all reference.
- Scoring is pure consequence (profit = sum over GO of
  (eff - K)), no labels anywhere. K1 audits zero
  `expected|answer|key|target`, zero
  `correct|reference_plan|gold`, zero `oracle`, zero `Tpred`.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 153 (24 train + 93 GO + 36 reference), preregistered.

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed tables (no new probing), at K=15:

- M_train = (0,-11,-12,-3); M_pred = (-7,-7,-4);
  bar_BAMK = (8,8,11).
- K4 (PRIMARY): UCB x V_BAMK total 248 > UCB x V_HKC total 225.
  Miscalibration-tracking beats harmful level-tracking.
- K6: UCB x V_BAMK @30 = 138 > UCB x V_WK @30 = 128 (takes
  s=10's +10; the signal helps where over-correction is real).
- K7: UCB x V_BAMK @45 = 40 < UCB x V_WK @45 = 55 (takes s=5's
  -15; the signal gets the sign wrong under the @45 shift).
- K9 (divergence): UCB x V_BAMK total 248 < UCB x V_WK total
  258. Miscalibration-tracking does not beat pure worth-K.
- K10 (divergence): V_XMG total 243 < UCB x V_WK total 258.
  Even the exact mean-gap signal fails; the mean is not
  decision-relevant.
- K5/K8: execute-all (43,113,-80); WC-FINAL=153.
