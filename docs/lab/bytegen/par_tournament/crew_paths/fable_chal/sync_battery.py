#!/usr/bin/env python3
"""SYNC-1 battery: cross-path A/V sync. Renders combos, measures per-event
|boing onset - ball Y-minimum|, checks bars (all <=50ms, mean <10ms).
Also: determinism (cmp+sha256), nearedge diagnostic, wall-clock timing."""
import hashlib, os, struct, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
ART = os.path.join(os.path.dirname(HERE), "artifacts", "WITHHELD-NOT-FOR-REVIEW", "fable_chal", "sync")
EV = os.path.join(HERE, "evidence")
os.makedirs(ART, exist_ok=True)
os.makedirs(EV, exist_ok=True)
BIN = os.path.join(SRC, "syncav")
SR, FPS = 44100, 60
NEV = 30

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def run(what, mode, tag, variant="seq"):
    out = os.path.join(ART, "sync_%s.raw" % tag)
    t0 = time.perf_counter()
    p = subprocess.run([BIN, what, mode, out, variant], capture_output=True, text=True)
    dt = time.perf_counter() - t0
    assert p.returncode == 0, (tag, p.stderr)
    return out, dt, sha256(out)

def read_ycent(path):
    data = open(path + ".ycent", "rb").read()
    n = len(data) // 64
    rows = []
    for i in range(n):
        f, sy, cn = data[i * 64:(i + 1) * 64].split()[:3]
        assert int(f) == i
        rows.append(int(sy) / int(cn))
    return rows

def contact_time(ys, k):
    fc = 30 + 60 * k
    lo, hi = fc - 10, fc + 10
    seg = ys[lo:hi + 1]
    m = max(seg)
    i = seg.index(m) + lo
    y0, y1, y2 = ys[i - 1], ys[i], ys[i + 1]
    den = y0 - 2 * y1 + y2
    off = 0.0 if den == 0 else 0.5 * (y0 - y2) / den
    return (i + off) / FPS

def onset_time(path, k, thresh=4000):
    t0 = 0.5 + k
    n0 = int((t0 - 0.1) * SR)
    with open(path, "rb") as f:
        f.seek(n0 * 2)
        raw = f.read(int(0.3 * SR) * 2)
    s = struct.unpack("<%dh" % (len(raw) // 2), raw)
    for i in range(1, len(s)):
        if abs(s[i]) >= thresh and abs(s[i - 1]) < thresh:
            frac = (thresh - abs(s[i - 1])) / max(1, abs(s[i]) - abs(s[i - 1]))
            return (n0 + i - 1 + frac) / SR
    for i in range(len(s)):
        if abs(s[i]) >= thresh:
            return (n0 + i) / SR
    return None

log = []
def emit(x):
    print(x, flush=True)
    log.append(x)

R = {}
jobs = [
    ("video", "vpar", "vpar_r1", "seq"), ("video", "vpar", "vpar_r2", "seq"),
    ("video", "vservo", "vservo_r1", "seq"), ("video", "vservo", "vservo_r2", "seq"),
    ("audio", "apar", "apar_r1", "seq"), ("audio", "apar", "apar_r2", "seq"),
    ("audio", "baudio", "baudio_r1", "seq"), ("audio", "baudio", "baudio_r2", "seq"),
    ("audio", "baudio", "baudio_edge", "nearedge"),
    ("audio", "apar", "apar_edge", "nearedge"),
]
for what, mode, tag, var in jobs:
    out, dt, sh = run(what, mode, tag, var)
    R[tag] = (out, dt, sh)
    emit("%s: wall=%.3fs sha256=%s" % (tag, dt, sh))

for a, b in [("vpar_r1", "vpar_r2"), ("vservo_r1", "vservo_r2"),
             ("apar_r1", "apar_r2"), ("baudio_r1", "baudio_r2")]:
    r = subprocess.run(["cmp", R[a][0], R[b][0]])
    sm = "sha256 match" if R[a][2] == R[b][2] else "SHA MISMATCH"
    emit("determinism %s vs %s: %s (%s)" % (a, b, "PASS" if r.returncode == 0 else "FAIL", sm))
    if a.startswith("v"):
        r2 = subprocess.run(["cmp", R[a][0] + ".ycent", R[b][0] + ".ycent"])
        emit("  sidecar %s: %s" % (a, "PASS" if r2.returncode == 0 else "FAIL"))

combos = [("vpar_r1", "apar_r1", "PAR-video + PAR-audio"),
          ("vpar_r1", "baudio_r1", "PAR-video + B-audio"),
          ("vservo_r1", "baudio_r1", "servo-video + B-audio")]
for vtag, atag, name in combos:
    ys = read_ycent(R[vtag][0])
    errs = []
    for k in range(NEV):
        tc = contact_time(ys, k)
        to = onset_time(R[atag][0], k)
        assert to is not None, (name, k)
        errs.append(abs(to - tc) * 1000.0)
    mean_e, max_e = sum(errs) / len(errs), max(errs)
    emit("%s: mean=%.2fms max=%.2fms [all<=50ms %s, mean<10ms %s]" %
         (name, mean_e, max_e,
          "OK" if max_e <= 50 else "KILL",
          "OK" if mean_e < 10 else "FAIL"))

def edge_onset(path):
    with open(path, "rb") as f:
        f.seek(220941 * 2 - 100 * 2)
        raw = f.read(400 * 2)
    s = struct.unpack("<%dh" % (len(raw) // 2), raw)
    for i in range(1, len(s)):
        if abs(s[i]) >= 4000 and abs(s[i - 1]) < 4000:
            return 220941 - 100 + i
    return None

oa = edge_onset(R["apar_edge"][0])
ob = edge_onset(R["baudio_edge"][0])
emit("nearedge boing t=5.01s: apar onset=%s baudio onset=%s (expect 220941 both)" % (oa, ob))

with open(os.path.join(EV, "sync1.log"), "w") as f:
    f.write("\n".join(log) + "\n")
emit("wrote evidence/sync1.log")
