# H3 lesion-ablation calibration controls (prereg §4)

These lesions validate the HARNESS (scorer), not the learner. They run against
the frozen fixtures + frozen scorer. If either lesion passes, the scorer is
void: verdict BLOCKED, no learner conclusion drawn. This is what makes
"I failed to learn" detectable at the harness level.

## L1 — recall-always-match

- Lesion: replace the recall/match function so EVERY processed S-sentence is
  reported KNOWN (matches installed memory K), regardless of content.
  One-line change (or config flag) in novel.zag's driver; nothing else changes.
- Run against: battery N (corpora N1–N4), frozen fixtures, frozen scorer.
- Required outcome: the scorer MUST FAIL this run on H3-K2
  (plain-novel recall: 16/16 planted facts installed). A lesioned learner
  installs 0/16 and reports no novel facts, so a correct scorer fails it
  (FNR = 16/16, precision undefined → FAIL).
- If the scorer passes L1 → scorer void → BLOCKED.

## L2 — recall-never-match

- Lesion: replace the recall/match function so NO S-sentence ever matches K
  (every sentence is a novel-candidate).
- Run against: battery E (corpora E1–E4), frozen fixtures, frozen scorer.
- Required outcome: the scorer MUST FAIL this run on H3-K1
  (empty honesty: 0 novel claims, 0 installs, 4/4 EMPTY). A lesioned learner
  claims novelty on every known quote, so a correct scorer fails it
  (FPR = 4/4 → FAIL).
- If the scorer passes L2 → scorer void → BLOCKED.

## Notes

- Lesions are harness-validation controls owned by the mechanism/scorer crew;
  they are specified here (frozen) so the fixtures they run against cannot
  be re-tuned after the fact.
- Lesioned runs must not be confused with genuine learner runs: lesion runs
  are labeled `LESION|L1|` / `LESION|L2|` in logs and excluded from verdict
  tallies.
