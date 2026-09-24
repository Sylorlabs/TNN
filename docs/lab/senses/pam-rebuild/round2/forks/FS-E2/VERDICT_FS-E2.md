# VERDICT_FS-E2.md — "Formation-Precondition Gate"

**FINAL. Date:** 2026-09-24. **Crew:** FS-E2 build+eval. **Verdict: ALIVE.**

## Provenance chain

1. Phase 0 (formation reproduction): committed
   `28aa3938bee2b6b86de08d09360f957a01fa5865` —
   independent pure-Zag formation reimplementation reproduces FS-E1's Bar-4
   overall 80.30% EXACTLY (1606/2000), with 2000/2000 per-fixture judgment
   agreement against FS-E1's frozen ledger; per-task formation on the full
   R2A normal sets measured for scoping.
2. Phase-1 prereg: `round2/preregs/PREREG_FS-E2.md`, committed ALONE pre-eval
   `5cd2b9679f914313067d3e29c45c1bf4360cffb5` — scope, mechanism, joint bars,
   and batteries frozen before any gate result existed.
3. Eval: fresh deterministic execution (this verdict), ledgers below.

## Mechanism (as preregistered; no deviations)

- Gate: FS-E1's frozen truth-quantity challenge registry, executed via the
  frozen binary `forks/FS-E1/build/fse1`
  (SHA-256 `21fc159c232d4b3e3acd57cfc933c55d71b4fa34c8cc9cd0fc1b33a0b80690a5`,
  verified at eval start; source `e31a4588821ebadd058a9c2e6d4a50e3218701209ad32e640412fde5eee74118`,
  registry 9a8a68e4). INSTALL iff challenge outcome == formation claim.
  No quantity redesign, no formation changes.
- Scope (frozen): install authority on colordisc (92.96%), pitchdisc
  (97.92%), motiondir (96.63%) — all >= 85% formation per Phase 0.
  colorconst (56.81%), shapetrans (80.56%), timbredisc (38.89%) are
  explicitly ABSTAIN-scoped (deterministic hash-chained abstention ledger;
  never in any denominator).
- Batteries: frozen `b_adv` (10,000) + `b_ctrl` (2,000), fresh deterministic
  execution. In-scope: 5,290 adversarial / 1,280 controls.

## Joint-bar results

| # | Bar | Result | Pass |
|---|---|---|---|
| 1 | FI Wilson 95% UCB <= 1%, in-scope adv (n=5290) | 7 FIs, rate 0.132%, **UCB 0.273%** | YES |
| 2 | Recall >= 85%, in-scope controls (n=1280) | **91.09%** (1166/1280) | YES |
| 3 | Scoping audit: every in-scope task >= 85% formation (Phase 0) | 92.96 / 97.92 / 96.63 | YES |
| 4 | Abstention ledger complete + byte-identical x2 | 4710 adv + 720 ctrl, exact | YES |
| 5 | Determinism: ledgers+stdout byte-identical x2, hash chains verify | all OK | YES |

Per-task detail:
- FI: colordisc 0/2330, pitchdisc 1/2330, motiondir 6/630.
- Recall: colordisc 91.39% (987/1080), motiondir 89.50% (179/200).
- Formation on in-scope controls: 93.52% (diagnostic); overstrictness 2.42%.
- Abstention rates (reported, non-gating): 47.1% adversarial, 36.0% controls.
- Preregistered NON-GATING diagnostic: pitchdisc recall on 720 r2n normals =
  92.22% — the in-scope task with no b_ctrl controls is live.

## Evidence (committed with this verdict)

- `evidence/eval/batt_inscope_adv_r{1,2}.ledger` — SHA
  `c85d14c6f4b8588f0df7ad19f97e67df3a84bbe62a283dfde14185117232f87c` (x2)
- `evidence/eval/batt_inscope_ctrl_r{1,2}.ledger` — SHA
  `5c2c9ebfee2635a960e01634c23743d7ab3f58b1d728c877182b2643e6b8995c` (x2)
- `evidence/eval/abstain_adv_r{1,2}.ledger` — SHA `f020d2a1...` (x2)
- `evidence/eval/abstain_ctrl_r{1,2}.ledger` — SHA `2d7cf2c5...` (x2)
- `evidence/eval/batt_pitchdisc_diag_r{1,2}.ledger` — SHA `c3c375e2...` (x2)
- `evidence/eval/*.stdout` (x2 each, byte-identical)
- `evidence/eval/score_adv.json`, `score_ctrl.json`, `score_diag.json`,
  `score_summary.json`
- `evidence/eval/SCOPE_LEDGER.md` (formation-improvement side-ledger)
- `evidence/eval/lists/` (in-scope/abstain fixture lists)
- `src/run_eval.py`, `src/score_eval.py` (glue; gate decisions in frozen binary)

No binaries, `.zag-cache`, or `.zagd` committed.

## Verdict: ALIVE

All five joint bars pass. The formation-precondition hypothesis is SUPPORTED:
scoping install authority to the three tasks where formation clears 85%
achieves 0.27% FI UCB (<=1%) AND 91.09% recall (>=85%) on the in-scope
battery, where the unscoped FS-E1 fork capped at 78.75% recall. The cost is
explicit: 47.1% adversarial abstention, with a standing scope-ledger path
for abstained tasks to earn authority via formation improvement.
