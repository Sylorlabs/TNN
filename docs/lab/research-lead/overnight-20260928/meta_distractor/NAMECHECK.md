# NAMECHECK: META-DISTRACTOR (Option C: distractor-then-original)

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
(`~/workspace/docs/lab/research-lead/overnight-20260928/meta_distractor/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first commit
contains ONLY PREREG.md (fresh, v1) and NAMECHECK.md (Step 0 + this design
record). The Zag source, binary, run logs, and REPORT.md come in later
commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

META-DISTRACTOR tests the last untested option of META-GENERALIZE's honest
boundary ("Options B (different task family) and C (distractor-then-
original) remain untested"): Option C, with the LEARNER FROZEN.

Sequence (frozen): 24 episodes of Bernoulli bias learning (LM2's original
family; the family question was Option B's, left UNDECIDED by C419, and is
not re-litigated here). Phase D (distractor), episodes 1-12: 9 typical
episodes use r* = PRNG permutation of {16..24} (mean 20; MG's validated
distribution, opposite side of 50 from the original), 3 atypical episodes
(idx 3,7,11) use a permutation of {40,47,54}. Phase R (return to original),
episodes 13-24: 9 typical episodes (idx 12,13,14,16,17,18,20,21,22) use r*
= PRNG permutation of {76..84} (mean 80; LM2's original distribution), 3
atypical episodes (idx 15,19,23) use a permutation of {40,47,54}. N=1200
flips per episode per condition; independent streams per condition
(SEED_T treatment, SEED_C control; SEED_B shared parameters). The learner
is LM2's frozen shrinkage estimator; treatment accumulates (sum, count),
control resets m=50 every episode.

Why this distractor: the 20-location is the validated MG distribution, so
Phase D is a replication-with-new-seeds (manipulation check), and 20 sits
on the opposite side of the naive 50 from 80, maximizing the shift's
stringency: the distractor prior (~26) ends up FARTHER from the original
typicals (80) than even the naive prior (50).

Mechanism-derived predictions (frozen before the run):
- Treatment enters Phase R with m = floor(321/12) = 26 DETERMINISTICALLY
  (9x20 + 40+47+54 = 321 regardless of permutation order). Control m=50.
- Phase-R typicals: treatment drifts from ~26 (distance ~54), control from
  50 (distance 30) -> treatment slower: ADV_R < 0 (INTERFERENCE).
- As Phase-R reveals (~80s) accumulate, m climbs 26 -> ~49: treatment's own
  etc decreases across Phase R (RECOVERY), approaching but not beating
  control within 12 episodes (full return to ~80 needs ~100+ reveals).
- Phase-R atypicals (40,47,54): treatment m ~= 37..49 is CLOSER than
  control's 50 -> treatment faster: ADV_O2 > 0 (REVERSAL of LM2's
  signature; the distractor helps exactly where the original prior hurt).
- Phase D replicates MG: ADV_D > 0, ADV_OD < 0.

The atypical set {40,47,54} repeats across phases BY DESIGN (both phases
use their historically validated distributions); within-phase parameters
are all distinct. The B4 novelty bar is defined per-phase accordingly.

Pre-prereg design-phase work (all in /tmp, never in the lane; no frozen
experiment executed):
- `/tmp/cal_md.zag`: threshold-calibration Monte Carlo, pure Zag,
  znc-compiled. Replicates the EXACT frozen learner (verbatim `etc_ep`;
  `run_cond` with the 24-episode loop bound) under the Option C design
  over R=1000 reps with fresh non-overlapping seeds
  (51,000,000+7*rep+{0,1,2}, disjoint from the frozen 20261013/14/15 and
  all earlier seeds). Power analysis, not seed selection: no frozen-seed
  outcome was observed or selected. Results recorded in PREREG.md
  Section 5 and used SOLELY to set frozen thresholds.
- C419 lesson applied: adequate power demanded on the primary bar, and the
  floor-validity bar uses a luck-robust MEDIAN over the 9 naive control
  typicals per phase (not T1 alone, which tripped C419's luck tripwire at
  calibrated P ~= 0.31).
- Calibration CORRECTED one design hypothesis: the predicted "reversal"
  (ADV_O2 > 0, distractor helping on block-R atypicals) does not hold --
  MC gives ADV_O2 mean -8, sd 99 (~0). Reason: which atypical value lands
  on the early block-R episodes is permuted, so the distractor prior is
  sometimes closer and sometimes farther, averaging to ~0. ADV_O2 is
  therefore report-only in the prereg (predicted ~= 0), not a bar. This is
  what the calibration is for; the prereg records the corrected prediction.
- Frozen seed triple for the experiment: SEED_B=20261013,
  SEED_T=20261014, SEED_C=20261015 (consecutive, disjoint from LM2's
  20261004/05/06, MG's 20261007/08/09, FB's 20261010/11/12, and all
  calibration seeds; fixed in PREREG before implementation).

## Build record

- 2026-10-03: `md1.zag` written by copying frozen `lm2.zag` and applying
  ONLY the seven prereg-permitted change classes (a)-(g): (a) `gen()`
  two-block parameter assignment (block-D {16..24}/{40,47,54}, block-R
  {76..84}/{40,47,54}) with 24-episode loops; (b) seeds 20261004/05/06 ->
  20261013/14/15; (c) arena offsets/sizes for 24 episodes (fT 28800 at 200,
  fC at 29000, eT/eC at 57800/57896, tmp regions, medscratch);
  (d) threshold literals (B5a sign, B5b 75, B5c 150, B5d medians 25,
  B5d2 365, B5g sign, MARG [12700,15700]); (e) header/output label strings
  (MD1, E01..E24, ADV_D/ADV_R/ADV_OD/ADV_O2, neutral identifiers);
  (f) malloc 32768 -> 65536; (g) `med9` median helper for the B5d floor.
  Full diff vs `lm2.zag` audited hunk-by-hunk: `etc_ep` byte-identical;
  `run_cond` differs ONLY in the loop-bound literal 12 -> 24; no other
  learner-code changes. B7 case-insensitive grep for the frozen 29-word
  list returns empty (one pre-build catch: a comment containing "biases"
  tripped the "bias" substring; reworded to "parameters", rebuilt).
  Compiled with pinned safebin znc -> `md1_bin`; one A0101 analyzer
  warning, confirmed false positive (max index fbase+e*1200+1199, in
  bounds; same warning class as LM2/MG/FB, learner code unchanged).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `4f30fbf2311113f4fc314d8517605d2ffa840974077c839680e46aa40b2b1ea7`
  (run1/2/3.txt). The pre-comment-fix binary produced the identical digest,
  confirming the fix touched only a comment.
- 2026-10-03: REPORT.md written. Frozen verdict: INTERFERENCE
  DEMONSTRATED (B5a PASS: ADV_R=-680 <= 0; B5d PASS: MEDCD=73, MEDCR=66;
  B5d2 PASS: ADV_D=718 >= 365). Secondary bars B5b/B5c missed on unlucky
  late treatment streams (E21=429, E23=232); the prior recovered
  monotonically (m: 26 -> 49) but first-passage noise swamped the recovery
  sums. Details in REPORT.md.
- Commit order self-check: prereg v1 (c9fba0a) + v1.1 amendment (b1eb484)
  strictly before this implementation commit. PASS (B1).
