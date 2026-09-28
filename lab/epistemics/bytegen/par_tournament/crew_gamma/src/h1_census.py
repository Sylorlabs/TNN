#!/usr/bin/env python3
"""CREW GAMMA H1 — mechanical voice census from the fixture generator source.

Parses f3_gen_song / f3_gen_mood in a field.zag copy, unrolls the literal
k-loops, and computes the plan-authored worst-case mix bound:

  B = max over frames of sum over voices active in that frame of
      e * 28 * S(br)

where S(br) = sum_{h=1..8} w_h/1000, w_h = 1000/h^d, d = 4-(br/100)*3/10
(the hifi synth's brightness table), per-voice |sample| <= e*28*S because
|j2_get16| <= 32767 and ew = es*28*w/1000 with es <= authored e.

H1 re-staging rule: scale every authored energy in the fixture by
32767/B (exact rational, integer math e*32767/B). By the triangle
inequality |mix| <= 32767 on every sample -> 0% at rail, by construction.
No render is measured; B comes from the authored voice list only.
(Conservative: same-bin voices take max via f3_amax but are summed here;
phases are assumed worst-aligned.)
"""
import re, sys

SRC = sys.argv[1]

def S_of_br(br):
    q = br // 100
    q = max(0, min(10, q))
    d = 4 - q * 3 // 10
    return sum(1000.0 / (h ** d) for h in range(1, 9)) / 1000.0

def eval_expr(expr, k):
    return eval(expr.replace("k", str(k)), {"__builtins__": {}}, {})

with open(SRC) as f:
    lines = f.readlines()

def fn_range(name):
    start = next(i for i, l in enumerate(lines) if l.startswith("fn %s(" % name))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].rstrip() == "}")
    return start, end

CALL = re.compile(r"f3_(tone|harm|sweep|noise)\(ar,\s*(.*)\)\s*;")
voices = []  # (fixture, prim, args-as-strings)

def parse_range(lo, hi, fixture):
    i = lo
    while i <= hi:
        line = lines[i].strip()
        # literal k loop: let k:i64 = 0;  while (k < N) { ... k = k + 1; }
        mk = re.match(r"let (\w+):i64 = 0;", line)
        if mk and re.match(r"while \(%s < (\d+)\) \{" % mk.group(1),
                           lines[i + 1].strip() if i + 1 <= hi else ""):
            var = mk.group(1)
            n = int(re.match(r"while \(%s < (\d+)\) \{" % var,
                             lines[i + 1].strip()).group(1))
            j = i + 2
            body = []
            while not re.match(r"%s = %s \+ 1;" % (var, var), lines[j].strip()):
                body.append(lines[j])
                j += 1
            for kk in range(n):
                for bl in body:
                    cm = CALL.match(bl.strip())
                    if cm:
                        args = [str(eval_expr(a, kk))
                                for a in cm.group(2).split(",")]
                        voices.append((fixture, cm.group(1), args))
            i = j + 1
            continue
        cm = CALL.match(line)
        if cm:
            args = [a.strip() for a in cm.group(2).split(",")]
            voices.append((fixture, cm.group(1), args))
        i += 1

s_lo, s_hi = fn_range("f3_gen_song")
m_lo, m_hi = fn_range("f3_gen_mood")
parse_range(s_lo, s_hi, "song")
# mood blocks: 'if (mood == 0) {' ... 'return;' | 'if (mood == 1) {' ... 'return;' | rest
bounds = []
cur = None
start = m_lo
for i in range(m_lo, m_hi + 1):
    s = lines[i].strip()
    if s == "if (mood == 0) {":
        bounds.append(("happy", i + 1, None)); cur = 0
    elif s == "if (mood == 1) {":
        bounds[-1] = ("happy", bounds[-1][1], i - 1)
        bounds.append(("scary", i + 1, None)); cur = 1
    elif s == "return;" and cur == 1:
        bounds[-1] = ("scary", bounds[-1][1], i - 1)
        bounds.append(("calm", i + 1, m_hi)); cur = None
for name, lo, hi in bounds:
    parse_range(lo, hi, name)

def voice_frame_bound(prim, args):
    # args exclude the leading `ar,`:
    # tone/harm: fbin,t0,t1,e,atk,dec,br | sweep: f0,f1,t0,t1,e,br | noise: t0,t1,e,br
    if prim in ("tone", "harm"):
        e, br = int(args[3]), int(args[6])
        S = S_of_br(br)
        parts = [e] if prim == "tone" else [e, e * 6 // 10, e * 4 // 10]
        return sum(p * 28 * S for p in parts)
    if prim == "sweep":
        e, br = int(args[4]), int(args[5])
        return 3 * e * 28 * S_of_br(br)
    if prim == "noise":
        e, br = int(args[2]), int(args[3])
        return 48 * e * 28 * S_of_br(br)
    raise ValueError(prim)

def active_frames(prim, args):
    if prim in ("tone", "harm"):
        return range(int(args[1]), int(args[2]) + 1)
    if prim == "sweep":
        return range(int(args[2]), int(args[3]) + 1)
    if prim == "noise":
        return range(int(args[0]), int(args[1]) + 1)

for fx in ["song", "happy", "scary", "calm"]:
    frame = {}
    nv = 0
    for (name, prim, args) in voices:
        if name != fx:
            continue
        nv += 1
        b = voice_frame_bound(prim, args)
        for t in active_frames(prim, args):
            frame[t] = frame.get(t, 0.0) + b
    B = max(frame.values())
    tmax = max(t for t, v in frame.items() if v == B)
    print("%-5s voices=%2d B=%7.0f worst_frame=%2d  scale=32767/%d = %.6f" %
          (fx, nv, B, tmax, round(B), 32767.0 / B))
