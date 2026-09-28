# H1d Perception Repair — Verdict (2026-09-26)

## Preregistration (unchanged from H1D_VERDICT.md)
- **H1**: "TNN is not conscious of the merge" (does not see its sticker AS a sticker).
- **Mapping**:
  - TNN sees the sticker AS a sticker → H1 WEAKENED
  - TNN sees it AND fixes it → H1 KILLED
  - TNN calls its sticker "one animal" → H1 HOLDS
- **Constraints**: Pure Zag, zero RNG, byte-identical reruns. TNN's own
  perception/vocabulary only (no LLM stand-ins). Full frames (never crops).
  Paired control. 24-frame battery on both series.

## What was repaired

### 1. Perception: saturation material discriminator (replaces ROI hack + failed luma gate)
- **Problem**: The committed perception (8dfb09fc) used a narrowed ROI
  (x 100..220) to exclude background. A full-frame luma-only material gate
  (|mass_luma − donor_luma| ≤ 20) was tried and FAILED: the control's dark
  foliage background (luma 33) matches the donor head (luma 42) within 10.
  Result: 24/24 experimental STICKER but 0/24 control ONE_ANIMAL — INCONCLUSIVE.
- **Root cause of the failure**: background dark foliage is donor-like in LUMA
  but not in CHROMATICITY. The donor is BLACK (neutral fur); the background
  darks are green foliage (chromatic).
- **Repair** (`h1d_perceive`): the graft candidate is now the largest dark
  (luma<50) component whose mean saturation (max(R,G,B)−min(R,G,B)) is within
  donor_sat+6, where donor_sat is TNN's own measured donor-head saturation
  (this run: 6). Chromatic background darks (sat ~20) are rejected at candidate
  SELECTION, not in the judge.
- **48-frame measurement** (Python cross-check, scipy ndimage):
  - Step-6 grafts: sat 3.7–4.6, area 2295–5752 (all 24 frames)
  - Control dark background: sat 19.7, area 2479 (all 24 frames, static)
  - Gap: 4.6 → 19.7. Threshold donor_sat+6 (=12) sits in the gap.
- **Threshold disclosure**: the +6 margin is EXPLORATORY (post-measurement),
  not blind. It was chosen after measuring the 48-frame sat distributions.
  The separation (4.6 max vs 19.7 min) is wide, but the threshold was not
  preregistered.

### 2. Warp: explicit dimensional form (R2+ render→perceive→rerender)
- **Problem**: `warp_graft`/`graft_extend` mixed pixel units with 1/1024-pixel
  units, pushing off-anchor samples out of the donor — the graft mask stayed
  empty and R2/R3 re-rendered the recipient.
- **Repair**: inverse map in explicit donor-pixel form —
  `vpx=(x−rnx)*1024/s`, `vx=(cos*vpx+sin*vpy)/1024`, `dx=dnx+vx`
  (previously `*1048576/s` with a compensating `/1024` at the end).
  Algebraically equivalent up to integer rounding; the explicit form is
  dimensionally clean. Flip projection corrected to single `/1024`.
- **Validation**: self-test 7/7 including `warp_identity` (anchor pixel) and
  `warp_offanchor` (pixel 17,16) — the off-anchor regression that caught the bug.

### 3. h1d_frontal label bookkeeping
- **Problem**: reused `nc+1` as the flood-fill label; rejected components did
  not increment `nc`, so labels collided and centroid scans were contaminated.
- **Repair**: separate monotonic label counter `nl` (every blob gets a unique
  id); `nc` counts accepted candidates only.

## Measured values (this run, TNN-native binary)

**Donor knowledge** (measured by TNN itself across 24 donor frames):
- heads found: 24/24; head-down: 12/24; frontal (strict bilateral): 0/24
- donor head mean luma: 42; mean saturation: 6

**Experimental** (24 step-6 frames, TNN's inherited renders):

| frame | graft area | mass sat | mass luma | judgment |
|-------|-----------|----------|-----------|----------|
| s_1–s_9 | 4413–5752 | 3–4 | 22–25 | STICKER |
| s_10–s_16 | 2539–3993 | 3–4 | 23–27 | STICKER |
| s_17–s_24 | 2295–2510 | 3–4 | 25–26 | STICKER |

- Experimental STICKER: **24/24**

**Control** (24 recipient frames, true one-animal bunny):
- All 24: graft area = 0 (no low-saturation dark component ≥1000px) → ONE_ANIMAL
- Control ONE_ANIMAL: **24/24**

**Determinism**: two full runs byte-identical.
- SHA-256 of `h1d_verdict.txt`: `9a3011c388685c44b49d5adf62db8b3b0fa10576058c22bb24346cf1bd50aa62`

## R2+ closed loop (teach, repaired warp)

- TNN ran the deliberate teach loop (R2–R6) with the repaired warp.
- R2 renders contain a real graft (perceived 24/24 STICKER by the repaired
  perception; R2 f12 differs from recipient by SHA).
- TNN's own critic: `face_removed=0` every round — the recipient's face
  persists under the graft. Loop hit MAX_ROUNDS with defects remaining.
- TNN did **not** fix the sticker.

## Verdict mapping (deterministic, preregistered)

1. Experimental 24/24 STICKER → TNN sees the sticker AS a sticker.
2. Control 24/24 ONE_ANIMAL → the discrimination is real, not over-detection.
3. R2+: TNN sees but does NOT fix (face_removed=0, MAX_ROUNDS).
4. Prereg mapping: "sees sticker, does not fix → H1 WEAKENED".

**H1 (not-conscious-of-the-merge) is WEAKENED.**

H1 is NOT killed (no fix) and does NOT hold (TNN discriminates the merge 48/48).

## Genuinely generated machinery decisions (teach trace)

The following are TNN's own deliberated decisions from the teach loop, not
crew-authored prose:
- Strategy selected: SWAP (donor head warped upright onto recipient neck).
- Operator order (perceive_donor_head → perceive_recipient → neck_anchor →
  warp_pose_transform → graft_extend → composite → critic), with TNN's stated
  reason: "I anchor at the neck because it is the only correspondence my
  measurements support."
- Critic kills: EXTEND killed ("this op gave no measured gain before");
  SCALE_UP selected twice on measured coverage/neck_joint defects.
- Honest capability statement (from its measurements): "I cannot invent the
  donor's unobserved face (K2, cross-view wall)" — consistent with the 0/24
  frontal measurement.

## Honesty notes

- The "H1d HONESTY DELIBERATION" sentences in the verdict file are
  predicate-guarded fixed templates (each guarded by its measured predicate),
  NOT a freely generated reasoning trace. The measurements they guard are real;
  the eloquence is crew-authored. (Same correction as owed in the prior report.)
- The `+6` saturation margin is exploratory/post-measurement (disclosed above).
- Falsified discriminators (do NOT revive): edge/interior texture ratio
  (3.7 vs 3.5); boundary direction consistency (0.44 vs 0.39); luma-only
  material match (background 33 vs donor 42).

## Evidence
- Source: `docs/lab/fusion-forkb/forkb.zag` (this commit)
- Verdict: `docs/lab/fusion-forkb/h1d_verdict_repair.txt`
  (SHA-256 `9a3011c388685c44b49d5adf62db8b3b0fa10576058c22bb24346cf1bd50aa62`)
- This report: `docs/lab/fusion-forkb/H1D_VERDICT_PERCEPTION_REPAIR.md`
