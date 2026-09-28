# H5 Debate Prep — Independent Ground Truth + Steelmans

Date: 2026-09-24. Independent of grok (round 1 returned empty content; sol still
provider-down). All numbers below re-derived from the raw per-run records in
`~/workspace/scratch-h5/sweep/` (60 cells × A/B: jsonl + ledger + stdout), NOT from
`RESULTS_H5.md`. Accuracy recomputed from `verdict==ground_truth`, not from the
`correct` field (which was separately verified consistent across all 5,262 records).

## 1. Ground-truth verification: every number checks out

| Claim (RESULTS_H5.md) | Re-derived | Verdict |
|---|---|---|
| Trap accuracy d1/d2/d4/d8/deep16/adaptive = 0.000/0.331/0.961/1.000/1.000/1.000 (n=127) | 0/127, 42/127, 122/127, 127/127, 127/127, 127/127 → exact | PASS |
| Pooled = 0.855/0.903/0.994/1.000/1.000/1.000 (n=877) | 750/877, 792/877, 872/877, 877/877, 877/877, 877/877 → 0.855/0.903/0.994/1.000/1.000/1.000 | PASS |
| Mean rounds all 30 battery×config cells | all 30 match to 2dp (e.g. trap 1.00/2.00/3.48/3.81/3.81/3.81; admit 1.00/1.97/3.63/6.20/9.11/4.15) | PASS |
| §6 early stops: admit 181/248, revoke 63/113, logic 3/264, trap 0/127, cost 40/125 | reproduced item-wise (adaptive rounds_used < deep16 rounds_used) | PASS |
| Cap-hit rate 0/877 | 0 cap=1 flags in all 5 adaptive ledgers, 877 VERDICT lines | PASS |
| C6-wason: 5 items, wrong at d4, right at d8 | TRAP-C6-001..005: d4 WRONG (4/7 evidence seen), d8/deep16/adaptive CORRECT (7/7 seen) | PASS |
| A/B byte-identical 60 cells × jsonl/ledger/stdout; parse 877/877 every cell | PASS |
| `correct` field = verdict==GT | 0 inconsistencies in 5,262 records | PASS |

**Zero discrepancies of any size vs RESULTS_H5.md.** The sweep data are solid.

### New facts the raw records add (not in the summary doc)

1. **The doc's headline "knee at depth 4" is not the frozen rule's output.** Mechanical
   frozen rule (d(p)=acc(p)−acc(p/2) in pp, knee = smallest p with d(p)<1 and all
   later <1): trap → d(2)=+33.07, d(4)=+62.99, d(8)=+3.94, d(16)=+0.00 → **knee=16**;
   pooled → d(2)=+4.79, d(4)=+9.12, d(8)=+0.57, d(16)=+0.00 → **knee=8**. The doc's
   "knee at 4" is a third, non-frozen quantity (eyeball on per-nominal-round gains).
   Three "knee" numbers are in play: 4 (doc rhetoric), 8 (pooled frozen rule),
   16 (trap-only frozen rule). The adjudication flagged the 16 as off-by-one; the
   4 was never the rule's output at all.
2. **The "two orders of magnitude per round" rhetoric is ~32×, not 100×, and both
   numbers divide by nominal cap.** Per rounds *actually spent* on trap:
   d1→d2 +42 items/1.00 round = 42.0/round; d2→d4 +80 items/1.48 rounds = 54.1/round;
   d4→d8 +5 items/0.33 rounds = 15.1/round; d8→d16 0/0. The per-round decline past
   d4 is **~3.6×** (54.0 → 15.1), and d2→d4 is the *best* interval per round spent.
   The 100× figure is (0.315)/(0.0098) ≈ 32× per *nominal* round — 1.5 orders, not two.
3. **The d4→d8 gain is pure evidence-window.** The 5 wason items each carry 7
   evidence items and naturally terminate at 8 rounds (7 evidence + a final
   elimination/refutation round, evidence_consumed=7, rounds_used=8). At d4 they
   see only 4 of 7 premises → wrong; at d8 they see all 7 → right. "Depth" here
   = "how many of the ≤9 evidence items you were allowed to consume."
4. **Trap natural round-lengths are 2/3/4/5/8** (adaptive distribution:
   24/18/58/22/5 items) — set entirely by evidence-set sizes. Cap 16 never binds
   because no stream is longer than 9 items. All 127 adaptive trap runs consumed
   100% of their evidence: natural termination, not settling.
5. **Adaptive < deep16 ⟺ §6 fired first** (verified in `dlb_delib.zag`: the loop
   is identical until a stop fires; `progress==0` natural termination would stop
   both at the same round). So the 181/248, 63/113, 40/125 early stops on
   admit/revoke/cost are genuinely §6 firings with zero accuracy loss.
6. **Cost battery `optimal_stopping_depth` was dropped by the encoder**
   (items_v2/cost.jsonl keys: ground_truth, id, input, task_type only) — matches
   the doc's §8.2 admission. The prereg expectation "ADAPTIVE rounds_used should
   track d*" is untestable on this data.
7. **The sensor is coarser than the doc implies.** Confidence (thousandths,
   clamp(leader−runner-up,0,1000), 1000 if one hypothesis alive) takes only
   values {400,500,700,710,764,800,1000} across all batteries. ε=20 in these
   units. "Stable" means "clamped margin stopped moving" — on verdict-anchored
   batteries it slams to 1000 almost immediately.

## 2. Steelman FOR the adjudicated position

**(a) Knee = operating envelope, not a constant.**
- Four of five batteries are ceilinged at depth 1; the pooled curve is the trap
  curve diluted (pooled d1 = 750/877 = 0.855 exactly = non-trap items all right,
  all 127 trap items wrong). A "pooled knee" is not a system property.
- On the only battery with a curve, the entire d4→d8 gain is 5 wason items whose
  natural length is 8 rounds — i.e., the "knee" is set by *evidence-set lengths in
  this item distribution* (max 9 items), not by a property of deliberation.
  Change the distribution, change the knee. RESULTS §8.3 already concedes the knee
  may not generalize beyond this harness's score mechanics.
- Cap 16 is a null (0/877 hits; trap d8 == deep16 == 3.81 rounds exactly). Nothing
  distinguishes 8 from 16 on this data, so any constant ≥8 is arbitrary; 4 leaves
  known-wrong items on the table. The honest summary is an envelope: saturation at
  cap 8, ~3.8 mean trap rounds, d4 at 96.1%, the d4-vs-d8 choice = exactly 5 wason
  items.
- Three inconsistent "knee" numbers already exist (4 rhetoric / 8 pooled-rule /
  16 trap-rule). Enshrining any one of them as law bakes the off-by-one into the
  architecture.

**(b) Residual-flip bound for conflict streams; §6 kept as cost heuristic.**
- On traps the §6 rule was vacuous *by correctness*: the margin was honestly
  moving until evidence exhaustion, and a stability rule *should* refuse to stop
  there. The data support "run until evidence exhaustion" as the right policy for
  finite conflict-bearing streams — the harness already implements the exhaustion
  half of the bound naturally (all 127 trap adaptive runs consumed 100% evidence).
- The residual-flip half ("stop when remaining evidence provably cannot flip the
  leader") strictly dominates §6 on safety: it can only stop where §6's "settled"
  condition is provably safe w.r.t. future flips. On the easy batteries where §6
  currently fires, contenders are eliminated (conf=1000, one hypothesis alive) —
  and an eliminated contender *provably* cannot flip, so the bound would fire
  there too, no later than §6. The 284/486 genuine §6 savings are preserved under
  the bound; the bound adds a principled floor that §6's stability heuristic lacks.
- Uncalibrated sensor + ε in incomparable units means §6's "settled" is a score
  artifact; the bound is denominated in *leader-flippability*, which is the actual
  decision-relevant quantity. Recalibration and the bound are complements: the
  bound says *when it is safe* to stop, calibration says *what thresholds mean*.

**(c) The delayed-disconfirmation battery is the right next test.**
- It is the one input class the frozen design never contained: a ≥3-round
  confidence plateau while the running answer is wrong, then a late flip. The
  current data cannot tell whether §6's 284 easy-battery stops are "genuine
  settling" or "plateaus that happened not to flip" — k=3 cannot distinguish a
  mid-stream plateau from exhaustion, and this design never tried.
- It simultaneously tests both live hypotheses with one battery: if §6 stops
  inside a wrong plateau, ADAPTIVE-WINS is an artifact of never-plateauing traps
  and the verdict needs revision; if extra depth flips correct→wrong (the
  overthinking matched set), deeper caps are non-monotone and any knee/cap
  thinking is unsafe; if neither happens, evidence-exhaustion is confirmed as
  the right trap policy and the sensor is demoted to a cost heuristic for easy
  items. One battery, three decisive branches — maximum information per run.
- The misleading-premise dose curve (0/1/2/6) gives the first distributional
  evidence on whether rounds track residual conflict, which is exactly what the
  operating-envelope position needs to graduate from "one harness, one curve."

## 3. Steelman AGAINST the adjudicated position

**A constant is justified — and the off-by-one has a clean answer.**
- Operationally the harness needs *some* config value; "envelope" is not a
  setting. The strongest constant is **cap 8**, justified on accuracy, not on the
  knee rule: d8 achieves 1.000 on all 877 items (the smallest depth that does —
  d4 leaves 5/127 trap items wrong), and cap 16 buys nothing over 8 on this
  distribution. If the deployment cares about adversarial/misleading inputs — and
  the trap battery is *the* depth probe (the other four are convergence checks
  per §8.1) — then d4 is provably unsafe and 8 is the minimal safe constant.
- The off-by-one critique is answered by fixing the rule, not abandoning it:
  rewrite "knee" as the smallest p where the doubling *arriving at* p is <1pt
  **and** acc(p) is already saturated — i.e., label the *state* at p, not the
  interval. Applied per battery: trap saturates at 8 (mechanical 16 was the
  labeling error; pooled already gives 8). The doc's eyeball-4 then reads
  honestly as the *cost-efficiency elbow* (per-round returns decline 3.6× past
  d4), a separate quantity from the saturation constant. Constant for accuracy:
  8. Elbow for cost: ~4. No contradiction, no envelope needed — two numbers, two
  purposes.
- Micah's standing law is "when in doubt, test both" — the constant position is
  testable (does cap 8 hold 1.000 on new batteries?) while "envelope" risks being
  an unfalsifiable hedge. A wrong constant gets falsified by the next battery;
  an envelope absorbs everything and predicts nothing.

**The residual-flip bound is vacuous in practice, or §6 suffices.**
- The bound's premise — a known, finite, pre-listed evidence stream whose
  remaining items have bounded weights — is exactly the harness's artificiality.
  In the real architecture deliberation is open-ended state: "remaining evidence"
  is undefined, so the bound collapses to "never stop early except on
  exhaustion" plus whatever heuristic you were trying to replace. It is
  well-defined only where it is unneeded.
- Even in the harness, implementing the bound requires the judge to see future
  evidence weights up front — the item encoding already exposes all evidence at
  once, which a real deliberator never has. The bound is testable in the harness
  but not portable to any system that generates its own considerations.
- Empirically, §6 already *is* the bound on this data: on conflict streams it
  refused to stop while the margin honestly moved (0/127 premature stops — the
  correct behavior, provable post hoc: every §6 stop on easy batteries had zero
  accuracy loss, and every trap run exhausted its evidence). The residual-flip
  bound adds machinery to certify what the sweep already demonstrated. And where
  the bound would fire *before* exhaustion (leader insurmountable mid-stream),
  that is precisely the eliminated-contender case where §6 fires anyway via
  conf=1000 → gains of 0. The bound's firing set is a subset of {§6 firings ∪
  natural terminations} on every battery measured. New rule, same behavior,
  more code.

**ADAPTIVE-WINS is already solid; no new battery is needed.**
- The prereg criteria are met mechanically: |acc_adaptive − acc_deep| = 0 ≤ 1pt
  on all five batteries; mean rounds lower on 4/5 (54%/34%/12%/2% savings, 0%
  on trap where §6 was correctly vacuous); censoring 0/877 ≪ 1/3. The verdict is
  prereg-valid and doesn't need rescuing.
- The plateau-then-flip battery is a bespoke adversarial construction: any
  fixed-k stability rule is defeatable by a (k+1)-round plateau *by theorem*,
  so the battery tests the encoder's ability to defeat §6, not a property of
  deliberation. What matters for an operating envelope is the *base rate* of
  plateau-then-flip in natural evidence streams, which a hand-built battery
  cannot supply — it can only produce an existence proof, which we already have
  by construction.
- The overthinking matched set (extra depth flips correct→wrong) cuts against
  the program's own evidence: the sweep shows monotone convergence on all 877
  items, and the wason mechanics show depth = evidence consumption. Deliberately
  building misleading-late-evidence items measures the encoder's malice budget,
  not the system's stopping policy.
- Opportunity cost: the same effort spent on harness variations (different score
  mechanics, longer/noisier streams — §8.3's stated generalization gap) would
  test whether the knee replicates, which is the actual open question.

## 4. Undecided questions

| # | Question | Evidence that would settle it | Exists yet? |
|---|---|---|---|
| 1 | Knee: operating envelope vs a constant (4? 8? 16?) | Replicate the sweep on ≥2 harness variations (different score mechanics, longer/noisier evidence streams, different item distributions): does saturation-at-cap-8 with ~4 mean rounds replicate, or does the knee move with the distribution? | No — one harness, one distribution, one score mechanic (§8.3 concedes this) |
| 2 | Confidence-sensor recalibration: what quantity replaces clamped leader−runner-up, and how are thresholds set? | A recalibration trial: candidate sensor(s) with reliability measurement (binned predicted confidence vs empirical accuracy) on a battery with graded difficulty; ε/k chosen from the calibration curve, not inherited | No — current sensor is clamp(margin,0,1000), 7 distinct values observed, ε=20 in incomparable units; no calibration data exists |
| 3 | Residual-flip bound vs §6 for conflict streams: is the bound implementable, and does it ever fire before exhaustion? | Implement the bound in the harness (needs a stated per-evidence weight ceiling), rerun the sweep: count bound-firings on trap/admit/revoke/cost; then run it on plateau-then-flip items to check it refuses where §6 fires | No — the bound is a paragraph in the adjudication, not code; no firing data |
| 4 | Delayed-disconfirmation battery: build it (plateau-then-flip + matched overthinking + misleading-premise dose curve), or is ADAPTIVE-WINS sufficient? | The battery itself, run under frozen §6 with preregistered item-level stop rounds: does §6 stop inside a wrong plateau? does extra depth flip correct→wrong? do rounds track the 0/1/2/6 dose? | No — not built; deeper dispute is whether the battery should be adversarial (existence proof) or distributional (base rates) |

## 5. Notes for the debate round (do not act on yet)

- Do NOT propose new battery designs in this round — per task, that comes after
  grok's response lands. (Grok round 1 came back empty; sol still provider-down.)
- Raw records: `~/workspace/scratch-h5/sweep/` (not committed to the repo branch;
  committed `results_v2/` holds only RESULTS_H5.md). Independent re-derivation
  script: `~/workspace/h5_resolution/debate_prep/rederive_h5.py`.
- Commit nothing; scratch prep only.
