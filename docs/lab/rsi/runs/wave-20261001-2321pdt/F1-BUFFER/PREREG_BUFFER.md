# PREREG_BUFFER: trigger-time buffer features vs constructor overfit

Lane F1-BUFFER, wave wave-20261001-2321pdt. This prereg is frozen
alone (separate commit) before any fresh sealed fixture is generated
or any fresh sealed run executes. It tests the natural next
hypothesis named by F1-FOLLOWUP Part 2: that the greedy depth-1
trial constructor's overfit is predictable from the first-trigger
buffer (the trial-buffer contents at the moment the windowed trigger
first fires), which whole-fixture features cannot see. The F1
binary (constructor and trigger) is used read-only; no
implementation work touches it.

No em-dashes are used in this document.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
NAMECHECK.md Step 0 of this lane. PATH is safebin only. `which
python3` prints nothing. All work is pure Zag compiled by the pinned
znc, or shell invoking znc, running binaries, git ops,
cmp/sha256sum, and file moves/copies. Any forbidden executable
invocation is automatic PROCESS-FAIL.

## 1. Calibration status (training knowledge, frozen before this prereg)

The 5100-series (F1-FOLLOWUP Part 2 sealed artifacts) and the 2301
fixture are training knowledge for this lane. Calibration on the 24
committed 5100-series train traces (dev/CALIBRATION_5100.md, committed
before this prereg; no fresh fixture generated, no fresh learner run
executed) found:

- Best single-feature buffer rule: predict OVERFIT iff T >= 12,
  misc = 5/24 on the training series.
- Collision proof: seeds 6/18 (both buffer (S0,S1,N,TRIG)=(3,7,2,1),
  opposite labels) and seeds 11/17 (both (5,6,2,1), opposite labels)
  are identical on every frozen buffer feature, so no deterministic
  rule over these features can beat misc = 2 on the training series.
  The error-mass-balance hypothesis in single-threshold form (R, D)
  is falsified on training data (misc 7 to 8).

The sealed test below is a genuine out-of-sample check of whether
the best-calibrated buffer rule generalizes to fresh worlds.

## 2. Frozen definitions

Let the frozen F1 binary be
docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn, sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
(verified before runs; the binary is read-only).

For one sealed train run, the FIRST-TRIGGER BUFFER B is defined
mechanically from the train trace:

- t = the episode index on the first trace line beginning with
  "TRIGGER " (fields: TRIGGER <ep> winfail=<n> win=<n> buf=<n>).
- B = the set of EP lines with episode index 0..t. Every train
  episode carries truth, and the learner pushes exactly the
  truth-episodes into its BUFN trial buffer in order, so at fire
  time the trial buffer holds precisely episodes 0..t (count t+1,
  matching the trace's buf= field).

Frozen buffer features (computed by the frozen pure-Zag dev/bufx,
which reads only the trace):

- S0(B) = sum of x0 over B; S1(B) = sum of x1 over B.
- T(B) = S0(B) + S1(B) (total buffer mass).

If a train trace contains no TRIGGER line, the world is reported as
NOTRIG and excluded from the rule evaluation (counted separately;
more than 2 NOTRIG worlds voids the test set).

## 3. Frozen decision rule

Predict OVERFIT iff T(B) >= 12. Otherwise predict CORRECT.

This is the exact best-calibrated single-feature rule from section
1, frozen unchanged. The threshold, feature, and direction were
fixed during calibration on training data and do not move.

## 4. Fresh sealed fixture design (frozen)

World family: sum2, y = 2*(x0+x1), 2 inputs, exactly as in
F1-FOLLOWUP PREREG_PART2 section 2:

- Train: 24 episodes, x0 and x1 in 0..4 (rng range 0..5), truth shown.
- Hidden: 30 episodes, x0 and x1 in 5..14 (rng range 5..15), truth
  masked as ?. Truth paired file shares the (kind, seed, n).

Generator: the pure-Zag f1_wgen copied read-only into this lane
(identical binary behavior; byte-identical reproduction of a
reference fixture verified before any sealed generation).

Fresh seed series, never used by dev (9000-series), F1 sealed
(1100..3100), or Part 2 (5100-series); the 5100-series and the 2301
fixture are NOT reused here: for i = 0..23 (N = 24 seeds),

- train seed = 8100 + 2*i
- hidden/truth seed = 8101 + 2*i

The seed series is frozen here. The fixture SHA-256 manifest is
committed (sealed3/FIXTURE_SHA256.txt) before any sealed run begins.

## 5. Run protocol per seed (frozen binary, read-only)

- train (seed state in) -> state/trace/pred
- hidden (masked, trained state in) -> pred
- 3/3 byte-identical reruns per seed (cmp-verified), 24 seeds.

Scoring: the frozen pure-Zag f1_score (copied read-only), `f1_score
acc <pred> <truth>` on the 30-probe hidden set.

Classification (frozen, same as Part 2):

- CORRECT: hidden accuracy at least 80 percent (24/30).
- OVERFIT: hidden accuracy below 80 percent.

Rule application: the frozen pure-Zag dev/bufapply (implements
exactly section 3, committed after this prereg) reads dev/bufx
output plus the frozen labels and prints per-seed predictions and
the contingency table. No threshold or feature may differ from
section 3.

## 6. Frozen bar

BUFFER-PREDICTIVE iff ALL of:

(a) all 24 fresh seeds complete with 3/3 byte-identical reruns;
(b) at most 2 NOTRIG worlds (else VOID, not a verdict);
(c) the frozen rule (T(B) >= 12 predicts OVERFIT) misclassifies at
    most 2 of the 24 fresh seeds (misclassified = predicted OVERFIT
    but CORRECT, or predicted CORRECT but OVERFIT), with the full
    per-seed table and contingency cells reported.

## 7. Reference outcome

If (c) fails, the verdict is BUFFER-NOT-PREDICTIVE with the exact
misclassification count, the per-seed table, and the contingency
cells. This is an informative negative, reported fully, not hidden.
It would mean the constructor's greedy failure is not predictable
from the trigger-time buffer mass under this rule, consistent with
the training-series collision proof (seeds 6/18, 11/17) and the
observed later-trigger repair dynamics.

## 8. Determinism standard

3/3 byte-identical reruns per seed (cmp-verified); SHA-256 of each
raw output recorded. Zero randomness in decision paths. Any
nondeterminism voids that seed's results.

## 9. Architecture accounting

0 cognition-substrate source lines added; no file outside this lane
is touched; the F1 and F1-FOLLOWUP lanes are read-only (sources
extracted via git show; binaries used read-only with sha256
verification). New code in this lane is sealed methodology only
(feature extractor, rule applier, run scripts). No new semantic
cases, modes, bridges, routers, or handlers.

## 10. Verdict rule and void conditions

- BUFFER-PREDICTIVE: section 6 is met; report the rule, its
  contingency table, and the misclassification count.
- BUFFER-NOT-PREDICTIVE: section 6(c) fails; report the
  misclassification count, per-seed table, and contingency cells.
- VOID: ordering violation (any fresh fixture generated or any
  fresh learner run executed before this prereg's commit),
  contamination, toolchain violation, seal leak (e.g. choosing the
  seed series, rule, or threshold after seeing fresh results), more
  than 2 NOTRIG worlds, or any forbidden researcher response
  (adding SUB, DIV, PARITY, 2-threshold COND, or other
  researcher-authored semantic cases). A VOID verdict is terminal
  for this prereg.

A frozen rule is never weakened to force a pass. No em-dashes are
used in this document.
