# PREREG_PART2: Constructor seed-sensitivity characterization (sum2 family)

Lane F1-FOLLOWUP, wave wave-20261001-2321pdt. This prereg is frozen
alone (separate commit from PREREG_PART1) before any Part 2 sealed
fixture is generated or any Part 2 sealed run executes. It
characterizes the greedy depth-1 trial constructor's seed-sensitivity
as its own investigation, independent of the trigger. The constructor
is the F1 frozen binary's constructor, used read-only; no
implementation work occurs in this lane. This is a finding, not a
claim: the verdict is CHARACTERIZED (with the overfit rate and the
identified pattern) or NOT-FOUND (if no pattern emerges).

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing. All work is pure Zag compiled by the pinned znc, or
shell invoking znc, running binaries, git ops, cmp/sha256sum, grep, and
file moves/copies. Any forbidden executable invocation is automatic
PROCESS-FAIL.

## 1. The observation to characterize

In F1's sealed evaluation, the greedy depth-1 trial constructor
(single-ISA-element insertions before the terminal WRITE, frozen ISA
order, strictly-improving argmin over the BUFN = 8 trial buffer)
overfits sealed seed 2301's sum2 train set (y = 2*(x0+x1)) to the
degenerate structure [ADD r0,f1,f1; ADD r0,r0,f1; ADD r0,r0,f0;
ADD r0,r0,f0], scoring 0/30 on the hidden set. The prior wave's binary
fails identically on the same fixtures, so this is a constructor
property, not a trigger regression. Informative negatives from F1 dev
(sum3 overfit, 0/30, also reproduced by the old binary) point the same
way. The question: on the R-W2-style world family, which seeds overfit
and why.

## 2. Sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs.
- Train: 24 episodes, x0 and x1 in 0..4 (rng range 0..5), truth shown.
- Hidden: 30 episodes, x0 and x1 in 5..14 (rng range 5..15), truth
  masked as ?. Truth paired file shares the (kind, seed, n) and shows y.
- Generator: F1's pure-Zag `f1_wgen` (kind sum2), copied read-only into
  this lane; binary behavior identical (verified by regenerating one
  F1 fixture and cmp-matching it before any sealed generation).

Fresh seed series (never used by dev 9000-series or F1 sealed
1100..3100 series): for i = 0..23 (N = 24 seeds),
- train seed = 5100 + 2*i
- hidden/truth seed = 5101 + 2*i

The seed series is frozen here; the generator is invoked only after
this prereg's commit. The fixture SHA-256 manifest is committed in
sealed2/FIXTURE_SHA256.txt before any sealed run begins.

## 3. Run protocol per seed

`f1_learn` (F1 frozen binary, sha256 verified before runs):
- train (seed state in) -> state/trace/pred
- hidden (masked, trained state in) -> pred
- 3/3 byte-identical reruns per seed (cmp-verified), 24 seeds.

Scoring: `f1_score acc <pred> <truth>` on the hidden set (frozen
pure-Zag scorer, copied read-only).

Classification (frozen):
- CORRECT: hidden accuracy at least 80 percent (24/30).
- OVERFIT: hidden accuracy below 80 percent.
The final main-graph signature (f1_score sig) is recorded for every
seed for structural bookkeeping.

## 4. Frozen feature set and pre-registered hypotheses

A pure-Zag analyzer (committed before the sealed runs; it implements
exactly the fields below) computes per seed, from the sealed TRAIN
fixture and the train trace:

Fixture properties (computable before running the learner):
- F1: number of distinct (x0,x1) pairs in the 24-episode train set
- F2: duplicate pair occurrences (24 minus F1)
- F3: episodes with x0 == x1
- F4: episodes with y == 0
- F5: number of distinct y values
- F6: episodes with x0 == 0 or x1 == 0

Learner-behavior properties (recorded for explanation, not for the
separation rule):
- F7: first CONSTRUCT event's op and operand pattern class
- F8: total CONSTRUCT events in the train trace
- F9: first TRIGGER episode

Pre-registered pattern hypotheses (fixture properties only):
- H1 (duplicates): overfit seeds have at least k duplicate pairs
- H2 (equal inputs): overfit seeds have at least k episodes with
  x0 == x1
- H3 (zero anchors): overfit seeds have at least k episodes with y == 0
- H4 (low diversity): overfit seeds have at most k distinct y values
- H5 (zero inputs): overfit seeds have at least k episodes with a
  zero input

Thresholds k are not pre-fixed numerically; for each hypothesis the
analyzer reports the full contingency table over all k and the best-k
separation is reported honestly with its k.

## 5. Frozen decision rule (finding-characterization bars)

CHARACTERIZED iff ALL of:
(a) all 24 seeds complete with 3/3 byte-identical reruns;
(b) the overfit rate is reported as an exact count (overfit / 24);
(c) at least one fixture property (F1..F6) separates the OVERFIT seeds
    from the CORRECT seeds with at most 2 total misclassified seeds on
    the frozen 24-seed set, and the property, its threshold, and its
    full contingency table are reported.

NOT-FOUND if no fixture property meets (c): then all hypothesis tables
are reported and the verdict is NOT-FOUND with the honest negative.

Consistency check (post-hoc, not part of the decision rule): compute
the identified property on F1's sealed rW2 overfit train fixture
(seed 2301) and report whether it shares the overfit property.

This characterization carries no kill bar, no promotion, and no L3
claim. It is evidence about the constructor's greedy trial, to inform
future constructor work.

## 6. Determinism standard

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of each raw
output recorded. Zero randomness in decision paths. Any
nondeterminism voids that seed's results.

## 7. Architecture accounting

0 cognition-substrate source lines added; no file outside this lane is
touched; the F1 lane is read-only. New code in this lane is sealed
characterization methodology only (feature analyzer, run scripts),
committed before fixture generation and sealed runs. No new semantic
cases, modes, bridges, routers, or handlers.

## 8. Verdict rule and void conditions

- CHARACTERIZED: the decision rule in section 5 is met; report the
  overfit rate and the identified pattern with its contingency table.
- NOT-FOUND: no fixture property separates; report all hypothesis
  tables and the overfit rate.
- VOID: ordering violation, contamination, toolchain violation, seal
  leak (e.g. choosing seeds or thresholds after seeing results beyond
  the frozen procedure), or any forbidden researcher response (adding
  SUB, DIV, PARITY, 2-threshold COND, or other researcher-authored
  semantic cases). A VOID verdict is terminal for this prereg.

A frozen rule is never weakened to force a pattern. No em-dashes are
used in this document.
