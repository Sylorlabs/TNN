import wave, numpy as np, sys
sys.path.insert(0, '../shared')
from analyze import frame, autocorr_period
f = 'clipA.wav'
w = wave.open(f); d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float); w.close()
sr = 44100
xf = frame(d)
f0, per = autocorr_period(xf, sr, 80, 1200)
# print F0 track for note 2 (0.6-1.1s) and note 1
for lo, hi, name in ((0.1, 0.5, 'note1-440'), (0.7, 1.0, 'note2-494')):
    a, b = int(lo*100), int(hi*100)
    seg = f0[a:b]
    print(name, 'mean', round(seg.mean(), 2), 'std', round(seg.std(), 3),
          'min', round(seg.min(), 1), 'max', round(seg.max(), 1))
    # show first 10
    print('  ', np.round(seg[:10], 1))
