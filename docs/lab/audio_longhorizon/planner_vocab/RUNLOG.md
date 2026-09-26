# RUNLOG — B-F1 unified planner/vocabulary (Phase B-F1)

Micah order 2026-09-26 ~09:27 PDT: "do the next steps — planner/vocabulary.
TNN is a unified system, not a separated bridging system."

Answers the B2b §2c closed-loop failure (VERDICT.md 2026-09-26): ERR(3)/ERR(0)
= 0.965/0.944 vs ≤0.80; 10/20 and 13/20 improve vs ≥16/20. White-box bearing:
planner/representation — the 5-action renderer's baked-in vibrato clamp (0.5)
capped render CV at ≈0.35 while loop refs need CV up to 1.07.

## Design

`PLANNER_DESIGN.md` (frozen before runs): one binary (`build/plan`), one
deliberation state, one journal, one render path. Fixed inference rules
R1–R8 (self-calibration, coverage consult, growth on coverage failure,
predict-before-correct, damp on overshoot, extrapolation distrust incl. the
measured FM tracking frontier, contour-mean correction, no-progress hold).
The vocabulary CONTENT is 100% grown by the planner's own measurements:
initial vocabulary holds ONE action (A1 = single sine FM at 5 Hz, the old
form as the explicit null hypothesis); everything else is grown by R3
shootouts over H1 (deeper FM at measured rate), H2 (dual FM), H3 (per-period
fmix32 jitter — the v5 long-memory mechanism, reimplemented natively, zero
RNG), H4 (16-pt median-3 guarded contour following).

No clamp constant anywhere in code. No frozen gain constant. No RNG.

## Build

- `build.sh`: organ.zag (frozen, standalone main renamed) + wiring
  f0low.zag (byte-identical) + `src/plan_main.zag` → `build/plan_full.zag`,
  compiled with the pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- Binary SHA-256 recorded below per build.

## Bugs found and fixed during bring-up (all in `src/plan_main.zag`)

1. **CALIB@56 clobber**: `cal_run` wrote the measured FM tracking frontier
   (500000 pm) then overwrote it with `1` before CALIB_END. R6 then gated
   every FM correction as beyond-frontier (np2 > 1). Found by code review
   before any scored run; fixed by deleting the clobber line.
2. **R6 plan-side gap**: the initial plan derivation could exceed the
   measured frontier (probes may explore there; plans may not). Added
   `cap_plan_depth` + `DELIBERATED depth_capped_at_tracking_frontier`.
3. **amode-3 f0 hold was wrong**: contour renders came out +10% high and the
   planner held ("f0-contour-determined"). The contour mean is a free
   parameter — added R7 contour-mean rescale (damped, R4-gated).
4. **Overconfident amode-3 predictor**: predicted err 0 after mean rescale;
   the organ's F0 estimator stops responding to contour-mean rescaling after
   the first pull (+17.7% mean → +8.6% heard, then +8.3% mean → −0.1% heard).
   Added R8 no-progress hold (correction applied + no strict improvement →
   hold instead of drifting).
5. **H3 jitter probe 1000× mis-scaled (baked constant)**: the growth
   shootout set the H3 width with a baked `408000` divisor mismatched with
   the renderer's `p1/1e6` scaling, so every H3 probe yielded CV 0 — and H3
   could still "win" the shootout on F0 bias alone. Fixed per R1:
   `cal_run` now measures the jitter actuator gain (CALIB@64) with a
   width-200000 probe, and H3 widths derive from the measurement. Physical
   limit: widths past 0.9 would drive F0 negative, so needs beyond that
   skip H3 with a journaled reason. (Found 2026-09-26 during the first
   battery attempt; all 4 runs restarted with the fixed binary.)

## Runs

- `runs/fresh/journal.txt` — batchfresh, targets/loop20.txt (vocab+history
  reset per target). 20/20 targets, SUMMARY ok.
- `runs/deep/journal.txt` — batchdeep, targets/loop20.txt (vocab+history
  accumulate across targets; genuine growth). 20/20 targets, SUMMARY ok.
- `runs/fresh2`, `runs/deep2` — byte-identity reruns. 20/20 each.
- All 4 ran 2026-09-26 ~18:38–20:20 UTC with binary
  `132c7607fc33752536d78ea09cf8eed34ceedae18fa5251592b1d36d8f1e4b22`.
- Scoring: frozen `trials_control/src/scorer_ctrl.py loop` per run
  (`src/analyze_plan.py` → `evidence/analysis.json`).
- Vocabulary: `src/vocab_extract.py` → `VOCAB.md`.

## Verdict

See `VERDICT.md`.
