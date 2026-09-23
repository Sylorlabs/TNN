# Autonomous RSI Run 1 — Phase 0 baseline (frozen)

Date: 2026-09-22. Prereg: RUN_PREREG.md (frozen, amending only with Micah's word).

## What is being measured

The autonomous run subjects the RSI-3 champion to a 1-hour autonomous
self-improvement loop. Scores to compare before/after (measured, not assumed):

| Score | Before (frozen source) | Where measured |
|---|---|---|
| Recency-vs-coherence battery, ask-first arm | acc 22/24, wrong 2/24, cost 424, RECALL 10000, COST-quiet 200 | work/fidelity + VERDICT_R4C.md (commits 48bde930, 0c12d717) |
| Coding | 18/18 | committed verdict record (to cite at post-run regression) |
| Epistemics | 59/94 | committed verdict record (to cite at post-run regression) |
| Speed mechanisms | ~65.1% fewer evaluations, ~37.8% fewer compiler calls | committed verdict record (to cite at post-run regression) |

Post-run FULL regression inventories every historical runnable suite
(RUN_PREREG.md §12) — no score is assumed, every one is re-measured.

## Subject proven in Phase 0 (fidelity gate, all passed)

- work/subject.zag = byte-verbatim rsi4c.zag + decide.zag.inc prepended
  + a `prop` mode. SHA256 (subject.zag): `06eaec29...` (see ORIGIN_SHA256/SUBJECT_SHA256).
- The frozen oracle (verify_rsi4c.py) on subject's 4 original modes
  reproduces VERDICT_R4C exactly: base 8/0/0, recency 8/16/48,
  coherence 20/4/168, askfirst 22/2/424, 5/5 byte-identical,
  fields==CSV, NO-CHAMPION (the KB3 drafting defect — recorded, not altered).
- gt never leaves the batteries: subject source references no
  gt-carrying file; decide() receives only fields; the proposer receives
  only proxy gt (the 24 disjoint calibration items) and real fields.

## Champion at loop start (ROUND 1 state)

- Policy: ask-first (measured 22/24, 2 wrong, cost 424 — the best
  measured arm; the KB3 no-champion verdict is recorded as a defect and
  does not override the measured scores).
- State: kept=- tried=- retired=- barren=b0 web=web0.
- Proposer round-0 deliberation (3/3 deterministic) selected C1 with
  published predictions: dacc=+2, dwrong=-2, cost=456.

## Restoration

Nothing outside rsi/autonomous_run_1/ is touched by the loop. The RSI-3
sources, batteries, and oracles are unchanged (ORIGIN_SHA256). If the
run corrupts itself, the restore is: nothing — the lab directory is
additive-only.
