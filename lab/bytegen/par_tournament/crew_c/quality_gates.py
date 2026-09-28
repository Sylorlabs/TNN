#!/usr/bin/env python3
"""CREW GAMMA — Python port of consistency_gate/src/gate.zag for short clips.

Same 9 bar definitions and limits as the frozen gate; the only adaptation is
the minimum-length guard (gate.zag requires >= 10 s; fixtures here are
2.6-3.1 s). Window math (50 ms / 1 s) is unchanged. Validated against the
real gate_bin on fork_par/src/par_seq1.wav (30 s) — must agree to ~1e-3.

Deterministic, zero RNG.
"""
import sys, struct
import numpy as np

def read_wav(path):
    with open(path, "rb") as f:
        raw = f.read()
    assert raw[0:4] == b"RIFF" and raw[36:40] == b"data", "not a 16-bit mono WAV"
    nsamp = struct.unpack("<i", raw[40:44])[0] // 2
    pcm = np.frombuffer(raw[44:44 + nsamp * 2], dtype="<i2").astype(np.float64)
    assert len(pcm) == nsamp
    return pcm

def mdb(sumsq, n):
    sumsq = np.asarray(sumsq, dtype=np.float64)
    out = np.full_like(sumsq, -120.0)
    ok = sumsq > 0
    out[ok] = 10.0 * np.log10(sumsq[ok] / n)
    return out

def gate(path, min_s=2.0):
    pcm = read_wav(path)
    nsamp = len(pcm)
    assert nsamp >= int(44100 * min_s), "clip too short"
    W50 = 2205
    NW = nsamp // W50
    x = pcm[:NW * W50].reshape(NW, W50)
    sumsq = (x ** 2).sum(axis=1)
    peak = np.abs(x).max()
    tot = sumsq.sum()
    edb = mdb(sumsq, W50)

    NS1 = nsamp // 44100
    db1 = mdb(sumsq[:NS1 * 20].reshape(NS1, 20).sum(axis=1), 44100)
    m1 = db1.mean()
    sta_std = np.sqrt(((db1 - m1) ** 2).mean())
    sta_range = db1.max() - db1.min()

    me = edb.mean()
    lurch_std = np.sqrt(((edb - me) ** 2).mean())

    # spectral: 64-band Goertzel per 1 s window
    NB = 64
    freqs = 86.13 + 172.27 * np.arange(NB)
    w = 2 * np.pi * freqs / 44100.0
    c = 2 * np.cos(w)
    cents = np.zeros(NS1)
    flux_max = 0.0
    prev = np.zeros(NB)
    for s1 in range(NS1):
        seg = pcm[s1 * 44100:(s1 + 1) * 44100] / 32768.0
        s_1 = np.zeros(NB)
        s_2 = np.zeros(NB)
        for v in seg:
            s0 = v + c * s_1 - s_2
            s_2, s_1 = s_1, s0
        E = s_1 ** 2 + s_2 ** 2 - c * s_1 * s_2
        E = np.maximum(E, 0.0)
        maxe = E.max()
        if maxe <= 0:
            maxe = 1.0
        mag = np.sqrt(E)
        cent = (freqs * mag).sum() / mag.sum() if mag.sum() > 0 else 0.0
        cents[s1] = cent
        nm = mag / np.sqrt(maxe)
        if s1 > 0:
            fl = np.sqrt((((nm - prev) ** 2)).mean())
            flux_max = max(flux_max, fl)
        prev = nm
    mc = cents.mean()
    cent_std = np.sqrt(((cents - mc) ** 2).mean())

    # envelope autocorr, lags 0.5..25 s (10..500 windows of 50 ms)
    d = edb - me
    ac0 = (d ** 2).sum()
    ac_max = 0.0
    lagmax = min(NW - 10, 500)
    for lag in range(10, lagmax + 1):
        r = (d[:NW - lag] * d[lag:]).sum() / ac0 if ac0 > 0 else 0.0
        ac_max = max(ac_max, r)

    # onsets: >6 dB rises per 50 ms, per 2 s bins
    nbins = NW // 40
    onmax = 0
    for bi in range(nbins):
        seg = edb[bi * 40:(bi + 1) * 40]
        onmax = max(onmax, int((np.diff(seg) > 6.0).sum()))

    # gaps: windows < -60 dBFS
    isgap = edb < -60.0
    gapfrac = isgap.mean()
    best = 0
    run = 0
    for g in isgap:
        run = run + 1 if g else 0
        best = max(best, run)
    gaplong = best / 20.0

    peakf = peak / 32768.0
    rmsall = np.sqrt(tot / nsamp) / 32768.0
    crest = peakf / rmsall if rmsall > 0 else 0.0

    bars = [
        ("G-PER", ac_max, 0.35),
        ("G-STA", sta_std, 3.0),
        ("G-LURCH", lurch_std, 5.0),
        ("G-DRIFT", cent_std, 800.0),
        ("G-FLUXm", flux_max * 1000.0, 350.0),
        ("G-SIL1", gapfrac, 0.02),
        ("G-SIL2", gaplong, 0.5),
        ("G-CLIP", peakf, 0.95),
        ("G-CREST", crest, 14.0),
    ]
    return bars

if __name__ == "__main__":
    path = sys.argv[1]
    min_s = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    print("clip", path)
    fails = 0
    for name, v, bar in gate(path, min_s):
        ok = v <= bar
        fails += (not ok)
        print("%s %.3f bar %.3f %s" % (name, v, bar, "PASS" if ok else "FAIL"))
    print("GATE:", "PASS" if fails == 0 else "FAIL (%d bars)" % fails)
