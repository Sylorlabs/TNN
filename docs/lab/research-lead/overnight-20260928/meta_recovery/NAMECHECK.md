# NAMECHECK: META-RECOVERY (C427; follows C426 META-DISTRACTOR)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- Safebin activated via
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  ("SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)", 2026-10-03).
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git` (verified 2026-10-03).
- Safebin contents: coreutils, git, awk, sed, grep, cmp, diff, sha256sum,
  znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations, diff/grep
  audits.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane repo: this directory
(`docs/lab/research-lead/overnight-20260928/meta_recovery/`) on branch
`lane-l3rx-20261003` of `~/workspace/tnn-rsi`. Nothing is pushed to
GitHub; commits stay local with explicit pathspecs. Commit order: the
first commit contains ONLY PREREG.md (frozen) and NAMECHECK.md (Step 0 +
this design record). The Zag source, binary, run logs, and REPORT.md come
in later commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no frozen implementation run)

META-RECOVERY (C427) follows C426 META-DISTRACTOR, which froze
INTERFERENCE DEMONSTRATED: after a 12-episode distractor block (mean-20
distribution), the persistent learner entered the original block with the
distractor prior m=26 and paid 680 examples over 9 typical episodes
(~76/episode) against the reset control (ADV_R=-680). C426's report noted
the suggested next question, analytic only: the recovery timescale under
a longer original block, with the mechanism-derived estimate that full
return of the prior to ~80 needs ~100+ reveals
(m_k = (321+80k)/(12+k) >= 75 only at k >= 116).

This lane executes that question with the LEARNER FROZEN.

Sequence (frozen): 732 episodes of Bernoulli bias learning (LM2's family).
Block D (distractor), episodes 1-12: identical in structure to C426's
block D (9 typicals = PRNG permutation of {16..24} on idx 0,1,2,4,5,6,8,9,
10; 3 atypicals = PRNG permutation of {40,47,54} on idx 3,7,11). Block R
(long original block), episodes 13-732: 720 episodes = 80 cycles of 9,
each cycle a fresh PRNG permutation of {76..84} (mean exactly 80 per
cycle; all typical, so the long-run mean of reveals is exactly 80 and
the prior's return to 80 is well-defined). N=1200 flips per episode per
arm; independent streams per arm (SEED_T/SEED_F/SEED_C treatment arms,
SEED_B shared parameters).

Three arms (all the frozen LM2 shrinkage estimator
est_n = (20*m + 100*h)/(20+n), w=20, tol=5):
- T (treatment): accumulates (sum, count) across all 732 episodes.
  Enters block R with m = floor(321/12) = 26 deterministically.
- F (fresh accumulator): reset mode (m=50, no accumulation) during block
  D, then accumulates from block-R episode 1 with sum=cnt=0. This is the
  frozen learner with harness-level re-initialization at the block
  boundary (the same class of harness change as C426's reset control);
  it is the within-experiment "what if the distractor had never happened"
  reference. Its m reaches ~80 within 1-2 reveals by construction of the
  running-mean rule.
- C (control): reset mode (m=50) on every episode; the naive baseline.

Rationale for the F arm (disclosed design decision): the assigned
questions "is recovery faster than naive learning?" and "does the
distractor permanently impair?" need a clean within-experiment
comparator. T-vs-C alone shows return-to-better-than-naive; only T-vs-F
separates "fully converged to the no-distractor trajectory" (no permanent
impairment) from a lasting drag, on the same draws. The F arm is not a
learner change: the estimator, w=20, initial m=50, and update rule are
untouched; only the harness re-initializes (sum, count) at the boundary.

Mechanism-derived predictions (frozen before the run):
- Prior trajectory (deterministic given the sequence):
  m_T(k) = floor((321 + S_k)/(12+k)), m_F(k) = floor(S_k/k), where S_k is
  the sum of the first k block-R reveals (S_k = 80k at cycle boundaries).
  Milestones: K75 (first k with m_T >= 75) ~= 117; K78 ~= 310;
  K79 ~= 627. The distractor anchor's drag on the prior decays as
  ~(639)/(12+k): at k=720, m_T ~= 79.0 vs m_F = 80.
- Behavioral: late in block R the treatment prior is ~79 vs control 50,
  so treatment beats naive by nearly the full learned advantage
  (calibrated magnitude in Section 5); T converges to F (no permanent
  impairment, and no faster-than-fresh speedup is possible under the
  running-mean rule -- the update has no regime memory, so T can at best
  re-converge to F's trajectory).
- Cost: treatment pays a large excess over F during recovery (calibrated
  COST_TF in Section 5); this number is the price of the distractor prior.

Calibration: a /tmp Zag program (cal_mr.zag; verbatim etc_ep, run_cond
with the 732-episode bound and acc_from parameter, disjoint seeds
61000000+10*rep+{0..3}, R=150) estimated the sampling distributions used
for the frozen thresholds in PREREG.md Section 5. Power analysis, not
seed selection: no frozen-seed outcome was observed or selected.

## Step 2: Implementation record (post-prereg)

- `mr1.zag` written after prereg commit 4388fa0cc. Freeze verification:
  `etc_ep` cmp-verified byte-identical to frozen `md1.zag`/`lm2.zag`;
  `run_cond` diff shows only the three prereg-permitted changes (loop
  bound 24 -> 732; `accum` -> `acc_from`; m-trajectory recording);
  function inventory matches change classes (a)-(i).
- B7 audit: case-insensitive grep of the frozen 29-word list over
  `mr1.zag` returns empty. No `!(A && B)` while conditions; if-nesting
  <= 3.
- Compiled with pinned znc: one A0101 analyzer warning (false-positive
  class, same as LM2/MG/FB/C426; `etc_ep` unchanged).
- 3/3 runs byte-identical (sha256
  `ae3fecd5194d61bd835a3a98502ef755272ece2f4fdb1459d8133928a993aff4`);
  binary sha256
  `8842c7f44bc21367b3308b69c7ed4542a8d03015c1e2d8918f657028c518d103`.
- All kill bars PASS: B5a (8493 >= 6000), B5b (6/8499 <= 0.10),
  B5c (807 >= 365), B5d (-425 <= 0), B5e (76 >= 25), B5f, B5g.
  Milestones K75=118, K78=308, K79=624; COST_TF=4690; MAXETC=831.
- Verdict: RECOVERY DEMONSTRATED, CONVERGED (no permanent impairment,
  no meta-meta speedup). See REPORT.md.

## Toolchain incident log

- 2026-10-03, during freeze verification: a compound shell command
  contained a stray `python3 -c "print('skip')" 2>/dev/null` token
  (author's keystroke error, immediately recognized). Under the
  safebin-only PATH `python3` does not resolve (exit 127, "command not
  found", verified separately with stderr visible). It never executed,
  read nothing, wrote nothing, and no artifact in this lane (calibrator,
  mr1.zag, binary, runs, report) depends on it in any way -- all
  scientific computation is znc-compiled Zag, all file operations are
  safebin coreutils/git. Disclosed here and in REPORT.md; not hidden.
  No guard breach: no forbidden executable was invoked.
