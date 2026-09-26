#!/usr/bin/env python3
"""P-R1: apply +1 dB gain to the 20 perturbation questions per subtest.

Reads manifest_p.json pr1 qids. Writes perturbed WAVs to test_wavs_pert/.
+1 dB = multiply by 10^(1/20) = 1.1220184543. Clips at int16 (deterministic).
"""
import json, os, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
G = 10 ** (1.0 / 20.0)

man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
os.makedirs(os.path.join(HERE, 'test_wavs_pert'), exist_ok=True)

for name, qids in man['pr1']['qids'].items():
    for qid in qids:
        for suffix in (['_A.wav', '_B.wav'] if name in ('pitchrel', 'rhy', 'hf')
                       else ['.wav']):
            src = os.path.join(HERE, 'test_wavs', qid + suffix)
            w = wave.open(src, 'rb')
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
            w.close()
            y = np.clip(np.round(x * G), -32768, 32767).astype(np.int16)
            dst = os.path.join(HERE, 'test_wavs_pert', qid + suffix)
            ww = wave.open(dst, 'wb')
            ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(44100)
            ww.writeframes(y.tobytes()); ww.close()
print('perturbed WAVs written')
