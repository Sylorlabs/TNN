# NAMECHECK.md -- IVWC-CONSEQUENCE

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_consequence/`
  (fresh lane; all other lanes untouched).
- Worktree: `~/workspace/tnn-rsi` (shared checkout; branch
  `lane-ma4b-20261003` for the worktree, but all commits for this
  lane target `tnn-native-lab` via explicit pathspec plumbing that
  leaves the shared index untouched).
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing (rc=1), `which python` returns
  nothing (rc=1). Pinned znc at `$HOME/safebin/znc`. Pure Zag only.
  No python, no C, no JS, no Rust in implementation, scoring, or
  analysis. Absolutely no python3/python invocation at any step.
  This lane is clean: no toolchain incident, no disclosure needed.
- Git: `/usr/bin/git` directly (the safebin `git` symlink is
  known-broken for writes per AGENTS.md). Commits local, explicit
  pathspecs confined to `ivwc_consequence/` (via separate
  GIT_INDEX_FILE plumbing; shared index and worktree files
  untouched), targeting `tnn-native-lab`. Pushing to origin is
  AUTHORIZED per Micah's 2026-10-03 authorization (fresh GitHub
  PAT; exclude reproducible cache/build artifacts; push promptly
  as the token will be deleted soon).
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_consequence.zag`: the consequence-aware hybrid verdict.
World/belief/composer/stepper/seeds/biases/bars are verbatim from
IVWC-HYBRID-VERDICT / IVWC-APPLIED (K3 re-verifies: ThyA=13/20/6,
ThyB=13/20/13, TFIXED=12, CVAL=15). What is NEW: two verdicts that
incorporate the stakes K=EXCOST=15 (a world parameter, not a
label).

- **V_HKC (consequence-aware hybrid, KEY):** bar_HKC(sh) =
  max(ThyA(sh), K). The learner's GO/NO-GO verdict clears BOTH
  the hybrid bar (batch-responsive, correction-independent) and
  the stakes. Correction-independence is preserved structurally:
  the bar reads only preff (sealed, bias-free), C (train-fixed),
  and K (world constant) -- never the learner's sealed corrected
  scores (adjucb/d1adj/d2adj), so the fenced +40 probes cannot
  move it.
- **V_WK (worth-K control):** bar = K. The pure consequence
  question ("worth K?") with no batch-relative component. Tests
  whether the hybrid's relative-trust level carries any
  profit-relevant information once stakes are incorporated.
- Baselines re-verified verbatim: UCB x V_HA, D1b x V_HA,
  D2b x V_HA, plus the fenced execute-all reference.
- Scoring is pure consequence (profit = sum over GO of
  (eff - K)), no labels anywhere. K1 audits zero
  `expected|answer|key|target`, zero
  `correct|reference_plan|gold`, zero `oracle`, zero `Tpred`.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 167 (24 train + 107 GO + 36 reference), preregistered.

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed verdict-wave per-case tables (no new probing),
at K=15:

- K4 (PRIMARY): UCB x V_HKC total 225 > UCB x V_HA total 210.
  Consequence-awareness improves profit on the real learner case.
- K6: UCB x V_HKC @45 = 55 > UCB x V_HA @45 = 40. The K-floor
  blocks s=5's false GO (adjucb=13 < 15; eff=0), recovering the
  @45 loss priced in APPLIED's K6.
- K7: D1b x V_HKC @15 = 72. The K-floor does not bind @15
  (max(13,15)=15) and the un-blocking is preserved.
- K9 (preregistered divergence): D1b totals V_HKC=262 <
  V_WK=280. The pure worth-K bar beats the consequence-aware
  hybrid: the hybrid's batch-tracking is profit-harmful under the
  @30 shift (bar 20 skips s=2's +18).
- K10 (preregistered divergence): UCB totals V_HKC=225 <
  V_WK=258. Same finding on the learner arms.
- K5/K8: execute-all (43,113,-80); WC-FINAL=167.
