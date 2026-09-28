#!/usr/bin/env python3
"""Crew C frozen scorer: measures renders against target descriptors.

Frozen BEFORE test runs (prereg 5.2). Builders may read this source for
measurement DEFINITIONS; the control binary never calls it.

Measurement definitions (all deterministic, no RNG):
- pitch: median F0 over voiced frames; properly normalized autocorrelation
  (each lag normalized by its overlapping segment energies, no triangular
  lag bias) over lags 36..552 (79.9..1225 Hz); the fundamental is the FIRST
  strong local peak scanning ascending lags (pure tones correlate ~1.0 at
  every period multiple), parabolic interpolation around it; frame voiced
  iff peak r >= 0.40 and frame RMS > -50 dBFS. Hit: |F0-t|/t <= 2%.
- envelope: frame RMS (2048/1024); m1/m3 = mean RMS of first/last third of
  frames; rise iff m3/m1 > 1.5; decay iff m1/m3 > 1.5; else flat.
  Hit: class == target class.
- rhythm: onsets = frames where frame-RMS derivative crosses 0.25 * max
  (positive-going, 4-frame refractory; no onsets at all unless the max
  derivative exceeds an absolute 0.02 floor); IOIs from onset times; 'few'
  if < 4 IOIs; ratio = median(upper half IOIs)/median(lower half IOIs);
  swing iff ratio >= 1.25 else even. Hit: class == target class.
- prosody: CV% = 100*std/mean of voiced-frame F0s (>= 10 voiced frames).
  Hit: |CV-t|/t <= 35%.

CLI: scorer_c.py <wav> <descriptor>  -> JSON on stdout.
"""
import json
import math
import struct
import sys

import numpy as np

SR = 44100
FRAME = 2048
HOP = 1024
LAG_MIN, LAG_MAX = 36, 552
VOICED_R = 0.40
VOICED_RMS_DB = -50.0


def read_wav(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[0:4] == b"RIFF" and data[8:12] == b"WAVE", "not a WAV"
    assert struct.unpack("<H", data[20:22])[0] == 1, "not PCM"
    assert struct.unpack("<H", data[22:24])[0] == 1, "not mono"
    assert struct.unpack("<I", data[24:28])[0] == SR, "not 44100 Hz"
    assert struct.unpack("<H", data[34:36])[0] == 16, "not 16-bit"
    n = struct.unpack("<I", data[40:44])[0] // 2
    samples = np.frombuffer(data[44:44 + 2 * n], dtype=np.int16).astype(np.float64)
    return samples / 32768.0


def frame_rms(samples):
    n = len(samples)
    nf = (n - FRAME) // HOP + 1
    out = np.empty(nf)
    for i in range(nf):
        fr = samples[i * HOP:i * HOP + FRAME]
        out[i] = math.sqrt(float(np.mean(fr * fr)))
    return out


def f0_of_frame(x):
    # properly normalized autocorrelation: each lag normalized by the
    # overlapping segment energies (removes the triangular lag bias)
    lags = np.arange(LAG_MIN, LAG_MAX + 1)
    rs = np.empty(len(lags))
    for j, l in enumerate(lags):
        a = x[:FRAME - l]
        b = x[l:]
        den = math.sqrt(float(np.dot(a, a)) * float(np.dot(b, b)))
        rs[j] = float(np.dot(a, b)) / den if den > 0 else 0.0
    jmax = int(np.argmax(rs))
    best_r = float(rs[jmax])
    if best_r < VOICED_R:
        return None, best_r
    # first strong peak scanning ascending lags = fundamental period
    # (pure tones correlate ~1.0 at every multiple of the period)
    th = max(VOICED_R, 0.5 * best_r)
    j = None
    for k in range(1, len(rs) - 1):
        if rs[k] >= rs[k - 1] and rs[k] >= rs[k + 1] and rs[k] >= th:
            j = k
            break
    if j is None:
        j = jmax
    lag = float(lags[j])
    if 0 < j < len(rs) - 1:
        y0, y1, y2 = rs[j - 1], rs[j], rs[j + 1]
        den = y0 - 2 * y1 + y2
        if den != 0:
            lag = lag + 0.5 * (y0 - y2) / den
    return SR / lag, best_r


def measure(samples):
    rms = frame_rms(samples)
    db = np.where(rms > 0, 20 * np.log10(np.maximum(rms, 1e-12)), -999.0)
    nf = len(rms)
    f0s = []
    for i in range(nf):
        if db[i] > VOICED_RMS_DB:
            f0, r = f0_of_frame(samples[i * HOP:i * HOP + FRAME])
            if f0 is not None:
                f0s.append(f0)
    med_f0 = float(np.median(f0s)) if f0s else None

    # envelope thirds
    m1 = float(np.mean(rms[: nf // 3])) if nf // 3 else 0.0
    m3 = float(np.mean(rms[2 * nf // 3:])) if nf - 2 * nf // 3 else 0.0
    if m1 > 0 and m3 / m1 > 1.5:
        env = "rise"
    elif m3 > 0 and m1 / m3 > 1.5:
        env = "decay"
    else:
        env = "flat"

    # onsets (absolute floor: no real attack -> no onsets, not noise)
    dr = np.diff(rms)
    mx = float(np.max(dr)) if len(dr) else 0.0
    onsets = []
    last = -10
    if mx > 0.02:
        for j in range(1, len(dr)):
            if dr[j] > 0.25 * mx and dr[j] >= dr[j - 1] and j - last >= 4:
                onsets.append(j * HOP / SR)
                last = j
    iois = [onsets[j + 1] - onsets[j] for j in range(len(onsets) - 1)]
    if len(iois) < 4:
        rhy = "few"
    else:
        srt = sorted(iois)
        lo = srt[: len(srt) // 2]
        hi = srt[len(srt) // 2:]
        lom = float(np.median(lo))
        him = float(np.median(hi))
        rhy = "swing" if (him / lom) >= 1.25 else "even"

    # prosody CV
    cv = None
    if len(f0s) >= 10:
        fa = np.array(f0s)
        mean = float(np.mean(fa))
        cv = 100.0 * float(np.std(fa)) / mean if mean > 0 else None

    return {"f0": med_f0, "n_voiced": len(f0s), "env": env,
            "n_onsets": len(onsets), "rhy": rhy, "cv": cv}


def parse_descriptor(desc):
    axes = {}
    for part in desc.split("+"):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        if k == "pitch":
            axes["pitch"] = float(v)
        elif k == "env":
            axes["env"] = v
        elif k == "rhy":
            axes["rhy"] = "swing" if v.startswith("swing") else v
        elif k == "prosody":
            axes["prosody"] = float(v)
    return axes


def score(wav_path, descriptor):
    samples = read_wav(wav_path)
    m = measure(samples)
    axes = parse_descriptor(descriptor)
    verdicts = {}
    if "pitch" in axes:
        t = axes["pitch"]
        verdicts["pitch"] = (m["f0"] is not None
                             and abs(m["f0"] - t) / t <= 0.02)
    if "env" in axes:
        verdicts["env"] = (m["env"] == axes["env"])
    if "rhy" in axes:
        verdicts["rhy"] = (m["rhy"] == axes["rhy"])
    if "prosody" in axes:
        t = axes["prosody"]
        verdicts["prosody"] = (m["cv"] is not None
                               and abs(m["cv"] - t) / t <= 0.35)
    hit = all(verdicts.values()) if verdicts else False
    return {"measurements": m, "axes": axes, "verdicts": verdicts,
            "hit": hit}


def main():
    wav_path, descriptor = sys.argv[1], sys.argv[2]
    print(json.dumps(score(wav_path, descriptor), indent=1))


if __name__ == "__main__":
    main()
