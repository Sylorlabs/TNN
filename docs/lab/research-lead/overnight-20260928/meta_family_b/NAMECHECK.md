# NAMECHECK: META-FAMILY-B (Option B: different task family)

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
(`~/workspace/docs/lab/research-lead/overnight-20260928/meta_family_b/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first commit
contains ONLY PREREG.md (fresh, v1) and NAMECHECK.md (Step 0 + this design
record). The Zag source, binary, run logs, and REPORT.md come in later
commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

META-FAMILY-B tests META-GENERALIZE's honest boundary ("Options B
(different task family) and C (distractor-then-original) remain untested")
via Option B: a DIFFERENT task family with the learner frozen.

Family choice (why Poisson rate learning): the frozen learner is a
shrinkage estimator of a running mean in hundredths,
est = (20*m + 100*h)/(20+n), where h accumulates the observations.
The task family is the (parameter, observation model, criterion) triple.
LM2/MG: parameter = Bernoulli bias, observations = binary flips,
noise = Bernoulli. New family: parameter = Poisson rate r* (hundredths,
e.g. 80 -> 0.80 events per position), observations = per-position
nonnegative integer counts drawn from Poisson(r*/100) by CDF inversion
against one 31-bit LCG draw per position. The parameter is a rate (not a
probability), the observations are counts (not bits), the noise model is
Poisson (variance = mean, not p(1-p)). The learner code is LITERALLY
unchanged (h now accumulates counts; the estimator form is identical), so
the family change is isolated as the single causal variable. A Gaussian
mean family was considered and rejected: with observations in hundredths
it would need est = (20*m + h)/(20+n), i.e. a learner change, violating
the frozen-learner constraint. A categorical-mode family was rejected:
the estimand is not a mean, so the shrinkage form does not apply.

Location held at LM2's (typical {76..84}, atypical {40,47,54}) so that
ONLY the family changes relative to LM2 (META-GENERALIZE already isolated
location). Naive-vs-informed gap held at 30 (|50-80|).

Pre-prereg design-phase work (all in /tmp, never in the lane; no frozen
experiment executed):
- `/tmp/cal_fb.zag`: threshold-calibration Monte Carlo, pure Zag,
  znc-compiled. Replicates the EXACT frozen learner (`etc_ep`,
  `run_cond` copied verbatim from frozen `lm2.zag`) under the NEW family
  (typical {76..84}, atypical {40,47,54} on episodes 4/8/12, independent
  streams, same LCG; Poisson observations via integer CDF-inversion
  tables with fixed-point e^-x series and genfail self-checks) over
  R=1000 reps with fresh non-overlapping seeds
  (41,000,000+7*rep+{0,1,2}, disjoint from the frozen 20261010/11/12 and
  all earlier seeds). Power analysis, not seed selection: no frozen-seed
  outcome was observed or selected. Results recorded in PREREG.md
  Section 5 and used SOLELY to set frozen thresholds.
- Design decisions from the calibration: B5a set at 0.48x calibrated
  ADV_C mean (same principle as LM2's 350 and MG's 370); B5b/B5c/B5d kept
  at the substantive levels 75/150/25; MARG bounds kept at [6480,12240]
  with the new meaning (per-condition TOTAL observation counts, not
  ones; expected 10332, sd ~102, ~19/38sd gross-fault check).
- Frozen seed triple for the experiment: SEED_B=20261010,
  SEED_T=20261011, SEED_C=20261012 (consecutive, disjoint from LM2's
  20261004/05/06, MG's 20261007/08/09, and all calibration seeds; fixed
  in PREREG before implementation).

## Build record

- 2026-10-03: `fb1.zag` written by copying frozen `lm2.zag` and applying
  ONLY the six prereg-permitted change classes: (a) header comments
  (neutral rewording), `draw` + `ptab` fns, and CDF-inversion observation
  loops replacing the binary-flip loop (typical-parameter literals
  UNCHANGED at 76+i); (b) seeds 20261004/05/06 -> 20261010/11/12;
  (c) MARG comment reworded, code and bounds [6480,12240] unchanged;
  (d) B5a literal 350 -> 343; (e) header label string LM2 -> FB1;
  (f) arena layout comment (+128 bytes threshold scratch at 29052).
  Full diff vs `lm2.zag` confirms no other changes; `etc_ep` and
  `run_cond` are byte-identical (extracted-function cmp). B7
  case-insensitive grep for the frozen 21-word list (coin, bias, heads,
  tails, shrink, prior, learn, meta, cluster, outlier, typical, atypical,
  general, poisson, rate, lambda, gauss, count, event, slot, family)
  returns empty (header reworded to "FB1 experiment" to avoid the "meta"
  substring, following MG's precedent); stale-literal grep (old seeds)
  returns empty; new seeds 20261010/11/12 confirmed.
  Compiled with pinned safebin znc -> `fb1_bin`; one A0101 analyzer
  warning, confirmed false positive (max observation index
  fbase+e*1200+1199, in bounds; same warning class as LM2/MG, learner
  code unchanged).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `815edbab7f1965c4139a2f0049ee801bb0de8fc5f4748233f3936256cce53157`
  (run1/2/3.txt).
- 2026-10-03: REPORT.md written. Frozen verdict: UNDECIDED (B5d floor
  failure: T1=14 < 25, the pre-registered luck tripwire at calibrated
  P~=0.31; precedence bullet of the frozen mapping). B5a primary also
  unmet (267 < 343) on a positive in-direction advantage at the 22nd
  percentile of the calibrated distribution -- an underpowered draw, not
  a signature mismatch (B5g -148 <= 0 with predicted sign; B5e/B5f/B4/B6/B7
  all PASS). The run licenses neither a transfer claim nor a
  family-specificity claim.
- Toolchain note (disclosed, see REPORT.md): one stray shell fragment in
  an audit command referenced `python3`; under the safebin-only PATH it
  did not resolve (command not found). Verified: no python* files in
  ~/safebin, `which python3` empty, no python processes. Zero execution,
  zero involvement in any computation. The guard worked as designed.
- Commit order self-check: prereg 71d6ee7 (PREREG.md + NAMECHECK.md only)
  strictly before this implementation commit. PASS (B1).
