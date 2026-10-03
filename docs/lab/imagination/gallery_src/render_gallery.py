#!/usr/bin/env python3
"""GALLERY crew renderer: TNN imagination-design trial scenes -> viewable PNGs.

Reads the frozen scene dumps and renders every Q2 design (briefs 1..6, both
modes) plus Q1 scenes 1 and 2 (both modes) as PNGs.

All interpretation choices are documented in RENDER-NOTES.md in this dir.
The scene data itself is NEVER altered: every interpretation step is a
gallery-layer mapping from handles/values to pixels.

Usage: python3 render_gallery.py <out_dir>
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

IMAG = os.path.expanduser("~/workspace/tnn-lab/imagination")

# ---------------------------------------------------------------- colors ---
HUE_BASE = {  # hue wheel base RGBs, from the frozen task table
    0: (200, 40, 40), 1: (210, 90, 30), 2: (220, 130, 30),
    3: (220, 170, 40), 4: (210, 200, 50), 5: (140, 180, 60),
    6: (60, 160, 70), 7: (50, 150, 140), 8: (60, 160, 200),
    9: (80, 130, 210), 10: (60, 80, 190), 11: (130, 70, 170),
}
HUE_NAME = ["RED", "RED_ORANGE", "ORANGE", "AMBER", "YELLOW", "YELLOW_GREEN",
            "GREEN", "TEAL", "CYAN", "SKY", "BLUE", "VIOLET"]
ACHRO = {2000: (10, 10, 10), 2001: (70, 70, 70), 2002: (140, 140, 140),
         2003: (200, 200, 200), 2004: (245, 245, 245)}
ACHRO_NAME = {2000: "BLACK", 2001: "DARK_GRAY", 2002: "GRAY",
              2003: "LIGHT_GRAY", 2004: "WHITE"}


def human_color(handle):
    """1000+hue*6+light*2+sat -> RGB. Returns (rgb, name)."""
    if handle in ACHRO:
        return ACHRO[handle], ACHRO_NAME[handle]
    rem = handle - 1000
    hue, rem = divmod(rem, 6)
    light, sat = divmod(rem, 2)
    r, g, b = HUE_BASE[hue]
    if light == 0:      # DARK x0.55
        r, g, b = r * 0.55, g * 0.55, b * 0.55
    elif light == 2:    # LIGHT: toward white 40%
        r, g, b = r + 0.4 * (255 - r), g + 0.4 * (255 - g), b + 0.4 * (255 - b)
    if sat == 0:        # MUTED: desaturate 50% toward gray
        gray = (r + g + b) / 3
        r, g, b = r + 0.5 * (gray - r), g + 0.5 * (gray - g), b + 0.5 * (gray - b)
    name = "%s %s %s" % (HUE_NAME[hue],
                         ["DARK", "MID", "LIGHT"][light],
                         ["MUTED", "SATURATED"][sat])
    return (int(round(r)), int(round(g)), int(round(b))), name


# ------------------------------------------------------------------ zones ---
ZONE_CENTER = {0: (167, 167), 1: (500, 167), 2: (833, 167),
               3: (167, 500), 4: (500, 500), 5: (833, 500),
               6: (167, 833), 7: (500, 833), 8: (833, 833)}
ZONE_NAME = {0: "TL", 1: "TC", 2: "TR", 3: "ML", 4: "C", 5: "MR",
             6: "BL", 7: "BC", 8: "BR"}


# ------------------------------------------------------------------ scenes --
def load_q2():
    """Parse logs/q2m.txt and logs/q2h.txt -> {(mode, brief): [elements]}."""
    scenes = {}
    for fname, mode in (("logs/q2m.txt", 0), ("logs/q2h.txt", 1)):
        with open(os.path.join(IMAG, fname)) as f:
            key = None
            for line in f:
                p = line.split()
                if not p:
                    continue
                if p[0] == "Q2":
                    key = (int(p[1]), int(p[2]))
                    scenes[key] = []
                elif p[0] == "E":
                    scenes[key].append({
                        "elidx": int(p[3]), "domain": int(p[4]),
                        "kind": int(p[5]),
                        "a": [int(x) for x in p[6:14]],
                    })
    return scenes


# Q1 scene construction, transcribed from src/imagine.zag (ig_q1_sc1/ig_q1_sc2).
# These are the scenes AS IMAGINED (initial placement, before the mid-question
# attribute mutations performed by the Q1 battery itself; see RENDER-NOTES).
def q1_scene(scene, mode):
    """Return list of element dicts for Q1 scene (1|2) and mode (0|1)."""
    if scene == 1 and mode == 0:
        return [
            {"elidx": 0, "domain": 1, "kind": 3,
             "a": [832, 125, 80, 80, 200, 60, 30, 0]},
            {"elidx": 1, "domain": 1, "kind": 2,
             "a": [499, 375, 100, 100, 60, 130, 200, 0]},
            {"elidx": 2, "domain": 1, "kind": 4,
             "a": [832, 875, 200, 60, 240, 200, 90, 0]},
            {"elidx": 3, "domain": 1, "kind": 2,
             "a": [499, 875, 90, 90, 240, 240, 240, 0]},
        ]
    if scene == 1 and mode == 1:
        return [
            {"elidx": 0, "domain": 1, "kind": 3,
             "a": [2, 1003, 3001, 3101, 3202, 0, 0, 0]},
            {"elidx": 1, "domain": 1, "kind": 2,
             "a": [4, 1015, 3000, 3100, 3200, 0, 0, 0]},
            {"elidx": 2, "domain": 1, "kind": 4,
             "a": [8, 1023, 3002, 3101, 3201, 0, 0, 0]},
            {"elidx": 3, "domain": 1, "kind": 2,
             "a": [7, 2004, 3000, 3100, 3200, 0, 0, 0]},
        ]
    if scene == 2 and mode == 0:
        return [
            {"elidx": 0, "domain": 1, "kind": 1,
             "a": [499, 125, 200, 120, 20, 60, 160, 0]},
            {"elidx": 1, "domain": 1, "kind": 2,
             "a": [166, 125, 110, 110, 240, 240, 225, 0]},
            {"elidx": 2, "domain": 1, "kind": 3,
             "a": [832, 375, 90, 90, 200, 60, 30, 0]},
            {"elidx": 3, "domain": 1, "kind": 4,
             "a": [832, 875, 170, 50, 240, 90, 20, 0]},
        ]
    if scene == 2 and mode == 1:
        return [
            {"elidx": 0, "domain": 1, "kind": 1,
             "a": [1, 1059, 3002, 3101, 3201, 0, 0, 0]},
            {"elidx": 1, "domain": 1, "kind": 2,
             "a": [0, 2004, 3000, 3100, 3200, 0, 0, 0]},
            {"elidx": 2, "domain": 1, "kind": 3,
             "a": [5, 1003, 3001, 3101, 3202, 0, 0, 0]},
            {"elidx": 3, "domain": 1, "kind": 4,
             "a": [8, 1027, 3002, 3101, 3201, 0, 0, 0]},
        ]
    raise ValueError((scene, mode))


# ------------------------------------------------------------------ render --
FONT = ImageFont.load_default()


def draw_shape(d, kind, cx, cy, w, h, fill):
    """Draw a visual-domain shape centered at (cx, cy). kind: 1 rect, 2 circle,
    3 triangle, 4 text panel."""
    if kind == 1:
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                    fill=fill, outline=(30, 30, 30), width=2)
    elif kind == 2:
        d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                  fill=fill, outline=(30, 30, 30), width=2)
    elif kind == 3:
        d.polygon([(cx, cy - h / 2), (cx - w / 2, cy + h / 2),
                   (cx + w / 2, cy + h / 2)],
                  fill=fill, outline=(30, 30, 30), width=2)
    elif kind == 4:
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                    fill=fill, outline=(30, 30, 30), width=2)
        tw = d.textlength("TEXT", font=FONT)
        d.text((cx - tw / 2, cy - 6), "TEXT", fill=(30, 30, 30), font=FONT)


def render_visual(elems, mode):
    img = Image.new("RGB", (1000, 1000), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for e in elems:
        a = e["a"]
        if mode == 0:
            x, y, w, h, r, g, b = a[0], a[1], a[2], a[3], a[4], a[5], a[6]
            fill = (r, g, b)
            cx, cy = x, y
        else:
            zone, ch = a[0], a[1]
            cx, cy = ZONE_CENTER[zone]
            fill, _ = human_color(ch)
            if e["kind"] == 4:
                w, h = 200, 60
            else:
                w, h = 120, 120
        draw_shape(d, e["kind"], cx, cy, w, h, fill)
    return img


def bin_to_freq(b):
    return 110.0 * (2.0 ** (b / 12.0))


def timbre_wave(timbre, phase):
    if timbre == 5001:   # BRIGHT: sine + 2nd harmonic
        return math.sin(phase) + 0.4 * math.sin(2 * phase)
    if timbre == 5002:   # DARK: soft triangle
        return 0.8 * (2.0 / math.pi) * math.asin(math.sin(phase))
    if timbre == 5003:   # RICH: saw-ish, first 4 harmonics 1/n
        return (2.0 / math.pi) * sum(math.sin(k * phase) / k
                                     for k in range(1, 5))
    return math.sin(phase)  # 5000 PURE


# Human scenes carry no duration or amplitude. The gallery-layer choice:
# each human note takes the per-note duration of the same brief's machine
# design (brief 3: 250 ms, brief 4: 150 ms) and 0.8 amplitude. Documented.
HUMAN_NOTE_DUR = {3: 250, 4: 150}


def render_audio(elems, mode, brief):
    notes = []
    for e in elems:
        a = e["a"]
        if mode == 0:
            notes.append({"freq": float(a[0]), "dur": float(a[1]),
                          "amp": a[2] / 1000.0, "timbre": 5000})
        else:
            notes.append({"freq": bin_to_freq(a[0]),
                          "dur": float(HUMAN_NOTE_DUR[brief]),
                          "amp": 0.8, "timbre": a[1]})
    total_s = sum(n["dur"] for n in notes) / 1000.0
    W, H, SR = 800, 200, 8000
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.line([0, H // 2, W, H // 2], fill=(210, 210, 210), width=1)
    # per-pixel sample
    pts = []
    for x in range(W):
        t = (x / W) * total_s
        # find note
        tt, note = t, notes[0]
        for n in notes:
            dur_s = n["dur"] / 1000.0
            if tt < dur_s:
                note = n
                break
            tt -= dur_s
        val = note["amp"] * timbre_wave(note["timbre"], 2 * math.pi * note["freq"] * tt)
        pts.append((x, H // 2 - val * (H // 2 - 12)))
    d.line(pts, fill=(20, 60, 160), width=1)
    # segment boundaries + labels
    acc = 0.0
    for n in notes:
        bx = int(acc / total_s * W)
        d.line([bx, 0, bx, H], fill=(200, 200, 200), width=1)
        cx = int((acc + n["dur"] / 1000.0 / 2) / total_s * W)
        label = "%d Hz" % int(round(n["freq"]))
        tw = d.textlength(label, font=FONT)
        d.text((cx - tw / 2, H - 14), label, fill=(80, 80, 80), font=FONT)
        acc += n["dur"] / 1000.0
    return img


BLOCK_FILL, BLOCK_LINE = (178, 142, 96), (90, 60, 30)
STONE_FILL, STONE_LINE = (155, 155, 155), (60, 60, 60)


def render_struct(elems, mode):
    img = Image.new("RGB", (1000, 1000), (255, 255, 255))
    d = ImageDraw.Draw(img)
    bottom = 1000
    for e in elems:
        a = e["a"]
        kind = e["kind"]
        if mode == 0:
            if kind == 1:  # block: side view
                x, z, size = a[0], a[2], a[3]
                w, h = size, size * 0.6
                base_y = bottom - z - h
                d.rectangle([x - w / 2, base_y - h, x + w / 2, base_y],
                            fill=BLOCK_FILL, outline=BLOCK_LINE, width=2)
            else:          # stone: top view
                x, y, size = a[0], a[1], a[3]
                d.ellipse([x - size / 2, y - size / 2, x + size / 2, y + size / 2],
                          fill=STONE_FILL, outline=STONE_LINE, width=2)
    if mode == 1:
        rects = {}

        def block_rect(idx):
            if idx in rects:
                return rects[idx]
            e = elems[idx]
            a = e["a"]
            zone, rel, relt, rank = a[0], a[1], a[2], a[3]
            cx, _ = ZONE_CENTER[zone]
            w, h = rank * 45, rank * 27
            if rel == 5:  # STACKED_ON
                tx0, ty0, tx1, ty1 = block_rect(relt)
                tcy = (tx0 + tx1) / 2
                r = (tcy - w / 2, ty0 - h, tcy + w / 2, ty0)
            else:         # NONE: sitting on the ground
                r = (cx - w / 2, bottom - h, cx + w / 2, bottom)
            rects[idx] = r
            return r

        for i, e in enumerate(elems):
            a = e["a"]
            if e["kind"] == 1:
                r = block_rect(i)
                d.rectangle(r, fill=BLOCK_FILL, outline=BLOCK_LINE, width=2)
            else:
                zone, rel, relt, rank = a[0], a[1], a[2], a[3]
                cx, cy = ZONE_CENTER[zone]
                s = rank * 50
                d.ellipse([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                          fill=STONE_FILL, outline=STONE_LINE, width=2)
    return img


# letter -> (mode, brief), from Q4-PACKET.md footer (unblinding order)
LETTERS = {"A": (0, 3), "B": (1, 3), "C": (0, 4), "D": (1, 4),
           "E": (1, 1), "F": (1, 2), "G": (0, 5), "H": (0, 1),
           "I": (0, 2), "J": (0, 6), "K": (1, 5), "L": (1, 6)}
MODE_NAME = {0: "machine", 1: "human"}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    scenes = load_q2()
    made = []
    for letter in sorted(LETTERS):
        mode, brief = LETTERS[letter]
        elems = scenes[(mode, brief)]
        domain = elems[0]["domain"]
        if domain == 1:
            img = render_visual(elems, mode)
        elif domain == 2:
            img = render_audio(elems, mode, brief)
        else:
            img = render_struct(elems, mode)
        name = "brief%d_%s_%s.png" % (brief, MODE_NAME[mode], letter)
        img.save(os.path.join(out, name))
        made.append(name)
    for scene in (1, 2):
        for mode in (0, 1):
            img = render_visual(q1_scene(scene, mode), mode)
            name = "q1_s%d_%s.png" % (scene, MODE_NAME[mode])
            img.save(os.path.join(out, name))
            made.append(name)
    print("wrote %d PNGs" % len(made))
    for m in sorted(made):
        print(" ", m)


if __name__ == "__main__":
    main()
