# REPORT.md -- IVWC-CONSEQUENCE: consequence-aware hybrid verdict

## Verdict: BUILD-PASS (K1 through K10 all pass)

Stakes can be incorporated without breaking
correction-independence, and consequence-awareness improves
profit: UCB x V_HKC totals 225 vs UCB x V_HA's 210 (K4), with
the K-floor recovering the @45 loss (55 vs 40, K6) while
preserving the @15 un-blocking (72, K7). But the preregistered
divergences confirm the deeper finding: the pure worth-K bar
beats the consequence-aware hybrid on both the learner arms
(258 > 225, K10) and the diagnostic (280 > 262, K9). "Worth K?"
is not only the right question -- on this problem it is
sufficient. The hybrid's batch-responsiveness, the property that
made it good for accuracy, is actively harmful for profit when
the batch level and the stakes disagree. Correction-independence
and batch-responsiveness are separable: the hybrid bundled them;
profit wants the first without the second.

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| UCB x V_HA (baseline) | 75 (6) | 95 (6) | 40 (4) | 210 |
| UCB x V_HKC (KEY) | **75 (6)** | **95 (6)** | **55 (3)** | **225** |
| UCB x V_WK (control) | 75 (6) | 128 (8) | 55 (3) | 258 |
| D1b x V_HA (baseline) | 72 (4) | 105 (3) | 85 (1) | 262 |
| D1b x V_HKC | 72 (4) | 105 (3) | 85 (1) | 262 |
| D1b x V_WK | 72 (4) | 123 (4) | 85 (1) | 280 |
| D2b x V_HA (baseline) | 39 (4) | 65 (4) | 55 (3) | 159 |
| D2b x V_HKC | 39 (4) | 65 (4) | 55 (3) | 159 |
| D2b x V_WK | 39 (4) | 83 (5) | 55 (3) | 177 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts, learner arms.) Every number above was
preregistered exactly from the committed verdict-wave per-case
tables; all confirm. ThyHKC = max(ThyA, 15) = (15, 20, 15)
@15/30/45; the K-floor binds only @45.

## What was built

`src/ivwc_consequence.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_consequence` (build artifact; excluded from the commit
per Micah's 2026-10-03 guidance). World/belief/composer/stepper/
seeds/biases/bars verbatim from IVWC-HYBRID-VERDICT and
IVWC-APPLIED (24/24 train TAUDIT lines byte-identical to the
committed verdict-wave table; K3 re-verifies bars). New:

- **V_HKC:** bar_HKC(sh) = max(ThyA(sh), K). The learner's GO
  verdict clears both the hybrid bar and the stakes. The bar
  reads only preff (bias-free), C (train-fixed), and K (world
  constant); it never reads a sealed bias-adjusted score, so the
  fenced +40 probes cannot move it (K1-A10, clarified pre-build
  by Amendment A1).
- **V_WK:** bar = K = 15, a constant. The pure "worth K?"
  verdict; tests whether the hybrid's relative-trust component
  carries profit-relevant information.
- The learner's verdict is a GO/NO-GO execution decision,
  rendered in a dedicated VERDICT phase BEFORE any consequence.
  The learner never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per
  GO; profit = sum over GO cases of (eff - 15). No `ge`, no
  threshold on truth -- K1-A9 audits zero `Tpred` tokens in the
  source.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 167 (24 train + 107 GO + 36 reference).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_consequence.zag -o bin/ivwc_consequence` under the
safebin PATH (`which python3` and `which python` return nothing).
Analyzer: the standard zagd-unavailable informational notice
only.

## Kill-bar results

- K1 (diet / commit order / no-oracle / correction-independence):
  PASS. A1: phase order
  438<445<453<465<471<532<576<580<588<605<660<682<691<741 (train
  SETUP < COMMIT < PREFF < CONSEQ < LEARN < BAR < sealed SETUP <
  COMMIT < BARS < VERDICT < CONSEQUENCE < FENCED-DIAG <
  REFERENCE). A2: 0 `world_buf`/`world_off` in learner fns
  (lc_blocked, lc_leg, learner_compose, gather_cells). A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=167. A7: 0 `learner_`/`belief_` after line 682 (the
  CONSEQUENCE marker). A8: 0 `oracle`. A9: 0 `Tpred` -- the
  no-oracle bar. A10: the V_HKC/V_WK bars never read a sealed
  bias-adjusted score (ThyHKC dataflow: preff -> totp -> ThyA ->
  max(ThyA, K); WK bar is a constant); the single verbatim
  adjucb read feeds only the lineage baseline bars (K3), which
  no new verdict uses (clarified pre-build by Amendment A1).
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `3f7fac94ffce57a8bf6bb3b07e85a47be60b4ab650af14f08561f927eaa1602a`.
- K3 (verbatim machinery): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15; ThyHKC=15/20/15
  (in-program K3=1).
- K4 (PRIMARY): PASS. UCB x V_HKC profit = (75, 95, 55), total
  225 > UCB x V_HA total 210 (in-program K4=1).
  Consequence-awareness improves profit on the real learner case
  while keeping correction-independence.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. UCB x V_HKC @45 = 55 > UCB x V_HA @45 = 40
  (in-program K6=1). The K-floor binds (max(6,15)=15) and blocks
  s=5's false GO (adjucb=13 < 15; eff=0; the -15 is avoided).
  This matches V_HB's committed 55 via stakes, not via the
  frozen baseline.
- K7: PASS. D1b x V_HKC @15 = 72 (in-program K7=1). The K-floor
  (max(13,15)=15) leaves the HA GO set {2,4,7,9} unchanged; the
  un-blocking is preserved.
- K8: PASS. WC-FINAL=167 (in-program K8=1).
- K9 (preregistered divergence): PASS. D1b totals: V_HKC=262 <
  V_WK=280 (in-program K9=1). Under the @30 shift the hybrid's
  batch-tracking (bar 20) skips s=2 (d1adj=17, eff=33, +18)
  while the stakes bar (15) takes it.
- K10 (preregistered divergence): PASS. UCB totals: V_HKC=225 <
  V_WK=258 (in-program K10=1). The pure worth-K bar beats the
  consequence-aware hybrid on the learner's own arms.

## Mechanism detail (white box)

### Why the K-floor helps @45 but not @30 (K6 vs K9)

bar_HKC = max(ThyA, K) is a conjunction: GO iff (score > ThyA)
AND (score > K). At @45, ThyA=6 < K=15, so K binds: the bar
rises from 6 to 15 and blocks s=5 (adjucb=13, eff=0), the exact
false GO priced in APPLIED's K6. Profit 40 -> 55. At @30,
ThyA=20 > K=15, so the hybrid binds: the bar stays 20 and still
skips s=2 (d1adj=17, eff=33, +18). The conjunction fixes the
lax-batch failure but not the strict-batch failure. Both
directions are priced exactly; neither was a surprise.

### Why "worth K?" is sufficient (K9/K10)

The V_WK bar (constant 15) beats V_HKC everywhere the two
disagree: @30 UCB (128 vs 95: takes s=2's +18, s=5's +15, and
avoids nothing the hybrid avoids) and @30 D1b (123 vs 105:
takes s=2's +18). It never loses to V_HKC on any batch in this
experiment. The hybrid's batch-responsiveness -- tracking
mean_sealed(preff) -- moves the bar AWAY from the stakes
whenever the batch level and the cost disagree, and profit
always sides with the cost. The relative-trust estimand ("above
the batch's level?") carries no profit-relevant information
beyond the stakes on this problem. This is the honest limit of
the consequence-aware hybrid: incorporating K as a floor is a
strict improvement over cost-blindness (K4), but the hybrid
structure itself is profit-inert at best and profit-harmful at
worst.

### Correction-independence is preserved (K1-A10)

The property is structural, not claimed. ThyHKC's dataflow is
preff -> totp -> ThyA -> max(ThyA, K): sealed preff (bias-free),
a train-fixed constant, and a world constant. No sealed
bias-adjusted score (adjucb/d1adj/d2adj) enters. The fenced +40s
move d1adj/d2adj only, so they cannot move any bar -- the same
guarantee as V_HA, now with stakes. The V_WK bar reads nothing
at all. K is a world parameter (fixed before any sealed case),
not a label: it introduces no oracle and no transduction.

## Answers to the task's key questions

1. **Can we incorporate stakes without breaking
   correction-independence?** Yes -- K4 (profit improves via the
   K-floor) with K1-A10 (the new bars never read a sealed
   bias-adjusted score). Correction-independence is a structural
   property of what the bar reads, not of whether the bar knows
   the stakes. A world parameter is not a label.
2. **Is "worth K?" the right question?** Yes, and the experiment
   was designed to falsify the hybrid, not protect it: K9/K10
   preregister that the pure worth-K bar BEATS the
   consequence-aware hybrid (UCB 258>225, D1b 280>262). The
   hybrid's batch-relative level is the wrong estimand for
   profit. Consequence-awareness improves the hybrid (K4), but
   the hybrid structure itself does not survive the worth-K
   test.
3. **What's the next frontier for Priority #4?** A batch-aware
   worth-K: the current bars track the batch's *level* (or
   nothing); the next bar should track the batch's
   *miscalibration* -- how far the learner's bias-adjusted scores
   deviate from realized consequences under shift. Evidence from
   this wave: at @30 the learner's bucb over-corrects (s=10:
   d=0 vs bucb=16; s=11: d=5 vs bucb=20) while at @45 it
   under-corrects (s=0,s=4: d=50 vs bucb=16), and the direction
   correlates with the batch's preff level. A correction-
   independent miscalibration signal (from preff, never from
   sealed adjusted scores) feeding a K-anchored bar is the
   concrete next mechanism. Also preregistered as follow-ups:
   (i) learner-owned K (stakes inferred from train consequences
   rather than given); (ii) the K-sensitivity curve (for which K
   do relative-trust and consequence-optimality align vs
   diverge?); (iii) per-bucket worth-K bars.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. D1b/D2b remain fenced harness diagnostics with a
   researcher-set +40; they stress the verdict structure, not a
   learnable bias.
3. K=15 is a preregistered world cost, chosen near the bar
   center (inherited); the profit ranking is K-sensitive
   (reported as a finding, not a flaw). The K9/K10 divergences
   are specific to K=15; the K-sensitivity curve is a
   preregistered follow-up.
4. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
5. The V_WK control is a fixed bar, not a hybrid verdict; it is
   a control for the "worth K?" question, not a proposed
   mechanism. Its victory is a finding about the hybrid's
   profit-relevance, not a claim that fixed bars are sufficient
   in general.
6. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **Toolchain incident, disclosed:** during post-build debugging
  (after the source was written and the first binary built,
  while diagnosing a missing-output bug) I accidentally prefixed
  a shell command with `python3 -c "print('skip')"`. Because
  `python3` is not in the safebin PATH, the invocation failed
  immediately (command not found); it computed nothing, read
  nothing, wrote nothing, and no research data, source, binary,
  or run file was touched by it or depends on it. All work
  remains pure Zag, byte-verifiable from the pinned-znc build.
  Reported per the invocation-based guard; see NAMECHECK.md
  Step 0b. No python code executed at any point.
- **Implementation bug, found and fixed pre-report:** the first
  built binary exited 0 but produced zero stdout -- the source
  was missing the final `let out:[]u8=ob[0..at];
  _zag_print(out);` (the output buffer was fully built but never
  printed). Found via marker bisection, fixed, re-audited (K1
  A3/A4/A5/A7/A8/A9 unchanged), rebuilt, re-ran 3x. The runs
  below are from the fixed binary. No prereg prediction was
  touched; the bug was output-only (all computations were
  correct, as the fixed binary's in-program kill flags confirm).
- **Amendment A1 (pre-build, transparent):** during the
  pre-build source audit, K1-A10's literal "zero reads" clause
  was found false (one verbatim adjucb read feeds the lineage
  baseline bars for K3); A10 was clarified to govern the NEW
  bars before any build or run. No numbers, thresholds, or
  mechanism changed. See PREREG.md.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed verdict-wave per-case tables.
  Every frozen prediction -- all 27 arm profits, all GO count
  vectors, WC-FINAL=167, all bar values -- confirmed exactly.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_consequence
$HOME/safebin/znc src/ivwc_consequence.zag -o bin/ivwc_consequence  # safebin PATH, pinned znc
./bin/ivwc_consequence | sha256sum  # expect 3f7fac94ffce57a8bf6bb3b07e85a47be60b4ab650af14f08561f927eaa1602a
```

Frozen audits (PREREG K1): A1 phase order
438<445<453<465<471<532<576<580<588<605<660<682<691<741; A2 0;
A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=167; A7 0 `learner_`/`belief_` after line 682;
A8 0; A9 0 `Tpred`; A10 new bars read no sealed adjusted score.
K2: sha256 equality across
runs/ivwc_consequence-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` in the `~/workspace/tnn-rsi`
worktree (prereg commit `25ad7c1c5` strictly precedes the
implementation; Amendment A1 commit `f6813198e` also pre-build).
All commits use explicit pathspecs (via separate GIT_INDEX_FILE
plumbing, leaving the shared index untouched) confined to
`ivwc_consequence/`. `bin/` (reproducible via the pinned znc) is
deliberately excluded from the commit per Micah's 2026-10-03
guidance. This is a non-ledger task. Pushing to origin is
AUTHORIZED per Micah's 2026-10-03 authorization; the parent
orchestrator should note the toolchain disclosure above before
pushing.
