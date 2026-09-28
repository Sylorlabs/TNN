#!/usr/bin/env python3
"""R10 beauty generator — builds the r10 beauty .zag from the FROZEN r8b
source by string patching (never hand-transcribed).

Usage:
  gen_beauty.py [CX0 CY0] [OUTNAME]
    no args        -> full-frame 1024 r10_beauty_1024.zag
    CX0 CY0        -> 256x256 crop of the 1024 frame at (CX0,CY0) for iteration
    OUTNAME        -> output .zag filename (default derived)

Mechanism set (all zero-RNG, T1 sun accessors byte-identical):
  r9 revs (pending-judgment, crew's own iteration evidence):
    F  rock angularity rev2 (ridged displacement, smin 0.8, tint, crackle)
    P  cobbles rev3 (9.0 cell, r 2.0-4.5, per-cobble tint)
    D  ejecta-sorted grain rev2
    b  downslope striation
    e  talus chips
    c  cirrus filaments (weak-logic)
  r10 beauty (this round):
    B-LAKE   T14: the graben floods — real water SDF + wave normals +
             sky reflection + sun glitter + fresnel + aerial fog
    B-FILL   two-lobe hemisphere sky ambient from the deliberated dome
    B-GLINT  microfacet fix: glint lobe fades with pixel footprint
    B-AERIAL stronger exponential scatter for the deliberated dust load
    B-MOON   planetshine to display legibility (airless: no limb glow)
    B-CLOUD  silver lining (forward scatter) on cirrus edges
    B-STRATA flood-basalt flow banding on steep faces
"""
import sys, os, re

IMGDIR = os.path.dirname(os.path.abspath(__file__)) + "/.."
R10SRC = os.path.dirname(os.path.abspath(__file__)) + "/src"
os.makedirs(R10SRC, exist_ok=True)

CX0 = CY0 = None
OUTNAME = None
DEBUGMASK = False
args = sys.argv[1:]
if args and args[0] == "--debugmask":
    DEBUGMASK = True
    args = args[1:]
if len(args) >= 2 and args[0].lstrip("-").isdigit():
    CX0, CY0 = int(args[0]), int(args[1])
    args = args[2:]
if len(args) >= 1:
    OUTNAME = args[0]
CROP = CX0 is not None
if OUTNAME is None:
    OUTNAME = f"r10_beauty_crop_{CX0}_{CY0}.zag" if CROP else "r10_beauty_1024.zag"

src = open(f"{IMGDIR}/r8b_alien.zag").read()
orig_sun_block = src[src.index("// T1"):src.index("// T2")]

def rep(old, new, count=1):
    global src
    assert src.count(old) >= count, f"PATCH MISS: {old[:80]!r}"
    src = src.replace(old, new, count)

def ins_before_line_containing(sub, text):
    """Insert text as its own lines before the first line containing sub."""
    global src
    lines = src.split("\n")
    for i, ln in enumerate(lines):
        if sub in ln:
            lines.insert(i, text)
            src = "\n".join(lines)
            return
    raise AssertionError(f"INSERT MISS: {sub!r}")

T7MARK = "seeing is occlusion, not paint"

# ---------- crop plumbing (baked constants; no atoi in substrate) ----------
if CROP:
    rep("""            let ndcx:f64 = (2.0 * (x as f64) + 1.0) / (w as f64) - 1.0;
            let ndcy:f64 = 1.0 - (2.0 * (y as f64) + 1.0) / (h as f64);""",
        f"""            let ndcx:f64 = (2.0 * ((x as f64) + {CX0}.0) + 1.0) / 1024.0 - 1.0;
            let ndcy:f64 = 1.0 - (2.0 * ((y as f64) + {CY0}.0) + 1.0) / 1024.0;""")
    rep('    let aspect:f64 = (w as f64) / (h as f64);',
        '    let aspect:f64 = 1.0; // R10 crop: square pixels preserved')
    rep("""        if (y - (y / 64) * 64 == 0) {
            _zag_print("row ");
            _zag_println(_zag_i64_to_str(y));
        }""", """        if (0 == 1) {
            _zag_print("row ");
            _zag_println(_zag_i64_to_str(y));
        }""")

# ================= r9 rev mechanisms (pending judgment) =================
# ---- M-e: talus chips ----
ins_before_line_containing(T7MARK, """// R9 M-e: angular talus chips at rock bases. Scene truth: mechanical
// weathering sheds joint-bounded fragments that accumulate around the
// outcrop they fell from — octahedron SDF (angular by construction),
// hashed scatter, half-buried in local ground.
fn b_talus(px:f64, py:f64, pz:f64, gd:f64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64) f64 {
    let best:f64 = 1000000000.0;
    let i:i64 = 0;
    while (i < 5) {
        let cx:f64 = b_rockpick(i, 0);
        let cz:f64 = b_rockpick(i, 1);
        let dx:f64 = px - cx;
        let dz:f64 = pz - cz;
        if (dx * dx + dz * dz < 900.0) {
            let cy:f64 = c0;
            if (i == 1) { cy = c1; }
            if (i == 2) { cy = c2; }
            if (i == 3) { cy = c3; }
            if (i == 4) { cy = c4; }
            let j:i64 = 0;
            while (j < 8) {
                let h1:i64 = b_h01(i * 131 + j * 17 + 1, 7, 920);
                let h2:i64 = b_h01(i * 131 + j * 17 + 2, 7, 921);
                let ox:f64 = ((h1 as f64) / 1024.0 - 0.5) * 44.0;
                let oz:f64 = ((h2 as f64) / 1024.0 - 0.5) * 44.0;
                if (ox * ox + oz * oz < 484.0) {
                    let h3:i64 = b_h01(i * 131 + j * 17 + 3, 7, 922);
                    let cr:f64 = 0.25 + (h3 as f64) / 1024.0 * 0.65;
                    let qx:f64 = cx + ox;
                    let qz:f64 = cz + oz;
                    let gy:f64 = py - gd - cr * 0.30;
                    let ex:f64 = b_abs(px - qx);
                    let ey:f64 = b_abs(py - gy);
                    let ez:f64 = b_abs(pz - qz);
                    let di:f64 = (ex + ey * 1.3 + ez) * 0.55 - cr;
                    if (di < best) { best = di; }
                }
                j = j + 1;
            }
        }
        i = i + 1;
    }
    return best;
}""")
rep("""        if (rd < d) { d = rd; }
    }
    return d;
}""",
"""        if (rd < d) { d = rd; }
    }
    if (d < 8.0) {
        let td:f64 = b_talus(px, py, pz, d, c0, c1, c2, c3, c4);
        if (td < d) { d = td; }
    }
    return d;
}""", count=2)

# ---- M-P: cobbles rev3 (9.0 cell) + per-cobble tint ----
ins_before_line_containing(T7MARK, """// R9 M-P: discrete cobble bodies rev3. Scene truth: weathering/rockfall
// shed discrete stones that sit ON the ground as separate bodies —
// min-blended (never smooth-min welded), each throwing its own contact
// shadow through the existing shadow march. Hashed 9.0-unit grid,
// near field only; each stone gets its own mineral tint below.
fn b_pebd(px:f64, py:f64, pz:f64, gd:f64, camx:f64, camz:f64) f64 {
    let ddx:f64 = px - camx;
    let ddz:f64 = pz - camz;
    if (ddx * ddx + ddz * ddz > 67600.0) { return 1000000000.0; }
    let cs:f64 = 9.0;
    let cx0:i64 = b_ifloor(px / cs) - 1;
    let cz0:i64 = b_ifloor(pz / cs) - 1;
    let best:f64 = 1000000000.0;
    let ix:i64 = 0;
    while (ix < 3) {
        let iz:i64 = 0;
        while (iz < 3) {
            let cx:i64 = cx0 + ix;
            let cz2:i64 = cz0 + iz;
            let h0:i64 = b_h01(cx, cz2, 910);
            if (h0 > 780) {
                let jx:f64 = ((b_h01(cx * 3 + 1, cz2, 911) as f64) / 1024.0 - 0.5) * 2.5 * 2.0;
                let jz:f64 = ((b_h01(cx, cz2 * 3 + 1, 912) as f64) / 1024.0 - 0.5) * 2.5 * 2.0;
                let pr:f64 = 2.0 + (b_h01(cx * 5 + 2, cz2 * 5 + 3, 913) as f64) / 1024.0 * 2.5;
                let qx:f64 = (cx as f64) * cs + jx;
                let qz:f64 = (cz2 as f64) * cs + jz;
                let gy:f64 = py - gd - pr * 0.20;
                let ex:f64 = px - qx;
                let ey:f64 = (py - gy) * 1.35;
                let ez:f64 = pz - qz;
                let di:f64 = b_sqrt(ex * ex + ey * ey + ez * ez) - pr;
                if (di < best) { best = di; }
            }
            iz = iz + 1;
        }
        ix = ix + 1;
    }
    return best;
}
// R9 M-P: per-cobble tint from the same hashed field as b_pebd.
fn b_pcobtint(px:f64, pz:f64) f64 {
    let cs:f64 = 9.0;
    let cx0:i64 = b_ifloor(px / cs) - 1;
    let cz0:i64 = b_ifloor(pz / cs) - 1;
    let best:f64 = 1000000000.0;
    let btint:f64 = 1.0;
    let ix:i64 = 0;
    while (ix < 3) {
        let iz:i64 = 0;
        while (iz < 3) {
            let cx:i64 = cx0 + ix;
            let cz2:i64 = cz0 + iz;
            let h0:i64 = b_h01(cx, cz2, 910);
            if (h0 > 780) {
                let jx:f64 = ((b_h01(cx * 3 + 1, cz2, 911) as f64) / 1024.0 - 0.5) * 2.5 * 2.0;
                let jz:f64 = ((b_h01(cx, cz2 * 3 + 1, 912) as f64) / 1024.0 - 0.5) * 2.5 * 2.0;
                let pr:f64 = 2.0 + (b_h01(cx * 5 + 2, cz2 * 5 + 3, 913) as f64) / 1024.0 * 2.5;
                let qx:f64 = (cx as f64) * cs + jx;
                let qz:f64 = (cz2 as f64) * cs + jz;
                let ex:f64 = px - qx;
                let ez:f64 = pz - qz;
                let dh:f64 = b_sqrt(ex * ex + ez * ez) - pr;
                if (dh < best) {
                    best = dh;
                    let th:i64 = b_h01(cx * 7 + 4, cz2 * 7 + 5, 914);
                    btint = 0.72 + (th as f64) / 1024.0 * 0.55;
                }
            }
            iz = iz + 1;
        }
        ix = ix + 1;
    }
    if (best < 1.2) { return btint; }
    return 1.0;
}""")
rep("""    if (d < 8.0) {
        let td:f64 = b_talus(px, py, pz, d, c0, c1, c2, c3, c4);
        if (td < d) { d = td; }
    }
    return d;
}""",
"""    if (d < 8.0) {
        let td:f64 = b_talus(px, py, pz, d, c0, c1, c2, c3, c4);
        if (td < d) { d = td; }
    }
    if (d < 6.0) {
        let pd:f64 = b_pebd(px, py, pz, d, camx, camz);
        if (pd < d) { d = pd; }
    }
    return d;
}""", count=2)
# per-cobble tint inside b_tshade (positional: first sx-block after b_tshade)
_ti = src.index("fn b_tshade(")
_tj = src.index("    let sx:f64 = b_sunx();", _ti)
_tintblock = """    // R9 M-P: per-cobble tint — separate stones, separate mineral tint.
    let pctint:f64 = b_pcobtint(px, pz);
    ar = ar * pctint; ag = ag * pctint; ab = ab * pctint;
"""
src = src[:_tj] + _tintblock + src[_tj:]

# ---- M-F: rock angularity rev2 ----
rep("""fn b_rockd(px:f64, py:f64, pz:f64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64) f64 {
    let d:f64 = 1000000000.0;
    let i:i64 = 0;
    while (i < 5) {
        let cx:f64 = b_rockpick(i, 0);
        let cz:f64 = b_rockpick(i, 1);
        let rr:f64 = b_rockpick(i, 2);
        let cy:f64 = c0;
        if (i == 1) { cy = c1; }
        if (i == 2) { cy = c2; }
        if (i == 3) { cy = c3; }
        if (i == 4) { cy = c4; }
        let qx:f64 = (px - cx) * 0.3 + (i as f64) * 7.0;
        let qy:f64 = (py - cy) * 0.3;
        let qz:f64 = (pz - cz) * 0.3;
        let disp:f64 = rr * (1.0 + 0.55 * (b_vn3(qx, qy, qz, 510 + i) - 0.5) * 2.0);
        let ex:f64 = px - cx;
        let ey:f64 = py - cy;
        let ez:f64 = pz - cz;
        let di:f64 = b_sqrt(ex * ex + ey * ey + ez * ez) - disp;
        d = b_smin(d, di, 3.0);
        i = i + 1;
    }
    return d;
}""",
"""// R9 M-F: per-rock signed distance with ANGULAR displacement rev2.
// Scene truth: jointed basalt breaks into angular blocks with planar
// fracture faces — broad-facet ridged swells, not smooth value-noise
// lumps, not spikes. Blocks stay discrete (smin 0.8, not welded).
fn b_rockdi(px:f64, py:f64, pz:f64, i:i64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64) f64 {
    let cx:f64 = b_rockpick(i, 0);
    let cz:f64 = b_rockpick(i, 1);
    let rr:f64 = b_rockpick(i, 2);
    let cy:f64 = c0;
    if (i == 1) { cy = c1; }
    if (i == 2) { cy = c2; }
    if (i == 3) { cy = c3; }
    if (i == 4) { cy = c4; }
    let qx:f64 = (px - cx) * 0.12 + (i as f64) * 7.0;
    let qy:f64 = (py - cy) * 0.12;
    let qz:f64 = (pz - cz) * 0.12;
    let rn:f64 = b_vn3(qx, qy, qz, 510 + i);
    let rg:f64 = 1.0 - b_abs(rn + rn - 1.0);
    let disp:f64 = rr * (0.78 + 0.34 * rg * rg);
    let ex:f64 = px - cx;
    let ey:f64 = py - cy;
    let ez:f64 = pz - cz;
    return b_sqrt(ex * ex + ey * ey + ez * ez) - disp;
}
fn b_rockd(px:f64, py:f64, pz:f64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64) f64 {
    let d:f64 = 1000000000.0;
    let i:i64 = 0;
    while (i < 5) {
        let di:f64 = b_rockdi(px, py, pz, i, c0, c1, c2, c3, c4);
        d = b_smin(d, di, 0.8);
        i = i + 1;
    }
    return d;
}
fn b_rockidx(px:f64, py:f64, pz:f64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64) i64 {
    let best:i64 = 0;
    let bd:f64 = 1000000000.0;
    let i:i64 = 0;
    while (i < 5) {
        let di:f64 = b_rockdi(px, py, pz, i, c0, c1, c2, c3, c4);
        if (di < bd) { bd = di; best = i; }
        i = i + 1;
    }
    return best;
}""")
rep("""    if (slope > 0.5) {
        let st:f64 = 0.93 + 0.14 * b_vn3(px * 0.045, py * 0.045, pz * 0.045, 77);
        ar = ar * st; ag = ag * st; ab = ab * st;
    }""",
"""    if (slope > 0.5) {
        let st:f64 = 0.93 + 0.14 * b_vn3(px * 0.045, py * 0.045, pz * 0.045, 77);
        ar = ar * st; ag = ag * st; ab = ab * st;
    }
    // R9 M-F: rock identity — per-block mineral tint + fracture crackle.
    // Crackle: thin dark lines where 3D noise crosses 0.5 (joint traces).
    let rrd:f64 = b_rockd(px, py, pz, c0, c1, c2, c3, c4);
    let rockness:f64 = 1.0 - b_ss((rrd + 1.5) / 3.0);
    if (rockness > 0.01) {
        let ri2:i64 = b_rockidx(px, py, pz, c0, c1, c2, c3, c4);
        let rh2:i64 = b_h01(ri2 * 37 + 11, 5, 901);
        let tint2:f64 = 0.78 + (rh2 as f64) / 1024.0 * 0.47;
        let cr2:f64 = 1.0 - b_abs(b_vn3(px * 0.55, py * 0.55, pz * 0.55, 902) - 0.5) * 2.0;
        let crackline:f64 = b_ss((cr2 - 0.965) / 0.02);
        let cm2:f64 = 1.0 - crackline * 0.45 * rockness;
        ar = ar * tint2 * cm2; ag = ag * tint2 * cm2; ab = ab * tint2 * cm2;
    }""")

# ---- M-b: downslope striation ----
rep("""    if (slope > 0.5) {
        let st:f64 = 0.93 + 0.14 * b_vn3(px * 0.045, py * 0.045, pz * 0.045, 77);
        ar = ar * st; ag = ag * st; ab = ab * st;
    }""",
"""    if (slope > 0.5) {
        let st:f64 = 0.93 + 0.14 * b_vn3(px * 0.045, py * 0.045, pz * 0.045, 77);
        ar = ar * st; ag = ag * st; ab = ab * st;
    }
    // R9 M-b: fine downslope striation. Scene truth: wind/water carve
    // gullies downhill — streaks elongated along the fall line, at two
    // scales, gated by slope so flats keep their dust.
    if (slope > 0.35) {
        let sk3:f64 = b_ss((slope - 0.35) / 0.25);
        let sdist:f64 = 1.0 - b_clamp(t / 700.0, 0.0, 1.0);
        let st1:f64 = b_vn2(px * 0.55 + py * 0.10, pz * 0.55 - py * 0.10, 803) - 0.5;
        let st2:f64 = b_vn2(px * 1.60 + py * 0.35, pz * 1.60 - py * 0.35, 804) - 0.5;
        let sm3:f64 = 1.0 + (st1 * 0.38 + st2 * 0.20) * sk3 * sdist;
        ar = ar * sm3; ag = ag * sm3; ab = ab * sm3;
    }""")

# ---- R10 B-STRATA: flood-basalt flow banding on steep faces ----
rep("""        let sm3:f64 = 1.0 + (st1 * 0.38 + st2 * 0.20) * sk3 * sdist;
        ar = ar * sm3; ag = ag * sm3; ab = ab * sm3;
    }""",
"""        let sm3:f64 = 1.0 + (st1 * 0.38 + st2 * 0.20) * sk3 * sdist;
        ar = ar * sm3; ag = ag * sm3; ab = ab * sm3;
    }
    // R10 B-STRATA: flood-basalt layering. Scene truth: a shield volcano
    // stacks lava flows — thin strata show on steep faces as
    // world-space y-banding warped by 3D noise, subtle, distance-faded.
    if (slope > 0.55) {
        let bandn:f64 = b_vn3(px * 0.05, py * 0.55, pz * 0.05, 961) - 0.5;
        let stfade:f64 = 1.0 - b_clamp(t / 700.0, 0.0, 1.0);
        let stm:f64 = 1.0 + bandn * 0.22 * b_ss((slope - 0.55) / 0.2) * stfade;
        ar = ar * stm; ag = ag * stm; ab = ab * stm;
    }""")

# ---- M-D: ejecta-sorted grain rev2 ----
rep("""    let sx:f64 = b_sunx();
    let sy:f64 = b_suny();
    let sz:f64 = b_sunz();
    let dif:f64 = nx * sx + ny * sy + nz * sz;""",
"""    // R9 M-D: multi-scale grain as ejecta sorting rev2. Scene truth:
    // mechanical weathering makes coarse fragments near their source
    // rock; wind settles fines where dust already settles (flats,
    // sheltered concavities). World-space hashes — no tiling;
    // distance-faded against aliasing.
    let g1:f64 = b_vn2(px * 2.1 + 7.7, pz * 2.1 + 3.1, 801) - 0.5;
    let g2:f64 = b_vn2(px * 6.3 + 1.2, pz * 6.3 + 9.4, 802) - 0.5;
    let rdx9:f64 = b_rockd(px, py, pz, c0, c1, c2, c3, c4);
    let prox:f64 = 1.0 - b_ss((rdx9 + 2.0) / 24.0);
    let sortm:f64 = 0.35 + 0.65 * b_clamp(prox + dust * 0.7, 0.0, 1.0);
    let gf2:f64 = 1.0 - b_clamp(t / 450.0, 0.0, 1.0);
    let gr2:f64 = 1.0 + (g1 * 0.55 + g2 * 0.14) * sortm * gf2;
    ar = ar * gr2; ag = ag * gr2; ab = ab * gr2;
    // sharp dark speckle: individual mineral grains
    let spq:f64 = 0.5 - b_abs(b_vn2(px * 4.6 + 1.2, pz * 4.6 + 9.4, 808) - 0.5);
    let spkq:f64 = 1.0 - spq * 2.0 * 0.30 * sortm * gf2;
    ar = ar * spkq; ag = ag * spkq; ab = ab * spkq;
    let sx:f64 = b_sunx();
    let sy:f64 = b_suny();
    let sz:f64 = b_sunz();
    let dif:f64 = nx * sx + ny * sy + nz * sz;""")

# ---- M-c: cirrus filaments along the deliberated wind ----
rep("""        let m:f64 = b_ss((cm - 0.56) / 0.16) * b_ss((dy - 0.02) / 0.15) * 0.55;""",
"""        let m:f64 = b_ss((cm - 0.56) / 0.16) * b_ss((dy - 0.02) / 0.15) * 0.55;
        // R9 M-c: wind-sheared filaments. Scene truth: upper winds run
        // along +x/-z (deliberated T2 flow); ice streaks stretch downwind
        // and fray across it. Honest only while tied to this azimuth.
        let wu:f64 = px * 0.8 - pz * 0.6;
        let wv:f64 = px * 0.6 + pz * 0.8;
        let fil:f64 = b_rid2(wu * 0.8 + 2.2, wv * 4.0 + 5.5, 605, 3);
        m = m * (0.45 + 0.55 * fil);""")

# ---- R10 B-CLOUD: silver lining (forward Mie scatter on sunward edges) ----
rep("""        let cr:f64 = b_mix(0.55, 1.0, sunAmt);
        let cg:f64 = b_mix(0.42, 0.72, sunAmt);
        let cb:f64 = b_mix(0.48, 0.55, sunAmt);
        r = b_mix(r, cr, m);
        g = b_mix(g, cg, m);
        b = b_mix(b, cb, m);""",
"""        let cr:f64 = b_mix(0.55, 1.0, sunAmt);
        let cg:f64 = b_mix(0.42, 0.72, sunAmt);
        let cb:f64 = b_mix(0.48, 0.55, sunAmt);
        // R10 B-CLOUD: silver lining — ice streaks between viewer and sun
        // forward-scatter; the sunward edges silver. Gated to cloud
        // edges (m*(1-m)) so cores keep their body color.
        let lin:f64 = b_ss((sunAmt - 0.5) / 0.35) * m * (1.0 - m) * 1.4;
        let crl:f64 = cr + lin * 0.85;
        let cgl:f64 = cg + lin * 0.62;
        let cbl:f64 = cb + lin * 0.45;
        r = b_mix(r, crl, m);
        g = b_mix(g, cgl, m);
        b = b_mix(b, cbl, m);""")

# ================= r10 beauty mechanisms =================
# ---- B-FILL: two-lobe hemisphere sky ambient ----
rep("""    let amb:f64 = (0.3 + 0.7 * ao) * (0.5 + 0.5 * (ny * 0.5 + 0.5));
    // dusk fill: the dusty sky scatters generously; shadowed ground
    // stays readable, never pitch black (deliberated atmosphere §2)
    lr = lr + ar * b_sky(nx, ny, nz, 0) * amb * 0.9;
    lg = lg + ag * b_sky(nx, ny, nz, 1) * amb * 0.9;
    lb = lb + ab * b_sky(nx, ny, nz, 2) * amb * 0.9;""",
"""    let amb:f64 = (0.3 + 0.7 * ao) * (0.5 + 0.5 * (ny * 0.5 + 0.5));
    // R10 B-FILL: two-lobe hemisphere ambient from the deliberated sky
    // dome. Scene truth: a ground point's sky hemisphere includes the
    // bright sunward horizon band, not just the zenith above its normal.
    // The old single sample (normal direction only) threw the horizon
    // light away — that is why shadowed ground went black. Lobe 0: sky
    // in the normal direction. Lobe 1: sky at the sunward horizon, whose
    // azimuth is the T1 sun's ground track (b_sunamt's constants).
    // Gains are set for 0.6 bar of silicate dust: multiple scattering is
    // generous; single-scatter would lie about this air.
    let f0r:f64 = b_sky(nx, ny, nz, 0);
    let f0g:f64 = b_sky(nx, ny, nz, 1);
    let f0b:f64 = b_sky(nx, ny, nz, 2);
    let f1r:f64 = b_sky(-0.628, 0.06, -0.778, 0);
    let f1g:f64 = b_sky(-0.628, 0.06, -0.778, 1);
    let f1b:f64 = b_sky(-0.628, 0.06, -0.778, 2);
    lr = lr + ar * (f0r * 0.40 + f1r * 0.60) * amb;
    lg = lg + ag * (f0g * 0.40 + f1g * 0.60) * amb;
    lb = lb + ab * (f0b * 0.40 + f1b * 0.60) * amb;""")

# ---- B-GLINT: microfacet fix — lobe fades with pixel footprint ----
rep("""    let sp:f64 = sp32 * sp16 * sp8 * sp4 * 0.12 * (1.0 - b_ss((slope - 0.15) / 0.3)) * sh;""",
"""    // R10 B-GLINT: microfacet honesty. A rough surface's specular
    // integrates over the pixel footprint: the lobe must weaken with
    // distance instead of firing on isolated pixels (the old sparkle
    // chains and waxy smears). Near-field volcanic glass still glints.
    let glintfade:f64 = 1.0 / (1.0 + t / 260.0);
    let sp:f64 = sp32 * sp16 * sp8 * sp4 * 0.10 * glintfade * (1.0 - b_ss((slope - 0.15) / 0.3)) * sh;""")

# ---- B-AERIAL: stronger scatter for the deliberated dust load ----
rep("""    // aerial perspective
    let f:f64 = 1.0 - b_expneg(t * 0.0011);""",
"""    // R10 B-AERIAL: exponential scatter at the deliberated dust load.
    // 0.6 bar of silicate dust scatters hard: far ranges pale toward
    // the azimuth-dependent horizon and lose contrast with distance.
    // The far plane dissolves instead of ending in a slab edge.
    let f:f64 = 1.0 - b_expneg(t * 0.0019);""")

# ---- B-MOON: planetshine to display-size legibility ----
rep("""    let r:f64 = alb * (1.0 * dif * 1.25 + 0.34);
    let g:f64 = alb * (0.66 * dif * 1.25 + 0.32);
    let b:f64 = alb * (0.42 * dif * 1.25 + 0.33);""",
"""    // R10 B-MOON (T14): planetshine raised to display-size legibility.
    // Earthshine is real; Cinder stays airless (T3) — no limb glow, the
    // terminator stays sharp, crater shading stays sun-consistent.
    let r:f64 = alb * (1.0 * dif * 1.25 + 0.52);
    let g:f64 = alb * (0.66 * dif * 1.25 + 0.50);
    let b:f64 = alb * (0.42 * dif * 1.25 + 0.51);""")

# ---- B-LAKE (T14): the graben floods ----
ins_before_line_containing(T7MARK, """// T14 — DELIBERATION (the trace judges itself again): the T13b taper
// flattened the far field into a dead gray band with a razor horizon
// edge — the single most 2000s-CG element in the frame. I reconceive
// it: the rift is a tectonic graben, and graben floors below the water
// table flood. Vesper's rift holds a still dark lake — a rift lake, the
// honest geology of a basaltic world (the East African Rift keeps
// Tanganyika the same way). The band becomes water: a real surface in
// the distance field, reflecting the deliberated sky dome (fresnel),
// carrying the sun-glitter path (wave normals toward the T1 sun — the
// path lands on the sun's azimuth by construction), with wave parallax
// (ripples resolve near, flatten far). It reaches the far plane fully
// fogged, so the horizon seam dissolves instead of cutting.
fn b_lakewl() f64 { return -9.0; }
fn b_lakemask(x:f64, z:f64, camx:f64, camz:f64) f64 {
    let dx:f64 = x - camx;
    let dz:f64 = z - camz;
    if (dx * dx + dz * dz < 129600.0) { return 0.0; }
    // NOTE: the tapered field (b_hfull), not raw b_hbase — the mask must
    // agree with the ground the SDF actually renders, or water and land
    // disagree in the far field (caught 2026-09-22: untapered mask left
    // the lake dry where the taper had pulled ground below WL).
    let h:f64 = b_hfull(x, z, camx, camz);
    return b_ss((b_lakewl() + 1.5 - h) / 3.0);
}
// water shading: sky reflection + fresnel + sun glitter + dust fog
fn b_wshade(px:f64, py:f64, pz:f64, vx:f64, vy:f64, vz:f64, t:f64, camx:f64, camz:f64, c0:f64, c1:f64, c2:f64, c3:f64, c4:f64, ch:i64) f64 {
    // wave normal: two deterministic scales; the fine ripple fades with
    // distance (parallax: near ripples resolve, far water mirrors).
    let wfade:f64 = 1.0 - b_ss((t - 120.0) / 700.0);
    let w1:f64 = b_vn2(px * 0.45 + 3.1, pz * 0.45 + 8.7, 951) - 0.5;
    let w2:f64 = b_vn2(px * 1.70 + 9.2, pz * 1.70 + 4.4, 952) - 0.5;
    let w3:f64 = b_vn2(px * 0.11 + 5.5, pz * 0.11 + 1.9, 953) - 0.5;
    let sl:f64 = 0.55 * wfade + 0.06;
    let nx:f64 = (w1 * 1.4 + w3 * 0.8) * sl;
    let nz:f64 = (w2 * 1.4 - w3 * 0.6) * sl;
    let ny:f64 = 1.0;
    let nl:f64 = b_sqrt(nx * nx + ny * ny + nz * nz);
    nx = nx / nl; ny = ny / nl; nz = nz / nl;
    // mirror the view ray in the wave normal: the sky it reflects
    let vdn:f64 = vx * nx + vy * ny + vz * nz;
    let rx:f64 = vx - 2.0 * vdn * nx;
    let ry:f64 = vy - 2.0 * vdn * ny;
    let rz:f64 = vz - 2.0 * vdn * nz;
    let skyc:f64 = b_sky(rx, ry, rz, ch);
    // fresnel: steep view sees the dark body; grazing view mirrors sky
    let cth:f64 = 0.0 - vdn;
    if (cth < 0.0) { cth = 0.0; }
    if (cth > 1.0) { cth = 1.0; }
    let fr:f64 = 1.0 - cth;
    let fr2:f64 = fr * fr;
    let fr5:f64 = fr2 * fr2 * fr;
    let frsn:f64 = 0.02 + 0.98 * fr5;
    let body:f64 = 0.020;
    if (ch == 1) { body = 0.034; }
    if (ch == 2) { body = 0.048; }
    // sun glitter: half-vector lobe toward the deliberated T1 sun,
    // shadow-marched like everything else (one sun, one field).
    let sx:f64 = b_sunx();
    let sy:f64 = b_suny();
    let sz:f64 = b_sunz();
    let hx:f64 = sx - vx;
    let hy:f64 = sy - vy;
    let hz:f64 = sz - vz;
    let hl:f64 = b_sqrt(hx * hx + hy * hy + hz * hz);
    hx = hx / hl; hy = hy / hl; hz = hz / hl;
    let dh:f64 = nx * hx + ny * hy + nz * hz;
    if (dh < 0.0) { dh = 0.0; }
    let g2:f64 = dh * dh;
    let g4:f64 = g2 * g2;
    let g8:f64 = g4 * g4;
    let g16:f64 = g8 * g8;
    let g32:f64 = g16 * g16;
    let sh:f64 = b_shadow(px, py, pz, nx, ny, nz, camx, camz, c0, c1, c2, c3, c4);
    let glit:f64 = g32 * g16 * 2.6 * sh;
    let sheen:f64 = g8 * 0.10 * sh;
    let scol:f64 = b_sunc(ch);
    let col:f64 = body * (1.0 - frsn) + skyc * frsn + (glit + sheen) * scol;
    // R10 B-AERIAL (shared fog, same pass as terrain): the far lake must
    // dissolve into the horizon sky exactly as far ground does. b_render
    // applies no fog of its own, so this IS the single shared pass —
    // identical formula to b_tshade (same t, same azimuth-dependent
    // horizon target). (2026-09-22 repair: the pre-render source fogged
    // only inside b_tshade, leaving water unfogged to the far plane.)
    let wf:f64 = 1.0 - b_expneg(t * 0.0019);
    let wsun:f64 = b_sunamt(vx, vz);
    if (ch == 0) { col = b_mix(col, b_mix(0.45, 0.85, wsun), wf); }
    if (ch == 1) { col = b_mix(col, b_mix(0.32, 0.45, wsun), wf); }
    if (ch == 2) { col = b_mix(col, b_mix(0.44, 0.28, wsun), wf); }
    return col;
}""")
# lake plane in both SDFs (after the pebble hook)
rep("""    if (d < 6.0) {
        let pd:f64 = b_pebd(px, py, pz, d, camx, camz);
        if (pd < d) { d = pd; }
    }
    return d;
}""",
"""    if (d < 6.0) {
        let pd:f64 = b_pebd(px, py, pz, d, camx, camz);
        if (pd < d) { d = pd; }
    }
    if (py < 25.0) {
        let wlm:f64 = b_lakemask(px, pz, camx, camz);
        if (wlm > 0.5) {
            let wd:f64 = py - b_lakewl();
            if (wd < d) { d = wd; }
        }
    }
    return d;
}""", count=2)
# render dispatch: water-aware shading
rep("""                let ao:f64 = b_aocc(px, py, pz, nx, ny, nz, cox, coz, c0, c1, c2, c3, c4);
                cr = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 0);
                cg = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 1);
                cb = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 2);""",
"""                let ao:f64 = b_aocc(px, py, pz, nx, ny, nz, cox, coz, c0, c1, c2, c3, c4);
                // R10: water-aware dispatch — the hit is water where the
                // lake mask holds at the water level; the shoreline blends.
                let wwm:f64 = b_lakemask(px, pz, cox, coz) * (1.0 - b_ss(b_abs(py - b_lakewl()) / 3.0));
                if (wwm < 0.002) {
                    cr = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 0);
                    cg = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 1);
                    cb = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 2);
                } else {
                    let wr:f64 = b_wshade(px, py, pz, rdx, rdy, rdz, t, cox, coz, c0, c1, c2, c3, c4, 0);
                    let wg:f64 = b_wshade(px, py, pz, rdx, rdy, rdz, t, cox, coz, c0, c1, c2, c3, c4, 1);
                    let wb:f64 = b_wshade(px, py, pz, rdx, rdy, rdz, t, cox, coz, c0, c1, c2, c3, c4, 2);
                    if (wwm > 0.998) {
                        cr = wr; cg = wg; cb = wb;
                    } else {
                        let tr:f64 = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 0);
                        let tg:f64 = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 1);
                        let tb:f64 = b_tshade(px, py, pz, nx, ny, nz, t, rdx, rdy, rdz, ao, cox, coz, c0, c1, c2, c3, c4, 2);
                        cr = b_mix(tr, wr, wwm);
                        cg = b_mix(tg, wg, wwm);
                        cb = b_mix(tb, wb, wwm);
                    }
                }""")

if DEBUGMASK:
    # debug: visualize the lake mask (red) and hit height vs WL (green).
    # Both shading branches must be dead or they overwrite the debug color.
    rep("""                let wwm:f64 = b_lakemask(px, pz, cox, coz) * (1.0 - b_ss(b_abs(py - b_lakewl()) / 3.0));
                if (wwm < 0.002) {""",
        """                let wwm:f64 = b_lakemask(px, pz, cox, coz) * (1.0 - b_ss(b_abs(py - b_lakewl()) / 3.0));
                cr = wwm; cg = b_clamp((py - b_lakewl()) / 30.0 + 0.5, 0.0, 1.0); cb = 0.0;
                if (0 == 1) {""")
    rep("""                } else {
                    let wr:f64 = b_wshade(""",
        """                } else if (0 == 1) {
                    let wr:f64 = b_wshade(""")

# ---------- output names ----------
rep('    let name:[]u8 = "r8b_alien_1024.bmp";', '    let name:[]u8 = "r10_beauty_1024.bmp";')
rep('if (_zag_strcmp(szs, "256") == 1) { name = "r8b_alien_256.bmp"; }',
    'if (_zag_strcmp(szs, "256") == 1) { name = "r10_beauty_256.bmp"; }')
rep('if (_zag_strcmp(szs, "2048") == 1) { name = "r8b_alien_2048.bmp"; }',
    'if (_zag_strcmp(szs, "2048") == 1) { name = "r10_beauty_2048.bmp"; }')
if CROP:
    rep('    let name:[]u8 = "r10_beauty_1024.bmp";',
        f'    let name:[]u8 = "r10_crop_{CX0}_{CY0}.bmp";')
    if DEBUGMASK:
        rep(f'    let name:[]u8 = "r10_crop_{CX0}_{CY0}.bmp";',
            f'    let name:[]u8 = "r10_debugmask_{CX0}_{CY0}.bmp";')
    rep("""    let w:i64 = 1024;
    let h:i64 = 1024;
    if (_zag_strcmp(szs, "256") == 1) { w = 256; h = 256; }
    if (_zag_strcmp(szs, "2048") == 1) { w = 2048; h = 2048; }""",
        """    let w:i64 = 256;
    let h:i64 = 256;""")

# ---------- sun-accessor integrity: T1 block must be byte-identical ----------
new_sun_block = src[src.index("// T1"):src.index("// T2")]
assert new_sun_block == orig_sun_block, "SUN BLOCK CHANGED — abort"
# ---------- banned-token audit (D-COMP) on executable code ----------
BANNED = [r'\brect\b', r'\bband\b', r'\bblotch\b', r'\bfill_rect\b',
          r'\bfill\b', r'\bstroke\b', r'\bcircle\b', r'\bellipse\b']
for ln, line in enumerate(src.split("\n"), 1):
    code = line.split("//")[0]
    for pat in BANNED:
        assert not re.search(pat, code), f"D-COMP FAIL {OUTNAME}:{ln} [{pat}] {line.strip()[:70]}"

outpath = f"{R10SRC}/{OUTNAME}"
open(outpath, "w").write(src)
print("wrote", outpath, "sun-ok")
