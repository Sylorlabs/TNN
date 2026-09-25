import wave, numpy as np
w = wave.open('pluck_full.wav')
d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
w.close()
sr = 44100
# spectrum of first note (steady part, 0.2-0.4s)
seg = d[int(0.2*sr):int(0.4*sr)] * np.hanning(int(0.2*sr))
S = np.abs(np.fft.rfft(seg, 16384))
fr = np.fft.rfftfreq(16384, 1/sr)
# find peaks
for f in (523, 1046, 1569, 2093):
    idx = int(f * 16384 / sr)
    print(f, 'Hz:', int(S[idx-2:idx+3].max()))
# check F0 via autocorr on clean segment
seg2 = d[int(0.2*sr):int(0.3*sr)]; seg2 = seg2 - seg2.mean()
r = np.correlate(seg2, seg2, 'full'); r = r[len(seg2)-1:]; r = r/(r[0]+1e-12)
for lag in range(80, 90):
    print('lag', lag, 'F0', round(sr/lag, 1), 'r', round(r[lag], 3))
