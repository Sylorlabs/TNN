# NAMECHECK.md -- IVWC-NONTRANSDUCTIVE

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_nontransductive/`
  (fresh lane; `ivwc_scorebias/` and `ivwc_casebias_retry/` untouched).
- Worktree: `~/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.
- Safebin: `export PATH="$HOME/safebin"`. Verified this session:
  `which python3` returns nothing (no output). Pinned znc at
  `$HOME/safebin/znc`. Pure Zag only. No python, no C, no JS, no Rust
  in implementation, scoring, or analysis. Absolutely no python3/python
  invocation at any step (lesson from the retry's disclosed deviation).
- Git: `/usr/bin/git` directly (the safebin `git` symlink is known-broken
  for writes per AGENTS.md). Commits local, explicit pathspecs confined
  to `ivwc_nontransductive/`, never pushed.
- Prereg commit (PREREG.md + NAMECHECK.md) strictly precedes the
  implementation commit.

## Step 1: What is being built

`src/ivwc_nontransductive.zag`: verbatim copy of
IVWC-CASEBIAS-RETRY's world/belief/composer/stepper/verifier/seeds
(sealed (bucket, eff) pairs bit-identical; K3/K4 anchors verify), with
the SENS machinery REMOVED and the verdict structure as the experimental
variable:

- Train (learner): COMMIT, PREFF, CONSEQ (harness), LEARN (UCB bucket
  bias recomputed), then BAR: T_fixed = mean over the 24 train cases of
  (preff_tr - bucb[bkt_tr]) (integer division; preregistered
  expectation 12). No sealed data, no researcher-set constant.
- Sealed loop sh=0..2 (wp=15/30/45), seeds verbatim:
  - COMMIT (learner): preff, adjV_ucb = preff - bucb[bkt]. No world
    calls.
  - Learner verdicts: A1 = (adjV_ucb > TV_ucb), TV_ucb = mean sealed
    adjV_ucb (transductive); A2 = (adjV_ucb > T_fixed)
    (non-transductive).
  - Anchors OF/X3/HYB/MG re-scored in-program.
  - SCORING (harness, fenced): world_execute per case (WC-FINAL=60
    total), labels ge = (eff >= Tpred), nphantom counts from the true
    world, D1b/D2b biases (+40 iff nphantom>0, resp. rotated-by-7),
    verdicts A3 = (d1adj > TV_d1b), A4 = (d1adj > T_fixed), A5 =
    (d2adj > TV_d2b), A6 = (d2adj > T_fixed).
- The ONLY difference between V_T and V_N arms is the scope of the
  mean bar (sealed batch vs train). Bias content is identical within
  each bias row, so the 2x2 isolates the verdict structure.

## Step 2: Diet declaration

24 train cases at wp=15 (seeds verbatim). Sealed: 12 cases each at
wp=15/30/45 (seeds verbatim). Labels ge live only in SCORING. No sealed
truth reaches the learner. The fenced D1b/D2b diagnostics use true-world
phantom counts exactly as in the retry (harness-only, never
learner-visible). The word "oracle" is avoided entirely.

## Step 3: Mechanism predictions (preregistered before implementation)

See PREREG.md (frozen). Headline: A4 (D1b x non-transductive) @15 =
11/12, errors exactly {s=5}: the theoretical ceiling of the (D1b x
threshold-verdict) family (proof: s=5 at adjV=-16 must PASS while s=3
at adjV=-6 must FAIL; no threshold separates them). The transductive
bar scores 3 below this ceiling (A3 = 8/12); the non-transductive bar
attains it. A2 (UCB x non-transductive) @15 = 10/12 {s=0,s=3}: the
fixed bar loses UCB's load-bearing strict-margin tie-break at TV=13,
so the bar change is not a general improvement, it specifically
un-blocks large corrections. A4 @45 = 12/12; A4 @30 = 11/12 {s=2} >
A3 @30 = 10/12. A6 @15 = 8/12 < A4: the gain is signal content.

## Step 4: Answers to the task's key questions (preregistered positions)

1. 12/12 @15 with D1 under a non-transductive verdict? Predicted NO
   (11/12 = ceiling). The bar was the bottleneck for 3 of D1's 4
   errors; the 4th is binary-bias crudeness (s=5, true-positive phantom),
   unfixable by any threshold verdict.
2. Right non-transductive structure? Train-scoped mean bar: same
   statistic as TV, train scope; corrections cannot move it.
3. Generalize or overfit? Predicted: no overfit to the phantom signal
   (K8), but no adaptation to law change either (A2 degrades @30/@45
   vs A1; the transductive bar's virtue is adaptation, its vice is
   chase-down).
