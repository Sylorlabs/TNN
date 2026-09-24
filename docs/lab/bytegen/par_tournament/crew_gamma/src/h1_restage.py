#!/usr/bin/env python3
"""CREW GAMMA H1 — re-stage fixture plan energies for the gain-1 world.

Rewrites every authored energy literal E in f3_gen_song / f3_gen_mood as
(E*32767/B) with the fixture's authored polyphony bound B (from h1_census.py,
mechanical voice census of the generator source — no render measured):

  song  B=420743 | happy B=503783 | scary B=285954 | calm B=61240

This is a PLAN-AUTHORING rule: uniform per-fixture headroom, baked into the
fixture generators. Inter-voice ratios are preserved (uniform scale, up to
integer rounding); |mix| <= 32767 by the triangle inequality -> 0% at rail
by construction.
"""
import re, sys

SRC, DST = sys.argv[1], sys.argv[2]
BOUNDS = {"song": 420743, "happy": 503783, "scary": 285954, "calm": 61240}
# energy arg index (after stripping `ar,`): tone/harm e=3, sweep e=4, noise e=2
EIDX = {"tone": 3, "harm": 3, "sweep": 4, "noise": 2}
CALL = re.compile(r"^(\s*)f3_(tone|harm|sweep|noise)\(ar,(.*)\);\s*$")

with open(SRC) as f:
    lines = f.readlines()

def fn_range(name):
    start = next(i for i, l in enumerate(lines) if l.startswith("fn %s(" % name))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].rstrip() == "}")
    return start, end

s_lo, s_hi = fn_range("f3_gen_song")
m_lo, m_hi = fn_range("f3_gen_mood")

# mood block line ranges inside f3_gen_mood
happy_lo = next(i for i in range(m_lo, m_hi) if lines[i].strip() == "if (mood == 0) {") + 1
scary_kw = next(i for i in range(m_lo, m_hi) if lines[i].strip() == "if (mood == 1) {")
happy_hi = scary_kw - 1
scary_lo = scary_kw + 1
scary_ret = next(i for i in range(scary_lo, m_hi)
                 if lines[i].strip() == "return;")
scary_hi = scary_ret - 1
calm_lo = scary_ret + 1
calm_hi = m_hi

RANGES = [("song", s_lo, s_hi), ("happy", happy_lo, happy_hi),
          ("scary", scary_lo, scary_hi), ("calm", calm_lo, calm_hi)]

HDR = ("    // H1 (CREW GAMMA): authored uniform headroom for the gain-1 world.\n"
       "    // Every energy below is authored as e*32767/%d: 32767/B with B the\n"
       "    // plan-authored polyphony bound (mechanical voice census of this\n"
       "    // generator, h1_census.py). |mix| <= 32767 by the triangle\n"
       "    // inequality -> 0%% at rail by construction. No render measured.\n")

def scale_line(line, num, den):
    m = CALL.match(line.rstrip("\n"))
    if not m:
        return line, False
    indent, prim, argstr = m.group(1), m.group(2), m.group(3)
    args = [a.strip() for a in argstr.split(",")]
    ei = EIDX[prim]
    assert re.fullmatch(r"\d+", args[ei]), "non-literal energy: %s" % line
    args[ei] = "(%s*%d/%d)" % (args[ei], num, den)
    return "%sf3_%s(ar, %s);\n" % (indent, prim, ", ".join(args)), True

out = list(lines)
n_changed = 0
# apply from last range to first so line numbers stay valid; insert headers after
for name, lo, hi in sorted(RANGES, key=lambda r: -r[1]):
    B = BOUNDS[name]
    changed = 0
    for i in range(lo, hi + 1):
        nl, hit = scale_line(out[i], 32767, B)
        if hit:
            out[i] = nl
            changed += 1
    # insert header after the generator's opening lines:
    # for song: after 'fn ... {' line (lo is the fn line); find first non-empty
    # body line. Simplest: insert at lo+1 for song; for moods insert at block start.
    hdr_at = lo + 1 if name == "song" else lo
    out.insert(hdr_at, HDR % B)
    print("%-5s: %d energy args re-staged (B=%d)" % (name, changed, B))
    n_changed += changed

with open(DST, "w") as f:
    f.writelines(out)
print("total re-staged:", n_changed, "->", DST)
