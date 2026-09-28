#!/usr/bin/env python3
"""Dither-stability spot check (prereg 5.3): deterministic x1.001 gain on the 20
run-1 iter0 renders -> re-run the native organ -> stability = same env class AND
|dF0|/F0 <= 0.5%. Need >= 19/20. Deterministic."""
import json, os, subprocess, struct, wave

HERE = os.path.dirname(os.path.abspath(__file__))
CREW = os.path.dirname(HERE)
MAN = json.load(open(os.path.join(CREW, "manifests", "intent_manifest.json")))
ORGAN = os.path.join(CREW, "build", "organ")
EV = os.path.join(CREW, "evidence")
DD = os.path.join(EV, "dither")

def organ_measure(path):
    p = subprocess.run([ORGAN, "measure", path], capture_output=True, text=True, timeout=300)
    d = {}
    for tok in p.stdout.split():
        k, v = tok.split("=")
        d[k] = v
    return {"f0_mhz": int(d["f0_mhz"]), "env": int(d["env"])}

def apply_gain(src, dst, g=1.001):
    w = wave.open(src, 'rb')
    fr = w.readframes(w.getnframes())
    params = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes(),
              w.getcomptype(), w.getcompname())
    w.close()
    s = struct.unpack('<%dh' % (len(fr) // 2), fr)
    o = [max(-32768, min(32767, int(round(v * g)))) for v in s]
    w = wave.open(dst, 'wb')
    w.setnchannels(params[0]); w.setsampwidth(params[1]); w.setframerate(params[2])
    w.writeframes(struct.pack('<%dh' % len(o), *o))
    w.close()

def main():
    os.makedirs(DD, exist_ok=True)
    stable = 0
    rows = []
    for c in MAN:
        cid = c["case_id"]
        src = os.path.join(EV, "run1", cid, "%s_iter0.wav" % cid)
        dst = os.path.join(DD, "%s_x1001.wav" % cid)
        apply_gain(src, dst)
        a = organ_measure(src)
        b = organ_measure(dst)
        df = abs(b["f0_mhz"] - a["f0_mhz"]) / max(a["f0_mhz"], 1)
        ok = (a["env"] == b["env"]) and df <= 0.005
        stable += 1 if ok else 0
        rows.append({"case": cid, "f0_orig": a["f0_mhz"], "f0_dith": b["f0_mhz"],
                     "env_orig": a["env"], "env_dith": b["env"], "stable": ok})
        print(cid, "f0 %d -> %d" % (a["f0_mhz"], b["f0_mhz"]),
              "env %d -> %d" % (a["env"], b["env"]), "OK" if ok else "FLIP")
    json.dump({"stable": stable, "n": len(rows), "pass": stable >= 19, "rows": rows},
              open(os.path.join(EV, "dither.json"), "w"), indent=2)
    print("dither stability: %d/%d (need >=19)" % (stable, len(rows)))

if __name__ == "__main__":
    main()
