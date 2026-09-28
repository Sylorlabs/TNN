#!/usr/bin/env python3
"""verify_q1v.py — INDEPENDENT verifier for the Q1V video/temporal battery.

Hand-written from the Q1V design spec (PREREG-amendment-2026-09-22-video.md
+ the Q1V section header in src/imagine.zag), NOT from running imagine_bin.
Reimplements the scene data, the four temporal queries, and the edits in
Python, then checks the binary's Q1V output lines against them.

Usage: python3 verify_q1v.py <binary-output.txt>
Exit 0 iff every line matches (12/12 per mode).
"""

import sys

# Direction codes
STILL, N, NE, E, SE, S, SW, W, NW = 6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008
SLOW, MEDIUM, FAST = 6100, 6101, 6102

# Element: machine = (frame, x, y, r, g, b, dx, dy)
#          human   = (frame, zone, color, dir, speed, corners, curve, sym)

SCENES = {
    # V1: ball rolls L->R constant speed, 3 frames
    (0, 1): [
        (0, 100, 500, 255, 0, 0, 0, 0),
        (1, 500, 500, 255, 0, 0, 400, 0),
        (2, 900, 500, 255, 0, 0, 400, 0),
    ],
    (1, 1): [
        (0, 3, 1003, 6000, SLOW, 3000, 3100, 3200),
        (1, 4, 1003, E, MEDIUM, 3000, 3100, 3200),
        (2, 5, 1003, E, MEDIUM, 3000, 3100, 3200),
    ],
    # V2: bird arch up/down, 4 frames
    (0, 2): [
        (0, 200, 800, 110, 70, 40, 0, 0),
        (1, 400, 450, 110, 70, 40, 200, -350),
        (2, 600, 450, 110, 70, 40, 200, 0),
        (3, 800, 800, 110, 70, 40, 200, 350),
    ],
    (1, 2): [
        (0, 6, 1012, 6000, SLOW, 3003, 3100, 3200),
        (1, 4, 1012, NE, FAST, 3003, 3100, 3200),
        (2, 4, 1012, E, MEDIUM, 3003, 3100, 3200),
        (3, 8, 1012, SE, FAST, 3003, 3100, 3200),
    ],
    # V3: car accelerates, 3 frames
    (0, 3): [
        (0, 100, 500, 20, 60, 160, 0, 0),
        (1, 300, 500, 20, 60, 160, 200, 0),
        (2, 800, 500, 20, 60, 160, 500, 0),
    ],
    (1, 3): [
        (0, 3, 1059, 6000, SLOW, 3002, 3101, 3201),
        (1, 3, 1059, E, SLOW, 3002, 3101, 3201),
        (2, 5, 1059, E, FAST, 3002, 3101, 3201),
    ],
    # V4: pendulum out and back, 4 frames
    (0, 4): [
        (0, 500, 500, 200, 200, 200, 0, 0),
        (1, 750, 500, 200, 200, 200, 250, 0),
        (2, 750, 500, 200, 200, 200, 0, 0),
        (3, 500, 500, 200, 200, 200, -250, 0),
    ],
    (1, 4): [
        (0, 4, 2003, 6000, SLOW, 3001, 3101, 3202),
        (1, 5, 2003, E, FAST, 3001, 3101, 3202),
        (2, 5, 2003, 6000, SLOW, 3001, 3101, 3202),
        (3, 4, 2003, W, FAST, 3001, 3101, 3202),
    ],
}

# (mode, scene): (q1-op, q2-op, edit, q3-op)
# ops: "traj", "spd", "reentry", "mid"
# edits: ("mv", frame, nx, ny) machine / ("attr", frame, slot, val) human
#   human slots: zone=1, color=2, dir=3, speed=4 (0-based within tuple)
PLAN = {
    (0, 1): ("traj", "spd", ("mv", 2, 900, 200), "traj"),
    (1, 1): ("traj", "spd", ("attr", 2, 1, 2), "traj"),
    (0, 2): ("reentry", "mid", ("mv", 3, 200, 800), "reentry"),
    (1, 2): ("reentry", "mid", ("attr", 3, 1, 6), "reentry"),
    (0, 3): ("spd", "traj", ("mv", 1, 600, 500), "spd"),
    (1, 3): ("spd", "traj", ("attr", 1, 4, FAST), "spd"),
    (0, 4): ("traj", "reentry", ("mv", 3, 750, 500), "reentry"),
    (1, 4): ("traj", "reentry", ("attr", 3, 1, 5), "reentry"),
}


def zcol(z):
    return z % 3


def zrow(z):
    return z // 3


def zone_of_xy(x, y):
    cx = min(x // 334, 2)
    cy = min(y // 334, 2)
    return cy * 3 + cx


def qv_dir(dx, dy, th):
    if abs(dx) <= th and abs(dy) <= th:
        return STILL
    cx = 1 if dx > 0 else (-1 if dx < 0 else 0)
    cy = 1 if dy > 0 else (-1 if dy < 0 else 0)
    if (cy, cx) == (-1, 0):
        return N
    if (cy, cx) == (-1, 1):
        return NE
    if (cy, cx) == (0, 1):
        return E
    if (cy, cx) == (1, 1):
        return SE
    if (cy, cx) == (1, 0):
        return S
    if (cy, cx) == (1, -1):
        return SW
    if (cy, cx) == (0, -1):
        return W
    return NW


def qv_trajectory(frames, mode):
    n = len(frames)
    if n < 2:
        return STILL
    if mode == 1:
        z0, zl = frames[0][1], frames[-1][1]
        return qv_dir(zcol(zl) - zcol(z0), zrow(zl) - zrow(z0), 0)
    dx = frames[-1][1] - frames[0][1]
    dy = frames[-1][2] - frames[0][2]
    return qv_dir(dx, dy, 10)


def qv_speed(f, mode):
    if mode == 1:
        h = f[4]
        return 2 if h == FAST else (1 if h == MEDIUM else 0)
    return abs(f[6]) + abs(f[7])


def qv_speedchange(frames, mode):
    n = len(frames)
    if n < 2:
        return -1
    bf, bc = 1, -1
    for k in range(n - 1):
        c = abs(qv_speed(frames[k + 1], mode) - qv_speed(frames[k], mode))
        if c > bc:
            bc, bf = c, k + 1
    return bf


def qv_zone(f, mode):
    if mode == 1:
        return f[1]
    return zone_of_xy(f[1], f[2])


def qv_reentry(frames, mode):
    if len(frames) < 2:
        return 0
    return 1 if qv_zone(frames[0], mode) == qv_zone(frames[-1], mode) else 0


def qv_midpoint(frames, mode):
    m = len(frames) // 2
    return frames[m][1]


OPS = {"traj": qv_trajectory, "spd": qv_speedchange,
       "reentry": qv_reentry, "mid": qv_midpoint}


def apply_edit(frames, mode, edit):
    frames = [list(f) for f in frames]
    if edit[0] == "mv":
        _, f, nx, ny = edit
        frames[f][1], frames[f][2] = nx, ny
        if f > 0:
            frames[f][6] = nx - frames[f - 1][1]
            frames[f][7] = ny - frames[f - 1][2]
        else:
            frames[f][6] = frames[f][7] = 0
        if f + 1 < len(frames):
            frames[f + 1][6] = frames[f + 1][1] - nx
            frames[f + 1][7] = frames[f + 1][2] - ny
    else:
        _, f, slot, val = edit
        frames[f][slot] = val
    return [tuple(f) for f in frames]


def expected():
    out = {}
    for (mode, scene), (q1, q2, edit, q3) in PLAN.items():
        frames = list(SCENES[(mode, scene)])
        out[(mode, scene, 1)] = OPS[q1](frames, mode)
        out[(mode, scene, 2)] = OPS[q2](frames, mode)
        frames = apply_edit(frames, mode, edit)
        out[(mode, scene, 3)] = OPS[q3](frames, mode)
    return out


def main():
    exp = expected()
    lines = open(sys.argv[1]).read().splitlines()
    got = {}
    fmode = None
    for ln in lines:
        p = ln.split()
        if len(p) == 5 and p[0] == "Q1V":
            fmode = int(p[1])
            got[(int(p[1]), int(p[2]), int(p[3]))] = int(p[4])
    # only score the mode(s) present in this file
    exp = {k: v for k, v in exp.items() if fmode is None or k[0] == fmode}
    fails = 0
    for key, want in sorted(exp.items()):
        have = got.get(key, None)
        ok = have == want
        if not ok:
            fails += 1
            print(f"MISMATCH mode={key[0]} scene={key[1]} qid={key[2]}: "
                  f"expected {want}, binary {have}")
    per_mode = {}
    for (mode, scene, qid), want in exp.items():
        per_mode.setdefault(mode, [0, 0])
        per_mode[mode][1] += 1
        if got.get((mode, scene, qid)) == want:
            per_mode[mode][0] += 1
    for mode in sorted(per_mode):
        c, t = per_mode[mode]
        print(f"mode={mode}: {c}/{t} "
              f"({'PASS' if c >= 9 else 'FAIL'} vs IMAG-V bar 9/12)")
    if fails:
        print(f"TOTAL MISMATCHES: {fails}")
        sys.exit(1)
    print("ALL MATCH — verifier agrees 12/12 per mode.")


if __name__ == "__main__":
    main()
