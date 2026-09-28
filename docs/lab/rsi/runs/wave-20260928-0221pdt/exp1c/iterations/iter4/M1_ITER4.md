# EXP1c Iteration 4: Pre-run / Milestone 1 Freeze

Wave: wave-20260928-0221pdt. EXP1c attempt 4. Written before any
attempt-4 run or calibration data has been generated.

## Prereg unchanged

The frozen prereg remains commit `8b456736b`; the frozen addendum
remains commit `d9e96ad913052921d712a843440f8948334191b6`. Neither is
reopened. Iteration 4 changes only the retuned variant family and the
third calibrator, as the prereg's retune procedure authorizes.

## Frozen inputs

- Run-start HEAD: `43f339e60dad44bf5ceccef83962248b7a434256` (checked
  2026-09-28).
- Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`, SHA-256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
  verified 2026-09-28.
- World blob: `fff8af2493bc6dbe9de6fc76f9a6206d887d586a`. The
  iteration-4 implementation uses the REAL frozen world API
  (apos, W_NCELLS, w_step, w_storm_active, w_storm_within, w_in_zone,
  w_sheltered, w_reflex_storm, w_reflex_emergency); there is no world
  reimplementation.

## Retune iteration 4 family

12 fresh world variants (`x1c4_variants.zag`), same-side family:
every mote, crystal, start, and home on the same side of the void
pair; vel=0 with lo<hi and tight drift ranges per the stationarity
binding; void pairs cycle (10,11), (4,5), (16,17); home outside the
storm zone [6,17] so the taught ward strategy can shelter; motes
cluster near home and start to give blind enumeration a fair survival
chance. Four crystals, three storms in thirds of the 1200-tick
horizon. The 12th variant differs only in its numbers.

## Frozen K6 operationalization (bound by the 2026-09-28 judge ruling)

The ablation retains all 399 sketches, all scoring, all selection,
all plan lengths, and the same enumeration machinery. On the ablation
arm only, executed COMBINE primitives are excluded from plan
selection (`no_combine` skips COMBINE-containing sketches in
`xi_pick`). This is the frozen attempt-4 K6 intervention. The
exploration-risk confound identified by the 2321pdt judge is recorded
in the evidence note; the ablation arm is a measurement from the run,
never evidence about invention.

## C3: distinctness qualifier struck (binding 2321pdt fix)

The third calibrator is f2, an open-loop patrol oscillating on
[home-2, home+2], eating only active motes on its cell, storming home,
energy-gated. It uses no target seeking, unlike f0 (nearest-mote
forage) and f1 (stormflee then forage). Per the 2026-09-28 judge
ruling, the iteration-3 "qualitatively distinct" gloss is struck as
unsupported by measurement: f2 vector diffs were e_end-only, dXY >= 1
is a hair trigger, and the calibrators sit at the 1200 ceiling and
discriminate nothing about survival. The in-Zag per-variant
(ticks, e_end) vector comparison is kept as a reported measurement,
not as a distinctness certification. Code-level strategy differences
are documented from source reading only. C3 is evaluated on the
measurable gate: three scripted strategies each with median >= 720.

## What is frozen here

- Sources: `x1c4_out.zag`, `x1c4_params.zag`, `x1c4_variants.zag`,
  `x1c4_agents.zag`, `x1c4_emit.zag`, `x1c4_check.zag`,
  `x1c4_calib.zag`, `x1c4_run.zag`, `x1c4_evidence.zag`.
- The evidence generator is frozen in milestone 1, before any run
  data is visible. Any later edit to it requires a new freeze and a
  complete rerun.
- M3 is verbatim: mean experienced delta-energy + B0/(1+n), integer
  division, strict-greater argmax, B0 schedule 40/120, no extra
  bonuses. M4 contains exactly the three frozen reflexes, with H9 as
  the final gate. P-arm 25-tick anticipation is taught text, not an
  added reflex.

## What has not happened yet

No attempt-4 run or calibration data has been generated. The record
states explicitly what the old instrument emitted: nothing. All
prior attempt-4 sources listed here are new files; nothing from
attempts 1-3 was modified. Past VOID attempts remain uncertified
history.

## Sequence after this freeze

1. Commit milestone 1 (sources plus this note) before running
   calibration or the experiment.
2. Run mode check, calibration twice, variant emitter, full
   experiment twice.
3. Verify byte-identical SHA-256 outputs.
4. Run the frozen Zag evidence generator; commit milestone 2 data,
   then milestone 3 generated evidence note.
