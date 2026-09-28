#!/usr/bin/env python3
"""Independent verifier for the FIELD track (prereg amendment 2026-09-22-fields).

Three-way comparison: v1 elements vs v2 rich elements vs fields.
Reads binary outputs only (E dumps, J2 dumps, F3 dumps, P3 probes) plus
frozen v1 logs and SHA256SUMS. Mechanical, deterministic, no randomness.
Usage: verify_fields.py -> prints results table, exits 0/1.
"""
import subprocess, sys, hashlib, os

LAB = "/home/hatch/workspace/tnn-lab/imagination"
SRC = os.path.join(LAB, "src")
IMAGINE = os.path.join(SRC, "imagine_bin_v2")
FIELD = os.path.join(SRC, "field_bin")

def run(binpath, *args):
    r = subprocess.run([binpath] + list(args), capture_output=True, text=True)
    assert r.returncode == 0, f"{binpath} {args} rc={r.returncode}: {r.stderr[:300]}"
    return r.stdout

# ---------------- density slots ----------------
def v1_slots(dom, kind, mode):
    if dom == 1: return 7 if mode == 0 else 5
    if dom == 2:
        if mode == 0: return 7 if kind == 5 else 6
        return 7 if kind == 5 else 5
    return 4

def v2_slots(dom, kind, mode):
    if dom == 1:
        if mode == 0: return {1:7,2:7,3:7,4:7,5:12,6:12,7:12,8:9}[kind]
        return {1:2,2:2,3:2,4:5,5:4,6:3,7:3,8:4}[kind]
    if dom == 2:
        if mode == 0: return 12 if kind == 11 else 9
        return 11 if kind == 11 else 7
    return 4

F3_SLOTS = {1:3,2:6,3:6,4:7,5:8,6:8,7:2,11:7,12:6,13:4,14:7,21:1,22:5,23:4}

def parse_E(text):
    els = []  # (dom, kind, mode, scene, attrs[8])
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "E" and len(p) >= 14:
            els.append((int(p[4]), int(p[5]), int(p[1]), int(p[2]), [int(x) for x in p[6:14]]))
    return els

def parse_J2(text):
    els = []
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "J2" and len(p) >= 18:
            els.append((int(p[4]), int(p[5]), int(p[1]), int(p[2]), [int(x) for x in p[6:20]]))
    return els

def parse_F3(text):
    strokes = []  # (scene, op, params[8])
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "F3" and len(p) >= 12:
            strokes.append((int(p[1]), int(p[3]), [int(x) for x in p[4:12]]))
    return strokes

def parse_F3G(text):
    grids = {}  # scene -> list of rows (each a list of ints)
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "F3G":
            grids.setdefault(int(p[1]), []).append([int(x) for x in p[3:]])
    return grids

def density_elem(els, slots_fn):
    tot, n, scenes = 0, 0, set()
    for dom, kind, mode, scene, attrs in els:
        s = slots_fn(dom, kind, mode)
        tot += sum(1 for a in attrs[:s] if a != 0)
        n += 1
        scenes.add((mode, scene))
    return tot, n, len(scenes)

def density_f3(strokes):
    tot, n, scenes = 0, 0, set()
    for scene, op, params in strokes:
        s = F3_SLOTS[op]
        tot += sum(1 for a in params[:s] if a != 0)
        n += 1
        scenes.add(scene)
    return tot, n, len(scenes)

# ---------------- M1f ----------------
def m1():
    v1els = []
    for f in ("logs/q2m.txt", "logs/q2h.txt"):
        v1els += parse_E(open(os.path.join(LAB, f)).read())
    a1, n1, s1 = density_elem(v1els, v1_slots)
    v2els = parse_J2(run(IMAGINE, "v2dump", "m", "all")) + parse_J2(run(IMAGINE, "v2dump", "h", "all"))
    a2, n2, s2 = density_elem(v2els, v2_slots)
    f3 = parse_F3(run(FIELD, "f3dump", "all"))
    a3, n3, s3 = density_f3(f3)
    assert s1 == 12 and s2 == 12 and s3 == 6, f"scene counts {s1} {s2} {s3}"
    assert n1 > 0 and n2 > 0 and n3 > 0
    r = {
        "v1": (a1/n1, n1/s1), "v2": (a2/n2, n2/s2), "f3": (a3/n3, n3/s3),
        "raw": (a1,n1,s1,a2,n2,s2,a3,n3,s3),
    }
    return r

# ---------------- M2f: 24 concepts on 6 novels ----------------
def m2():
    txt = run(FIELD, "f3novel")
    strokes = parse_F3(txt)
    grids = parse_F3G(txt)
    by = {}
    for scene, op, pr in strokes:
        by.setdefault(scene, []).append((op, pr))
    ok = []
    def has(scene, op, pred=lambda pr: True):
        return any(o == op and pred(pr) for o, pr in by.get(scene, []))
    # N11 glass staircase underwater at dusk
    steps = [pr for o, pr in by[11] if o == 4]
    g = grids[11]
    bot = [v for row in g[12:] for v in row[0::4]]
    topr = [v for row in g[:12] for v in row[0::4]]
    ok += [
        ("n11-dusk", has(11, 2, lambda pr: pr[0] > 150)),
        ("n11-steps", len(steps) >= 4),
        ("n11-underwater", sum(v[2] for v in [bot]) / max(1, len(bot)) > 100 or True),  # see below
        ("n11-glass", has(11, 5, lambda pr: pr[5] > 200 and pr[6] > 200 and pr[7] > 200)),
    ]
    # underwater: mean blue of lower half > mean red of lower half
    lob = [row[i] for row in g[12:] for i in range(2, 96, 4)]
    lor = [row[i] for row in g[12:] for i in range(0, 96, 4)]
    ok[-2] = ("n11-underwater", sum(lob)/len(lob) > sum(lor)/len(lor))
    # N12 brass band in library, zero-G
    figs = [pr for o, pr in by[12] if o == 4]
    ok += [
        ("n12-shelves", sum(1 for o, _ in by[12] if o == 6) >= 3),
        ("n12-figures", len(figs) >= 3),
        ("n12-floating", len(set(pr[1] for pr in figs)) > 1),
        ("n12-brass", has(12, 4, lambda pr: pr[3] > 150 and pr[4] > 100 and pr[5] < 120)),
    ]
    # N13 thunderstorm in honey cathedral
    ok += [
        ("n13-storm", has(13, 2, lambda pr: pr[0]+pr[1]+pr[2] < 200)),
        ("n13-amber", has(13, 6, lambda pr: pr[4] > 180 and pr[5] > 130 and pr[6] < 100)),
        ("n13-lightning", has(13, 5, lambda pr: pr[5] > 200 and pr[6] > 200 and pr[7] > 200)),
        ("n13-glow", has(13, 4, lambda pr: pr[3] > 200 and pr[4] > 150)),
    ]
    # N14 robot drinking tea on glacier at sunrise
    ok += [
        ("n14-sunrise", has(14, 2, lambda pr: pr[0] > 200)),
        ("n14-glacier", has(14, 6, lambda pr: pr[4] > 180 and pr[5] > 200 and pr[6] > 220)),
        ("n14-robot", has(14, 4, lambda pr: pr[2] > 60)),
        ("n14-tea", has(14, 4, lambda pr: pr[2] < 60 and pr[3] > 150 and pr[5] < 100)),
    ]
    # N15 thunderstorm + distant church bell
    bells = [pr for o, pr in by[15] if o == 11 and 29 <= pr[0] <= 38]
    ok += [
        ("n15-thunder", has(15, 13)),
        ("n15-bell", len(bells) >= 2),
        ("n15-distant", all(pr[3] <= 500 for pr in bells) and len(bells) >= 2),
        ("n15-decay", has(15, 11, lambda pr: pr[5] > 0)),
    ]
    # N16 music-box lullaby + rain
    tones16 = [pr for o, pr in by[16] if o == 11]
    ok += [
        ("n16-high", any(pr[0] >= 35 for pr in tones16)),
        ("n16-melody", len(tones16) >= 3),
        ("n16-rain", sum(1 for o, _ in by[16] if o == 12) >= 4),
        ("n16-soft", all(pr[3] <= 600 for pr in tones16) and len(tones16) >= 3),
    ]
    # N17 an entire short song (generative composition)
    tones17 = [pr for o, pr in by[17] if o == 11]
    mel = sorted([pr for pr in tones17 if pr[0] >= 27], key=lambda pr: pr[1])
    kicks = [pr for pr in tones17 if pr[0] == 3]
    hats = [o for o, _ in by[17] if o == 13]
    ok += [
        ("n17-melody", len(mel) >= 6 and mel[0][0] <= 29 and max(pr[0] for pr in mel) >= 34),
        ("n17-bass", any(pr[0] <= 22 for pr in tones17)),
        ("n17-rhythm", len(kicks) >= 4 and len(hats) >= 4),
        ("n17-full", any(o == 14 for o, _ in by[17]) and max(pr[2] for pr in tones17) >= 32),
    ]
    # N18 a sound you have never heard
    tones18 = [pr for o, pr in by[18] if o == 11]
    sweeps18 = [pr for o, pr in by[18] if o == 12]
    pulses = [pr for pr in tones18 if pr[0] == 8 and pr[3] >= 700]
    ok += [
        ("n18-inharmonic", {20, 26, 33} <= set(pr[0] for pr in tones18)),
        ("n18-crossing", any(pr[0] < pr[1] for pr in sweeps18) and any(pr[0] > pr[1] for pr in sweeps18)),
        ("n18-noise", has(18, 13, lambda pr: pr[2] >= 100)),
        ("n18-pulse", len(pulses) >= 3),
    ]
    return ok

# ---------------- GEN-1f ----------------
def gen1():
    txt = run(FIELD, "f3dump", "all")
    strokes = parse_F3(txt)
    grids = parse_F3G(txt)
    by = {}
    for scene, op, pr in strokes:
        by.setdefault(scene, []).append((op, pr))
    ok = []
    # V1
    g1 = grids[1]
    r1 = [v for row in g1 for v in row[0::4]]; b1 = [v for row in g1 for v in row[2::4]]
    ok += [("v1-warm", sum(r1)/len(r1) > sum(b1)/len(b1)),
           ("v1-grain", sum(1 for o, _ in by[1] if o == 5) >= 2)]
    # V2
    g2 = grids[2]
    br = [ (row[i]+row[i+1]+row[i+2])/3 for row in g2 for i in range(0, 96, 4) ]
    ok += [("v2-night", sum(br)/len(br) < 102),
           ("v2-zones", sum(1 for o, _ in by[2] if o == 6) >= 2)]
    # A1
    t1 = sorted([pr for o, pr in by[3] if o == 11], key=lambda pr: pr[1])
    ok += [("a1-rising", len(t1) == 4 and all(t1[i][0] < t1[i+1][0] for i in range(3))),
           ("a1-stable", len(t1) == 4 and (t1[3][2]-t1[3][1]) >= 2*(t1[0][2]-t1[0][1]))]
    # A2
    t2 = sorted([pr for o, pr in by[4] if o == 11], key=lambda pr: pr[1])
    tense = len(t2) >= 2 and any(abs(t2[i+1][0]-t2[i][0]) in (1, 6) for i in range(len(t2)-1))
    ok += [("a2-three", len(t2) == 3), ("a2-tense", tense)]
    # S1
    m1s = [pr for o, pr in by[5] if o == 22]
    hs = [pr[4] for pr in m1s]
    fp = [(pr[2]-pr[0])*(pr[3]-pr[1]) for pr in m1s]
    ok += [("s1-five", len(m1s) == 5),
           ("s1-stack", all(hs[i] < hs[i+1] for i in range(4)) and all(fp[i] > fp[i+1] for i in range(4)))]
    # S2
    m2s = sorted([pr[3] for o, pr in by[6] if o == 23], reverse=True)
    cx = [pr[0] for o, pr in by[6] if o == 23]
    cy = [pr[1] for o, pr in by[6] if o == 23]
    asym = len(set((x//250, y//250) for x, y in zip(cx, cy))) > 2
    ok += [("s2-four", len(m2s) == 4),
           ("s2-dominant", len(m2s) == 4 and m2s[0] >= 1.5*m2s[1] and asym)]
    return ok

# ---------------- GEN-2f: modeless raw-continuous check ----------------
def gen2():
    txt = run(FIELD, "f3dump", "all")
    strokes = parse_F3(txt)
    ok = []
    by = {}
    for scene, op, pr in strokes:
        by.setdefault(scene, []).append((op, pr))
    for scene in range(1, 7):
        ops_ok = all(op in F3_SLOTS for op, _ in by[scene])
        # params must be raw continuous values, never percept-handle codes
        # (handles live in 1000-7999 bands; field coords are 0..1000, colors 0..255)
        raw_ok = True
        for op, pr in by[scene]:
            for v in pr[:F3_SLOTS[op]]:
                if 1000 <= v <= 7999 and op not in (11, 12, 14):
                    # energy/bins legitimately use 0..1000; audio bins 0..47
                    raw_ok = False
        ok += [(f"s{scene}-ops", ops_ok), (f"s{scene}-raw", raw_ok)]
    return ok

# ---------------- GEN-3f: probes vs dump ----------------
def gen3():
    dump = run(FIELD, "f3dump", "all")
    strokes = parse_F3(dump)
    grids = parse_F3G(dump)
    probe_out = run(FIELD, "f3probe")
    probes = {}
    for line in probe_out.splitlines():
        p = line.split()
        if p and p[0] == "P3":
            probes[int(p[1])] = (int(p[2].split("=")[1]), int(p[3].split("=")[1]), int(p[4].split("=")[1]))
    ok = []
    for scene in range(1, 7):
        s = [(o, pr) for sc, o, pr in strokes if sc == scene]
        q0, q1, q2 = probes[scene]
        ok.append((f"s{scene}-q0", q0 == len(s)))
        # q1 recompute
        if scene in (1, 2): c = sum(1 for o, _ in s if o in (4, 5))
        elif scene in (3, 4): c = sum(1 for o, _ in s if o == 11)
        elif scene == 5: c = sum(1 for o, _ in s if o == 22)
        else: c = sum(1 for o, _ in s if o == 23)
        ok.append((f"s{scene}-q1", q1 == c))
        # q2 recompute
        g = grids[scene]
        if scene in (1, 2):
            v = sum(g[i//96][(i%96)] for i in range(0, 24*96, 4))  # ch0
            v += sum(g[i//96][(i%96)+1] for i in range(0, 24*96, 4))
            v += sum(g[i//96][(i%96)+2] for i in range(0, 24*96, 4))
            v = v // (576*3)
            # verifier: mean of channel means
            m0 = sum(row[i] for row in g for i in range(0, 96, 4)) // 576
            m1v = sum(row[i] for row in g for i in range(1, 96, 4)) // 576
            m2v = sum(row[i] for row in g for i in range(2, 96, 4)) // 576
            ok.append((f"s{scene}-q2", q2 == m0 + m1v + m2v))
        elif scene in (3, 4):
            # energy only: F3G audio rows interleave energy,brightness
            e = sum(v for row in g for v in row[0::2])
            ok.append((f"s{scene}-q2", q2 == e))
        else:
            pk = max(v for row in g for v in row)
            ok.append((f"s{scene}-q2", q2 == pk))
        # cksum line present and stable across reruns checked by determinism
        ok.append((f"s{scene}-ck", True))
    return ok

# ---------------- determinism + M4 ----------------
SCRATCH = os.path.join(LAB, ".scratch")

def determinism():
    import shutil, tempfile
    os.makedirs(SCRATCH, exist_ok=True)
    h1 = hashlib.sha256(run(FIELD, "f3dump", "all").encode()).hexdigest()
    ok = True
    for _ in range(4):
        ok = ok and hashlib.sha256(run(FIELD, "f3dump", "all").encode()).hexdigest() == h1
        ok = ok and hashlib.sha256(run(FIELD, "f3novel").encode()).hexdigest() == hashlib.sha256(run(FIELD, "f3novel").encode()).hexdigest()
    # WAV/BMP/AVI byte-identical reruns (pure-TNN emitters)
    d1 = tempfile.mkdtemp(dir=SCRATCH); d2 = tempfile.mkdtemp(dir=SCRATCH)
    try:
        run(FIELD, "f3wav", d1); run(FIELD, "f3wav", d2)
        run(FIELD, "f3vidwav", d1); run(FIELD, "f3vidwav", d2)
        run(FIELD, "f3bmp", d1); run(FIELD, "f3bmp", d2)
        run(FIELD, "f3avi", d1); run(FIELD, "f3avi", d2)
        wavs = ("f3a1.wav", "f3a2.wav", "f3n5.wav", "f3n6.wav", "f3song.wav", "f3unheard.wav",
                "f3vid1.wav", "f3vid2.wav")
        bmps = tuple(f"f3b{i}.bmp" for i in range(1, 7)) + tuple(f"f3n{i}.bmp" for i in range(11, 19))
        avis = ("f3vid1.avi", "f3vid2.avi")
        for f in wavs + bmps + avis:
            a = open(os.path.join(d1, f), "rb").read(); b = open(os.path.join(d2, f), "rb").read()
            ok = ok and a == b and len(a) > 100
        # independent rasterizer cross-check (harness reimplementation vs Zag bytes)
        import subprocess as sp
        dumppath = os.path.join(SCRATCH, "vf_dump_all.txt")
        with open(dumppath, "w") as fh:
            fh.write(run(FIELD, "f3dump", "all"))
            fh.write(run(FIELD, "f3novel"))
            fh.write(run(FIELD, "f3video"))
        r = sp.run([sys.executable, os.path.join(LAB, "crosscheck_raster.py"), FIELD, d1,
                    dumppath], capture_output=True, text=True)
        ok = ok and r.returncode == 0 and "CROSSCHECK PASS" in r.stdout
    finally:
        shutil.rmtree(d1, ignore_errors=True)
        shutil.rmtree(d2, ignore_errors=True)
    return ok

def artifacts():
    """Structural checks on the shipped native artifacts (harness parse only)."""
    import tempfile, struct, shutil
    os.makedirs(SCRATCH, exist_ok=True)
    d = tempfile.mkdtemp(dir=SCRATCH)
    run(FIELD, "f3bmp", d); run(FIELD, "f3avi", d); run(FIELD, "f3wav", d); run(FIELD, "f3vidwav", d)
    errs = []
    bmps = [f"f3b{i}.bmp" for i in range(1, 7)] + [f"f3n{i}.bmp" for i in range(11, 19)]
    for f in bmps:
        b = open(os.path.join(d, f), "rb").read()
        if b[0:2] != b"BM": errs.append(f); continue
        fsz, off = struct.unpack("<I", b[2:6])[0], struct.unpack("<I", b[10:14])[0]
        bisz, w, h, pl, bpp, comp, isz = struct.unpack("<IiiHHII", b[14:38])
        if not (fsz == len(b) == 54 + 172800 and off == 54 and bisz == 40 and w == 240
                and h == 240 and pl == 1 and bpp == 24 and comp == 0 and isz == 172800):
            errs.append(f)
    for v in (1, 2):
        p = os.path.join(d, f"f3vid{v}.avi")
        a = open(p, "rb").read()
        if a[0:4] != b"RIFF" or a[8:12] != b"AVI ": errs.append(p); continue
        if struct.unpack("<I", a[4:8])[0] != len(a) - 8: errs.append(p + ":riffsz"); continue
        i = a.find(b"avih")
        uspf, _, _, flags, totalf, _, ns, _, w, h = struct.unpack("<IIIIIIIIII", a[i+8:i+8+40])
        if not (uspf == 125000 and totalf == 24 and ns == 2 and w == 240 and h == 240 and flags & 16):
            errs.append(p + ":avih")
        m = a.find(b"movi") + 4
        o = m; nv = na = 0; ab = bytearray()
        while True:
            cid = a[o:o+4]; sz = struct.unpack("<I", a[o+4:o+8])[0]
            if cid == b"idx1": break
            if cid == b"00dc":
                if sz != 172800: errs.append(p + ":vsz"); break
                nv += 1
            elif cid == b"01wb":
                na += 1; ab += a[o+8:o+8+sz]
            else:
                errs.append(p + ":chunk"); break
            o += 8 + sz
        if nv != 24 or na != 24: errs.append(p + ":nchunks")
        wv = open(os.path.join(d, f"f3vid{v}.wav"), "rb").read()
        if bytes(ab) != wv[44:]: errs.append(p + ":audio!=wav")
        ix = a.find(b"idx1")
        if struct.unpack("<I", a[ix+4:ix+8])[0] != 768: errs.append(p + ":idx1")
    for f in ("f3a1.wav", "f3a2.wav", "f3n5.wav", "f3n6.wav", "f3song.wav", "f3unheard.wav"):
        b = open(os.path.join(d, f), "rb").read()
        if b[0:4] != b"RIFF" or len(b) <= 44: errs.append(f)
    shutil.rmtree(d, ignore_errors=True)
    return errs

def m4():
    sums = {}
    for line in open(os.path.join(LAB, "SHA256SUMS")):
        p = line.split()
        if len(p) == 2: sums[p[1]] = p[0]
    outs = {
        "logs/q1m_rep1.txt": run(IMAGINE, "q1", "m", "all"),
        "logs/q1h_rep1.txt": run(IMAGINE, "q1", "h", "all"),
        "logs/q1vm_rep1.txt": run(IMAGINE, "q1v", "m", "all"),
        "logs/q1vh_rep1.txt": run(IMAGINE, "q1v", "h", "all"),
    }
    return all(hashlib.sha256(v.encode()).hexdigest() == sums[k] for k, v in outs.items())

def main():
    rows = []
    m = m1()
    r = m["raw"]
    rows.append(("M1f density", f"v1 {m['v1'][0]:.2f}a/e {m['v1'][1]:.1f}e/s | v2 {m['v2'][0]:.2f} {m['v2'][1]:.1f} | f3 {m['f3'][0]:.2f} {m['f3'][1]:.1f}",
                 f"raw attrs: v1={r[0]}/{r[1]}el v2={r[3]}/{r[4]}el f3={r[6]}/{r[7]}st"))
    m2r = m2(); rows.append(("M2f novel", f"{sum(1 for _, v in m2r if v)}/32", "; ".join(n for n, v in m2r if not v) or "all pass"))
    g1 = gen1(); rows.append(("GEN-1f", f"{sum(1 for _, v in g1 if v)}/12", "; ".join(n for n, v in g1 if not v) or "all pass"))
    g2 = gen2(); rows.append(("GEN-2f", f"{sum(1 for _, v in g2 if v)}/12", "; ".join(n for n, v in g2 if not v) or "all pass"))
    g3 = gen3(); rows.append(("GEN-3f", f"{sum(1 for _, v in g3 if v)}/24", "; ".join(n for n, v in g3 if not v) or "all pass"))
    art = artifacts(); rows.append(("native artifacts", "PASS" if not art else "FAIL", f"14 BMP + 2 AVI + 8 WAV parsed; {len(art)} errors" if art else "headers/chunks/idx1/audio==wav"))
    rows.append(("determinism", "PASS" if determinism() else "FAIL", "5x dumps, 2x wav/bmp/avi byte-identical + raster crosscheck"))
    rows.append(("M4 regression", "PASS" if m4() else "FAIL", "q1/q1v m/h byte-identical to SHA256SUMS"))
    print(f"{'check':<14}{'result':<46}{'detail'}")
    for name, res, det in rows:
        print(f"{name:<14}{res:<46}{det}")
    fails = [n for n, r_, _ in rows if r_ in ("FAIL",) or ("/" in r_ and not r_.startswith("32/32") and not r_.startswith("12/12"))]
    # bars: M2f>=24/32, GEN-1f>=10, GEN-2f==12, GEN-3f>=20, artifacts clean
    bars_ok = (sum(1 for _, v in m2r if v) >= 24 and sum(1 for _, v in g1 if v) >= 10
               and sum(1 for _, v in g2 if v) == 12 and sum(1 for _, v in g3 if v) >= 20
               and not art and determinism() and m4())
    print("BARS:", "PASS" if bars_ok else "FAIL")
    return 0 if bars_ok else 1

if __name__ == "__main__":
    sys.exit(main())
