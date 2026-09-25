#!/usr/bin/env python3
"""Generate 10 FROZEN reference WAVs for the Crew L organ self-check (prereg 3.5).
Deterministic closed-form synthesis; LCG (fixed seed) for the noise file.
No RNG module used anywhere."""
import wave, math, struct, hashlib, json, os

SR = 44100
DUR = 2.0
N = int(SR * DUR)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ref_wavs")

def lcg_noise(n, seed=20260925):
    x = seed
    out = []
    for _ in range(n):
        x = (1103515245 * x + 12345) % 2147483648
        out.append((x / 1073741824.0) - 1.0)  # [-1, 1)
    return out

def write_wav(path, samples):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(struct.pack('<%dh' % len(samples), *samples))

def fade(s, nf=220):
    s = list(s)
    for t in range(nf):
        m = 0.5 - 0.5 * math.cos(math.pi * t / nf)
        s[t] = int(s[t] * m); s[N - 1 - t] = int(s[N - 1 - t] * m)
    return s

def tone(f, env, amp=15000, vibrato=None, tremolo=None, noise_db=None, second=None):
    s = []
    nz = lcg_noise(N) if noise_db else None
    nscale = 10 ** (noise_db / 20.0) if noise_db else 0.0
    for t in range(N):
        fr = t / N
        if env == "flat": e = 1.0
        elif env == "rise": e = 0.05 + 0.85 * fr
        else: e = 0.9 - 0.85 * fr
        f_inst = f
        if vibrato:
            # exact FM phase: f(t)=f*(1+d*sin(2π fm t/SR))
            ph = 2 * math.pi * f * t / SR - (f * vibrato[0] / vibrato[1]) * \
                 math.cos(2 * math.pi * vibrato[1] * t / SR)
        else:
            ph = 2 * math.pi * f * t / SR
        v = amp * e * math.cos(ph)
        if tremolo:
            v *= 10 ** ((tremolo[0] * math.sin(2 * math.pi * tremolo[1] * t / SR)) / 20.0)
        if second:
            v += amp * 0.8 * e * math.cos(2 * math.pi * second * t / SR)
        if nz:
            v += amp * nscale * nz[t]
        v = max(-32768, min(32767, int(round(v))))
        s.append(v)
    return fade(s)

specs = [
    ("ref01_110_flat",      dict(f=110.0, env="flat")),
    ("ref02_220_rise",      dict(f=220.0, env="rise")),
    ("ref03_440_decay",     dict(f=440.0, env="decay")),
    ("ref04_880_flat",      dict(f=880.0, env="flat")),
    ("ref05_82d41_decay",   dict(f=82.41, env="decay")),
    ("ref06_1174d66_rise",  dict(f=1174.66, env="rise")),
    ("ref07_329d63_vib",    dict(f=329.63, env="flat", vibrato=(0.02, 5.0))),
    ("ref08_220_330_two",   dict(f=220.0, env="flat", second=329.63)),
    ("ref09_440_noisy",     dict(f=440.0, env="decay", noise_db=-20.0)),
    ("ref10_155d56_trem",   dict(f=155.56, env="flat", tremolo=(3.0, 4.0))),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    man = []
    for name, kw in specs:
        s = tone(**kw)
        path = os.path.join(OUT, name + ".wav")
        write_wav(path, s)
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        man.append({"name": name + ".wav", "sha256": h, "params": kw})
        print(name, h[:16])
    mp = os.path.join(os.path.dirname(OUT), "manifests", "ref_manifest.json")
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(man, open(mp, "w"), indent=2)
    print("wrote", mp)

if __name__ == "__main__":
    main()
