import wave, numpy as np, sys
f = sys.argv[1] if len(sys.argv) > 1 else 'clipA.wav'
w = wave.open(f); d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float); w.close()
sr = 44100
# note 2 (static 494 Hz in A), steady middle
seg = d[int(0.75*sr):int(0.95*sr)]; seg = seg - seg.mean()
r = np.correlate(seg, seg, 'full'); r = r[len(seg)-1:]; r = r / (r[0] + 1e-12)
lo, hi = 36, 551
p = lo + int(np.argmax(r[lo:hi]))
print('best lag', p, 'F0', round(sr/p, 2), 'r', round(r[p], 4))
for L in range(max(lo, p-4), min(hi, p+5)):
    print('  lag', L, 'F0', round(sr/L, 1), 'r', round(r[L], 4))
