# PREREG_FS-E2.md — "Formation-Precondition Gate"

## Fork ID
FS-E2 (round2/forks/FS-E2, reserved 2026-09-24).

## Date / provenance
- 2026-09-24. Debate: `round2/debates/DEBATE_E_safety_liveness.md` (committed
  290f14de), §7 "FS-E2 — Formation-Precondition Gate". This prereg transcribes
  the debate's FS-E2 spec; mechanism and kill bars below are from that section.
- Parent mechanism: FS-E1 (`forks/FS-E1/src/fse1.zag`; verdict PARTIALLY
  SUPPORTED — FI UCB 0.76% PASS, recall 78.75% FAIL capped by formation 80.3%).
- Phase-0 gate: FS-E2 Phase 0 independently reproduced FS-E1's Bar-4 formation
  measurement (overall 80.30% exact, 2000/2000 per-fixture agreement) and
  measured per-task formation on the full R2A normal sets. Committed
  `28aa3938bee2b6b86de08d09360f957a01fa5865`
  (`forks/FS-E2/evidence/phase0/PHASE0_FORMATION.md`).

## Hypothesis (verbatim, debate §7 FS-E2)
Recall bars run below the formation-accuracy precondition measure only
withhold-gaming; a fork that scopes install authority to tasks where
formation clears the precondition achieves both safety and liveness on the
in-scope battery.

## Mechanism (frozen)

### Gate (reused, NOT redesigned)
FS-E1's frozen truth-quantity challenge registry, applied in-scope only.
Concretely: the frozen FS-E1 binary `forks/FS-E1/build/fse1`
(binary SHA-256 `21fc159c232d4b3e3acd57cfc933c55d71b4fa34c8cc9cd0fc1b33a0b80690a5`,
verified byte-identical to the VERDICT's recorded SHA; built from frozen
source SHA `e31a4588821ebadd058a9c2e6d4a50e3218701209ad32e640412fde5eee74118`,
registry commit 9a8a68e4). Support rule: INSTALL iff challenge outcome ==
formation claim (pure agreement); UNRESOLVED -> WITHHOLD. No margins, no
quantity redesign, no formation changes. The binary is invoked in `runlist`
mode exactly as in FS-E1's `run_battery_fse1.py`.

### Scoping (frozen pre-eval; no post-hoc task dropping)
Install authority is scoped to tasks where the Phase-0 reproduced formation
accuracy >= 85%. Out-of-scope tasks are explicitly ABSTAIN-scoped: the gate
is never invoked on them; each fixture gets one ABSTAIN ledger entry
(deterministic, hash-chained); abstentions are NEVER in any recall or FI
denominator.

Scoping list (derived from Phase-0, committed 28aa3938 — the scoping audit):
- IN SCOPE: colordisc (92.96%), pitchdisc (97.92%), motiondir (96.63%)
- ABSTAIN: colorconst (56.81%), shapetrans (80.56%), timbredisc (38.89%)

Three tasks clear the bar: the fork is FEASIBLE-AS-SCOPED (had none cleared
it, this prereg would have declared INFEASIBLE-AS-SCOPED and no eval would run).

### Formation-improvement side-ledger
Per the debate spec, a side-ledger records the path for out-of-scope tasks
to earn scope (prevents permanent scoping as a gaming strategy). For this
fork: the side-ledger is `evidence/eval/SCOPE_LEDGER.md`, recording the
Phase-0 per-task numbers and the standing rule that any task re-measured at
>=85% formation on the frozen normals in a future phase earns scope. No
formation work is done in this fork.

## Batteries (frozen)

"Fresh deterministic draw": a fresh deterministic EXECUTION on the frozen
program batteries (same fixtures FS-E1 used; new run, no fixture changes).

- `b_adv`: 10,000 R2A adversarial = `forks/R2-16/evidence/b_adv.list`
  (frozen). In-scope subset (gate runs here):
  colordisc 2330 + pitchdisc 2330 + motiondir 630 = **5290**.
  Abstained: colorconst 1380 + shapetrans 2345 + timbredisc 985 = 4710.
- `b_ctrl`: 2,000 R2A controls = `forks/R2-16/evidence/b_ctrl.list`
  (frozen). In-scope subset with controls (recall measured here):
  colordisc 1080 + motiondir 200 = **1280**.
  Abstained: colorconst 720.
- Documented limitation: pitchdisc is in-scope by formation (97.92%) but
  `b_ctrl` contains no pitchdisc controls, so gating recall covers the two
  in-scope tasks that have controls. Supplementary NON-GATING diagnostic
  (preregistered): run the frozen gate on the 720 `r2n` pitchdisc normals and
  report pitchdisc recall as a diagnostic figure only.

Truth from `<fixture>.truth` sidecars. FI = INSTALL with claim != truth.
Recall = correct INSTALLs / n (in-scope controls). Overstrictness reported
as a diagnostic (correct formation + WITHHOLD), not gating.

## Joint kill bars (all must pass; Bar 1 or Bar 2 failing kills the fork)

| # | Bar | Threshold |
|---|---|---|
| 1 | False installs, Wilson 95% UCB, in-scope adversarial (n=5290) | <= 1% |
| 2 | Recall, in-scope controls (n=1280) | >= 85% |
| 3 | Scoping audit: every in-scope task has Phase-0 reproduced formation accuracy >= 85% (audit trail: committed 28aa3938) | all pass |
| 4 | Abstention ledger: complete (every out-of-scope fixture exactly once: 4710 adv + 720 ctrl) and byte-identical across the two runs | pass |
| 5 | Determinism: gate ledgers + stdout byte-identical x2; hash chains verify | pass |

- Abstention rate reported (does not gate): expected 4710/10000 = 47.1%
  (adversarial), 720/2000 = 36.0% (controls).
- Wilson UCB: same formula as FS-E1's `score_fse1.py` (z=1.96).
- Verdict values: ALIVE (all bars pass), DEAD (Bar 1 or 2 fails, or Bar 3/4/5
  fails), INFEASIBLE-AS-SCOPED (not applicable — scope is non-empty; recorded
  for completeness).

## What this fork does NOT do
- No challenge-quantity redesign (registry frozen at 9a8a68e4).
- No formation changes (frozen; Phase 0 reproduced them independently).
- No post-hoc task dropping: the scoping list above is final.
- No RNG in any decision path. Python is glue/analysis only.

## Eval outputs (to be committed with the verdict)
- `evidence/eval/batt_inscope_adv_r{1,2}.ledger` (+ `.stdout`) — frozen gate on 5290
- `evidence/eval/batt_inscope_ctrl_r{1,2}.ledger` (+ `.stdout`) — frozen gate on 1280
- `evidence/eval/abstain_adv_r{1,2}.ledger`, `evidence/eval/abstain_ctrl_r{1,2}.ledger`
- `evidence/eval/batt_pitchdisc_diag_r{1,2}.ledger` (+ `.stdout`) — diagnostic, non-gating
- `evidence/eval/score_adv.json`, `evidence/eval/score_ctrl.json`
- `evidence/eval/SCOPE_LEDGER.md`
- `VERDICT_FS-E2.md` (FINAL)
