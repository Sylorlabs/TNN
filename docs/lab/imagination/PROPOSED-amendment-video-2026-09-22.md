# PROPOSED prereg amendment — explicit VIDEO/TEMPORAL imagination tests

Date: 2026-09-22. Status: **PROPOSED — NOT APPLIED. Requires Micah's
explicit approval.** (Frozen `PREREG.md` says any change to questions,
batteries, bars, metrics, or taste functions needs a dated amendment;
this is the dated proposal.)

## Governance gap it fixes

Micah's 2026-09-21 order explicitly lists video: "humans we can imagine
things like audio images video all in our heads". The frozen Q1 battery
covers 4 visual + 4 audio + 4 structural scenes — temporal/video
imagination is NOT tested. This amendment adds it without touching the
12 frozen Q1 scenes, the frozen taste functions, or any frozen bar.

## Proposed addition: Q1V — video/temporal probe (both modes, 12 questions)

Representation (fits the existing 10-word element + 8 attribute slots;
no mechanism change): a VIDEO scene is a sequence of up to 8 FRAMES;
each frame is one element with domain=4 (VIDEO), kind = shot type,
attributes:

| Mode | attrs |
|---|---|
| MACHINE | frame index, x, y (centroid of the moving subject 0..1000), r, g, b (dominant color), motion dx, dy (per-frame displacement) |
| HUMAN | frame index, zone 0..8, color handle, motion-direction handle (6000–6008), motion-speed handle (6100–6102), shape tuple |

Queries (answered from the partition only): `query_trajectory`
(direction code of the subject across frames), `query_speed_change`
(frame index of largest speed change), `query_reentry` (does the
subject return to its start zone?), `query_midpoint` (subject
position/zone at the middle frame).

## Proposed scenes (4, one per temporal pattern)

- V1: ball rolls left→right at constant speed (3 frames).
- V2: bird flies up then down — arch trajectory (4 frames).
- V3: car accelerates — increasing displacement (3 frames).
- V4: pendulum — swings out and returns to start zone (4 frames).

Each: build frames → 2 questions about emergent temporal properties →
EDIT one frame → 1 question about the post-edit state. 12 questions per
mode, same format as Q1.

## Proposed bar

| Bar | Rule |
|---|---|
| IMAG-V | ≥ 9/12 per mode → temporal imagination works in that mode; < 9/12 → FAIL for that mode |

(Same 75% pass fraction as IMAG-1's 26/36.)

## What this amendment does NOT change

- The 12 frozen Q1 scenes, questions, and IMAG-1 bar: untouched.
- The frozen taste functions: untouched.
- Q2, Q3, Q4: untouched.
- Determinism rule: Q1V runs get the same 5-rep byte-identical treatment.

## Approval requested

Micah: approve / reject / modify. On approval, this file is renamed to
`PREREG-amendment-2026-09-22-video.md`, committed, and Q1V is built and
run under the same governance.
