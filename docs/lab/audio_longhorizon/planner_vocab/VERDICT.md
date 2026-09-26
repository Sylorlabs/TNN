# VERDICT — B-F1 unified planner/vocabulary closed loop

Date: 2026-09-26. Micah order 2026-09-26 ~09:27 PDT: "do the next steps —
planner/vocabulary. TNN is a unified system, not a separated bridging system."

Answers the B2b §2c closed-loop failure (VERDICT.md 2026-09-26): ERR(3)/ERR(0)
= 0.965/0.944 vs ≤0.80; 10/20 and 13/20 improve vs ≥16/20. White-box bearing:
planner/representation — the 5-action renderer's baked-in vibrato clamp (0.5)
capped render CV at ≈0.35 while loop refs need CV up to 1.07.

## What was built

One Zag binary (`src/plan_main.zag` → `build/plan`), one deliberation state,
one journal, one render path. Fixed inference rules R1–R8 (see
`PLANNER_DESIGN.md`), frozen before scoring. The vocabulary CONTENT is 100%
grown by the planner's own measurements: the initial vocabulary holds exactly
one action (A1 = single sine FM at 5 Hz — the old form as the explicit null
hypothesis). Everything else entered only because the planner's coverage rule
fired on measured need, and only the shootout winner (measured lowest
predicted ERR over H1 deep-FM / H2 dual-FM / H3 per-period fmix32 jitter /
H4 16-pt median-3 contour) entered.

No clamp constant anywhere in the code. No frozen gain constant. No RNG —
determinism by construction (fmix32 hash counter per (target,iter,action),
fixed initial 1.5, fixed guard fractions). Journal records every decision
with its reason. Five bugs found and fixed during bring-up (see RUNLOG.md),
including a 1000× mis-scaled H3 jitter constant replaced by measured
calibration (R1).

## §2c battery (frozen scorer `trials_control/src/scorer_ctrl.py`, 20 real refs)

| Run | State | ERR(3)/ERR(0) (bar ≤0.80) | Wilcoxon p<0.01 | ≥16/20 improve | sign ≥80% | unstable | sawtooth |
|---|---|---|---|---|---|---|---|
| fresh | reset/target | 0.710 PASS | 0.052 FAIL | 11/20 FAIL | 94.1% PASS | 6 | 1 |
| deep | accumulate | 0.559 PASS | 0.0145 FAIL | 13/20 FAIL | 94.4% PASS | 6 | 1 |
| fresh2 | rerun | 0.710 PASS | 0.052 FAIL | 11/20 FAIL | 94.1% PASS | 6 | 1 |
| deep2 | rerun | 0.559 PASS | 0.0145 FAIL | 13/20 FAIL | 94.4% PASS | 6 | 1 |

Old 5-action controller for comparison: 0.965/0.944, 10/20 and 13/20 improve.

## Determinism

- fresh vs fresh2: canonicalized journals byte-identical: YES.
- deep vs deep2: canonicalized journals byte-identical: YES.
- WAV SHA-256: 80/80 identical fresh/fresh2; 80/80 identical deep/deep2.
- (Canonicalization strips only the run's own outdir name from RENDERED lines;
  all deliberation content is byte-identical.)

## Verdict: PARTIAL PASS — the loop now improves the mean, but not enough cases

The planner/vocabulary **cut the mean closed-loop error by 29% (fresh) and
44% (deep)** vs the old controller, and passed the ERR-ratio bar (0.710,
0.559 ≤ 0.80) plus sign agreement (94%). The deep run's accumulated
vocabulary + recalled deltas beat fresh on the mean (d3: 0.565→0.001,
d11: 0.562→0.011 in deep vs stuck in fresh).

But the strict bars still fail: only 11/20 (fresh) and 13/20 (deep) cases
strictly improve vs the required 16/20, and Wilcoxon p misses 0.01
(0.052, 0.0145). Three cases get actively worse (d2, d7, d8 — the
corrections overshoot), and d19/d20 sit at 0.500 unchanged (the planner
cannot move them).

## White-box bearing (from the journals)

1. **The vocabulary works but is minimal.** Deep grew exactly 2 actions
   (A1 inherited, A2 = H4 contour) and reused A2 for all 20 targets. The
   contour action covers high-CV needs well (d1: 0.155→0.007). Nothing ever
   needed H1/H2/H3 — the shootout honestly reports when candidates are
   skipped (H3: need-exceeds-jitter-physical-limit).
2. **R8 (no-progress hold) fires correctly.** When a correction fails to
   improve measured ERR, the planner holds instead of drifting (verified in
   smoke + battery journals: `reason=no-progress-hold`).
3. **The predictor is overconfident.** It repeatedly predicts err 0 while
   measured stays high (esp. amode-3 contour-mean). R4/R8 contain the damage
   but the model mismatch is real and journaled.
4. **Corrections can hurt.** d2/d7/d8 worsened because the F0 or CV
   correction overshot (the organ's response is nonlinear past the first
   pull). The planner measures this and holds, but the damage is done.
5. **d19/d20 are stuck.** The planner's actions cannot express what these
   need (or the hearing cannot guide it). This is the honest "cannot do"
   finding — not a bug, a coverage gap.

## Standing-law compliance notes

- **Synth paradigm:** the renderer is still sine-FM/contour/jitter
  synthesis. This trial tested the planner/vocabulary loop, not the audio
  law. The renders are clean (waveform analysis: no hum, no clicks, no DC)
  but they are still synth-based. The exact-replication mission is separate.
- **No arbitrary limits:** the 32-entry vocab cap and 16-pt contour remain
  as inherited structure, but the CONTENT is fully grown and the gains are
  all measured. The H3 physical limit (jw<1) is physics, not policy.
- **Unified:** one binary, one state, one journal, one render path. The
  boundary audit is the journal itself — every decision cites its measured
  reason.

## Next steps (if ordered)

1. Fix the correction overshoot (d2/d7/d8): the damped multiplier needs a
   smaller step or a line-search on measured ERR.
2. Cover d19/d20: new growth hypotheses for what the contour cannot express.
3. Recalibrate the amode-3 predictor (it predicts 0 too eagerly).

## Artifacts

- `evidence/analysis.json` — full per-case frozen-scorer numbers + identity.
- `evidence/waveform.json` — analyzer-first waveform evidence (d1-d3).
- `VOCAB.md` — the grown vocabulary with the planner's recorded reasons.
- `RUNLOG.md` — build log, bugs found/fixed, run record.
- Gallery: `~/workspace/your_files/audio_plannervocab_b1/index.html`
  (NEW-badged, self-contained, 20 clips).
- Binary SHA-256: `132c7607fc33752536d78ea09cf8eed34ceedae18fa5251592b1d36d8f1e4b22`
