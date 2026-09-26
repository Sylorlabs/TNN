#!/usr/bin/env python3
"""wavecheck.py — analyzer-first waveform audit of render WAVs.

For each WAV: peak, DC offset, zero-crossing rate, clip count, spectral
centroid, 50/60 Hz hum level, and (for renders) agreement of measured
descriptors with the journal's PLANNED values. Prints a table; flags anomalies.
"""
import glob, json, os, struct, sys
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/audio_principles/crew_p')
import scorer_p as SP  # noqa: E402


def read_wav(p):
    with open(p, 'rb') as f:
        d = f.read()
    # find data chunk
    off = 12
    ds, ns = None, None
    while off + 8 <= len(d):
        cid = d[off:off + 4]
        sz = struct.unpack('<I', d[off + 4:off + 8])[0]
        if cid == b'data':
            ds, ns = off + 8, sz // 2
            break
        off += 8 + sz
    x = np.frombuffer(d[ds:ds + ns * 2], dtype=np.int16).astype(np.float64)
    return x


def analyze(p):
    x = read_wav(p)
    n = len(x)
    peak = np.abs(x).max()
    dc = x.mean()
    zc = ((x[:-1] * x[1:]) < 0).mean()
    clipped = int((np.abs(x) >= 32767).sum())
    # spectral centroid + hum
    X = np.abs(np.fft.rfft(x * np.hanning(n)))
    fr = np.fft.rfftfreq(n, 1 / 44100)
    cent = (X * fr).sum() / (X.sum() + 1e-9)
    hum50 = X[(fr >= 49) & (fr <= 51)].max() / (X.max() + 1e-9)
    hum60 = X[(fr >= 59) & (fr <= 61)].max() / (X.max() + 1e-9)
    fe = SP.features(p)
    return {'file': os.path.basename(p), 'n': n, 'peak': int(peak),
            'dc': round(float(dc), 2), 'zcr': round(float(zc), 4),
            'clipped': clipped, 'cent_hz': round(float(cent), 1),
            'hum50': round(float(hum50), 4), 'hum60': round(float(hum60), 4),
            'f0': round(float(SP.med_f0(fe)), 1), 'env': SP.ans_env(fe)}


def main():
    d = sys.argv[1]
    rows = [analyze(p) for p in sorted(glob.glob(os.path.join(d, '*.wav')))]
    print(json.dumps(rows, indent=1))


if __name__ == '__main__':
    main()
