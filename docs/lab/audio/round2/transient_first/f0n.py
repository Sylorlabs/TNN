import wave, numpy as np
w = wave.open('pluck_full.wav')
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
seg = rn[:, 36:552]
pk = seg.argmax(axis=1)
f0 = sr / (36 + pk)
# note 0 (C5 523Hz), 0.1-0.9s
s = f0[10:90]
print('note0 F0 mean', round(float(s.mean()),1), 'std', round(float(s.std()),2))
print('first 10:', np.round(s[:10],0))
print('last 10:', np.round(s[-10:],0))
