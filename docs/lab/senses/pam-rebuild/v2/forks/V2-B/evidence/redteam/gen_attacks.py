#!/usr/bin/env python3
"""V2-B red-team attack span generator (Gap Crew C). Deterministic, zero RNG.
Crafts colordisc attack spans per ATTACK_PREREG_V2-B.md (frozen).
Single-span .r24 = u32LE w,h + 24576 RGB bytes. Runs the compiled vsense
binary on F/G/P1/P2/P3 and emits a records file for attack_gate.zag."""
import os, struct, subprocess, sys

W, H = 128, 64
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "spans")
VSENSE = os.path.join(os.path.dirname(HERE), "src", "vsense_bin")
REC = os.path.join(HERE, "attack_records.txt")

GRAY_BG = [64, 96, 128, 160, 192, 224]
RED, GREEN = (255, 0, 0), (0, 255, 0)

def img(pixels):
    return struct.pack("<II", W, H) + bytes(pixels)

def uniform(v):
    return [v] * (W * H * 3)

def halves(l, r):
    px = []
    for y in range(H):
        for x in range(W):
            px += list(l if x < W // 2 else r)
    return px

def spoof(bg, left, right):
    """Scene=bg gray; sampled rows (y%16 in {0,8}) carry left/right colors."""
    px = []
    for y in range(H):
        for x in range(W):
            if y % 16 == 0 or y % 16 == 8:
                px += list(left if x < W // 2 else right)
            else:
                px += [bg, bg, bg]
    return px

def p1(payload):
    out = bytearray(payload)
    for i in range(0, len(out), 3):
        r, g, b = out[i], out[i+1], out[i+2]
        out[i], out[i+1], out[i+2] = g, b, r
    return bytes(out)

def p2(payload):
    out = bytearray(payload)
    for y in range(H // 3, 2 * H // 3):
        for x in range(W):
            o = (y * W + x) * 3
            out[o] = out[o+1] = out[o+2] = 0
    return bytes(out)

def p3(payload):
    out = bytearray(payload)
    for i in range(len(out)):
        out[i] ^= ((i * 0x9E3779B9) >> 16) & 0xFF
    return bytes(out)

def run_vsense(path):
    r = subprocess.run([VSENSE, "colordisc", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"vsense failed on {path}: {r.stdout} {r.stderr}")
    d = {}
    for line in r.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    j = 1 if d["judgment"] == "DIFFERENT" else 0
    return j, int(d["confidence"]), int(d["measure"])

def main():
    os.makedirs(OUT, exist_ok=True)
    trials = []  # (name, truth(0/1), F_payload, G_payload)
    # Attack A: 12 sparse-row spoofs (bg x color-order)
    n = 0
    for bg in GRAY_BG:
        for (l, r) in [(RED, GREEN), (GREEN, RED)]:
            n += 1
            name = f"A{n:02d}"
            bg2 = bg + 16 if bg < 200 else bg - 16  # disjoint G background
            trials.append((name, 0, spoof(bg, l, r), spoof(bg2, l, r)))
    # Attack C1: 12 uniform grays
    for i, v in enumerate([32, 64, 96, 128, 160, 192, 224, 16, 48, 80, 112, 144]):
        trials.append((f"C1{i+1:02d}", 0, uniform(v), uniform(v)))
    # Attack C2: 12 grayscale black/white (and gray-level) halves
    pairs = [(0, 255), (255, 0), (32, 224), (224, 32), (64, 192), (192, 64),
             (0, 200), (200, 0), (16, 240), (240, 16), (48, 208), (208, 48)]
    for i, (l, r) in enumerate(pairs):
        trials.append((f"C2{i+1:02d}", 1, halves((l, l, l), (r, r, r)),
                       halves((l, l, l), (r, r, r))))
    rec_lines = []
    # resume: load already-recorded trials
    done = set()
    if os.path.exists(REC):
        for line in open(REC):
            line = line.strip()
            if line:
                done.add(line.split("|")[0])
                rec_lines.append(line)
    for name, truth, fpay, gpay in trials:
        if name in done:
            continue
        spans = {"F": fpay, "G": gpay, "P1": p1(gpay), "P2": p2(gpay), "P3": p3(gpay)}
        vals = {}
        for s, pay in spans.items():
            p = os.path.join(OUT, f"{name}_{s}.r24")
            if not os.path.exists(p):
                with open(p, "wb") as fh:
                    fh.write(img(pay))
            vals[s] = run_vsense(p)
        jF, cF, mF = vals["F"]; jG, cG, mG = vals["G"]
        rec = [name, "colordisc", str(truth), str(jF), str(cF), str(mF),
               str(jG), str(cG), str(mG)]
        for s in ["P1", "P2", "P3"]:
            j, c, m = vals[s]
            rec += [str(j), str(m)]
        rec_lines.append("|".join(rec))
        print(f"{name} truth={'DIFF' if truth else 'SAME'} "
              f"F=(j{jF},c{cF},m{mF}) G=(j{jG},c{cG},m{mG}) " +
              " ".join(f"{s}=(j{vals[s][0]},m{vals[s][2]})" for s in ["P1","P2","P3"]),
              flush=True)
    with open(REC, "w") as fh:
        fh.write("\n".join(rec_lines) + "\n")
    print(f"wrote {REC} ({len(rec_lines)} trials)")

if __name__ == "__main__":
    main()
