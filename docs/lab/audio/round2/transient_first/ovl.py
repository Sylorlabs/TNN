import wave, numpy as np
w = wave.open('pluck_full.wav')
d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
w.close()
sr = 44100
# check amplitude at note boundaries (overlap?)
for t in (0.45, 0.5, 0.55, 0.95, 1.0, 1.05):
    seg = d[int(t*sr):int(t*sr)+4410]
    print(t, 'rms', int(np.sqrt((seg**2).mean())))
# F0 track around note 1->2 transition
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
print('F0 0.3-0.7s:', np.round(f0[30:70:5], 0))
