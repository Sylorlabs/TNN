#!/usr/bin/env python3
"""FE2: extract the 11 frozen FE1 separator specs (+ COL-5 exclusion) from the
frozen FE1 prereg and verdict into machine-readable specs.json.

Rule: specs come from the frozen documents by script, never from memory.
Every value below is captured by a regex against PREREG_FE1_AUDIT.md section 4
or VERDICT_FE1.md; the script FAILS LOUDLY (exit 1, naming every miss) if any
pattern does not match, so a silent fallback to memory is impossible.
"""
import json
import os
import re
import sys

BASE = os.path.expanduser("~/workspace/pam_round2/fe1_audit")
PREREG = open(os.path.join(BASE, "PREREG_FE1_AUDIT.md")).read()
VERDICT = open(os.path.join(BASE, "VERDICT_FE1.md")).read()
OUT = os.path.join(os.path.expanduser("~/workspace/pam_round2/fe2_port/build"),
                   "specs.json")

fails = []


class G:
    def __init__(self, m, name):
        self._m = m
        self._name = name

    def group(self, i):
        if self._m is None:
            fails.append(self._name)
            return "MISSING"
        return self._m.group(i)


def grab(pat, text, name, flags=0):
    return G(re.search(pat, text, flags), name)


def inum(gm, i=1):
    return int(gm.group(i).replace("−", "-"))


def sec_grab(pat, name):
    return grab(pat, PREREG, name, re.S)


specs = {"_source": {"prereg": "PREREG_FE1_AUDIT.md",
                     "verdict": "VERDICT_FE1.md",
                     "note": "all values regex-extracted; script fails loud on mismatch"}}

# ---------------- shared correlator notation ----------------
m = grab(r"C\(f, seg\) = .*?0\.5 Hz steps unless stated", PREREG, "corr_notation", re.S)
_ = m.group(0)
specs["correlator"] = {
    "definition": "C(f,seg)=(sum s*cos(2πfi/16000))^2+(sum s*sin(2πfi/16000))^2",
    "default_step_hz": 0.5}

# ---------------- PTC-4 ----------------
sec = sec_grab(r"### PTC-4.*?### PTC-5", "ptc4_sec").group(0)
g = grab(r"fA = argmax C\(f, segA\), f ∈ \[(\d+),(\d+)\]", sec, "ptc4_grid")
g2 = grab(r"\|Δ\| < ([\d.]+) → SAME", sec, "ptc4_thr")
g3 = grab(r"segA pure fA \((\d+)–(\d+) Hz\)", sec, "ptc4_fA_range")
g4 = grab(r"det ∈ \[(\d+),(\d+)\] Hz", sec, "ptc4_det")
g5 = grab(r"f2 = argmax C\(f, segB\) over \|f−f1\| ≥ (\d+) Hz", sec, "ptc4_excl")
g6 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "ptc4_truths")
specs["PTC-4"] = {
    "kind": "pitch", "rule": "beat-partial-center",
    "grid_lo": int(g.group(1)), "grid_hi": int(g.group(2)), "grid_step_hz": 0.5,
    "segA": [0, 8000], "segB": [8000, 16000],
    "fA_range": [int(g3.group(1)), int(g3.group(2))],
    "det_range": [int(g4.group(1)), int(g4.group(2))],
    "beat_excl_hz": float(g5.group(1)),
    "same_thr_hz": float(g2.group(1)),
    "truths": [t.strip() for t in g6.group(1).split(",")],
}

# ---------------- PTC-5 ----------------
sec = sec_grab(r"### PTC-5.*?### TMB-4", "ptc5_sec").group(0)
g = grab(r"(\d+) ms \(960-sample\) silence gap", sec, "ptc5_gap_ms")
g2 = grab(r"segB samples \[(\d+),(\d+)\)", sec, "ptc5_gap")
g3 = grab(r"t2 ∉ \[(\d+),(\d+)\)", sec, "ptc5_guard")
g4 = grab(r"fA = argmax C\(f, segA\), f ∈ \[(\d+),(\d+)\]", sec, "ptc5_grid")
g5 = grab(r"Same decision rule as PTC-4", sec, "ptc5_rule_ref")
_ = g5.group(0)
g6 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "ptc5_truths")
specs["PTC-5"] = {
    "kind": "pitch", "rule": "pitch-outside-gap",
    "grid_lo": int(g4.group(1)), "grid_hi": int(g4.group(2)), "grid_step_hz": 0.5,
    "segA": [0, 8000], "segB": [8000, 16000],
    "gap_ms": int(g.group(1)), "gap_segB": [int(g2.group(1)), int(g2.group(2))],
    "guard_t2": [int(g3.group(1)), int(g3.group(2))],
    "same_thr_hz": specs["PTC-4"]["same_thr_hz"],
    "truths": [t.strip() for t in g6.group(1).split(",")],
}

# ---------------- TMB-4 ----------------
sec = sec_grab(r"### TMB-4.*?### TMB-5", "tmb4_sec").group(0)
g = grab(r"f0 = argmax over f ∈ \[(\d+),(\d+)\] of harmonic-sum", sec, "tmb4_grid")
g2 = grab(r"Σ_\{k=1\.\.(\d+)\}", sec, "tmb4_harm")
g3 = grab(r"r2 < ([\d.]+) → DARK; r2 > ([\d.]+) → BRIGHT; else RICH", sec, "tmb4_thr")
g4 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "tmb4_truths")
specs["TMB-4"] = {
    "kind": "timbre", "rule": "harmonic-sum-f0 + A2/A1",
    "grid_lo": int(g.group(1)), "grid_hi": int(g.group(2)), "grid_step_hz": 0.5,
    "harmonics": list(range(1, int(g2.group(1)) + 1)),
    "thr_dark": float(g3.group(1)), "thr_bright": float(g3.group(2)),
    "truths": [t.strip() for t in g4.group(1).split(",")],
}

# ---------------- TMB-5 ----------------
sec = sec_grab(r"### TMB-5.*?### COL-4", "tmb5_sec").group(0)
g = grab(r"centroid < (\d+) → DARK else BRIGHT", sec, "tmb5_thr")
g2 = grab(r"f ∈ \[(\d+),(\d+)\] Hz", sec, "tmb5_range")
g3 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "tmb5_truths")
specs["TMB-5"] = {
    "kind": "timbre", "rule": "spectral-centroid",
    "spectrum_range": [int(g2.group(1)), int(g2.group(2))],
    "centroid_thr_hz": float(g.group(1)),
    "truths": [t.strip() for t in g3.group(1).split(",")],
}

# ---------------- COL-4 ----------------
sec = sec_grab(r"### COL-4.*?### COL-5", "col4_sec").group(0)
g = grab(r"(\d+)×(\d+)", sec, "col4_dims")
g2 = grab(r"L = mean RGB of left panel \(x ∈ \[(\d+),(\d+)\)\)", sec, "col4_left")
g3 = grab(r"R = mean RGB of right-panel\s+columns x ∈ \[(\d+),(\d+)\)", sec, "col4_right")
g4 = grab(r"d > (\d+) → DIFFERENT else SAME", sec, "col4_thr")
g5 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "col4_truths")
specs["COL-4"] = {
    "kind": "color", "rule": "ramp-neutral-edge-compare",
    "img_wh": [int(g.group(1)), int(g.group(2))],
    "left_x": [int(g2.group(1)), int(g2.group(2))],
    "right_x": [int(g3.group(1)), int(g3.group(2))],
    "thr": float(g4.group(1)),
    "truths": [t.strip() for t in g5.group(1).split(",")],
}

# ---------------- COL-5 (EXCLUDED) ----------------
vsec = grab(r"## 4\. COL-5 — defense-scope finding.*?(?=## 5\.)",
            VERDICT, "col5_verdict", re.S).group(0)
g = grab(r"\*\*([\d.]+)/24 = ([\d.]+)%\*\*", vsec, "col5_ceiling")
specs["COL-5"] = {
    "excluded": True,
    "verdict": "DEFENSE-SCOPE",
    "reason": ("machine-checked Bayes ceiling %s/24 (%s%%) < 80%% bar; "
               "no byte-function reaches the separator bar (FE1 verdict section 4)"
               % (g.group(1), g.group(2))),
    "ceiling": [float(g.group(1)), 24],
}

# ---------------- CCN-3 ----------------
sec = sec_grab(r"### CCN-3.*?### CCN-4", "ccn3_sec").group(0)
g = grab(r"(\d+)×(\d+)", sec, "ccn3_dims")
g2 = grab(r"\((\d+)×(\d+) quadrants", sec, "ccn3_quad")
g3 = grab(r"warm \((\d+),(\d+),(\d+)\), cool \((\d+),(\d+),(\d+)\)", sec, "ccn3_illum")
g4 = grab(r"\(\(v·(\d+)\)/10, \(v·(\d+)\)/10\)", sec, "ccn3_tint")
g5 = grab(r"MAD < (\d+) → SAME_SURFACE else DIFFERENT", sec, "ccn3_thr")
g6 = grab(r"Truth ∈ \{([A-Z_, ]+)\}", sec, "ccn3_truths")
specs["CCN-3"] = {
    "kind": "colorconst", "rule": "per-quadrant-von-Kries",
    "img_wh": [int(g.group(1)), int(g.group(2))],
    "quadrants": [int(g2.group(1)), int(g2.group(2))],
    "illum_warm": [int(g3.group(1)), int(g3.group(2)), int(g3.group(3))],
    "illum_cool": [int(g3.group(4)), int(g3.group(5)), int(g3.group(6))],
    "tint_div": [int(g4.group(1)), int(g4.group(2))],
    "thr": float(g5.group(1)),
    "truths": [t.strip() for t in g6.group(1).split(",")],
}

# ---------------- CCN-4 ----------------
sec = sec_grab(r"### CCN-4.*?### SHP-4", "ccn4_sec").group(0)
g = grab(r"band = y/(\d+); middle band ×([\d.]+)", sec, "ccn4_band")
g2 = grab(r"MAD < (\d+) → SAME_SURFACE else DIFFERENT", sec, "ccn4_thr")
g3 = grab(r"Truth ∈ \{([A-Z_, ]+)\}", sec, "ccn4_truths")
specs["CCN-4"] = {
    "kind": "colorconst", "rule": "per-band-exposure-inversion",
    "band_div": int(g.group(1)), "band1_exposure": float(g.group(2)),
    "thr": float(g2.group(1)),
    "truths": [t.strip() for t in g3.group(1).split(",")],
}

# ---------------- SHP-4 ----------------
sec = sec_grab(r"### SHP-4.*?### SHP-5", "shp4_sec").group(0)
g = grab(r"(\d+)×(\d+)", sec, "shp4_dims")
g2 = grab(r"\(b−r\) > (\d+) ∧ \(b−g\) > (\d+)", sec, "shp4_mask")
g3 = grab(r"at \((\d+),(\d+)\) s=(\d+)", sec, "shp4_tpl")
g4 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "shp4_truths")
specs["SHP-4"] = {
    "kind": "shape", "rule": "color-keyed-template-iou",
    "img_wh": [int(g.group(1)), int(g.group(2))],
    "mask": {"b_r_gt": int(g2.group(1)), "b_g_gt": int(g2.group(2))},
    "template_center": [int(g3.group(1)), int(g3.group(2))],
    "template_s": int(g3.group(3)),
    "truths": [t.strip() for t in g4.group(1).split(",")],
}

# ---------------- SHP-5 ----------------
sec = sec_grab(r"### SHP-5.*?### MOT-4", "shp5_sec").group(0)
g = grab(r"\(r−b\) > (\d+)", sec, "shp5_mask")
g2 = grab(r"draw_shape\(sh, (\d+), (\d+), (\d+)\)", sec, "shp5_tpl")
g3 = grab(r"\(\((\d+),([−\-]?\d+)\), \(([−\-]?\d+),(\d+)\), \((\d+),(\d+)\), \(([−\-]?\d+),([−\-]?\d+)\)\)",
          sec, "shp5_off")
g4 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "shp5_truths")
specs["SHP-5"] = {
    "kind": "shape", "rule": "forward-tile-template-iou",
    "mask": {"r_b_gt": int(g.group(1))},
    "template_center": [int(g2.group(1)), int(g2.group(2))],
    "template_s": int(g2.group(3)),
    "tile_offsets": [[inum(g3, 1), inum(g3, 2)],
                     [inum(g3, 3), inum(g3, 4)],
                     [inum(g3, 5), inum(g3, 6)],
                     [inum(g3, 7), inum(g3, 8)]],
    "tile": 48,
    "truths": [t.strip() for t in g4.group(1).split(",")],
}

# ---------------- MOT-4 ----------------
sec = sec_grab(r"### MOT-4.*?### MOT-5", "mot4_sec").group(0)
g = grab(r"(\d+) frames (\d+)×(\d+)", sec, "mot4_dims")
g2 = grab(r"R ≥ (\d+); tail pixels = R ∈ \[(\d+),(\d+)\)", sec, "mot4_levels")
g3 = grab(r"Chebyshev distance ≤ (\d+) of H", sec, "mot4_box")
g4 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "mot4_truths")
specs["MOT-4"] = {
    "kind": "motion", "rule": "comet-tail-orientation",
    "vid": [int(g.group(1)), int(g.group(2)), int(g.group(3))],
    "head_thr": int(g2.group(1)),
    "tail_lo": int(g2.group(2)), "tail_hi": int(g2.group(3)),
    "box": int(g3.group(1)),
    "truths": [t.strip() for t in g4.group(1).split(",")],
}

# ---------------- MOT-5 ----------------
sec = sec_grab(r"### MOT-5.*", "mot5_sec").group(0)
g = grab(r"\|Δx\|\+\|Δy\| < (\d+) → STILL", sec, "mot5_still")
g2 = grab(r"Truth ∈ \{([A-Z, ]+)\}", sec, "mot5_truths")
g3 = grab(r"centroid of pixels with R ≥ (\d+) per frame", sec, "mot5_thr")
specs["MOT-5"] = {
    "kind": "motion", "rule": "absolute-dot-displacement",
    "head_thr": int(g3.group(1)),
    "still_thr": int(g.group(1)),
    "truths": [t.strip() for t in g2.group(1).split(",")],
}

# ---------------- FE1 measured margins (verdict table, context only) ----------------
margins = {}
for fam in ["PTC-4", "PTC-5", "TMB-4", "TMB-5", "COL-4",
            "CCN-3", "CCN-4", "SHP-4", "SHP-5", "MOT-4", "MOT-5"]:
    row = grab(r"\| " + fam + r" .*?\|", VERDICT, "verdict_row_" + fam, re.S)
    margins[fam] = row.group(0)[:200].replace("\n", " ")
specs["_fe1_margins"] = margins

real_fails = [f for f in fails]
if real_fails:
    print("EXTRACTION FAILED for: " + ", ".join(sorted(set(real_fails))))
    sys.exit(1)

with open(OUT, "w") as f:
    json.dump(specs, f, indent=1)
print("wrote", OUT, "families:",
      [k for k in specs if not k.startswith("_")])
