#!/usr/bin/env python3
"""B-gamma STUDY pipeline: analyze study recordings -> grain library -> gamma.grpk.

Deterministic: no RNG; k-means uses fixed init; all thresholds are constants
documented in STUDY_LOG.md. Study materials are LOCAL ONLY, never committed.
"""
import json, math, os, struct, subprocess, sys
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "study_src")
OUT = os.path.join(HERE, "study_out")
os.makedirs(OUT, exist_ok=True)

def load_mono(path):
    """-> float32 mono @44100 via ffmpeg."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ar", str(SR),
                        "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg failed on {path}: {p.stderr[:200]}")
    return np.frombuffer(p.stdout, dtype=np.float32).copy()

def stft_mag(x, n=2048, hop=512):
    w = np.hanning(n)
    nfr = 1 + (len(x) - n) // hop
    out = np.empty((nfr, n // 2 + 1), dtype=np.float64)
    for i in range(nfr):
        f = x[i * hop:i * hop + n] * w
        out[i] = np.abs(np.fft.rfft(f))
    return out

def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1.0 / SR)
    X[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float64)

def spectral_flux(x, n=2048, hop=512, lo=0, hi=20000):
    if lo > 0 or hi < 20000:
        x = bandpass(x, lo, hi)
    M = stft_mag(x, n, hop)
    d = np.diff(M, axis=0)
    d[d < 0] = 0
    return d.sum(axis=1), hop

def pick_peaks(v, thresh, min_dist):
    """Deterministic peak picker. Returns frame indices."""
    cand = np.where(v > thresh)[0]
    peaks = []
    for c in cand:
        if peaks and c - peaks[-1] < min_dist:
            if v[c] > v[peaks[-1]]:
                peaks[-1] = c
        else:
            peaks.append(c)
    return np.array(peaks, dtype=np.int64)

def rc_fade(n):
    t = np.arange(n) / max(n - 1, 1)
    return 0.5 - 0.5 * np.cos(np.pi * t)

def cut_grain(x, start, end, fade=88):
    g = x[max(start, 0):end].astype(np.float64)
    if len(g) < 64:
        return None
    f = min(fade, len(g) // 4)
    w = rc_fade(2 * f)
    g[:f] *= w[:f]
    g[-f:] *= w[f:]
    return g

def features(g):
    """centroid, rms, attack_ms, zcr, dur_ms."""
    n = len(g)
    if n == 0:
        return (0, 0, 0, 0, 0)
    X = np.abs(np.fft.rfft(g * np.hanning(n)))
    fr = np.fft.rfftfreq(n, 1.0 / SR)
    cent = float((X * fr).sum() / max(X.sum(), 1e-12))
    rms = float(np.sqrt((g ** 2).mean()))
    env = np.abs(g)
    peak = env.max()
    att = int(np.argmax(env > 0.5 * peak)) / SR * 1000.0 if peak > 0 else 0
    zcr = float(((g[:-1] * g[1:]) < 0).mean())
    return (cent, rms, att, zcr, n / SR * 1000.0)

# ---------------- deterministic k-means (fixed init) ----------------
def kmeans(X, k, iters=50):
    # init: k points spread across the sorted first-dimension order
    order = np.argsort(X[:, 0])
    idx = [order[(i * len(order)) // k] for i in range(k)]
    C = X[idx].copy()
    lab = np.zeros(len(X), dtype=np.int64)
    for _ in range(iters):
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        nl = d.argmin(axis=1)
        if (nl == lab).all():
            break
        lab = nl
        for j in range(k):
            m = lab == j
            if m.any():
                C[j] = X[m].mean(axis=0)
    return lab

# ---------------- source registry ----------------
SOURCES = [
    # name, file, class of material, license, url
    ("play_berlin", "play_berlin.wav", "playground/children",
     "CC0", "https://commons.wikimedia.org/wiki/File:209901_foongaz_city-playground-boxhagenerplatz-berlin.wav"),
    ("play_park", "play_park.oga", "children playing in park",
     "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Ambient_sound_children_playing_in_a_park_2026-05-19.oga"),
    ("play_douzen", "play_douzen.ogg", "kids on playground",
     "Public domain", "https://commons.wikimedia.org/wiki/File:Douzen_kids_on_playground.ogg"),
    ("feet_gravel", "feet_gravel.mp3", "footstep on gravel",
     "CC BY 4.0 (Gravity Sound)", "https://commons.wikimedia.org/wiki/File:Footstep_on_Gravel_(Gravity_Sound).mp3"),
    ("surf_lake", "surf_lake.ogg", "lake surf",
     "CC BY-SA 4.0", "https://commons.wikimedia.org/wiki/File:Lake_Okeechobee_Surf_in_April_2016.ogg"),
    ("wood_casket", "wood_casket.ogg", "creaky wooden casket",
     "Public domain", "https://commons.wikimedia.org/wiki/File:Creaky_wooden_casket.ogg"),
    ("wood_chair", "wood_chair.ogg", "creaky wooden swivel chair",
     "Public domain", "https://commons.wikimedia.org/wiki/File:Creaky_wooden_swivel_chair.ogg"),
    ("swings", "swings.wav", "playground swings",
     "CC BY 4.0 (Gravity Sound)", "https://commons.wikimedia.org/wiki/File:Playground_swings_(Gravity_Sound).wav"),
]

AUD = os.path.join(HERE, "..")  # aud/
EXTRA = [
    ("ice_crack", os.path.join(AUD, "inspiration", "an_ice_crackling.wav"), "ice crackling field", "Public domain (NASA via SOURCES.md)"),
    ("thunder", os.path.join(AUD, "inspiration", "an_storm_thunderbolts.wav"), "storm thunder field", "Public domain (SOURCES.md)"),
    ("mars_wind", os.path.join(AUD, "inspiration", "an_mars_wind_supercam.wav"), "Mars wind (SuperCam)", "Public domain (NASA)"),
    ("dustdevil", os.path.join(AUD, "inspiration", "an_mars_dustdevil.wav"), "Mars dust devil (SuperCam)", "Public domain (NASA)"),
]

GRAINS = []  # dicts: src, cls, start, end, samples(np f64), feat

def add_grain(src, cls, x, s0, s1):
    g = cut_grain(x, s0, s1)
    if g is None:
        return
    GRAINS.append(dict(src=src, cls=cls, start=max(s0, 0), end=s1, x=g, feat=features(g)))

# ---------------- per-source segmentation ----------------
def seg_laughs(name, x, lo=300, hi=6000, k=3.0, min_gap_ms=90, max_len_ms=700):
    """Onset-anchored grains for vocal bursts (laughs/shouts/squeals)."""
    flux, hop = spectral_flux(x, lo=lo, hi=hi)
    med = np.median(flux)
    mad = np.median(np.abs(flux - med)) + 1e-12
    peaks = pick_peaks(flux, med + k * mad, int(min_gap_ms / 1000 * SR / hop))
    frames = peaks * hop
    for i, f0 in enumerate(frames):
        s0 = int(f0 - 0.020 * SR)
        s1 = int(f0 + max_len_ms / 1000 * SR)
        if i + 1 < len(frames):
            s1 = min(s1, int(frames[i + 1] - 0.010 * SR))
        add_grain(name, "vocal", x, s0, s1)

def seg_thumps(name, x, lo=60, hi=400, k=4.0, min_gap_ms=150, max_len_ms=450):
    flux, hop = spectral_flux(x, lo=lo, hi=hi)
    med = np.median(flux)
    mad = np.median(np.abs(flux - med)) + 1e-12
    peaks = pick_peaks(flux, med + k * mad, int(min_gap_ms / 1000 * SR / hop))
    for f0 in peaks * hop:
        add_grain(name, "thump", x, int(f0 - 0.015 * SR), int(f0 + max_len_ms / 1000 * SR))

def seg_cracks(name, x, k=5.0, min_gap_ms=60, max_len_ms=350):
    flux, hop = spectral_flux(x, lo=800, hi=12000)
    med = np.median(flux)
    mad = np.median(np.abs(flux - med)) + 1e-12
    peaks = pick_peaks(flux, med + k * mad, int(min_gap_ms / 1000 * SR / hop))
    for f0 in peaks * hop:
        add_grain(name, "crack", x, int(f0 - 0.008 * SR), int(f0 + max_len_ms / 1000 * SR))

def seg_texture(name, x, win_s, step_s, cls):
    n = int(win_s * SR)
    st = int(step_s * SR)
    for s0 in range(0, len(x) - n, st):
        add_grain(name, cls, x, s0, s0 + n)

def main():
    report = {}
    for name, fn, _desc, _lic, _url in SOURCES:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            print("MISSING", p); continue
        x = load_mono(p)
        print(f"{name}: {len(x)/SR:.1f}s")
        if name.startswith("play_"):
            seg_laughs(name, x)
            seg_thumps(name, x)
        elif name == "feet_gravel":
            add_grain(name, "thump", x, 0, len(x))
        elif name == "surf_lake":
            # swell-anchored long grains: detect slow envelope peaks
            # (moving average via cumsum -- direct convolve is O(N*w))
            env = np.abs(x).astype(np.float64)
            w = int(1.0 * SR)
            cs = np.cumsum(np.concatenate([[0.0], env]))
            envs = (cs[w:] - cs[:-w]) / w
            envs = np.concatenate([envs[:w // 2], envs, envs[-(w - w // 2):]])[:len(env)]
            step = int(0.25 * SR)
            ev = envs[::step]
            med = np.median(ev); mad = np.median(np.abs(ev - med)) + 1e-12
            pk = pick_peaks(ev, med + 1.2 * mad, int(3.0 / 0.25))
            for f0 in pk * step:
                add_grain(name, "swell", x, int(f0 - 1.5 * SR), int(f0 + 3.0 * SR))
            seg_texture(name, x[:int(60 * SR)], 3.0, 3.0, "wash")
        elif name.startswith("wood_"):
            seg_cracks(name, x, k=3.0, min_gap_ms=120, max_len_ms=900)
            if not any(g["src"] == name for g in GRAINS):
                add_grain(name, "creak", x, 0, len(x))
            for g in GRAINS:
                if g["src"] == name:
                    g["cls"] = "creak"
        elif name == "swings":
            seg_cracks(name, x, k=3.0, min_gap_ms=200, max_len_ms=1200)
            for g in GRAINS:
                if g["src"] == name:
                    g["cls"] = "creak"
        report[name] = len(x) / SR

    for name, p, _desc, _lic in EXTRA:
        if not os.path.exists(p):
            print("MISSING", p); continue
        x = load_mono(p)
        print(f"{name}: {len(x)/SR:.1f}s")
        if name == "ice_crack":
            seg_cracks(name, x)
        elif name == "thunder":
            # bursts + tails
            flux, hop = spectral_flux(x, lo=40, hi=900)
            med = np.median(flux); mad = np.median(np.abs(flux - med)) + 1e-12
            peaks = pick_peaks(flux, med + 4.0 * mad, int(1.5 * SR / hop))
            for f0 in peaks * hop:
                add_grain(name, "boom", x, int(f0 - 0.03 * SR), int(f0 + 0.6 * SR))
                add_grain(name, "rumble", x, int(f0 + 0.5 * SR), int(f0 + 3.0 * SR))
            seg_texture(name, x[:int(30 * SR)], 3.0, 6.0, "rumble")
        elif name in ("mars_wind", "dustdevil"):
            seg_texture(name, x, 3.0, 3.0, "wind")
        report[name] = len(x) / SR

    # ---- subdivide vocal grains by measured features ----
    voc = [g for g in GRAINS if g["cls"] == "vocal"]
    for g in voc:
        cent, rms, att, zcr, dur = g["feat"]
        if cent > 2000 and dur < 500:
            g["cls"] = "squeal"
        elif dur < 320 and cent > 900:
            g["cls"] = "laugh"
        else:
            g["cls"] = "shout"

    # ---- voice clustering: per vocal SUBCLASS -> 3 voice ids (deterministic) ----
    def assign_voices(gs):
        X = np.array([[math.log1p(g["feat"][0]), g["feat"][4] / 1000.0,
                       math.log1p(g["feat"][1] + 1e-9)] for g in gs])
        mu, sd = X.mean(0), X.std(0) + 1e-12
        lab = kmeans((X - mu) / sd, 3)
        # repair empty clusters deterministically: split the largest cluster
        for _ in range(3):
            counts = [int((lab == j).sum()) for j in range(3)]
            if all(c > 0 for c in counts):
                break
            empty = counts.index(0)
            big = int(np.argmax(counts))
            members = np.where(lab == big)[0]
            members = members[np.argsort(X[members, 0])]
            lab[members[len(members) // 2:]] = empty
        # order voices by median centroid (0=lowest)
        medc = [np.median([g["feat"][0] for g, l in zip(gs, lab) if l == j])
                for j in range(3)]
        order = np.argsort(medc)
        remap = {int(o): i for i, o in enumerate(order)}
        for g, l in zip(gs, lab):
            g["voice"] = remap[int(l)]
    for sub in ("laugh", "squeal", "shout"):
        gs = [g for g in GRAINS if g["cls"] == sub]
        if len(gs) >= 3:
            assign_voices(gs)
        else:
            for g in gs:
                g["voice"] = 0

    # ---- write grain pack ----
    cls_ids = {}
    def cid(c):
        return cls_ids.setdefault(c, len(cls_ids))
    src_names = []
    def sid(s):
        if s not in src_names:
            src_names.append(s)
        return src_names.index(s)
    for g in GRAINS:
        g["cid"] = cid(g["cls"]); g["sid"] = sid(g["src"])

    # ---- per (class, voice) index tables; voice=254 = all voices merged ----
    tables = {}
    for i, g in enumerate(GRAINS):
        key = (g["cid"], g.get("voice", 255))
        tables.setdefault(key, []).append(i)
    for (c, _v), idxs in list(tables.items()):
        if any(v != 255 for (_c2, v) in tables if _c2 == c):
            tables.setdefault((c, 254), []).extend(idxs)
    # deterministic order
    tables = {k: sorted(v) for k, v in sorted(tables.items())}

    pk = os.path.join(OUT, "gamma.grpk")
    with open(pk, "wb") as f:
        f.write(b"GRPK")
        f.write(struct.pack("<II", 2, len(GRAINS)))
        f.write(struct.pack("<I", len(src_names)))
        for s in src_names:
            b = s.encode()
            f.write(struct.pack("<I", len(b)) + b)
        f.write(struct.pack("<I", len(cls_ids)))
        for c, i in sorted(cls_ids.items(), key=lambda kv: kv[1]):
            b = c.encode()
            f.write(struct.pack("<I", len(b)) + b)
        # tables
        f.write(struct.pack("<I", len(tables)))
        for (c, v), idxs in tables.items():
            f.write(struct.pack("<III", c, v, len(idxs)))
            f.write(struct.pack("<%dI" % len(idxs), *idxs))
        for g in GRAINS:
            xs = np.clip(g["x"], -1, 1)
            q = (xs * 32767).astype(np.int16)
            f.write(struct.pack("<IIIIII", len(q), g["sid"], g["start"], g["cid"],
                                g.get("voice", 255), int(g["feat"][0])))
            f.write(q.tobytes())
    # manifest csv
    with open(os.path.join(OUT, "grains.csv"), "w") as f:
        f.write("idx,src,cls,voice,start_s,dur_ms,centroid,rms,attack_ms,zcr\n")
        for i, g in enumerate(GRAINS):
            c, r, a, z, d = g["feat"]
            f.write(f"{i},{g['src']},{g['cls']},{g.get('voice',255)},{g['start']/SR:.3f},{d:.1f},{c:.0f},{r:.4f},{a:.1f},{z:.3f}\n")
    # summary
    summ = {}
    for g in GRAINS:
        summ[g["cls"]] = summ.get(g["cls"], 0) + 1
    print("grain classes:", summ)
    print("total grains:", len(GRAINS), "pack bytes:", os.path.getsize(pk))
    json.dump({"sources": report, "classes": summ,
               "class_names": cls_ids, "src_names": src_names},
              open(os.path.join(OUT, "study_summary.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
