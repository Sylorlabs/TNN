# REPORT.md - F1RT independent red team on the F1 seed-sensitivity finding

Lane: F1RT, wave wave-20261002-1121pdt. Branch: lane-f1rt-20261002-1121pdt.
Task: promotion pipeline step 10 (independent red team) for the F1
seed-sensitivity finding. This lane did not produce the finding.

## Provenance of the artifact under judgment

- Finding: "Greedy-trial seed-sensitivity is a constructor property with
  measured magnitude X" where X = (R=13/40 overfit, T=2 first-trial
  classes, D_ops=9 structural paths, Cmax_ops=15/40 concentration).
- Verdict commit: 655c8d7d6cffff47cef29e41c5b2dba31ae5ba27 on branch
  lane-f1-20261002-0821pdt ("F1: sealed runs + analysis + verdict. K-DET
  PASS, NC-HARNESS PASS, bars ALL-PASS. FINDING CONFIRMED.").
- Commit order verified: prereg 7eb914323 < methodology ae9036bf5 <
  fixture manifest 86cbc3a73 < results 655c8d7d6. No ordering violation.
- Frozen constructor binary: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn,
  sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
  used read-only throughout; hash verified before every use.

## RED-TEAM VERDICT: the finding SURVIVES

All four attack classes were executed in pure Zag under the safebin guard
(`which python3` empty; Step 0 recorded in NAMECHECK.md, commit 96a199052).
None killed the finding. Two framing qualifications are recorded below;
they weaken the description, not the numbers or the mechanism.

## Attack (d): independent reproduction from committed source alone

- Recompiled f1_wgen, f1_score, f1s_analyze from the committed .zag sources
  with the pinned znc: all three byte-identical to the committed binaries.
- Regenerated all 120 sealed fixtures (55xx series, 40 train + 40 hidden +
  40 truth): byte-identical to the committed sealed5/ fixtures.
- Re-ran the full battery (40 seeds x 3 repetitions, frozen binary):
  K-DET PASS, 3/3 byte-identical reruns on the independent execution.
- Independent outputs == committed runs/1 byte-identically: all 40 seeds,
  all six artifact kinds (state, trace, pred, stdout, stderr, rc).
- DETERMINISM_SHA256.txt: all 240 artifact hashes match the committed file.
- Independent analyzer rt_analyze.zag (written from scratch for this red
  team; safe single-buffer emit pattern, independent accuracy computation):
  SUMMARY N=40 R=13 T=2 D_ops=9 Cmax_ops=15, exactly matching the committed
  analysis/RESULTS.txt. This also guards against the pinned-znc _zag_print
  miscompile pattern present in the lane's analyzer.

Result: REPRODUCTION SURVIVES. The numbers are exactly what the committed
source produces.

## Attack (a): harness artifact

- Seed leakage: KILLED as an alternative. f1_learn takes no seed argument
  (confirmed from the committed source). The seed enters the constructor
  only through the train episode values. Trial enumeration is frozen ISA
  order with first-tie-wins argmin; the whole run is deterministic in the
  episode file (K-DET re-verified independently).
- Non-determinism in the test path: none found. 3/3 byte-identical reruns
  on the independent execution; independent outputs match committed.
- Scorer / hidden-truth audit: independent accuracy recomputation confirms
  all 40 hidden accuracies. The near-miss seeds (18: 1/30, 26: 1/30,
  29: 3/30) are genuine wrong laws (verified in traces: X0+4*X1, 3*X0+X1),
  not mis-scored or misaligned rows. Correct seeds get exactly 30/30, so
  the hidden truths are correct.
- NC-HARNESS independently re-verified: 6/6 Part 2 fixtures byte-identical,
  3/3 deterministic reruns, hidden preds byte-identical to the prior lane's
  runs2/1, known accuracies (30, 30, 5, 0, 30, 2) all reproduced exactly.

Result: NO HARNESS ARTIFACT FOUND.

## Attack (b): alternative explanations and ablation

- "Two failure modes" (red-team hypothesis that the ncons-3 near-misses
  were a different phenomenon): KILLED by evidence. All 13 failure seeds
  show the documented greedy-compounding signature in raw traces
  (strictly error-reducing trials that re-add an already-added feature or
  double the accumulator). The verdict's white-box check cited seeds 0
  and 5; this red team verified the signature on all 13, so the check is
  stronger than reported.
- "It is the data, not the constructor" (train data unidentifiable):
  KILLED by evidence. The final constructed graphs achieve only 3/24 to
  8/24 on their own 24-episode train sets (measured by running the final
  state on truth-masked train episodes through the frozen binary), while
  the correct law achieves 24/24 by construction. The train data identifies
  the law; the greedy search fails to find it. This is a constructor
  property, not a data property.
- "Frozen-order tie-breaking artifact": KILLED by evidence. First-trial
  winners are strict argmin on the buffer, not ties (e.g., seed 0:
  ADD R0,X1,X1 strictly beat ADD R0,X0,X0 on its 2-episode buffer).
- Mechanism ablation (trigger timing): built an exact Zag reimplementation
  of the constructor (verified byte-identical to the frozen binary on all
  40 seeds first), then delayed the failure trigger FMIN 2 -> 4 so the
  first burst decides on 4-6 episodes instead of 2. Result: R drops 13 -> 8
  but the identical compounding signature persists; the failing set shifts
  (6 persist, 7 recover, 2 new). T=2, D_ops=9, Cmax_ops=18; all three
  property bars would still pass. The phenomenon is robust to trigger
  timing, not an artifact of FMIN=2.
- White-box mechanism fully characterized from the ISA source: ADD
  overwrites R0 (R[p1] = op(p2) + op(p3)); the failures are irreversible
  overshoots (final laws 2*X0+3*X1, 3*X0+2*X1, X0+4*X1, 3*X0+X1); the
  recoveries (groups 2, 7, 8) occur exactly when a later burst's argmin
  selects a corrective overwrite. Every CONSTRUCT line in every failure
  trace strictly reduces buffer error while moving away from the true law.

Result: MECHANISM ATTRIBUTION SURVIVES. The greedy-compounding failure
mode is real, white-box visible, and robust.

## Attack (c): metric gaming

- R counts genuine catastrophic misses (10 at 0/30, 2 at 1/30, 1 at 3/30);
  the frozen binary cannot adapt to the metric. The accuracy distribution
  is not a threshold artifact.
- T=2 and D_ops=9 / Cmax_ops=15 are structural facts read from traces.
  The frozen bars are weak floors (T>=2 observed exactly 2; Cmax<=32
  observed 15), but they are honestly reported and the finding's weight
  rests on the measured X, not the floors.

Result: NO METRIC GAMING FOUND.

## Qualifications (framing weakened, numbers untouched)

1. "Overfit" is a misnomer. The 13 failures are not classical overfit
   (fit train, fail test): the final graphs score only 3/24 to 8/24 on
   their own train sets. The accurate description is greedy local-optimum
   trapping: the 1-step argmin overfits the tiny evaluation buffer
   (2 episodes at the first trigger) and the ADD-only irreversibility
   makes the trap fatal. The prereg stipulates "overfit" operationally as
   any hidden miss, so the numbers stand, but future citations should call
   R a catastrophic-failure / greedy-trap rate, not an overfit rate.
2. T=2 is not causal for the failures. Both first-trial classes contain
   correct and failed seeds (seed 8 starts ADD_X1_X1 and scores 30/30;
   seed 5 starts ADD_X0_X0 and scores 0/30). K-SS-TRIAL measures real
   trial-choice variation, but the failure driver is the compounding path
   (D_ops), not the first trial.

## Process note

The attack plan came from the task specification (a)-(d); no separate
frozen red-team prereg was written before the ablations (FMIN=4 was chosen
during the work). All analyses were kill-attempts, so any bias runs toward
killing, not saving; the SURVIVES verdict is conservative.

## Commits (this lane branch lane-f1rt-20261002-1121pdt)

- 96a199052: NAMECHECK.md Step 0 (safebin guard PASS) + read-only
  extraction of F1 methodology and frozen binary.
- (this commit): REPORT.md + red-team tools (rt_analyze.zag, rt_mask.zag,
  rt_f1var.zag exact reimplementation, rt_f1var_fmin4.zag ablation) and
  evidence (rt_report.txt, rt_report_fmin4.txt, var_fmin4_acc.txt,
  manifests). No file outside this lane's dirs touched.

## Queued next (for coordinator)

- Correct the "overfit" label in the finding's canonical description
  (recommend "greedy-trap rate"); coordinator decision.
- Optional: 2-step-lookahead ablation to separate 1-step myopia from
  buffer myopia; not required for the verdict.
- FMIN4 robustness evidence (R=8, same mechanism) is filed in this lane
  for any future generality discussion.
- Promotion pipeline step 10 is complete: no red-team block on the F1
  finding. Promotion itself remains the coordinator's/Micah's decision.
