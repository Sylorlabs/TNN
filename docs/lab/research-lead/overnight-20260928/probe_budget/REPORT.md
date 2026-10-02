# REPORT: Experience-Set Probe Budgets (PBUDGET)

Verdict: PROBE-BUDGET-COMPLETE. All 5 frozen kill bars pass. 3/3 runs
byte identical.

## Result

The learner managed a 5 probe budget across a 30 step stream with a
regime drift at t=15. Behavior, from learner state alone (surprise
gated by an adaptive threshold, no drift knowledge, no info values,
no baseline knowledge):

- 0 probes spent on the 15 redundant pre drift steps, despite budget
  being available from t=0.
- All 5 probes concentrated on the drift window t=15,16,17,18,19.
- Budget exhausted exactly at t=19; 6 further probe-wants refused at
  t=20,23,25,26,28,29 (the cap demonstrably binds and is respected).
- Captured information 50 of 50 available informative units, vs 14
  for the uniform baseline (3.57x).

## Kill bars (frozen in PREREG.md)

KB1 budget respected and binding: probes_used=5 <= 5, refused=6 >= 1.
PASS.
KB2 informative probes under constraint: captured=50 >= 40. PASS.
KB3 drift detected within budget: drift_probes=5 >= 4. PASS.
KB4 beats naive allocation: captured=50 >= 2*14=28. PASS.
KB5 determinism: 3 runs byte identical, sha256
2426075a922faa388f9307dfd008737fdba9cd7d4400787c05210a0b0bccccb7
x3 (runs/sha256sums.txt). PASS.

## Method notes

- Single pure Zag file src/probe_budget.zag (world + learner +
  driver, one raw syscall flush). Compiled with the pinned znc,
  first try, no warnings beyond the zagd notice.
- Static audit: pb_learner and pb_learn never call pb_info; hidden
  labels are resolved by the driver only after a spend decision.
- Zero modes, bridges, handlers. No forbidden executable invoked at
  any point (safebin PATH, python3/python do not resolve).
- One hand trace sign slip was found during verification (t=24 pred);
  the binary's own trace is self consistent and the bar margins are
  unaffected.

## What this shows, and the boundary

Shown: a generic surprise gated learner can manage a hard probe
budget across time: it spends nothing while the world is predictable,
concentrates the full budget on the informative drift window, and
stops when the budget binds. Not claimed: triage among competing
simultaneous novelties under a budget too small for all of them;
probe input selection from an open pool under a budget (LPROBE had
no budget); learner set budget sizing (budget=5 is a frozen
experimental parameter); transfer of the budgeting policy across
domains.

## Governance

- Prereg commit 2ae81480a (NAMECHECK.md + PREREG.md first appear
  there; no implementation existed). Disclosure: the commit swept in
  two other workers' already staged files
  (truncate_theorem/PREREG_AMENDMENT1.md and a 4 line
  learner_probes/NAMECHECK.md touch); unrelated to this wave and
  left untouched.
- Implementation commit: (recorded after commit).
- Nothing pushed. Paper untouched. Frozen assets read only.
