# PREREG_SEEDSENS: Greedy-trial seed-sensitivity as a constructor finding (fresh battery)

Lane F1, wave wave-20261002-0521pdt. This prereg is frozen alone
(committed with NAMECHECK.md only; no methodology, generator,
analyzer, fixture, or run artifact exists in this lane yet) before
any sealed fixture is generated or any sealed run executes.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which
python3` prints nothing. All work is pure Zag compiled by the pinned
znc, or shell invoking znc, running binaries, git ops,
cmp/sha256sum, grep, and file moves/copies. Any forbidden executable
invocation is automatic PROCESS-FAIL.

## 1. The candidate claim (NEW constructor finding, not a verdict change)

"Greedy-trial seed-sensitivity is a constructor property with
measured magnitude X": the F1 greedy depth-1 trial constructor
exhibits seed-dependent trial outcomes on the sum2 family on a
fresh sealed battery. The constructor's first greedy trial choice
varies with the train seed, and seed-dependent overfit outcomes via
the documented greedy-compounding failure mode reproduce on fresh
seeds, at or above the frozen floors in section 6.

Relation to prior verdicts, stated so nothing is re-litigated:
- F1 (wave-20261002-0221pdt) BUILD-PASS on POLICY-C stands untouched.
- F1-FOLLOWUP (wave-20261002-0221pdt) BUILD-FAIL on the "behavioral
  sensitivity at or above a 10 percent floor" claim stands untouched;
  R = 3/40 missed the frozen 10 percent floor and that claim stays
  failed.
- This lane files the RT-EXEC-recommended SEPARATE constructor
  finding: a qualitative constructor property (seed-dependent trial
  choices plus seed-dependent overfit outcomes via the documented
  mechanism) with its own frozen seed set, frozen normalization, and
  frozen bars. It is a finding about the constructor, not a
  promotion, not an L3 claim, not a repair, and not a second attempt
  at the failed 10-percent claim. The measured overfit rate is
  reported and pooled with prior batteries, never reified as the
  constructor's rate.

## 2. Constructor under test (read-only; no implementation in this lane)

- Binary: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn,
  sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
  hash-verified before any run in this lane.
- Constructor: greedy depth-1 trial (single-ISA-element insertions
  before the terminal WRITE, frozen ISA order, strictly-improving
  argmin over the BUFN = 8 trial buffer), construction burst up to
  KB = 4 events. Identical constructor logic to the binary used in
  the 0221pdt battery, so the constructor is the isolated variable.
- The windowed failure-density trigger is the accepted fixed failure
  monitor. On sum2 worlds it fires at episode 1 or 2, so the trigger
  is not the variable under test: the constructor's greedy trial
  choices are.

## 3. Sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs. This is the family
where the phenomenon was observed (rW2 overfit; prior Part 2
measured 6/24 overfit; the 0221pdt battery measured 3/40). Keeping
the family and geometry identical to prior batteries isolates the
constructor as the variable; switching families would confound
seed-sensitivity with family-sensitivity.

- N = 40 seeds, i = 0..39:
  - train: seed = 5500 + 2*i, 24 episodes, x0 and x1 in 0..4
    (rng range 0..5), truth shown.
  - hidden: seed = 5501 + 2*i, 30 episodes, x0 and x1 in 5..14
    (rng range 5..15), truth masked as ?. Paired truth file shares
    (kind, seed, n) and shows y.
- The 55xx series is verified unused by every prior wave (dev used
  9xxx; F1 sealed used 11xx..31xx; prior Part 2 used 51xx; the
  0221pdt battery used 53xx). No post-hoc seed selection: all 40
  seeds enter the denominator of every metric.
- Generator: F1's pure-Zag f1_wgen (kind sum2), source copied
  read-only into this lane's dev/ and compiled by the pinned znc.
  Before any sealed generation, the copy must regenerate prior Part
  2 fixtures byte-identically (cmp against the prior lane's
  sealed2/), proving the methodology reproduces the frozen
  generator.
- Fixture SHA-256 manifest sealed5/FIXTURE_SHA256.txt is committed
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

This prereg adopts the owned calibration fix from the 0221pdt
red-team Attack 2: the frozen metric is op/operand-only grouping.
Error magnitudes (err_before / err_after) vary with fixture x-values
even when the constructor builds identical op/operand structures, so
they are excluded from the frozen convergence metric.

Raw CONSTRUCT line format (from the frozen binary):
`CONSTRUCT <ep> <bidx> NODE id=<id> op=<OP> p1=<a> p2=<b> p3=<c> err_before=<eb> err_after=<ea>`

Operand classes (frozen): 8 -> X0, 9 -> X1, 0 -> R0, any other
value -> O (F1 ISA binding; registers 8 and 9 are the two fixed
feature registers and register 0 is the accumulator on every seed).

- Normalized event: `OP C(p1) C(p2) C(p3)`. Episode index, burst
  index, node id, AND err transitions are dropped as timing/buffer
  artifacts; op and operand classes are kept. This is the
  structural convergence path unit.
- First-trial class: `OP C(p2) C(p3)` of the first CONSTRUCT event
  in the train trace (`NONE` if a trace has no CONSTRUCT events).
  This is the constructor's first greedy trial choice.
- Normalized sequence: the seed's normalized events joined by `|`,
  in trace order.

The pure-Zag analyzer f1s_analyze (committed before any sealed run;
it implements exactly the normalization above) computes:

- R = number of seeds with hidden accuracy below 100 percent
  (acc_num < acc_den). Overfit is any miss: the constructor either
  solves the law (30/30 in all prior correct cases) or it does not.
- T = number of distinct first-trial classes across the 40 seeds.
  Direct measure of "which trials get constructed".
- D_ops = number of distinct normalized op/operand sequences across
  seeds.
- Cmax_ops = largest number of seeds sharing one normalized
  op/operand sequence (structural concentration).

Diagnostics (reported, not bars): first-TRIGGER episode per seed,
CONSTRUCT event count per seed, hidden accuracy distribution,
per-seed table (i, acc, first-trial class, sequence id), pooled
overfit rate across the three sealed batteries (prior Part 2,
0221pdt, this lane).

## 6. Frozen kill bars

- K-SS-TRIAL: T >= 2. The constructor must not always build the
  same first trial across seeds.
- K-SS-OVERFIT: R >= 1 AND the white-box check: at least one
  overfit seed's raw train trace must show the documented
  greedy-compounding failure mode (a trial that strictly reduces
  the seed-driven buffer error yet compounds an incorrect partial
  law: re-adding an already-added feature to the accumulator, or
  doubling the accumulator, with the compounding visible in the
  raw CONSTRUCT op/operand lines). A lone low-accuracy seed whose
  trace does not show this mechanism fails the white-box check and
  the bar.
- K-SS-CONV: D_ops >= 2 AND Cmax_ops <= 32. At least two distinct
  structural convergence paths, with no single path taken on more
  than 80 percent of seeds.
- K-DET: all 40 seeds complete with 3/3 byte-identical reruns
  (cmp-verified); SHA-256 of each raw output recorded. Any
  nondeterminism voids the measurement.
- NC-HARNESS (calibration, executed before the sealed runs): with
  this lane's generator copy, regenerate prior Part 2 fixtures
  i = 0..5 (train seeds 5100, 5102, 5104, 5106, 5108, 5110) and
  cmp-verify byte-identical against the prior lane's sealed2/
  fixtures; run all 6 through this lane's run script (3/3
  byte-identical); require hidden acc < 30/30 for i in {2,3,5}
  (the known overfits, 5/30, 0/30, 2/30) and hidden acc = 30/30 for
  i in {0,1,4} (the known corrects), and hidden pred outputs
  byte-identical to the prior lane's runs2/1 preds. Any mismatch
  means the harness does not measure the constructor, and the
  prereg is void.

## 7. Verdict rule and void conditions

- FINDING CONFIRMED: K-SS-TRIAL, K-SS-OVERFIT, and K-SS-CONV all
  pass, with K-DET and NC-HARNESS passing. The measured magnitude
  X = (R/40 overfit rate, T first-trial classes, D_ops structural
  paths, Cmax_ops/40 structural concentration) is reported with the
  full per-seed table and distribution, the white-box compounding
  evidence, and the pooled rate across batteries. The constructor
  finding is filed. No promotion, no L3 claim, no change to any
  prior verdict.
- NOT CONFIRMED: any of the three property bars fails. The failed
  bar(s) and the measured values are named. A constructor that is
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

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of each
raw output recorded. Zero randomness in decision paths; the only
seeded input is the fixture generator's RNG.

Architecture accounting: 0 cognition-substrate source lines added;
no file outside this lane is touched; the F1 lane and the 2321pdt
F1 lane are read-only. New code in this lane is sealed
characterization methodology only (generator and scorer copies,
f1s_analyze, run scripts), committed before fixture generation and
sealed runs. New hardcoded semantic cases 0; new modes 0; new
bridges 0; new routers 0; new task-specific handlers 0.
