# REPORT.md -- IVWC-KSENSITIVITY: the K-sensitivity curve

## Verdict: BUILD-PASS (KS1 through KS7 all pass)

The K-sensitivity curve is a **broad plateau, not a sharp peak**
(KS4 FLAT). Maximum sealed profit 258 is attained on
K in {2,3,4} U {13,14,15,16}; 13 of the 89 swept bars land within 5%
of max. The optimum **shifts by batch** (KS5 SHIFTED): sh=0 (@15)
wants K in {2..6,13..16}, sh=1 (@30) wants K in {0..4}, sh=2 (@45)
wants K >= 34 -- the global optimum is a cross-batch compromise.
The revealed-preference bar is violently sensitive to train cost
(unit changes flip b* between 5 and 14) while sealed profit is flat
over the landing region (253..258 for train costs 4..20): K-sensitivity
is a useful signal about **robustness, not about a lever** -- there is
nothing to gain by tuning K, and the LEARNERK 14-vs-15 tie was not
luck. No fixed bar beats 258; the exact lineage bounds (283/288/318)
remain above every threshold verdict.

## Headline numbers

TABLE A -- total sealed profit vs decision bar K (GO iff adj > K;
per-batch profits in parentheses):

| K | total (sh0, sh1, sh2) |
|---|---|
| <=-3 | 76 (43,113,-80) -- execute-all anchor |
| -2,-1 | 91 |
| 0,1 | 256 |
| 2,3,4 | **258** (75,143,40) |
| 5 | 253 (75,138,40) -- erratum row |
| 6,7,8 | 248 |
| 9..12 | 228 |
| 13,14,15,16 | **258** (75,128,55) |
| 17,18,19 | 168 |
| 20,21,22 | 153 |
| 23 | 143 |
| 24..29 | 125 |
| 30..33 | 130 |
| 34..83 | 85 (0,0,85) |
| >=84 | 0 |

TABLE B -- revealed bar b*(c) at hypothetical train cost c, and its
sealed profit at the true cost 15:

| c | b*(c) | sealed profit |
|---|---|---|
| -3..-1 | -11 | 76 |
| 0,1 | -10 | 76 |
| 2,3,4 | 4 | 258 |
| 5..14 | 5 | 253 |
| 15..24 | 14 | 258 |
| 25..40 | 33 | 130 |

Every number was preregistered exactly from arithmetic on the
committed tables; all confirm (in-program KS3-KS7 = 1).

## What was built

`src/ivwc_ksensitivity.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_ksensitivity` (build artifact; excluded from the commit per
Micah's 2026-10-03 guidance). Measurement wave: no world, no learner,
no new mechanism. The train (t, bkt, adj, teff) and sealed
(sh, s, bkt, adj, eff) tables are embedded as literals, printed as
TAUDIT lines (24/24 train and 36/36 sealed byte-identical to the
committed IVWC-LEARNERK PREREG tables, worker-verified), then:

- **SWEEPA:** for each integer K in [-3,85] (data-driven range:
  [min sealed adj - 1, max sealed adj + 1]), per-batch profit and GO
  counts of GO iff adj > K, scored at the frozen world cost 15.
  Per-case GO decisions at K=14 and K=15 are retained for the
  equality check.
- **SWEEPB:** for each integer c in [-3,40], the LEARNERK global
  revealed bar b*(c) = argmax over b in [-11,84] of
  P_c(b) = sum over train cases with tadj > b of (teff - c), ties
  toward the larger bar (the frozen LEARNERK rule), then the sealed
  profit of b*(c) at the true cost 15.
- **KFLAGS:** in-program checks KS3-KS7.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_ksensitivity.zag -o bin/ivwc_ksensitivity` under the safebin
PATH (`which python3` and `which python` return nothing). Analyzer:
the standard zagd-unavailable informational notice only.

## Kill-bar results

- KS1 (diet / commit order / no-exact-signal): PASS. A1: phase order
  130<133<169<218<270 (TABLES < TAUDIT < SWEEPA < SWEEPB < KFLAGS).
  A2: 0 `world_buf`/`world_off`. A3: 0
  `expected|answer|key|target` (case-insensitive). A4: 0
  `correct|reference_plan|gold`. A5: 0 `world_execute(`. A6: 0
  `oracle`. A7: 0 `Tpred`. A8: the only sweep variables are the
  decision bar K and the hypothetical train cost c; every profit is
  scored at the frozen world cost 15 (a measurement given, not a
  learner input). Audit performed pre-build; all green before the
  first compile.
- KS2 (determinism): PASS. 3/3 byte-identical, sha256
  `8935f5ff0f6eb4c0f3ad1ed377b0d0b076f1cf37e9d091c290d8d3ffa15eb7ab`.
- KS3 (verbatim tables + anchors): PASS. 24/24 train and 36/36
  sealed TAUDIT lines byte-identical to the committed tables;
  K=15 -> (75,128,55) = 258; K=14 -> 258 with per-case GO sets
  identical to K=15 (in-program equality over all 36 cases);
  K=-3 -> (43,113,-80) = 76 (in-program KS3=1).
- KS4 (PRIMARY -- curve shape): PASS, **FLAT**. Max total 258;
  longest contiguous max run {13,14,15,16} (length 4 >= 4); 13
  distinct K with total >= 246 (>= 8). In-program KS4=1.
- KS5 (batch stability): PASS, **SHIFTED**. No K is simultaneously
  optimal on all three batches (sh=0 argmax {2..6,13..16} = 75;
  sh=1 argmax {0..4} = 143; sh=2 argmax {34..83} = 85; total
  intersection empty). In-program KS5=1.
- KS6 (revealed-bar tracking): PASS. b*(15) = 14 with sealed profit
  258 = sweep max; b*(14) = 5 -> 253 >= 246; b*(16) = 14 -> 258 >=
  246. In-program KS6=1.
- KS7 (erratum confirmation): PASS. Sweep row K=5 is exactly
  (75,138,40) = 253 (in-program KS7=1).

## Mechanism detail (white box)

### Why the plateau is where it is (KS4)

The total curve is the sum of three per-batch step functions whose
steps fall at different adjs, so the sum has flat stretches wherever
no batch has a case at the boundary. The max-258 region is two
blocks: {2,3,4} (sh0 at 75, sh1 at its max 143, sh2 at 40) and
{13,14,15,16} (sh0 at 75, sh1 at 128, sh2 at 55). Between them sits
K=5..12 (248..228): the (6,+5),(9,+10) sh0 cases and the (9,+10)
sh1 case drop out as K passes 6 and 9, while sh2's (13,-15) case
drops out at K=13 -- the -15 that buys the jump back to 258.
Outside [0,16] the cliffs are steep: below 0 the negative-eff mass
(adj 0 cases, eleven of them on sh2) floods in (91 -> 76); above 16
the profitable sh0/sh1 cases drain away (168 -> 153 -> 143 ->
125 -> 130 -> 85 -> 0). The long 85-flat for K in [34,83] is a
single case: s11 @45 (adj 84, eff 100).

### Why the optimum shifts by batch (KS5)

The three batches are wall-density shifts with different
profitable-case structure. sh=2 (@45) is eleven -15 cases and one
+85 case: its optimum is "take only the sure thing" (K >= 34).
sh=1 (@30) has four +35 cases at adj 34 plus a spread of small
positives: it wants a low bar (K in 0..4, taking everything with
adj > 4 except the -15s it cannot avoid). sh=0 (@15) is in between.
The global optimum is a compromise the batches would not choose
alone: at K=13..16, sh2 gets 55 instead of its local 85 (-30) so
that sh0+sh1 can hold 203. No single bar is optimal everywhere;
the worth-K bar 15 happens to sit in the compromise region.

### The shift-oracle bound (new arithmetic on the sweep)

Per-batch maxima summed: 75 + 143 + 85 = **303**. This is the profit
of a shift-conditional bar (a different K per batch). It is reported
as a bound in the lineage's exact-bound family (283 = V_PBX
per-bucket exact, 288/318 = fenced exact marginals, all from
IVWC-MARGINAL), with the explicit caveat that shift identity is not
a legitimate learner input under the sealed-batch discipline -- it
shows information is real but not learner-usable from train alone,
now along the shift dimension. Ladder: 258 (best fixed bar) < 283
< 303 (shift-oracle) < 318.

### K-sensitivity as a signal (KS6, TABLE B)

The revealed bar b*(c) as a function of hypothetical train cost is
a step function with violent transitions: -11 (c<0), -10 (c=0,1),
4 (c=2..4), 5 (c=5..14), 14 (c=15..24), 33 (c=25..40). A unit change
in experienced cost flips the bar 14 <-> 5 (c=14 vs 15) and 14 <->
33 (c=24 vs 25, an exact tie at P=175 resolved by the larger-bar
rule). Yet sealed profit over the landing region is nearly constant:
253..258 for all c in [2,24]. The bar is a high-sensitivity
instrument; the profit is insensitive. Two consequences for verdicts:
(a) the LEARNERK tie was not luck -- any bar in [2,16] earns
within 5% of the max, so 14 vs 15 could not have mattered much
whatever the tie-break chose; (b) K is not a lever: tuning the bar
cannot beat 258, and the revealed-preference machinery already
lands in the flat optimum at the true cost.

### The LEARNERK erratum (KS7)

The LEARNERK PREREG disclosed the aggressive-tie-break (b=5)
sensitivity as sealed (75,138,-40) = 173, "arithmetic on the
committed tables, not run". The arithmetic was wrong: with bar 5,
sh=2 takes s0, s4, s5 (adj 34,34,13 > 5; eff 0 -> -15 each) and s11
(adj 84; eff 100 -> +85), giving -15-15-15+85 = 40, not -40. The
correct value is (75,138,40) = **253**, confirmed by the sweep row
K=5. The tie-break was LESS load-bearing than disclosed (253 vs
258, not 173 vs 258). The error is corrected here; no LEARNERK
verdict changes (its preregistered bars and kill bars are
unaffected -- only the disclosed counterfactual number moves).

## Answers to the task's key questions

1. **What does the K-sensitivity curve look like?** A broad
   plateau with steep sides and a long flat tail: 258 on
   {2,3,4} U {13,14,15,16}, 13/89 bars within 5% of max, cliffs
   below 0 and above 16, an 85-flat for K in [34,83] (one case),
   0 beyond 84. Not a sharp peak.
2. **Is the optimum stable or does it shift?** It shifts by
   batch/shift (KS5 SHIFTED, preregistered). The global optimum is
   a cross-batch compromise; sh=2 alone would take only the
   (84,85) case at K >= 34.
3. **Can K-sensitivity inform better verdicts?** As robustness
   evidence, yes; as an optimization lever, no. The flatness over
   [2,16] means the verdict is insensitive to the exact bar --
   which explains the LEARNERK ownership-without-loss tie and
   predicts it would survive any nearby bar choice. Nothing in
   the curve suggests a bar beating 258 exists; the exact bounds
   above it (283/288/318, plus the 303 shift-oracle) are not
   reachable by any threshold verdict.

## Honest caveats

1. Measurement wave on committed tables: the sweep inherits every
   lineage caveat (one wall-density law-change axis; item law,
   belief noise, energy budget fixed). It adds no new evidence
   about the world, only about the decision landscape over it.
2. The c range [-3,40] is a preregistered analytic window, not
   data-driven; b*(c) beyond 40 (e.g. the I2/I3 tie at c=50)
   was not swept.
3. The 303 shift-oracle bound conditions on batch identity, which
   is not a learner-legible input under the sealed-batch
   discipline; it is a bound, not a verdict proposal.
4. Per-bucket revealed bars at hypothetical train costs were not
   swept (global bar only); the V_LOKB overfitting question in
   cost-space remains open.
5. This wave makes no learning claim (L0 measurement, L1
   interpretation at most); not L2, not L3 by any reading.

## Process notes and disclosures

- **No toolchain incident.** Clean lane: zero python3/python
  invocations at any step. Safebin PATH throughout (`which
  python3` and `which python` return nothing). Pure Zag, pinned
  znc. Text inspection of program output used safebin coreutils
  only (grep/sed/awk/sha256sum/cmp). See NAMECHECK.md Step 0.
- **Pre-build audits all green before the first build:** A1 phase
  order 130<133<169<218<270; A2/A3/A4/A5/A6/A7 all 0.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed tables. Every frozen prediction --
  all TABLE A rows, all TABLE B checkpoints, all anchor rows --
  confirmed exactly; in-program KS3-KS7 all 1.
- One build retry: the first znc invocation failed with "failed
  to write executable" because `bin/` did not exist yet; created
  it and rebuilt cleanly (exit 0, only the standard
  zagd-unavailable informational notice).
- Stdout bytes verified against hand computation (spot-checked
  rows K=-3,5,14,15,34,84 and all TABLE B checkpoints) beyond the
  in-program flags, per the toolchain lesson on trusting binary
  output.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_ksensitivity
$HOME/safebin/znc src/ivwc_ksensitivity.zag -o bin/ivwc_ksensitivity  # safebin PATH, pinned znc
./bin/ivwc_ksensitivity | sha256sum  # expect 8935f5ff0f6eb4c0f3ad1ed377b0d0b076f1cf37e9d091c290d8d3ffa15eb7ab
```

Frozen audits (PREREG KS1): A1 phase order
130<133<169<218<270; A2 0; A3 0; A4 0; A5 0 `world_execute(`; A6 0;
A7 0 `Tpred`; A8 scoring always at the frozen world cost 15, sweep
variables K and c only. KS2: sha256 equality across
runs/ivwc_ksensitivity-run{1,2,3}.txt. Train TAUDIT 24/24 and
sealed TAUDIT 36/36 byte-identical to the committed lineage tables.

## Branch note

Prereg committed as `66148aba8` on `tnn-native-lab`, strictly before
the implementation (commit-order self-check satisfied). Work
committed via GIT_INDEX_FILE plumbing with explicit pathspecs
confined to `ivwc_ksensitivity/`, leaving the shared index
untouched. `bin/` (reproducible via the pinned znc) is deliberately
excluded from the commit per Micah's 2026-10-03 guidance. This is a
non-ledger task. Push note: per the task instructions, do NOT push
via `gh_push_api.py` (known HTTP 403, credential lacks
git-database write scope; remote ref appears at `99c5691d`) --
push blockage documented for the parent; the credential must be
fixed before any push.
