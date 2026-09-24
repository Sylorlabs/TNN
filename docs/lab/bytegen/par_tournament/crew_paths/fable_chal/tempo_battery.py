#!/usr/bin/env python3
"""TEMPO-1 battery: determinism (cmp+sha256), centroid jitter, kill check, wall-clock."""
import hashlib, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
ART = os.path.join(os.path.dirname(HERE), "artifacts", "WITHHELD-NOT-FOR-REVIEW", "fable_chal", "tempo")
EV = os.path.join(HERE, "evidence")
os.makedirs(ART, exist_ok=True)
os.makedirs(EV, exist_ok=True)
BIN = os.path.join(SRC, "tempo")
NF, W, H, FS = 300, 320, 240, 320 * 240 * 3

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def run(mode, variant, tag):
    out = os.path.join(ART, f"tempo_{tag}.raw")
    t0 = time.perf_counter()
    p = subprocess.run([BIN, mode, out, variant], capture_output=True, text=True)
    dt = time.perf_counter() - t0
    assert p.returncode == 0, (tag, p.stderr)
    return out, dt, sha256(out)

def read_cen(path):
    rows = []
    with open(path + ".cen", "rb") as f:
        data = f.read()
    assert len(data) == NF * 64, (path, len(data))
    for i in range(NF):
        rec = data[i * 64:(i + 1) * 64].split()[0:3]
        fr, sx, cn = int(rec[0]), int(rec[1]), int(rec[2])
        assert fr == i, (path, i, fr)
        rows.append((sx, cn))
    return rows

def analyze(tag):
    rows = read_cen(os.path.join(ART, f"tempo_{tag}.raw"))
    xs = []
    for f, (sx, cn) in enumerate(rows):
        assert cn > 0, (tag, f, "empty mask")
        xs.append(sx / cn)
    exp = [(15360 + 171 * f) / 256.0 for f in range(NF)]
    jit = [abs(a - e) for a, e in zip(xs, exp)]
    mean_jit = sum(jit) / NF
    max_jit = max(jit)
    step = 171 / 256.0
    vel = [abs((xs[f + 1] - xs[f]) - step) for f in range(NF - 1)]
    max_veldev = max(vel)
    kill_jump = abs(xs[51] - xs[50])
    return dict(mean_jit=mean_jit, max_jit=max_jit, max_veldev=max_veldev,
                kill_jump=kill_jump, n=NF)

log = []
def emit(s):
    print(s, flush=True)
    log.append(s)

results = {}
for mode, tag in [("par", "par_r1"), ("par", "par_r2"), ("b", "b_r1"), ("b", "b_r2"), ("par", "par_scr")]:
    variant = "scr" if tag == "par_scr" else "seq"
    out, dt, sh = run(mode, variant, tag)
    results[tag] = (out, dt, sh)
    emit(f"{tag}: wall={dt:.3f}s sha256={sh}")

# determinism: byte-identical reruns
for a, b in [("par_r1", "par_r2"), ("b_r1", "b_r2")]:
    pa, pb = results[a][0], results[b][0]
    r = subprocess.run(["cmp", pa, pb])
    det = "PASS" if r.returncode == 0 else "FAIL"
    shm = "match" if results[a][2] == results[b][2] else "MISMATCH"
    emit(f"determinism {a} vs {b}: {det} (sha256 {shm})")
# scr order-free for par
r = subprocess.run(["cmp", results["par_r1"][0], results["par_scr"][0]])
emit(f"par seq vs scr order-free: {'PASS byte-identical' if r.returncode == 0 else 'FAIL'}")
r = subprocess.run(["cmp", results["par_r1"][0] + ".cen", results["par_scr"][0] + ".cen"])
emit(f"par seq vs scr sidecar: {'PASS byte-identical' if r.returncode == 0 else 'FAIL'}")

for tag in ["par_r1", "b_r1"]:
    a = analyze(tag)
    emit(f"{tag}: jitter mean={a['mean_jit']:.4f}px max={a['max_jit']:.4f}px "
         f"(bar <2px); max frame-to-frame vel dev={a['max_veldev']:.4f}px; "
         f"frames50-51 jump={a['kill_jump']:.4f}px (kill bar: 10px discontinuity)")

with open(os.path.join(EV, "tempo1.log"), "w") as f:
    f.write("\n".join(log) + "\n")
emit("wrote evidence/tempo1.log")
