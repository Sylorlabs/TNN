import wave, numpy as np
for f in ('clipA.wav', 'clipB.wav'):
    w = wave.open(f); d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float); w.close()
    print(f, 'peak', int(np.abs(d).max()), 'rms', int(np.sqrt((d**2).mean())))
