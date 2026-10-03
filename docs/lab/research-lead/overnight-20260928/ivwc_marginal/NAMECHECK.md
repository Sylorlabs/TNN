# NAMECHECK.md -- IVWC-MARGINAL

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_marginal/`
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
  pathspecs confined to `ivwc_marginal/` (via separate
  GIT_INDEX_FILE plumbing; shared index and worktree files
  untouched), targeting `tnn-native-lab`. Pushing to origin is
  AUTHORIZED per Micah's 2026-10-03 authorization (fresh GitHub
  PAT; exclude reproducible cache/build artifacts; push promptly
  as the token will be deleted soon).
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit. No amendments.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_marginal.zag`: marginal (decision-boundary-local)
per-bucket miscalibration. World/belief/composer/stepper/seeds/
biases/bars are verbatim from the IVWC lineage (K3 re-verifies:
ThyA=13/20/6, ThyB=13/20/13, TFIXED=12, CVAL=15, ThyHKC=15/20/15,
mcalib=(0,-11,-12,-3), pbkbar=(15,4,3,12),
pboptbar=(15,16,5,15)). What is NEW: instead of measuring
miscalibration over the whole bucket (driven by far-from-margin
cases), measure it only on the marginal train cases near the
worth-K bar, and set each bucket's bar from that local estimate.

- **V_PMW (marginal window, KEY-1):** per bucket b, the marginal
  train set is {t : bkt_t = b, |adj_t - K| <= 10} with K=15 and
  W=10 frozen. Local miscalibration = trunc mean of (adj - eff)
  over the marginal set; if the set is empty, fall back to the
  full-bucket train mcalib. bar_b = K + local. Computed:
  mwmcalib=(0,0,-12,-3), bars (15,15,3,12). Reads only bkt_s
  (sealed, bias-free), train-fixed local quantities, K, and the
  frozen structural window rule. Never reads a sealed
  bias-adjusted score; probe-proof by structure (K1-A10).
- **V_PMN (marginal N-nearest, KEY-2):** per bucket b, the
  marginal train set is the N_b = ceil(n_b/2) train cases in
  bucket b with smallest |adj_t - K|, ties by lowest train
  index (N_b is data-driven; no magnitude constant). Local
  miscalibration = trunc mean of (adj - eff) over those N_b
  cases. bar_b = K + local. Computed: mncalib=(0,-7,-12,-5),
  bars (15,8,3,10). Learner-computable, no sealed data,
  probe-proof by structure (K1-A10).
- **V_PMWX / V_PMNX (fenced marginal exact diagnostics):** the
  exact sealed marginal gaps under the same two marginality
  rules, computed fenced AFTER the REFERENCE phase. They bound
  the marginal estimand: the best any decision-boundary-local
  signal could do. Read sealed eff, so explicitly NOT learner
  bars and NOT candidate mechanisms. Zero world calls. The
  token "oracle" appears nowhere in source, per K1-A8.
- Comparators re-run verbatim in the same binary: UCB x V_WK
  (bar = K, the fixed-K control) and UCB x V_PBK (bars
  (15,4,3,12), the bucket-mean approach). Fenced: V_PBX
  (per-bucket exact, 283) and execute-all.
- Scoring is pure consequence (profit = sum over GO of
  (eff - K)), no labels anywhere. K1 audits zero
  `expected|answer|key|target`, zero
  `correct|reference_plan|gold`, zero `oracle`, zero `Tpred`.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 138 (24 train + 17 + 21 + 19 + 21 GO + 36
  reference; PMWX/PMNX/PBX use zero world calls), preregistered.

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed tables (no new probing), at K=15:

- Marginal bars: PMW (15,15,3,12); PMN (15,8,3,10).
- K4 (PRIMARY, preregistered NULL): UCB x V_PMW total = 228 <
  258 AND UCB x V_PMN total = 248 < 258. No learner-computable
  marginal bar beats the fixed stakes bar. Locality does not
  repair the transfer defect: the train->sealed marginal gap
  shifts are not predictable from bucket identity either (b2
  marginal: -12 train vs +13 sealed @15; b3 marginal: -3 train
  vs +13 sealed @45; b1 marginal: 0 train vs -16 sealed).
- K6: UCB x V_PMN = 248 = V_PBK. The half-nearest marginal bars
  (15,8,3,10) make identical GO commitments to the bucket-mean
  bars (15,4,3,12): the differential bands (b1: (4,8], b3:
  (10,12]) contain no sealed cases on these batches.
- K7: UCB x V_PMW = 228 < 248 = V_PMN. The W=10 window keeps
  only 2 train cases in b1 (gaps -16 and +17), so the local
  estimate is 0 and the b1 bar stays at 15, missing s10's +10
  at @15 and @30. Fewer cases make the estimate noisier, not
  more decision-relevant.
- K9 (divergence): UCB x V_PMN total 248 < UCB x V_WK total 258.
- K10 (divergence): V_PMWX total 288 > 228 AND V_PMNX total
  318 > 248. The exact marginal signal beats the learner
  marginal signal by 60/70: the marginal information is real
  (PMNX gains 30 over PBX at @45 by avoiding s0/s4's -15s via
  the exact local gap +34) but not extractable from {train,
  bkt, K}.
- K5/K8: execute-all (43,113,-80); WC-FINAL=138.
