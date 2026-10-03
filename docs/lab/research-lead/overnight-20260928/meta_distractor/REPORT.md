# REPORT: META-DISTRACTOR -- Does a distractor distribution interfere with subsequent learning on the original distribution?

## Frozen verdict: INTERFERENCE DEMONSTRATED

Per the frozen verdict mapping, B5a (primary, original-block typical
advantage) PASSED (ADV_R = -680 <= 0) with B5d (luck-robust floor) PASS
(MEDCD=73, MEDCR=66) and B5d2 (manipulation) PASS (ADV_D=718 >= 365), so
the preregistered headline verdict is INTERFERENCE DEMONSTRATED: the
distractor distribution's learned prior interferes with subsequent
learning on the original distribution. The LM2 meta-learning is NOT
robust to distribution shift. Nothing was weakened or reinterpreted.

## What was built (pure Zag, safebin-only)

- `md1.zag`: the LM2 experiment with ONLY the episode sequence changed
  (Option C: distractor-then-original). 24 episodes of Bernoulli bias
  learning; hidden integer parameter p* per episode; N=1200 flips per
  episode per condition from INDEPENDENT streams (SEED_T=20261014
  treatment, SEED_C=20261015 control; SEED_B=20261013 shared parameters).
  Block D (episodes 1-12): 9 use p* = PRNG permutation of {16..24}
  (mean 20; MG's distribution), 3 (idx 3,7,11) use permutation of
  {40,47,54}. Block R (episodes 13-24): 9 use p* = permutation of
  {76..84} (mean 80; LM2's original), 3 (idx 15,19,23) use permutation of
  {40,47,54}. Learner: est_n = (20*m + 100*h)/(20+n); treatment m =
  floor(mean of past revealed p) carried across all 24 episodes, control
  m = 50 always. Criterion |est_n - p*| < 5, smallest n in 1..1200, else
  1201.
- Learner freeze verified: full diff of `md1.zag` vs frozen `lm2.zag`
  shows ONLY the seven prereg-permitted change classes (a)-(g)
  (Section 3, incl. v1.1 amendment for the `med9` helper). `etc_ep` is
  byte-identical; `run_cond` differs ONLY in the episode-count loop-bound
  literal 12 -> 24 (harness change; estimator and update statements
  byte-identical).
- Commit order honored: prereg v1 (c9fba0a, PREREG.md + NAMECHECK.md only)
  and v1.1 amendment (b1eb484, adds permitted class (g); no bar changed),
  both strictly before any implementation file. This commit adds the
  implementation + report only.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/
  node all unresolvable; zero forbidden invocations. One znc analyzer
  warning (A0101 on `etc_ep`, same false-positive class as LM2/MG/FB;
  learner code unchanged). One pre-build B7 self-catch: a comment
  containing "biases" tripped the "bias" substring grep; reworded to
  "parameters" and rebuilt (pre-fix binary produced the identical digest,
  confirming the fix touched only a comment). Disclosed here, not hidden.
- Determinism: 3/3 runs byte-identical,
  sha256 `4f30fbf2311113f4fc314d8517605d2ffa840974077c839680e46aa40b2b1ea7`.

## Results (frozen binary output, 3/3 identical)

```
E01 P=23 ET=27  EC=31
E02 P=20 ET=7   EC=133
E03 P=18 ET=1   EC=85
E04 P=54 ET=41  EC=22
E05 P=17 ET=6   EC=153
E06 P=24 ET=1   EC=63
E07 P=19 ET=2   EC=35
E08 P=47 ET=144 EC=2
E09 P=21 ET=1   EC=23
E10 P=22 ET=4   EC=73
E11 P=16 ET=24  EC=195
E12 P=40 ET=16  EC=18
E13 P=78 ET=106 EC=62
E14 P=84 ET=119 EC=252
E15 P=76 ET=123 EC=39
E16 P=54 ET=182 EC=16
E17 P=80 ET=206 EC=89
E18 P=81 ET=97  EC=39
E19 P=77 ET=78  EC=66
E20 P=47 ET=1   EC=1
E21 P=82 ET=429 EC=72
E22 P=79 ET=84  EC=54
E23 P=83 ET=232 EC=121
E24 P=40 ET=11  EC=3
ADV_D=718 ADV_R=-680 ADV_OD=-159 ADV_O2=-174 T1=27 TEARLY=348 TMIDR=381 TLATE=745 MEDCD=73 MEDCR=66
B5A=1 B5B=0 B5C=0 B5D=1 B5D2=1 B5E=1 B5F=1 B5G=1
DISTINCTBD=1 DISTINCTBR=1 DISTINCTF=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
```

Bar scorecard:
- B1 COMMIT-ORDER: PASS (prereg v1 + v1.1 amendment strictly predate all
  implementation commits).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded, zero incidents).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 block-D biases distinct; 12 block-R biases
  distinct; 48 flip vectors pairwise distinct).
- B5a INTERFERENCE (PRIMARY): PASS (-680 <= 0).
- B5b RECOVERY: FAIL (348-745 = -397 < 75).
- B5c STABILITY: FAIL (745-381 = 364 > 150).
- B5d FLOOR-VALIDITY (luck-robust): PASS (MEDCD=73 >= 25, MEDCR=66 >= 25).
- B5d2 MANIPULATION: PASS (718 >= 365).
- B5e STREAM-VALIDITY: PASS (PARID=1; XDISJ=1; MARG=1: per-condition ones
  within [12700,15700]).
- B5f APPARATUS: PASS (max etc 429 <= 1200, genfail 0).
- B5g NEGATIVE-TRANSFER: PASS (-159 <= 0; sign as predicted).
- B5h MAGNITUDE: ADV_R=-680 is below the 0.48x level (-195): the
  interference exceeds the family's substantive magnitude level.
- B6 NO-RESEARCHER-META-RULE: PASS (learner fns verified; update's only
  input is the revealed p; no episode-conditioned logic; sum/cnt touched
  only by the update; only the seven permitted diff classes).
- B7 OPAQUE-IDS: PASS (labels E01..E24; case-insensitive grep for the
  frozen 29-word list returns empty).

## Reading of the result

The persistent learner entered block R with the distractor prior m=26
(deterministic: (9x20+40+47+54)/12) against the reset control's m=50, and
paid for it on the original distribution's typical episodes: treatment was
slower than control by 680 examples over 9 episodes (~76/episode),
ADV_R=-680, at the ~23rd percentile of the calibrated distribution on the
negative side (more interference than the calibrated mean of -406). The
manipulation check confirms the distractor was genuinely learned
(ADV_D=718 ~= calibrated mean 765; block D replicates MG's signature:
treatment typicals 27,7,1,6,1,2,1,4,24 vs control 31,133,85,153,63,35,23,
73,195). The reset ablation attributes the block-R slowdown to the
persistent distractor history: the ONLY treatment/control difference is
the accumulated (sum, count).

The mechanism's signature is intact and extended: the learned prior helps
on block-D typicals (+718) and hurts on block-D atypicals (-159, B5g PASS
with the predicted sign) -- and then hurts again on block-R typicals
(-680). This is the meta-learning analogue of catastrophic interference:
the "meta-knowledge" is a single-regime prior commitment that overwrites
when the distribution shifts, rather than a general learning-to-learn
improvement.

The two secondary misses (B5b, B5c) need the honest quantitative reading,
not a binary one. Both are driven by two unlucky late treatment streams:
E21 (ET=429, m=44, p*=82) and E23 (ET=232, m=48, p*=83), against control's
72 and 121 on independent streams. The prior itself recovered
monotonically exactly as the mechanism predicts -- m entering each
block-R episode: 26,30,34,37,38,40,43,44,44,44,46,48,49 -- but
first-passage etc noise (heavy right tail; calibrated DEC_R sd=247)
swamped the recovery sums on this draw (DEC_R=-397 sits at ~1st
percentile of the calibrated distribution). B5b/B5c are secondary bars;
their misses do not overturn the primary interference finding, and the
m-trajectory confirms the mechanism behaved as predicted.

ADV_O2=-174 (report-only, predicted ~= 0): more negative than the
calibrated mean (-8, sd 99; ~5th percentile), driven by E16's permuted
placement (P=54 on the early block-R episode where m~=37, so treatment
was far: 182 vs 16). This is the permuted-placement effect the
calibration identified: on block-R atypicals the distractor prior is
sometimes closer and sometimes farther, with no systematic sign. Reported
as preregistered, not a bar.

## Honest boundaries

- This is ONE shift scenario (20 -> 80, Bernoulli family, 12-episode
  blocks, w=20 inertia): the verdict is "interference under this shift,"
  NOT that all shifts interfere. Recovery speed and magnitude are
  specific to this design (full return to ~80 needs ~100+ reveals).
- What was learned is the PRIOR MEAN over biases: empirical-Bayes
  base-rate learning (L1/L2-ish), same as LM2/MG/FB. Not strategy
  invention, not L3. The estimator form, w=20, initial m=50 are
  researcher-supplied mechanism; the learned quantity is m.
- The truth-reveal per episode is supervised; within-episode learning has
  zero feedback.
- One frozen sequence, one frozen seed triple (20261013/14/15), fixed
  before implementation; no seed selected on outcomes.
- The primary bar was a sign bar (not the family's usual 0.48x magnitude
  bar) because the calibrated sd (377) left the magnitude bar
  underpowered (~71%); the directional prediction carried ~86% nominal
  power. The 0.48x level (-195) is reported as B5h: observed -680 clears
  it. Stated in the prereg, not hidden.
- C419 (Option B, cross-family) remains UNDECIDED and is not re-litigated
  here; this result does not imply cross-family generality.
- The generalization map is now complete: Option A (location) TRANSFER
  DEMONSTRATED (C415); Option B (family) UNDECIDED (C419); Option C
  (distractor-then-original) INTERFERENCE DEMONSTRATED (this experiment).

## Artifacts in this commit

- `md1.zag`: frozen implementation (learner byte-identical to `lm2.zag`
  modulo the preregistered loop bound; B6/B7 audited).
- `md1_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `4f30fbf2311113f4fc314d8517605d2ffa840974077c839680e46aa40b2b1ea7`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
