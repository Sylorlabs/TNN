# NAMECHECK: LIFETIME-META-2 (examples-to-criterion decrease with experience)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- Safebin contents: 49 entries (coreutils, git, awk, sed, grep, cmp, diff,
  sha256sum, znc, ...); no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/lifetime_meta2/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first commit
contains ONLY PREREG.md (this file, v1 fresh) and NAMECHECK.md (Step 0 +
this design record). The Zag source, binary, run logs, and REPORT.md come
in later commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

LM2 follows up LM1's split finding (B5b PASS / B5a FAIL) per the LM1b
recommendation: primary bar on cluster episodes only, recalibrated
thresholds, independent flip streams per condition.

Pre-prereg design-phase work (all in /tmp, never in the lane; no frozen
experiment executed):
- `/tmp/cal.zag`: threshold-calibration Monte Carlo, pure Zag, znc-compiled.
  Replicates the exact frozen mechanism (w=20, tol=5, N=1200, cluster
  {76..84}, outliers {40,47,54} on episodes 4/8/12, independent streams,
  same LCG) over R=1000 reps with fresh non-overlapping seeds
  (1,000,000+7*rep+13 etc., disjoint from frozen 20261004/05/06).
  One A0101 analyzer warning (false positive, same class as LM1: max flip
  index is N-1, in bounds). Results recorded in PREREG.md Section 5 and
  used SOLELY to set frozen thresholds (power analysis, not seed
  selection): ADV_C mean=724 sd=271; ADV_O mean=-275 sd=194;
  T1 mean=104 sd=81; DEC mean=259 sd=252; STAB mean=18 sd=77;
  cap-hit rate ~0.004%/episode-run at N=1200.
- Design decisions from the calibration: cluster mean moved 70->80 to
  enlarge the naive-vs-informed gap (LM1 recommendation #4; learner
  mechanism unchanged); N=600->1200 after the calibration showed the naive
  learner's right tail hitting the 600 cap (~6%/run VOID risk -> ~0.1%);
  B5c loosened 24->150 (LM1's 24 was noise-impossible: calibrated sd=77);
  B5e replaced (T_1==C_1 identity cannot hold under independent streams).

## Build record

- 2026-10-03: `lm2.zag` written (8768 bytes, neutral identifiers; B6/B7
  audits pass -- B7 case-insensitive grep clean after renaming the printed
  `BIASID` label to `PARID`). Compiled with pinned safebin znc -> `lm2_bin`
  (38037 bytes); one A0101 analyzer warning, confirmed false positive
  (max flip index fbase+e*1200+1199, in bounds).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `1a68561a44809c804bc8d7c1775d68595cf220d4abc0fe87feea1f40d5b0bcba`
  (run1/2/3.txt).
- 2026-10-03: REPORT.md written. Frozen verdict: META-LEARNING
  DEMONSTRATED (cluster episodes). All bars PASS: B5a 672>=350 (primary),
  B5b 179>=75, B5c -31<=150, B5d 63>=25, B5e (PARID=XDISJ=MARG=1),
  B5f (max etc 157<=1200), B5g -86<=0, B4/B6/B7 pass. Observed ADV_C=672
  vs calibration mean 724: the LM1 split finding (real learning on
  typical episodes) survives proper experimental design.
- Commit order self-check: prereg 77b1a98 (PREREG.md + NAMECHECK.md only)
  strictly before this implementation commit. PASS (B1).
