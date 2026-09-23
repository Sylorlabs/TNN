#!/usr/bin/env python3
"""HIFI-PREREG verification (harness-only, numpy): H2 headers, H3 no-clip,
H4 spectrum (correct 12-TET tuning), H5 bipolarity (sign-extension fix).
Usage: verify_hifi.py <dir-with-wavs>"""
import wave, struct, sys, os
import numpy as np

fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" " + detail if detail else ""))
    if not cond: fails.append(name)

def load(fn):
    w = wave.open(fn, 'rb')
    p = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes())
    n = w.getnframes(); raw = w.readframes(n); w.close()
    return p, np.array(struct.unpack('<%dh' % n, raw), dtype=np.float64)/32768.0

d = sys.argv[1]
files = ["f3song_hifi.wav", "f3mood_happy.wav", "f3mood_scary.wav", "f3mood_calm.wav"]
samps = {}
for fn in files:
    (ch, sw, sr, nf), s = load(os.path.join(d, fn))
    samps[fn] = (sr, s)
    check(f"H2 {fn} header 44100/16/mono", ch == 1 and sw == 2 and sr == 44100,
          f"frames={nf}")
    rail = int(np.sum(np.abs(s) >= 32767/32768.0))
    peak = float(np.max(np.abs(s)))
    check(f"H3 {fn} no-clip headroom", rail == 0 and peak <= 24001/32768.0,
          f"rail={rail} peak={peak*32768:.0f}")
    neg = int(np.sum(s < -0.001))
    check(f"H5 {fn} bipolar (sign fix)", neg > 1000, f"negative_samples={neg}")
    dc = abs(float(np.mean(s)))
    check(f"H5b {fn} no DC offset", dc < 0.05, f"mean={dc:.4f}")

# H4a: correct 12-TET tuning. Song frames 8-11: bass F4=349.23 (bin20),
# melody E5=659.26 (bin31); pad C4=261.63 (bin15) throughout.
BINHZ = {b: 110.0*2**(b/12.0) for b in range(48)}
def topfreqs(s, sr, start, nframes=4, n=8):
    seg = s[start:start+nframes*2756]
    seg = seg - np.mean(seg)
    spec = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
    freqs = np.fft.rfftfreq(len(seg), 1/sr)
    return sorted([float(freqs[i]) for i in np.argsort(spec)[-n:]])

sr, song = samps["f3song_hifi.wav"]
tf = topfreqs(song, sr, 8*2756)
want = [BINHZ[20], BINHZ[31], BINHZ[15]]
hit = sum(1 for w in want if any(abs(f-w) < 3.0 for f in tf))
print("   song frames8-11 top freqs:", [round(f) for f in tf])
check("H4a song correct 12-TET tuning", hit == 3, f"{hit}/3 of F4/E5-melody/C4-pad")

# H4b: peak prominence (no mud) — voice peaks stand >=12 dB above local valleys
def prominence(s, sr, start, freqs_want):
    seg = s[start:start+sr] - np.mean(s[start:start+sr])
    spec = np.abs(np.fft.rfft(seg*np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1/sr)
    res = []
    for w in freqs_want:
        pi = int(np.argmin(np.abs(fr-w)))
        pk = np.max(spec[max(0,pi-2):pi+3])
        valley = np.median(spec[max(0,pi-25):pi-8])
        res.append(20*np.log10(pk/max(valley,1e-9)))
    return res
pr = prominence(song, sr, 8*2756, [BINHZ[20], BINHZ[31]])
print("   prominences dB:", [round(p,1) for p in pr])
check("H4b voice separation (prominence>=12dB)", all(p >= 12 for p in pr))

# H4c: no 16 Hz frame-rate zipper sideband in hifi (compare legacy 8k)
def zipper(s, sr):
    hop = sr//200
    env = np.array([np.sqrt(np.mean(s[i:i+hop]**2)) for i in range(0, len(s)-hop, hop)])
    env = env - np.mean(env)
    N = 2048; e = np.zeros(N); e[:min(N,len(env))] = env[:N]
    mags = np.abs(np.fft.rfft(e)); hz = np.fft.rfftfreq(N, 1/200)
    sig = np.sum(mags[(hz>=14)&(hz<=18)]**2)
    ref = np.sum(mags[((hz>=8)&(hz<=12))|((hz>=20)&(hz<=26))]**2)
    return sig/max(ref,1e-18)
for fn in files:
    sr0, s0 = samps[fn]
    z = zipper(s0, sr0)
    check(f"H4c {fn} no 16Hz zipper", z < 1.0, f"16Hz/neib={z:.2f}")
old = "/home/hatch/workspace/your_files/imagination_video/f3song.wav"
if os.path.exists(old):
    ( _, _, sr0, _), s0 = load(old)
    print(f"   INFO legacy 8kHz f3song 16Hz/neib={zipper(s0, sr0):.2f}")

print("RESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}")
sys.exit(1 if fails else 0)
