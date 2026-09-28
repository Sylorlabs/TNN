#!/usr/bin/env python3
"""Python reimplementation of B's FROZEN relation tables (percept.zag).

Used for fitting B's color/pitch/shape judgments from emitted percept
handles. Verified against the binary's own judgments at hand-tuned
values (verify_relations.py) BEFORE any fitting.
"""
# ---- COLOR (percept.zag: pc_color_dist) ----
def _c_is_chroma(h):
    return 1000 <= h < 1072

def _c_hue(h):
    return (h - 1000) // 6

def _c_light(h):
    return ((h - 1000) % 6) // 2

def _c_sat(h):
    return (h - 1000) % 2

def _c_ach_rank(h):
    i = h - 2000
    if i <= 1:
        return 0
    if i == 2:
        return 1
    return 2

def _c_lrank(h):
    return _c_light(h) if _c_is_chroma(h) else _c_ach_rank(h)

def _c_wheeldist(a, b):
    d = abs(a - b)
    return 12 - d if d > 6 else d

def pc_color_dist(a, b):
    if a == b:
        return 0
    ca, cb = _c_is_chroma(a), _c_is_chroma(b)
    if ca and cb:
        return (_c_wheeldist(_c_hue(a), _c_hue(b))
                + abs(_c_light(a) - _c_light(b))
                + abs(_c_sat(a) - _c_sat(b)))
    if not ca and not cb:
        return abs(a - b)
    return 4 + abs(_c_lrank(a) - _c_lrank(b))

# ---- SHAPE (percept.zag: prototypes + pc_shape_match) ----
CIRCLE, TRIANGLE, SQUARE = 0, 1, 2
PROTO = [(3000, 3100, 3200),   # CIRCLE
         (3001, 3101, 3202),   # TRIANGLE
         (3002, 3101, 3201)]   # SQUARE
CLS_NAME = {0: "CIRCLE", 1: "TRIANGLE", 2: "SQUARE"}
# priority orders, grid index 0 = hand order (C,T,S), then lexicographic
PRIO_ORDERS = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

def shape_match(tup, i):
    return sum(1 for a, b in zip(tup, PROTO[i]) if a == b)

def shape_decide_hand(tup):
    """Exact current-binary rule: argmax, ties -> earliest (C,T,S)."""
    return shape_decide(tup, 0, (0, 1, 2))

def shape_decide(tup, min_matches, prio):
    """Crew-defined vote family (see CALIBRATION.md)."""
    m = [shape_match(tup, i) for i in range(3)]
    qual = [i for i in range(3) if m[i] >= min_matches]
    if qual:
        best = max(m[i] for i in qual)
        for i in prio:
            if i in qual and m[i] == best:
                return i
    return prio[0]

# ---- PITCH (percept.zag: handles are 4000+bin) ----
def pitch_bin(h):
    return h - 4000

# ---- fitted judgment functions ----
def b_color_judgment(p1, p2, k):
    return "SAME" if pc_color_dist(p1, p2) <= k else "DIFFERENT"

def b_colorconst_judgment(p1, p2, k):
    return "SAME_SURFACE" if pc_color_dist(p1, p2) <= k else "DIFFERENT"

def b_pitch_judgment(p1, p2, k):
    d = abs(p1 - p2)
    if d <= k:
        return "SAME"
    return "HIGHER" if p2 > p1 else "LOWER"

def b_shape_judgment(tup, min_matches, prio):
    return CLS_NAME[shape_decide(tup, min_matches, prio)]

def b_timbre_judgment(crest, bright, form, tc, tb, tf):
    if crest <= tc:
        return "RICH"
    if bright >= tb:
        return "BRIGHT"
    if form >= tf:
        return "DARK"
    return "PURE"

MOTION_DIR = {6000: "STILL", 6001: "N", 6002: "NE", 6003: "E", 6004: "SE",
              6005: "S", 6006: "SW", 6007: "W", 6008: "NW"}

def b_motion_judgment(mcount, dir_handle, t):
    if mcount < t:
        return "STILL"
    return MOTION_DIR[dir_handle]

# ---- A fitted judgment functions (from debug_vec scores) ----
def a_octant(dx, dy):
    ax, ay = abs(dx), abs(dy)
    if ax >= 2 * ay:
        return "E" if dx > 0 else "W"
    if ay >= 2 * ax:
        return "S" if dy > 0 else "N"
    if dx > 0 and dy > 0:
        return "SE"
    if dx < 0 and dy > 0:
        return "SW"
    if dx > 0 and dy < 0:
        return "NE"
    return "NW"

def a_color_judgment(dist, t):
    return "SAME" if dist <= t else "DIFFERENT"

def a_colorconst_judgment(dist, t):
    return "SAME_SURFACE" if dist <= t else "DIFFERENT"

def a_pitch_judgment(dppm, fam, fbm, t):
    if dppm < t:
        return "SAME"
    return "HIGHER" if fbm > fam else "LOWER"

def a_timbre_judgment(r, b1, b2, b3):
    if r < b1:
        return "PURE"
    if r < b2:
        return "DARK"
    if r < b3:
        return "RICH"
    return "BRIGHT"

def a_motion_judgment(mag, dx, dy, t):
    if mag < t:
        return "STILL"
    return a_octant(dx, dy)
