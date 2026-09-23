# Q1V — video/temporal imagination battery: RESULTS

Date: 2026-09-22 (~05:25 PDT). Governance: `PREREG-amendment-2026-09-22-video.md`
(APPLIED 2026-09-22; approved by Micah's standing test-authorization 2026-09-21 22:20
plus his explicit video-battery order). Bar: **IMAG-V ≥ 9/12 per mode → PASS**.

## Mechanism (pure Zag, zero RNG)

VIDEO = domain 4, kind 1. One element per frame, 8 attribute slots:

| Mode | attrs |
|---|---|
| MACHINE | frame index, x, y (centroid 0..1000), r, g, b (dominant color), dx, dy (per-frame displacement) |
| HUMAN | frame index, zone 0..8, color handle (1000–1071/2000–2004 vocab), motion-direction handle 6000–6008 (STILL,N,NE,E,SE,S,SW,W,NW), motion-speed handle 6100–6102 (SLOW,MEDIUM,FAST), shape tuple (corners/curve/symmetry) |

Queries, answered from the partition only:

| Query | Machine | Human |
|---|---|---|
| `query_trajectory` | net (dx,dy) of centroid first→last, threshold 10px | net (dcol,drow) of zones first→last |
| `query_speed_change` | largest \|spd(k+1)−spd(k)\|, spd=\|dx\|+\|dy\| | largest change in speed-handle rank (6100→0, 6101→1, 6102→2) |
| `query_reentry` | 1 iff last frame zone == first frame zone (zones from x,y) | 1 iff last frame zone == first frame zone |
| `query_midpoint` | x at frame n/2 | zone at frame n/2 |

Direction codes 6000–6008 shared: STILL/N/NE/E/SE/S/SW/W/NW. Speed-change
answer = the later frame index (k+1), tie → lowest k. Edits recompute the
stored dx,dy of the edited frame (from f−1) and its successor so the
partition stays displacement-consistent (deliberate, deterministic edit).

## Scenes

| Scene | Pattern | Frames | Pre-edit Qs | Edit | Post-edit Q |
|---|---|---|---|---|---|
| V1 | ball rolls L→R, constant speed | 3 | trajectory, speed_change | f2: (900,500)→(900,200) / zone 5→2 | trajectory |
| V2 | bird arch up-then-down | 4 | reentry, midpoint | f3: (800,800)→(200,800) / zone 8→6 | reentry |
| V3 | car accelerates (increasing displacement) | 3 | speed_change, trajectory | f1: x 300→600 / speed 6100→6102 | speed_change |
| V4 | pendulum swings out, returns to start zone | 4 | trajectory, reentry | f3: (500,500)→(750,500) / zone 4→5 | reentry |

## Answers (verifier-expected; binary matched 12/12 per mode)

Machine mode (0):

| Scene | Q1 | Q2 | Q3 (post-edit) |
|---|---|---|---|
| V1 | 6003 (E) | 1 | 6002 (NE) |
| V2 | 0 (no reentry) | 600 (x at mid frame) | 1 (reentry) |
| V3 | 2 (largest speed change at f2) | 6003 (E) | 1 (largest speed change now at f1) |
| V4 | 6000 (STILL — net displacement zero) | 1 (reentry) | 0 (no reentry) |

Human mode (1):

| Scene | Q1 | Q2 | Q3 (post-edit) |
|---|---|---|---|
| V1 | 6003 (E) | 1 | 6002 (NE) |
| V2 | 0 (no reentry) | 4 (zone at mid frame) | 1 (reentry) |
| V3 | 2 (largest speed change at f2) | 6003 (E) | 1 (largest speed change now at f1) |
| V4 | 6000 (STILL — net zone displacement zero) | 1 (reentry) | 0 (no reentry) |

Notable: both codecs agree on every emergent temporal property despite
disjoint vocabularies (raw x/y vs zones, dx/dy vs direction/speed handles).
V4 shows correct STILL net trajectory with positive reentry — direction and
return are distinct properties, both handled. The post-edit Q in V1/V3/V4
changed the answer; in V2 the answer changed 0→1. Every change lands where
the edit predicts.

## Determinism (5 reps per mode, byte-identical)

| File | SHA256 |
|---|---|
| logs/q1vm_rep1..5.txt | 55b26e0579528345ee218668557227d1fe6f3806f2566bd7b76c5fea6a221f40 (all 5 identical) |
| logs/q1vh_rep1..5.txt | 5bb4428240b6591662339150330275548c4a22c6277f7d4d5c84799b1190faa3 (all 5 identical) |

Independent verification: `verify_q1v.py` (hand-written from the spec, not
from the binary): **machine 12/12, human 12/12 on all 5 reps**.

## Verdict

| Mode | Score | IMAG-V (≥9/12) |
|---|---|---|
| MACHINE | 12/12 | **PASS** |
| HUMAN | 12/12 | **PASS** |

No build discrepancies: binary matched the verifier on every line of every
rep. Frozen Q1 scenes, taste functions, Q2/Q3/Q4, and IMAG-1 untouched.
