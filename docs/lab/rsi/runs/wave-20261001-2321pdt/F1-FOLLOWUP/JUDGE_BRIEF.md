# JUDGE_BRIEF.md - F1-FOLLOWUP narrowed trigger re-test and constructor characterization

Provenance:
- RENDER_SHA: 27116eb12 (sealed evaluation commit; preregs 001fcfaca
  and 6dee24671, methodology 34960a9bc, Part 2 fixtures 63922a500, all
  on branch tnn-native-lab, local only)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F1 BUILD-FAIL on K-C0C-REG R-W2, bar-calibration
  mistake owned (fresh-seed regression fixture conflated trigger
  regression with constructor seed-robustness)
- NEW_KNOWLEDGE_CLAIM: The windowed failure-density trigger introduces
  zero regression on the prior wave's validated W2 fixtures (identical
  trigger episode, construct sequence, structure, and hidden
  predictions), and the greedy depth-1 trial constructor overfits 6 of
  24 fresh sealed sum2 worlds (25 percent) with no pre-registered
  whole-fixture property separating overfit from correct seeds.

## Part 1 verdict: BUILD-PASS (corrected bars)

Governing bars (frozen in PREREG_PART1.md, committed alone at
001fcfaca before any sealed run of this lane; no implementation work
exists in this lane; binary under test is F1's frozen impl/f1_learn):

PASS:
- K-TRIG-FIRE: trigger fires within 12 episodes on all four sealed
  interleaving patterns (T-A ep 2; T-B ep 3; T-C ep 4; T-D ep 1).
- K-TRACE: 3, 2, 2, 6 construction events, all at or after the first
  trigger episode.
- K-LEARN-INTERLEAVED: 30/30 hidden on all four patterns (bar 80%).
- K-TRIG-CLEAN: 0 triggers on all three clean worlds (frozen rate 0).
- K-C0C-REG Leg W2 (the correction): on the prior wave's validated
  W2 fixtures, the new binary reproduces the old binary's behavior
  exactly: same TRIGGER episode (1), byte-identical normalized
  CONSTRUCT event sequence (3 events, err transitions 6->2, 2->1,
  1->0), identical final main-graph signature (f1_score sig ISO 1,
  structure [4 4 4 2]), hidden 30/30 for both, hidden pred outputs
  byte-identical. Zero trigger regression.
- K-C0C-REG Leg R-W3: 30/30 hidden, 2 construction events.
- K-ABL-TA: 57pp drop when the structure is removed (bar 40pp).
- K-BASE-TA: 57pp margin over the exact-match memorizer (bar 40pp).
- K-C0A: zero forbidden semantic sites in the frozen source.
- NC-TRIG: prior wave's binary produces 0 triggers on sealed T-A.
- Determinism: 24 invocations x 3 repetitions, all byte-identical.

No bar was weakened. The original BUILD-FAIL came from the
bar-calibration mistake, not from the trigger. Bounded L2+ ceiling
stands; no L3 claim follows.

## Part 2 verdict: NOT-FOUND (per the frozen decision rule)

Governing bars (frozen in PREREG_PART2.md, committed alone at
6dee24671 before any Part 2 fixture was generated; fixtures committed
at 63922a500 before any Part 2 sealed run):

- Overfit rate: 6/24 = 25 percent (seeds 2, 3, 5, 13, 17, 18; hidden
  accuracies 5, 0, 2, 0, 1, 0 out of 30; all 18 correct seeds at
  30/30). All 24 seeds complete 3/3 byte-identical.
- Separation analysis (pure-Zag cw2_sep, frozen rule misc <= 2): no
  fixture property qualifies. Best is F6 (zero-input episodes <= 6
  predicts overfit) with misc = 4. Full contingency tables are in
  SEALED_EVAL_PART2.md.
- Consistency check: F1's sealed rW2 overfit fixture (seed 2301)
  shares no cleanly separating property with the 6 overfit seeds.
- Mechanistic explanation (post-hoc, explicitly not the frozen-rule
  pattern): in all 6 overfit seeds the greedy second construct adds
  the same feature again (or doubles the accumulator) instead of the
  complementary feature, locking into a degenerate composition
  (3x0+x1, 3x0+2x1, 4x0+x1, 3x1+2x0, 4x1+x0, 3x1+2x0). The trigger
  fires at episode 1 on all 6, so the greedy path is decided by the
  x0/x1 error-mass balance of the first-trigger buffer, which the
  whole-fixture features F1..F6 cannot see. This is a candidate
  hypothesis for a future prereg (trigger-time-buffer features,
  frozen before runs), not an identified pattern here.

## What the judge should know

1. The F1 BUILD-FAIL is resolved as a calibration artifact: on the
   validated fixtures the trigger passes every bar including exact
   behavioral reproduction of the old binary. Accepting the windowed
   trigger as the fixed failure monitor remains the recommended
   coordinator action from F1's brief.
2. The constructor's greedy-trial seed-sensitivity is now quantified:
   25 percent overfit on fresh sealed sum2 worlds, with a mechanistic
   failure mode (greedy second-step compounding) but no validated
   whole-fixture predictor. This is constructor work for a future
   wave, not trigger work.
3. Commit-order self-check: preregs (001fcfaca, 6dee24671) precede
   methodology (34960a9bc), which precedes Part 2 fixtures
   (63922a500), which precede sealed runs and evaluations
   (27116eb12). No bar moved after freezing.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP/):
- PREREG_PART1.md, PREREG_PART2.md, NAMECHECK.md
- SEALED_EVAL_PART1.md, SEALED_EVAL_PART2.md
- sealed/ (Part 1 fixtures, FIXTURE_SHA256.txt, run_sealed1.sh)
- sealed2/ (Part 2 fixtures, FIXTURE_SHA256.txt, gen2.sh,
  run_sealed2.sh)
- runs1/, runs2/ (3 repetitions each, DETERMINISM_SHA256.txt)
- dev/ (f1_wgen, f1_score copies; cmp_events, cw2_analyze, cw2_sep
  pure-Zag sources and binaries)

No em-dashes in this document.
