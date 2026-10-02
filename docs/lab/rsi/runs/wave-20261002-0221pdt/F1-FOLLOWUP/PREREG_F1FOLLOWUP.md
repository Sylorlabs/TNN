# PREREG_F1FOLLOWUP: Greedy-trial seed-sensitivity as a constructor finding

Lane F1-FOLLOWUP, wave wave-20261002-0221pdt. This prereg is frozen
alone (committed with NAMECHECK.md only; no methodology, generator,
analyzer, fixture, or run artifact exists in this lane yet) before any
sealed fixture is generated or any sealed run executes.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing. All work is pure Zag compiled by the pinned znc, or
shell invoking znc, running binaries, git ops, cmp/sha256sum, grep, and
file moves/copies. Any forbidden executable invocation is automatic
PROCESS-FAIL.

## 1. The candidate claim (NEW candidate, not a verdict change)

"Greedy-trial seed-sensitivity is a constructor finding with measured
magnitude X": the F1 constructor exhibits seed-dependent trial outcomes
on the sum2 family. Which trials get constructed and how runs converge
vary with the train seed, at or above the frozen SENSITIVE floors in
section 6.

F1's BUILD-FAIL (wave-20261001-2321pdt, K-C0C-REG R-W2 trip) stands
untouched. This lane files the RT-EXEC-recommended separate
constructor finding with its own frozen seed set, sensitivity metric,
and kill bars. It is a finding about the constructor, not a promotion,
not an L3 claim, and not a re-litigation of the trigger.

## 2. Constructor under test (read-only; no implementation in this lane)

- Binary: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn,
  sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
  hash-verified before any run in this lane.
- Constructor: greedy depth-1 trial (single-ISA-element insertions
  before the terminal WRITE, frozen ISA order, strictly-improving
  argmin over the BUFN = 8 trial buffer), construction burst up to
  KB = 4 events. Unchanged from the prior wave; the lane is read-only
  toward the F1 lane.
- The windowed failure-density trigger is the accepted fixed failure
  monitor. On sum2 worlds it fires at episode 1 or 2 (seed-state
  predicts 0; almost every nonzero-x episode errors), so the trigger
  is not the variable under test here: the constructor's greedy trial
  choices are.

## 3. Sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs. This is the family where
the phenomenon was observed (F1 sealed rW2 overfit on seed 2301; prior
Part 2 measured 6/24 overfit on fresh sealed sum2 worlds). Keeping the
family and geometry identical to prior Part 2 isolates the constructor
as the variable; switching families would confound seed-sensitivity
with family-sensitivity.

- N = 40 seeds, i = 0..39:
  - train: seed = 5300 + 2*i, 24 episodes, x0 and x1 in 0..4
    (rng range 0..5), truth shown.
  - hidden: seed = 5301 + 2*i, 30 episodes, x0 and x1 in 5..14
    (rng range 5..15), truth masked as ?. Paired truth file shares
    (kind, seed, n) and shows y.
- The 53xx series is verified unused by every prior wave (dev used
  9000-series; F1 sealed used 1100..3100; prior Part 2 used 5100..5147).
  No post-hoc seed selection: all 40 seeds enter the denominator of
  every metric.
- Generator: F1's pure-Zag f1_wgen (kind sum2), source copied
  read-only into this lane's dev/ and compiled by the pinned znc.
  Before any sealed generation, the copy must regenerate prior Part 2
  fixtures byte-identically (cmp against the prior lane's sealed2/),
  proving the methodology reproduces the frozen generator.
- Fixture SHA-256 manifest sealed/FIXTURE_SHA256.txt is committed
  before any sealed run begins.

## 4. Run protocol per seed

`f1_learn <episodes> <state_in|-> <state_out> <trace> <pred>`:

- train (seed state in) -> train.state / train.trace / train.pred
- hidden (masked, trained state in) -> hidden.state / hidden.trace /
  hidden.pred
- 3/3 byte-identical reruns per seed (cmp-verified), 40 seeds.
- Scoring: `f1_score acc <hidden.pred> <truth>` (pure-Zag scorer,
  source copied read-only into this lane).

## 5. Frozen normalization and sensitivity metrics

Raw CONSTRUCT line format (from the frozen binary):
`CONSTRUCT <ep> <bidx> NODE id=<id> op=<OP> p1=<a> p2=<b> p3=<c> err_before=<eb> err_after=<ea>`

Operand classes (frozen): registers 8 and 9 are the two fixed feature
registers and register 0 is the accumulator on every seed (F1 ISA
binding; empirically confirmed on prior Part 2 traces: a first
construct of ADD 0 8 8 tracks the x0-first overfit structures, ADD 0 9 9
tracks the x1-first ones). Classes: 8 -> X0, 9 -> X1, 0 -> R0,
any other value -> O.

- Normalized event: `OP C(p1) C(p2) C(p3) eb ea`. Episode index,
  burst index, and node id are dropped as timing/buffer artifacts;
  op, operand classes, and error transitions are kept.
- First-trial class: `OP C(p2) C(p3)` of the first CONSTRUCT event in
  the train trace (`NONE` if a trace has no CONSTRUCT events). This is
  the constructor's first greedy trial choice.
- Normalized sequence: the seed's normalized events joined by `|`,
  in trace order. This is the convergence path.

The pure-Zag analyzer f1f_analyze (committed before any sealed run;
it implements exactly the normalization above) computes:

- R = number of seeds with hidden accuracy below 100 percent
  (acc_num < acc_den). Overfit is any miss: the constructor either
  solves the law (30/30 in all prior correct cases) or it does not.
- T = number of distinct first-trial classes across the 40 seeds.
  Direct measure of "which trials get constructed".
- D = number of distinct normalized full sequences across seeds.
- Cmax = largest number of seeds sharing one normalized sequence
  (concentration of convergence).

Diagnostics (reported, not bars): first-TRIGGER episode per seed,
CONSTRUCT event count per seed, hidden accuracy distribution,
per-seed table (i, acc, first-trial class, sequence id).

## 6. Frozen kill bars

- K-SENS-RATE: R >= 4 (10 percent). Prior Part 2 measured 6/24 =
  25 percent on the same family and geometry; 10 percent is the
  frozen floor for a finding-worthy behavioral sensitivity.
- K-SENS-TRIAL: T >= 2. The constructor must not always build the
  same first trial across seeds.
- K-SENS-CONV: D >= 3 AND Cmax <= 34. At least three distinct
  convergence paths, with no single path taken on more than 85
  percent of seeds.
- K-DET: all 40 seeds complete with 3/3 byte-identical reruns
  (cmp-verified); SHA-256 of each raw output recorded. Any
  nondeterminism voids the measurement.
- NC-HARNESS (calibration, executed before the sealed runs): with
  this lane's generator copy, regenerate prior Part 2 fixtures
  i = 0..5 (train seeds 5100, 5102, 5104, 5106, 5108, 5110) and
  cmp-verify byte-identical against the prior lane's sealed2/
  fixtures; run all 6 through this lane's run script (3/3
  byte-identical); require hidden acc < 30/30 for i in {2,3,5}
  (the known overfits) and hidden acc = 30/30 for i in {0,1,4}
  (the known corrects), and hidden pred outputs byte-identical to
  the prior lane's runs2/1 preds. Any mismatch means the harness
  does not measure the constructor, and the prereg is void.

## 7. Verdict rule and void conditions

- BUILD-PASS: K-SENS-RATE, K-SENS-TRIAL, and K-SENS-CONV all pass.
  The measured magnitude X = (R/40 overfit rate, T first-trial
  classes, D convergence paths, Cmax/40 concentration) is reported
  with the full per-seed table and distribution. The constructor
  finding is filed. No promotion, no L3 claim, no change to F1's
  BUILD-FAIL.
- BUILD-FAIL: any of the three SENS bars fails. The failed bar(s)
  and the measured values are named. A constructor that is
  trial-order sensitive but convergence-robust (or robust outright)
  is reported honestly as such.
- VOID: K-DET or NC-HARNESS failure, ordering violation,
  contamination, toolchain violation, seal leak (including choosing
  seeds, thresholds, or normalization after seeing data), or any
  forbidden researcher response (adding SUB, DIV, PARITY,
  2-threshold COND, or other researcher-authored semantic cases).
  A VOID verdict is terminal for this prereg.

A frozen kill bar is never weakened to force a pass. Verdicts name
the exact frozen bars that governed them. No em-dashes are used in
this document.

## 8. Determinism standard and architecture accounting

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of each raw
output recorded. Zero randomness in decision paths.

Architecture accounting: 0 cognition-substrate source lines added; no
file outside this lane is touched; the F1 lane is read-only. New code
in this lane is sealed characterization methodology only (generator
and scorer copies, f1f_analyze, run scripts), committed before
fixture generation and sealed runs. New hardcoded semantic cases 0;
new modes 0; new bridges 0; new routers 0; new task-specific
handlers 0.
