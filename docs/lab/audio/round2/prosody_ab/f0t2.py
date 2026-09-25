import wave, numpy as np
w = wave.open('clipA.wav')
d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
w.close()
sr = 44100
n, hop = 1102, 441
idx = np.arange(n)[None, :] + hop * np.arange((len(d) - n) // hop + 1)[:, None]
xf = d[idx]
xw = (xf - xf.mean(axis=1, keepdims=True)) * np.hanning(n)
N = 2048
S = np.abs(np.fft.rfft(xw, N)) ** 2
r = np.fft.irfft(S, N)[:, :n]
rn = r / (r[:, 0:1] + 1e-12)
lmin, lmax = 36, 551
seg = rn[:, lmin:lmax + 1]
pk = seg.argmax(axis=1)
ar = np.arange(len(seg))
pkm = np.clip(pk - 1, 0, seg.shape[1] - 1)
pkp = np.clip(pk + 1, 0, seg.shape[1] - 1)
a = seg[ar, pkm]; b = seg[ar, pk]; c = seg[ar, pkp]
den = a - 2 * b + c
shift = np.where(np.abs(den) > 1e-12, 0.5 * (a - c) / den, 0.0)
lag = lmin + pk.astype(float) + shift
f0 = sr / lag
for lo, hi, name in ((0.1, 0.5, 'note1-440'), (0.7, 1.0, 'note2-494')):
    s = f0[int(lo*100):int(hi*100)]
    print(name, 'mean', round(float(s.mean()), 2), 'std', round(float(s.std()), 3))
