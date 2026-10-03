# REPORT: Belief-Stance Trajectories Detect Source Defection (H-DECEPT-1, P1)

Wave: 2026-10-02. Verdict: BELIEF-DECEPTION-COMPLETE (with trajectory
analysis). All kill bars K1-K5 evaluated against the frozen PREREG.md.

## What was tested

The belief learner from C211/C223 (reliability from verification
outcomes only, independence discount, identity register, band derived
statuses) was exposed to two sealed-style world scripts, no source
changes between them:

- D1 (deception): source S builds rel 1000 over 20 correct rounds, then
  asserts a HIGH-STAKES (w=3) falsehood, contradicted by two independent
  weaker (w=2) sources telling the truth.
- R1 (reverse trap): S builds rel 1000 over 20 rounds, then tells an
  UNPOPULAR TRUTH (w=3), contradicted by two CORRELATED weak (w=1)
  sources (lockstep calibration history) telling falsehoods.

## Results

All 34 in-binary checks passed. 3/3 runs byte identical
(sha256 c9d421062f951e947b842513760dc1c133a43de311a83f8d5a40cf698c060de4).
Stdout byte verified with od -c spot check.

### D1 trajectory (the deception)

| step | rel(S) | stance | s1 | s2 |
|---|---|---|---|---|
| build rounds 15-20 | 1000 each | (no H1/H2 contact) | 0 | 0 |
| S strong false H1 | 1000 | 11 PROVISIONAL H1 | 3000 | 0 |
| + W1 moderate true H2 | 1000 | 12 UNCERTAIN lean H1 | 3000 | 2000 |
| + W2 moderate true H2 | 1000 | 22 UNCERTAIN lean H2 | 3000 | 4000 |
| exposure (S wrong) | 952 | 22 (unchanged) | 3000 | 4000 |
| post +1..+5 (all wrong) | 909, 869, 833, 800, 769 | 22 | 3000 | 4000 |

Finding (a): the learner REJECTS the falsehood. The stance moves
11 -> 12 -> 22 as independent evidence arrives: it first believes S
(S's 20-round record is real), wavers after one independent
contradiction, and sides with the two independent sources after the
second. The final 22 is rational 1/1 given the evidence: two
independent moderate claims (4000) outweigh one strong claim (3000),
and uncertainty is honest given S's genuine history. This is the
belief to deception transfer working at the instance level: weighted
independent evidence beats a high-reliability defector.

Finding (b): the downgrade is EXACTLY linear, not faster. Exposure moves
rel(S) 1000 -> 952 = 1000*20/21, and the five aftermath rounds trace
909/869/833/800/769 = 1000*20/(21+k) with zero deviation at every
point. The learner has no trajectory-shaped or stake-weighted
reliability update: a high-stakes betrayal after 20 correct rounds
moves reliability by exactly one instance, indistinguishable from any
ordinary error. The belief stance itself does not move on exposure;
the downgrade lives entirely in the source model.

### R1 trajectory (the reverse trap)

| step | stance | s1 | s2 |
|---|---|---|---|
| S strong true H1 | 11 PROVISIONAL H1 | 3000 | 0 |
| + W1 weak false H2 | 12 UNCERTAIN lean H1 | 3000 | 1000 |
| + W2 weak false H2 | 12 UNCERTAIN lean H1 | 3000 | 2000 |

The learner HOLDS WITH S. It does not follow the 2-vs-1 majority: the
machinery weights evidence (3000 vs 2000), it does not count heads.
Rational 1/1 given the evidence. Note the machinery cannot consume the
W1/W2 correlation (lockstep calibration is visible in history but
there is no correlation structure); it treats them as independent and
still loses 2000 < 3000. Correlation blindness is confirmed present
but non-decisive here.

### Rationality total: 2/2 (D1(a) 22, R1 12)

## Hypothesis verdict (frozen rule from PREREG.md)

H-DECEPT-1 holds iff (a) the learner rejects the falsehood (final D1
stance 22) AND (b) the downgrade is faster than linear
(rel(S) strictly below 952 at exposure or below 1000*20/(21+k) after).

(a) PASS. (b) FAIL, confirmed exact-linear at all six post-defection
checkpoints.

H-DECEPT-1 is NOT SUPPORTED as stated. The belief to deception
transfer is PARTIAL: instance-level rejection works (independent
weighting defeats the defector's claim), but the learner does NOT
recognize the defection TRAJECTORY as a pattern. Reliability learning
is purely instance based; there is no structure in the learner that
distinguishes "one error among many" from "a trust-building run
exploited by a high-stakes betrayal."

## What this specifies next

The missing mechanism is now precisely characterized: a
trajectory-shaped reliability update (e.g. a betrayal penalty keyed on
prior correct streak length times claim stake, or a source-stance
structure that records defection trajectories rather than just
correct/total fractions). That is the next hypothesis, not this one;
no such machinery was built or tested here. The exact linear null
values above (952; 909, 869, 833, 800, 769) are the frozen baseline
any candidate deception-pattern mechanism must beat.

## Kill bars

K1 PASS: 3/3 byte identical (sha256 c9d42106...).
K2 PASS: D1 build rel 1000/1000/1000; stance trajectory 11, 12, 22;
    s1 == 3000; s2 == 4000.
K3 PASS: exposure rel == 952; aftermath exactly 909/869/833/800/769;
    stance stays 22; zero evictions. Per the frozen verdict rule this
    CONFIRMS instance-only decay and FALSIFIES H-DECEPT-1(b).
K4 PASS: R1 stance trajectory 11, 12, 12; s1 == 3000; s2 == 2000;
    final st == 12 (holds with S, not the majority).
K5 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
    (safebin PATH, no python3/python present). Unfrozen variant only;
    frozen source untouched; paper untouched; nothing pushed; explicit
    pathspecs on all git operations.

## Artifacts

- PREREG.md (frozen, committed before implementation)
- NAMECHECK.md (toolchain guard Step 0 recorded)
- belief_deception.zag (source, pure Zag)
- belief_deception_bin (binary, 54692 bytes)
- compile.log (znc warnings only, same analyzer class as C223)
- run1.txt, run2.txt, run3.txt (byte identical outputs)

Architecture accounting: capability added 0 lines to the protected
core; new hardcoded semantic cases 0; modes/bridges/handlers 0;
learner-state structures created 0 (reused C211/C223 machinery with a
capacity constant change only).
