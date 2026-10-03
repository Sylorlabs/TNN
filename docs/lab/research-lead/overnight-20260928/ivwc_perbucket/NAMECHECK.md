# NAMECHECK.md -- IVWC-PERBUCKET

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_perbucket/`
  (fresh lane; all other lanes untouched).
- Worktree: `~/workspace/tnn-rsi` (shared checkout; all commits
  for this lane target `tnn-native-lab` via explicit pathspec
  plumbing that leaves the shared index untouched).
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing (rc=1), `which python` returns
  nothing (rc=1). Pinned znc at `$HOME/safebin/znc`
  (znc 2026.07.0-dev). Pure Zag only. No python, no C, no JS, no
  Rust in implementation, scoring, or analysis. Absolutely no
  python3/python invocation at any step. This lane is clean: no
  toolchain incident, no disclosure needed.
- Git: `/usr/bin/git` directly (the safebin `git` symlink is
  known-broken for writes per AGENTS.md). Commits local, explicit
  pathspecs confined to `ivwc_perbucket/` (via separate
  GIT_INDEX_FILE plumbing; shared index and worktree files
  untouched), targeting `tnn-native-lab`. Pushing to origin is
  AUTHORIZED per Micah's 2026-10-03 authorization (fresh GitHub
  PAT; exclude reproducible cache/build artifacts; push promptly
  as the token will be deleted soon).
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit. No amendments.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_perbucket.zag`: per-bucket worth-K verdicts.
World/belief/composer/stepper/seeds/biases/bars are verbatim from
the IVWC lineage (IVWC-HYBRID-VERDICT / IVWC-APPLIED /
IVWC-CONSEQUENCE / IVWC-BATCHAWARE; K3 re-verifies: ThyA=13/20/6,
ThyB=13/20/13, TFIXED=12, CVAL=15, ThyHKC=15/20/15,
mcalib=(0,-11,-12,-3)). What is NEW: the worth-K bar is set
per bucket instead of once per batch.

- **V_PBK (per-bucket worth-K, KEY-1):** bar_b = K + mcalib[b],
  K=15, so per-bucket bars (15,4,3,12). The miscalibration-
  corrected score is adj - mcalib[b]; GO iff adj > K +
  mcalib[b]. Reads only bkt (sealed, bias-free), mcalib
  (train-fixed), K (world constant). Never reads a sealed
  bias-adjusted score; probe-proof by structure (K1-A10).
- **V_PBOPT (train-optimal per-bucket bars, KEY-2):** per bucket,
  bar*_b = the train-profit-optimal bar (maximizes sum over
  train GO cases of (eff - K) on train consequences, which are
  learner-visible), ties broken toward K. Computed bars:
  (15,16,5,15). Learner-computable, no researcher constants, no
  sealed data. Probe-proof by structure (K1-A10).
- **V_PBX (fenced per-bucket exact diagnostic):** bar_b(sh) =
  K + exact sealed per-bucket gap, computed fenced AFTER the
  REFERENCE phase. Bounds the per-bucket estimand: the best any
  per-bucket miscalibration signal could do. Reads sealed eff,
  so explicitly NOT a learner bar and NOT a candidate mechanism.
  Zero world calls. Named `pbx` (the token "oracle" appears
  nowhere in source, per K1-A8).
- Lineage control re-verified verbatim: UCB x V_WK (bar = K).
  Fenced execute-all reference.
- Scoring is pure consequence (profit = sum over GO of
  (eff - K)), no labels anywhere. K1 audits zero
  `expected|answer|key|target`, zero
  `correct|reference_plan|gold`, zero `oracle`, zero `Tpred`.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 116 (24 train + 17 + 21 + 18 GO + 36 reference;
  PBX uses zero world calls), preregistered.

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed tables (no new probing), at K=15:

- Per-bucket PBK bars (15,4,3,12); PBOPT bars (15,16,5,15).
- K4 (PRIMARY, preregistered NULL): UCB x V_PBK total = 248 <
  258 AND UCB x V_PBOPT total = 243 < 258. No learner-computable
  per-bucket bar beats the fixed stakes bar. The below-batch
  information is real but not learner-usable from train alone:
  the train->sealed per-bucket gap shift (b2: -12 train vs +13
  sealed @15; b1: -11 train vs +17 sealed @45) is not
  predictable from bucket identity.
- K6: UCB x V_PBK = 248 (coincides with the V_BAMK lineage
  total; the differential bands between per-bucket bars and the
  batch-mix bar are empty on these batches).
- K7: UCB x V_PBOPT = 243 < 248 = V_PBK. Train-profit-optimal
  per-bucket bars overfit train (b1 bar 16 misses sealed s10's
  +10 twice; b3 bar 15 avoids s5's -15 once -- net worse).
- K9 (divergence): UCB x V_PBK total 248 < UCB x V_WK total 258.
- K10 (divergence): V_PBX total 283 > 248. The exact
  per-bucket signal beats the learner per-bucket signal by 35
  (sh0: s0's -15 avoided, s6's +5 taken = 20; sh1: 0; sh2: s5's
  -15 avoided = 15). The information is real; it lives below
  what train alone can supply.
- K5/K8: execute-all (43,113,-80); WC-FINAL=116.
