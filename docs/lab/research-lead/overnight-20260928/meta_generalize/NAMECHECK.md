# NAMECHECK: META-GENERALIZE (transfer of LM2 meta-learning to a new distribution)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
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
(`~/workspace/docs/lab/research-lead/overnight-20260928/meta_generalize/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first commit
contains ONLY PREREG.md (fresh, v1) and NAMECHECK.md (Step 0 + this design
record). The Zag source, binary, run logs, and REPORT.md come in later
commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

META-GENERALIZE tests LM2's honest boundary ("one frozen task distribution,
one frozen seed triple; generalization untested") via Option A: a different
typical-cluster location (near 20 instead of near 80), learner frozen.

Pre-prereg design-phase work (all in /tmp, never in the lane; no frozen
experiment executed):
- `/tmp/cal_mg.zag`: threshold-calibration Monte Carlo, pure Zag,
  znc-compiled. Replicates the EXACT frozen learner (`etc_ep`,
  `run_cond` copied verbatim from `lm2.zag`) under the NEW distribution
  (typical {16..24}, atypical {40,47,54} on episodes 4/8/12, independent
  streams, same LCG) over R=1000 reps with fresh non-overlapping seeds
  (31,000,000+7*rep+{1,2,3}, disjoint from frozen 20261007/08/09).
  One A0101 analyzer warning (false positive, same class as LM2: max flip
  index is fbase+e*1200+1199, in bounds). Results recorded in PREREG.md
  Section 5 and used SOLELY to set frozen thresholds (power analysis, not
  seed selection): ADV_C mean=772 sd=262; ADV_O mean=-219 sd=175;
  T1 mean=99 sd=81; DEC mean=275 sd=248; STAB mean=-3 sd=50;
  cap-hit rate 0/24,000 episode-runs at N=1200.
- Design decisions from the calibration: gap held constant at 30
  (|50-20|, same as LM2's |80-50|) so only cluster LOCATION changes;
  atypical set unchanged ({40,47,54}); B5a set at 0.48x calibrated mean
  (370, same principle as LM2's 350); B5b/B5c/B5d kept at LM2's
  substantive levels (75/150/25); MARG bounds moved to [2880,5040]
  (=[0.20,0.35] of 14400; expected 3852, sd~53, ~18sd gross-fault check)
  because the new distribution's expected marginal differs.
- Frozen seed triple for the experiment: SEED_B=20261007,
  SEED_T=20261008, SEED_C=20261009 (consecutive, disjoint from LM2's
  triple and all calibration seeds; fixed in PREREG before implementation).

## Build record

- 2026-10-03: `mg1.zag` written by copying frozen `lm2.zag` and applying
  ONLY the five prereg-permitted change classes: (a) gen() typical-bias
  literals 76+i -> 16+i; (b) seeds 20261004/05/06 -> 20261007/08/09;
  (c) MARG bounds [6480,12240] -> [2880,5040]; (d) B5a literal 350 -> 370;
  (e) header/output label strings (neutral identifiers). Full diff vs
  `lm2.zag` confirms no other changes; `etc_ep` and `run_cond` are
  byte-identical (learner frozen). B7 case-insensitive grep for the frozen
  word list (coin, bias, heads, tails, shrink, prior, learn, meta, cluster,
  outlier, typical, atypical, general) returns empty; stale-literal grep
  (76+i, old seeds, >=350, old MARG bounds, "LM2) returns empty.
  Compiled with pinned safebin znc -> `mg1_bin`; one A0101 analyzer
  warning, confirmed false positive (max flip index fbase+e*1200+1199,
  in bounds; same warning class as LM2, learner code unchanged).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `23132878677f5f93c3f8953544e3d56b4b93645929e77f448b3213f9c94ce112`
  (run1/2/3.txt).
- 2026-10-03: REPORT.md written. Frozen verdict: TRANSFER DEMONSTRATED
  (new distribution). All bars PASS: B5a 679>=370 (primary),
  B5b 86>=75, B5c 21<=150, B5d 37>=25, B5e (PARID=XDISJ=MARG=1),
  B5f (max etc 244<=1200), B5g -166<=0, B4/B6/B7 pass. Observed ADV_C=679
  vs calibration mean 772 (0.35 sd): the mechanism's sampling distribution
  is location-invariant; LM2's effect is not tied to the 80-location.
- Commit order self-check: prereg 86d015d (PREREG.md + NAMECHECK.md only)
  strictly before this implementation commit. PASS (B1).
