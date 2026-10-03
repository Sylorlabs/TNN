# AMENDMENT 01 — G6/P1: corrections to hand-traced predictions

**Date: 2026-09-22. Status: recorded BEFORE the implementation run is
finalized (the first smoke run exposed arithmetic slips in the frozen
predictions; the experimental design is unchanged).**

The fork-prereg's experimental design (schedule, arms, kill-bar
definitions) is untouched. What changes are six hand-traced *predicted
numbers*, each with a design-level derivation showing the code implements
the preregistered design correctly and my arithmetic was wrong:

- **A1 — identity probe count 19 → 20.** The schedule rule is
  "E%40==10 in E49–848". E50 satisfies it (50%40==10, 50%20≠0,
  50%4≠0) and was omitted from the hand count. Probe steps are
  50, 90, …, 810 (20 total). Consequential: KB-2/KB-3 identity counts
  19/19 → 20/20; scaffold persist contests 259 → 260 (200 + 40 + 20);
  `b_post_contest` 264 → 265; `b_total_contest` 277 → 278;
  `b_quar_used` 277 → 278; `b_ident_blind` 19 → 20.
- **A2 — baseline quarantine 267 → 264.** E11–13 calibration episodes
  simulate the rule on scratch copies (the trial's own design); they
  never touch the real store, so they contribute 0 quarantine entries —
  exactly as in the RL trial (48 contests / 48 quarantine used).
  `a_quar_used` 267 → 264. `a_total_contest` stays 264.
- **A3 — scaffold rekeys 8 → 9.** The probe cursor acts REKEY at E29
  (the episode the namespace audit then eliminates); it was omitted
  from the hand total. Rekeys: E13,15,17,19,21,23,25,27,29.
  `b_total_rekey` 8 → 9.

Kill-bar verdicts are evaluated against these corrected numbers. No
kill-bar definition, schedule rule, arm logic, or static check changed.
