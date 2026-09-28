#!/usr/bin/env python3
"""R2-8 companion generator: independent-source presentations + perturbations.

Reads <r2a>/SCENES.json and <r2a>/adversarial/*. For each adversarial scene:
  Gi  : clean independent presentation (same truth, fresh measurement)
  Pi1..3: the 3 frozen perturbations applied to Gi
  Qi1..3: the 3 frozen perturbations applied to Fi
Also generates recall companions for normal shapetrans/timbredisc:
  second presentation + 3 perturbations.

Perturbations (frozen, deterministic, stream 700+taskidx):
  P1: Gaussian noise (images/video: sigma=8 RGB; audio: sigma=300 LSB)
  P2: exposure/gain x1.25
  P3: JPEG q=70 recompress (images/video); 8-bit quantize (audio)

Output: <out>/companions/<task>/r2q_<task>_<idx>_{g,p1,p2,p3,q1,q2,q3}.ext
        <out>/companions/recall/r2q_recall_<i>_{g,p1,p2,p3}.ext
        <out>/MANIFEST_q.sha256
"""
import math, os, struct, sys, hashlib, json, random

sys.path.insert(0, os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness"))
import gen as H
sys.path.insert(0, os.path.expanduser("~/workspace/r28work"))
import gen_r2a as G

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
EXTS = [".img", ".img", ".img", ".pcm", ".pcm", ".vid"]

def pseed(taskidx, index):
    # deterministic perturbation seed
    return H.stream_seed(20260923, 700 + taskidx, index)

def _gauss(rng, sigma):
    # Box-Muller
    u1 = max(1e-12, rng.uniform()); u2 = rng.uniform()
    return sigma * math.sqrt(-2*math.log(u1)) * math.cos(2*math.pi*u2)

# ------------------------------------------------------------ Gi builders
def g_colordisc(scene, rng):
    c1, c2 = tuple(scene["c1"]), tuple(scene["c2"])
    px = []
    for y in range(64):
        for x in range(128):
            base = c1 if x < 64 else c2
            px.append(tuple(max(0, min(255, int(c + _gauss(rng, 8)))) for c in base))
    return (128, 64, px)

def g_colorconst(scene, rng, n_photos):
    # neutral d65 re-render of the same crop(s)
    ph, ox, oy = scene["photo"], scene["ox"], scene["oy"]
    crop = H.crop_photo(H.load_photo(ph), 160, ox, oy, 64, 64)
    p1 = H._render_panel(crop, "d65")
    if scene.get("photo2") is not None:
        ph2, ox2, oy2 = scene["photo2"], scene["ox2"], scene["oy2"]
        crop2 = H.crop_photo(H.load_photo(ph2), 160, ox2, oy2, 64, 64)
        p2 = H._render_panel(crop2, "d65")
    else:
        p2 = H._render_panel(crop, "d65")
    px = []
    for y in range(64):
        for x in range(128):
            base = p1[y*64+x] if x < 64 else p2[y*64+(x-64)]
            px.append(tuple(max(0, min(255, int(c + _gauss(rng, 8)))) for c in base))
    return (128, 64, px)

def g_shapetrans(scene, rng, n_photos):
    # fresh 48x48 clear render of the same kind
    kind = {"CIRCLE": "circle", "TRIANGLE": "triangle", "SQUARE": "square"}[scene["kind"]] \
        if scene["kind"] in ("CIRCLE", "TRIANGLE", "SQUARE") else scene["kind"]
    W = 48
    bg = [(30, 30, 30)] * (W*W)  # plain dark bg (clean, unoccluded)
    fg = (235, 235, 235)
    rot = rng.uniform()*2*math.pi; scale = rng.range(14, 20)
    cx, cy = W/2 + rng.range(-6, 6), W/2 + rng.range(-6, 6)
    px = G._raster_shape(kind, rng, W, bg, fg, rot, scale, cx, cy, occl=False)
    return (W, W, px)

def _tone_phase(freq, dur, harmonics, phase0, amp=0.75):
    n = int(H.SR*dur)
    out = [0.0]*n
    for k, a in harmonics:
        w = 2*math.pi*freq*k/H.SR
        for i in range(n):
            out[i] += a*math.sin(w*i + phase0)
    ramp = int(H.SR*0.02)
    for i in range(ramp):
        e = 0.5 - 0.5*math.cos(math.pi*i/ramp)
        out[i] *= e; out[n-1-i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    g = amp/peak
    return [int(max(-32768, min(32767, round(v*g*32767)))) for v in out]

def _chirp_phase(fs, fe, dur, harmonics, phase0, amp=0.75):
    n = int(H.SR*dur)
    out = [0.0]*n
    for k, a in harmonics:
        for i in range(n):
            f = fs + (fe-fs)*i/max(1, n-1)
            phase = 2*math.pi*k*(fs*i/H.SR + (fe-fs)*i*i/(2*max(1, n-1)*H.SR)) + phase0
            out[i] += a*math.sin(phase)
    ramp = int(H.SR*0.02)
    for i in range(ramp):
        e = 0.5 - 0.5*math.cos(math.pi*i/ramp)
        out[i] *= e; out[n-1-i] *= e
    peak = max(1e-9, max(abs(v) for v in out))
    g = amp/peak
    return [int(max(-32768, min(32767, round(v*g*32767)))) for v in out]

def g_pitchdisc(scene, rng, fam):
    ph = rng.uniform()*2*math.pi
    f0 = scene["f0"]
    gap = [0]*int(H.SR*0.08)
    tA = _tone_phase(f0, 0.4, H.RICH_H, ph)
    if fam == "PTC-2":
        tB = _chirp_phase(scene["fs"], scene["fe"], 0.4, H.RICH_H, ph)
    elif fam == "PTC-3":
        tB = _tone_phase(scene["f1"], 0.4, [tuple(h) for h in scene["harm"]], ph)
    else:  # PTC-1
        tB = _tone_phase(scene["f1"], 0.4, H.RICH_H, ph)
    return tA + gap + tB

def g_timbredisc(scene, rng):
    ph = rng.uniform()*2*math.pi
    harm = [tuple(h) for h in scene["harm"]]
    return _tone_phase(440.0, 0.8, harm, ph)

def g_motiondir(scene, rng, n_photos):
    # clean re-render: 2px/frame, full contrast, fresh offset
    truth = scene["dir"]
    vec = H.DIRS.get(truth, (0, 0))
    photo = H.load_photo(scene["photo"])
    return G._motion_frames(rng, photo, truth, vec, 64, 2, 1.0)

G_BUILDERS = {
    "COL-1": g_colordisc, "COL-2": g_colordisc, "COL-3": g_colordisc,
    "CCN-1": g_colorconst, "CCN-2": g_colorconst,
    "SHP-1": g_shapetrans, "SHP-2": g_shapetrans, "SHP-3": g_shapetrans,
    "PTC-1": g_pitchdisc, "PTC-2": g_pitchdisc, "PTC-3": g_pitchdisc,
    "TMB-1": g_timbredisc, "TMB-2": g_timbredisc, "TMB-3": g_timbredisc,
    "MOT-1": g_motiondir, "MOT-2": g_motiondir, "MOT-3": g_motiondir,
}

# ------------------------------------------------------------ perturbations
def pert_noise_img(px, rng, sigma=8):
    # Optimized with NumPy; deterministic via rng seed
    import numpy as np
    import random
    # Derive a Python Random from the rng's state for determinism
    # (H.Rng doesn't expose state; use the pseed indirectly via a counter)
    # Actually, use numpy with a seed from the rng's next 64 bits
    # Simpler: flatten and use Python loops but with array module
    # For speed, use numpy vectorization with pre-generated noise
    n = len(px)
    # Generate noise using Box-Muller in bulk via numpy (deterministic with seed)
    # Seed from rng: draw one 64-bit int
    seed = rng.int(2**31)
    np_rng = np.random.RandomState(seed)
    noise = np_rng.normal(0, sigma, n*3)
    arr = np.array(px, dtype=np.float64).reshape(-1)
    out = np.clip(arr + noise, 0, 255).astype(np.uint8)
    # Convert back to list of tuples
    return [tuple(out[i*3:(i+1)*3].tolist()) for i in range(n)]

def pert_noise_pcm(samps, rng, sigma=300):
    import numpy as np
    seed = rng.int(2**31)
    np_rng = np.random.RandomState(seed)
    noise = np_rng.normal(0, sigma, len(samps))
    arr = np.array(samps, dtype=np.float64)
    out = np.clip(arr + noise, -32768, 32767).astype(np.int16)
    return out.tolist()

def pert_expose_img(px, rng, gain=1.25):
    import numpy as np
    arr = np.array(px, dtype=np.float64)
    out = np.clip(arr * gain, 0, 255).astype(np.uint8)
    return [tuple(row.tolist()) for row in out]

def pert_expose_pcm(samps, rng, gain=1.25):
    import numpy as np
    arr = np.array(samps, dtype=np.float64)
    out = np.clip(arr * gain, -32768, 32767).astype(np.int16)
    return out.tolist()

def pert_jpeg_img(px, w, h, rng):
    # JPEG q=70 recompress via PIL; deterministic (no RNG used, fixed q)
    from PIL import Image
    import io
    im = Image.new("RGB", (w, h))
    im.putdata([tuple(p) for p in px])
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70)
    buf.seek(0)
    im2 = Image.open(buf).convert("RGB")
    return list(im2.getdata())

def pert_quant_pcm(samps, rng):
    # 8-bit uniform quantization (lossy-codec analog for audio)
    return [max(-32768, min(32767, int(round(s/256.0))*256)) for s in samps]

def apply_perts_img(w, h, px, taskidx, index):
    rng = H.Rng(pseed(taskidx, index*10 + 1))
    p1 = pert_noise_img(px, rng)
    rng = H.Rng(pseed(taskidx, index*10 + 2))
    p2 = pert_expose_img(px, rng)
    rng = H.Rng(pseed(taskidx, index*10 + 3))
    p3 = pert_jpeg_img(px, w, h, rng)
    return p1, p2, p3

def apply_perts_pcm(samps, taskidx, index):
    rng = H.Rng(pseed(taskidx, index*10 + 1))
    p1 = pert_noise_pcm(samps, rng)
    rng = H.Rng(pseed(taskidx, index*10 + 2))
    p2 = pert_expose_pcm(samps, rng)
    rng = H.Rng(pseed(taskidx, index*10 + 3))
    p3 = pert_quant_pcm(samps, rng)
    return p1, p2, p3

def apply_perts_vid(frames, w, h, taskidx, index):
    outs = [[], [], []]
    for fi, fr in enumerate(frames):
        rng = H.Rng(pseed(taskidx, (index*10 + 1)*100 + fi))
        outs[0].append(pert_noise_img(fr, rng))
        rng = H.Rng(pseed(taskidx, (index*10 + 2)*100 + fi))
        outs[1].append(pert_expose_img(fr, rng))
        rng = H.Rng(pseed(taskidx, (index*10 + 3)*100 + fi))
        outs[2].append(pert_jpeg_img(fr, w, h, rng))
    return outs[0], outs[1], outs[2]

# ------------------------------------------------------------ file IO
def load_img(path):
    import struct
    raw = open(path, "rb").read()
    w, h = struct.unpack("<II", raw[:8])
    px = [tuple(raw[8+i*3:8+i*3+3]) for i in range(w*h)]
    return w, h, px

def load_pcm(path):
    import struct
    raw = open(path, "rb").read()
    rate, cnt = struct.unpack("<II", raw[:8])
    samps = list(struct.unpack("<%dh" % cnt, raw[8:8+2*cnt]))
    return rate, samps

def load_vid(path):
    import struct
    raw = open(path, "rb").read()
    nf, w, h = struct.unpack("<III", raw[:12])
    frames = []
    off = 12
    for _ in range(nf):
        px = [tuple(raw[off+i*3:off+i*3+3]) for i in range(w*h)]
        frames.append(px); off += w*h*3
    return nf, w, h, frames

def write_companion(out_dir, stem, ext, kind, payload):
    path = os.path.join(out_dir, stem + ext)
    if kind == "img":
        w, h, px = payload
        H.write_img(path, w, h, px)
    elif kind == "pcm":
        H.write_pcm(path, H.SR, payload)
    elif kind == "vid":
        nf, w, h, frames = payload[0], payload[1], payload[2], payload[3]
        H.write_vid(path, w, h, frames)
    return path

# ------------------------------------------------------------ main
def main():
    r2a = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2a")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(r2a), "r2q")
    tasks_filter = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    scenes = json.load(open(os.path.join(r2a, "SCENES.json")))
    if tasks_filter:
        scenes = {k: v for k, v in scenes.items() if k.split("_")[1] in tasks_filter}
    n_photos = 170
    manifest = []
    def rec(path):
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        manifest.append((h, os.path.relpath(path, out)))
    cdir = os.path.join(out, "companions")
    # group scenes by task
    by_task = {}
    for fname, meta in scenes.items():
        task = fname.split("_")[1]  # r2a_<task>_<idx>.ext
        by_task.setdefault(task, []).append((fname, meta))
    for task, items in sorted(by_task.items()):
        ti = TASKS.index(task)
        ext = EXTS[ti]
        tdir = os.path.join(cdir, task)
        os.makedirs(tdir, exist_ok=True)
        items.sort()
        for fname, meta in items:
            idx = int(fname.split("_")[2].split(".")[0])
            fam = meta["family"]; scene = meta["scene"]
            fpath = os.path.join(r2a, "adversarial", fname)
            stem = "r2q_%s_%04d" % (task, idx)
            # Skip if already done (for resume)
            _sfxs = ["_g", "_p1", "_p2", "_p3", "_q1", "_q2", "_q3"]
            _all_exist = all(os.path.exists(os.path.join(tdir, stem + _sfx + ext)) for _sfx in _sfxs)
            if _all_exist:
                for _sfx in _sfxs:
                    rec(os.path.join(tdir, stem + _sfx + ext))
                continue
            # Gi
            rng = H.Rng(H.stream_seed(20260923, 600 + ti, idx))
            builder = G_BUILDERS[fam]
            if fam.startswith("COL"):
                g = builder(scene, rng); kind = "img"
            elif fam.startswith("CCN") or fam.startswith("SHP"):
                g = builder(scene, rng, n_photos); kind = "img"
            elif fam.startswith("PTC"):
                g = builder(scene, rng, fam); kind = "pcm"
            elif fam.startswith("TMB"):
                g = builder(scene, rng); kind = "pcm"
            else:
                g = builder(scene, rng, n_photos); kind = "vid"
            # normalize Gi payload
            if kind == "img":
                gw, gh, gpx = g; gpay = (gw, gh, gpx)
            elif kind == "pcm":
                gpay = g
            else:
                gpay = (len(g), 64, 64, g)
            pg = write_companion(tdir, stem + "_g", ext, kind, gpay)
            rec(pg)
            # Pi = perts of Gi
            if kind == "img":
                p1, p2, p3 = apply_perts_img(gw, gh, gpx, ti, idx)
                pays = [(gw, gh, p1), (gw, gh, p2), (gw, gh, p3)]
            elif kind == "pcm":
                p1, p2, p3 = apply_perts_pcm(g, ti, idx)
                pays = [p1, p2, p3]
            else:
                f1, f2, f3 = apply_perts_vid(g, 64, 64, ti, idx)
                pays = [(len(f1), 64, 64, f1), (len(f2), 64, 64, f2), (len(f3), 64, 64, f3)]
            for j, pay in enumerate(pays, 1):
                pp = write_companion(tdir, stem + "_p%d" % j, ext, kind, pay)
                rec(pp)
            # Qi = perts of Fi (load Fi bytes)
            if kind == "img":
                fw, fh, fpx = load_img(fpath)
                q1, q2, q3 = apply_perts_img(fw, fh, fpx, ti, 50000 + idx)
                qpays = [(fw, fh, q1), (fw, fh, q2), (fw, fh, q3)]
            elif kind == "pcm":
                rate, fsamps = load_pcm(fpath)
                q1, q2, q3 = apply_perts_pcm(fsamps, ti, 50000 + idx)
                qpays = [q1, q2, q3]
            else:
                nf, vw, vh, frames = load_vid(fpath)
                f1, f2, f3 = apply_perts_vid(frames, vw, vh, ti, 50000 + idx)
                qpays = [(len(f1), vw, vh, f1), (len(f2), vw, vh, f2), (len(f3), vw, vh, f3)]
            for j, pay in enumerate(qpays, 1):
                qp = write_companion(tdir, stem + "_q%d" % j, ext, kind, pay)
                rec(qp)
        print("companions %s: %d scenes x7" % (task, len(items)), flush=True)
    # recall companions: first 1008 normal shapetrans + 1008 normal timbredisc
    rdir = os.path.join(cdir, "recall")
    os.makedirs(rdir, exist_ok=True)
    ndir = os.path.join(r2a, "normal")
    for task, ti, need in [("shapetrans", 2, 1008), ("timbredisc", 4, 1008)]:
        ext = EXTS[ti]
        for i in range(need):
            fname = "r2n_%s_%04d%s" % (task, i, ext)
            fpath = os.path.join(ndir, fname)
            stem = "r2q_recall_%s_%04d" % (task, i)
            rng = H.Rng(H.stream_seed(20260923, 600 + ti, 90000 + i))
            if task == "shapetrans":
                # second presentation: fresh 48x48 clear render, kind from truth
                truth = open(fpath + ".truth").read().strip().split("=")[1]
                g = g_shapetrans({"kind": truth}, rng, n_photos)
                gw, gh, gpx = g
                pg = write_companion(rdir, stem + "_g", ext, "img", (gw, gh, gpx))
                rec(pg)
                p1, p2, p3 = apply_perts_img(gw, gh, gpx, ti, 90000 + i)
                for j, pay in enumerate([(gw, gh, p1), (gw, gh, p2), (gw, gh, p3)], 1):
                    rec(write_companion(rdir, stem + "_p%d" % j, ext, "img", pay))
            else:
                truth = open(fpath + ".truth").read().strip().split("=")[1]
                harm = G.R2A_TIMBRES[truth]
                g = _tone_phase(440.0, 0.8, harm, rng.uniform()*2*math.pi)
                pg = write_companion(rdir, stem + "_g", ext, "pcm", g)
                rec(pg)
                p1, p2, p3 = apply_perts_pcm(g, ti, 90000 + i)
                for j, pay in enumerate([p1, p2, p3], 1):
                    rec(write_companion(rdir, stem + "_p%d" % j, ext, "pcm", pay))
        print("recall %s: %d" % (task, need), flush=True)
    manifest.sort(key=lambda x: x[1])
    with open(os.path.join(out, "MANIFEST_q.sha256"), "w") as f:
        for h, rel in manifest:
            f.write("%s  %s\n" % (h, rel))
    print("TOTAL companion files: %d" % len(manifest))

if __name__ == "__main__":
    main()
