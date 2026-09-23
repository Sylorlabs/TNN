# KB4 C2 — PRE-RESULT DEBATE RECORD (frozen before test execution)

Four position papers + four rebuttals, committed before any test fixture was
scored. Each camp's prediction and falsifier are on record; the post-result
debate will score them.

## Final predictions (post-rebuttal)

| Camp | F1 (bits ≤ 0.15) | F2 (P(C|Y=0) ≥ 0.70) | F3 (validity) | F4 (false-install ≥ 0.15) | C2 deploys? |
|---|---|---|---|---|---|
| C1 | FIRES (~0.03–0.09 bits) | does NOT fire (noise-driven error) | green | near/over the line | no |
| C2 | FIRES (~70%) | does NOT fire on non-vacuous aggregate (~60%; central estimate 0.50–0.65) | PASSES (~85%) | fires (moot) | no — product is the F2 answer + per-task map |
| J (rebuttal) | FIRES (concedes C2's numbers) | quiet on non-vacuous aggregate | may void one sense | — | no (deploy prediction withdrawn) |
| Red | FIRES (70–75%) | FIRES SPURIOUSLY (60–65%) via estimator-covariance | voids ≥1 sense on ≥1 task (70%) | fires (~60%) | no |

Net: C1, C2, and J (post-rebuttal) converge on F1-fires/F2-quiet/C2-does-not-deploy;
the red team dissents, predicting a spurious F2 firing that would execute a
permanent family retirement on a confounded statistic.

## What each camp concedes / holds (post-rebuttal)

- **C1:** demoted from theorem to hypothesis — the band arithmetic (δ/σ) is a
  fixture-distribution problem that bites the analytic measurer too; σ′ ≪ δ is
  now C1's own preregistered engineering gate (stated oracle + measured σ′).
  Retracts "F2 cleanly confirms noise-driven error" (F2 reads
  estimator-covariance under T). HOLDS the exhaustion thesis (DPI) and all four
  falsifiers, with a procedural tightening on falsifier #1 (in-band
  stratification before treating a C2 deploy as genuine).
- **C2:** concedes F2-as-bare-aggregate can't carry program-permanent
  consequences (J's governance point taken in full); concedes the noise-vs-
  systematic dichotomy may be false (deterministic chaotic estimator breaks
  both branches' prescriptions — no instrument detects that regime).
  HOLDS: C2 runs first; C1 owes its σ′ proof before resources move; A1 and A2
  frozen (A2 now amended with the red team's covariance-calibration control,
  per-cell CIs, minimum denominators).
- **J:** withdraws the "looser band" defense (conceded vacuous — a band loose
  enough for judgment-side channels is loose enough for the raw judgment).
  Withdraws the C2-deploy prediction; now predicts C2's own numbers (F1 fires,
  F2 quiet non-vacuous). HOLDS: no permanent retirement on F2's aggregate in
  its current form — strengthened conjunct (i): non-vacuous tasks only (A2),
  minimum denominators, CIs, covariance-calibration control, law validation
  before F3 voiding; conjuncts (ii) honest C3 must run and fail, (iii) F2 must
  replicate on an independent battery.
- **Red:** grants C2's A2 closes the vacuous-inflation path, but not the core
  §1b attack (smooth-estimator covariance on non-vacuous tasks reads high
  P(C|Y=0) by construction). Stand-down list: zero for five. Recommendation:
  run C2 as a measurement, not a tribunal.

## Governance note (coordinator's ruling)

The debaters' governance objections (J, C2-rebuttal, red) are recorded and
serious — but the kill bars are Micah's frozen law, and this run executes
them as written in PREREG_FROZEN_TCP.md §6–§8. What the debate legitimately
changed pre-run: the A2 vacuous-cell interpretive rule (frozen in the prereg
before test scoring). What it did not change: the bars themselves. If F2
fires cleanly, the retirement verdict is recorded per §6/§7 with the full
confound evidence attached (both F2 aggregates, vacuity map, per-task rows,
and the prescribed covariance-calibration control as a follow-up test) —
the verdict names the outcome, the evidence shows its strength.

## Post-result debate (scheduled)

After scoring: the same four camps reconvene on measured data and record
whether their predictions survived. Mandatory questions: (1) did F1 fire;
(2) did F2 fire, and on which cells; (3) which vacuous cells, if any;
(4) does the covariance-calibration control change the F2 reading;
(5) the §7 branch taken and the follow-up (C3 / C1-scout / C1 scale-up)
launched.
