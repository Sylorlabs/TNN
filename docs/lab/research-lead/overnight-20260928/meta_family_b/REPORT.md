# REPORT: META-FAMILY-B -- Does the LM2 meta-learning transfer to a different task family?

## Frozen verdict: UNDECIDED

Per the frozen verdict mapping's precedence bullet ("B5d fail: UNDECIDED"),
the headline verdict is UNDECIDED: the floor-validity bar fired (T1 = 14 <
25, the pre-registered luck tripwire, calibrated P ~= 0.31), so this
instantiation cannot discriminate. The primary bar was also unmet
(ADV_C = 267 < 343), but on a positive, in-direction advantage at the 22nd
percentile of the calibrated sampling distribution -- an ordinary
underpowered draw, not a signature mismatch. Nothing was weakened or
reinterpreted. This run licenses NEITHER a transfer claim NOR a
family-specificity claim.

## What was built (pure Zag, safebin-only)

- `fb1.zag`: the LM2 experiment with ONLY the task family changed
  (Bernoulli bias learning -> Poisson rate learning). 12 episodes; hidden
  integer parameter r* per episode (hundredths); 9 episodes (idx
  0,1,2,4,5,6,8,9,10) use r* = PRNG permutation of {76..84} (mean 80,
  UNCHANGED location from LM2); 3 episodes (idx 3,7,11) use r* =
  permutation of {40,47,54} (unchanged). N=1200 positions per episode per
  condition; per position, one 31-bit LCG draw u, observation = smallest
  j in 0..15 with u < t[j], t[j] = round(2^31 * P(X<=j)) for
  X ~ Poisson(r*/100), computed per episode in integer fixed point
  (10^9 scale; e^-x alternating series; t[15] forced to 2^31; genfail
  self-checks on table sanity). Independent streams per condition
  (SEED_T=20261011 treatment, SEED_C=20261012 control; SEED_B=20261010
  for the shared parameter permutation). Learner: est_n =
  (20*m + 100*h)/(20+n); treatment m = floor(mean of past revealed r*),
  control m = 50 always. Criterion |est_n - r*| < 5, smallest n in
  1..1200, else 1201.
- Learner freeze verified: full diff of `fb1.zag` vs frozen `lm2.zag`
  shows ONLY the six prereg-permitted change classes (header comments;
  `draw` + `ptab` + CDF-inversion observation loops replacing the
  binary-flip loop; seeds 20261004/05/06 -> 20261010/11/12; MARG comment
  reworded with bounds unchanged; B5a literal 350 -> 343; label string
  LM2 -> FB1; arena layout +128 bytes threshold scratch). `etc_ep` and
  `run_cond` are byte-identical (no diff hunks in their ranges).
- Commit order honored: prereg v1 (71d6ee7, PREREG.md + NAMECHECK.md
  only) strictly before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/
  node all unresolvable; one A0101 analyzer warning, confirmed false
  positive (max observation index fbase+e*1200+1199, in bounds; same
  warning class as LM2/MG, learner code unchanged). DISCLOSED: one stray
  shell fragment in an audit command referenced `python3`; under the
  safebin-only PATH it did not resolve (command not found) -- verified no
  python files exist in ~/safebin and no python process ran. Zero
  execution, zero involvement in any computation. The guard worked as
  designed (forbidden executable unresolvable). Recorded here and in
  NAMECHECK.md Step 0 rather than hidden.
- Determinism: 3/3 runs byte-identical,
  sha256 `815edbab7f1965c4139a2f0049ee801bb0de8fc5f4748233f3936256cce53157`.

## Results (frozen binary output, 3/3 identical)

```
E01 P=76 ET=14 EC=33
E02 P=77 ET=1  EC=44
E03 P=78 ET=7  EC=27
E04 P=40 ET=110 EC=3
E05 P=83 ET=28 EC=147
E06 P=80 ET=1  EC=7
E07 P=81 ET=64 EC=73
E08 P=54 ET=26 EC=1
E09 P=79 ET=3  EC=35
E10 P=82 ET=40 EC=46
E11 P=84 ET=3  EC=16
E12 P=47 ET=17 EC=1
ADV_C=267 ADV_O=-148 T1=14 C1=33 TLATE=46 TMID=93
B5A=0 B5B=0 B5C=1 B5D=0 B5E=1 B5F=1 B5G=1
DISTINCTB=1 DISTINCTF=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg 71d6ee7 implementation-free, predates all
  implementation commits).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded; the stray `python3`
  fragment did not resolve and never executed; disclosed above).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 distinct parameters; 24 observation vectors
  pairwise distinct).
- B5a TYPICAL-ADVANTAGE (PRIMARY): FAIL (267 < 343).
- B5b DECREASE: FAIL (3*14-46 = -4 < 75).
- B5c STABILITY: PASS (46-93 = -47 <= 150).
- B5d FLOOR-VALIDITY: FAIL (14 < 25) -> verdict UNDECIDED per frozen mapping.
- B5e STREAM-VALIDITY: PASS (PARID=1; XDISJ=1; MARG=1: per-condition
  observation totals within [6480,12240]).
- B5f APPARATUS: PASS (max etc 147 <= 1200, genfail 0).
- B5g NEGATIVE-TRANSFER: PASS (-148 <= 0; sign as predicted).
- B6 NO-RESEARCHER-META-RULE: PASS (learner fns byte-identical to frozen
  LM2; update's only input is the revealed r*; only the six permitted
  diff classes).
- B7 OPAQUE-IDS: PASS (labels E01..E12; case-insensitive grep for the
  frozen 21-word list returns empty).

## Reading of the result

The frozen mapping's precedence bullet decides the headline: B5d failed,
so the verdict is UNDECIDED -- the naive learner's episode-1 draw
(T1=14) tripped the pre-registered luck tripwire (calibrated P ~= 0.31),
and the prereg says that outcome is "UNDECIDED (task too easy; redesign),
never a pass." B5b's failure is the tripwire's mechanical consequence:
with T1=14 it needed TLATE <= -33, impossible by construction.

B5a's failure needs the honest quantitative reading, not a binary one.
ADV_C = 267 is a POSITIVE, substantial advantage (~30 saved examples per
typical episode): treatment's typical mean is 17.8/episode vs control's
47.6/episode. Against the design-phase calibration (mean 715, sd 591),
267 sits at z = -0.76, the 22nd percentile -- an ordinary draw under a
74%-power bar, not a signature mismatch. What compressed it on this draw:
(a) control luck -- five typical episodes at EC = 7, 16, 27, 33, 35
against a calibration mean of ~112; (b) atypical-pollution slowing
treatment mid-run -- after the E04 (r*=40) and E08 (r*=54) reveals,
m ~= 71-72 sits 8-11 below typical r* ~= 81-84, so E07 (ET=64) and E10
(ET=40) needed drift. Both effects are inside the calibrated sampling
distribution (ADV_C min was -1100).

The mechanism's signature is visibly intact IN THE NEW FAMILY: the
learned prior (m -> ~73) does the work on typical episodes and hurts on
atypical ones -- treatment slower than control on all three atypical
episodes (110v3, 26v1, 17v1; ADV_O = -148, B5g PASS with the predicted
sign). A byte-identical Bernoulli-bias learner exhibits the full
empirical-Bayes signature (speedup on typicals, interference on
atypicals) under Poisson count observations it was never designed for.

Why this is UNDECIDED and not "NO TRANSFER (family-specific)": that
label would assert the effect is family-bound, i.e. absent here. The
data show the effect present (+267, correct interference signature).
Why it is not transfer either: the primary bar was not met, and the
floor tripwire fired. A 74%-power bar plus a 22nd-percentile draw plus a
fired luck tripwire = a non-discriminating run. The prereg anticipated
exactly this compound outcome and named it UNDECIDED.

Redesign implication (for a FUTURE fresh prereg, not executed here): the
B5d tripwire fired at its calibrated rate; a luck-robust floor (e.g.
median over early naive episodes rather than T1 alone) and/or a
higher-power design (more typical episodes; the Poisson family's per-
observation noise is the price of the family change) would discriminate.
Option C (distractor-then-original) remains untested either way.

## Honest boundaries

- This run discriminates nothing about cross-family transfer: UNDECIDED
  is a statement about the run, not about the hypothesis. Do not cite
  this experiment as evidence for OR against family-generality.
- What would have been learned is the PRIOR MEAN over parameters:
  empirical-Bayes base-rate learning (L1/L2-ish), same as LM2/MG. Not
  strategy invention, not L3.
- The truth-reveal per episode is supervised; within-episode learning has
  zero feedback.
- One frozen family, one frozen seed triple (20261010/11/12), fixed
  before implementation; no seed selected on outcomes.
- Nominal power on the primary bar was ~74% (stated in prereg, not
  hidden): the Poisson family is noisier per observation than Bernoulli,
  so the same 0.48x-mean bar principle buys less power. The bar was not
  moved to chase power.
- The ~4.5% per-run B5f VOID risk stated in the prereg did not
  materialize (max etc 147, GENFAIL=0).

## Artifacts in this commit

- `fb1.zag`: frozen implementation (learner byte-identical to `lm2.zag`;
  B6/B7 audited).
- `fb1_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `815edbab7f1965c4139a2f0049ee801bb0de8fc5f4748233f3936256cce53157`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
