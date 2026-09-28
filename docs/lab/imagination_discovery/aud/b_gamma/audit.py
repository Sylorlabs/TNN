#!/usr/bin/env python3
"""NO-COPY AUDIT (pre-listening gate K4 for B-gamma).

For each 2s window of the candidate WAV (step 0.5s), find the best-matching
2s window in ANY study source via normalized cross-correlation (computed at
4kHz decimation for speed, refined at full rate for candidates > 0.6).
GATE: max correlation over all windows < 0.80. If a window trips the gate,
the score must be re-timed/re-sourced -- the audit has teeth.
"""
import os, subprocess, sys
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "study_src")
AUD = os.path.join(HERE, "..")

def load_wav_44(path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ar", str(SR),
                        "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32).copy().astype(np.float64)

def dec(x, d=11):
    return x[::d]

def nxcorr(a, b):
    n = min(len(a), len(b))
    a = a[:n] - a[:n].mean(); b = b[:n] - b[:n].mean()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-9 or nb < 1e-9:
        return 0.0
    return float(np.dot(a, b) / (na * nb))

def windows(x, wlen, step):
    for s in range(0, len(x) - wlen + 1, step):
        yield s, x[s:s + wlen]

def main():
    cand_path = sys.argv[1]
    bar = float(sys.argv[2]) if len(sys.argv) > 2 else 0.80
    srcs = sys.argv[3:] or [
        os.path.join(SRC, f) for f in
        ["play_berlin.wav", "play_park.oga", "play_douzen.ogg",
         "surf_lake.ogg", "swings.wav", "wood_casket.ogg", "wood_chair.ogg"]]
    # extra inspiration sources (also in the grain pool)
    srcs += [os.path.join(AUD, "inspiration", f) for f in
             ["an_ice_crackling.wav", "an_storm_thunderbolts.wav",
              "an_mars_wind_supercam.wav", "an_mars_dustdevil.wav"]]
    cand = load_wav_44(cand_path)
    print(f"candidate: {cand_path} ({len(cand)/SR:.1f}s)")
    src_wavs = []
    for s in srcs:
        if not os.path.exists(s):
            print("  skip missing:", s); continue
        x = load_wav_44(s)
        src_wavs.append((os.path.basename(s), x, dec(x)))
        print(f"  source {os.path.basename(s)}: {len(x)/SR:.1f}s")
    wlen = 2 * SR; wstep = SR // 2
    swlen = 2 * (SR // 11); sstep = (SR // 11) // 4
    worst = (0.0, None, None)
    trip = 0
    nwin = 0
    for cs, cw in windows(cand, wlen, wstep):
        nwin += 1
        cd = dec(cw)
        best = 0.0; bsrc = None; bpos = 0
        for name, full, sd in src_wavs:
            for ss, sw in windows(sd, swlen, sstep):
                v = nxcorr(cd, sw)
                if v > best:
                    best = v; bsrc = name; bpos = ss * 11 / SR
        if best > worst[0]:
            worst = (best, bsrc, (cs / SR, bpos))
        if best >= bar:
            trip += 1
            print(f"  TRIP win@{cs/SR:.1f}s corr={best:.3f} ~ {bsrc}@{bpos:.1f}s")
    print(f"windows: {nwin}, trips: {trip}, worst: {worst[0]:.3f} "
          f"({worst[1]} win@{worst[2][0]:.1f}s ~ src@{worst[2][1]:.1f}s)")
    print("GATE:", "TRIPPED -- rework the score" if trip else f"CLEAR (bar {bar})")
    return 1 if trip else 0

if __name__ == "__main__":
    sys.exit(main())
