# NAMECHECK.md -- IVWC-APPLIED

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_applied/`
  (fresh lane; all other lanes untouched).
- Worktree: `~/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing, `which python` returns nothing.
  Pinned znc at `$HOME/safebin/znc` (2026.07.0-dev). Pure Zag only.
  No python, no C, no JS, no Rust in implementation, scoring, or
  analysis. Absolutely no python3/python invocation at any step.
- Git: `/usr/bin/git` directly (the safebin `git` symlink is
  known-broken for writes per AGENTS.md). Commits local, explicit
  pathspecs confined to `ivwc_applied/`. Pushing to origin is
  AUTHORIZED per Micah's 2026-10-03 authorization (fresh GitHub
  PAT; exclude reproducible cache/build artifacts; push promptly).
- Branch repair (same session, before this lane): commit
  `cef8c4095` restored the `tnn-native-lab` tip tree after
  `169894404` (empty tree) and `88e9108f4` (8-file tree) broke it.
  Repair tree = `560dd16a3` (last good, 165,250 files) + the 8
  `ivwc_hybrid_clean` files. Verified: diff shows exactly 8
  additions, 0 deletions. Done via a separate GIT_INDEX_FILE; the
  shared index and all worktree files untouched. The unrecoverable
  loss (COGOPS-PLEN-ADVANTAGE report artifacts, never committed
  anywhere) is documented in the repair commit message and will be
  flagged to the parent.
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_applied.zag`: applies the hybrid verdict (V_HA/V_HB from
IVWC-HYBRID-VERDICT) to selective execution -- a real internal
verification problem with no expected-answer oracle. World/belief/
composer/stepper/seeds/biases/bars are verbatim from the verdict
wave (K3 re-verifies: ThyA=13/20/6, ThyB=13/20/13, TFIXED=12,
CVAL=15). What is NEW:

- The learner's verdict becomes a GO/NO-GO execution decision
  (commit resources or abstain), made before any consequence.
- Scoring is pure consequence: the world charges K=15 per GO;
  profit = sum over GO cases of (eff - 15). No labels, no ge, no
  Tpred -- not for the learner, not even fenced for scoring.
  K1-A9 audits zero `Tpred` tokens in the source.
- Arms: A1/A2/A7a/A7b (learner-side: the learner's own UCB bias
  under V_T/V_N/V_HA/V_HB), A3/A4/A8a/A8b/A9a/A9b (fenced D1b/D2b
  diagnostics), plus a fenced execute-all reference.
- `world_execute(` appears exactly 4 times (1 def + 3 call
  sites); WC-FINAL = 185 (24 train + 125 GO + 36 reference).

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed verdict-wave per-case tables (no new probing),
at K=15:

- K4 (PRIMARY): UCB x V_HA profit = (75, 95, 40), total 210 >
  execute-all 76. Self-verification without an oracle works and
  beats no-verification by 134.
- K6: HA @45 = 40 < HB @45 = 55 -- the preregistered @45
  bias-mix limit as a 15-profit loss (s=5 false GO).
- K7: D1b x HA @15 = 72 > D1b x V_T @15 = 52 -- the un-blocking
  pays in consequences.
- K9: D1b totals HA=262, VT=270, VN=280 -- preregistered DIVERGENCE
  vs the verdict wave's accuracy table (A8a 35/36 > A4 34/36):
  accuracy-optimal != profit-optimal; the hybrid bar answers a
  relative-trust question, not a consequence question.
- K5/K8/K10: execute-all (43,113,-80); WC-FINAL=185; D2b x
  HA/HB totals 159/159.
