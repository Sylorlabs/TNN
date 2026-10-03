# NAMECHECK.md -- IVWC-HYBRID-VERDICT

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_hybrid_verdict/`
  (fresh lane; `ivwc_hybrid/`, `ivwc_nontransductive/`, and all other
  lanes untouched).
- Worktree: `~/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing, `which python` returns nothing.
  Pinned znc at `$HOME/safebin/znc`. Pure Zag only. No python, no C,
  no JS, no Rust in implementation, scoring, or analysis. Absolutely
  no python3/python invocation at any step.
- Source: `src/ivwc_hybrid_verdict.zag` is derived from the committed
  `ivwc_nontransductive` source (world/belief/composer/stepper/
  verifier/seeds verbatim); the ONLY changes are the hybrid-verdict
  machinery (train offset C, sealed bars ThyA/ThyB, arms A7a/A7b/
  A8a/A8b/A9a/A9b, extended prints and kill-bar counters).
- Git: `/usr/bin/git` directly (the safebin `git` symlink is
  known-broken for writes per AGENTS.md). Commits local, explicit
  pathspecs confined to `ivwc_hybrid_verdict/`, never pushed.
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit.
- Non-ledger task (claim minting paused).

## Step 1: What is being built

`src/ivwc_hybrid_verdict.zag`: verbatim world/belief/composer/stepper/
verifier/seeds from IVWC-NONTRANSDUCTIVE (sealed (bucket, eff) pairs
bit-identical; K3/K4 anchors verify). The experimental variable is the
verdict structure. Two hybrid bars are tested:

- V_HA (primary, preff-scoped): PASS iff adjV > ThyA(sh),
  ThyA(sh) = mean_sealed(preff) - C,
  C = mean over the 24 train cases of bucb[bkt_tr] (train-fixed,
  preregistered expectation 15). The bar is batch-responsive (sealed
  preff mean) yet correction-independent (no sealed adjV, no +40
  enters; C is train-fixed).
- V_HB (secondary, frozen-baseline-scoped): PASS iff adjV > ThyB(sh),
  ThyB(sh) = mean over the sealed batch of (preff - bucb_frozen[bkt])
  (algebraically = TVucb; computed explicitly). The bar additionally
  responds to the sealed batch's bucket composition through the
  FROZEN baseline bias, never through the experimental +40
  corrections.

Arms: A1..A6 verbatim from nontransductive (V_T/V_N anchors, required
for the three-way comparison), plus A7a=UCBxV_HA, A7b=UCBxV_HB,
A8a=D1bxV_HA, A8b=D1bxV_HB, A9a=D2bxV_HA, A9b=D2bxV_HB. Anchors
OF/X3/HYB/MG re-scored in-program.

## Step 2: Mechanism predictions (summary; full tables in PREREG.md)

From the committed nontransductive per-case tables (no new probing):
ThyA = 13/20/6 @15/30/45; ThyB = 13/20/13 (== TVucb).
- K5: A8a @15 = 11/12, errors exactly {s=5} (the (D1b x threshold)
  ceiling; V_HA keeps V_N's un-blocking).
- K7: A7a @15 = 11/12, errors exactly {s=3} (V_HA recovers V_T on UCB
  @15; the s=0 tie-break is preserved).
- K9: A8a @30 = 12/12 (batch responsiveness beats V_N's 11/12 @30).
- K10: A7a @45 = 9/12, errors exactly {s=0,s=4,s=5} (the LIMIT:
  preff-scoping does not recover V_T's 10/12 @45; the @45 batch is
  bucket-0 heavy and the train-fixed offset C miscalibrates).
- Secondary: A7b == A1 (11/9/10); A8b: 11/12, 12/12, 12/12;
  A9b: 9/12, 9/12, 10/12; A9a: 9/12, 9/12, 10/12.
